# Diataxis Documentation — self-docs example

This directory is the worked example for `skill-diataxis`: it documents the
skill *with* the skill. It is also a plain Hugo site you can build and serve.

## Build

```bash
make build           # export exercises + hugo  → public/
make serve           # export exercises + hugo server (live reload)
make exercises       # export marimo notebooks only
make clean           # remove public/ and resources/
```

Requires Hugo extended, Go 1.21+, `make`, and `uv` (for `marimo`). See
`howto/install-and-setup.md` for setup details.

## What's in here

- `diataxis.toml` — editorial source of truth (topic structure, coverage,
  guidance per file).
- `index.md`, `tutorials/`, `howto/`, `reference/`, `explanation/` —
  authored markdown with Hugo frontmatter. Generated and revised by the
  skill; do not hand-edit.
- `exercises/` — marimo notebook sources for interactive exercises.
- `hugo.toml`, `go.mod`, `go.sum`, `Makefile` — the Hugo publishing layer.
  User-owned; the skill never rewrites these.
- `static/exercises/`, `public/`, `resources/` — generated output
  (gitignored). `static/exercises/` holds the WASM bundles; `public/` is
  the rendered site to deploy.

## Output-only documentation

The authored content here is a **human-facing artifact derived from the
skill's source and instructions**. It is not authoritative for how the
skill behaves — the code in `skill/` is. If the rendered docs disagree
with the code, the code is right and the docs need regenerating.

Do not use files in this directory as input for design decisions, code
generation, build processes, or CI pipelines. For the authoritative
project documentation, see the repository root.
