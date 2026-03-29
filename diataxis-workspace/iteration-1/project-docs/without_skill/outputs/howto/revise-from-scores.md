# How to Revise Documentation Based on Scores

This guide shows you how to use the scoring output to systematically improve your Diataxis documentation.

## Prerequisites

- An existing Diataxis documentation project with a `diataxis.toml`
- At least one scoring run stored in `scores.toml`

## Steps

1. **Read the scores.** Open `scores.toml` or ask Claude to summarize the scoring results. Focus on the lowest scores first -- these are the highest-impact improvements.

2. **Identify the category of the issue.** Each scored criterion tells you a different thing:

    - **Coverage** score is low: the file is missing items listed in the `covers` field of `diataxis.toml`. Add the missing content.
    - **Detail compliance** score is low: the file does not match the format described in the `detail` field. For example, if `detail` says "tabular" but the file uses prose, restructure into tables.
    - **Guidance adherence** score is low: the file violates instructions in the `guidance` field. Read the guidance and fix the specific violations noted in the justification.
    - **Cross-linking** score is low: the file does not link to its sibling quadrant documents. Add links to related tutorials, how-to guides, reference, or explanation docs.
    - **Quadrant purity** score is low: the file contains content that belongs in a different quadrant. Move the content or replace it with a link.

3. **Update `diataxis.toml` first.** If your revision changes the scope, adds new files, or reflects user feedback, update the structure document before touching any content files. Add your intent to the `guidance` field so it persists across future revisions.

4. **Make the content changes.** Edit the markdown files to address the specific issues identified in the scoring justifications.

5. **Re-score.** Ask Claude to score again. Compare the new scores against the previous run. The comparison table will show which scores improved, regressed, or stayed the same.

6. **Repeat until satisfied.** The revision cycle is: structure first, content second, score third. Each round should show measurable improvement.

## Common Patterns

- **Quadrant cross-contamination**: A tutorial that explains "why" at length should have those paragraphs replaced with a link to the corresponding explanation document. A reference that walks through steps should link to the how-to guide instead.

- **Coverage gaps**: If a `covers` item is not addressed, either add it to the file or remove it from `diataxis.toml` if it no longer belongs.

- **Guidance drift**: After several rounds of revision, the `guidance` field may accumulate contradictory notes. Clean it up periodically.

## See Also

- [Scoring rubric reference](../reference/scoring-rubric.md) -- full details on what each criterion measures
- [Structure document reference](../reference/structure-schema.md) -- field definitions for `diataxis.toml`
