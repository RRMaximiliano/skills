# Design

`tfhandout.sty` is the ECON 2360 notes preamble on US Letter with 1-inch margins: XeLaTeX, Minion Pro + STIX Two Math, Menlo for code, 1.2 line spacing, no paragraph indent, sharp tcolorboxes, natbib/AER, webbrown links. Its header lists everything it provides.

## What to use

- `keybox` (titled tcolorbox): a student's question or one key result.
- `\begin{empheq}[box=\tcbhighmath]{equation}`: the one boxed equation.
- `defin`, `example`, `remark` environments.
- Colors: `webbrown`, `webgreen`, `webpurple`; figure palette `over` (blue), `under` (amber), `flip` (red).
- Macros: `\corr`, `\sd`, `\E`, `\sym{***}`; column types `C{}` and `L{}`.
- Load extra packages (pgfplots, subcaption, …) in the document, not in the package.

## Tables

An R script writes a complete `tabular` fragment to `handout/Tabs/`; never type numbers into a table. Wrap it as in `assets/template.tex`: `table[tbp]`, `\singlespacing`, `adjustbox{max width=\textwidth}`, `threeparttable`, caption on top, `tablenotes` with a `\textit{Notes}:` line.

## Figures

Caption on top, then `\fnote{\textit{Notes}: …}` explaining in plain language how to read the figure. Draw in TikZ or pgfplots (data from R as CSV in `handout/Figs/`) so fonts match.

## Folder

- `handout/` — the .tex, `Tabs/`, `Figs/`.
- `code/` — the student-facing R script (printed in the appendix with `\lstinputlisting[style=rcode]{../code/<script>.R}`) and a teaching-team script that writes the tables and stops if the numbers are off.
- `README.md` — files, sections, the two rebuild commands, and where every number comes from.

## Reference handouts

- `~/Library/CloudStorage/Dropbox/PhD/HGSE/11-TFing/API209/2026/TF Sessions/session06/` — OVB: TikZ figure, two R tables, R appendix.
- `~/Library/CloudStorage/Dropbox/PhD/HGSE/11-TFing/API209/2026/TF Sessions/homoskedasticity-note/` — student question: pgfplots figure, simulation table, R appendix.
