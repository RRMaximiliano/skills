---
name: stata-latex-tables
description: "Use for the user's personal Stata-to-LaTeX table workflow: esttab/eststo, estadd, panel fragments, balance tables, snippets, and paper-ready exports."
---

# Stata LaTeX Tables

Personal, opinionated Stata table-building style. Use for Stata code that
creates paper-ready LaTeX tables or snippets. This is not official DIME style;
for DIME data-workflow standards use `development-research-in-practice`.

## Workflow

1. Inspect existing master scripts, output folders, style globals, packages,
   table scripts, and custom ado files such as `texsave_custom`.
2. Classify the table: regression, balance, descriptive, panel, appendix,
   in-text snippet, or multiple-hypothesis correction table.
3. Load `references/stata-table-patterns.md` for detailed patterns.
4. Write/review code that regenerates the table from data or model results and
   exports by code.

## Standards

- No manual edits to generated `.tex` outputs.
- Paths must use project output macros.
- Use `eststo clear` before a new table family.
- First `esttab` write uses `replace`; later panels use `append`.
- `estadd` statistics use the correct sample, often `e(sample)`.
- Panel headers, model counts, and column specs must agree.
- Adjusted p-values must be computed and aligned intentionally.
- Balance variables must be continuous or binary before `iebaltab`.
- In-text snippets must come from the same code path as tables.

For reviews, lead with reproducibility, output correctness, and LaTeX structure
issues before style polish.
