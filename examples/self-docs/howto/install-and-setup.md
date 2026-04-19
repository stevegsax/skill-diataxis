+++
title = "How to Install and Set Up"
weight = 12
description = "Installation, first project, and the basic workflow"
topic = "getting-started"
covers = ["Installing uv", "Installing Hugo extended", "Installing Go (required for Hugo module resolution)", "Installing make", "Running the marimo Python dependency via uv"]
detail = "Concise install steps for macOS and Linux. No explanation of what the tools do."
+++
## Install uv

macOS / Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Verify:

```bash
uv --version
```

## Install Hugo extended

Use the **extended** distribution — Hextra and most docs themes assume it.

macOS:

```bash
brew install hugo
```

Linux (Debian/Ubuntu):

```bash
sudo snap install hugo
```

Or download a release from https://github.com/gohugoio/hugo/releases.

Verify:

```bash
hugo version
```

The output must include `extended`. For example:

```
hugo v0.160.1+extended ...
```

## Install Go

Hugo resolves themes through Go modules, so a Go toolchain (1.21+) must be on
`PATH`.

macOS:

```bash
brew install go
```

Linux (Debian/Ubuntu):

```bash
sudo apt install golang
```

Or download a release from https://go.dev/dl/.

Verify:

```bash
go version
```

## Install make

`make` is preinstalled on macOS (via Xcode Command Line Tools) and on most
Linux distributions. If it is missing:

macOS:

```bash
xcode-select --install
```

Linux (Debian/Ubuntu):

```bash
sudo apt install make
```

Verify:

```bash
make --version
```

## Install marimo

`marimo` is a Python dependency, pulled in by `uv sync`:

```bash
cd /path/to/skill-diataxis
uv sync
```

It is exposed as `uv run marimo` — the Makefile invokes it that way, so no
additional PATH setup is required.

For background on why these tools are needed, see
[Why Structure First](../explanation/why-structure-first/).
