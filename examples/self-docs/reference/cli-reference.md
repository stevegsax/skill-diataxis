# CLI Reference

All commands are run via `uv run`.

## Synopsis

```
uv run diataxis [-h] [-d DIR] {build,serve,serve-only} ...
```

## Global options

The `-d` flag works both before and after the subcommand.

| Flag | Default | Description |
|------|---------|-------------|
| `-d`, `--dir` | `./diataxis` | Path to the diataxis directory |
| `-h`, `--help` | | Show help and exit |

## diataxis build

Build HTML from markdown sources.

Reads `diataxis.toml`, validates the structure, generates landing pages,
converts markdown to HTML via pandoc, injects sidebar navigation, and inserts
marimo exercise iframes.

If `mmdc` is installed and markdown files contain ` ```mermaid ` blocks, the
diagrams are pre-rendered to SVG and saved in `_build/assets/mermaid/`. If
`mmdc` is not installed, mermaid blocks are left as-is in the output.

Output is written to `<diataxis-dir>/_build/`.

**Example:**

```bash
uv run diataxis build
uv run diataxis build -d examples/self-docs
```

## diataxis serve

Build and start local servers.

Runs the full build, then starts:

| Server | Port | Purpose |
|--------|------|---------|
| Static HTTP | 8000 | Serves `_build/` directory |
| Marimo ASGI | 2718 | Serves interactive exercise notebooks |

The marimo server only starts if exercises are defined in `diataxis.toml`.

Press Ctrl+C to stop both servers.

**Example:**

```bash
uv run diataxis serve
```

## diataxis serve-only

Start servers without rebuilding.

Requires a previous build (`_build/` must exist).

**Example:**

```bash
uv run diataxis serve-only
```
