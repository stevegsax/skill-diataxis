import marimo

app = marimo.App()


@app.cell
def _setup():
    import marimo as mo
    return (mo,)


@app.cell
def intro(mo):
    mo.md("""
    ## Valid Notebook

    Syntax parses cleanly.
    """)


if __name__ == "__main__":
    app.run()
