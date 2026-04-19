+++
title = "How to Build and Serve Documentation"
weight = 42
description = "The build pipeline, CLI commands, and local development workflow"
topic = "build-pipeline"
covers = ["Building the site with `make build`", "Running live reload with `make serve`", "Exporting marimo notebooks with `make exercises`", "Cleaning generated output with `make clean`", "Switching the Hugo theme by editing hugo.toml", "Where the rendered output lives and how to deploy it"]
detail = "Each task gets a numbered procedure. Show the expected terminal output."
+++
All commands run from inside the `diataxis/` directory (or use `make -C diataxis <target>` from elsewhere).

## Build the site

```bash
cd diataxis
make build
```

`make build` exports any marimo notebooks to self-contained WASM bundles
under `static/exercises/`, then runs `hugo` into `public/`. Rendered output
lives at `diataxis/public/`.

## Serve locally with live reload

```bash
make serve
```

This exports exercises, then runs `hugo server`. Hugo prints the URL it
bound to (usually `http://localhost:1313`).

Edits to authored markdown, `diataxis.toml`, `hugo.toml`, and anything
under `layouts/` are picked up automatically, because Hugo's content mounts
point straight at the authored files — there is no intermediate staging
step.

Press Ctrl+C to stop the server.

## Export exercises only

```bash
make exercises
```

Runs the marimo exports without invoking `hugo`. Useful when iterating on a
notebook and you don't want a full rebuild. After this, `hugo` or
`hugo server` (run directly) will see the updated WASM bundles.

## Clean generated output

```bash
make clean
```

Removes `public/` (Hugo output) and `resources/` (Hugo cache). Leaves
`static/exercises/` alone because re-exporting WASM bundles is slow.

## Switch the Hugo theme

The scaffolded `hugo.toml` wires in the Hextra theme via a Hugo module. To
use a different theme, edit `hugo.toml` and replace the `module.imports`
entry with any Hugo module theme from https://themes.gohugo.io/. Then
refresh the modules and rebuild:

```bash
hugo mod get -u
make build
```

Because the authored markdown uses standard Hugo frontmatter and generic
semantic markdown, any convention-following theme renders the content.

## Run `hugo` directly

The Makefile is convenience. After `make exercises`, you can run `hugo` or
`hugo server` yourself:

```bash
make exercises
hugo server
```

## Deploy

There is no custom publish command. The deployable site is
`diataxis/public/`. Deploy it with any standard Hugo workflow:
`hugo deploy` (S3, Azure, GCS), Netlify, Vercel, Cloudflare Pages, GitHub
Pages, or `rsync`. See https://gohugo.io/hosting-and-deployment/ for the
full catalog.

For the detailed reference, see
[Build Commands Reference](../reference/cli-reference/).
