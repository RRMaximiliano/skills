# Article-to-deck workflow

## Source audit

Inspect, in order:

1. `main.tex`, included section files, metadata, preamble, and bibliography configuration.
2. The compiled paper PDF for visual hierarchy, final numbering, and content that differs from source.
3. `Figs/`, `Tabs/`, and the bibliography database.
4. Labels and cross-references with `rg`.

Record the research question, contribution, setting, identification strategy, main findings, mechanisms, limitations, and the strongest existing visual evidence. Do not infer numerical results or citations that are absent.

## Storyboard

Default to this Montero-depth arc, adapting it to the paper:

1. Motivation and research question
2. Paper overview and findings
3. Contributions and literature
4. Background
5. Conceptual framework
6. Data and empirical strategy
7. Main results
8. Mechanisms
9. Additional outcomes or robustness
10. Conclusion and optional policy implications
11. References
12. Linked appendix

Do not map one paper section to one slide section mechanically. Lead with the question and evidence the audience needs. Use section outline frames as pacing devices.

## Talk length

Ask for duration when absent. If the user does not answer, assume a 45-minute academic seminar and roughly 25–35 substantive main frames, excluding overlay states, references, and appendix. Shorten for conferences; expand motivation, identification, and robustness for job talks or defenses.

## Content rules

- Retain verified findings, notation, numbering, citations, and asset labels.
- Preserve paper figure and table numbers, even when the slide sequence skips numbers.
- Use unnumbered equations unless the talk refers back to them. Preserve a paper equation number only when useful to navigation or discussion.
- Convert paragraphs to claims, evidence, and interpretation—not sentence fragments copied blindly.
- Put derivations, full dense tables, robustness detail, and secondary results in the appendix and link them from the relevant main frame.
- If source is PDF-only, request original figures/tables. Extraction or cropping is a last resort and must be visually checked.

## Shared-project layout

For a new combined project:

```text
project/
├── Article/
├── Beamer/
├── Figs/
├── Tabs/
└── references.bib
```

For an existing article already rooted at `project/`, do not move its files. Add `project/Beamer/` and use `../Figs/`, `../Tabs/`, and `../references.bib` from the deck.
