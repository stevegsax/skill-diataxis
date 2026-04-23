# marimo-cell-display fixtures

Test cases for `check-marimo-cell-display`, which flags any
`@app.cell` function whose last top-level statement is a compound
control-flow block (If/For/While/Try/With/Match/AsyncFor/AsyncWith/
TryStar). Marimo's compiler hardcodes the display to `None` in
that case — branches that call `mo.md(...)` produce no visible
output, silently.

| Fixture                        | Expected | What it tests |
|--------------------------------|----------|---------------|
| `pass/`                        | pass     | Cell uses the hoisted-default pattern (`_result = None; if …; _result`). |
| `pass-no-display-intended/`    | pass     | Setup and pure-compute cells end with import/assign — no display expected, not flagged. |
| `fail-if-else/`                | fail     | Cell body ends with an If/Else; each branch calls `mo.md` but marimo displays None. |
| `fail-for-loop/`               | fail     | Cell body ends with a For loop iterating `mo.md` calls — same silent-None behavior. |

Run with `bash run.sh`.
