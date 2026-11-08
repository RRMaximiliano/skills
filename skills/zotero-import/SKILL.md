---
name: zotero-import
description: Import downloaded PDFs into the user's local Zotero library, filed into the right collection after the user confirms, then offer to move the downloaded copies to the Trash. Use when the user points at new/downloaded PDFs (e.g. "import the new PDFs in Downloads", "add this paper to Zotero", "file these in Zotero"), asks which Zotero collection a paper belongs in, or asks whether a paper is already in their library.
---

# Zotero import

Files new PDFs into the user's Zotero 10 desktop library. Everything goes through
`scripts/zotero.py` in this skill's folder. It reads a **copy** of `~/Zotero/zotero.sqlite` and
writes **only** through Zotero's local connector (`localhost:23119`, the same channel as the
browser "Save to Zotero" button). Never write to `zotero.sqlite` directly. Zotero must be
running; the script opens it if needed.

Run the script as `python3 -I <skill-dir>/scripts/zotero.py <command>`, where `<skill-dir>` is the
folder containing this file (e.g. `~/.claude/skills/zotero-import`). It is written `zotero.py
<command>` below. Always type the full command; do not store it in a shell variable (zsh will
not split it).

## Workflow

1. **Find the PDFs.** Use the paths the user gave. If they said "new downloads", list
   `ls -lt ~/Downloads/*.pdf | head` and confirm which ones they mean if it's ambiguous.
   Many files already named `Author - Year - Title.pdf` were exported *from* Zotero, so the duplicate check matters.

2. **Read each PDF.** Run `pdftotext -l 2 "<file>" - | head -80` to get title, authors, year, abstract and DOI.
   (`pdfinfo` metadata is often junk like "Microsoft Word - draft.doc"; trust the text.)

3. **Check for duplicates:** `zotero.py search --title "<title>" [--doi <doi>]`. If there is a match (similarity ≥ 0.9 or a
   DOI hit), tell the user it is already in the library and which collections it is in. Do not import it
   unless they ask. If they want it in another collection, tell them to add it there by hand.

4. **Get the collection tree:** `zotero.py collections` (ids look like `C3`; `L2` is a group library).
   If the right home isn't obvious, `zotero.py peek C<n>` shows recent titles in a candidate collection.
   Course folders under `PhD` (semesters, classes) are for course readings. Only suggest them when the
   paper clearly is one.

5. **Propose and confirm. Never import without explicit confirmation.** Use AskUserQuestion with one
   question per PDF (max 4 per call). Put the short title in the question and a one-line summary of the paper.
   Offer 2–3 candidate collections, best first and marked "(Recommended)", each with a reason,
   plus a "Skip" option. The user can type another collection via "Other".
   Each import files the item into **one** collection.

6. **Import** each confirmed PDF, one at a time:
   `zotero.py import "<file>" --collection C<n>`
   The JSON result has `ok` (it landed in the target collection), `recognized` (Zotero created a
   parent item with metadata), the `item`, and `missing_fields`. Zotero copies the PDF into
   `~/Zotero/storage`, so the downloaded file is no longer needed once `ok` is true.

7. **Report** in a short table: title, collection, status. Flag problems plainly:
   - `ok: false`: say where it went and tell the user to move it.
   - `recognized: false`: it was saved as a standalone PDF. The user can right-click → "Retrieve Metadata for PDF"
     or "Create Parent Item".
   - Missing year, publication, or a wrong item type (e.g. a working paper saved as a journal article): list
     the correct values you read from the PDF so the user can fix them in Zotero. The connector cannot
     edit existing items.

8. **Offer to clean up the downloads.** Ask with one multi-select AskUserQuestion: "Move these
   downloaded PDFs to the Trash?". List each eligible file, by short title, as an option:
   - files whose import returned `ok: true`. A Zotero copy now exists; check
     `~/Zotero/storage/<attachment_key>/` holds a PDF before offering it.
   - files skipped because step 3 found them already in the library (say so in the option description).
   Do not offer files that failed to import or that the user skipped. Move only the files the user
   selects, with macOS `trash "<file>"` (recoverable from the Trash). Never use `rm`. If the user
   selects none, leave everything in place.

## Notes
- The import changes which collection is selected in Zotero's window (it selects the target collection). That is expected.
- If `collections` fails with a connection error, ask the user to open Zotero.
