# Skills

My opinionated agent skills, organized as an installable skills collection.

This repository is mainly for my personal use. The skills reflect my preferred
workflows, tools, and conventions. Treat them as personal defaults rather than
neutral guidance.

This repository follows the standard `skills` CLI layout:

```text
skills/
  <skill-name>/
    SKILL.md
    references/
    scripts/
    assets/
```

Only `SKILL.md` is required for each skill. Reference files, scripts, and assets
are optional.

## Available Skills

- `development-research-in-practice`: DIME-style Stata/R research data workflow,
  `iebaltab`/ietoolkit, reproducibility, and review.
- `stata-latex-tables`: opinionated Stata-to-LaTeX table workflows using
  `eststo`, `esttab`, `estadd`, panel table fragments, custom balance tables,
  and reproducible paper-ready outputs.
- `latex-paper-templates`: personal economics paper LaTeX templates using
  `article`, `natbib`, AER bibliography style, `threeparttable` table wrappers,
  input-based table fragments, configured captions, and figure conventions.
- `latex-beamer`: personal crimson economics Beamer slide templates using
  `slides_updated`, `math`, appendix navigation buttons, input-based tables,
  configured figures, and `biblatex` references.

## Choosing a Skill

- DIME-style data workflow or review: `development-research-in-practice`
- My Stata-to-LaTeX table style: `stata-latex-tables`
- My paper container and preamble: `latex-paper-templates`
- My crimson Beamer slide style: `latex-beamer`

## Maintenance

- Keep `description` under 180 characters.
- Keep `SKILL.md` under 250 words when possible.
- Put stable facts, command patterns, and checklists in references.
- Prefer scripts and assets over prose for repeatable work.
- Delete skill prose when it only steers model behavior.

## Install

Install with the `skills` CLI:

```bash
npx skills@latest add RRMaximiliano/skills
```

Install only one skill:

```bash
npx skills@latest add RRMaximiliano/skills --skill development-research-in-practice
npx skills@latest add RRMaximiliano/skills --skill stata-latex-tables
npx skills@latest add RRMaximiliano/skills --skill latex-paper-templates
npx skills@latest add RRMaximiliano/skills --skill latex-beamer
```

Install globally for Codex:

```bash
npx skills@latest add RRMaximiliano/skills \
  --skill development-research-in-practice \
  --agent codex \
  --global
```

Install from a direct GitHub path:

```bash
npx skills@latest add \
  https://github.com/RRMaximiliano/skills/tree/main/skills/development-research-in-practice

npx skills@latest add \
  https://github.com/RRMaximiliano/skills/tree/main/skills/stata-latex-tables

npx skills@latest add \
  https://github.com/RRMaximiliano/skills/tree/main/skills/latex-paper-templates

npx skills@latest add \
  https://github.com/RRMaximiliano/skills/tree/main/skills/latex-beamer
```

For local testing before publishing:

```bash
npx skills@latest add . --list
```

## Adding a Skill

Create a new folder under `skills/`:

```text
skills/new-skill-name/
  SKILL.md
```

Use lowercase hyphenated names. Keep the main `SKILL.md` focused and move
longer examples or implementation details into `references/`.
