---
name: tfhandout
description: Write and typeset Rony's TF handouts (reading handouts, TF notes, answers to student questions) with the tfhandout LaTeX package and his first-person teaching voice.
---

# TF Handout

Reading handouts for students, in one LaTeX design (`tfhandout.sty`) and one voice.

## Route the task

- New handout: confirm the destination does not exist, copy `assets/template.tex`, and fill it. The preamble stays three lines: `\documentclass{article}`, `\usepackage{tfhandout}`, `\hypersetup{pdftitle={...}}`. Never paste the package's preamble into a document.
- Design change: edit `assets/tfhandout.sty` (the TEXMFHOME copy is a symlink to it), then recompile the reference handouts and compare.
- Before writing, read `references/voice.md`. For tables, figures, folders, and the R appendix, read `references/design.md`.
- If the handout has companion slides, follow the project's AGENTS.md slide–handout mapping rules.

## Build

1. If R makes tables or figure data, run the R script first.
2. `latexmk -xelatex <file>.tex` (needs Minion Pro and STIX Two Math). No build script.

## Validate

1. No LaTeX errors, undefined references, or overfull boxes in the log.
2. Render every page with `pdftoppm` and look at it: no page holding only a reference list, no code spilling a few lines onto a new page, figures legible.
3. Default length: 4–5 pages of text, plus an optional R appendix.

## Install on a new machine

`ln -s <repo>/skills/tfhandout ~/.agents/skills/tfhandout` and
`ln -s <repo>/skills/tfhandout/assets/tfhandout.sty "$(kpsewhich -var-value TEXMFHOME)/tex/latex/tfhandout/tfhandout.sty"` (create the folder first).
