---
name: diataxis
description: >
  ALWAYS use this skill if the user requests diataxis documentation. This includes
  creating, updating, reviewing, scoring, or publishing diataxis-structured content.
---

# Diataxis Documentation Skill

This skill manages documentation projects structured around the Diataxis framework.
It handles the full lifecycle: scoping, structuring, authoring, scoring, revising,
and publishing.

## Core Concepts

Diataxis organizes documentation into four quadrants based on two axes:

|                        | Acquisition (study) | Application (work) |
|------------------------|--------------------|--------------------|
| **Action** (doing)     | Tutorial           | How-to Guide       |
| **Cognition** (thinking) | Explanation       | Reference          |

Each quadrant serves a different user need and has strict rules about what belongs
in it. The power of Diataxis comes from keeping these quadrants distinct — content
that bleeds across boundaries degrades the documentation.

Read `references/quadrants.md` for the detailed rules governing each quadrant type.
These rules are the basis for both content generation and scoring.

## Workflow

Every interaction with this skill follows this sequence. Steps can be skipped if
the user has already completed them, but the order matters.

### Step 1: Scope with Grill-Me

Before doing any work, invoke the `/grill-me` skill to clarify what the user wants.
This happens every time — even if the request seems clear. The goal is to establish:

- **Subject and audience**: What are we documenting, and for whom?
- **Depth**: Overview? Deep dive? Learning path with exercises?
- **Boundaries**: What's in scope and what's explicitly out?
- **Type**: Is this project documentation (documenting a codebase) or a learning
  path (teaching a subject)?
- **Prerequisites**: What does the audience already know?

If the user wants to move quickly, a single round of grill-me is fine. But the
scoping must happen — it directly shapes the structure document that drives
everything else.

For learning path requests ("help me learn X"), explore:
- What's their current level?
- What do they want to be able to do after?
- Do they want exercises? Interactive components?
- Any specific areas of focus or areas to skip?

### Step 2: Create or Update the Structure Document

The structure document (`diataxis.toml`) is the source of truth for the entire
project. It lives in the `diataxis/` directory alongside the documentation
directories. All Diataxis content lives under `project-root/diataxis/` — separate
from any other project files like README, source code, or other documentation.

Read `references/structure-schema.md` for the full TOML schema.

The structure document defines:
- Project metadata (name, audience, type)
- Topics, organized hierarchically
- For each topic and quadrant: the file path, what it covers, level of detail,
  and guidance notes for generation and scoring
- Exercise linkages (marimo notebooks)
- Status tracking per file

**Creating the initial structure**: After scoping, draft the `diataxis.toml` and
present it to the user for approval. Explain the topic decomposition and why you
organized it this way. The user should approve or adjust before any content is
generated.

**Updating structure**: When the user asks to add, remove, or reorganize content,
update `diataxis.toml` first. Then update the affected files. The structure
document is always updated before the content files — never the other way around.

**Capturing revision intent**: When the user requests a specific content change
(e.g., "make this section simpler", "add more detail about X", "don't use that
analogy"), update the `guidance` field in `diataxis.toml` for the affected file(s)
to reflect this feedback before making the content change. Integrate the feedback
into the existing guidance text — rewrite the guidance so it reads as a coherent
whole that incorporates the new direction. Do not append the feedback as a
separate labeled block (e.g., don't add a "REVISION FEEDBACK:" section). The
guidance should always read as if it were written from scratch with full knowledge
of all feedback received so far. This prevents regressions — if the file is
regenerated or revised later, the guidance carries forward the user's intent.
Without this step, a future revision might undo the user's requested change
because nothing in the structure document recorded it.

### Step 3: Generate Content

Once the structure is approved, generate content for each file according to its
entry in `diataxis.toml`. The `covers`, `detail`, and `guidance` fields in the
structure document are the brief for each file.

**Parallel generation**: Because each file's requirements are fully specified in
the structure document, files can be generated independently and in parallel.
When spawning subagents for generation, provide each one with:
1. The full `diataxis.toml` (for cross-linking context)
2. The specific topic and quadrant they're responsible for
3. The quadrant rules from `references/quadrants.md`

**Quadrant rules are non-negotiable during generation**:
- Tutorials: guide action, show results at every step, minimize explanation
- How-to guides: task-focused, no teaching, assume competence
- Reference: describe only, mirror product structure, use tables
- Explanation: discuss why, make connections, provide context

**Cross-linking**: Every file should link to its sibling quadrant docs. A tutorial
should link to the relevant explanation and reference. A how-to should link to
reference. These links use relative paths within the documentation directory.

**Math notation**: All mathematical expressions must use LaTeX notation with
standard delimiters, rendered via MathJax in the final HTML. Use `$...$` or
`\(...\)` for inline math and `$$...$$` or `\[...\]` for display/block math.
The build pipeline includes MathJax in the HTML template. Never write math
as plain text like `3/4 + 1/2` when it can be expressed as `$\frac{3}{4} + \frac{1}{2}$`.

**Exercises**: For tutorials in learning-path projects, create marimo `.py`
notebooks. These are authored as standard marimo notebooks and served via
`marimo run` in the final output. Each exercise file should be self-contained
and focused on one concept.

**Deterministic transforms**: When a task is purely mechanical (converting markdown
to HTML, formatting tables, validating structure), use the appropriate tool — not
LLM generation. Specifically:
- Markdown to HTML: `pandoc`
- HTML tidying: `tidy` or `htmlq`
- JSON/TOML manipulation: `jq`, `python`
- Markdown linting: `textlint`
- XML transforms: `xmlstarlet`

### Step 4: Score the Documentation

Scoring evaluates how well the documentation follows both the Diataxis framework
rules and the project's own structure document.

Read `references/scoring.md` for the full scoring rubric and output format.

Scoring operates at three levels:

**Project level**: Is the topic decomposition sound? Are the four quadrants
represented appropriately? Are there gaps or redundancies?

**Structural level**: Does each file match what `diataxis.toml` says it should
contain? Coverage completeness, detail level, guidance adherence.

**Quadrant level**: Does each file follow the rules for its quadrant type?
Cross-contamination detection (tutorial that explains, reference that instructs).

The scoring output is a structured TOML file (`scores.toml`) that tracks scores
over time so the user can see whether changes improved or degraded the
documentation. Each scoring run is timestamped and the previous scores are
preserved for comparison.

### Step 5: Revise

Based on scores and user feedback, revise the documentation:

1. Update `diataxis.toml` if the structure needs to change
2. Regenerate or edit affected files
3. Re-score to verify improvement

The revision cycle is: **structure first, content second, score third**. Always
update the structure document before touching content files. Always score after
making changes.

When the user gives feedback like "add more exercises about X" or "this is too
hard, add introductory material":
1. Identify where in the topic hierarchy the change belongs
2. Update `diataxis.toml` with new or modified entries
3. Generate the new content
4. Re-score the affected sections and the project as a whole

### Step 6: Build and Publish

The build pipeline transforms the authored content into user-facing HTML.

Read `references/build-pipeline.md` for the technical details.

The pipeline:
1. Reads `diataxis.toml` for the project manifest
2. Converts markdown files to HTML via `pandoc`
3. Generates navigation/index pages from the structure
4. Inserts iframe references for marimo notebooks
5. Outputs a directory of HTML files ready to serve

The marimo notebooks are served separately via `marimo run` — the HTML pages
contain iframes pointing to the marimo server. This means the full documentation
requires two processes: a static file server for the HTML and a marimo server for
the interactive components.

A `serve` command handles both, starting the marimo server and a Python HTTP
server for the static content.

## Directory Layout

A Diataxis project looks like this:

```
project-root/
├── README.md
├── src/                           # Project source code, etc.
└── diataxis/                      # All Diataxis content lives here
    ├── diataxis.toml              # Source of truth
    ├── scores.toml                # Scoring history
    ├── tutorials/
    │   ├── index.md               # Landing page (overview, not bare list)
    │   └── basic-operations.md
    ├── howto/
    │   ├── index.md
    │   └── add-fractions.md
    ├── reference/
    │   ├── index.md
    │   └── fraction-operations.md
    ├── explanation/
    │   ├── index.md
    │   └── why-fractions-work.md
    ├── exercises/
    │   └── basic-ops.py           # marimo notebook
    └── _build/                    # Generated HTML output
        ├── index.html
        ├── tutorials/
        ├── howto/
        ├── reference/
        ├── explanation/
        └── assets/
```

The `diataxis/` directory is self-contained and separate from any other project
files. All paths in `diataxis.toml` are relative to the `diataxis/` directory.

## Reference Files

These files contain detailed specifications. Read them when you need the details:

- `references/quadrants.md` — Rules for each Diataxis quadrant (generation + scoring)
- `references/structure-schema.md` — Full `diataxis.toml` schema with all fields
- `references/scoring.md` — Scoring rubric, output format, and comparison logic
- `references/build-pipeline.md` — Build and serve pipeline technical details
