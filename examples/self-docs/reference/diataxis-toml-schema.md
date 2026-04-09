# diataxis.toml Schema

## Project fields

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `name` | Yes | string | Project name, displayed in navigation |
| `description` | Yes | string | What the documentation covers |
| `purpose` | Yes | string | Why the project exists and what problems it solves — drives the introductory page |
| `type` | Yes | string | `"learning-path"` or `"project-docs"` |
| `audience` | Yes | string | Who the reader is |
| `prerequisites` | No | string | What the audience already knows |

## Topic fields

Defined under `[topics.<slug>]` where `<slug>` is a lowercase, hyphenated
identifier.

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `title` | Yes | string | Human-readable topic title |
| `description` | Yes | string | What this topic covers |
| `complexity` | Yes | string | `"beginner"`, `"intermediate"`, or `"advanced"` |
| `prerequisites` | No | array of strings | Topic slugs this depends on |
| `order` | No | integer | Display/learning order (lower = first) |

## Quadrant fields

Defined under `[topics.<slug>.tutorials]`, `[topics.<slug>.howto]`,
`[topics.<slug>.reference]`, or `[topics.<slug>.explanation]`.

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `file` | Yes | string | Path relative to the diataxis directory |
| `status` | Yes | string | `"planned"`, `"draft"`, `"review"`, or `"complete"` |
| `covers` | Yes | array of strings | Items this file must address (scoring contract) |
| `detail` | Yes | string | Depth, format, and scope guidance |
| `guidance` | Yes | string | Notes for content generation and scoring |
| `exercises` | No | array of strings | Marimo notebook paths (typically tutorials only) |

## Status values

| Status | Meaning |
|--------|---------|
| `planned` | Entry exists in structure, file not yet created |
| `draft` | Content exists, may need work |
| `review` | Ready for scoring and revision |
| `complete` | Meets all criteria |

## Example

```toml
[project]
name = "My Project"
description = "Documentation for My Project"
purpose = """Explain why this project exists and what problems it solves. This \
text drives the introductory page content."""
type = "project-docs"
audience = "Developers"

[topics.auth]
title = "Authentication"
description = "User authentication and authorization"
complexity = "intermediate"
order = 1

[topics.auth.tutorials]
file = "tutorials/auth-basics.md"
status = "draft"
covers = ["Setting up OAuth2", "Handling tokens"]
detail = "Step-by-step with code examples."
guidance = "Use a simple Flask app as the example."
exercises = ["exercises/auth-exercise.py"]
```

For a walkthrough of building this file, see the
[Writing diataxis.toml](../tutorials/writing-diataxis-toml.html) tutorial. For
why the structure document matters, see
[Why Structure First](../explanation/why-structure-first.html).
