# How to Edit the Structure Document

This guide shows you how to modify `diataxis.toml` to add, remove, or reorganize documentation content.

The structure document is always updated before content files. Never edit content files without first reflecting the change in `diataxis.toml`.

## How to Add a New Topic

1. Open `diataxis.toml` in your editor.
2. Add a new `[topics.<slug>]` section with a unique, lowercase, hyphenated slug.
3. Set the required fields: `title`, `description`, `complexity`.
4. Set `order` to position the topic relative to existing topics.
5. If the topic depends on others, add their slugs to `prerequisites`.
6. Add quadrant entries for the quadrants this topic needs. Not every topic requires all four.
7. For each quadrant entry, set `file`, `status = "planned"`, `covers`, `detail`, and `guidance`.
8. Ask Claude to generate the content files for the new topic.

```toml
[topics.error-handling]
title = "Error Handling"
description = "How the library handles and reports errors"
complexity = "intermediate"
prerequisites = ["basic-operations"]
order = 3

[topics.error-handling.reference]
file = "reference/error-handling.md"
status = "planned"
covers = [
    "Exception types and hierarchy",
    "Error codes and their meanings",
]
detail = "Tabular. One row per exception type."
guidance = "Link to how-to for recovery strategies."
```

## How to Remove a Quadrant from a Topic

1. Delete the quadrant section from the topic in `diataxis.toml` (e.g., remove `[topics.my-topic.tutorial]`).
2. Delete or archive the corresponding content file.
3. Check other files for cross-links pointing to the removed file and update them.

## How to Change Topic Ordering

1. Adjust the `order` field on each topic you want to reposition.
2. Update `prerequisites` arrays if the new order changes dependency relationships.
3. Rebuild to regenerate landing pages with the updated order.

## How to Update Guidance After Scoring

When scoring reveals issues, capture the fix in `guidance` before editing the content file. This prevents regressions on future regeneration.

1. Read the scoring feedback for the file in question.
2. Open `diataxis.toml` and find the quadrant entry for that file.
3. Append the scoring feedback to the `guidance` field as a specific instruction.
4. Edit or regenerate the content file to follow the updated guidance.
5. Re-score to verify the change improved the score.

```toml
# Before
guidance = "Keep examples simple. Link to reference for full API."

# After scoring found cross-contamination
guidance = """Keep examples simple. Link to reference for full API. \
Do not explain why common denominators are needed -- link to \
explanation doc instead (flagged in scoring run 2025-03-29)."""
```

## Further Reading

- See the [Structure Document Schema](../reference/structure-document-schema.md) for all available fields
- See [How to Score and Revise Documentation](score-and-revise.md) for the full revision cycle
