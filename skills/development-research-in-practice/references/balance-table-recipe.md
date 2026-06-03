# Balance Table Recipe

Use this reference when the user asks for a balance table, especially with
`iebaltab`. This is DIME-style implementation guidance, not the user's personal
Stata-to-LaTeX table style.

## Decision Path

1. Confirm the unit of observation.
2. Confirm the treatment/group variable and whether the design is binary or
   multi-arm.
3. Confirm the control group code.
4. Define the sample flag.
5. Inspect balance variables:
   - continuous variables can enter directly;
   - binary variables can enter directly;
   - categorical variables must be expanded to indicators first;
   - IDs, dates, strings, labels, and post-treatment outcomes do not belong in
     baseline balance unless explicitly justified.
6. Confirm clustering, strata/fixed effects, and covariates based on the design.
7. Export to a reproducible file, usually `.tex`; add `.csv` if review/debugging
   is useful.

## Pre-Checks

```stata
assert !missing(student_id)
isid student_id

assert inlist(treatment_arm, 0, 1) if !missing(treatment_arm)
assert inlist(sample_baseline, 0, 1)

tab treatment_arm if sample_baseline == 1, missing
```

For clustered assignment:

```stata
isid school_id treatment_arm if sample_baseline == 1
```

Use a project-specific version of the cluster check when the treatment is
assigned at the school, village, classroom, or group level.

## Convert Categoricals To Dummies

If `parent_educ` is coded 1/2/3/4, do not include it as continuous. Create
indicators:

```stata
tab parent_educ, gen(d_parent_educ_)

label var d_parent_educ_1 "Parent education: primary or less"
label var d_parent_educ_2 "Parent education: secondary"
label var d_parent_educ_3 "Parent education: tertiary"
label var d_parent_educ_4 "Parent education: other"
```

Decide whether to omit one category. For balance tables, showing all categories
can be useful for transparency, but avoid redundant rows if the table becomes
too long.

## Binary Treatment-Control Table

```stata
local balance_vars ///
    age_year ///
    female ///
    baseline_math ///
    baseline_language ///
    d_parent_educ_1 ///
    d_parent_educ_2 ///
    d_parent_educ_3

iebaltab `balance_vars' if (sample_baseline == 1), ///
    groupvar(treatment_arm) ///
    control(0) ///
    total ///
    rowvarlabels ///
    stats(desc(sd) pair(diff p) f(p)) ///
    vce(cluster school_id) ///
    savetex("${out_tables}/balance-table.tex") ///
    savecsv("${out_tables}/balance-table.csv") ///
    replace
```

## Multi-Arm Table

```stata
iebaltab `balance_vars' if (sample_baseline == 1), ///
    groupvar(treatment_arm) ///
    order(0 1 2) ///
    grouplabels("0 Control @ 1 Treatment A @ 2 Treatment B") ///
    total ///
    rowvarlabels ///
    stats(desc(sd) pair(diff p) feq(p)) ///
    vce(cluster school_id) ///
    savetex("${out_tables}/balance-table.tex") ///
    savecsv("${out_tables}/balance-table.csv") ///
    replace
```

## Review Checklist

Flag the table if:

- The control group is implicit.
- The analysis sample is implicit or repeated only as a long `if` condition.
- Categorical variables enter as numeric scales without justification.
- Clustered assignment is analyzed without clustered standard errors.
- The exported file is outside the project output folder.
- The table cannot be reproduced from the master script.
- Output is manually copied into a paper or slide deck.

## Interpretation Checks

After running the table:

- Confirm group counts match the randomization or baseline sample.
- Confirm no row is a variable that should have been excluded or converted.
- Confirm standard errors and p-values use the intended design.
- Confirm final table notes explain sample, groups, clustering, and variable
  definitions.
- If many covariates are tested, consider whether the project needs a joint test
  or multiple-hypothesis adjustment.
