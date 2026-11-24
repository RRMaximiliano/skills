#!/usr/bin/env python3
"""Helper for the zotero-import skill.

Talks only to the local Zotero desktop app:
  - reads a *copy* of zotero.sqlite (never the live file) for collections and duplicate checks
  - writes through Zotero's connector endpoints on localhost:23119 (what "Save to Zotero" uses)
  - adds items to extra collections through Zotero's local API (/api/), which must be enabled in
    Settings → Advanced and authorized once; the key is kept in KEY_FILE

Commands:
  collections                              collection tree with connector ids (C<n>) and item counts
  peek C<n> [--limit N]                    recent item titles in one collection (to judge fit)
  search --title "..." [--doi ...]         look for duplicates already in the library
  import PDF --collection C<n> [C<m> ...]  save PDF into the first collection, let Zotero fetch
                                           metadata, then add the item to the other collections
  add ITEMKEY --collection C<n> [C<m> ...] add an existing item to more collections
"""
import argparse
import atexit
import difflib
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
import unicodedata
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

BASE = "http://localhost:23119"
DATA_DIR = Path(os.environ.get("ZOTERO_DATA_DIR", str(Path.home() / "Zotero")))
SKIP_TYPES = "('attachment','note','annotation')"
KEY_FILE = Path.home() / "Library" / "Application Support" / "zotero-import" / "local-api-key"
APP_NAME = "zotero-import (Claude Code)"
ENABLE_HINT = ("Zotero's local API is off. Turn on Zotero → Settings → Advanced → "
               "\"Allow other applications on this computer to communicate with Zotero\", "
               "then run `add <item key> --collection ...` for the missing collections.")


# ---------- Zotero connection ----------

def post(path, body=None, data=None, headers=None, timeout=30):
    h = {"Content-Type": "application/json"}
    if headers:
        h.update(headers)
    payload = data if data is not None else json.dumps(body or {}).encode()
    req = urllib.request.Request(BASE + path, data=payload, headers=h, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read()
        return r.status, (json.loads(raw) if raw.strip() else None)


def ensure_running():
    for i in range(30):
        try:
            urllib.request.urlopen(BASE + "/connector/ping", timeout=2)
            return
        except Exception:
            if i == 0:
                subprocess.run(["open", "-g", "-a", "Zotero"])
            time.sleep(2)
    sys.exit("ERROR: Zotero is not responding on localhost:23119. Open Zotero and retry.")


def selected():
    return post("/connector/getSelectedCollection")[1]


# ---------- local API (for edits the connector cannot make) ----------

class LocalAPIError(Exception):
    pass


def api(method, path, body=None, headers=None, timeout=30):
    """Call the local API; return (status, headers, text) without raising on HTTP errors."""
    data = json.dumps(body).encode() if body is not None else None
    h = {"Content-Type": "application/json"} if data is not None else {}
    h.update(headers or {})
    req = urllib.request.Request(BASE + path, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.headers, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.headers, e.read().decode(errors="replace")


def api_key(renew=False):
    if KEY_FILE.exists() and not renew:
        return KEY_FILE.read_text().strip()
    print("Waiting for you to click \"Always Allow\" in Zotero…", file=sys.stderr)
    status, _, text = api("POST", "/api/local/authorize", {"appName": APP_NAME}, timeout=600)
    if status != 200:
        raise LocalAPIError(f"Zotero did not authorize {APP_NAME} (HTTP {status}: {text[:200]})")
    d = json.loads(text)
    if d.get("remember"):
        KEY_FILE.parent.mkdir(parents=True, exist_ok=True)
        fd = os.open(KEY_FILE, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w") as f:
            f.write(d["key"])
    return d["key"]


def add_to_collections(prefix, item_key, coll_keys):
    """Add the item to each collection key, keeping the collections it already has."""
    status, h, text = api("GET", f"/api/{prefix}/items/{item_key}")
    if status == 403 and "not enabled" in text:
        raise LocalAPIError(ENABLE_HINT)
    if status != 200:
        raise LocalAPIError(f"could not read item {item_key} (HTTP {status}: {text[:200]})")
    j = json.loads(text)
    current = j["data"].get("collections", [])
    wanted = current + [k for k in coll_keys if k not in current]
    if wanted == current:
        return
    renew = False
    for _ in range(2):
        status, _, text = api("PATCH", f"/api/{prefix}/items/{item_key}", {"collections": wanted}, {
            "Zotero-API-Key": api_key(renew),
            "Zotero-Server-ID": h["Zotero-Server-ID"],
            "If-Unmodified-Since-Version": str(j["version"]),
        })
        if status != 401:
            break
        KEY_FILE.unlink(missing_ok=True)  # key revoked or single-use: ask again once
        renew = True
    if status not in (200, 204):
        raise LocalAPIError(f"Zotero refused the collection change (HTTP {status}: {text[:200]})")


# ---------- read-only database snapshot ----------

def db():
    tmp = Path(tempfile.mkdtemp(prefix="zotero-snap-"))
    atexit.register(shutil.rmtree, tmp, True)
    for suf in ("", "-wal"):
        src = DATA_DIR / ("zotero.sqlite" + suf)
        if src.exists():
            shutil.copy2(src, tmp / ("zotero.sqlite" + suf))
    return sqlite3.connect(tmp / "zotero.sqlite")


def field(con, item_id, name):
    r = con.execute(
        """select v.value from itemData d join fields f using(fieldID)
           join itemDataValues v using(valueID) where d.itemID=? and f.fieldName=?""",
        (item_id, name)).fetchone()
    return r[0] if r else None


def summary(con, item_id):
    creators = [ln for (ln,) in con.execute(
        """select c.lastName from itemCreators ic join creators c using(creatorID)
           where ic.itemID=? order by ic.orderIndex""", (item_id,))]
    colls = [n for (n,) in con.execute(
        """select c.collectionName from collectionItems ci join collections c using(collectionID)
           where ci.itemID=?""", (item_id,))]
    key, typ = con.execute(
        "select i.key, t.typeName from items i join itemTypes t using(itemTypeID) where itemID=?",
        (item_id,)).fetchone()
    date = field(con, item_id, "date") or ""
    return {
        "key": key,
        "type": typ,
        "title": field(con, item_id, "title"),
        "authors": creators,
        "year": date[:4] or None,
        "publication": field(con, item_id, "publicationTitle"),
        "DOI": field(con, item_id, "DOI"),
        "collections": colls,
        "zotero_link": f"zotero://select/library/items/{key}",
    }


def norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return " ".join(re.sub(r"[^a-z0-9]+", " ", s).split())


# ---------- commands ----------

def cmd_collections(a):
    ensure_running()
    d = selected()
    con = db()
    counts = dict(con.execute("select collectionID, count(*) from collectionItems group by collectionID"))
    for t in d["targets"]:
        ind = "  " * t["level"]
        if t["id"].startswith("C"):
            print(f"{ind}{t['id']}  {t['name']}  ({counts.get(int(t['id'][1:]), 0)})")
        else:
            print(f"{ind}{t['id']}  [library: {t['name']}]")
    print(f"\nCurrently selected in Zotero: {d['name']}")


def cmd_peek(a):
    cid = int(a.collection.lstrip("C"))
    con = db()
    name = con.execute("select collectionName from collections where collectionID=?", (cid,)).fetchone()
    if not name:
        sys.exit(f"ERROR: no collection {a.collection}")
    print(f"{a.collection} {name[0]} — most recently added:")
    rows = con.execute(
        f"""select i.itemID from collectionItems ci join items i using(itemID)
            join itemTypes t using(itemTypeID)
            where ci.collectionID=? and t.typeName not in {SKIP_TYPES}
            and i.itemID not in (select itemID from deletedItems)
            order by i.dateAdded desc limit ?""", (cid, a.limit)).fetchall()
    for (iid,) in rows:
        s = summary(con, iid)
        au = s["authors"][0] if s["authors"] else "?"
        print(f"  - {au} ({s['year'] or 'n.d.'}): {s['title']}")
    subs = con.execute("select 'C'||collectionID, collectionName from collections where parentCollectionID=?", (cid,)).fetchall()
    if subs:
        print("  subcollections: " + ", ".join(f"{i} {n}" for i, n in subs))


def cmd_search(a):
    con = db()
    hits = {}
    if a.doi:
        d = a.doi.lower().strip()
        for (iid,) in con.execute(
                """select d.itemID from itemData d join fields f using(fieldID)
                   join itemDataValues v using(valueID)
                   where f.fieldName='DOI' and lower(trim(v.value))=?""", (d,)):
            hits[iid] = 1.0
    if a.title:
        q = norm(a.title)
        rows = con.execute(
            f"""select i.itemID, v.value from items i join itemTypes t using(itemTypeID)
                join itemData d using(itemID) join fields f using(fieldID)
                join itemDataValues v using(valueID)
                where f.fieldName='title'
                and (t.typeName not in {SKIP_TYPES}
                     or i.itemID in (select itemID from itemAttachments where parentItemID is null))
                and i.itemID not in (select itemID from deletedItems)""")
        for iid, title in rows:
            title = re.sub(r"^[A-Za-z0-9]{6}-", "", re.sub(r"\.pdf$", "", title or "", flags=re.I))
            sm = difflib.SequenceMatcher(None, q, norm(title))
            if sm.real_quick_ratio() < 0.7 or sm.quick_ratio() < 0.7:
                continue
            r = sm.ratio()
            if r >= 0.7:
                hits[iid] = max(hits.get(iid, 0), r)
    out = [dict(similarity=round(r, 2), **summary(con, iid))
           for iid, r in sorted(hits.items(), key=lambda x: -x[1])[:5]]
    print(json.dumps({"matches": out}, indent=1, ensure_ascii=False))


def resolve_collections(con, targets):
    """Validate C<n> ids (repeated or comma-separated) and return their details, in order."""
    ids = []
    for t in targets:
        for c in t.split(","):
            c = c.strip()
            if c and c not in ids:
                ids.append(c)
    out = []
    for c in ids:
        if not re.fullmatch(r"C\d+", c):
            sys.exit(f"ERROR: {c!r} is not a collection id like C3 (from `collections`).")
        r = con.execute("select collectionID, key, collectionName, libraryID from collections "
                        "where collectionID=?", (int(c[1:]),)).fetchone()
        if not r:
            sys.exit(f"ERROR: no collection {c}")
        cid, key, name, lib = r
        g = con.execute("select groupID from groups where libraryID=?", (lib,)).fetchone()
        out.append({"id": c, "num": cid, "key": key, "name": name, "library": lib,
                    "prefix": f"groups/{g[0]}" if g else "users/0",
                    "url": (f"zotero://select/groups/{g[0]}/collections/{key}" if g
                            else f"zotero://select/library/collections/{key}")})
    if len({c["library"] for c in out}) > 1:
        sys.exit("ERROR: all collections must be in the same library. Nothing changed.")
    return out


def add_extra(item_key, colls):
    """Add the item to colls; return an error message, or None on success."""
    if not colls:
        return None
    try:
        add_to_collections(colls[0]["prefix"], item_key, [c["key"] for c in colls])
    except LocalAPIError as e:
        return str(e)


def not_in(con, item_key, colls):
    """The collections in colls that the item is not in yet (by id: names repeat, e.g. "Class 1")."""
    have = {n for (n,) in con.execute(
        """select ci.collectionID from collectionItems ci join items i using(itemID)
           where i.key=? and i.libraryID=?""", (item_key, colls[0]["library"]))}
    return [c for c in colls if c["num"] not in have]


def collection_report(con, item_key, colls, error):
    iid = con.execute("select itemID from items where key=? and libraryID=?",
                      (item_key, colls[0]["library"])).fetchone()[0]
    item = summary(con, iid)
    missing = [c["id"] for c in not_in(con, item_key, colls)]
    rep = {"ok": not missing, "target_collections": [c["name"] for c in colls],
           "missing_collections": missing}
    if error:
        rep["collection_error"] = error
    return item, rep


def cmd_add(a):
    ensure_running()
    colls = resolve_collections(db(), a.collection)
    con = db()
    if not con.execute("select 1 from items where key=? and libraryID=?",
                       (a.item, colls[0]["library"])).fetchone():
        sys.exit(f"ERROR: no item {a.item} in the library that holds {colls[0]['id']}")
    error = add_extra(a.item, not_in(con, a.item, colls))
    item, rep = collection_report(db(), a.item, colls, error)
    print(json.dumps({**rep, "item": item}, indent=1, ensure_ascii=False))


def cmd_import(a):
    pdf = Path(a.pdf).expanduser().resolve()
    if not pdf.is_file() or pdf.suffix.lower() != ".pdf":
        sys.exit(f"ERROR: not a PDF file: {pdf}")
    ensure_running()
    colls = resolve_collections(db(), a.collection)
    first = colls[0]
    target_id = first["num"]

    # 1. make the first target collection the selected one, so the save lands there
    subprocess.run(["open", "-g", first["url"]])
    for _ in range(20):
        d = selected()
        if d.get("id") == target_id and d.get("name") != d.get("libraryName"):
            break
        time.sleep(0.5)
    else:
        sys.exit(f"ERROR: could not select {first['id']} in Zotero (selected: {d.get('name')}). Nothing imported.")
    if not d.get("filesEditable", True):
        sys.exit(f"ERROR: files are not editable in {d.get('name')}. Nothing imported.")

    # 2. save the PDF, then wait for Zotero's metadata recognition
    start = (datetime.now(timezone.utc) - timedelta(seconds=5)).strftime("%Y-%m-%d %H:%M:%S")
    sid = str(uuid.uuid4())
    meta = {"sessionID": sid, "title": a.title or pdf.stem, "url": pdf.as_uri()}
    try:
        _, res = post("/connector/saveStandaloneAttachment", data=pdf.read_bytes(),
                      headers={"Content-Type": "application/pdf", "X-Metadata": json.dumps(meta)},
                      timeout=180)
    except urllib.error.HTTPError as e:
        sys.exit(f"ERROR: Zotero refused the save: HTTP {e.code} {e.read()[:300]!r}")
    recognized = None
    if res and res.get("canRecognize"):
        try:
            _, recognized = post("/connector/getRecognizedItem", {"sessionID": sid}, timeout=180)
        except Exception as e:
            recognized = {"error": str(e)}

    # 3. verify from the database
    for _ in range(15):
        con = db()
        row = con.execute(
            """select i.itemID, a.parentItemID from items i join itemAttachments a using(itemID)
               where i.dateAdded >= ? order by i.itemID desc limit 1""", (start,)).fetchone()
        if row and (row[1] or not recognized):
            break
        time.sleep(1)
    if not row:
        sys.exit("ERROR: save reported success but the new attachment was not found in the database.")
    att_id, parent_id = row
    att_key = con.execute("select key from items where itemID=?", (att_id,)).fetchone()[0]
    item_key = con.execute("select key from items where itemID=?", (parent_id or att_id,)).fetchone()[0]

    # 4. add the top-level item to the remaining collections, then re-read
    error = add_extra(item_key, not_in(con, item_key, colls))
    item, rep = collection_report(db(), item_key, colls, error)
    missing = [k for k in ("year", "publication", "DOI") if not item.get(k)]
    print(json.dumps({
        **rep,
        "recognized": bool(parent_id),
        "stored": any((DATA_DIR / "storage" / att_key).glob("*.pdf")),
        "item": item,
        "attachment_key": att_key,
        "missing_fields": missing,
    }, indent=1, ensure_ascii=False))


def main():
    p = argparse.ArgumentParser()
    sp = p.add_subparsers(dest="cmd", required=True)
    sp.add_parser("collections")
    q = sp.add_parser("peek"); q.add_argument("collection"); q.add_argument("--limit", type=int, default=12)
    q = sp.add_parser("search"); q.add_argument("--title"); q.add_argument("--doi")
    q = sp.add_parser("import"); q.add_argument("pdf"); q.add_argument("--title")
    q.add_argument("--collection", required=True, nargs="+", action="extend")
    q = sp.add_parser("add"); q.add_argument("item")
    q.add_argument("--collection", required=True, nargs="+", action="extend")
    a = p.parse_args()
    {"collections": cmd_collections, "peek": cmd_peek, "search": cmd_search,
     "import": cmd_import, "add": cmd_add}[a.cmd](a)


if __name__ == "__main__":
    main()
