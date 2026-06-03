# Workflow Checklists

Use these checklists for DIME-style data management, cleaning, construction,
analysis, outputs, reproducibility packages, and code review.

## Project Structure and Data Management

Check for:

- A master script that runs the workflow after changing only one top-level path
  or configuration block.
- Clear folder roles for raw data, intermediate data, final data, documentation,
  code, and outputs.
- A README documenting software versions, packages, runtime, folders, scripts,
  outputs, and run instructions.
- Consistent unique IDs for each unit of observation.
- `isid` or equivalent uniqueness checks before merges and saves.
- Tidy data: one row per observation, one column per variable, one unit of
  observation per dataset.
- Stable sorting before operations that depend on order.
- No PII in analysis-ready or review-package data unless the task explicitly
  concerns confidential workflows.

## Cleaning Code

Cleaning code should:

- Start from raw or deidentified raw data and create cleaned data.
- Document corrections with a codebook, correction file, or explicit code.
- Preserve enough traceability to understand why observations or values changed.
- Label variables and values consistently.
- Use extended missing values where meaningful, such as "do not know" or
  "refused".
- Avoid interactive commands and manual edits.
- Avoid unstable duplicate handling such as `duplicates drop, force`.
- Verify transformations with `assert`, tabulations, counts, and summaries.
- Save final cleaned datasets once, with ID checks.

Common review findings:

- Dropped observations are not justified.
- Merge mismatches are ignored.
- String categories are not normalized before recoding.
- Date variables remain strings.
- Cleaning scripts create analysis variables that belong in construction.

## Indicator Construction

Construction code should:

- Start from cleaned data.
- Build analysis variables, indices, treatment variables, and sample flags.
- Keep variable construction separate from final analysis where practical.
- Use self-documenting names and labels.
- Justify transformations such as logs, winsorization, standardization, and
  imputation.
- Explicitly handle missing values.
- Check constructed variables against source variables and expected ranges.
- Save constructed or analysis datasets with ID checks.

Common review findings:

- Indicator logic does not match the codebook or pre-analysis plan.
- Categorical variables are treated as continuous.
- Sample restrictions are embedded in scattered `if` clauses instead of a named
  sample flag.
- Variable construction is repeated in multiple analysis scripts.

## Analysis Code

Analysis code should:

- Start from constructed or analysis-ready data.
- Avoid creating durable new variables except temporary variables needed for a
  specific output.
- Be modular enough for individual outputs to run independently after setup.
- Document sample selection, missing-data handling, model choice, clustering,
  fixed effects, weights, and covariates.
- Use methods appropriate to the variable type and research design.
- Export tables and figures reproducibly.
- Cross-check key statistics across outputs.

For balance tables, load `stata-command-cards.md` and use the `iebaltab` card.

Common review findings:

- Output files are manually copied or edited.
- Output scripts depend on hidden state from a previous script.
- Model specifications are inconsistent across related tables.
- Regression output is printed but not exported.

## Sampling and Randomization

Check for:

- Stable Stata version and random seed.
- Stable sorting before random numbers are generated.
- Unique IDs before assignment.
- Stratification, clustering, or blocking logic documented.
- Assignment counts checked against design requirements.
- Randomization output saved and not regenerated casually after field use.

## Reproducibility Package or Code Review Package

A reviewable package should include:

- All scripts to be reviewed.
- A main script that runs all code after changing only one top-level path.
- Deidentified data needed to run the code, if computational reproducibility is
  requested.
- README with software/version, runtime, folder purposes, objective, scripts,
  outputs, and reviewer instructions.
- Output mapping: which script creates each table, figure, or data artifact.
- Required packages or bundled dependencies.
- For Stata, do not assume `ssc install iebaltab` works. `iebaltab` is part of
  `ietoolkit`; install or bundle the package that contains the command.

For Stata:

- Set `version`, `matsize`, `varabbrev`, or use `ieboilstart`.
- Install required SSC packages or use a project `ado/` folder.
- Code should create all exhibits and in-text numbers used by the analysis when
  the request is about a reproducibility package.

For R:

- Load all packages in the main script.
- Prefer a reproducible dependency strategy when exact reproduction matters.

## Code Review Output Format

When the user asks for a review, lead with findings:

- Severity and concise title.
- File and line reference.
- What can go wrong.
- Concrete fix.
- DIME checklist category.

Then include open questions, test/reproducibility gaps, and a short summary.
