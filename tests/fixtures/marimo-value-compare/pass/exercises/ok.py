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
    # Compares against the mapped value — correct.
    if mode.value == "attack":
        mo.md("Roll the die.")
    else:
        mo.md("Hold the die.")


if __name__ == "__main__":
    app.run()
