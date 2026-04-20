# How to Install and Set Up

## Install uv

macOS / Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Verify:

```bash
uv --version
```

## Install pandoc

macOS:

```bash
brew install pandoc
```

Linux (Debian/Ubuntu):

```bash
sudo apt install pandoc
```

Verify:

```bash
pandoc --version
```

## Install mmdc (mermaid CLI)

mmdc renders mermaid diagram blocks to SVG during the build. Optional — if
not installed, mermaid blocks are left as code blocks in the output.

macOS:

```bash
brew install mermaid-cli
```

Linux (npm):

```bash
npm install -g @mermaid-js/mermaid-cli
```

Verify:

```bash
mmdc --version
```

## Install the diataxis CLI

From the skill-diataxis project directory:

```bash
uv sync
```

Verify:

```bash
uv run diataxis --help
```

You should see:

```
usage: diataxis [-h] [-d DIR] {build,serve,serve-only} ...
```

For background on why these tools are needed, see
[Why Structure First](../explanation/why-structure-first.html).
