---
name: latex-article
description: Create, edit, and validate modular LaTeX economics articles with AER/natbib references, Stata/R table fragments, figures, appendices, and publication-style layout.
---

# LaTeX Article

Build complete, compilable economics-paper projects. Default to a new modular project; edit existing projects conservatively.

## Route the task

- For a new paper, verify that the destination does not exist, copy `assets/article-template/` into it with standard filesystem tools, then tailor the copied project. Never overwrite or merge into an existing destination implicitly.
- For an existing paper, inspect its class, engine, folders, bibliography, commands, and dirty state before editing. Preserve established structure and paths unless the user requests migration.
- For detailed float and numbering rules, read `references/article-conventions.md`.
- When a table must span pages, also read `references/optional-capabilities.md`; use its `longtable` pattern instead of forcing the standard float wrapper across pages.
- Treat `Tabs/*.tex` as generated Stata/R artifacts. Diagnose and fix the producing script by default; patch a generated fragment only when explicitly requested.

## Build a new project

1. Confirm the destination does not exist. Copy `assets/article-template/` recursively into the requested destination. Stop rather than deleting or overwriting an existing path.
2. Fill `metadata.tex`; keep `pdfauthor` derived from `\PaperAuthors`.
3. Write through `Sections/` and `Appendices/`. Never invent citations, findings, data descriptions, or identification claims. Prefer supplied bibliography entries and sources; research only when explicitly requested. Set `\paperhasreferencestrue` in `metadata.tex` when the paper uses citations.
4. Put supplied graphics in `Figs/` and complete `tabular` fragments in `Tabs/`. Do not prescribe or generate analytical figures unless the user explicitly asks for that separate work.
5. Use the exact canonical wrappers from `snippets.tex` or the conventions reference.
6. Keep optional packages such as `subcaption`, `rotating`, `longtable`, `threeparttablex`, `pdflscape`, `dcolumn`, `bm`, TikZ, PGFPlots, and theorem systems out of the preamble until needed. Load only the capabilities required by the paper.
7. Load `caption` with `skip=0pt`, retain zero caption skip in the table- and figure-specific `\captionsetup` calls, and keep the bundled `threeparttable` patch that removes its separate post-caption gap.

## Edit an existing project

- Preserve the existing class, engine, folder names, bibliography system, and visual style unless migration is requested.
- Use the canonical float patterns for newly added tables and figures when compatible.
- Do not rewrite unrelated preamble code merely because it differs from this skill's new-project defaults.
- Flag conflicts and fragile patterns; change them only when required for the requested work or a clean build.
- Preserve user changes and generated outputs.

## Citation and evidence policy

- Use `\citet{}` and `\citep{}` with existing BibTeX keys.
- Reuse supplied entries instead of replacing or duplicating them.
- Add a citation only after verifying the source and creating a valid entry.
- Leave a clear placeholder for unsupported claims rather than fabricating support.
- Use `Table~\ref{}`, `Figure~\ref{}`, `Section~\ref{}`, and `equation~\eqref{}`.

## Validate every deliverable

1. From the project directory, run `latexmk -pdf main.tex`.
2. Inspect `main.log` with `rg -n 'LaTeX Error|undefined|multiply defined|Overfull|Fatal error|Emergency stop' main.log`. Also inspect the terminal output when BibTeX or `latexmk` reports a failure.
3. Fail on undefined citations, references, duplicate labels, missing files, or LaTeX errors.
4. Treat overfull boxes as warnings: fix them when practical; otherwise report them precisely.
5. Render the PDF with Poppler, for example `pdftoppm -png -r 150 main.pdf /tmp/latex-article-qa/page`, and visually inspect the title page, representative prose, every table or figure page changed, references, and appendix transitions. Check clipping, tiny text, caption alignment, note justification, page numbering, and float numbering.
6. Do not claim completion from source inspection alone.

## Defaults that may be overridden

- `11pt`, `letterpaper`, Palatino via `mathpazo`, one-inch margins, `microtype`.
- One-and-a-half-spaced body; single-spaced tables, figure notes, and bibliography.
- `natbib` author-year citations, `aer` bibliography style, page and footnote backlinks.
- Modular metadata, preamble, sections, appendices, `Figs/`, and `Tabs/`.
- Equations numbered within sections; main floats numbered globally; appendix floats use `A1`, `B1`, while appendix equations use `A.1`, `B.1`.
- References and appendices each start on a new page; appendix page numbering restarts at 1.
