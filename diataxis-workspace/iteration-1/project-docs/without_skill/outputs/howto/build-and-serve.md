# How to Build and Serve Documentation

This guide shows you how to transform your Diataxis markdown files into browsable HTML and serve them locally.

## Prerequisites

- A Diataxis documentation project with a valid `diataxis.toml`
- `pandoc` installed
- Content files written and present in the expected directories

## Steps

1. **Run the build command.**

    ```bash
    python -m scripts.build diataxis
    ```

    Replace `diataxis` with the path to your `diataxis/` directory if it is located elsewhere.

    You should see output listing each file as it is converted:

    ```
    Building from /path/to/diataxis
    Generating landing pages...
    Converting markdown to HTML...
      index.md -> index.html
      basic-operations.md -> basic-operations.html
    Build complete: /path/to/diataxis/_build
    ```

2. **Check for warnings.** The build validates that all files referenced in `diataxis.toml` exist. Missing files produce warnings:

    ```
    WARNING: Missing: howto/configure-output.md (topic: configuration, quadrant: howto)
    ```

    If you see warnings, either create the missing files or remove the entries from `diataxis.toml`.

3. **Serve the built documentation.**

    ```bash
    python -m scripts.build diataxis --serve
    ```

    This starts a static file server on port 8000. If the project has marimo exercises, it also starts the marimo server on port 2718.

4. **Open in your browser.** Navigate to `http://localhost:8000`.

5. **Stop the servers.** Press `Ctrl+C` in the terminal.

## Serve Without Rebuilding

If you have already built and just want to start the servers:

```bash
python -m scripts.build diataxis --serve-only
```

## See Also

- [Build pipeline reference](../reference/build-pipeline.md) -- full technical details
- [How to add interactive exercises](add-exercises.md) -- if your project includes marimo notebooks
