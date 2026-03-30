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
