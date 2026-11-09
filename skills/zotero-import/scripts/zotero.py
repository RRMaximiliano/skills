#!/usr/bin/env python3
"""Helper for the zotero-import skill.

Talks only to the local Zotero desktop app:
  - reads a *copy* of zotero.sqlite (never the live file) for collections and duplicate checks
  - writes through Zotero's connector endpoints on localhost:23119 (what "Save to Zotero" uses)

Commands:
  collections                         collection tree with connector ids (C<n>) and item counts
  peek C<n> [--limit N]               recent item titles in one collection (to judge fit)
  search --title "..." [--doi ...]    look for duplicates already in the library
  import PDF --collection C<n>        save PDF into that collection and let Zotero fetch metadata
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


def select_url(con, target):
    if not target.startswith("C"):
        sys.exit("ERROR: --collection must be a collection id like C3 (from `collections`).")
    r = con.execute("select key, libraryID from collections where collectionID=?", (int(target[1:]),)).fetchone()
    if not r:
        sys.exit(f"ERROR: no collection {target}")
    key, lib = r
    g = con.execute("select groupID from groups where libraryID=?", (lib,)).fetchone()
    return (f"zotero://select/groups/{g[0]}/collections/{key}" if g
            else f"zotero://select/library/collections/{key}")


def cmd_import(a):
    pdf = Path(a.pdf).expanduser().resolve()
    if not pdf.is_file() or pdf.suffix.lower() != ".pdf":
        sys.exit(f"ERROR: not a PDF file: {pdf}")
    ensure_running()
    target_id = int(a.collection.lstrip("C"))

    # 1. make the target collection the selected one, so the save lands there
    subprocess.run(["open", "-g", select_url(db(), a.collection)])
    for _ in range(20):
        d = selected()
        if d.get("id") == target_id and d.get("name") != d.get("libraryName"):
            break
        time.sleep(0.5)
    else:
        sys.exit(f"ERROR: could not select {a.collection} in Zotero (selected: {d.get('name')}). Nothing imported.")
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
    item = summary(con, parent_id or att_id)
    want = d["name"]
    missing = [k for k in ("year", "publication", "DOI") if not item.get(k)]
    att_key = con.execute("select key from items where itemID=?", (att_id,)).fetchone()[0]
    print(json.dumps({
        "ok": want in item["collections"],
        "target_collection": want,
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
    q = sp.add_parser("import"); q.add_argument("pdf"); q.add_argument("--collection", required=True); q.add_argument("--title")
    a = p.parse_args()
    {"collections": cmd_collections, "peek": cmd_peek, "search": cmd_search, "import": cmd_import}[a.cmd](a)


if __name__ == "__main__":
    main()
