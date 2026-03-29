# Tutorial: Creating Your First Diataxis Documentation Project

In this tutorial, we will create a Diataxis-structured documentation set for a small Python project. Along the way, we will scope the documentation, define its structure, generate content, score it, and build it into browsable HTML.

## Prerequisites

- Python 3.13 or later installed
- `pandoc` installed (used for markdown-to-HTML conversion)
- A Python project you want to document (or you can use any small project to follow along)

## Step 1: Trigger the Skill

Ask Claude Code to create Diataxis documentation for your project. You can use any of these phrases:

```
create diataxis documentation
create diataxis documentation for this project
help me learn about X (for learning paths)
```

Claude will invoke the Diataxis skill automatically.

You should see Claude begin asking you scoping questions rather than immediately generating docs.

## Step 2: Answer the Scoping Questions

The skill uses a structured interrogation (via the `grill-me` sub-skill) to clarify what you need. Expect questions like:

- What is the subject and who is the audience?
- What depth do you want -- overview, deep dive, or a full learning path with exercises?
- What is in scope and what is out?
- Is this project documentation (documenting a codebase) or a learning path (teaching a subject)?
- What does the audience already know?

Answer each question. If you want to move quickly, a single round of Q&A is sufficient, but more rounds produce tighter scoping.

After this step, Claude has a clear picture of what to document and for whom.

## Step 3: Review the Structure Document

Claude will produce a `diataxis.toml` file and present it to you. This file is the source of truth for the entire documentation project. It defines:

- Project metadata (name, audience, type)
- Topics, organized hierarchically
- For each topic: which quadrants to include, what each file covers, and guidance notes

Here is what a simple structure looks like:

```toml
[project]
name = "My CLI Tool"
description = "Documentation for the my-cli command-line tool"
type = "project-docs"
audience = "Developers who use my-cli in their build pipeline"

[topics.installation]
title = "Installation"
description = "Getting my-cli installed and configured"
complexity = "beginner"
order = 1

[topics.installation.tutorial]
file = "tutorials/installation.md"
status = "planned"
covers = ["Installing via pip", "Verifying the installation", "Running the first command"]
detail = "Step-by-step, show output at each stage"
guidance = "Keep to the happy path. Link to explanation for platform-specific notes."
```

Review the structure. You can ask Claude to add topics, remove quadrants, change the scope, or reorganize. The structure must be approved before any content is generated.

## Step 4: Generate Content

Once you approve the structure, Claude generates the documentation files. Each file follows the rules for its quadrant type:

- **Tutorials** guide action, show results at every step, minimize explanation
- **How-to guides** are task-focused, assume competence, no teaching
- **Reference** describes facts, uses tables, mirrors the subject structure
- **Explanation** discusses why, makes connections, provides context

You should see files appearing in the `diataxis/` directory under `tutorials/`, `howto/`, `reference/`, and `explanation/` subdirectories.

## Step 5: Score the Documentation

Ask Claude to score the documentation:

```
score the documentation
```

Claude evaluates at three levels:

1. **Project level** -- topic decomposition, quadrant balance, audience alignment
2. **Structural level** -- does each file cover what `diataxis.toml` says it should?
3. **Quadrant level** -- does each file follow the rules for its type?

You will receive a `scores.toml` file with scores on a 1-5 scale and specific justifications for each score.

## Step 6: Revise Based on Scores

Review the scores and give feedback. For example:

```
The tutorial explains too much -- link to explanation docs instead.
Add a how-to guide for configuring the output format.
Make the reference doc use tables instead of paragraphs.
```

Claude will update `diataxis.toml` first (capturing your feedback in the `guidance` fields), then revise the content, then re-score. You should see the scores improve.

## Step 7: Build and Serve

Ask Claude to build the documentation:

```
build the diataxis docs
```

The build pipeline:

1. Validates that all referenced files exist
2. Generates landing pages for each quadrant
3. Converts all markdown to HTML via pandoc
4. Inserts iframe references for any marimo exercise notebooks
5. Outputs everything to `diataxis/_build/`

To view the result in your browser:

```
python -m scripts.build diataxis --serve
```

You should see output like:

```
Starting static server on port 8000...
Open http://localhost:8000 in your browser.
```

Navigate to `http://localhost:8000` to browse the documentation.

## What You Have Built

You now have a complete Diataxis documentation project with:

- A `diataxis.toml` structure document that serves as the source of truth
- Content files organized into the four Diataxis quadrants
- Scores tracking documentation quality over time
- A built HTML site you can serve and browse

## Next Steps

- [How to revise documentation based on scores](../howto/revise-from-scores.md) -- for targeted improvements
- [How to add interactive exercises](../howto/add-exercises.md) -- for learning-path projects
- [Structure document reference](../reference/structure-schema.md) -- full field reference for `diataxis.toml`
- [About the Diataxis framework](../explanation/diataxis-framework.md) -- why this structure works
