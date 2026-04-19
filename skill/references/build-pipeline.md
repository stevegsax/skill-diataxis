# Build Pipeline

The `diataxis/` directory is a plain [Hugo](https://gohugo.io/) site. Hugo
renders the markdown, builds navigation from the section hierarchy, applies
the theme, and produces the final HTML. The skill does not build the site;
it only manages the content Hugo consumes.

The one piece Hugo cannot do on its own is export marimo `.py` notebooks to
self-contained WASM bundles. That's what the `Makefile` is for.

## Table of Contents

- [Overview](#overview)
- [The Makefile](#the-makefile)
- [Hugo configuration](#hugo-configuration)
- [Content authoring conventions](#content-authoring-conventions)
- [Marimo WASM export](#marimo-wasm-export)
- [Theme](#theme)
- [Serving](#serving)
- [Deploying](#deploying)
- [Directory structure](#directory-structure)

---

## Overview

```
                               make build
                               ─────────────
diataxis.toml ─────► (Hugo data file)        ─┐
                                               │
tutorials/*.md  ───► (Hugo content mounts)    ─┼─► hugo ──► public/
howto/*.md                                     │
reference/*.md                                 │
explanation/*.md                               │
index.md                                       │
                                               │
exercises/*.py  ───► marimo export html-wasm ─┘   (writes to static/exercises/)
```

Everything above is deterministic. The skill's job is to keep the authored
files valid and in sync with `diataxis.toml`; the Makefile's job is to run
the marimo export; Hugo's job is to render the site.

---

## The Makefile

```makefile
EXERCISE_SOURCES := $(wildcard exercises/*.py)
EXERCISE_BUNDLES := $(patsubst exercises/%.py,static/exercises/%/index.html,$(EXERCISE_SOURCES))

.PHONY: build serve exercises clean

build: exercises
	hugo --cleanDestinationDir

serve: exercises
	hugo server

exercises: $(EXERCISE_BUNDLES)

clean:
	rm -rf public resources

static/exercises/%/index.html: exercises/%.py
	@mkdir -p $(@D)
	uv run marimo export html-wasm $< -o $(@D) --mode run -f
```

Targets:

- `make build` — export exercises (only those whose `.py` is newer than
  the bundle), then run `hugo` into `public/`.
- `make serve` — export exercises, then run `hugo server` for live reload.
- `make exercises` — export exercises only. Useful if you're iterating on
  prose and don't want `hugo` to run.
- `make clean` — remove Hugo's output (`public/`) and cache (`resources/`).
  The WASM bundles under `static/exercises/` survive, because re-exporting
  them is slow.

The Makefile is the only build tool. Users who prefer to run `hugo`
directly can do so after `make exercises` — the Makefile is just
convenience over the explicit sequence.

---

## Hugo configuration

`diataxis/hugo.toml` (user-owned after scaffold) declares the theme and
mounts the authored paths into Hugo's expected content tree:

```toml
[module]
  [[module.imports]]
    path = "github.com/imfing/hextra"

  # Authored quadrants → Hugo content sections
  [[module.mounts]]
    source = "tutorials"
    target = "content/tutorials"
  [[module.mounts]]
    source = "howto"
    target = "content/howto"
  [[module.mounts]]
    source = "reference"
    target = "content/reference"
  [[module.mounts]]
    source = "explanation"
    target = "content/explanation"

  # Homepage
  [[module.mounts]]
    source = "index.md"
    target = "content/_index.md"

  # Editorial metadata as a Hugo data file
  [[module.mounts]]
    source = "diataxis.toml"
    target = "data/diataxis.toml"

  # Marimo WASM bundles as static assets
  [[module.mounts]]
    source = "static"
    target = "static"
```

The mounts keep authored paths skill-native (`tutorials/first-project.md`,
not `content/tutorials/first-project.md`). Hugo sees the content at its
expected locations.

---

## Content authoring conventions

The skill generates markdown that Hugo can consume directly. Each file starts
with a TOML frontmatter block:

```toml
+++
title = "Your First Project"
weight = 11
description = "First steps with the Widget library"
topic = "getting-started"
covers = ["Installing the library", "Creating a first widget"]
detail = "Step-by-step with code examples."
+++
```

Conventions:

- `title` comes from the H1 the author would otherwise write. The H1 is
  **not** repeated in the body — Hugo's theme renders the title from
  frontmatter, and duplicating it in the body produces a visible duplicate.
- `weight` is `topic.order * 10 + quadrant_weight`, where quadrant_weight is
  1 (tutorials), 2 (howto), 3 (reference), 4 (explanation). This gives the
  sidebar the standard Tutorials → How-to → Reference → Explanation order
  within each topic.
- `description` comes from the topic's `description`.
- `topic`, `covers`, and `detail` pass the editorial metadata through as
  page params so any theme template that wants them can read them.

The homepage (`index.md`) has its own frontmatter with `[cascade] type = "docs"`
so every child page inherits the theme's docs layout.

When an entry in `diataxis.toml` lists exercises, the author appends an
`## Exercises` section at the end of the body with markdown links to each
exercise's standalone page (`/exercises/<stem>/`).

---

## Marimo WASM export

Each exercise `.py` is exported to a self-contained WASM HTML bundle:

```bash
uv run marimo export html-wasm exercises/basic-ops.py \
    -o static/exercises/basic-ops/ \
    --mode run \
    -f
```

The bundle is a directory with its own `index.html` plus all assets, all
using relative paths. It loads Pyodide in the browser — no server-side
Python is needed to run exercises.

**Caching.** Export is slow. The Makefile declares each bundle's
`index.html` as a target with the corresponding `.py` as a prerequisite, so
`make` only rebuilds bundles whose sources have changed.

**Standalone rendering.** Exercise bundles bypass Hugo's theme entirely.
They keep their own look and feel (marimo's UI), and parent tutorials link
to them via the `## Exercises` section appended during content generation.
There are no iframes.

Requirements for exercise `.py` files:

- Must be a valid marimo notebook (`marimo.App()` with `@app.cell` functions).
- Must only import packages available under Pyodide. Pure-Python packages and
  the common scientific stack (numpy, pandas, scipy, matplotlib) are supported;
  packages requiring system C libraries or OS-level resources are not.
- Should be self-contained — do not `import` from sibling project modules.

---

## Theme

The default theme is [Hextra](https://imfing.github.io/hextra/), imported as
a Hugo module in the scaffolded `hugo.toml`:

```toml
[[module.imports]]
  path = "github.com/imfing/hextra"
```

Hextra supplies: sidebar navigation auto-generated from sections, search,
dark mode, KaTeX math, mermaid diagrams, syntax highlighting, TOC, and
responsive layouts.

**Switching themes.** Edit `hugo.toml` and replace the `module.imports`
entry with any other Hugo module theme. Examples:

- `github.com/alex-shpak/hugo-book`
- `github.com/McShelby/hugo-theme-relearn`
- `github.com/hugo-sid/hugo-blog-awesome`

Then:

```bash
cd diataxis && hugo mod get -u
make build
```

Because the skill writes only standard Hugo frontmatter and generic semantic
markdown, any theme that follows Hugo conventions renders the content.
Theme-specific features (search, dark mode toggle, etc.) are the theme's
concern, not the skill's.

**Overriding layouts.** Drop files into `diataxis/layouts/` to override any
template from the current theme. Hugo's layout lookup prefers local files
over theme files.

---

## Serving

`make serve` runs `hugo server` after re-exporting exercises. Hugo's server
provides live reload — edits to `hugo.toml` or anything under `layouts/`
are picked up automatically.

Edits to authored markdown (`tutorials/`, `howto/`, etc.) and to
`diataxis.toml` are also picked up live, because the mounts map them
directly into Hugo's content tree — there's no intermediate staging step.

Press Ctrl+C to stop the server.

---

## Deploying

There is no `diataxis publish` command. The deployable site is
`diataxis/public/`. Deploy it with any standard Hugo workflow:

- `hugo deploy` to S3, Azure, GCS
- Push to a Git branch that Netlify/Vercel/Cloudflare Pages watches
- `rsync` to a static host
- GitHub Pages via Actions

See [Hugo's hosting and deployment docs](https://gohugo.io/hosting-and-deployment/).

---

## Directory structure

After a build:

```
<project-root>/
└── diataxis/
    ├── diataxis.toml             # editorial source of truth
    ├── hugo.toml                 # Hugo config (user-owned)
    ├── go.mod                    # Hugo module manifest
    ├── go.sum                    # Module checksum (generated by Hugo)
    ├── Makefile                  # build orchestration
    ├── README.md                 # guard file
    ├── index.md                  # homepage (has Hugo frontmatter)
    ├── scores.toml               # scoring history
    ├── tutorials/
    │   └── basic-ops.md          # authored markdown with Hugo frontmatter
    ├── howto/
    ├── reference/
    ├── explanation/
    ├── exercises/
    │   └── basic-ops.py          # authored marimo notebook
    ├── static/
    │   └── exercises/            # WASM bundles (Makefile target)
    │       └── basic-ops/
    │           ├── index.html
    │           └── assets/
    ├── layouts/                  # optional theme overrides (user-owned)
    ├── resources/                # Hugo cache (gitignored)
    └── public/                   # Hugo output (gitignored)
```

Committed: `diataxis.toml`, `hugo.toml`, `go.mod`, `go.sum`, `Makefile`,
`README.md`, authored markdown and notebooks, and any `layouts/` overrides.

Gitignored: `public/`, `resources/`, `static/exercises/` (regenerable from
the `.py` sources).
