# Task Recipes

Use this reference when the user asks for a concrete DIME-style implementation
rather than a broad review. These are operational defaults for Stata-first data
management, cleaning, construction, analysis, and output work.

## 1. Master Do-File Setup

Use when starting a project workflow, repairing a fragile run order, or preparing
a reproducibility/code-review package.

Minimum structure:

```stata
* ============================================================================ *
* Project master do-file
* ============================================================================ *

* User input: change only this path
global project_root "C:/path/to/project"

* Folder globals
global code       "${project_root}/Code"
global data       "${project_root}/Data"
global dt_raw     "${data}/Raw"
global dt_clean   "${data}/Clean"
global dt_final   "${data}/Final"
global outputs    "${project_root}/Outputs"
global out_tables "${outputs}/Tables"
global out_figs   "${outputs}/Figures"
global ado        "${project_root}/ado"

cap which ietoolkit
if (_rc == 111) ssc install ietoolkit

ieboilstart, versionnumber(18.0) adopath("${ado}", strict)
`r(version)'

do "${code}/1_clean/clean_baseline.do"
do "${code}/2_construct/construct_analysis.do"
do "${code}/3_analysis/analysis_main.do"
```

Checks before accepting:

- Only one user-edited root path or config block is needed.
- Package setup appears before any project script runs.
- Every called script can run from a fresh session after the master setup.
- Output folders are created by code when they may be missing.
- Run order maps cleanly to data stages and output artifacts.

## 2. Survey Cleaning

Use when converting raw/deidentified survey files into clean data.

Preferred flow:

1. Load raw or deidentified raw data.
2. Confirm the intended unit of observation.
3. Check IDs, duplicates, dates, and enumerator/submission metadata.
4. Normalize strings before recoding.
5. Apply documented corrections through code, `iecorrect`, or `iecodebook`.
6. Convert special response values to extended missing values where useful.
7. Label variables and values.
8. Assert valid ranges and internal consistency.
9. Save once, with ID checks.

Pattern:

```stata
use "${dt_raw}/baseline.dta", clear

assert !missing(student_id)
isid student_id

replace gender = trim(itrim(lower(gender)))
gen female = (gender == "female") if !missing(gender)
label var female "Student is female"

assert inrange(age, 5, 25) if !missing(age)
assert inlist(female, 0, 1) if !missing(female)

iesave "${dt_clean}/baseline_clean.dta", ///
    idvars(student_id) ///
    version(14) ///
    report ///
    replace
```

Flag:

- Ad hoc `drop if` commands with no counted reason.
- Cleaning scripts that create final analysis indices or treatment effects.
- Corrections that live only in comments.
- Unchecked string-to-numeric recodes.

## 3. Merge Workflow

Use when joining datasets or reviewing merge logic.

Required pre-checks:

```stata
use "${dt_clean}/student_baseline.dta", clear
isid student_id
tempfile baseline
save `baseline'

use "${dt_clean}/student_endline.dta", clear
isid student_id

merge 1:1 student_id using `baseline'
tab _merge
```

After merge:

```stata
count if _merge == 1
local master_only = r(N)

count if _merge == 2
local using_only = r(N)

assert _merge == 3 if analysis_sample == 1
drop _merge
```

Review logic:

- Use `merge 1:1`, `m:1`, or `1:m` only when both sides pass the corresponding
  ID checks.
- Do not use `merge m:m`.
- Count and explain unmatched observations.
- Keep `_merge` until checks are complete.
- If unmatched rows are expected, name the sample flag that determines which
  rows enter analysis.

## 4. Append/Harmonization Workflow

Use when stacking survey rounds, arms, cohorts, schools, countries, or files.

Pattern:

```stata
use "${dt_clean}/baseline_clean.dta", clear
gen survey_round = "baseline"
tempfile baseline
save `baseline'

use "${dt_clean}/endline_clean.dta", clear
gen survey_round = "endline"

append using `baseline'

assert inlist(survey_round, "baseline", "endline")
isid survey_round student_id
```

Review logic:

- Harmonize variable names and labels before appending when possible.
- Do not use `append, force` as a default.
- Track source file or survey round explicitly.
- Check that value labels mean the same thing across rounds.
- Use `iecodebook append` when harmonization is substantial or repeated.

## 5. Indicator Construction And Sample Flags

Use when creating analysis variables, treatment indicators, indices, and samples.

Pattern:

```stata
use "${dt_clean}/baseline_clean.dta", clear

gen d_treat = (treatment_arm == 1) if !missing(treatment_arm)
label var d_treat "Assigned to treatment"

gen sample_main = !missing(outcome_math, d_treat, school_id)
label var sample_main "Main analysis sample"

egen z_math = std(outcome_math) if sample_main == 1
label var z_math "Math score, standardized"

assert inlist(d_treat, 0, 1) if !missing(d_treat)
assert inlist(sample_main, 0, 1)

iesave "${dt_final}/analysis_data.dta", ///
    idvars(student_id) ///
    version(14) ///
    report ///
    replace
```

Review logic:

- Prefer named sample flags over repeated `if` clauses.
- Justify logs, winsorization, imputation, standardization, and index rules.
- Keep construction out of final output scripts unless it is temporary and local
  to one output.
- Check generated variables against expected ranges and source variables.

## 6. Analysis Output Workflow

Use when producing tables, figures, or in-text statistics.

Minimum standard:

- Start from constructed or analysis-ready data.
- Define sample, treatment, outcomes, covariates, fixed effects, and clustering
  in named locals/macros.
- Export every output by code.
- Save tables/figures to project output folders.
- Make the script rerunnable without relying on hidden results from another
  script.

Pattern:

```stata
use "${dt_final}/analysis_data.dta", clear

local outcomes z_math z_language z_stress
local controls female age baseline_score
local fe i.region
local clust school_id

foreach y of local outcomes {
    regress `y' d_treat `controls' `fe' if sample_main == 1, ///
        vce(cluster `clust')
    estimates store reg_`y'
}

esttab reg_z_math reg_z_language reg_z_stress ///
    using "${out_tables}/main-results.tex", ///
    replace booktabs label se
```

If the user wants the user's personal table style, route to
`stata-latex-tables`.

## 7. Reproducibility Or Code-Review Package

Use when the user asks whether a package is reviewer-ready.

Package evidence to inspect:

- Main run script.
- README with run instructions, software versions, runtime, folder roles, and
  output map.
- Required input data or instructions for acquiring them.
- Scripts that create every reviewed dataset, table, figure, and in-text number.
- Package or ado dependency setup.
- Logs or outputs that prove the scripts ran.

Minimum reviewer README sections:

```text
Purpose
Software and versions
Folder structure
How to run
Inputs
Outputs
Script order and output map
Known limitations
```

Do not call the package DIME-ready if the reviewer cannot map each output back
to the script and data that created it.
