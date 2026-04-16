# Build and Serve Pipeline

The build pipeline transforms authored content (markdown + marimo notebooks) into
user-facing HTML. The publish step is always separate from authoring — the skill
never generates HTML directly.

## Table of Contents

- [Overview](#overview)
- [Build Steps](#build-steps)
- [Marimo Integration](#marimo-integration)
- [Serve](#serve)
- [Publish](#publish)
- [Directory Structure](#directory-structure)

---

## Overview

The pipeline reads `diataxis/diataxis.toml` as its manifest and produces a
`diataxis/_build/` directory containing static HTML files and assets. Interactive components (marimo
notebooks) are served by a separate marimo process — the built HTML references
them via iframes.

```
diataxis.toml ──┐
                │
markdown files ─┼── build script ── _build/ (HTML)
                │
marimo notebooks ── marimo run ──── localhost:2718 (interactive)
```

All transforms in the build pipeline are deterministic. The build script does not
generate or modify content — it transforms formats and assembles the final output.

---

## Build Steps

### 1. Validate structure

Read `diataxis.toml` and verify:
- All referenced files exist
- No orphan files (files in docs directories not listed in structure)
- Exercise files exist for entries that reference them

Report any issues before proceeding.

### 2. Generate the site introductory page

Generate `_build/index.html` from `diataxis/index.md`. This is the site root —
the first page a reader lands on. It must answer two questions concisely:

- **Why does this project exist?** What problems does it solve? Draw from the
  `purpose` field in `diataxis.toml`.
- **What does it do?** A brief description of what the project provides. Draw
  from the `description` field.

The introductory page is a signpost. It orients the reader and links into the
four quadrant sections rather than explaining things in detail itself. Typical
links:

- "New here? Start with the tutorial" (points to tutorials/)
- "Need to do X? See the how-to guides" (points to howto/)
- "Looking up specifics? Check the reference" (points to reference/)
- "Want to understand why? Read the explanation" (points to explanation/)

The introductory page is authored (in `diataxis/index.md`), not generated — it
reflects the project's voice and framing. The build step converts it to HTML
like any other markdown file.

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
the iframe insertion points for marimo notebooks.

### 5. Insert marimo iframe references

For tutorial files that have exercises listed in `diataxis.toml`, insert iframe
elements pointing to the marimo server:

```html
<div class="marimo-exercise">
    <h3>Exercise: Basic Operations</h3>
    <iframe
        src="http://localhost:2718/basic-ops"
        sandbox="allow-scripts allow-same-origin allow-downloads allow-popups allow-forms"
        width="100%"
        height="600"
        loading="lazy">
    </iframe>
</div>
```

The iframe src paths correspond to marimo's ASGI app mount points (see
[Marimo Integration](#marimo-integration)).

### 6. Generate site navigation

Build a navigation structure from `diataxis.toml`:
- Top-level links to each quadrant section
- Within each section, links to individual documents
- Breadcrumb trail on each page
- Previous/next links based on topic ordering

Inject navigation into each HTML page via the pandoc template.

### 7. Copy assets

Copy any static assets (images, CSS, fonts) to `_build/assets/`.

---

## Marimo Integration

Marimo notebooks are served via the programmatic ASGI API, mounting multiple
notebooks under a single server:

```python
import marimo

app = marimo.create_asgi_app()

# Mount at root level to avoid double-prefix redirects
app = app.with_app(path="/basic-ops", root="./exercises/basic-ops.py")
app = app.with_app(path="/simplify", root="./exercises/simplify.py")

# .build() returns the callable ASGI app
app = app.build()
```

This runs as a separate process alongside the static file server.

The build script generates the ASGI app configuration from `diataxis.toml` by
reading all `exercises` entries and mapping them to mount points.

### Marimo server configuration

- **Host**: `localhost`
- **Port**: `2718` (default, configurable)
- **Allow origins**: `*` (required for iframe embedding from the static server)
- The ASGI app should be run with uvicorn or similar

---

## Serve

The `serve` command starts both servers:

1. **Static server**: Python's `http.server` (or similar) serving `_build/` on
   port 8000
2. **Marimo server**: The ASGI app serving notebooks on port 2718

Both are started as background processes and can be stopped together.

```bash
# Build only
uv run diataxis build

# Build and serve
uv run diataxis serve

# Serve existing build
uv run diataxis serve-only
```

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
   copy cleanly.
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
    │   └── basic-ops.py          # Marimo notebook
    └── _build/
        ├── index.html            # Site root / home page
        ├── tutorials/
        │   ├── index.html        # Landing page
        │   └── basic-ops.html    # Converted from markdown
        ├── howto/
        ├── reference/
        ├── explanation/
        └── assets/
            ├── style.css
            └── nav.js
```

The `_build/` directory is the only output. It should be added to `.gitignore`
since it is fully reproducible from the source files. All paths in `diataxis.toml`
are relative to the `diataxis/` directory.
