# Stata Command Cards

Use these cards when the user asks for DIME Stata commands or when the task
matches a command's workflow. Check command help for edge cases.

## `ieboilstart`

Purpose: harmonize Stata settings for collaboration and reproducibility.

Use when writing a master do-file, starting a reproducibility package, or
reviewing whether code can run from a fresh session.

Minimum pattern:

```stata
cap which ietoolkit
if (_rc == 111) ssc install ietoolkit

ieboilstart, versionnumber(18.0)
`r(version)'
```

Project-specific ado pattern:

```stata
global project_root "C:/Users/username/Documents/GitHub/project"
global ado         "${project_root}/ado"

ieboilstart, versionnumber(18.0) adopath("${ado}", strict)
`r(version)'
```

Review checks:

- `r(version)` appears immediately after `ieboilstart`.
- Use `versionnumber()` or the abbreviated option `v()`, not `version()`.
- The version is stable and not changed casually after randomization.
- User-written command dependencies are installed or bundled.
- `varabbrev` is off directly or through `ieboilstart`.
- For reproducibility packages, prefer a project-specific `ado/` folder rather
  than relying on user-installed packages.

## `iebaltab`

Purpose: produce difference-in-means balance tables across treatment or group
categories.

Use when creating baseline balance tables, treatment-control comparison tables,
or reviewable analysis outputs.

Pre-checks:

- `ietoolkit` is installed or available.
- `groupvar()` is a single numeric integer variable.
- `groupvar()` has clear value labels or explicit `grouplabels()`.
- Balance variables are continuous or binary. Convert categorical variables to
  binary indicators before including them.
- The analysis sample restriction is explicit.
- The control group code is explicit if the table is treatment-versus-control.
- Clustering, fixed effects, and covariates are chosen intentionally.
- Output path uses a project output macro and includes `replace`.

Basic treatment-control table:

```stata
local balance_vars age_year educ_year d_employed ride_frequency

iebaltab `balance_vars' if (analysis_sample == 1), ///
    groupvar(treatment_arm) ///
    control(0) ///
    total ///
    rowvarlabels ///
    stats(desc(sd) pair(diff p) f(p)) ///
    vce(cluster cluster_id) ///
    savetex("${out_tables}/balance-table.tex") ///
    replace
```

Multi-arm table with custom labels:

```stata
iebaltab `balance_vars' if (baseline_sample == 1), ///
    groupvar(treatment_arm) ///
    order(0 1 2) ///
    grouplabels("0 Control @ 1 Treatment A @ 2 Treatment B") ///
    total ///
    rowvarlabels ///
    stats(desc(sd) pair(diff p) feq(p)) ///
    savecsv("${out_tables}/balance-table.csv") ///
    replace
```

Common mistakes to flag:

- Including variables such as `marital_status` coded 1/2/3 as if continuous.
- Leaving the control group implicit.
- Omitting cluster-robust variance when treatment assignment is clustered.
- Saving only to Excel when a Git-friendly table is expected.
- Relying on default notes for a final publication table.

## `iesave`

Purpose: save datasets after reproducibility-oriented checks.

Use when saving cleaned, constructed, or final analysis datasets.

Pattern:

```stata
iesave "${dt_final}/baseline-clean.dta", ///
    idvars(household_id) ///
    version(14) ///
    report ///
    replace
```

Review checks:

- ID variables fully and uniquely identify observations.
- `isid` would pass for the specified IDs.
- The `.dta` save version is explicit and compatible with the team or package.
- A metadata report is used when changes to data should be trackable in Git.
- Final datasets are saved once at the end of the task.
- The dataset is compressed and labeled where appropriate.

## `iefolder`

Purpose: create DIME-style project folder structures and master do-files.

Use when setting up a new Stata research data project or aligning an existing
project to DIME conventions.

Practical guidance:

- Prefer using `iefolder` for new projects when Stata is available.
- When writing without running Stata, mirror its principles: master script,
  data folders, documentation folders, output folders, and task-level do-files.
- Do not impose `iefolder` mechanically on mature projects unless the user asks
  for restructuring.

## `ieduplicates` and `iecompdup`

Purpose: detect, compare, and resolve duplicate records in survey or primary
data workflows.

Use when reviewing data cleaning around repeated submissions, duplicate IDs,
or survey completion checks.

Review checks:

- Duplicate resolution is documented and stable.
- Code does not use `duplicates drop, force` as a substitute for review.
- Resolution preserves an audit trail or correction record.
- The final cleaned dataset passes `isid` on the intended ID.
- `ieduplicates` is run on the raw data that still contains all duplicates,
  because it reads and reapplies corrections from the existing Excel report.
- `uniquevars()` identifies rows within duplicate groups so corrections can be
  merged back reliably.

Pattern:

```stata
ieduplicates respondent_id using "${doc}/duplicates-report.xlsx", ///
    uniquevars(submission_id) ///
    keepvars(interviewer survey_date village)
```

Use `force` only when the team has intentionally accepted dropping unresolved
duplicates; do not include it as the default pattern.

## `iecodebook` and `iecorrect`

Purpose: use structured spreadsheet instructions to clean, harmonize, document,
and correct datasets.

Use when a cleaning workflow needs to be understandable to nontechnical team
members, repeatedly applied across survey rounds, or documented in a codebook.

Apply pattern:

```stata
iecodebook template using "${doc}/baseline-codebook.xlsx", replace
* Fill the spreadsheet, then run:
iecodebook apply using "${doc}/baseline-codebook.xlsx", ///
    missingvalues(.d "Don't know" .r "Refused" .n "Not applicable")
```

Append/harmonization pattern:

```stata
iecodebook template ///
    "${dt_clean}/baseline.dta" ///
    "${dt_clean}/endline.dta" ///
    using "${doc}/harmonization.xlsx", ///
    surveys(Baseline Endline) ///
    replace

iecodebook append ///
    "${dt_clean}/baseline.dta" ///
    "${dt_clean}/endline.dta" ///
    using "${doc}/harmonization.xlsx", ///
    clear surveys(Baseline Endline) ///
    generate(survey_round) ///
    report replace
```

Export pattern:

```stata
iecodebook export using "${doc}/analysis-codebook.xlsx", ///
    replace signature
```

Review checks:

- The codebook/correction spreadsheet is in the repository or package.
- Corrections are documented outside ad hoc code comments.
- Variable labels, value labels, recodes, and drops align with the codebook.
- Cleaned data are checked after applying the codebook.

## `ietestform`

Purpose: test SurveyCTO/ODK form programming against data-quality practices.

Use when the task is survey instrument QA before data collection.

Review checks:

- The form is tested before field launch.
- Issues likely to create Stata import or cleaning problems are addressed.
- Survey metadata assumptions are documented.

Pattern:

```stata
ietestform using "${form}/baseline.xlsx", ///
    reportsave("${output}/ietestform-report.csv") ///
    date replace
```

## `iegraph`

Purpose: graph treatment effects from common impact evaluation regressions.

Use immediately after a regression, or after restoring stored estimates, when
the model is OLS with treatment dummies or a simple difference-in-differences
setup.

Pattern:

```stata
regress outcome treatment_1 treatment_2 covariates, vce(cluster cluster_id)
iegraph treatment_1 treatment_2, ///
    basictitle("Treatment effect on outcome") ///
    yzero ///
    save("${out_graphs}/treatment-effect.gph")
graph export "${out_graphs}/treatment-effect.png", replace
```

Review checks:

- The graph is created from the intended regression result.
- Treatment dummies match the omitted control group.
- The exported graph is reproducible and not manually edited.
- Use `r(cmd)` with `norestore` only for debugging graph options.

## `iekdensity`

Purpose: plot kernel densities by treatment assignment, optionally adding
descriptive statistics or treatment-effect notes.

Use for distributional balance or outcome exploration by treatment arm.

Pattern:

```stata
iekdensity outcome if (analysis_sample == 1), ///
    by(treatment_arm) ///
    stat(mean) ///
    effect ///
    control(0) ///
    regressionoptions(cluster cluster_id)
graph export "${out_graphs}/outcome-density.png", replace
```

Review checks:

- Outcome is continuous and numeric.
- Treatment variable is a dummy or factor variable.
- Control group is explicit for treatment-effect notes.
- Regression options align with the analysis design.

## `iematch`

Purpose: match base observations to target observations on a single continuous
matching variable.

Use for nearest-value matching workflows, commonly treatment-to-control matching
on a score or baseline measure.

Pattern:

```stata
isid respondent_id
set seed 987654

iematch, ///
    grpdummy(treated) ///
    matchvar(propensity_score) ///
    idvar(respondent_id) ///
    maxdiff(.05) ///
    seedok
```

Review checks:

- `grpdummy()` is numeric and only 0/1/missing.
- `matchvar()` is numeric and continuous.
- `idvar()` uniquely identifies observations.
- A seed is set before matching when duplicate match values exist.
- Panel data are not accidentally matched across repeated observations.

## `ieddtab`

Purpose: produce difference-in-differences tables with baseline means, first
differences, and the second difference.

Use for simple two-period, treatment-control diff-in-diff summaries.

Pattern:

```stata
ieddtab outcome_1 outcome_2 if (analysis_sample == 1), ///
    time(post) ///
    treatment(treated) ///
    covariates(age_year educ_year) ///
    vce(cluster cluster_id) ///
    rowlabtype(varlabel) ///
    savetex("${out_tables}/diff-in-diff.tex") ///
    replace
```

Review checks:

- `time()` and `treatment()` are 0/1/missing dummies.
- The table sample is the second-difference regression sample.
- Covariates and clustering match the analysis plan.
- The output note explains the specification.

## Balance Table Decision Guide

When asked to "make a balance table":

1. Identify the treatment/group variable and control group.
2. Identify the baseline variables; exclude post-treatment variables.
3. Convert categorical balance variables to dummies.
4. Decide sample restriction.
5. Decide variance estimator: robust, clustered, bootstrap, or default.
6. Decide fixed effects/covariates only if part of the design or specification.
7. Export reproducibly to `.tex`, `.csv`, or `.xlsx`.
8. Add assertions for group codes, sample size, and variable availability.
