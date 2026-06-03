# Stata Table Patterns

Use this reference when the user asks to write, review, or improve Stata tables,
especially LaTeX tables for papers, appendices, and reproducibility packages.
These are opinionated patterns drawn from the user's Stata table workflow and
general reproducibility expectations. They are personal conventions, not
official DIME table standards.

## Core Table Philosophy

Tables should be reproducible Stata outputs, not manually edited artifacts. The
preferred workflow is:

1. Define table style and statistics once in the master or table script.
2. Run estimation through small wrapper programs when the same design repeats
   across outcomes, waves, panels, or samples.
3. Store results with `eststo`.
4. Add table-only statistics with `estadd`.
5. Export LaTeX fragments with `esttab using ..., replace/append`.
6. Use `prehead()` and `postfoot()` to create booktabs-compatible panels.
7. Export single in-text estimates as `.tex` snippets when the paper needs
   inline numbers.
8. Keep all table paths under an output macro such as `${outputs}/Tabs`.

## Master-Level Table Setup

Define reusable style macros once. Keep these in the master script or at the
top of a table script when the script must run independently.

```stata
#delimit ;
global stats `"stats(cmean count N,
    labels("Control group outcome mean" "\# of control variables selected" "Obs.")
    fmt(3 0 %9.0gc))"' ;

global style `"label nolines fragment nomtitle nonumbers noobs nodep
    collabels(none) booktabs b(3) se(3)
    star(* 0.10 ** 0.05 *** 0.01)"' ;

global cells `"cells(b(fmt(3) star) se(par fmt(3)) pw(par([ ] )))"' ;
#delimit cr
```

Review checks:

- Style macros are defined before table scripts use them.
- Star levels are consistent across related tables.
- `cells()` matches the stored estimates. For example, do not include `pw`
  unless a p-value matrix has been added with `estadd matrix pw`.
- Output paths are built from project macros.

## Estimation Wrapper Programs

Use wrapper programs when several tables repeat the same specification across
outcomes, waves, experiments, or panels. The wrapper should:

- Accept a `varlist` of outcomes.
- Accept clustering, fixed effects/strata, controls, and treatment variables as
  options.
- Run the model for each outcome.
- Store estimates with systematic names such as `exp1`, `exp2`, `wave1`, etc.
- Add control means, observations, selected-control counts, fixed-effect flags,
  and adjusted p-values with `estadd`.

Pattern:

```stata
capture program drop make_main_estimates
program define make_main_estimates, eclass
    syntax varlist [if] [in], ///
        CLUSter(varname) ///
        STRAta(varname) ///
        CONTROLS(varlist) ///
        TREATment(varname)

    local col = 1
    foreach outcome of local varlist {
        reghdfe `outcome' `treatment' `controls' `if' `in', ///
            absorb(`strata') ///
            vce(cluster `cluster')

        eststo model`col'

        quietly summarize `outcome' if (`treatment' == 0) & e(sample)
        estadd scalar cmean = r(mean) : model`col'
        estadd local groupfe "Yes" : model`col'

        local ++col
    }
end
```

Review checks:

- Wrapper names encode the design, not a vague table number.
- Stored estimate names are predictable and do not collide with prior tables.
- `eststo clear` appears before a new table family.
- Summary statistics are computed on `e(sample)` when they describe the
  estimation sample.
- Clustering and fixed effects are explicit options, not hardcoded surprises.

## Multiple-Hypothesis P-Values

When using adjusted p-values, compute them before the `esttab` export and attach
them to each stored model as a matrix. The table `cells()` can then show ordinary
SEs and adjusted p-values together.

Pattern:

```stata
* Suppose pmatrix has one row per outcome and one column named treatment.
matrix pw = pmatrix[`row', 1]
matrix colnames pw = treatment
estadd matrix pw : model`row'

esttab model* using "${out_tabs}/table-main.tex", ///
    replace ${style} ${stats} ///
    cells(b(fmt(3) star) se(par fmt(3)) pw(par([ ] ))) ///
    keep(treatment) nocons
```

Review checks:

- Matrix row order matches the outcome order in the table.
- Matrix column name matches the coefficient kept in `esttab`.
- The table note explains what bracketed p-values represent.
- Bootstrap/repetition count and seed are set in a visible setup block.

## Panel Tables With `esttab`

Use `replace` for the first panel and `append` for later panels. Put the
complete `tabular` opening in the first `prehead()` and close the table with
`postfoot()` on the last panel.

Pattern:

```stata
eststo clear
make_main_estimates y1 y2 y3, ///
    cluster(cluster_id) ///
    strata(strata_id) ///
    controls(`controls') ///
    treatment(treatment)

esttab model* using "${out_tabs}/table-outcomes.tex", ///
    replace ${style} ${stats} ${cells} ///
    keep(treatment) nocons ///
    prehead(`"\begin{tabular}{@{}l*{3}{c}}"' ///
            `"\toprule"' ///
            `" & Outcome 1 & Outcome 2 & Outcome 3 \\"' ///
            `" & (1) & (2) & (3) \\"' ///
            `"\midrule"' ///
            `"\multicolumn{4}{@{}l}{\textbf{Panel A. Sample A}} \\"')

esttab model_b* using "${out_tabs}/table-outcomes.tex", ///
    append ${style} ${stats} ${cells} ///
    keep(treatment) nocons ///
    prehead(`"\midrule \multicolumn{4}{@{}l}{\textbf{Panel B. Sample B}} \\"') ///
    postfoot(`"\bottomrule \end{tabular}"')
```

Review checks:

- The first export uses `replace`; subsequent panels use `append`.
- Exactly one table opening and one table closing are written.
- `booktabs` commands are balanced and intentional.
- Column counts in `tabular`, headers, model columns, and panel labels agree.
- File names map clearly to manuscript table numbers.

## In-Text Estimate Snippets

For in-text results, export each number to a small `.tex` file from the same
estimation code that creates the table. This avoids manually copying numbers
into the manuscript.

Pattern:

```stata
capture program drop send_estimate
program define send_estimate
    syntax using/, VALUE(string)

    file open outfile using "`using'", write replace
    file write outfile "`value'"
    file close outfile
end

local beta : display %04.2f _b[treatment]
send_estimate using "${out_est}/main_beta.tex", value("`beta'")
```

Review checks:

- Snippets come from the same model used in the table.
- Formatting is explicit.
- Snippet filenames are stable and descriptive.
- The README or output map indicates which script creates snippets.

## Custom Balance Tables From `iebaltab`

Use `iebaltab` directly when its standard output is enough. For custom
publication tables, a practical workflow is:

1. Run `iebaltab` once for standard errors and save the browsed table to a
   temporary dataset.
2. Run `iebaltab` again for coefficients/differences.
3. Merge the two temporary table datasets.
4. Combine coefficient and SE strings into publication cells.
5. Insert panel rows, F-test rows, and custom labels.
6. Export with a table-data-to-LaTeX utility such as `texsave_custom`.

Pattern:

```stata
preserve
    iebaltab `balance_vars' if (baseline_sample == 1), ///
        groupvar(treatment) ///
        fixedeffect(strata) ///
        vce(cluster cluster_id) ///
        browse ///
        stats(desc(se) pair(se)) ///
        order(1 0) ///
        nostars ///
        rowvarlabels ///
        format(%9.2f) ///
        onerow

    gen row_id = _n
    tempfile balance_se
    save `balance_se'
restore

preserve
    iebaltab `balance_vars' if (baseline_sample == 1), ///
        groupvar(treatment) ///
        fixedeffect(strata) ///
        vce(cluster cluster_id) ///
        browse ///
        stats(desc(se) pair(beta)) ///
        order(1 0) ///
        starlevels(.1 .05 .01) ///
        rowvarlabels ///
        format(%9.2f) ///
        onerow

    gen row_id = _n
    merge 1:1 row_id using `balance_se', nogen
    * Combine beta and SE columns here.
    tempfile balance_table
    save `balance_table'
restore
```

Review checks:

- `browse` is used intentionally to create a dataset for post-processing. Do not
  leave unrelated `browse` or interactive commands in production scripts.
- Merge keys for table post-processing are stable. Prefer an explicit row
  number variable over bare `merge using`.
- Manual row insertion is documented and deterministic.
- F-test p-values are computed from the exact variable list and sample used in
  the balance table.
- Categorical variables are converted to dummies before `iebaltab`.
- The exported LaTeX table is created entirely by code.
- `starsnoadd` may appear in older code, but prefer the current `nostars`
  option when suppressing stars.

## Table Review Checklist

Flag table code when:

- Style globals are duplicated with inconsistent values across files.
- A table script depends on results left in memory by a previous script.
- `esttab` exports omit `replace` or `append` intentionally.
- A table reports control means not restricted to `e(sample)`.
- Panel headers or model counts no longer match the estimates.
- Adjusted p-values are added without explaining their method.
- Output table files are not generated by the master script.
- Table scripts contain hardcoded local machine paths.
