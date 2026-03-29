# Build Pipeline Reference

The build pipeline transforms authored markdown and marimo notebooks into static HTML documentation. It reads `diataxis.toml` as its manifest and produces a `_build/` directory.

## CLI Usage

```
python -m scripts.build [diataxis-dir] [--serve] [--serve-only]
```

| Argument | Default | Description |
|----------|---------|-------------|
| `diataxis-dir` | `./diataxis` | Path to the diataxis directory |
| `--serve` | off | Start servers after building |
| `--serve-only` | off | Start servers without rebuilding |

## Pipeline Steps

| Step | Input | Output | Description |
|------|-------|--------|-------------|
| 1. Validate | `diataxis.toml` | warnings to stderr | Checks that all referenced content and exercise files exist |
| 2. Generate landing pages | `diataxis.toml` | `index.md` per quadrant + root `index.md` | Creates navigation pages from structure metadata |
| 3. Convert markdown | `*.md` files | `_build/**/*.html` | Runs pandoc with `--toc --toc-depth=2 --standalone` |
| 4. Insert iframes | HTML files with exercises | modified HTML | Adds marimo iframe elements before `</body>` |
| 5. Generate navigation | `diataxis.toml` | injected into HTML | Top-level links, breadcrumbs, prev/next based on topic order |
| 6. Copy assets | `_assets/` directory | `_build/assets/` | Static files (CSS, images, fonts) |
| 7. Generate marimo config | exercise entries | `_serve_exercises.py` | ASGI app script for marimo notebook serving |

## Pandoc Conversion

Each markdown file is converted with:

```bash
pandoc input.md \
    --from markdown \
    --to html5 \
    --standalone \
    --metadata title="Page Title" \
    --toc \
    --toc-depth=2 \
    -o output.html
```

If a template exists at `_templates/page.html`, it is passed via `--template`.

## Marimo Integration

Exercises listed in `diataxis.toml` are served via marimo's ASGI API.

| Setting | Value |
|---------|-------|
| Host | `localhost` |
| Port | `2718` (default) |
| Allow origins | `*` (required for iframe embedding) |
| Runner | uvicorn or similar ASGI server |

Mount paths are derived from exercise file stems: `exercises/basic-ops.py` mounts at `/exercises/basic-ops`.

Iframe elements inserted into HTML:

```html
<div class="marimo-exercise">
    <iframe
        src="http://localhost:2718/exercises/basic-ops"
        sandbox="allow-scripts allow-same-origin allow-downloads allow-popups allow-forms"
        width="100%" height="600" loading="lazy">
    </iframe>
</div>
```

## Serve

The `serve` command starts two processes:

| Server | Port | Serves |
|--------|------|--------|
| Static (Python `http.server`) | `8000` | `_build/` directory |
| Marimo (ASGI via uvicorn) | `2718` | Interactive exercise notebooks |

Both are stopped together on `Ctrl+C`.

## Directory Structure After Build

```
diataxis/
├── diataxis.toml
├── tutorials/
│   ├── index.md              # Generated landing page
│   └── basic-ops.md          # Authored content
├── howto/
├── reference/
├── explanation/
├── exercises/
│   └── basic-ops.py          # Marimo notebook
├── _templates/
│   └── page.html             # Optional pandoc template
├── _assets/
│   └── style.css             # Optional static assets
├── _serve_exercises.py        # Generated marimo config
└── _build/
    ├── index.html
    ├── tutorials/
    │   ├── index.html
    │   └── basic-ops.html
    ├── howto/
    ├── reference/
    ├── explanation/
    └── assets/
```

The `_build/` directory is fully reproducible and should be added to `.gitignore`.

## Further Reading

- For how to run a build, see [How to Build and Serve Documentation](../howto/build-and-serve.md)
- For the structure document that drives the build, see [Structure Document Schema](structure-document-schema.md)
