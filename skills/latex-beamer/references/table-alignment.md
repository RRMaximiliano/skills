# Native LaTeX table alignment

LaTeX aligns boxes by internal reference points, not by the visible first lines of their text. A p/X construction can therefore compile cleanly while a short label sits midway down a wrapped definition. Changing tabularxcolumn to m can also affect later tables and introduce new alignment defects.

Never mix paragraph columns (`p` or `X`) with ordinary baseline cells (`l`, `c`, or `r`), or mix `p`, `m`, and `b` families, within a prose row. Their boxes use different vertical reference models, so the first and last columns may look displaced even when the source appears symmetrical.

## Choose the structure by content

- Numeric results, matrices, and writable grids may use tabular or tabularx.
- Schedules use a plain tabular with fixed-width m columns throughout.
- Glossaries, label--definition pairs, and prose comparison lists are not tables. Build each row from explicitly top-aligned columns or parboxes.

Do not use manual vspace, rule struts chosen by eye, or raisebox to repair a defective table row.

## Schedule pattern

Use fixed widths whose total, including intercolumn spacing, fits the text width:

    \begin{tabular}{@{}
      >{\raggedright\arraybackslash\color{crimson}\bfseries}m{2.2cm}
      >{\raggedright\arraybackslash}m{6.6cm}
      >{\raggedleft\arraybackslash}m{1.25cm}@{}}
      0:00--0:05 & Opening question & 5 min \\
      0:05--0:17 & Working with objectives & 12 min \\
    \end{tabular}

Every cell uses the same m-column model. No tabularxcolumn redefinition can leak into a later frame.

## Beamer label--definition pattern

Use one top-aligned columns environment per semantic row:

    \begin{columns}[t,onlytextwidth]
      \column{0.32\textwidth}{\bfseries\color{crimson}Objective}
      \column{0.64\textwidth}A condition the policy should improve.
    \end{columns}

Repeat the complete columns environment for each row. The t option aligns the first baselines, including when one side wraps.

## Handout label--definition pattern

Use paired top-aligned parboxes. Begin both boxes with the same strut:

    \noindent
    \parbox[t]{1.6in}{\raggedright\strut\textbf{\color{crimson}Objective}}%
    \hspace{0.16in}%
    \parbox[t]{\dimexpr\linewidth-1.76in\relax}{%
      \raggedright\strut A condition the policy should improve.}\par

## Required visual check

Render every page containing a table-like layout and the page immediately after it. At readable zoom, trace a horizontal line through the first baseline of each row and verify that the left, middle, and right cells meet it. Also check for leaked alignment definitions. A clean compile is not evidence of visual alignment.
