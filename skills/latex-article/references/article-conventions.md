# Article conventions

## Contents

1. Project contract
2. Typography and citations
3. Tables
4. Multipage tables
5. Figures
6. Numbering
7. Existing-project policy
8. Quality gate

## Project contract

New projects default to:

```text
main.tex
preamble.tex
metadata.tex
references.bib
snippets.tex
.latexmkrc
.gitignore
README.md
Sections/
Appendices/
Figs/
Tabs/
```

`Tabs/*.tex` contains a complete `tabular` environment only. Float placement, caption, label, notes, `adjustbox`, and `threeparttable` belong in the section or appendix file. Treat generated table fragments as immutable unless the user explicitly requests a direct patch.

## Typography and citations

- Use 11pt US Letter, Palatino (`mathpazo`), one-inch margins, traditional paragraph indentation, and no paragraph skip.
- Use `\onehalfspacing` for prose and `\singlespacing` for tables and references.
- Load `threeparttable` with its `flushleft` option so table notes align with the table body rather than inheriting the default list indentation.
- Load `caption` with `skip=0pt` and retain the bundled patch to `threeparttable`'s internal post-caption skip so the title sits directly above the top rule.
- Use `natbib`, `\citet`, `\citep`, and `\bibliographystyle{aer}`.
- Define `winered` as `\definecolor{winered}{rgb}{0.5,0,0}`.
- Enable `pagebackref`; format bibliography backlinks as `(Cited on ...)`; load `footnotebackref` after `hyperref`.
- Prefer supplied bibliography entries. Never fabricate sources, findings, or empirical details.

Use label namespaces `sec:`, `subsec:`, `eq:`, `tab:`, `fig:`, and `app:`. Put `\label` immediately after `\caption` for floats and immediately after the section command for sections.

## Tables

Every standard table must use `[H]`, `\centering`, `\singlespacing`, and the complete `adjustbox` then `threeparttable` wrapper:

```latex
\begin{table}[H]
  \centering
  \singlespacing
  \adjustbox{max width=\textwidth}{%
    \begin{threeparttable}
      \caption{Descriptive table title}\label{tab:descriptive_label}
      \input{Tabs/table_fragment.tex}
      \begin{tablenotes}
        \setlength\labelsep{0pt}
        \footnotesize
        \item \textit{Notes}: Describe the unit of observation, specification,
        controls, inference, and significance notation.
      \end{tablenotes}
    \end{threeparttable}
  }
\end{table}
```

Always retain `adjustbox`, even when the table already fits. Use `\sym{***}`, `\sym{**}`, and `\sym{*}` for significance markers. If resizing makes a table unreadable, add `rotating` only when needed and use a landscape `sidewaystable`; do not silently shrink text to illegibility.

Load and apply the supporting caption setup as:

```latex
\usepackage[flushleft]{threeparttable}
\AtBeginDocument{\captionsetup[table]{format=myformat}}
\AtBeginDocument{\captionsetup[figure]{format=myformat}}
```

Imported Stata/R fragments should resemble:

```latex
\begin{tabular}{@{}l*{3}{c}}
  \toprule
  & (1) & (2) & (3) \\
  \midrule
  Treatment & 0.100\sym{**} & 0.120\sym{***} & 0.110\sym{**} \\
            & (0.040)        & (0.040)         & (0.050)        \\
  \bottomrule
\end{tabular}
```

## Multipage tables

A genuine multipage table is the sole exception to the standard `adjustbox` and `threeparttable` wrapper: a boxed or floating table cannot break across pages. Load `longtable` and `threeparttablex` only when needed; add `pdflscape` only for landscape pages. Read `optional-capabilities.md` and use its canonical wrapper.

Keep the same visual standard as a regular table:

- single spacing;
- centered caption above the table;
- flush-left, footnotesize, justified notes below the final rule;
- repeated column headings and a continued caption on later pages;
- caption, rules, table body, and notes constrained to the same width.

Set `\LTcapwidth` explicitly to the table's measured natural width. The measurement row must contain the widest expected entry in every column; otherwise the caption can be narrower than the final table. Never use `\TPTminimum{\linewidth}` merely to widen the notes, and do not use `@{\extracolsep{\fill}}` unless the table is intentionally designed to occupy the full available line width.

## Figures

Consume supplied or existing figure assets. Figure production and analytical plotting are outside this skill's scope unless the user explicitly requests them.

Use `[H]`, caption and label above the graphic, full line width by default, and a justified `\fnote` below:

```latex
\begin{figure}[H]
  \caption{Descriptive figure title}
  \label{fig:descriptive_label}
  \centering
  \includegraphics[width=1\linewidth]{Figs/figure_file.pdf}
  \fnote{\textit{Notes}: Explain the estimand, sample, confidence intervals,
  standardization, controls, and source.}
\end{figure}
```

Add `subcaption` only when multi-panel figures are required. Do not include unused example panels in a new scaffold.

## Numbering

- Main equations: `(1.1)`, `(1.2)`, `(2.1)`.
- Main tables and figures: `Table 1`, `Figure 1`, continuing globally.
- Appendix floats: `Table A1`, `Figure A1`, reset within each appendix section.
- Appendix equations: `(A.1)`, `(A.2)`, then `(B.1)`.
- Begin references on a new page.
- Begin appendices on a new page, restart printed appendix pages at 1, and use modular files such as `A_data.tex`, `B_theory.tex`, and `C_additional_results.tex`.

## Existing-project policy

Preserve an existing project's class, engine, folder names, bibliography system, and styling unless the user asks to migrate. New projects use `Figs/` and `Tabs/`; existing projects keep their current paths. Do not perform unrelated preamble cleanup.

## Quality gate

Compile with `latexmk -pdf`. Fail delivery on undefined citations or references, duplicate labels, missing inputs, and LaTeX errors. Render and inspect affected pages. Overfull boxes may remain only when explicitly reported with their locations and impact.
