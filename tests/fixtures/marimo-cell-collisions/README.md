# marimo-cell-collisions fixtures

Test cases for `check-marimo-cell-collisions`, which flags non-underscore
names assigned at the top level of more than one `@app.cell` in the same
notebook. Marimo's reactive runtime rejects these at browser-load time
with "This cell wasn't run because it redefines variables from other
cells," but `marimo export html-wasm` passes cleanly.

| Fixture                   | Expected | What it tests |
|---------------------------|----------|---------------|
| `pass/`                   | pass     | Distinct cell-globals per cell; underscore-prefixed locals. |
| `pass-underscore-private/`| pass     | Same spelling in multiple cells, but underscore-prefixed — marimo treats those as cell-local, so no collision. |
| `fail-shared-global/`     | fail     | `result` is bound in one cell directly and in another cell inside an `if` branch — still a cell-global, still a collision. |

Run with `bash run.sh`.
