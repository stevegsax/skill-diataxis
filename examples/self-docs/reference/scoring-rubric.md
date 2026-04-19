+++
title = "Scoring Rubric"
weight = 54
description = "How to evaluate documentation quality using the scoring rubric"
topic = "scoring"
covers = ["The 1-5 score scale with definitions", "Project-level criteria (decomposition, balance, audience, completeness)", "Structural criteria (coverage, detail compliance, guidance adherence, cross-linking)", "Quadrant-level criteria per type", "The scores.toml output format"]
detail = "Tabular. One table per scoring level. Include the comparison format."
+++
## Score scale

| Score | Meaning |
|-------|---------|
| 5 | Fully meets criteria |
| 4 | Meets criteria with minor issues |
| 3 | Partially meets criteria, notable gaps |
| 2 | Significant gaps or violations |
| 1 | Does not meet criteria |

Each score includes a justification explaining why and what would improve it.

## Project-level criteria

| Criterion | Weight | What to check |
|-----------|--------|---------------|
| Topic decomposition | High | Are topics appropriately scoped? Gaps or redundancies? |
| Quadrant balance | Medium | Are the four quadrants used appropriately for this project type? |
| Audience alignment | High | Does complexity match the stated audience? |
| Completeness | Medium | What percentage of planned files have content? |

## Structural criteria (per file)

| Criterion | Weight | What to check |
|-----------|--------|---------------|
| Coverage | High | Is each item in `covers` addressed? |
| Detail compliance | Medium | Does the file match the depth and format in `detail`? |
| Guidance adherence | High | Does the file follow the instructions in `guidance`? |
| Cross-linking | Medium | Does the file link to sibling quadrant documents? |
| Exercise presence | Low | If exercises are listed, do the files exist and are they linked? |

## Quadrant criteria

### Tutorial scoring

| Criterion | What to check |
|-----------|---------------|
| Action-oriented | Does every section contain steps? |
| Results shown | Are results visible within every 3 steps? |
| Narrative of expected | Does it say what the learner should see? |
| Minimal explanation | Are explanations brief (1--2 sentences) with links? |
| No choices | Does it avoid presenting alternatives? |
| Completable | Does it reach a defined endpoint? |

### How-to scoring

| Criterion | What to check |
|-----------|---------------|
| Task-focused | Does the title state a task? |
| No teaching | Does it avoid explaining fundamentals? |
| Assumes competence | Does it skip basics? |
| Actionable steps | Is every step something the reader can do? |

### Reference scoring

| Criterion | What to check |
|-----------|---------------|
| Description only | Free of instruction and opinion? |
| Consistent structure | Do all items follow the same format? |
| Mirrors subject | Does doc structure reflect the thing it describes? |
| Brief examples | Are examples short and illustrative? |

### Explanation scoring

| Criterion | What to check |
|-----------|---------------|
| Answers "why" | Does it address reasons and motivation? |
| Makes connections | Does it relate concepts to broader context? |
| No instructions | Does it avoid step-by-step procedures? |
| Topic-scoped | Is it bounded to a clear topic? |

## Output format (scores.toml)

```toml
[[runs]]
timestamp = "2026-03-29T14:30:00Z"
description = "Scoring after first draft"

[runs.project]
topic_decomposition = { score = 4, justification = "..." }
quadrant_balance = { score = 3, justification = "..." }
audience_alignment = { score = 5, justification = "..." }
completeness = { score = 2, justification = "..." }

[runs.files."tutorials/first-project.md"]
coverage = { score = 4, justification = "..." }
detail_compliance = { score = 5, justification = "..." }
guidance_adherence = { score = 3, justification = "..." }
cross_linking = { score = 2, justification = "..." }
quadrant_purity = { score = 4, justification = "..." }
```

For how to run scoring and interpret results, see
[How to Score and Revise](../howto/score-and-revise/).
