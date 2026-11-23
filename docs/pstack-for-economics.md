# pstack for economics

How I use [pstack](https://github.com/cursor/plugins/tree/main/pstack), Lauren
Tan's (poteto's) engineering skill stack, for empirical economics work. If a
pstack skill already does a job, I use it. This repo adds only what pstack
lacks.

## Setup

| Agent | Install | Run |
|---|---|---|
| Claude Code | `claude plugin marketplace add cursor/plugins` then `claude plugin install pstack@cursor-plugins` | `/pstack:poteto-mode <task>` |
| Codex | `codex plugin marketplace add michael-denyer/pstack-claude` then `codex plugin add pstack@pstack-claude` | `$poteto-mode <task>` |

After installing, run `setup-pstack` once in each agent. In Codex, also turn
on the routing hook under `/hooks`.

Companion skill from another repo, which I install rather than copy:

```bash
npx skills@latest add ctfysh/craft-of-research -g   # Socratic research-question guide
```

## The layer this repo adds

- [`rules/research-guardrails.md`](../rules/research-guardrails.md): always-on
  rules that tell the agent where research practice differs from pstack's
  defaults. Load it from `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md`.
- The econ skills in `skills/` (tables, articles, Beamer, DIME workflow).

Not built, because pstack already covers each one:

| Need | pstack skill to use |
|---|---|
| Personal working mode | `poteto-mode`, or `automate-me` to write a personal mode skill |
| Referee-style review | `interrogate`, framed as referees who must cite a table, code line, or run |
| Checking a reported number | `principle-explain-the-number` (applied by `poteto-mode`) |
| Replication verification | `create-verification-skill`, which writes the check into each project |
| Import checks, sample ledger | `correct` and the Feature playbook, which add asserts to the project's own code |
| Spec registry | `architect` + `principle-model-the-domain` |
| Checking paper numbers | `swarm`, or a script built under `principle-build-the-lever` |

The one possible gap is an `identify` skill that questions an identification
strategy. Build it only if `craft-of-research`, prompted toward
identification, falls short.

## Skills by pipeline stage

| Stage | Skills | Principles |
|---|---|---|
| Import raw | `how`, `tdd` | boundary-discipline |
| Clean and merge | `correct`, `blast-radius` | fix-root-causes, model-the-domain |
| Construct variables | `architect`, `interrogate` | foundational-thinking, test-behavior-not-implementation |
| Estimate | `swarm`, `show-me-your-work` | explain-the-number, make-operations-idempotent |
| Tables and figures | `create-verification-skill` | build-the-lever, prove-it-works |
| Package and ship | `technical-writing`, `unslop`, `swarm` | sequence-verifiable-units |

## Verification for a research project

Run `/pstack:create-verification-skill` in each project and give it the
layers below. pstack calls this generated skill `verify-<app>`. Here it
checks the pipeline. Its feature map has one file per table, figure, or key
number.

| Layer | What it checks |
|---|---|
| 0. Environment check | Stata/R and package versions, raw-file checksums, seeds |
| 1. Import contracts | `isid`, expected N per year, value ranges, missing-value rates, value labels |
| 2. Step invariants | N in and N out at each step with reasons, merge counts, unique keys |
| 3. Reference outputs | Coefficient, SE, N, clusters, and R² per table cell, compared after a clean rerun from raw |
| 4. Determinism | Two runs give identical outputs |
| 5. Paper vs. outputs | Every number in the `.tex` traces to an output file |
| 6. Known truth | Simulated data with a planted effect, run through the real estimation code |
| 7. Checks can fail | Each layer turns red on a deliberately broken variant |

Start with layers 2, 3, and 4. Add layer 6 for the main estimator.

Before reporting an estimate, check these points:

1. Did it run on the sample you think it did? Check N, clusters, and
   `e(sample)`.
2. Did anything fail quietly? Look for `capture`, `quietly`, omitted
   collinear variables, and dropped singletons.
3. Did the step run? Check the file contents and the log, not the timestamp.
4. Is the difference bigger than the noise from seeds, bootstraps, or
   permutations?
5. Is the size plausible relative to the outcome's standard deviation?
6. What else could it be measuring? Consider sample composition, missing
   values coded as 0, or a mechanical correlation.
7. Keep the run, N, seed, and data checksum with the number.

## Recipes

```text
/pstack:poteto-mode Table 2 col 3 went from 0.124 to 0.091 after the 2025 data refresh. Reproduce on both vintages, split the change into sample composition versus variable definitions, and find the first step where they diverge. Do not change any specifications.

/pstack:poteto-mode Refactor code/03_analysis/. Pin current outputs first. Target: one sample and spec registry. Results must match to within 1e-8.

/pstack:swarm For each table and figure in paper/main.tex, one worker: regenerate it and check every number the text cites against the output.

/pstack:correct Recurring mistakes: merges without assert(), m:m merges, "if x > 0" including missing, absolute paths. Turn each into a check that fails loudly, and prove each one catches a real past case.

/pstack:interrogate Act as three referees on the identification in code/02_construct/treatment.do. Every objection must cite a table, a line of code, or a run.
```
