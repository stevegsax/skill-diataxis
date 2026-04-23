import marimo

app = marimo.App()


@app.cell
def _setup():
    import marimo as mo
    return (mo,)


@app.cell
def intro(mo):
    mo.md("""
    ## First Exercise

    Move the slider to watch the value update.
    """)


@app.cell
def step_1(mo):
    value = mo.ui.slider(1, 10, label="Pick a number")
    mo.md(f"**Pick a number:**\n\n{value}")
    return (value,)


@app.cell
def step_1_result(mo, value):
    mo.md(f"You chose **{value.value}**.")


if __name__ == "__main__":
    app.run()
