# Review Rubric

Use this rubric when the user asks for a code review, reproducibility review, or
DIME-style audit. Lead with findings ordered by severity.

## Severity Levels

`P0`: Blocking reproducibility or data integrity.

- The workflow cannot run from a fresh session.
- The wrong data, sample, unit of observation, or merge logic can change the
  estimates.
- Randomization or treatment assignment can be regenerated or altered
  unintentionally.
- Important datasets are saved without unique ID checks and the unit of
  observation is ambiguous.

`P1`: Likely to affect estimates, tables, or reviewer trust.

- Merge mismatches or drops are ignored.
- Missing-value logic is probably wrong.
- Clustered or stratified design is not reflected in analysis.
- Balance-table variables are misclassified.
- Output depends on hidden state from a previous script.

`P2`: Fragile reproducibility or maintainability.

- Hardcoded paths exist outside the setup block.
- Packages are undeclared or rely on local installations.
- Script order is implied rather than documented.
- Outputs are exported inconsistently or without clear mapping.
- Sample restrictions are scattered and hard to audit.

`P3`: Style, clarity, or polish.

- Names are unclear.
- Comments do not explain non-obvious decisions.
- Sectioning is inconsistent.
- Labels or output file names could be clearer.

## Finding Format

Use this structure:

```text
P1 - Merge mismatches are ignored
File: Code/1_clean/merge_baseline.do:42
Why it matters: Unmatched observations may change the analysis sample silently.
DIME checklist area: Data management / merge checks.
Concrete fix: Count each `_merge` category, document expected unmatched records,
and assert the required merge status for `sample_main`.
```

## Review Rules

- Findings first, then open questions, then a short summary.
- Do not bury P0/P1 issues under style comments.
- If no high-severity issues are found, say so and list remaining test gaps.
- Prefer concrete fixes over general advice.
- Mention when Stata could not be run and findings are based on static review.

## Approval Language

Avoid saying "DIME-ready" unless the evidence proves:

- Fresh-session run path is clear.
- Paths and packages are explicit.
- IDs and units of observation are checked.
- Data transformations are documented and verified.
- Analysis choices are explicit.
- Outputs are reproducible.
- Reviewers can map inputs, scripts, and outputs without guessing.
