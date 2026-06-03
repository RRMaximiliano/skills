# Stata Style and Reproducibility

Use this reference for Stata code writing and review. It summarizes the DIME
Analytics Data Handbook coding appendix and DIME code review checklist.

## Good Code Standard

Good research code must be correct, readable, reusable, and reviewable. Evaluate
it on three dimensions:

- Structure: files, folders, master scripts, dependencies, and outputs are easy
  to locate and can be run in order.
- Syntax: commands express the research intention clearly and use common Stata
  patterns.
- Style: comments, names, spacing, and indentation make errors easier to spot.

## Master Do-File

Prefer a master do-file that:

- Has a header with purpose, outline, required inputs, created outputs, and ID
  variables where relevant.
- Installs or points to required user-written commands.
- Harmonizes settings with `ieboilstart` or explicit equivalents.
- Sets Stata `version` once and does not change it casually after
  randomization.
- Defines all root folder paths in one top-level block.
- Runs task scripts in the intended order from a fresh Stata session.
- Uses `run` for subfiles when command-window output is not needed.

Boilerplate pattern:

```stata
* Install or make project commands available before use
cap which ietoolkit
if (_rc == 111) ssc install ietoolkit

* Harmonize settings
ieboilstart, versionnumber(18.0)
`r(version)'
```

For standalone reproducibility packages, prefer a project-specific `ado/`
folder. Two common patterns are acceptable:

```stata
* Reproducibility repository template style
global project "???"
global code    "${project}/code"
sysdir set PLUS "${code}/ado"
```

```stata
* Strict project adopath through ietoolkit
global ado "${project}/code/ado"
ieboilstart, versionnumber(18.0) adopath("${ado}", strict)
`r(version)'
```

The strict `adopath()` pattern is strongest when the package includes all
user-written commands. The `sysdir set PLUS` pattern is common in World Bank
reproducibility templates and still avoids hidden dependence on each user's
personal Stata installation.

## Paths

DIME sources emphasize both dynamic absolute paths and code-review packages that
run after changing only one directory. Reconcile these as:

- Put user-specific absolute paths only in one top-level root configuration.
- Build all project paths from that root with globals/macros.
- Use forward slashes.
- Include file extensions.
- Avoid relying on `cd` except when a command strictly requires it.
- Flag hardcoded paths like `C:/Users/name/...` outside the setup block.
- For code-review or reproducibility packages, code should run after changing
  only the top-level directory path.

Pattern:

```stata
global project_root "C:/Users/username/Documents/GitHub/project"
global data        "${project_root}/data"
global outputs     "${project_root}/outputs"

use "${data}/final/analysis-data.dta", clear
```

## Comments and Sections

Use comments to organize code and explain decisions, especially why a choice was
made. Prefer self-documenting variable names over comments that explain cryptic
code.

Use section bookmarks where helpful:

```stata
**# Construct outcome variables
```

Use inline comments sparingly for local decisions:

```stata
local min_wage 12 // Illinois minimum wage used for 2022 estimates.
```

## Names and Abbreviations

- Do not abbreviate variable names.
- Avoid wildcard variable lists unless they are created and checked explicitly
  with commands such as `unab` or `lookfor`.
- Keep common command abbreviations readable. Accepted examples include `gen`,
  `reg`, `sum`, `tab`, `bys`, `qui`, `noi`, `cap`, `forv`, `mat`, `lab`, `tw`,
  and `di`.
- Do not abbreviate `local`, `global`, `save`, `merge`, `append`, or `sort`.
- Use descriptive loop indexes such as `crop`, `plot_num`, or `outcome`, not
  `i` or `j`, except for generic matrix/iteration examples.

## Whitespace and Line Breaks

- Use four spaces for indentation inside loops, conditionals, and programs.
- Align repeated operations when the same central variable is being modified.
- Break long lines around 80 characters with `///`.
- Do not use `#delimit` in ordinary analysis scripts.
- Do not use `/* */` as a line-break device.

Readable pattern:

```stata
graph hbar outcome               /// Outcome variable
     if (analysis_sample == 1)   /// Analysis sample only
   , over(treatment_arm)         /// Treatment arm categories
     ytitle("Mean outcome")
```

## Conditionals and Missing Values

- Put conditionals in parentheses where they are compound or nontrivial.
- Use `!` for logical negation.
- Use explicit truth checks such as `if (eligible == 1)`.
- Use `missing(var)` or `!missing(var)` rather than numeric comparisons with
  `.` unless extended missing logic is intentional.
- Consider Stata's extended missing values before writing `!= .` logic.
- Prefer `if/else` when cases are mutually exclusive.

Pattern:

```stata
replace gender_string = "Woman" if (gender == 1)
replace gender_string = "Man"   if ((gender != 1) & !missing(gender))
```

## Data Management Checks

Add checks near the operation they protect:

```stata
isid household_id
assert !missing(household_id)
assert inlist(treatment_arm, 0, 1, 2) if !missing(treatment_arm)
```

Avoid:

- `duplicates drop, force`
- `merge m:m`
- `append, force`
- `save ..., replace` without first checking IDs when saving important cleaned,
  constructed, or final data
- repeated overwriting of final datasets
- `edit` or `browse` in production do-files
- manual table/figure copying

Use `tempfile` for intermediate data that is not a workflow artifact.

## Outputs

- Export outputs by code with `replace`.
- Save final tables in Git-friendly formats when possible: `.csv`, `.txt`,
  `.tex`.
- Save graphs with `graph export`.
- Name output files descriptively and store them in dedicated folders.
- Start and close logs when logs are part of the workflow.
