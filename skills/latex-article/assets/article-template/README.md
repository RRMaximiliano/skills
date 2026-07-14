# LaTeX article project

Build the paper with:

```bash
latexmk -pdf main.tex
```

Clean intermediate files with:

```bash
latexmk -c
```

Write prose in `Sections/` and `Appendices/`, place graphics in `Figs/`, and
place complete generated `tabular` fragments in `Tabs/`. Copy float patterns
from `snippets.tex`; that file is not included in the compiled paper.

When the paper first uses citations, set `\paperhasreferencestrue` in
`metadata.tex` so the AER-style bibliography is emitted.
