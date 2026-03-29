# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build and Development Commands

```bash
uv sync                          # Install dependencies
uv run diataxis build            # Build HTML from diataxis/ directory
uv run diataxis serve            # Build + start servers (static :8000, marimo :2718)
uv run diataxis serve-only       # Start servers without rebuilding
uv run diataxis build -d <path>  # Use a different diataxis directory
stylelint skill/assets/style.css # Lint CSS
```

Requires Python 3.13+, `pandoc`, and `uv`.

## Architecture

This is a Claude Code skill that manages Diataxis-structured documentation. It has two roles:

1. **Skill instructions** (`skill/SKILL.md` + `skill/references/`) — read by Claude when the skill triggers, guiding it through a six-step workflow: scope with grill-me, create `diataxis.toml` structure, generate content, score, revise, build.

2. **Build pipeline** (`skill/scripts/build.py`) — an installable CLI (`diataxis`) that transforms authored markdown + marimo notebooks into a static HTML site. The pipeline reads `diataxis.toml` as its manifest, runs pandoc with a bundled template (`skill/assets/template.html`), injects sidebar navigation and marimo iframes, and outputs to `_build/`.

The key architectural concept: `diataxis.toml` is the single source of truth. Its `covers`, `detail`, and `guidance` fields per file serve as both the generation brief (telling Claude what to write) and the scoring rubric (evaluating what was written). User revision feedback is integrated into the `guidance` fields before content changes, preventing regressions on regeneration.

## Conventions

- TOML quadrant keys match directory names: `tutorials`, `howto`, `reference`, `explanation`. The constant `QUADRANT_DIRS` in `build.py` is the single source for these.
- All math uses LaTeX notation (`$...$` inline, `$$...$$` display), rendered via MathJax.
- Deterministic transforms (markdown to HTML, etc.) use tools (pandoc, tidy, jq), not LLM generation.
- Interactive exercises are marimo `.py` notebooks served via `marimo.create_asgi_app().build()` — mounted at root-level paths to avoid double-prefix redirects.
- The build script post-processes pandoc output to convert `.md` hrefs to `.html`.
- CSS changes must pass `stylelint` with the project `.stylelintrc.json`.
