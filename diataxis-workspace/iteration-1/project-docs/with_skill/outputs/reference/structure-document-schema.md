# Structure Document Schema

The `diataxis.toml` file is the source of truth for a Diataxis documentation project. It lives in the `diataxis/` directory alongside the documentation content. All paths within the file are relative to the `diataxis/` directory.

## Project Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Project name, used in generated landing pages and navigation |
| `description` | string | Yes | What the documentation covers |
| `type` | string | Yes | `"learning-path"` or `"project-docs"` |
| `audience` | string | Yes | Who the reader is -- skill level, role, context |
| `prerequisites` | string | No | What the audience is expected to already know |

```toml
[project]
name = "Calculator Library"
description = "Documentation for the calc Python library"
type = "project-docs"
audience = "Python developers using the calc library"
prerequisites = "Basic Python knowledge"
```

## Topic Fields

Topics are the primary organizational unit. Each topic groups related content across the four Diataxis quadrants. Topics are defined under `[topics.<slug>]` where `<slug>` is a stable, lowercase, hyphenated identifier.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | Yes | Human-readable topic title |
| `description` | string | Yes | What this topic covers |
| `complexity` | string | Yes | `"beginner"`, `"intermediate"`, or `"advanced"` |
| `prerequisites` | array of strings | No | Topic slugs this depends on |
| `order` | integer | No | Numeric position in the learning/display sequence |

```toml
[topics.basic-operations]
title = "Basic Operations"
description = "Addition, subtraction, multiplication, and division"
complexity = "beginner"
prerequisites = []
order = 1
```

## Quadrant Fields

Each topic may define up to four quadrant entries: `tutorial`, `howto`, `reference`, `explanation`. Not every topic requires all four. Define only the quadrants that serve the audience.

Quadrant entries are defined under `[topics.<slug>.<quadrant>]`.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | string | Yes | Path to content file, relative to `diataxis/` directory |
| `status` | string | Yes | Current state of the file (see Status Values below) |
| `covers` | array of strings | Yes | Specific items this file must address; each item is a scoring checkpoint |
| `detail` | string | Yes | Depth, format, and scope guidance for generation and scoring |
| `guidance` | string | Yes | Free-form notes: do's, don'ts, cross-linking instructions, revision feedback |
| `exercises` | array of strings | No | Paths to marimo notebook files (typically tutorials only) |

```toml
[topics.basic-operations.tutorial]
file = "tutorials/basic-operations.md"
status = "draft"
covers = [
    "Creating a calculator instance",
    "Performing basic arithmetic",
    "Checking results",
]
detail = "Step-by-step with visible output at each stage."
guidance = "Keep examples simple. Link to reference for full API."
exercises = ["exercises/basic-ops.py"]
```

## Status Values

| Value | Meaning |
|-------|---------|
| `"planned"` | Entry exists in structure but no content file has been created |
| `"draft"` | Content file exists with initial content |
| `"review"` | Content has been scored and is undergoing revision |
| `"complete"` | Content meets scoring criteria and is approved |

## Topic Slug Rules

- Lowercase letters, numbers, and hyphens only
- Must be stable identifiers that do not change as the project evolves
- File paths can change; slugs should not
- Used in `prerequisites` arrays to express dependencies between topics

## File Path Rules

- All paths are relative to the `diataxis/` directory
- Content files go in quadrant directories: `tutorials/`, `howto/`, `reference/`, `explanation/`
- Exercise files go in `exercises/`
- Landing pages (`index.md`) are generated during build and should not be listed in the structure document

## Further Reading

- For how to edit the structure document, see [How to Edit the Structure Document](../howto/edit-structure-document.md)
- For why the structure document drives the project, see [Why Diataxis?](../explanation/why-diataxis.md)
- For the build pipeline that consumes this file, see [Build Pipeline Reference](build-pipeline.md)
