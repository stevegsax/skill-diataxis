# How to Build and Serve Documentation

## Build HTML

From your project root (the directory containing `diataxis/`):

```bash
uv run diataxis build
```

Output appears in `diataxis/_build/`. Each markdown file becomes an HTML page
with navigation and styling. If any markdown files contain ` ```mermaid ` blocks
and `mmdc` is installed, the diagrams are pre-rendered to SVG in
`_build/assets/mermaid/`.

## Serve locally

```bash
uv run diataxis serve
```

This builds first, then starts a static file server on
`http://localhost:8000`. Exercises run in the browser via Pyodide, so there
is no separate server process.

Open `http://localhost:8000` in your browser. Press Ctrl+C to stop the server.

## Serve without rebuilding

If you've already built and just want to restart the server:

```bash
uv run diataxis serve-only
```

## Rebuild after changes

After editing markdown files or `diataxis.toml`, rebuild:

```bash
uv run diataxis build
```

Landing pages and navigation are regenerated from `diataxis.toml` on every
build. The `_build/` directory is replaced entirely.

## Use a custom directory

If your diataxis content is not in `./diataxis`, pass `-d` after the
subcommand:

```bash
uv run diataxis build -d path/to/my-diataxis
```

For the full CLI reference, see [CLI Reference](../reference/cli-reference.html).
