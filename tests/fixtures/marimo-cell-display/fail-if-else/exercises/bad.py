import marimo

app = marimo.App()


@app.cell
def _setup():
    import marimo as mo
    return (mo,)


@app.cell
def ui(mo):
    pick = mo.ui.slider(start=1, stop=10, label="Pick a number")
    mo.md(f"**Choose**: {pick}")
    return (pick,)


@app.cell
def respond(mo, pick):
    # Bug: cell ends with an If. Each branch calls mo.md, but
    # marimo's compiler displays None because the *last* top-level
    # statement is the If, not an Expr.
    if pick.value < 5:
        mo.md(f"{pick.value} is small.")
    else:
        mo.md(f"{pick.value} is large.")


if __name__ == "__main__":
    app.run()
