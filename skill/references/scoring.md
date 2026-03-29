# Scoring Rubric

Scoring evaluates documentation against both the Diataxis framework rules and the
project's own structure document (`diataxis.toml`). Scores are tracked over time
so changes can be measured as improvements or regressions.

## Table of Contents

- [Score Levels](#score-levels)
- [Project-Level Scoring](#project-level-scoring)
- [Structural Scoring](#structural-scoring)
- [Quadrant Scoring](#quadrant-scoring)
- [Output Format](#output-format)
- [Comparison](#comparison)

---

## Score Levels

All scores use a 1-5 scale:

| Score | Meaning |
|-------|---------|
| 5 | Fully meets criteria, no issues |
| 4 | Meets criteria with minor issues |
| 3 | Partially meets criteria, some notable gaps |
| 2 | Significant gaps or violations |
| 1 | Does not meet criteria |

Each score includes a justification explaining why that score was given and what
would need to change to improve it. Justifications should be specific and
actionable.

---

## Project-Level Scoring

Evaluates the documentation as a whole.

### Criteria

**Topic decomposition** (weight: high)
- Are topics appropriately scoped — neither too broad nor too narrow?
- Is the subject covered at the right level of detail for the audience?
- Are there gaps in coverage? Redundancies between topics?
- Does the topic hierarchy make logical sense?

**Quadrant balance** (weight: medium)
- Are the four quadrants used appropriately for this project type?
- Is any quadrant over- or under-represented relative to the audience's needs?
- A learning-path project should lean toward Tutorials and Explanation
- A project-docs project should lean toward How-to and Reference

**Audience alignment** (weight: high)
- Does the complexity match the stated audience?
- Are prerequisites reasonable for the stated audience?
- Is the language level appropriate?

**Completeness** (weight: medium)
- What percentage of planned files have status "draft" or better?
- Are there topics with no content at all?

---

## Structural Scoring

Evaluates each file against its entry in `diataxis.toml`.

### Criteria

**Coverage** (weight: high)
- For each item in `covers`: is it addressed in the file?
- Score: proportion of items addressed, weighted by importance
- An item is "addressed" if a reader could find the information by reading the file

**Detail compliance** (weight: medium)
- Does the file match the depth and format described in `detail`?
- If `detail` says "tabular", is it tabular?
- If `detail` says "step-by-step with visual examples", are there steps and visuals?

**Guidance adherence** (weight: high)
- Does the file follow the instructions in `guidance`?
- Does it avoid what `guidance` says to avoid?
- This is evaluated item by item when `guidance` contains distinct instructions

**Cross-linking** (weight: medium)
- Does the file link to sibling quadrant documents?
- Are the links relevant and correctly placed?

**Exercise presence** (weight: low, tutorials only)
- If `exercises` are listed, do the corresponding marimo notebooks exist?
- Are they referenced/linked from the tutorial content?

---

## Quadrant Scoring

Evaluates whether each file follows the rules for its quadrant type. These rules
come from the Diataxis framework itself (see `references/quadrants.md`).

### Tutorial scoring

| Criterion | What to check |
|-----------|---------------|
| Action-oriented | Does every section contain steps for the learner to take? |
| Results shown | Are results/output shown after steps (within every 3 steps)? |
| Narrative of expected | Does it say what the learner should see/notice? |
| Minimal explanation | Are explanations brief (1-2 sentences max) with links? |
| No choices | Does it avoid presenting alternatives or options? |
| Completable | Does it reach a satisfying, defined endpoint? |
| Concrete | Does it work with specific examples, not abstract concepts? |

### How-to scoring

| Criterion | What to check |
|-----------|---------------|
| Task-focused | Does the title state a task? Does the content stay on task? |
| No teaching | Does it avoid explaining fundamentals? |
| Assumes competence | Does it skip basics the reader should already know? |
| Actionable steps | Is every step something the reader can do? |
| Real-world | Does it handle edge cases and complexity? |

### Reference scoring

| Criterion | What to check |
|-----------|---------------|
| Description only | Is the content neutral description, free of instruction? |
| Consistent structure | Do all items follow the same format/pattern? |
| Mirrors subject | Does the doc structure reflect the structure of what it describes? |
| Complete within scope | Are all items in the declared scope documented? |
| Brief examples | Are examples short and illustrative, not tutorial-like? |

### Explanation scoring

| Criterion | What to check |
|-----------|---------------|
| Answers "why" | Does it address reasons, context, and motivation? |
| Makes connections | Does it relate concepts to each other or to broader context? |
| No instructions | Does it avoid step-by-step procedures? |
| Provides context | Does it give background, history, or design rationale? |
| Topic-scoped | Is it bounded to a clear topic? |

### Cross-contamination detection

The most common scoring issue. Check for:
- Tutorial paragraphs that explain "why" at length (should link to Explanation)
- Reference sections that walk through steps (should link to How-to)
- How-to guides that teach from scratch (should link to Tutorial)
- Explanation that includes code listings as reference (should link to Reference)

---

## Output Format

Scores are stored in `scores.toml` in the project root. Each scoring run is
a timestamped entry preserving history for comparison.

```toml
[[runs]]
timestamp = "2025-03-29T14:30:00Z"
description = "Initial scoring after first draft"

[runs.project]
topic_decomposition = { score = 4, justification = "Topics are well-scoped but 'Advanced Operations' is too broad — consider splitting into sub-topics." }
quadrant_balance = { score = 3, justification = "Heavy on tutorials, missing most how-to guides. Appropriate for a learning path but how-tos would help retention." }
audience_alignment = { score = 5, justification = "Language and complexity match the stated audience of adult learners refreshing high school math." }
completeness = { score = 2, justification = "Only 4 of 12 planned files have drafts." }

[runs.files."tutorials/basic-ops.md"]
coverage = { score = 4, justification = "Covers 4 of 5 items in 'covers'. Missing: dividing fractions by flipping and multiplying." }
detail_compliance = { score = 5, justification = "Step-by-step format with worked examples as specified." }
guidance_adherence = { score = 3, justification = "Contains a 4-paragraph explanation of why common denominators are needed. Guidance says to link to explanation doc instead." }
cross_linking = { score = 2, justification = "No links to sibling quadrant documents." }
quadrant_purity = { score = 3, justification = "Two sections drift into explanation territory. Paragraphs starting 'The reason this works...' should be replaced with links." }

[runs.files."reference/fraction-operations.md"]
coverage = { score = 5, justification = "All items in 'covers' are addressed." }
detail_compliance = { score = 4, justification = "Mostly tabular. One section uses narrative prose where a table would be more appropriate." }
guidance_adherence = { score = 5, justification = "Follows all guidance notes." }
cross_linking = { score = 4, justification = "Links to how-to guides present. Missing link to explanation." }
quadrant_purity = { score = 5, justification = "Pure reference — describes without instructing or explaining." }
```

---

## Comparison

When re-scoring after changes, compare against the most recent previous run:

- **Improved**: score went up. Report the delta and what changed.
- **Regressed**: score went down. Flag this prominently — the user needs to know.
- **Unchanged**: score stayed the same. Note if the justification changed even
  if the number didn't.
- **New**: file was scored for the first time (no comparison available).

Present comparison as a summary table:

```
File                              Coverage  Detail  Guidance  Quadrant  Overall
tutorials/basic-ops.md            4 → 5     5 → 5   3 → 4     3 → 4    +3
reference/fraction-operations.md  5 → 5     4 → 5   5 → 5     5 → 5    +1
howto/add-fractions.md            NEW       NEW     NEW       NEW      (new)
```

Follow the table with specifics on what improved and what regressed.
