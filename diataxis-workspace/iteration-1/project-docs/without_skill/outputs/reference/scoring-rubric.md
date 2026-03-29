# Scoring Rubric Reference

Scoring evaluates documentation against both the Diataxis framework rules and the project's structure document (`diataxis.toml`). Scores are stored in `scores.toml` and tracked over time.

## Score Scale

| Score | Meaning |
|-------|---------|
| 5 | Fully meets criteria, no issues |
| 4 | Meets criteria with minor issues |
| 3 | Partially meets criteria, some notable gaps |
| 2 | Significant gaps or violations |
| 1 | Does not meet criteria |

Every score includes a justification explaining the rating and what would improve it.

## Scoring Levels

### Project-Level Criteria

| Criterion | Weight | What it evaluates |
|-----------|--------|-------------------|
| Topic decomposition | High | Whether topics are appropriately scoped, without gaps or redundancies |
| Quadrant balance | Medium | Whether quadrant usage matches the project type and audience needs |
| Audience alignment | High | Whether complexity and language match the stated audience |
| Completeness | Medium | Percentage of planned files that have status "draft" or better |

### Structural Criteria (Per File)

| Criterion | Weight | What it evaluates |
|-----------|--------|-------------------|
| Coverage | High | Whether each item in `covers` is addressed in the file |
| Detail compliance | Medium | Whether the file matches the format described in `detail` |
| Guidance adherence | High | Whether the file follows the instructions in `guidance` |
| Cross-linking | Medium | Whether the file links to sibling quadrant documents |
| Exercise presence | Low | Whether listed exercises exist and are referenced (tutorials only) |

### Quadrant Criteria

#### Tutorial

| Criterion | What to check |
|-----------|---------------|
| Action-oriented | Every section contains steps for the learner |
| Results shown | Output shown within every 3 steps |
| Narrative of expected | States what the learner should see |
| Minimal explanation | Explanations are 1-2 sentences with links |
| No choices | No alternatives or options presented |
| Completable | Reaches a satisfying endpoint |
| Concrete | Works with specific examples |

#### How-to Guide

| Criterion | What to check |
|-----------|---------------|
| Task-focused | Title states a task; content stays on task |
| No teaching | Does not explain fundamentals |
| Assumes competence | Skips basics the reader should know |
| Actionable steps | Every step is something the reader can do |
| Real-world | Handles edge cases and complexity |

#### Reference

| Criterion | What to check |
|-----------|---------------|
| Description only | Neutral description, free of instruction |
| Consistent structure | All items follow the same format |
| Mirrors subject | Doc structure reflects the structure of what it describes |
| Complete within scope | All declared items documented |
| Brief examples | Short and illustrative, not instructional |

#### Explanation

| Criterion | What to check |
|-----------|---------------|
| Answers "why" | Addresses reasons, context, motivation |
| Makes connections | Relates concepts to each other or broader context |
| No instructions | No step-by-step procedures |
| Provides context | Background, history, or design rationale |
| Topic-scoped | Bounded to a clear topic |

## Output Format

Scores are stored in `scores.toml`. Each scoring run is a timestamped entry.

```toml
[[runs]]
timestamp = "2025-03-29T14:30:00Z"
description = "Initial scoring after first draft"

[runs.project]
topic_decomposition = { score = 4, justification = "..." }
quadrant_balance = { score = 3, justification = "..." }
audience_alignment = { score = 5, justification = "..." }
completeness = { score = 2, justification = "..." }

[runs.files."tutorials/basic-ops.md"]
coverage = { score = 4, justification = "..." }
detail_compliance = { score = 5, justification = "..." }
guidance_adherence = { score = 3, justification = "..." }
cross_linking = { score = 2, justification = "..." }
quadrant_purity = { score = 3, justification = "..." }
```

## Score Comparison

When re-scoring, each file is compared against its most recent previous score:

| Status | Meaning |
|--------|---------|
| Improved | Score went up; delta and cause reported |
| Regressed | Score went down; flagged prominently |
| Unchanged | Score stayed the same; justification changes still noted |
| New | File scored for the first time |
