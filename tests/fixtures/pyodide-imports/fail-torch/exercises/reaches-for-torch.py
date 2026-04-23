import marimo

app = marimo.App()


@app.cell
def _setup():
    import marimo as mo
    import torch
    return mo, torch


@app.cell
def intro(mo, torch):
    mo.md(f"Torch {torch.__version__} in the browser? Not in this Pyodide build.")


if __name__ == "__main__":
    app.run()
