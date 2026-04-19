+++
title = "How to Score and Revise Documentation"
weight = 53
description = "How to evaluate documentation quality using the scoring rubric"
topic = "scoring"
covers = ["Running the deterministic check suite (Phase 1)", "Asking Claude for the qualitative scoring pass (Phase 2)", "Reading scores.toml output", "Identifying cross-contamination", "Revising based on scores"]
detail = "Task-focused. Each task gets a short procedure."
+++
Scoring runs in two phases. Phase 1 is a deterministic nushell check
suite that catches structural problems. Phase 2 is a qualitative pass by
Claude against the rubric in `diataxis.toml`. Always run Phase 1 first.

## Phase 1: Run the deterministic checks

From the repository root:

```bash
nu skill/checks/run-checks.nu diataxis
```

This runs 12 checks for structural integrity, quadrant rules, and format
compliance, and writes a JSON report to stdout. Each result is `pass`,
`fail`, `skip`, or `error`, with evidence and a fix suggestion when
applicable.

If any checks fail, fix them before continuing. The most common failures:

- A file referenced in `diataxis.toml` does not exist on disk
- A how-to title that does not start with "How to"
- A reference doc with no tables or structured lists
- Missing cross-references between quadrants

You can ask Claude to fix the failures, or fix them by hand and re-run.
Only proceed to Phase 2 once the suite is clean — or explicitly tell
Claude to score anyway.

## Phase 2: Ask Claude for the qualitative pass

```
Score the diataxis documentation
```

Claude reads `diataxis.toml` and evaluates each file against its
`covers`, `detail`, and `guidance` fields, plus the Diataxis quadrant
rules. The skill instructions require a fresh read of every file each
time — Claude does not reuse prior scores.

## Read the output

Scores are appended to `diataxis/scores.toml` as a new `[[runs]]` entry.
Each entry looks like:

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

The most common qualitative issue: content drifting into the wrong
quadrant. Look for:

- Tutorial paragraphs that explain "why" at length (should link to Explanation)
- Reference docs that walk through steps (should link to How-to)
- How-to guides that teach from scratch (should link to Tutorial)

## Revise based on scores

Ask Claude to revise the affected files. The skill will:

1. Update the `guidance` field in `diataxis.toml` to integrate the feedback
2. Revise the affected content files
3. Re-score to confirm improvement

You can also revise structure-level concerns (add or remove topics,
reorder them) by editing `diataxis.toml` directly or by asking Claude to.

For the full scoring rubric, see
[Scoring Rubric](../../reference/scoring-rubric/). For background on why
structure changes come before content changes, see
[Why Structure First](../../explanation/why-structure-first/).
