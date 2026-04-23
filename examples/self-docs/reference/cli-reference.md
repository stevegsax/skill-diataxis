+++
title = "Build Commands Reference"
weight = 44
description = "The build pipeline, CLI commands, and local development workflow"
topic = "build-pipeline"
covers = ["make build — what it does", "make serve — what it does", "make exercises — what it does", "make clean — what it does", "Running `hugo` directly without make", "WASM exercise export behavior and caching (via make's dependency graph)", "How the default Hextra theme is wired in and how to swap it"]
detail = "One subsection per target. Use a consistent format: synopsis, description, examples."
+++
There is no custom CLI. Building a Diataxis site is `make` plus `hugo`. The
`Makefile` lives inside the `diataxis/` directory; commands run from there
or via `make -C diataxis <target>`.

## Synopsis

```
make [build | serve | exercises | clean]
```

## make build

Export any marimo notebooks that have changed, then run `hugo` to render
the site.

Equivalent to:

```bash
uv run marimo export html-wasm exercises/<foo>.py -o static/exercises/<foo>/ --mode run -f   # per changed notebook
hugo --cleanDestinationDir
```

Output is written to `public/`.

### Behavior notes

- **Validation happens in Hugo.** Missing referenced files or broken
  frontmatter abort the build via Hugo's own error reporting.
- **WASM export caching.** The Makefile declares each bundle's `index.html`
  as a target whose prerequisite is the corresponding `.py` source. An
  exercise is re-exported only when its source is newer than the existing
  bundle.
- **Marimo is required when exercises exist.** If `diataxis/exercises/*.py`
  files are present, `marimo` must be available via `uv run`. A missing
  binary is a fatal error.
- **Hugo and Go are required.** `hugo` (extended) and `go` must be on
  `PATH`. Hugo resolves themes through Go modules, so both are needed even
  if you do not run any Go commands directly.

### Example

```bash
cd diataxis
make build
```

## make serve

Export exercises, then run `hugo server` with live reload.

Hugo prints the URL it bound to (usually `http://localhost:1313`). Edits
to any authored file (markdown, `diataxis.toml`, `hugo.toml`, layouts/)
are picked up automatically.

### Example

```bash
cd diataxis
make serve
```

Press Ctrl+C to stop the server.

## make exercises

Export marimo notebooks only. Useful when iterating on notebook sources
without wanting a full Hugo rebuild.

### Example

```bash
cd diataxis
make exercises
```

After this, `hugo` or `hugo server` run directly will see the updated
WASM bundles.

## make clean

Remove `public/` (Hugo output) and `resources/` (Hugo cache). Leaves
`static/exercises/` alone, because re-exporting WASM bundles is slow.

### Example

```bash
cd diataxis
make clean
```

## Running `hugo` directly

The Makefile is convenience. After ensuring exercises are exported, you can
run `hugo` or `hugo server` directly:

```bash
cd diataxis
make exercises     # only if any notebook has changed
hugo               # one-shot build
hugo server        # live reload
```

## Switching the Hugo theme

The scaffolded `hugo.toml` preconfigures [Hextra](https://imfing.github.io/hextra/):

```toml
[module]
  [[module.imports]]
    path = "github.com/imfing/hextra"
```

To use a different theme, replace that import with any module theme from
https://themes.gohugo.io/, then refresh the module cache:

```bash
cd diataxis
hugo mod get -u
```

The authored markdown uses standard Hugo frontmatter (`title`, `weight`,
`description`, plus `topic`, `covers`, `detail` as page params) and generic
semantic markdown, so any convention-following theme renders the content.

## Deploying

The deployable site is `diataxis/public/`. Deploy with any standard Hugo
workflow (`hugo deploy`, Netlify, Vercel, GitHub Pages, rsync). See
https://gohugo.io/hosting-and-deployment/.

## Exit codes

The Makefile exits with Hugo's or marimo's exit code:

| Code | Meaning |
|------|---------|
| `0`  | Success |
| non-zero | A preprocessing step (marimo export) or `hugo` itself failed. See stderr for the error message. |

## See also

- [How to Build and Serve Documentation](/howto/build-and-serve/) — the
  task-focused walkthrough for the same commands.
- [How to Install and Set Up](/howto/install-and-setup/) — installing
  `uv`, Hugo extended, Go, make, and marimo.
- [diataxis.toml Schema](../diataxis-toml-schema/) — the manifest
  these commands read.
