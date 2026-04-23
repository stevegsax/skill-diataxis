import marimo

app = marimo.App()


@app.cell
def _setup():
    import marimo as mo
    return (mo,)


@app.cell
def ui(mo):
    mode = mo.ui.dropdown(
        options={"Attack Roll": "attack", "Saving Throw": "save"},
        value="Attack Roll",
    )
    mo.md(f"Choose: {mode}")
    return (mode,)


@app.cell
def respond(mo, mode):
    # Bug: comparing against the KEY (label), but .value returns the
    # mapped value ("attack"/"save"). This comparison is always False.
    if mode.value == "Attack Roll":
        mo.md("Roll the die.")
    else:
        mo.md("Hold the die.")


if __name__ == "__main__":
    app.run()
