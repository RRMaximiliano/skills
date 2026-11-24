---
name: zotero-import
description: Import downloaded PDFs into the local Zotero library. Check for duplicates, file each into one or more collections the user confirms, then offer to trash the downloads.
---

# Zotero Import

All Zotero access goes through `scripts/zotero.py`. It reads a copy of `zotero.sqlite` and writes only through Zotero's own endpoints: the connector for saving PDFs, and the local API for adding an item to more collections. Never touch `zotero.sqlite` directly. Type the full command each time, `python3 -I <skill-dir>/scripts/zotero.py <command>`, with no shell variable. If it cannot connect, ask the user to open Zotero.

## Workflow

1. **Find.** Use the given paths, or `ls -lt ~/Downloads/*.pdf | head` and confirm which files.
2. **Read.** `pdftotext -l 2 "<file>" - | head -80` for title, authors, year, DOI. Ignore `pdfinfo`.
3. **Deduplicate.** `search --title "<title>" [--doi <doi>]`. A DOI hit or similarity ≥ 0.9 means it is already in the library: report its collections and skip it unless asked. To file an existing item in more collections, use `add <item key> --collection C<n> [C<m> ...]`. `Author - Year - Title.pdf` names are often Zotero exports.
4. **Choose.** `collections` lists ids (`C3`); `peek C<n>` shows recent titles. Use `PhD` course folders only for course readings.
5. **Confirm.** Never import unconfirmed. Ask one multi-select AskUserQuestion per PDF (max 4 per call): short title, one-line summary, 2–3 collections with reasons (best marked "(Recommended)"), and "Skip". Say in the question that several collections can be picked. If "Skip" is picked, skip the PDF.
6. **Import** one at a time: `import "<file>" --collection C<n> [C<m> ...]`. The PDF is saved into the first collection, and the item is then added to the others. Put the recommended collection first.
7. **Report** a table of title, collections, status. `ok: false`: name the `missing_collections` and where the item did land. If `collection_error` says the local API is off, ask the user to turn on Zotero → Settings → Advanced → "Allow other applications on this computer to communicate with Zotero", then run `add` for the missing collections. The first `add` or multi-collection import shows an authorization prompt in Zotero; ask the user to click "Always Allow". `recognized: false`: suggest "Retrieve Metadata for PDF". For `missing_fields` or a wrong item type, give the correct values from the PDF; the script does not edit item metadata.
8. **Clean up.** Ask one multi-select AskUserQuestion, "Move these downloaded PDFs to the Trash?", offering only files with `stored: true` or skipped as duplicates. Trash the selected files with the macOS command `/usr/bin/trash "<file>"`, never `rm`. `zotero.py` has no trash command.
