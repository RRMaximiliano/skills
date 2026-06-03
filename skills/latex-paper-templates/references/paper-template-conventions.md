# Paper Template Conventions

These notes summarize the user's personal LaTeX paper style from the provided
templates. Treat them as opinionated defaults, not universal LaTeX guidance.

## Document Shape

- Use `\documentclass[11pt,a4paper,english]{article}` as the normal paper base.
- Prefer a cleaned, single-pass preamble over the older duplicate-package style.
- Use `geometry` for margins. The common cleaned default is
  `\usepackage[margin=1.25in]{geometry}`.
- Use `setspace`; the cleaned paper style uses `\linespread{1.25}`, while some
  older drafts use `\setstretch{1.5}`.
- Use `mathpazo` for the paper font, with `amsmath`, `amssymb`, `amsthm`, and
  `bm` for math.
- Keep theorem environments available for economics theory or empirical design
  papers: theorem, lemma, proposition, claim, corollary, definition, example,
  assumption, and remark.

## References

The paper style uses `natbib` with author-year citations and AER bibliography
style:

```tex
\usepackage[authoryear]{natbib}
...
\begin{singlespace}
\bibliographystyle{aer}
\bibliography{references}
\end{singlespace}
```

Use this unless the user explicitly asks for a different journal style. The
default bibliography database name is `references.bib`.

## Tables

Tables are usually generated outside the paper body, often from Stata or R, and
included as fragments under `Tabs/`.

Preferred table shell:

```tex
\begin{table}[H]
\centering
\caption{Table title}
\label{tab:table-label}
\adjustbox{width=\textwidth}{
\begin{threeparttable}
\input{Tabs/table-fragment.tex}
\begin{tablenotes}
\setlength\labelsep{0pt}
\footnotesize
\item \textit{Notes}: Describe the sample, variables, standard errors, and
significance stars.
\end{tablenotes}
\end{threeparttable}
}
\end{table}
```

Table conventions:

- Load `booktabs`, `multirow`, `adjustbox`, and `threeparttable`.
- Use `\usepackage[flushleft]{threeparttable}` when notes should align cleanly.
- Use `threeparttablex` only when the paper needs long tables.
- Use `dcolumn` only when decimal-aligned numeric columns are needed.
- Use `\sym{}` to support Stata-style significance stars:

```tex
\def\sym#1{\ifmmode^{#1}\else\(^{#1}\)\fi}
```

- Prefer `booktabs` rules over vertical lines.
- Put the table note in the LaTeX wrapper when the generated fragment should
  stay reusable across papers.
- Put the note in the generated table fragment only when the table-generation
  script owns the whole table.

## Figures

Figure defaults:

```tex
\usepackage{graphicx}
\usepackage{float}
\usepackage{subfig}
\usepackage{pdflscape}
\graphicspath{{Figs/}{figs/}}
```

Preferred figure shell:

```tex
\begin{figure}[H]
\centering
\caption{Figure title}
\label{fig:figure-label}
\includegraphics[width=.9\textwidth]{Figs/figure-file.pdf}
\end{figure}
```

Use `subfig` when the figure needs panels. Use `pdflscape` for large figures or
tables that genuinely need landscape orientation. Keep figure widths explicit so
the rendered paper remains predictable.

## TikZ And PGFPlots

When the paper includes diagrams or plots built in LaTeX, use:

```tex
\usepackage{tikz}
\usepackage{pgfplots}
\usetikzlibrary{arrows,positioning,calc,decorations.markings}
\pgfplotsset{compat=1.3}
```

The older template uses TikZ externalization. Only enable externalization when
the compile command supports shell escape and the output directories are
configured.

## Captions And Hyperlinks

The templates use `caption` with bold labels and a custom centered caption
format. If using the `myformat` caption format, load `varwidth` explicitly:

```tex
\usepackage{varwidth}
\usepackage[labelfont=bf,skip=0pt]{caption}
\DeclareCaptionFormat{myformat}{%
  \begin{varwidth}{\linewidth}#1#2#3\end{varwidth}%
}
\captionsetup[table]{format=myformat}
\captionsetup[figure]{format=myformat}
```

Hyperlink defaults use custom colors and `colorlinks=true`, with `webbrown` as
the common link, cite, and URL color.

## Common Commands

Keep these commands available when useful:

```tex
\DeclareMathOperator*{\argmin}{arg\,min}
\DeclareMathOperator*{\argmax}{arg\,max}
\newcommand{\tint}{\textstyle\int}
\newcommand{\tsum}{\textstyle\sum}
\newcommand\scaleivan[2][4]{\scalebox{#1}{$#2$}}
\def\sym#1{\ifmmode^{#1}\else\(^{#1}\)\fi}
```

For raw Stata `esttab` fragments that need primitive TeX input behavior, the
older template used:

```tex
\let\primitiveinput\input
```

Only keep this if the table fragments require it.

## Clean-Up Rules

- Remove duplicate package loads.
- Keep package order readable: encoding/language, math/fonts, layout, tables,
  figures, captions/colors, hyperlinks, references, custom commands.
- Do not mix `Figs/`, `figs/`, `Figures/`, and `Tabs/` casually. Pick a project
  convention and keep it consistent.
- Avoid turning the paper body into table code. Generate table fragments
  separately and keep the paper readable.
