import marimo

app = marimo.App()


@app.cell
def _setup():
    # Setup cell: ends with a return, the displaying_stmt is the
    # import. Not a compound; no display intended; should pass.
    import marimo as mo
    return (mo,)


@app.cell
def compute(mo):
    # Pure-compute cell: last statement is an assignment, export via
    # return, no display intended. Should pass.
    payload = {"hello": "world"}
    return (payload,)


@app.cell
def show(mo, payload):
    # Displaying cell: ends with an Expr. Should pass.
    mo.md(f"payload: {payload}")


if __name__ == "__main__":
    app.run()
