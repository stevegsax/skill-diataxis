import marimo

app = marimo.App()


@app.cell
def _setup():
    import marimo as mo
    return (mo,)


@app.cell
def intro(mo):
    # Missing closing paren — ast.parse will reject this file.
    mo.md("A syntax error sits on the next line."
    return None


if __name__ == "__main__":
    app.run()
