import marimo

app = marimo.App()


@app.cell
def _setup():
    import marimo as mo
    import numpy as np
    import pandas as pd
    return mo, np, pd


@app.cell
def intro(mo):
    mo.md("Uses only Pyodide-compatible packages.")


if __name__ == "__main__":
    app.run()
