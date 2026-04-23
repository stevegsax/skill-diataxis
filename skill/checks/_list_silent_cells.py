#!/usr/bin/env python3
"""List ``@app.cell`` functions whose last top-level statement is a
compound control-flow statement — meaning marimo will silently
display ``None`` instead of whatever the branches produce.

Usage:
    python3 _list_silent_cells.py <path>

Emits JSON:

    {"silent": [{"cell": "<function-name>",
                 "cell_line": <int>,
                 "last_line": <int>,
                 "last_type": "If" | "For" | "While" | ...},
                ...]}

Background: marimo's cell compiler (see ``marimo/_ast/compiler.py``)
extracts the cell body, strips a trailing ``return`` if present, and
treats the final statement as the cell's display expression — but
only if it is an ``ast.Expr``. Any other statement type (an
assignment, an ``if``/``else`` block, a ``for`` loop) causes the
compiler to hardcode the display to ``None``. So a cell that ends
with::

    if mode.value == "attack":
        mo.md("Roll the die.")
    else:
        mo.md("Hold the die.")

renders as nothing in the browser. The ``mo.md`` calls are inside
branches of the final ``If``; the *last* top-level statement is the
``If`` itself, and marimo throws its value away.

The fix pattern is always the same: hoist a default into a local
(underscore-prefixed so it does not leak as a cell export), mutate it
inside the branches, and reference the local as a bare expression at
the end::

    _result = None
    if mode.value == "attack":
        _result = mo.md("Roll the die.")
    else:
        _result = mo.md("Hold the die.")
    _result

This helper is intentionally narrow: it flags only compound
control-flow statements at the tail of a cell body, not arbitrary
non-``Expr`` tails. Setup cells that end with an import and a
return, and compute cells that end with an assignment and a
return, do not (and should not) produce a display — flagging them
would be noise. The compound-statement tail is the specific
regression pattern observed in practice.

Exits 1 on syntax error so the caller can surface "run
check-marimo-ast first" rather than chasing an empty report.
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

# Compound statements whose value marimo discards. ``TryStar`` is
# Python 3.11+ (``except*``); ``Match`` is 3.10+.
SILENT_TAIL_TYPES: tuple[type[ast.stmt], ...] = tuple(
    t
    for t in (
        getattr(ast, "If"),
        getattr(ast, "For"),
        getattr(ast, "AsyncFor"),
        getattr(ast, "While"),
        getattr(ast, "Try"),
        getattr(ast, "TryStar", None),
        getattr(ast, "With"),
        getattr(ast, "AsyncWith"),
        getattr(ast, "Match", None),
    )
    if t is not None
)


def is_app_cell_decorator(dec: ast.expr) -> bool:
    """True if ``dec`` is ``@app.cell`` or ``@app.cell(...)``."""
    target = dec.func if isinstance(dec, ast.Call) else dec
    return (
        isinstance(target, ast.Attribute)
        and target.attr == "cell"
        and isinstance(target.value, ast.Name)
        and target.value.id == "app"
    )


def last_displaying_stmt(body: list[ast.stmt]) -> ast.stmt | None:
    """Return the statement marimo would evaluate for display.

    Marimo strips a trailing ``return`` before compiling, so we mirror
    that here. Returns ``None`` when the body is empty (or only a
    bare ``return``) — such cells have nothing to display and should
    not be flagged.
    """
    stmts = list(body)
    if stmts and isinstance(stmts[-1], ast.Return):
        stmts = stmts[:-1]
    return stmts[-1] if stmts else None


def collect_silent(tree: ast.AST) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for node in tree.body if isinstance(tree, ast.Module) else []:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if not any(is_app_cell_decorator(d) for d in node.decorator_list):
            continue
        last = last_displaying_stmt(node.body)
        if last is None:
            continue
        if isinstance(last, SILENT_TAIL_TYPES):
            out.append(
                {
                    "cell": node.name,
                    "cell_line": node.lineno,
                    "last_line": last.lineno,
                    "last_type": type(last).__name__,
                }
            )
    return out


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: _list_silent_cells.py <path>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    try:
        tree = ast.parse(path.read_text())
    except SyntaxError as exc:
        print(f"SyntaxError: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({"silent": collect_silent(tree)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
