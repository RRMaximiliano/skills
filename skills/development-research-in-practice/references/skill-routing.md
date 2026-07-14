# Skill Routing

Use this reference when the request overlaps with another skill in this
repository.

## Route To `development-research-in-practice`

Use this skill for:

- DIME-style Stata or R research data workflows.
- Data management, cleaning, construction, analysis, and output reproducibility.
- DIME Stata commands such as `iebaltab`, `ieboilstart`, `iesave`,
  `iecodebook`, `ieduplicates`, `ietestform`, `iegraph`, `iekdensity`,
  `iematch`, and `ieddtab`.
- Code review, reproducibility package review, and reviewer-readiness checks.
- Fresh-session run order, project setup, and package dependency questions.

## Route To `stata-latex-tables`

Use when the user wants the user's personal Stata-to-LaTeX output style:

- `eststo`, `esttab`, `estadd`, custom panel fragments, and paper-ready table
  fragments.
- Personal table conventions that may differ from DIME practice.
- Stata code that creates LaTeX table fragments for papers or slides.

If a balance table is requested with `iebaltab`, stay in
`development-research-in-practice`. If the user asks for custom personal table
formatting outside DIME defaults, route to `stata-latex-tables`.

## Route To `latex-article`

Use when the task is the LaTeX paper container:

- Article preamble.
- AER/natbib bibliography style.
- `threeparttable` wrappers in the paper.
- Figure paths and paper caption conventions.

## Route To `latex-beamer`

Use when the task is the Beamer slide container:

- Crimson Beamer deck style.
- `slides_updated.sty` and `math.sty`.
- Appendix navigation buttons.
- Slide wrappers for imported tables and figures.

## Mixed Tasks

For mixed tasks, apply skills by layer:

1. Generate or review data/table code with `development-research-in-practice` or
   `stata-latex-tables`.
2. Place the resulting table or figure in the final paper with
   `latex-article`.
3. Place the resulting table or figure in slides with `latex-beamer`.
