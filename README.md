# skill-diataxis

> A Claude Code skill for generating and maintaining [Diataxis](https://diataxis.fr/)-structured documentation (tutorials, how-to guides, reference, explanation).

Keeping documentation current and complete is a task that is often forgotten or ignored. The purpose of this skill is to **delegate** documentation tasks to a robot. The skill provides criteria to evaluate the quality and completeness of the documentation. The human's role is to ensure that the correct topics are present, the lessons are thorough and correct, and the tone is appropriate. You are delegating day-to-day tasks, but the human is still responsible for editorial voice.

One of the main advantages of this tool is that we create the documentation in a separate, self-contained directory. Thus, you can **create new tutorials for projects you don't control** without messing up the original repo. In addition to general documentation for your own projects, you would use it if you ever wanted:

- A new tutorial for a framework that's customized to exactly what you're doing
- A flexible learning path for some topic that always interested you. You can start broad and then ask it to expand or remove topics following your interest
- A flexible research report on some subject

At SAX Capital, we use it to create live tutorials for our internal tools that are always up to date with the latest version of the software. It also keeps the documentation in sync with the push, but lots of tools do that.

This project is part of a larger initiative at SAX to enhance our knowledge management practices. The arrival of agents has given us both a compelling reason to do this work and a set of tools that make it practical.

**Important:** The goal of this skill is to delegate documentation generation and management to the LLM. **Hand edits to markdown files will be overwritten unless you explicitly tell the robot what to do or avoid**. Most of your changes will probably be in `diataxis.toml`.

**Note:** Page generation is currently integrated into the diataxis publishing script. This is probably a mistake — a future version will switch to a dedicated "publish" skill that delegates to a well-supported static site generator like Hugo or Jekyll.

See [`skill/SKILL.md`](skill/SKILL.md) for the instructions Claude loads when the skill is invoked.

## Worked example

**The documentation for this repository is itself authored with this skill.** The complete inputs (`diataxis.toml`, markdown, marimo exercises) and generated HTML live under [`examples/self-docs/`](examples/self-docs/). Rebuild it locally with:

```bash
uv run diataxis build -d examples/self-docs
```

## Requirements

- Python 3.13+ and [uv](https://docs.astral.sh/uv/)
- [pandoc](https://pandoc.org/)
- [nushell](https://www.nushell.sh/) — for the deterministic check suite
- [mermaid-cli](https://github.com/mermaid-js/mermaid-cli) (`mmdc`) — optional, only if sources contain mermaid diagrams

This skill was developed on macOS. Paths, shell commands, and tooling assumptions (e.g. `~/Sites/`, zsh) will likely need adjustment to run on Windows or Linux.

## External tools

A key design insight of this project is that our computers already host tools for managing web text. We're not starting from scratch. The robot *uses* those tools — it does not replace them. It is a teammate and collaborator: it makes editorial decisions and orchestrates the pipeline, while each tool below does the work it was built for.

`uv sync` installs the Python dependencies; the rest are installed separately.

- **pandoc** — converts each markdown source to HTML5 using a bundled template, with MathJax enabled for LaTeX math
- **nushell** (`nu`) — runs the deterministic check suite under `skill/checks/` that validates structure, cross-links, quadrant rules, and formatting before any LLM scoring pass
- **mmdc** (mermaid-cli) — pre-renders mermaid fenced code blocks to SVG at build time; optional and skipped when not installed
- **marimo** — exports each exercise `.py` notebook to a self-contained WASM HTML bundle that runs in-browser via Pyodide (Python dependency, no marimo server required at runtime)
- **check-jsonschema** — validates `diataxis.toml` against the bundled schema and verifies check-suite output against `check-schema.json` (dev-group dependency)
- **jinja2** — renders `~/Sites/index.html` from `sites-index.html.j2` when publishing (Python dependency)
- **uvicorn** — serves the `_build/` directory for `diataxis serve` and `serve-only` (Python dependency)

In the generated site itself, **MathJax** is loaded in the browser to render LaTeX, and **Pyodide** is bundled inside each marimo exercise to run the Python runtime client-side.

**Future directions:** The list above isn't exhaustive. We haven't added **textlint** or other style checkers, but nothing prevents it. The skill assumes a full system underneath — anything you could install and run yourself is also available to the robot.

## Install

Install Python dependencies:

```bash
uv sync
```

To make the skill available to Claude Code, copy or symlink the `skill/` directory into your Claude Code skills location (e.g. `~/.claude/skills/diataxis/`). Once installed, invoke it by asking Claude to create, update, score, or publish Diataxis documentation for a project.

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
│   └── self-docs/                   # Worked example: documents this project
├── evals/
│   └── evals.json                   # Test cases
├── diataxis-workspace/              # Scratch area for eval runs and grading output
├── pyproject.toml
└── README.md
```

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
    ├── scores.toml            # Scoring history across runs
    ├── tutorials/
    ├── howto/
    ├── reference/
    ├── explanation/
    ├── exercises/             # Marimo notebooks
    └── _build/                # Generated HTML
```

The `diataxis.toml` structure document defines topics, what each file should cover, and guidance notes that serve as both the generation brief and scoring criteria. `scores.toml` accumulates the result of each scoring pass so regressions across runs are visible over time.

## CLI

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

`publish` rebuilds the site, then copies `_build/` to `~/Sites/<slug>/`, where `<slug>` is derived from `project.name` in `diataxis.toml`. Any existing contents at that destination are removed and replaced. It then regenerates `~/Sites/index.html` from a Jinja2 template by scanning each `~/Sites/*/.diataxis-meta.json` manifest. Pass `--sites-dir` to target a different location.
