#!/usr/bin/env python3
"""Find ``<widget>.value == <key>`` comparisons that look like they are
testing the key of a dict-options widget instead of its mapped value.

Usage:
    python3 _list_value_miscompares.py <path>

Emits JSON:

    {"miscompares": [{"var": "mode",
                      "line": 42,
                      "literal": "Attack Roll",
                      "keys": ["Attack Roll", "Saving Throw"],
                      "values": ["attack", "save"]},
                     ...]}

Context: ``mo.ui.radio`` and ``mo.ui.dropdown`` constructed with a
dict ``options={label: mapped}`` take a key for the default
``value=`` kwarg, but ``.value`` read at runtime returns the
*mapped* value. An author who writes ``widget.value == "Attack
Roll"`` (the label) has a comparison that is always ``False`` — a
silent bug: the widget looks unresponsive in the browser with no
error to debug. This helper flags the narrow case where it can be
statically certain (dict literal passed to ``options=``, literal
string compared against ``.value``, literal is a key but not a
value).

Intentionally conservative. Non-literal ``options=``, dicts whose
keys are also values (equivalent to passing a list), comparisons
against non-literal operands, and comparisons using ``in`` or
``match`` are all skipped — a false positive on this check is worse
than a miss, because authors start ignoring noisy static checks.

Exits 1 on syntax error so the caller can surface "run
check-marimo-ast first" rather than chasing an empty report.
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

DICT_OPTION_WIDGETS = {"radio", "dropdown"}


def widget_call(call: ast.Call) -> str | None:
    """Return 'radio' or 'dropdown' if ``call`` is ``mo.ui.<widget>(...)``."""
    func = call.func
    if not isinstance(func, ast.Attribute):
        return None
    if func.attr not in DICT_OPTION_WIDGETS:
        return None
    mid = func.value
    if not (isinstance(mid, ast.Attribute) and mid.attr == "ui"):
        return None
    root = mid.value
    if not (isinstance(root, ast.Name) and root.id == "mo"):
        return None
    return func.attr


def dict_options_kwarg(call: ast.Call) -> ast.Dict | None:
    """Return the ``options=`` argument if it is a literal dict, else None."""
    for kw in call.keywords:
        if kw.arg != "options":
            continue
        if isinstance(kw.value, ast.Dict):
            return kw.value
        return None
    return None


def literal_str_items(node: ast.Dict) -> tuple[list[str], list[str]] | None:
    """Flatten a dict literal into (keys, values) of constant strings.

    Returns None when any key or value is non-literal — that disables
    the check for this widget rather than guessing.
    """
    keys: list[str] = []
    values: list[str] = []
    for k, v in zip(node.keys, node.values):
        if not (isinstance(k, ast.Constant) and isinstance(k.value, str)):
            return None
        if not isinstance(v, ast.Constant):
            return None
        keys.append(k.value)
        # str() on constants lets us compare against `.value == 1` or
        # `.value == "attack"` uniformly later.
        values.append(v.value if isinstance(v.value, str) else repr(v.value))
    return keys, values


def collect_widgets(tree: ast.AST) -> dict[str, dict[str, list[str]]]:
    """Map widget variable name → {'keys': [...], 'values': [...]}."""
    widgets: dict[str, dict[str, list[str]]] = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        if not isinstance(node.value, ast.Call):
            continue
        if widget_call(node.value) is None:
            continue
        opts = dict_options_kwarg(node.value)
        if opts is None:
            continue
        items = literal_str_items(opts)
        if items is None:
            continue
        keys, values = items
        # Keys that are ALSO values (e.g. ``{"a": "a", "b": "b"}``) make
        # the comparison unambiguous — skip those widgets.
        if set(keys) <= set(values):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name):
                widgets[target.id] = {"keys": keys, "values": values}
    return widgets


def compare_pair(cmp: ast.Compare) -> tuple[ast.expr, ast.expr] | None:
    """Return (widget_value_access, literal_operand) if the comparison
    matches ``<x>.value == <literal>`` or ``<literal> == <x>.value``."""
    if len(cmp.ops) != 1 or not isinstance(cmp.ops[0], (ast.Eq, ast.NotEq)):
        return None
    if len(cmp.comparators) != 1:
        return None
    left, right = cmp.left, cmp.comparators[0]
    for a, b in ((left, right), (right, left)):
        if (
            isinstance(a, ast.Attribute)
            and a.attr == "value"
            and isinstance(a.value, ast.Name)
            and isinstance(b, ast.Constant)
        ):
            return a, b
    return None


def collect_miscompares(
    tree: ast.AST, widgets: dict[str, dict[str, list[str]]]
) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Compare):
            continue
        pair = compare_pair(node)
        if pair is None:
            continue
        attr, literal = pair
        assert isinstance(attr, ast.Attribute)
        assert isinstance(attr.value, ast.Name)
        var = attr.value.id
        if var not in widgets:
            continue
        lit_value = literal.value if isinstance(literal, ast.Constant) else None
        lit_repr = lit_value if isinstance(lit_value, str) else repr(lit_value)
        info = widgets[var]
        if lit_repr in info["keys"] and lit_repr not in info["values"]:
            out.append(
                {
                    "var": var,
                    "line": node.lineno,
                    "literal": lit_repr,
                    "keys": info["keys"],
                    "values": info["values"],
                }
            )
    return out


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: _list_value_miscompares.py <path>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    try:
        tree = ast.parse(path.read_text())
    except SyntaxError as exc:
        print(f"SyntaxError: {exc}", file=sys.stderr)
        return 1
    widgets = collect_widgets(tree)
    print(json.dumps({"miscompares": collect_miscompares(tree, widgets)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
