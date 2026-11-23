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

After installing, run `setup-pstack` once in each agent.

- Claude Code writes the model sheet to `~/.claude/rules/pstack-models.md`,
  which loads into every session. The official plugin has no session hook, so
  call `/pstack:poteto-mode` yourself.
- Codex writes `~/.codex/pstack-models.md`. Its step 7 pastes the model rows
  into `~/.codex/AGENTS.md`. Skip that step when `AGENTS.md` is a symlink to
  the guardrails, or the rows land in this repo. Then trust the routing hook
  under `/hooks` in the Codex terminal app.

When a project's git repo sits inside a larger folder (for example `Analysis/`
inside a Dropbox project), a session started at the outer folder does not list
the repo's project skills until it reads a file inside the repo. Start sessions
in the repo, or add a one-line pointer to a `CLAUDE.md` in the outer folder.

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
| 3. Reference outputs | Every cell each table exports (coefficient, SE, N, p-value, and clusters or R² where exported), compared after a clean rerun from raw, with references keyed to the data snapshot |
| 4. Determinism | Two runs give identical datasets and tables, compared with a row hash or with `cf` after sorting on a unique key |
| 5. Paper vs. outputs | Every number in the `.tex` traces to an output file |
| 6. Known truth | Simulated data with a planted effect, run through the real estimation code |
| 7. Checks can fail | Every check turns red on a broken variant aimed at it: one variant per check, not per layer |

Start with layers 2, 3, and 4, and prove each check with layer 7. Add layer 6
for the main estimator.

How to build it:

- Run the pipeline in throwaway copies: a copy of the code, read-only inputs,
  empty output folders, and no credentials folder. That makes the guardrails
  hold by construction: no downloads, no writes to frozen inputs, and every run
  starts from raw. It also lets broken variants and proposed edits run without
  touching the real code.
- Stata batch mode exits 0 even when a do-file fails. Decide whether a run
  succeeded by reading the log.
- `datasignature` checksums each column separately, so it misses reordered
  rows and values swapped between rows, which is what a bad merge produces.
  Don't use it alone to prove two datasets are the same.
- Store references with the snapshot ID they came from. A new snapshot shows
  "no reference" until I classify the change (rule 7) and approve the new
  reference.
- Evidence is counts, hashes, and table cells. Logs that list study IDs stay
  local and never go into the report.

A first trial on a Stata RCT pipeline produced 118 checks and 27 broken
variants. A full verification run (two reruns from raw plus all checks) took
about 9 seconds. Fast pipelines make full reruns cheap. For slow ones, use the
master's step switches to rerun only the affected steps.

## Where pstack fits research badly

`create-verification-skill` is written for apps, so translate its terms:
launching the app means building a run copy and running the master do-file,
and "ready" means the log reports that the run completed. Watch these
mismatches:

- pstack's proof standard is driving one feature once. Research needs every
  check on every run, reference outputs with tolerances, determinism, and
  proof that checks can fail. Those come from the layer table above, not from
  pstack.
- pstack's "capture all the evidence" conflicts with rule 8. Report
  aggregates only.
- pstack's "if it doesn't build, fix it first" conflicts with rule 1. Ask
  before editing pipeline code, and show the diff.
- pstack's generic web checks (ports, accessibility, seed data) don't apply.
  The real checks come from the DIME checklist and
  `audit_stata_project.py` in `development-research-in-practice`.

Before reporting an estimate, check these points:

1. Did it run on the sample you think it did? Check N, clusters, and
   `e(sample)`.
2. Did anything fail quietly? Look for `capture`, `quietly`, omitted
   collinear variables, and dropped singletons.
3. Did the step run? Check the file contents and the log, not the timestamp
   or the exit code.
4. Is the difference bigger than the noise from seeds, bootstraps, or
   permutations?
5. Is the size plausible relative to the outcome's standard deviation?
6. What else could it be measuring? Consider sample composition, missing
   values coded as 0, or a mechanical correlation.
7. Keep the run, N, seed, and data checksum with the number.

## Recipes

```text
/pstack:create-verification-skill Build a verification skill for this Stata pipeline: layers 2, 3, and 4 from docs/pstack-for-economics.md, with one broken variant per check. Run in throwaway copies, never download data or write to frozen inputs, report aggregates only, and ask before editing any existing do-file. Use the DIME checklists and audit script as the source of checks. Don't commit.

/pstack:poteto-mode Table 2 col 3 went from 0.124 to 0.091 after the 2025 data refresh. Reproduce on both vintages, split the change into sample composition versus variable definitions, and find the first step where they diverge. Do not change any specifications.

/pstack:poteto-mode Refactor code/03_analysis/. Pin current outputs first. Target: one sample and spec registry. Results must match to within 1e-8.

/pstack:swarm For each table and figure in paper/main.tex, one worker: regenerate it and check every number the text cites against the output.

/pstack:correct Recurring mistakes: merges without assert(), m:m merges, "if x > 0" including missing, absolute paths. Turn each into a check that fails loudly, and prove each one catches a real past case.

/pstack:interrogate Act as three referees on the identification in code/02_construct/treatment.do. Every objection must cite a table, a line of code, or a run.
```
