---
name: development-research-in-practice
description: "Use for DIME-style Stata/R research data workflows: project setup, cleaning, construction, analysis, iebaltab/ietoolkit, reproducibility packages, and code review."
---

# Development Research in Practice

Stata-first DIME-style guidance: runnable workflows, clear IDs/samples,
explicit packages/paths, verified transformations, and reproducible outputs.
Use R when requested.

## Quick Workflow

1. Inspect roots, master scripts, packages, folders, README, and output map.
2. Classify the task: setup, cleaning, construction, analysis, output,
   package, command help, or review.
3. Load the smallest needed resource:
   - `references/task-recipes.md`: concrete Stata workflows.
   - `references/balance-table-recipe.md`: `iebaltab` implementation.
   - `references/stata-command-cards.md`: ietoolkit command patterns.
   - `references/stata-style.md`: Stata style and reproducibility.
   - `references/workflow-checklists.md`: review checks.
   - `references/review-rubric.md`: P0-P3 review severity.
   - `references/r-workflows.md`: R and mixed Stata/R workflows.
   - `references/skill-routing.md`: when another personal skill fits better.
   - `references/sources.md`: source links.
4. Produce code or severity-ranked findings. If Stata is unavailable for review,
   run `scripts/audit_stata_project.py <project-root>` and treat results as
   leads.

## Standards

- One entry point runs after one root/config edit.
- Dependencies are installed, bundled, or exposed up front.
- `ieboilstart` is followed by `` `r(version)' ``.
- IDs are checked before merges/saves.
- Cleaning, construction, and analysis are separated when useful.
- Merges, appends, duplicates, drops, recodes, imputation, winsorization, and
  samples are justified.
- Outputs are created by code.
- `iebaltab` variables are continuous/binary; categorical variables become
  indicators.

## Review Output

For reviews, use `review-rubric.md`. Findings need file/line, risk, checklist
area, and fix. "DIME-ready" requires clear run path, dependencies, IDs,
transformations, analysis choices, outputs, and output map.
