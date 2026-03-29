# skill-diataxis

A Claude Code skill for creating, revising, scoring, and publishing documentation structured around the [Diataxis](https://diataxis.fr/) framework.

## What it does

Manages the full lifecycle of Diataxis-structured documentation:

- **Scope** — uses the grill-me skill to clarify what the user wants before starting
- **Structure** — generates a `diataxis.toml` manifest that defines topics, files, coverage criteria, and guidance notes
- **Generate** — creates content across all four Diataxis quadrants (tutorials, how-to guides, reference, explanation)
- **Score** — evaluates documentation against the Diataxis rules and the project's own structure document
- **Revise** — updates structure first, then content, preserving user feedback in guidance fields
- **Build** — converts markdown to HTML via pandoc, injects sidebar navigation, and serves marimo exercises via iframe

## Project layout

```
skill-diataxis/
├── skill/
│   ├── SKILL.md                     # Skill instructions
│   ├── assets/
│   │   ├── style.css                # Standard stylesheet
│   │   └── template.html            # Pandoc HTML template
│   ├── references/
│   │   ├── quadrants.md             # Diataxis quadrant rules
│   │   ├── structure-schema.md      # diataxis.toml schema
│   │   ├── scoring.md               # Scoring rubric
│   │   └── build-pipeline.md        # Build/serve details
│   └── scripts/
│       └── build.py                 # Build pipeline and CLI
├── evals/
│   └── evals.json                   # Test cases
├── diataxis-workspace/              # Eval results and grading
├── pyproject.toml
└── README.md
```

## CLI

Requires Python 3.13+ and [pandoc](https://pandoc.org/).

```bash
# Build HTML from a diataxis/ directory
uv run diataxis build

# Build and start local servers (static on :8000, marimo on :2718)
uv run diataxis serve

# Start servers without rebuilding
uv run diataxis serve-only

# Specify a different directory
uv run diataxis build -d path/to/diataxis
```

## Authoring format

- Static prose is authored in **Markdown**
- Interactive exercises are authored as **marimo** `.py` notebooks
- All math uses **LaTeX** notation (`$...$` inline, `$$...$$` display), rendered via MathJax
- Deterministic transforms (markdown to HTML, etc.) use tools like pandoc, not LLM generation

## Documentation structure

Each Diataxis project lives in a `diataxis/` directory:

```
project-root/
└── diataxis/
    ├── diataxis.toml          # Source of truth
    ├── scores.toml            # Scoring history
    ├── tutorials/
    ├── howto/
    ├── reference/
    ├── explanation/
    ├── exercises/             # Marimo notebooks
    └── _build/                # Generated HTML
```

The `diataxis.toml` structure document defines topics, what each file should cover, and guidance notes that serve as both the generation brief and scoring criteria.
