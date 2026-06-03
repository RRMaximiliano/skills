# R Workflows

Use this reference for R tasks in DIME-style development research projects.
DIME's R training is less prescriptive than the Stata style guide, so use DIME
workflow principles plus the tidyverse style guide.

## Scope

Use R for:

- Data wrangling with tidyverse tools.
- Descriptive statistics.
- Data visualization with `ggplot2`.
- Geospatial data work.
- Dynamic documents with R Markdown or Quarto when requested.
- Mixed reproducibility packages where R handles maps or specialized outputs
  and Stata handles core analysis.

## Main Script

Prefer a main script that:

- Defines user inputs and root paths at the top.
- Loads or installs packages in one section.
- Defines project subfolders with `file.path()`.
- Uses flags or explicit source calls to run selected sections.
- Documents outputs and runtime in the README.

Pattern:

```r
# PART 1: User inputs ---------------------------------------------------------

project_root <- "C:/Users/username/Documents/GitHub/project"

run_cleaning <- FALSE
run_analysis <- TRUE

# PART 2: Packages ------------------------------------------------------------

packages <- c("tidyverse", "broom", "readr")

missing_packages <- packages[!(packages %in% installed.packages()[, "Package"])]
if (length(missing_packages) > 0) {
  install.packages(missing_packages)
}

invisible(lapply(packages, library, character.only = TRUE))

# PART 3: Paths ---------------------------------------------------------------

data_dir <- file.path(project_root, "data")
code_dir <- file.path(project_root, "code")
out_dir  <- file.path(project_root, "outputs")

# PART 4: Run scripts ---------------------------------------------------------

if (run_cleaning) source(file.path(code_dir, "cleaning.R"))
if (run_analysis) source(file.path(code_dir, "analysis.R"))
```

When exact dependency reproduction matters, consider `renv` or a lockfile, but
do not present it as a DIME-specific requirement unless the project already uses
it or the user asks for strict reproducibility.

## Style

Use tidyverse style:

- Clear object names.
- Spaces around operators.
- One pipe step per line for long pipelines.
- Functions for repeated logic.
- No hidden global state in analysis scripts.
- `file.path()` instead of hardcoded path separators.

## Data Cleaning

R cleaning scripts should:

- Normalize names and variable types early.
- Convert dates to date classes.
- Convert categorical variables to factors or labeled numeric variables only
  when appropriate for the downstream workflow.
- Use explicit missing-value handling.
- Write cleaned data once at the end of the script.
- Include checks with `stopifnot()`, `assertthat`, or project test helpers.

## Analysis and Outputs

Analysis scripts should:

- Start from constructed or analysis-ready data.
- Use named sample flags rather than repeated hidden filters.
- Export tables and figures with code.
- Keep plot themes and output dimensions stable.
- Save outputs to a dedicated folder.

Example:

```r
balance_data |>
  filter(analysis_sample == 1) |>
  group_by(treatment_arm) |>
  summarize(
    mean_age = mean(age_year, na.rm = TRUE),
    sd_age = sd(age_year, na.rm = TRUE),
    n = n(),
    .groups = "drop"
  ) |>
  readr::write_csv(file.path(out_dir, "tables", "balance-summary.csv"))
```

## Mixed Stata/R Packages

When a package has both `MASTER.do` and `MASTER.R`:

- Make clear which outputs each language reproduces.
- Keep folder path conventions parallel.
- Document any outputs that cannot be reproduced without confidential data.
- Avoid requiring users to run scripts in undocumented order.
