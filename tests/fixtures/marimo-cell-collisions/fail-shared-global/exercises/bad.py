import marimo

app = marimo.App()


@app.cell
def _setup():
    import marimo as mo
    return (mo,)


@app.cell
def ui(mo):
    mode = mo.ui.radio(options=["a", "b"], value="a")
    # `result` is assigned here and also in the next cell — collision.
    result = 1
    return (mode, result)


@app.cell
def compute(mo, mode):
    # Nested in a conditional, but still a cell-global binding.
    if mode.value == "a":
        result = "hit"
    else:
        result = "miss"
    return (result,)


if __name__ == "__main__":
    app.run()
