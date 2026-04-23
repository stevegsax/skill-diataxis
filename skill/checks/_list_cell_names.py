#!/usr/bin/env python3
"""List top-level names assigned inside each ``@app.cell`` function.

Usage:
    python3 _list_cell_names.py <path>

Emits JSON:

    {"cells": [{"name": "<cell-function-name>",
                "line": <int>,
                "names": ["<assigned-name>", ...]},
               ...]}

Each entry in ``cells`` corresponds to one ``@app.cell``-decorated
function definition at module scope. ``names`` is the set of
identifiers the cell's body assigns at its own top level — the names
that marimo will treat as cell-global exports — excluding
underscore-prefixed names (marimo treats those as cell-private, and
the skill relies on that). Only the body's own top level is walked;
names bound inside nested functions, comprehensions, class bodies, or
conditional blocks are ignored, because marimo's cell-collision rule
fires on straight-line assignments.

Exits 1 on syntax error so the caller can surface "fix the AST check
first" rather than chasing a missing collision report.
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path


def is_app_cell_decorator(dec: ast.expr) -> bool:
    """True if ``dec`` is ``@app.cell`` or ``@app.cell(...)``."""
    target = dec.func if isinstance(dec, ast.Call) else dec
    return (
        isinstance(target, ast.Attribute)
        and target.attr == "cell"
        and isinstance(target.value, ast.Name)
        and target.value.id == "app"
    )


def names_from_target(target: ast.expr) -> list[str]:
    """Flatten tuple/list unpacking targets; skip attribute and subscript writes."""
    if isinstance(target, ast.Name):
        return [target.id]
    if isinstance(target, (ast.Tuple, ast.List)):
        out: list[str] = []
        for elt in target.elts:
            out.extend(names_from_target(elt))
        return out
    # Starred targets (e.g. ``a, *rest = seq``) — descend into the inner
    # target. Attribute and subscript writes (``foo.bar = 1``,
    # ``arr[0] = 1``) do not introduce new top-level names.
    if isinstance(target, ast.Starred):
        return names_from_target(target.value)
    return []


def cell_top_level_names(body: list[ast.stmt]) -> list[str]:
    """Names bound at the cell's module scope.

    A cell body is effectively module-level Python, so ``if``/``for``/
    ``while``/``with``/``try`` blocks *do* introduce top-level bindings.
    Only function, async-function, and class definitions open a new
    scope — names bound inside those do not leak out. We walk the
    body, descending through control flow but stopping at scope
    boundaries, and collect every assignment target that would become
    a cell-global export.
    """
    names: list[str] = []

    def visit(node: ast.AST) -> None:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                names.extend(names_from_target(target))
        elif isinstance(node, (ast.AugAssign, ast.AnnAssign)):
            names.extend(names_from_target(node.target))
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            names.append(node.name)
            return  # Do not descend — the inner body opens a new scope.
        elif isinstance(node, ast.ClassDef):
            names.append(node.name)
            return
        elif isinstance(node, ast.Import):
            for alias in node.names:
                names.append(alias.asname or alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                names.append(alias.asname or alias.name)
        elif isinstance(node, ast.For):
            names.extend(names_from_target(node.target))
        elif isinstance(node, ast.AsyncFor):
            names.extend(names_from_target(node.target))
        elif isinstance(node, ast.With):
            for item in node.items:
                if item.optional_vars is not None:
                    names.extend(names_from_target(item.optional_vars))
        elif isinstance(node, ast.AsyncWith):
            for item in node.items:
                if item.optional_vars is not None:
                    names.extend(names_from_target(item.optional_vars))
        elif isinstance(node, ast.ExceptHandler):
            if node.name:
                names.append(node.name)

        # Descend into children that can contain nested statements —
        # but not into function/class scopes (handled with `return`
        # above). Comprehensions have their own scope in Python 3, so
        # ast.iter_child_nodes skipping ast.expr subtrees is close
        # enough: we only care about statement-level bindings.
        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.stmt) or isinstance(child, ast.ExceptHandler):
                visit(child)

    for stmt in body:
        visit(stmt)
    # Drop underscore-prefixed names: marimo treats them as cell-local.
    # Preserve first-occurrence order but deduplicate within the cell
    # (a name assigned twice in the same cell is still one export).
    seen: set[str] = set()
    deduped: list[str] = []
    for n in names:
        if n.startswith("_") or n in seen:
            continue
        seen.add(n)
        deduped.append(n)
    return deduped


def collect_cells(tree: ast.AST) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for node in tree.body if isinstance(tree, ast.Module) else []:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if not any(is_app_cell_decorator(d) for d in node.decorator_list):
            continue
        out.append(
            {
                "name": node.name,
                "line": node.lineno,
                "names": cell_top_level_names(node.body),
            }
        )
    return out


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: _list_cell_names.py <path>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    try:
        tree = ast.parse(path.read_text())
    except SyntaxError as exc:
        print(f"SyntaxError: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({"cells": collect_cells(tree)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
