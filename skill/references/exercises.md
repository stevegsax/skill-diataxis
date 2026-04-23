# Writing Marimo Exercises

When `diataxis.toml` lists an `exercises` entry on a tutorial, the
skill must create the corresponding marimo notebook under
`diataxis/exercises/<stem>.py`. This is not an optional follow-up —
it is part of the tutorial's generation task. A tutorial that lists
exercises and ships without the notebooks is incomplete in exactly
the way a tutorial that lists steps and then ships without any of
them is incomplete.

Every notebook the project ships shows up in two places in the
published site: inline on the tutorial page that owns it (via the
`## Exercises` section appended during content generation) and on
the Examples landing page (`examples/_index.md`, `weight = 50`), which
becomes the fifth top-level nav section whenever the project has any
`exercises/*.py`. The Examples page is a project-wide index — grouped
by topic, with a one-line description per entry — so a reader can
discover a notebook without knowing which tutorial owns it. Keep it
regenerated in the same change whenever you add, remove, or rename an
`exercises` entry anywhere in `diataxis.toml`. When the project has
no notebooks, the Examples section does not exist, and that is
correct — see `SKILL.md` "Examples (optional fifth section)" for the
authoring rule and `references/quadrants.md` "Examples (optional)"
for what the page must and must not do.

The check suite enforces this two ways: `check-exercise-exists` fails
if the `.py` file is missing, and `check-exercise-content` fails if
the file is a placeholder stub (only one cell, `# TODO` markers, or a
bare `pass` cell body). Both failures have a deterministic remediation:
write a real exercise. This reference describes what "real" means and
gives a template to start from.

## What a real exercise is

A marimo exercise runs in the reader's browser (via Pyodide) and lets
them interact with the concept the tutorial just taught. The medium is
the message: a block of static text that says "try this" is not an
exercise — an exercise is something the reader actually *does*. That
means every exercise has at least:

- **A setup cell** that imports `marimo as mo` and anything else the
  exercise needs. Kept separate so the UI cells below read cleanly.
- **One or more UI cells** that present inputs the reader can
  manipulate: `mo.ui.slider`, `mo.ui.text`, `mo.ui.dropdown`,
  `mo.ui.text_area`, `mo.ui.number`, `mo.ui.button`, etc.
- **One or more response cells** that *read* those inputs and render
  something — a computed result, a rendered TOML snippet, a rendered
  diagram, an encouragement message when the input matches a target,
  a next-step prompt when it does not.

Two cells is the functional minimum (input + response). Below that,
marimo's reactive graph has nothing to react to and the exercise
cannot be interactive; it is just a static page with extra machinery.

## The shape of a cell

Marimo cells look like functions but are not — they are reactive nodes
in a DAG. A cell's parameters name the cells whose returned values it
depends on, and its `return` tuple names the values other cells can
depend on. A few practical consequences:

- **Every `mo.ui.*` binding must be returned** so response cells can
  read `.value` off it.
- **Top-level names are module-scoped across all cells**, so no two
  cells can assign to the same name. Rename local variables per cell
  (`step_1_result`, `step_2_result` rather than a shared `result`).
- **Imports live in the setup cell** and are returned from it so other
  cells can parameterize on them. Marimo will not lift module-level
  imports into every cell's scope automatically.

## Template for a minimal exercise

Use this as a starting point. It is shaped to pass the checks on its
own and is easy to extend — add a UI cell + response cell for each
concept the exercise covers.

```python
import marimo

app = marimo.App()


@app.cell
def _setup():
    import marimo as mo
    return (mo,)


@app.cell
def intro(mo):
    mo.md("""
    ## <Exercise title>

    <One or two sentences orienting the reader. What will they try?
    What should they pay attention to?>
    """)


@app.cell
def step_1(mo):
    # UI cell: present an input the reader can manipulate.
    value = mo.ui.slider(1, 10, label="<what does this control?>")
    mo.md(f"**<prompt for the reader>**\n\n{value}")
    return (value,)


@app.cell
def step_1_result(mo, value):
    # Response cell: read the input and render something that changes
    # as the reader plays with it.
    if value.value < 5:
        mo.md(f"You chose **{value.value}**. Try a larger value.")
    else:
        mo.md(f"You chose **{value.value}**. Notice how <observation>.")


if __name__ == "__main__":
    app.run()
```

This is ~30 lines and 4 cells. It passes every check, is meaningful
on its own, and scales straightforwardly by adding more step pairs.

## Tailoring the exercise to the tutorial

The tutorial's `diataxis.toml` entry is the brief. Read `covers`,
`detail`, and `guidance` before writing the exercise — they describe
what the tutorial teaches, and the exercise should let the reader
practice exactly that. Two heuristics:

- **One concept per exercise.** If the tutorial covers three distinct
  skills, write one exercise per skill (three files) rather than one
  omnibus exercise. Each entry in the `exercises` list in
  `diataxis.toml` is a separate file, so the grain is already
  encoded — honor it.
- **Mirror the tutorial's examples.** If the tutorial walks through
  building a `diataxis.toml`, the exercise lets the reader build one
  interactively. If the tutorial demos a `slice()` call on strings,
  the exercise lets them type a string and a slice and see the result.
  The exercise is not a quiz on the tutorial — it is a playground
  for the thing the tutorial just taught.

## Pyodide constraint

Exercises run in the browser via Pyodide (through `marimo export
html-wasm`), so every imported package must be Pyodide-compatible.
The standard library is available. `numpy`, `pandas`, `matplotlib`,
`scipy`, and many other scientific Python packages are available.
Anything that wraps C extensions without a WASM build (`lxml`,
`psycopg2`, most ML frameworks with GPU bindings) is not. If unsure,
prefer the standard library or pure-Python packages.

## What to avoid

- **Single-cell exercises.** The check fails and nothing interactive
  works. If the concept genuinely needs only one cell, it is not an
  exercise — it is a code example, and belongs inline in the tutorial
  as a fenced code block.
- **Placeholder cells.** `pass`, `# TODO`, `# placeholder`, or a cell
  that only imports are all stubs. The check fails. Write real
  content.
- **Exercises disconnected from the tutorial.** If a reader finishes
  the tutorial and the exercise tests something the tutorial did not
  teach, the exercise is ornament. Pull its substance from `covers`.
- **Overreaching on UI.** One or two `mo.ui.*` widgets per concept is
  plenty. A dashboard-grade exercise with ten controls obscures what
  the reader is supposed to learn.
