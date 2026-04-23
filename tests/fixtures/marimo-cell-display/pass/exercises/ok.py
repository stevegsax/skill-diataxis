import marimo

app = marimo.App()


@app.cell
def _setup():
    import marimo as mo
    return (mo,)


@app.cell
def step_1(mo):
    step_1_input = mo.ui.slider(start=1, stop=10, label="Pick a number")
    mo.md(f"**Choose**: {step_1_input}")
    return (step_1_input,)


@app.cell
def step_1_result(mo, step_1_input):
    _chosen = step_1_input.value
    _result = None
    if _chosen < 5:
        _result = mo.md(f"{_chosen} is small.")
    else:
        _result = mo.md(f"{_chosen} is large.")
    _result


if __name__ == "__main__":
    app.run()
