# Build and Serve Pipeline

The build pipeline transforms authored content (markdown + marimo notebooks) into
user-facing HTML. The publish step is always separate from authoring — the skill
never generates HTML directly.

## Table of Contents

- [Overview](#overview)
- [Build Steps](#build-steps)
- [Marimo WASM Export](#marimo-wasm-export)
- [Serve](#serve)
- [Publish](#publish)
- [Directory Structure](#directory-structure)

---

## Overview

The pipeline reads `diataxis/diataxis.toml` as its manifest and produces a
`diataxis/_build/` directory containing static HTML files, assets, and
self-contained exercise bundles. The output is fully static: exercises run in
the browser via Pyodide, so no separate marimo server process is required.

```
diataxis.toml ──┐
                │
markdown files ─┼── build script ── _build/ (HTML + WASM exercise bundles)
                │
marimo notebooks ─ marimo export html-wasm ─┘
```

All transforms in the build pipeline are deterministic. The build script does not
generate or modify prose content — it transforms formats and assembles the final output.

---

## Build Steps

### 1. Validate structure

Read `diataxis.toml` and verify:
- All referenced files exist
- No orphan files (files in docs directories not listed in structure)
- Exercise files exist for entries that reference them

Report any issues before proceeding.

### 2. Convert the site introductory page

Convert `diataxis/index.md` to `_build/index.html`. This is the site root — the
first page a reader lands on — and it is authored, not generated. The build
step runs it through pandoc like any other markdown file and never overwrites
it. If `diataxis/index.md` is absent the build simply skips the home page.

The intro page must answer two questions concisely:

- **Why does this project exist?** What problems does it solve? Draw from the
  `purpose` field in `diataxis.toml`.
- **What does it do?** A brief description of what the project provides. Draw
  from the `description` field.

It is a signpost. It orients the reader and links into the four quadrant
sections rather than explaining things in detail itself. Typical links:

- "New here? Start with the tutorial" (points to tutorials/)
- "Need to do X? See the how-to guides" (points to howto/)
- "Looking up specifics? Check the reference" (points to reference/)
- "Want to understand why? Read the explanation" (points to explanation/)

### 3. Generate quadrant landing pages

For each quadrant directory (`tutorials/`, `howto/`, `reference/`, `explanation/`),
generate an `index.md` from the structure document. Landing pages contain:

- A heading and brief overview of the section
- Organized links to each document in the section, grouped by topic
- Brief descriptions pulled from the `covers` fields

Landing pages are generated, not authored. They are overwritten on each build.

### 4. Convert markdown to HTML

Use `pandoc` for all markdown-to-HTML conversion:

```bash
pandoc input.md \
    --from markdown \
    --to html5 \
    --standalone \
    --mathjax \
    --template=template.html \
    --metadata title="Page Title" \
    --toc \
    --toc-depth=2 \
    -o output.html
```

The `--mathjax` flag enables LaTeX math rendering. All mathematical expressions
in the markdown source should use standard LaTeX delimiters (`$...$` for inline,
`$$...$$` for display). MathJax is loaded from CDN in the HTML template.

The template provides consistent styling, navigation, MathJax configuration, and
the iframe insertion points for exercise bundles.

### 5. Export exercises to WASM bundles

For every unique exercise referenced in `diataxis.toml`, export the marimo
notebook to a self-contained WASM HTML bundle:

```bash
marimo export html-wasm path/to/exercises/basic-ops.py \
    -o _build/exercises/basic-ops/ \
    --mode run \
    -f
```

Each bundle is a directory containing its own `index.html` and `assets/`, all
with relative paths, so the bundle is relocatable. The bundles load Pyodide in
the browser — no server-side Python is needed to run exercises.

### 6. Insert exercise iframe references

For pages that reference exercises in `diataxis.toml`, insert iframe elements
pointing at the exported bundles. Because exercises live under
`_build/exercises/` and pages live under `_build/<quadrant>/`, the src uses a
relative path:

```html
<div class="marimo-exercise">
    <h3>Exercise: Basic Ops</h3>
    <iframe
        src="../exercises/basic-ops/index.html"
        sandbox="allow-scripts allow-same-origin allow-downloads allow-popups allow-forms"
        width="100%"
        height="600"
        loading="lazy">
    </iframe>
</div>
```

Because the iframe src is a relative path inside `_build/`, the page works
identically under `diataxis serve`, under any static file host, and after
`publish` copies the tree to `~/Sites/<slug>/`.

The exercise heading and iframe height come from the exercise entry in
`diataxis.toml`. A bare string (`"exercises/foo.py"`) uses a humanized title
derived from the file stem and the default 600px height. A table entry
(`{ file = "exercises/foo.py", title = "Foo", height = 800 }`) overrides
either or both.

### 7. Generate site navigation

Build a navigation structure from `diataxis.toml`:
- Top-level links to each quadrant section
- Within each section, links to individual documents
- Breadcrumb trail on each page
- Previous/next links based on topic ordering

Inject navigation into each HTML page via the pandoc template.

### 8. Copy assets

Copy any static assets (images, CSS, fonts) to `_build/assets/`.

---

## Marimo WASM Export

Each exercise is exported independently via `marimo export html-wasm`. The
resulting bundle under `_build/exercises/<stem>/` contains the full marimo JS
runtime plus Pyodide, so it is large (on the order of tens of MB per exercise).
Bundles are not deduplicated across exercises.

**Caching.** Because export is the slowest step, the build preserves any
existing `_build/exercises/` tree across rebuilds and only re-runs the export
for a given exercise when its source `.py` is newer than the exported
`index.html`. An unchanged `.py` will reuse its bundle, so iterating on prose
does not trigger a full re-export.

Requirements for the exercise `.py` files:

- Must be a valid marimo notebook (`marimo.App()` with `@app.cell` functions).
- Must only import packages available under Pyodide. Pure-Python packages and
  the common scientific stack (numpy, pandas, scipy, matplotlib) are supported;
  packages requiring system C libraries or OS-level resources are not.
- Should be self-contained — do not `import` from sibling project modules.

The `marimo` CLI must be available on `PATH` during the build. It is declared
as a runtime dependency in `pyproject.toml`, so `uv run diataxis build` picks
it up automatically.

The iframe must be served over HTTP (not `file://`) because the bundle loads
its assets via fetch. `diataxis serve`, any static host, and `~/Sites/` served
over HTTP all satisfy this.

---

## Serve

The `serve` command rebuilds the site and starts a single static server:

```bash
# Build only
uv run diataxis build

# Build and serve on localhost:8000
uv run diataxis serve

# Serve existing build without rebuilding
uv run diataxis serve-only
```

Because exercises are pre-exported WASM bundles, there is no second server
process and no port coordination. The static server alone is sufficient.

---

## Publish

The `publish` command deploys a built site to a user-level sites directory
(`~/Sites/` by default) so it can be viewed alongside other published projects.

```bash
# Rebuild and deploy to ~/Sites/<project-slug>/
uv run diataxis publish

# Deploy somewhere other than ~/Sites
uv run diataxis publish --sites-dir /path/to/sites
```

### What publish does

1. **Rebuilds the site.** Publish always runs the full build first, so the
   deployed output reflects the current sources. There is no way to publish
   stale `_build/` contents.
2. **Derives a slug from `project.name`.** The project name in `diataxis.toml`
   is lowercased and any run of non-alphanumeric characters is collapsed to a
   hyphen. For example, `"Hello World Docs"` becomes `hello-world-docs`. The
   command fails if the slug is empty.
3. **Copies `_build/` to `<sites-dir>/<slug>/`.** Any existing directory at
   that destination is removed first, so re-publishing replaces the previous
   copy cleanly. Exercise bundles under `_build/exercises/` come along with
   the rest of the tree, so exercises keep working after publish.
4. **Writes a per-project manifest.** A small JSON file at
   `<sites-dir>/<slug>/.diataxis-meta.json` records the project name, slug,
   and description. This is what the top-level catalog reads.
5. **Regenerates the top-level catalog.** `<sites-dir>/index.html` is rendered
   from the Jinja2 template at `skill/assets/sites-index.html.j2` by scanning
   every `<sites-dir>/*/.diataxis-meta.json` manifest. Projects appear in
   alphabetical order by slug. Projects without a manifest are ignored.

### Requirements

- `project.name` must be set in `diataxis.toml`. An empty or missing name is
  an error.
- `jinja2` is a runtime dependency (pulled in via `pyproject.toml`).
- The destination `<sites-dir>` is created if it does not exist.
- `~/Sites/` (or whichever sites directory is used) must be served over HTTP
  for exercise iframes to load.

### Directory layout after publishing

```
~/Sites/
├── index.html                        # Generated catalog, overwritten on every publish
├── hello-world-docs/
│   ├── index.html                    # Copied from _build/
│   ├── tutorials/
│   ├── howto/
│   ├── reference/
│   ├── explanation/
│   ├── exercises/                    # WASM bundles, one subdir per exercise
│   │   └── basic-ops/
│   │       ├── index.html
│   │       └── assets/
│   ├── assets/
│   └── .diataxis-meta.json           # {name, slug, description}
└── another-project/
    └── ...
```

---

## Directory Structure

After a build:

```
project-root/
└── diataxis/
    ├── diataxis.toml
    ├── tutorials/
    │   ├── index.md              # Generated landing page
    │   └── basic-ops.md          # Authored content
    ├── howto/
    ├── reference/
    ├── explanation/
    ├── exercises/
    │   └── basic-ops.py          # Marimo notebook source
    └── _build/
        ├── index.html            # Site root / home page
        ├── tutorials/
        │   ├── index.html        # Landing page
        │   └── basic-ops.html    # Converted from markdown
        ├── howto/
        ├── reference/
        ├── explanation/
        ├── exercises/            # Exported WASM bundles
        │   └── basic-ops/
        │       ├── index.html
        │       └── assets/
        └── assets/
            ├── style.css
            └── nav.js
```

The `_build/` directory is the only output. It should be added to `.gitignore`
since it is fully reproducible from the source files. All paths in `diataxis.toml`
are relative to the `diataxis/` directory.
