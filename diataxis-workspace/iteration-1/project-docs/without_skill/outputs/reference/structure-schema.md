# Structure Document Reference (`diataxis.toml`)

The structure document is the source of truth for a Diataxis documentation project. It defines project metadata, topic organization, and per-file content specifications.

## Location

`diataxis/diataxis.toml` -- relative to the project root. All file paths within the document are relative to the `diataxis/` directory.

## Project Fields

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `name` | Yes | String | Project name |
| `description` | Yes | String | What the documentation covers |
| `type` | Yes | String | `"learning-path"` or `"project-docs"` |
| `audience` | Yes | String | Who the reader is -- skill level, role, context |
| `prerequisites` | No | String | What the audience is expected to already know |

## Topic Fields

Topics are defined under `[topics.<slug>]` where `<slug>` is a stable, lowercase, hyphenated identifier.

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `title` | Yes | String | Human-readable topic title |
| `description` | Yes | String | What this topic covers |
| `complexity` | Yes | String | `"beginner"`, `"intermediate"`, or `"advanced"` |
| `prerequisites` | No | Array of strings | Topic slugs this depends on |
| `order` | No | Integer | Display/learning order within the project |

## Quadrant Fields

Each topic can have up to four quadrant entries: `tutorial`, `howto`, `reference`, `explanation`. Each is defined under `[topics.<slug>.<quadrant>]`.

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `file` | Yes | String | Path to content file, relative to `diataxis/` |
| `status` | Yes | String | `"planned"`, `"draft"`, `"review"`, `"complete"` |
| `covers` | Yes | Array of strings | Specific items this file must address |
| `detail` | Yes | String | Depth, format, and scope guidance |
| `guidance` | Yes | String | Free-form notes for generation and scoring |
| `exercises` | No | Array of strings | Marimo notebook paths (typically tutorials only) |

## Status Values

| Status | Meaning |
|--------|---------|
| `planned` | Entry exists in the structure but no content file has been created |
| `draft` | Content file exists with initial content |
| `review` | Content has been scored and is being refined |
| `complete` | Content meets quality standards and scoring targets |

## Example

```toml
[project]
name = "My CLI Tool"
description = "Documentation for the my-cli command-line tool"
type = "project-docs"
audience = "Developers who use my-cli in their build pipeline"
prerequisites = "Familiarity with command-line tools and YAML configuration"

[topics.installation]
title = "Installation"
description = "Getting my-cli installed and configured"
complexity = "beginner"
order = 1

[topics.installation.tutorial]
file = "tutorials/installation.md"
status = "draft"
covers = [
    "Installing via pip",
    "Verifying the installation",
    "Running the first command",
]
detail = "Step-by-step, show output at each stage"
guidance = "Keep to the happy path. Link to explanation for platform-specific notes."

[topics.installation.reference]
file = "reference/cli-options.md"
status = "planned"
covers = [
    "All CLI flags and their defaults",
    "Environment variable overrides",
    "Configuration file format",
]
detail = "Tabular, one-line descriptions per flag"
guidance = "Use consistent formatting. Every flag gets the same treatment."
```

## Rules

- Update `diataxis.toml` before creating or modifying content files.
- Not every topic needs all four quadrants. Define only what serves the audience.
- Topic slugs are stable identifiers. File paths can change; slugs should not.
- The `covers` array is the scoring contract. Each item is evaluated during scoring.
- The `guidance` field evolves over time with user feedback and scoring results.
- Landing pages (`index.md` in each quadrant directory) are generated from the structure during build -- they are not listed as topic entries.
