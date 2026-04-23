import marimo

app = marimo.App()


@app.cell
def _setup():
    import marimo as mo
    return (mo,)


@app.cell
def listing(mo):
    # Bug: cell ends with a `for` loop. Each iteration calls mo.md,
    # but marimo displays None — the loop is not an Expr.
    items = ["alpha", "beta", "gamma"]
    for item in items:
        mo.md(f"- {item}")


if __name__ == "__main__":
    app.run()
