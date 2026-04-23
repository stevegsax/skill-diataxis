# marimo-ast fixtures

Minimal fixtures exercising `skill/checks/check-marimo-ast.nu`.

The check parses every `exercises/*.py` through `ast.parse` and fails
if any file is syntactically invalid Python.
`check-marimo-format` is pattern-based and will pass a notebook with
a missing paren; this check is the real guard.

## The fixtures

| Fixture               | notebook        | expected status | scenario tested                     |
|-----------------------|-----------------|-----------------|-------------------------------------|
| `pass/`               | `ok.py`         | `pass`          | Syntactically valid marimo notebook. |
| `fail-syntax-error/`  | `broken.py`     | `fail`          | Missing paren — `ast.parse` rejects it. |

`run.sh` asserts each status matches the table.
