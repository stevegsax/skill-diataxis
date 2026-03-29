# How to Score and Revise Documentation

This guide shows you how to evaluate your Diataxis documentation against the framework rules and structure document, then revise based on the results.

## How to Run a Scoring Pass

1. Ensure your `diataxis.toml` is up to date and all content files listed in it exist.
2. Ask Claude to score the documentation:

    ```
    Score the diataxis documentation
    ```

3. Claude evaluates each file at three levels: project-level, structural, and quadrant adherence.
4. Review the generated `scores.toml` file in the `diataxis/` directory.

## How to Interpret Scores

Scores use a 1-5 scale. Each score includes a justification.

| Score | Meaning |
|-------|---------|
| 5 | Fully meets criteria |
| 4 | Meets criteria with minor issues |
| 3 | Partially meets, notable gaps |
| 2 | Significant gaps or violations |
| 1 | Does not meet criteria |

Focus on:

- **Coverage scores below 4**: Items from `covers` are missing from the content.
- **Quadrant purity scores below 4**: Content has drifted into another quadrant's territory.
- **Guidance adherence scores below 4**: The file does not follow its own `guidance` notes.

## How to Address Cross-Contamination

Cross-contamination is the most common issue. A tutorial that explains "why" at length, or a reference page that walks through steps.

1. Identify the offending paragraphs noted in the scoring justification.
2. Determine which quadrant the content belongs in.
3. If the target document exists, move the content there (or verify it is already covered).
4. Replace the offending content with a cross-link: "For more on why this works, see [Explanation title](path)."
5. Update `guidance` in `diataxis.toml` to prevent the contamination from recurring.

## How to Re-Score After Revisions

1. Make your revisions to the content files.
2. Ask Claude to score again:

    ```
    Re-score the diataxis documentation
    ```

3. Claude compares the new scores against the previous run and reports improvements and regressions.
4. Review the comparison table in the output. Any regressions should be investigated.

The revision cycle is: structure first, content second, score third. Repeat until scores meet your standards.

## Further Reading

- See the [Quadrant Rules Reference](../reference/quadrant-rules.md) for the criteria being scored
- See [How to Edit the Structure Document](edit-structure-document.md) for updating structure before content
