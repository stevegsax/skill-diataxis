# Structure Document Schema (`diataxis.toml`)

The structure document is the source of truth for a Diataxis documentation project.
It defines what exists, what each file should contain, and how the project is
organized. Every content change starts with updating this file.

## Full Schema

```toml
[project]
name = "Project Name"                    # Required
description = "What this project covers" # Required
type = "learning-path"                   # "learning-path" or "project-docs"
audience = "Who this is for"             # Required
prerequisites = "What the audience already knows"  # Optional

# Topics are the primary organizational unit. Each topic groups related content
# across the four Diataxis quadrants.

[topics.topic-slug]
title = "Human-readable Topic Title"     # Required
description = "What this topic covers"   # Required
complexity = "beginner"                  # "beginner", "intermediate", "advanced"
prerequisites = ["other-topic-slug"]     # Topic slugs this depends on
order = 1                                # Display/learning order within the project

# Each quadrant within a topic is optional. Only define the quadrants that
# make sense for this topic. Not every topic needs all four.

[topics.topic-slug.tutorials]
file = "tutorials/topic-name.md"         # Required: path relative to docs root
status = "draft"                         # "planned", "draft", "review", "complete"
covers = [                               # Required: specific items this file addresses
    "First thing it must cover",
    "Second thing it must cover",
    "Third thing it must cover",
]
detail = """Guidance on the level of depth, format expectations, and scope \
boundaries. This should describe HOW to cover the topics — what level of \
detail, what format, what analogies or approaches to use."""
guidance = """Free-form notes for the content generator and scorer. What to \
do, what to avoid, what to watch out for. Cross-linking instructions. \
Complexity constraints. These notes evolve as the project matures."""
exercises = [                            # Optional: marimo notebook paths
    "exercises/topic-exercise.py",
]

[topics.topic-slug.howto]
file = "howto/topic-task.md"
status = "planned"
covers = [
    "Specific task or problem this addresses",
]
detail = "Concise, no teaching. Assume competence."
guidance = """Title must start with 'How to'. Link to reference for full \
option lists. Include prerequisites if the task requires prior setup."""

[topics.topic-slug.reference]
file = "reference/topic-ref.md"
status = "planned"
covers = [
    "Rules, properties, or specifications to document",
]
detail = "Tabular where possible. Structure mirrors the subject."
guidance = """Use consistent formatting throughout. Every item gets the same \
treatment. No narrative prose."""

[topics.topic-slug.explanation]
file = "explanation/topic-why.md"
status = "planned"
covers = [
    "Conceptual questions this answers",
]
detail = "Discursive, connect to intuition and context."
guidance = """Answer 'why', not 'how'. Connect to the audience's existing \
knowledge. OK to discuss history, alternatives, tradeoffs."""
```

## Field Reference

### Project Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Project name |
| `description` | Yes | What the documentation covers |
| `type` | Yes | `"learning-path"` (educational) or `"project-docs"` (codebase documentation) |
| `audience` | Yes | Who the reader is — skill level, role, context |
| `prerequisites` | No | What the audience is expected to already know |

### Topic Fields

| Field | Required | Description |
|-------|----------|-------------|
| `title` | Yes | Human-readable topic title |
| `description` | Yes | What this topic covers |
| `complexity` | Yes | `"beginner"`, `"intermediate"`, or `"advanced"` |
| `prerequisites` | No | Array of topic slugs this depends on |
| `order` | No | Numeric position in the learning/display sequence |

### Quadrant Fields

| Field | Required | Description |
|-------|----------|-------------|
| `file` | Yes | Path to the content file, relative to docs root |
| `status` | Yes | `"planned"`, `"draft"`, `"review"`, `"complete"` |
| `covers` | Yes | Array of specific items this file must address |
| `detail` | Yes | Depth, format, and scope guidance |
| `guidance` | Yes | Free-form notes: do's, don'ts, watch-outs, cross-linking |
| `exercises` | No | Array of marimo notebook paths (typically tutorials only) |

## Rules

1. **Structure before content**: Always update `diataxis.toml` before creating
   or modifying content files.

2. **Not every topic needs all four quadrants**: A purely conceptual topic might
   only need Explanation and Reference. A practical skill might focus on Tutorial
   and How-to. Define only what serves the audience.

3. **Topic slugs are stable identifiers**: Use lowercase, hyphenated slugs that
   won't change as the project evolves. File paths can change; slugs shouldn't.

4. **`covers` is the scoring contract**: Each item in `covers` is a checkable
   claim. When scoring, the file is evaluated against these items.

5. **`guidance` evolves**: These notes are expected to change as you learn what
   works and what doesn't. Tune them based on scoring results and user feedback.

6. **`detail` sets expectations**: This tells the generator (and scorer) what
   "good" looks like for this specific file. A reference doc with
   `detail = "Tabular, one-line descriptions"` will be scored differently from
   one with `detail = "Detailed paragraphs with examples"`.

7. **Landing pages**: Each quadrant directory gets an `index.md` that serves as
   a landing page. Landing pages are not listed per-topic — they are generated
   from the structure document during the build step. They contain an overview
   and organized links to the content within that section.
