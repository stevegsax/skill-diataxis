# How to Build and Serve Documentation

This guide shows you how to transform your Diataxis markdown files into HTML and view them in a browser.

## Prerequisites

- A `diataxis/` directory with `diataxis.toml` and content files
- `pandoc` installed and available on your PATH
- Python 3.13+
- If your project includes exercises: `marimo` and `uvicorn` installed

## How to Build

1. From your project root, run:

    ```bash
    python -m scripts.build diataxis/
    ```

2. The build script validates the structure, generates landing pages, converts markdown to HTML, and outputs everything to `diataxis/_build/`.
3. Check stderr for any warnings about missing files.

## How to Serve Locally

1. Build and start both servers in one command:

    ```bash
    python -m scripts.build diataxis/ --serve
    ```

2. Open `http://localhost:8000` in your browser.
3. If your project has exercises, the marimo server runs on port `2718`. Exercise iframes load automatically.
4. Press `Ctrl+C` to stop both servers.

To serve without rebuilding (if you have already built):

```bash
python -m scripts.build diataxis/ --serve-only
```

## How to Rebuild After Changes

1. Edit your content files or update `diataxis.toml`.
2. Run the build command again:

    ```bash
    python -m scripts.build diataxis/
    ```

3. The `_build/` directory is deleted and recreated on each build. Landing pages are regenerated from the current structure.
4. Refresh your browser to see the changes.

## Further Reading

- See the [Build Pipeline Reference](../reference/build-pipeline.md) for technical details on each pipeline step
- See the [Structure Document Schema](../reference/structure-document-schema.md) for the manifest format consumed by the build
