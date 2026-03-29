# Your First Diataxis Documentation Project

In this tutorial, we will create a complete Diataxis documentation project for a small Python library. Along the way, we will encounter the scoping process, the structure document, content generation, and the four documentation quadrants.

By the end, you will have a working documentation project with tutorials, how-to guides, reference docs, and explanation docs -- all generated from a single structure file.

## Prerequisites

- Claude Code installed and configured
- A Python project you want to document (we will use a simple example)

## Step 1: Start the Diataxis Skill

Open Claude Code in your project directory and ask for Diataxis documentation.

```
Create diataxis documentation for this project
```

You should see Claude respond by asking clarifying questions about your project. This is the scoping step -- it happens every time, even if your request seems clear.

## Step 2: Answer the Scoping Questions

Claude will ask about your project's audience, scope, and depth. For our example calculator library, we answer:

- **Subject**: A Python calculator library with basic arithmetic operations
- **Audience**: Python developers who want to use the library
- **Depth**: Practical project documentation
- **Type**: project-docs

You should see Claude acknowledge your answers and begin drafting a structure.

## Step 3: Review the Structure Document

Claude presents a `diataxis.toml` file. This is the source of truth for your entire documentation project. It defines topics, what each file covers, and guidance for content generation.

You should see something like this:

```toml
[project]
name = "Calculator Library"
description = "Documentation for the calc Python library"
type = "project-docs"
audience = "Python developers using the calc library"

[topics.basic-operations]
title = "Basic Operations"
description = "Addition, subtraction, multiplication, and division"
complexity = "beginner"
order = 1

[topics.basic-operations.tutorial]
file = "tutorials/basic-operations.md"
status = "planned"
covers = [
    "Creating a calculator instance",
    "Performing basic arithmetic",
    "Checking results",
]
```

Review the topics and quadrants. If something is missing or misplaced, tell Claude to adjust it now -- before any content is generated.

## Step 4: Approve and Generate

Once you are satisfied with the structure, tell Claude to proceed:

```
Looks good, generate the content
```

Claude generates each documentation file according to the structure document. You should see files being created in the `diataxis/` directory:

```
diataxis/
├── diataxis.toml
├── tutorials/
│   └── basic-operations.md
├── howto/
│   └── use-advanced-features.md
├── reference/
│   └── api-reference.md
└── explanation/
    └── design-decisions.md
```

## Step 5: Inspect the Results

Open one of the generated files. Notice how each file stays within its quadrant's rules:

- The tutorial guides you through steps with visible results
- The how-to guide is task-focused and assumes competence
- The reference describes the API without instructing
- The explanation discusses design decisions and tradeoffs

Each file also includes cross-links to its siblings in other quadrants.

## What You Have Built

You now have a complete Diataxis documentation project with:

- A `diataxis.toml` structure document that serves as the source of truth
- Content files across all four quadrants, each following its quadrant's rules
- Cross-links between related documents

## Next Steps

- For more on why Diataxis organizes content this way, see [Why Diataxis?](../explanation/why-diataxis.md)
- For the full structure document schema, see the [Structure Document Reference](../reference/structure-document-schema.md)
- For how to improve your docs with scoring, see [How to Score and Revise Documentation](../howto/score-and-revise.md)
