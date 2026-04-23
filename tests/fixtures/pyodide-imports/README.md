# pyodide-imports fixtures

Minimal fixtures exercising `skill/checks/check-pyodide-imports.nu`.

The check walks every `exercises/*.py` via `_list_imports.py` (a
small `ast.walk` helper) and flags any top-level package name that
appears in a short deny list of libraries known not to work in
Pyodide. The deny list is intentionally narrow — it contains only
packages that demonstrably cannot run in the browser (native-only C
or GPU dependencies) — so a fail from this check is a real fail,
not a style preference.

## The fixtures

| Fixture                | imports                     | expected status | scenario tested                                      |
|------------------------|-----------------------------|-----------------|------------------------------------------------------|
| `pass/`                | `marimo`, `numpy`, `pandas` | `pass`          | All imports are Pyodide-compatible.                  |
| `fail-torch/`          | `marimo`, `torch`           | `fail`          | `torch` ships as native CUDA code; not in Pyodide.   |
| `fail-psycopg2/`       | `marimo`, `psycopg2`        | `fail`          | `psycopg2` wraps libpq; no WASM build available.     |

`run.sh` asserts each status matches the table.
