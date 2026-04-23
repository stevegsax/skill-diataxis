import marimo

app = marimo.App()


@app.cell
def _setup():
    import marimo as mo
    from psycopg2 import connect
    return mo, connect


@app.cell
def intro(mo):
    mo.md("Database notebook — does not run in Pyodide, no native libpq.")


if __name__ == "__main__":
    app.run()
