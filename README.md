# skill-diataxis

A Claude Code skill for creating, revising, scoring, and publishing documentation structured around the [Diataxis](https://diataxis.fr/) framework.

## What it does

Manages the full lifecycle of Diataxis-structured documentation:

- **Scope** — uses the grill-me skill to clarify what the user wants before starting
- **Structure** — generates a `diataxis.toml` manifest that defines topics, files, coverage criteria, and guidance notes
- **Generate** — creates content across all four Diataxis quadrants (tutorials, how-to guides, reference, explanation)
- **Score** — runs a deterministic nushell check suite, then an LLM qualitative pass against the structure document
- **Revise** — updates structure first, then content, preserving user feedback in guidance fields
- **Build** — converts markdown to HTML via pandoc, pre-renders mermaid diagrams to SVG, exports marimo exercises to self-contained WASM bundles, and injects sidebar navigation

## Project layout

```
skill-diataxis/
├── skill/
│   ├── SKILL.md                     # Skill instructions
│   ├── assets/
│   │   ├── style.css                # Standard stylesheet
│   │   ├── template.html            # Pandoc HTML template
│   │   ├── diataxis-schema.json     # JSON Schema for diataxis.toml
│   │   └── sites-index.html.j2      # Jinja2 template for ~/Sites/index.html
│   ├── references/
│   │   ├── quadrants.md             # Diataxis quadrant rules
│   │   ├── structure-schema.md      # diataxis.toml schema
│   │   ├── scoring.md               # Scoring rubric
│   │   └── build-pipeline.md        # Build/serve details
│   ├── checks/
│   │   ├── run-checks.nu            # Deterministic check runner
│   │   ├── check-schema.json        # JSON Schema for check output
│   │   └── check-*.nu               # Individual structural/format checks
│   └── scripts/
│       └── build.py                 # Build pipeline and CLI
├── examples/
│   └── self-docs/                   # Self-documentation project
├── evals/
│   └── evals.json                   # Test cases
├── diataxis-workspace/              # Eval results and grading
├── pyproject.toml
└── README.md
```

## CLI

Requires Python 3.13+, [pandoc](https://pandoc.org/), and [nushell](https://www.nushell.sh/) (for the check suite). [mermaid-cli](https://github.com/mermaid-js/mermaid-cli) (`mmdc`) is optional — required only if sources contain mermaid diagrams.

```bash
# Build HTML from a diataxis/ directory
uv run diataxis build

# Build and start a local static server on :8000
uv run diataxis serve

# Start the static server without rebuilding
uv run diataxis serve-only

# Specify a different directory
uv run diataxis build -d path/to/diataxis

# Publish the built site to ~/Sites/<project-slug>/ and refresh ~/Sites/index.html
uv run diataxis publish
```

All subcommands accept `-d <path>` to point at a non-default diataxis directory. For the bundled self-documentation example, pass the directory explicitly:

```bash
uv run diataxis publish -d examples/self-docs
```

`publish` rebuilds the site, then copies `_build/` to `~/Sites/<slug>/`, where `<slug>` is derived from `project.name` in `diataxis.toml`. It then regenerates `~/Sites/index.html` from a Jinja2 template by scanning each `~/Sites/*/.diataxis-meta.json` manifest. Pass `--sites-dir` to target a different location.

## Authoring format

- Static prose is authored in **Markdown**
- Interactive exercises are authored as **marimo** `.py` notebooks, exported to self-contained WASM bundles that run in-browser via Pyodide (no marimo server required)
- Diagrams are authored as **mermaid** fenced code blocks, pre-rendered to SVG at build time
- All math uses **LaTeX** notation (`$...$` inline, `$$...$$` display), rendered via MathJax
- Deterministic transforms (markdown to HTML, schema validation, structural checks) use tools like pandoc, `check-jsonschema`, and nushell — not LLM generation

## Documentation structure

Each Diataxis project lives in a `diataxis/` directory:

```
project-root/
└── diataxis/
    ├── diataxis.toml          # Source of truth
    ├── index.md               # Introductory page
    ├── scores.toml            # Scoring history
    ├── tutorials/
    ├── howto/
    ├── reference/
    ├── explanation/
    ├── exercises/             # Marimo notebooks
    └── _build/                # Generated HTML
```

The `diataxis.toml` structure document defines topics, what each file should cover, and guidance notes that serve as both the generation brief and scoring criteria.
