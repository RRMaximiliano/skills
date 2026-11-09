---
name: zotero-import
description: Import downloaded PDFs into the local Zotero library. Check for duplicates, file each into a collection the user confirms, then offer to trash the downloads.
---

# Zotero Import

All Zotero access goes through `scripts/zotero.py`. It reads a copy of `zotero.sqlite` and writes only through the local connector. Never touch `zotero.sqlite` directly. Type the full command each time, `python3 -I <skill-dir>/scripts/zotero.py <command>`, with no shell variable. If it cannot connect, ask the user to open Zotero.

## Workflow

1. **Find.** Use the given paths, or `ls -lt ~/Downloads/*.pdf | head` and confirm which files.
2. **Read.** `pdftotext -l 2 "<file>" - | head -80` for title, authors, year, DOI. Ignore `pdfinfo`.
3. **Deduplicate.** `search --title "<title>" [--doi <doi>]`. A DOI hit or similarity ≥ 0.9 means it is already in the library: report its collections and skip it unless asked. `Author - Year - Title.pdf` names are often Zotero exports.
4. **Choose.** `collections` lists ids (`C3`); `peek C<n>` shows recent titles. Use `PhD` course folders only for course readings.
5. **Confirm.** Never import unconfirmed. Ask one AskUserQuestion per PDF (max 4 per call): short title, one-line summary, 2–3 collections with reasons (best marked "(Recommended)"), and "Skip".
6. **Import** one at a time: `import "<file>" --collection C<n>`.
7. **Report** a table of title, collection, status. `ok: false`: say where it landed. `recognized: false`: suggest "Retrieve Metadata for PDF". For `missing_fields` or a wrong item type, give the correct values from the PDF; the connector cannot edit items.
8. **Clean up.** Ask one multi-select AskUserQuestion, "Move these downloaded PDFs to the Trash?", offering only files with `stored: true` or skipped as duplicates. Trash the selected files with `trash "<file>"`, never `rm`.
