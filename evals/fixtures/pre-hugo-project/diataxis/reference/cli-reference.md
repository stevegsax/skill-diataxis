# CLI Reference

All commands are run via `uv run`.

## Synopsis

```
uv run diataxis [-h] [-v] {build,serve,serve-only,publish} [-d DIR] ...
```

## Global options

| Flag | Description |
|------|-------------|
| `-h`, `--help` | Show help and exit |
| `-v`, `--version` | Print the `diataxis` version and exit |

The `-d`/`--dir` flag is defined per subcommand, not at the top level. It
must appear after the subcommand name.

## diataxis build

Build HTML from markdown sources.

Reads `diataxis.toml`, validates that every referenced content and exercise
file exists, generates quadrant landing pages, converts markdown to HTML via
`pandoc`, exports each marimo exercise to a self-contained WASM bundle under
`_build/exercises/<stem>/`, injects sidebar navigation, and inserts iframe
references pointing at the exercise bundles.

Output is written to `<diataxis-dir>/_build/`.

### Flags

| Flag | Default | Description |
|------|---------|-------------|
| `-d`, `--dir` | `./diataxis` | Path to the diataxis directory |

### Behavior notes

- **Validation is fatal.** Missing content files, missing exercise files, or
  exercise stem collisions abort the build with a non-zero exit.
- **Mermaid pre-rendering.** If `mmdc` is on `PATH`, ` ```mermaid ` blocks are
  pre-rendered to SVG in `_build/assets/mermaid/`. If it is not, blocks are
  left as-is and a warning is printed.
- **WASM export caching.** The `_build/exercises/` subtree is preserved
  across rebuilds. An exercise is re-exported only when its source `.py` is
  newer than the previously exported `index.html`. Unchanged exercises are
  reused.
- **Marimo is required for exercises.** When `diataxis.toml` references any
  exercise, `marimo` must be on `PATH`. A missing binary is a fatal error.

### Example

```bash
uv run diataxis build
uv run diataxis build -d examples/self-docs
```

## diataxis serve

Build and start a local static server.

Runs the full build, then starts a single HTTP server on `localhost:8000`
rooted at `_build/`. Exercises run in the browser via Pyodide — no separate
process is required.

### Flags

| Flag | Default | Description |
|------|---------|-------------|
| `-d`, `--dir` | `./diataxis` | Path to the diataxis directory |

If port 8000 is in use, the next available port up to 8099 is selected and
reported on startup.

Press Ctrl+C to stop the server.

### Example

```bash
uv run diataxis serve
```

## diataxis serve-only

Start the static server without rebuilding. Requires a previous build
(`_build/` must exist).

### Flags

| Flag | Default | Description |
|------|---------|-------------|
| `-d`, `--dir` | `./diataxis` | Path to the diataxis directory |

### Example

```bash
uv run diataxis serve-only
```

## diataxis publish

Rebuild the site and copy it to a user-level sites directory so it can be
viewed alongside other published projects.

The project name from `diataxis.toml` is lowercased and non-alphanumeric runs
are collapsed to hyphens to form a slug. `_build/` is copied to
`<sites-dir>/<slug>/`; any existing directory at that path is replaced
atomically. A per-project manifest (`.diataxis-meta.json`) is written, and
`<sites-dir>/index.html` is regenerated from every project's manifest.

### Flags

| Flag | Default | Description |
|------|---------|-------------|
| `-d`, `--dir` | `./diataxis` | Path to the diataxis directory |
| `--sites-dir` | `~/Sites` | Target sites directory |

### Example

```bash
uv run diataxis publish
uv run diataxis publish --sites-dir /path/to/sites
```

## Exit codes

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | Fatal error (missing files, invalid `diataxis.toml`, missing `marimo` when exercises are present, etc.) |

## See also

- [How to Build and Serve Documentation](../howto/build-and-serve.html) — the
  task-focused walkthrough for the same commands.
- [How to Install and Set Up](../howto/install-and-setup.html) — installing
  `uv`, `pandoc`, `mmdc`, and the `diataxis` CLI.
- [diataxis.toml Schema](diataxis-toml-schema.html) — the manifest these
  commands read.
