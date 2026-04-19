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

Publishing is handled by [Hugo](https://gohugo.io/). The `diataxis/` directory is a plain Hugo site — the skill authors the content (markdown, frontmatter, marimo notebooks) and Hugo builds the HTML. A small `Makefile` preprocesses marimo notebooks into WASM bundles (Hugo cannot do that on its own) and then invokes `hugo`. Layouts, navigation, styling, math, mermaid, and search come from whichever Hugo theme is configured in `hugo.toml`; the skill scaffolds a sensible default ([Hextra](https://imfing.github.io/hextra/)) but users can swap themes freely.

See [`skill/SKILL.md`](skill/SKILL.md) for the instructions Claude loads when the skill is invoked.

## Worked example

**The documentation for this repository is itself authored with this skill.** The complete inputs (`diataxis.toml`, markdown, marimo exercises) and generated HTML live under [`examples/self-docs/`](examples/self-docs/). Rebuild it locally with:

```bash
make -C examples/self-docs build
```

## Requirements

- Python 3.13+ and [uv](https://docs.astral.sh/uv/)
- [Hugo extended](https://gohugo.io/installation/) — renders the site
- [Go](https://go.dev/) 1.21+ — needed by Hugo to resolve theme modules
- [nushell](https://www.nushell.sh/) — for the deterministic check suite

This skill was developed on macOS. Paths, shell commands, and tooling assumptions (e.g. zsh) will likely need adjustment to run on Windows or Linux.

## External tools

A key design insight of this project is that our computers already host tools for managing web text. We're not starting from scratch. The robot *uses* those tools — it does not replace them. It is a teammate and collaborator: it makes editorial decisions and orchestrates the pipeline, while each tool below does the work it was built for.

`uv sync` installs the Python dependencies; the rest are installed separately.

- **Hugo** — renders the site. The skill stages a Hugo site from the authored content (markdown + frontmatter derived from `diataxis.toml`) and invokes `hugo` to produce the final HTML. Layouts, navigation, syntax highlighting, math, mermaid, and search all come from the chosen Hugo theme.
- **nushell** (`nu`) — runs the deterministic check suite under `skill/checks/` that validates structure, cross-links, quadrant rules, and formatting before any LLM scoring pass
- **marimo** — exports each exercise `.py` notebook to a self-contained WASM HTML bundle that runs in-browser via Pyodide. Bundles live at `/exercises/<stem>/` as standalone pages with their own look and feel.
- **check-jsonschema** — validates `diataxis.toml` against the bundled schema and verifies check-suite output against `check-schema.json` (dev-group dependency)

**Future directions:** The list above isn't exhaustive. We haven't added **textlint** or other style checkers, but nothing prevents it. The skill assumes a full system underneath — anything you could install and run yourself is also available to the robot.

## Choosing a theme

The first build scaffolds `<diataxis-dir>/site/hugo.toml` with [Hextra](https://imfing.github.io/hextra/) preconfigured. Hextra provides sidebar navigation, search, dark mode, KaTeX math, mermaid, syntax highlighting, and responsive layouts out of the box.

To use a different theme, edit `site/hugo.toml` and replace the `module.imports` entry with any Hugo module theme (see [themes.gohugo.io](https://themes.gohugo.io/)). Then:

```bash
cd site && hugo mod get -u && cd ..
uv run diataxis build
```

Because the stager writes standard Hugo frontmatter and generic semantic markdown, any convention-following theme renders the content correctly. Theme-specific features (custom nav, search, etc.) are the theme's concern.

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
- **Build** — `make build` (or `hugo` directly). The `diataxis/` directory is a plain Hugo site; layouts, navigation, and styling come from the chosen theme. Marimo exercises are exported to self-contained WASM bundles by the Makefile and served as standalone pages.

## Project layout

```
skill-diataxis/
├── skill/
│   ├── SKILL.md                     # Skill instructions
│   ├── assets/
│   │   └── diataxis-schema.json     # JSON Schema for diataxis.toml
│   ├── templates/                   # Scaffolded into new diataxis/ projects
│   │   ├── Makefile                 # make build / make serve
│   │   ├── hugo.toml                # Hugo config with content mounts
│   │   └── go.mod                   # Hugo module manifest
│   ├── references/
│   │   ├── quadrants.md             # Diataxis quadrant rules
│   │   ├── structure-schema.md      # diataxis.toml schema
│   │   ├── scoring.md               # Scoring rubric
│   │   └── build-pipeline.md        # Hugo + Makefile pipeline details
│   └── checks/
│       ├── run-checks.nu            # Deterministic check runner
│       ├── check-schema.json        # JSON Schema for check output
│       └── check-*.nu               # Individual structural/format checks
├── examples/
│   └── self-docs/                   # Worked example: documents this project
├── evals/
│   └── evals.json                   # Test cases
├── diataxis-workspace/              # Scratch area for eval runs and grading output
├── pyproject.toml
└── README.md
```

## Authoring format

- Static prose is authored in **Markdown** using generic, semantic HTML5 — no skill-specific CSS classes. Any Hugo theme renders the content correctly.
- Interactive exercises are authored as **marimo** `.py` notebooks, exported to self-contained WASM bundles that run in-browser via Pyodide (no marimo server required)
- Diagrams are authored as **mermaid** fenced code blocks, rendered client-side by the theme
- All math uses **LaTeX** notation (`$...$` inline, `$$...$$` display), rendered by the theme (KaTeX or MathJax depending on the theme)
- Deterministic transforms (markdown to HTML, schema validation, structural checks) use tools like Hugo, `check-jsonschema`, and nushell — not LLM generation

## Documentation structure

Each Diataxis project lives in a `diataxis/` directory:

```
project-root/
└── diataxis/
    ├── diataxis.toml          # Source of truth (authored)
    ├── hugo.toml              # Hugo config (user-owned after scaffold)
    ├── go.mod                 # Hugo module manifest (user-owned)
    ├── Makefile               # Build orchestration (user-owned)
    ├── README.md              # Guard file ("this is generated")
    ├── index.md               # Homepage (authored, has Hugo frontmatter)
    ├── scores.toml            # Scoring history across runs
    ├── tutorials/             # Authored markdown with Hugo frontmatter
    ├── howto/
    ├── reference/
    ├── explanation/
    ├── exercises/             # Authored marimo notebooks
    ├── layouts/               # Optional theme overrides (user-owned)
    ├── static/exercises/      # WASM bundles (regenerated by `make exercises`)
    └── public/                # Rendered site — deploy this
```

The `diataxis.toml` structure document defines topics, what each file should cover, and guidance notes that serve as both the generation brief and scoring criteria. `scores.toml` accumulates the result of each scoring pass so regressions across runs are visible over time.

## Building

The `diataxis/` directory is a plain Hugo site with one extra step: marimo notebooks must be exported to WASM bundles before Hugo runs. A small `Makefile` handles that:

```bash
cd diataxis
make build           # export exercises + hugo
make serve           # export exercises + hugo server (live reload)
make exercises       # export exercises only
make clean           # remove public/ and resources/
```

For the bundled self-documentation example:

```bash
make -C examples/self-docs build
```

Users who prefer to skip `make` can run `hugo` directly after ensuring exercises are exported. The rendered site lands at `diataxis/public/`. Deploy it with any Hugo-compatible workflow (`hugo deploy`, Netlify, GitHub Pages, rsync, etc.). See [Hugo's hosting docs](https://gohugo.io/hosting-and-deployment/) for the full catalog.
