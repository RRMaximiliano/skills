---
name: latex-beamer
description: "Use for the user's crimson economics Beamer slides: slides_updated/math, appendix buttons, bottom links, input tables, figures, and biblatex."
---

# LaTeX Beamer

Personal crimson Beamer slide style. Use for the slide container, not Stata/R
code that generates tables. For paper `.tex` containers use
`latex-paper-templates`.

## Workflow

1. Start new decks from `assets/beamer-template/`.
2. Define crimson colors before loading `slides_updated,math`.
3. Load `references/beamer-conventions.md` only when implementation details are
   needed.
4. Keep figures and tables in separate folders, usually `Figures/` and
   `Tables/`.
5. Use stable main-slide and `appendix:...` labels for navigation.
6. Compile when feasible; if it fails, check style-file paths, missing assets,
   `biblatex`/`biber`, and package conflicts.

## Defaults

- `\documentclass[aspectratio=169,11pt]{beamer}`.
- Harvard crimson `A51C30` as `accent` and `harvardcrimson`.
- Bundled `slides_updated.sty` and `math.sty`.
- `\bottomleft{...}` / `\bottomright{...}` for buttons.
- Forward links use `\beamergotobutton`; appendix returns use
  `\beamerreturnbutton`.
- Tables use `adjustbox`, `threeparttable`, and `\input{Tables/...}`.
- Figures use `\graphicspath` and explicit `\includegraphics` widths.
- Citations use `biblatex` from the style file, not AER/natbib.
