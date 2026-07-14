# Optional article capabilities

Read only the sections needed for the current paper. Do not add these packages or commands to an otherwise standard project.

## Multipage tables

Load:

```latex
\usepackage{longtable}
\usepackage{threeparttablex}
```

For landscape pages, also load:

```latex
\usepackage{pdflscape}
```

Use the following wrapper. Replace the column specification, measurement row, titles, label, notes, and input path. The measurement row must contain the widest expected entry in each column so `\LTcapwidth` matches the natural table width.

```latex
\begin{landscape}
\begin{singlespace}
\newlength{\LandscapeLongTableWidth}
\settowidth{\LandscapeLongTableWidth}{%
  \begin{tabular}{@{}l*{8}{r}@{}}
    Widest item label & 999 & 999 & 999 & 999 & 999 & 999 & 999 & 999
  \end{tabular}%
}
\setlength{\LTcapwidth}{\LandscapeLongTableWidth}
\begin{ThreePartTable}
  \begin{TableNotes}[flushleft]
    \setlength\labelsep{0pt}
    \footnotesize
    \item \textit{Notes}: Describe the unit of observation, specification,
    controls, inference, and significance notation.
  \end{TableNotes}
  \begin{longtable}{@{}l*{8}{r}@{}}
    \caption{Descriptive multipage table title}
    \label{tab:multipage_label}\\
    \toprule
    Item & M1 & M2 & M3 & M4 & M5 & M6 & M7 & M8 \\
    \midrule
    \endfirsthead
    \caption[]{Descriptive multipage table title (continued)}\\
    \toprule
    Item & M1 & M2 & M3 & M4 & M5 & M6 & M7 & M8 \\
    \midrule
    \endhead
    \midrule
    \multicolumn{9}{r}{\textit{Continued on next page}}\\
    \endfoot
    \bottomrule
    \insertTableNotes\\
    \endlastfoot
    \input{Tabs/multipage_rows.tex}
  \end{longtable}
\end{ThreePartTable}
\end{singlespace}
\end{landscape}
```

Do not wrap `longtable` in `table`, `adjustbox`, `threeparttable`, `minipage`, or another unbreakable box. Do not force `\TPTminimum` to `\linewidth`; doing so makes the notes wider than a naturally sized table.

If the table is intentionally full-width, design the column specification for that width and set `\LTcapwidth` to the same explicit width. Do not accidentally stretch a narrow table merely to align its notes.

## Decimal-aligned columns

Load `dcolumn` only when decimal alignment is requested. Define a reusable numeric column type appropriate to the paper, for example:

```latex
\usepackage{dcolumn}
\newcolumntype{d}[1]{D{.}{.}{#1}}
```

Retain the canonical standard-table wrapper around the imported `tabular` fragment.

## Bold mathematics and optimization operators

Load `bm` only when bold mathematical symbols are required. Define optimization operators only when used:

```latex
\usepackage{bm}
\DeclareMathOperator*{\argmin}{arg\,min}
\DeclareMathOperator*{\argmax}{arg\,max}
```

## Theorem environments

Use `amsthm` only when formal theorem-like statements appear. Share numbering within sections unless the user requests another scheme:

```latex
\usepackage{amsthm}
\theoremstyle{plain}
\newtheorem{theorem}{Theorem}[section]
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{proposition}[theorem]{Proposition}
\newtheorem{claim}[theorem]{Claim}
\newtheorem{corollary}[theorem]{Corollary}
\theoremstyle{definition}
\newtheorem{definition}[theorem]{Definition}
\newtheorem{example}[theorem]{Example}
\newtheorem{assumption}[theorem]{Assumption}
\theoremstyle{remark}
\newtheorem{remark}[theorem]{Remark}
```
