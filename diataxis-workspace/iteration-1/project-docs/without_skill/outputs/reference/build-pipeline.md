# Build Pipeline Reference

The build pipeline transforms authored markdown and marimo notebooks into browsable HTML. It is implemented in `skill/scripts/build.py`.

## CLI Usage

```bash
python -m scripts.build [diataxis-dir] [--serve] [--serve-only]
```

| Argument | Default | Description |
|----------|---------|-------------|
| `diataxis-dir` | `diataxis` | Path to the diataxis directory |
| `--serve` | Off | Start servers after building |
| `--serve-only` | Off | Start servers without rebuilding |

## Build Steps

| Step | Action | Input | Output |
|------|--------|-------|--------|
| 1. Validate | Check that all files in `diataxis.toml` exist | `diataxis.toml` | Warnings to stderr |
| 2. Generate landing pages | Create `index.md` for each quadrant and the site root | `diataxis.toml` | `index.md`, `tutorials/index.md`, `howto/index.md`, `reference/index.md`, `explanation/index.md` |
| 3. Convert markdown | Run pandoc on all `.md` files | `.md` files | `.html` files in `_build/` |
| 4. Insert exercise iframes | Add marimo iframe blocks to tutorial HTML | `diataxis.toml` exercises entries | Modified HTML files |
| 5. Copy assets | Copy `_assets/` to `_build/assets/` | `_assets/` directory | `_build/assets/` |
| 6. Generate marimo config | Create ASGI app for serving exercises | Exercise entries | `_serve_exercises.py` |

## Pandoc Conversion

Each markdown file is converted with:

```bash
pandoc input.md --from markdown --to html5 --standalone \
    --metadata title="Page Title" --toc --toc-depth=2 -o output.html
```

If a template exists at `_templates/page.html`, it is passed via `--template`.

## Marimo Integration

Exercises are served via a marimo ASGI app on port 2718. The build script generates `_serve_exercises.py` which mounts each exercise at `/exercises/<stem>`.

Iframes are inserted into the HTML before the closing `</body>` tag:

```html
<div class="marimo-exercise">
    <h3>Exercise: Basic Ops</h3>
    <iframe src="http://localhost:2718/exercises/basic-ops"
        sandbox="allow-scripts allow-same-origin allow-downloads allow-popups allow-forms"
        width="100%" height="600" loading="lazy">
    </iframe>
</div>
```

## Server Ports

| Server | Port | Serves |
|--------|------|--------|
| Static (http.server) | 8000 | `_build/` directory |
| Marimo (uvicorn) | 2718 | Interactive exercise notebooks |

## Directory Structure After Build

```
diataxis/
├── diataxis.toml
├── scores.toml
├── _serve_exercises.py          # Generated if exercises exist
├── tutorials/
│   ├── index.md                 # Generated landing page
│   └── *.md                     # Authored content
├── howto/
│   ├── index.md
│   └── *.md
├── reference/
│   ├── index.md
│   └── *.md
├── explanation/
│   ├── index.md
│   └── *.md
├── exercises/
│   └── *.py                     # Marimo notebooks
├── _assets/                     # Static assets (optional)
└── _build/                      # Build output
    ├── index.html
    ├── tutorials/
    │   ├── index.html
    │   └── *.html
    ├── howto/
    ├── reference/
    ├── explanation/
    └── assets/
```

The `_build/` directory is fully reproducible and should be added to `.gitignore`.
