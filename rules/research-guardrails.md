# Research guardrails

These rules apply to empirical research code and writing (Stata, R, Python,
LaTeX). They override any skill default that conflicts with them, including
pstack's "never block on the human".

1. Identification decisions are mine. Do not change sample restrictions,
   estimators, fixed effects, clustering, controls, or outcome and treatment
   definitions without asking, even when the edit is easy to undo. Propose
   the change with evidence and let me decide.
2. Never set a goal about an estimate. Loops, hillclimbs, arenas, and
   autonomous runs may aim for reproducibility, correctness, runtime, or
   coverage. They never aim for a coefficient's size, sign, or significance.
3. Name the estimand before choosing the estimator.
4. Every number you report traces to code and a run. State N, the sample,
   and the output file it came from. A do-file that ran without errors is
   not proof that the result is right.
5. Fix data problems where they start, and record every dropped observation
   with its reason.
6. Make runs deterministic and safe to restart: set seeds, sort on unique
   keys or use stable sorts, and overwrite outputs instead of appending to
   them.
7. When a reference output changes, classify the change as an intended
   specification change, a new data vintage, or a regression. Never update a
   reference just to make a check pass.
8. Restricted data stays local. Keep raw records out of prompts, subagents,
   and multi-model panels, and use synthetic fixtures for tests.
