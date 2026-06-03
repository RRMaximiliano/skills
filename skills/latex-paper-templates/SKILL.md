---
name: latex-paper-templates
description: "Use for the user's economics paper LaTeX template: article preamble, AER/natbib refs, threeparttable inputs, captions, and figures."
---

# LaTeX Paper Templates

Personal economics paper container, not a general LaTeX guide and not DIME
style. Use for paper preambles, table/figure wrappers, and reference setup. For
Stata code that generates table fragments, use `stata-latex-tables`.

## Workflow

1. For new papers, start from `assets/paper-template/main.tex`.
2. For existing `.tex` files, load `references/paper-template-conventions.md`
   only when details are needed.
3. Preserve the user's conventions unless a journal/submission format overrides
   them.
4. Keep table bodies under `Tabs/` and figures under a consistent folder such as
   `Figs/` or `figs/`.
5. Compile or inspect structure when feasible.

## Defaults

- `article` class unless requested otherwise.
- `natbib` author-year citations with `\bibliographystyle{aer}`.
- Tables use `booktabs`, `adjustbox`, `threeparttable`, `tablenotes`, and
  `\input{Tabs/...}`.
- Use `\sym{}` for Stata stars in imported fragments.
- Figures use `graphicx`, stable paths, and explicit widths.
- If custom captions use `varwidth`, load `\usepackage{varwidth}`.
- Put `\label{}` after `\caption{}` and keep `tab:`/`fig:` prefixes consistent.
