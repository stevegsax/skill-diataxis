import marimo

app = marimo.App()


@app.cell
def _setup():
    import marimo as mo
    return (mo,)


@app.cell
def a(mo):
    # Cell-local name — underscore-prefixed, not returned.
    _tmp = 1
    mo.md(f"a: {_tmp}")


@app.cell
def b(mo):
    # Same spelling, also cell-local. No collision because both are
    # underscore-prefixed, which marimo treats as cell-private.
    _tmp = 2
    mo.md(f"b: {_tmp}")


if __name__ == "__main__":
    app.run()
