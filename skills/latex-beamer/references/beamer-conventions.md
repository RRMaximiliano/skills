# Beamer Conventions

These notes summarize the user's personal Beamer style from `JWEE.tex`,
`slides_updated.sty`, and `math.sty`.

## Identity And Preamble

- Use `\documentclass[aspectratio=169,11pt]{beamer}`.
- Define crimson colors before loading `slides_updated.sty`. The style file uses
  `\providecolor`, so predefining `accent` is the right way to override defaults.
- Always keep Harvard crimson as the main accent:

```tex
\definecolor{accent}{HTML}{A51C30}
\definecolor{accent2}{HTML}{1E1E1E}
\definecolor{harvardcrimson}{HTML}{A51C30}
\definecolor{harvarddark}{HTML}{8C1515}
\definecolor{harvardslate}{HTML}{293352}
\usepackage{slides_updated,math}
```

- The source deck uses `\graphicspath{{../Figures/}}`; for reusable templates,
  prefer `\graphicspath{{Figures/}{../Figures/}}`.
- The source deck uses `\addbibresource{../cites.bib}`. For reusable templates,
  prefer `\addbibresource{cites.bib}` unless the deck lives in an Overleaf
  subfolder.

## Style Files

`slides_updated.sty` defines:

- Crimson/slate/zinc color palette.
- Alegreya Sans as the main font.
- White background, crimson frame titles, compact margins, and frame numbering.
- Button colors and border colors.
- `\bottomleft{...}` and `\bottomright{...}` helpers using `textpos`.
- Appendix frame numbering through `appendixnumberbeamer`.
- `zincBlock`, `purpleBlock`, and `cranberryBlock`.
- `codeblock` for code snippets.
- `biblatex` with `natbib=true`, `backend=biber`, and
  `style=ext-authoryear-ecomp`.
- Table support: `adjustbox`, `booktabs`, `tabularx`, `dcolumn`, and the custom
  `\note` and `\tabletitle` commands.
- Table highlighting through `\marktopleft{...}` and `\markbottomright{...}`.
- `\imageframe{...}` for full-bleed image slides.
- `transitionframe` for crimson transition slides.

`math.sty` defines compact math helpers:

- Brackets: `\bc`, `\bp`, `\bs`, `\abs`, `\norm`, `\floor`.
- Operators: `\argmax`, `\argmin`, `\E`, `\P`, `\var`, `\cov`, `\corr`,
  `\sd`, `\se`, `\plim`.
- Other notation: `\one`, `\indep`, `\iid`, `\asto`, `\dto`, `\pto`.

## Navigation Buttons

Main slides should have stable labels. Appendix slides should use
`appendix:...` labels. Use forward buttons from main slides:

```tex
\hyperlink{appendix:budget}{\beamergotobutton{UKR consolidated budget}}
```

Use return buttons from appendix slides:

```tex
\bottomleft{
  \hyperlink{motivation}{\beamerreturnbutton{Motivation}}
  \hyperlink{context}{\beamerreturnbutton{Context}}
}
```

For details that should stay out of the main flow, place buttons in
`\bottomleft{...}`. Inline buttons are fine when the detail is attached to a
specific bullet.

Overlay-specific buttons are allowed:

```tex
\hyperlink<2->{appendix:main_results_exp2}{\beamergotobutton{Table Experiment 2}}
```

## Tables

The Beamer table style matches the paper workflow: generate the body separately
and import it into the deck.

Preferred appendix table shell:

```tex
\begin{frame}\label{appendix:main-table}
\vspace*{-.5cm}
\begin{table}[H]
\centering
\adjustbox{max width=.85\textwidth}{%
\begin{threeparttable}
\caption{Table title}
\label{tab:main-table}
\input{Tables/main-table}
\end{threeparttable}
}
\end{table}
\bottomleft{\hyperlink{main:results}{\beamerreturnbutton{Return to results}}}
\end{frame}
```

Table conventions:

- Load `multirow`, `threeparttable`, `threeparttablex`, and `varwidth` in the
  deck when needed.
- Use `\def\sym#1{\ifmmode^{#1}\else\(^{#1}\)\fi}` for Stata stars.
- Keep generated fragments under `Tables/`.
- Scale tables with `\adjustbox{max width=...}`. Common widths are
  `.4\textwidth`, `.5\textwidth`, `.8\textwidth`, `.9\textwidth`, and
  `\textwidth`.
- Use negative vertical spacing only when needed to fit appendix tables.

## Figures

Preferred figure shell:

```tex
\begin{frame}\label{main:figure}
\frametitle{Figure Title}
\begin{figure}
\centering
\includegraphics[width=.8\textwidth]{figure-file.pdf}
\end{figure}
\end{frame}
```

Figure conventions:

- Configure `\graphicspath` once.
- Use concise file names in `\includegraphics`.
- Use `columns` for side-by-side figures.
- Use `\imageframe{file}` only for full-slide image moments.
- Use captions when they clarify the figure, especially in appendix slides.

## Captions

The source deck uses `caption` plus `varwidth`:

```tex
\usepackage[skip=0pt]{caption}
\DeclareCaptionLabelFormat{AppendixTables}{A.#2}
\DeclareCaptionFormat{myformat}{%
  \begin{varwidth}{\linewidth}%
    \centering
    #1#2#3%
  \end{varwidth}%
}
\captionsetup{format=myformat}
```

Keep this when revising a deck. If a compile error mentions `varwidth`, make
sure `\usepackage{varwidth}` is loaded.

## Bibliography

Unlike the paper template, this Beamer setup does not use
`\bibliographystyle{aer}`. The style file loads `biblatex` with `natbib=true`.
Use `\addbibresource{...}` in the deck. Add a references frame only when needed:

```tex
\begin{frame}[allowframebreaks]{References}
\printbibliography
\end{frame}
```

Compile with `pdflatex`, `biber`, then `pdflatex` twice when citations or
references need to resolve.
