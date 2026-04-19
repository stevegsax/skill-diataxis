+++
title = "How to Score and Revise Documentation"
weight = 52
description = "How to evaluate documentation quality using the scoring rubric"
topic = "scoring"
covers = ["Running a scoring pass", "Reading scores.toml output", "Identifying cross-contamination", "Revising based on scores"]
detail = "Task-focused. Each task gets a short procedure."
+++
## Run a scoring pass

Ask Claude to score the documentation:

```
Score the diataxis documentation
```

Claude reads `diataxis.toml` and evaluates each file against its `covers`,
`detail`, and `guidance` fields, plus the Diataxis quadrant rules.

## Read the output

Scores are written to `diataxis/scores.toml`. Each entry looks like:

```toml
[runs.files."tutorials/first-project.md"]
coverage = { score = 4, justification = "Covers 3 of 4 items. Missing: rendering output." }
detail_compliance = { score = 5, justification = "Step-by-step format as specified." }
guidance_adherence = { score = 3, justification = "Uses a complex example instead of a simple one." }
quadrant_purity = { score = 4, justification = "One paragraph drifts into explanation." }
```

Scores use a 1--5 scale. Each includes a justification.

## Compare after changes

After revising and re-scoring, a comparison table shows what improved or
regressed:

```
File                           Coverage  Detail  Guidance  Quadrant
tutorials/first-project.md     4 → 5     5 → 5   3 → 4     4 → 5
```

## Identify cross-contamination

The most common issue: content drifting into the wrong quadrant. Look for:

- Tutorial paragraphs that explain "why" at length (should link to Explanation)
- Reference docs that walk through steps (should link to How-to)
- How-to guides that teach from scratch (should link to Tutorial)

## Revise based on scores

1. Update the `guidance` field in `diataxis.toml` to reflect the feedback
2. Revise the affected content files
3. Re-score to confirm improvement

For the full scoring rubric, see
[Scoring Rubric](../reference/scoring-rubric.html). For background on why
structure changes come before content changes, see
[Why Structure First](../explanation/why-structure-first.html).
