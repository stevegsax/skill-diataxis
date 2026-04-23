import marimo

app = marimo.App()


@app.cell
def _setup():
    import marimo as mo
    return (mo,)


@app.cell
def ui(mo):
    # Sequence options — no dict, so keys and values are the same
    # strings and `.value == "one"` is unambiguous.
    pick = mo.ui.radio(options=["one", "two"], value="one")
    mo.md(f"Pick: {pick}")
    return (pick,)


@app.cell
def respond(mo, pick):
    if pick.value == "one":
        mo.md("picked one")
    else:
        mo.md("picked two")


if __name__ == "__main__":
    app.run()
