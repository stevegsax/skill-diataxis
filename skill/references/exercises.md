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
the Exercises landing page (`examples/_index.md`, `title = "Exercises"`,
`weight = 50`), which becomes the fifth top-level nav section whenever
the project has any `exercises/*.py`. The landing page is a project-wide
index — grouped by topic, with a one-line description per entry — so a
reader can discover a notebook without knowing which tutorial owns it.
Keep it regenerated in the same change whenever you add, remove, or
rename an `exercises` entry anywhere in `diataxis.toml`. When the project
has no notebooks, the Exercises section does not exist, and that is
correct — see `SKILL.md` "Exercises (optional fifth section)" for the
authoring rule and `references/quadrants.md` "Exercises (optional)"
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

- **Every `mo.ui.*` binding a later cell reads must be returned** so
  response cells can read `.value` off it.
- **Top-level names are module-scoped across all cells.** Marimo
  enforces one definition per global name across the whole notebook,
  and a collision surfaces in the browser as "This cell wasn't run
  because it redefines variables from other cells." It does *not*
  show up during `marimo export html-wasm`, which is why the check
  suite includes an AST pass — see "The cell-collision trap" below.
- **Prefix cell-local names with `_`** (e.g. `_tmp`, `_row`,
  `_needed`) for any value that only the current cell uses. Marimo
  treats underscore-prefixed names as cell-private, so they do not
  collide across cells and, importantly, **they must not appear in
  the cell's `return (...)` tuple** — a cell cannot export a
  private name. The only names that belong in `return (...)` are
  cross-cell dependencies: the UI widget a response cell reads, a
  DataFrame another cell filters, the `mo` module itself.
- **Imports live in the setup cell** and are returned from it so other
  cells can parameterize on them. Marimo will not lift module-level
  imports into every cell's scope automatically.

### The silent-display trap

Marimo's cell compiler (see `marimo/_ast/compiler.py`) treats a
cell body's *last* top-level statement as the display expression —
but only if it is an `ast.Expr` (a bare expression statement). If
the last statement is anything else — an `if`/`else`, a `for`
loop, an `assign`, a `with` block — the compiler replaces the
display with a hardcoded `None`. A cell that ends like this::

    if mode.value == "attack":
        mo.md("Roll the die.")
    else:
        mo.md("Hold the die.")

renders as *nothing* in the browser. The `mo.md` calls are inside
branches of the final `If`; the last *top-level* statement is the
`If` itself, and marimo throws its value away. `marimo export
html-wasm` emits the bundle without complaint — the bug only
surfaces when a reader opens the page.

The fix pattern is always the same: hoist a default into an
underscore-prefixed local (so it does not become a cell export),
assign to it inside each branch, and end the cell with a bare
expression referencing the local.

    _result = None
    if mode.value == "attack":
        _result = mo.md("Roll the die.")
    else:
        _result = mo.md("Hold the die.")
    _result

A single-branch version works the same way::

    _result = mo.md("Fill in the fields above.")
    if pick.value and submit.value:
        _result = mo.md(f"Got {pick.value}.")
    _result

For simple binary cases, a ternary inside one `mo.md` call is often
cleaner and avoids the pattern entirely::

    mo.md(f"{pick.value} is {'small' if pick.value < 5 else 'large'}.")

The `check-marimo-cell-display` check flags any cell whose last
top-level statement is a compound control-flow block. It is
intentionally narrow — setup cells that end with an import and a
return, and pure-compute cells that end with an assignment and a
return, are *supposed* to have no display and are not flagged.

### The cell-collision trap

Names like `table`, `result`, `needed`, `total`, `r`, `df`, `fig`, and
`out` are the usual offenders — an author writes a cell that computes
`result` and returns it, and the next cell also computes `result` for
its own purposes, and nothing complains at generation time. The
`marimo export html-wasm` step is a pure code emitter: it serializes
the cells, it does not evaluate the DAG. The collision only trips when
a browser loads the exported bundle and marimo's runtime actually
wires the graph.

The rule that prevents this: **before a name goes into a cell's
`return (...)`, ask whether another cell actually consumes it.** If
nothing else reads it, rename it with a leading underscore and remove
it from the return tuple. Keeping `return (needed,)` "just in case"
is precisely how collisions are born. A short-lived local should stay
local.

The `check-marimo-cell-collisions` check runs on every score pass and
flags any non-underscore name assigned at the top level of more than
one `@app.cell` body. A failure names the offending cells and
variable; the fix is always the same shape (underscore-prefix the
cell-local occurrences and drop them from `return`).

## Marimo API drift and how to stay ahead of it

Marimo is pre-1.0 and the `mo.ui.*` constructors break compatibility
between minor versions. Two consequences for this skill:

1. **Check `https://docs.marimo.io/api/` before using any `mo.ui.*`
   widget the notebook does not already demonstrate.** Training-data
   snapshots of marimo APIs drift out of date fast. One WebFetch of
   the widget's page (e.g. `/api/inputs/slider/`,
   `/api/inputs/dropdown/`) is cheap and catches parameter renames
   before they become a broken exported bundle. Do this *every*
   time you author a new exercise, not just the first one — the
   drift catalog below gets longer with each marimo release.
2. **The WASM export silently accepts stale parameter names** when
   they are passed by position, and silently accepts nonexistent
   kwargs on some widgets up to the point the browser tries to
   render them. In both cases the error only surfaces after the
   user clicks into the exercise. Treat the published site, not
   the export step, as ground truth for whether the API call is
   current.

Known drift the skill has been bitten by — audit new exercises for
each one:

- **`mo.ui.slider`**: the maximum bound is `stop=`, not `end=`. Use
  `mo.ui.slider(start=1, stop=10, label=…)` or the positional form
  `mo.ui.slider(1, 10, label=…)`. `end=` raises at render time.
- **`mo.ui.radio` / `mo.ui.dropdown` with dict `options=`**: the
  `value=` default passed at construction is a **key** (the label
  the reader sees), but `.value` read at runtime returns the
  **mapped value** (the dict value), not the key. So a constructor
  like `mo.ui.dropdown(options={"Attack Roll": "attack",
  "Saving Throw": "save"}, value="Attack Roll")` must be paired
  with response-cell comparisons that test the mapped value —
  `if mode.value == "attack":`, not `== "Attack Roll"`. If the
  author wants to compare against the key, use `.selected_key`
  instead of `.value`.

When fixing a constructor kwarg, audit every `<widget>.value ==`
comparison downstream. Stale equality checks silently evaluate to
`False` and the exercise appears to "do nothing" in the browser —
there is no error, just an unresponsive widget.

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
    # Use start=/stop= on sliders — end= is a stale alias that raises
    # in the browser. Positional (1, 10) is also correct.
    step_1_input = mo.ui.slider(start=1, stop=10, label="<what does this control?>")
    mo.md(f"**<prompt for the reader>**\n\n{step_1_input}")
    return (step_1_input,)


@app.cell
def step_1_result(mo, step_1_input):
    # Response cell: read the input and render something that changes
    # as the reader plays with it. Two rules at work here:
    #   1. `_chosen` is cell-local (underscore prefix) so it does
    #      not collide with any other cell's `_chosen` and does not
    #      appear in `return (...)`.
    #   2. The cell ends with a bare `_result` expression. If it
    #      ended with the `if`/`else` instead, marimo would display
    #      None no matter which branch ran (see "The silent-display
    #      trap" above).
    _chosen = step_1_input.value
    _result = None
    if _chosen < 5:
        _result = mo.md(f"You chose **{_chosen}**. Try a larger value.")
    else:
        _result = mo.md(f"You chose **{_chosen}**. Notice how <observation>.")
    _result


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
- **Stale kwargs on `mo.ui.*` widgets.** `end=` on `slider`,
  `on_value=` where the current API is `on_change=`, anything else
  the training snapshot remembers from an old marimo version. The
  cell-by-cell template above is known to work on the installed
  runtime; deviations should be checked against
  `https://docs.marimo.io/api/` first.
- **Exporting cell-locals.** Anything in a cell's `return (...)`
  tuple that no other cell parameterizes on is either unused or —
  worse — silently colliding with a same-name export from another
  cell. Rename it with a leading underscore and drop it from the
  return.
- **Ending a cell with a compound statement.** Any cell whose last
  top-level statement is an `if`/`else`, `for`, `while`, `with`,
  `try`, or `match` displays `None`, regardless of what the
  branches produce. The branches may call `mo.md(...)` a dozen
  times and it changes nothing — marimo's compiler only displays
  the *last* top-level `Expr`. Use the `_result = None; if …;
  _result` pattern from "The silent-display trap" above.
