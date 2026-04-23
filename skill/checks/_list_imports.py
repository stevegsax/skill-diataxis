#!/usr/bin/env python3
"""List the top-level package names imported by a Python file.

Usage:
    python3 _list_imports.py <path>

Emits JSON: {"imports": ["numpy", "pandas", "marimo"]}. Imports that
live inside function bodies or conditional blocks are included, which
is the behavior we want for a notebook check — any import we can
reach is one that will actually get executed at Pyodide load time.

Exits 1 on syntax error so the caller can surface "the AST check
should run first" rather than getting an empty import list.
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path


def top_level(dotted: str) -> str:
    return dotted.split(".")[0] if dotted else ""


def gather(tree: ast.AST) -> list[str]:
    seen: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = top_level(alias.name)
                if name:
                    seen.add(name)
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0 and node.module:
                name = top_level(node.module)
                if name:
                    seen.add(name)
    return sorted(seen)


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: _list_imports.py <path>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    try:
        tree = ast.parse(path.read_text())
    except SyntaxError as exc:
        print(f"SyntaxError: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({"imports": gather(tree)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
