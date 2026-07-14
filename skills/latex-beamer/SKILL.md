---
name: latex-beamer
description: Create, convert, edit, and validate modular economics Beamer presentations in the user's crimson Montero–Yang style. Use for new slide scaffolds, article-to-deck conversion, or work on existing LaTeX Beamer decks involving 4:3 Lato slides, section outlines, imported figures and Stata/R table fragments, AER/natbib references, appendix navigation, overlays, and visual PDF QA.
---

# LaTeX Beamer

Build sparse, projection-readable economics presentations with a white background, Lato typography, Harvard crimson (`#A51C30`), top-aligned content, and the visual grammar of the Montero–Yang reference deck.

## Choose the mode

1. **Article to deck.** Inspect the paper source, compiled PDF, bibliography, `Figs/`, and `Tabs/`. Prefer source plus PDF, then source plus assets, then PDF alone. Ask for original assets when a PDF is the only source; crop or extract from the PDF only as a last resort. Read `references/article-to-deck.md`.
2. **New scaffold.** Copy `assets/beamer-template/` into a new destination. Preserve its modular structure and replace descriptive placeholders with supplied content.
3. **Existing deck.** Inspect before editing. If its theme differs, ask whether to preserve it or migrate to this canonical style. Never migrate silently.

If talk length is absent in article-to-deck mode, ask once. If unanswered, use a 45-minute academic economics seminar and target roughly 25–35 substantive main frames before overlays, references, and appendix. Assume an academic economics audience unless the prompt identifies another audience.

## Hard requirements

- Default to 4:3. Use 16:9 only when the user explicitly requests it; retain projection-readable outline type in widescreen mode.
- Keep content top-aligned. Never shrink prose to rescue an overcrowded frame; split it.
- Use ordinary `itemize`/`enumerate`, concise bullets, small triangle first-level bullets, and dash second-level bullets.
- Use automatic section outline frames unless the user requests a short deck without them. Current section is crimson; inactive sections are pale gray; current subsections are indented and italic. Stop automatic outlines before references and appendix.
- Show substantive main-deck slide numbers at bottom right as `current/total`. Exclude the title page and outline frames from both display and count; hide the counter in the appendix.
- Keep the custom command surface limited to `\goto`, `\backto`, `\bottomleft`, `\bottomright`, `\topleft`, `\topright`, `\fnote`, and `\sym`.
- Use `natbib`, `\citet`, `\citep`, BibTeX, and `\bibliographystyle{aer}`. Do not add page-backreferences to slides.
- Render `\citep{}` at 80% of the surrounding font size in a subdued crimson; retain ordinary `\citet{}` treatment.
- Put references after the conclusion and optional closing frame, and before the appendix. Use `[allowframebreaks]` with Roman continuation titles only when references need more than one frame.
- Omit speaker notes unless explicitly requested.

## Project structure

For a standalone deck, use local `Figs/`, `Tabs/`, and `references.bib`. For a new paper-and-deck project, use root-shared `Figs/`, `Tabs/`, and `references.bib` with sibling `Article/` and `Beamer/` directories. When adding slides to an existing article project, do not restructure it; add a sibling `Beamer/` directory and reference the article's existing assets.

Use one source file per major section, not one file per frame. Keep metadata in `metadata.tex`, packages and project-specific macros in `preamble.tex`, and visual rules in `beamer_style.sty`.

## Figures and tables

Read `references/exhibits-and-navigation.md` before adding exhibits or appendix buttons.

- Reuse supplied assets; do not generate analytical figures or fabricate data.
- Standard tables use slightly reduced (`\small`) body text and imported `Tabs/*.tex` fragments inside `adjustbox` and `threeparttable`, with a caption and left-aligned `tablenotes`. Load `caption` with `skip=0pt` and remove the gap between the caption and top rule. Treat generated fragments as immutable.
- Do not invoke a table-generation, Stata, R, Python, or research-data skill unless the user separately and explicitly requests that work. If a required slide fragment is absent, report it or leave a descriptive placeholder.
- Figures use a caption above and justified `\fnote` below.
- In article-derived decks, preserve paper table and figure numbers even when there are gaps. In standalone decks, number sequentially.
- Simplify table layout for projection when needed, but never alter numerical content. Put a full dense table in the linked appendix when the main frame needs a readable subset.
- Prefer bottom-left navigation. Use another position only when the layout or prompt requires it, and give every button an informative destination or return label—never a bare `Back`.

## Narrative and overlays

In article-to-deck mode, derive a talk rather than mechanically converting paper sections. Show a concise storyboard and proceed unless a materially consequential ambiguity requires approval. Reuse the paper's notation; number only equations referenced later. Put derivations in the appendix.

Use overlays only when they control exposition. Prefer explicit overlay specifications or `\pause`; never set global `<+->`. The final overlay must show the complete intended composition. Leave figures, tables, and static factual lists static by default.

## Validate every deliverable

1. Compile from the project directory with `latexmk -pdf main.tex`.
2. Scan the log with:
   `rg -n 'LaTeX Error|undefined|multiply defined|Overfull|Fatal error|Emergency stop|File .* not found' main.log`
3. Render every PDF page with Poppler (`pdftoppm`) and inspect every slide for clipping, weak contrast, small tables, broken notes, bad line breaks, and crowded layouts.
4. Validate every `\goto`/`\backto` target and every citation, reference, label, and asset path.
5. Keep the reusable template free of build artifacts.

Do not report success while unresolved references, missing files, duplicate labels, clipping, or unreported overfull boxes remain.
