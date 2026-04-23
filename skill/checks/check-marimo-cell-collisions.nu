#!/usr/bin/env nu
# Check that no two `@app.cell` functions in a marimo notebook define
# the same top-level name at module scope.
#
# Marimo's reactive runtime enforces one definition per global name
# across the whole notebook. A cell that redefines a name already
# defined by an earlier cell silently refuses to run in the browser
# ("This cell wasn't run because it redefines variables from other
# cells"). The error does NOT surface during `marimo export
# html-wasm` — it is a runtime-only check — so a notebook that
# passes export cleanly can still be dead on arrival when a reader
# opens it.
#
# The helper `_list_cell_names.py` walks the AST, collects names
# assigned at each cell's own top level (excluding underscore-
# prefixed names, which marimo treats as cell-local), and emits them
# cell-by-cell. This check groups them by name and fails on any
# non-underscore name that appears in more than one cell.
#
# The fix pattern is always the same: rename the cell-local
# occurrences with a leading underscore and drop them from the
# cell's `return (...)` tuple. See `references/exercises.md` for the
# rule and template.

use mod.nu [make-result make-evidence]

def main [diataxis_dir: string] {
    let abs_dir = ($diataxis_dir | path expand)
    let exercises_dir = ($abs_dir | path join "exercises")
    let helper = ($env.FILE_PWD | path join "_list_cell_names.py")

    if not ($exercises_dir | path exists) {
        print (make-result "check-marimo-cell-collisions" "skip" [
            (make-evidence "exercises/" "directory does not exist")
        ] [] | to json)
        return
    }

    let notebooks = (glob ($exercises_dir | path join "*.py"))

    if ($notebooks | length) == 0 {
        print (make-result "check-marimo-cell-collisions" "skip" [
            (make-evidence "exercises/" "no .py files under exercises/")
        ] [] | to json)
        return
    }

    # For each notebook, build a list of (name, cell, line) triples, then
    # group by name within the notebook and keep only names that appear
    # in more than one cell. Cross-notebook collisions are fine — marimo
    # scopes are per-notebook — so we never merge across files.
    let per_file_findings = ($notebooks | each {|nb|
        let rel = ($nb | path relative-to $abs_dir)
        let result = (^python3 $helper $nb | complete)
        if $result.exit_code != 0 {
            # Syntax errors are caught by check-marimo-ast; skip
            # here to avoid double-reporting.
            null
        } else {
            let parsed = (try { $result.stdout | from json } catch { null })
            if $parsed == null {
                null
            } else {
                let cells = ($parsed | get -o cells | default [])
                let triples = ($cells | each {|c|
                    $c.names | each {|n| {name: $n, cell: $c.name, line: $c.line} }
                } | flatten)
                let collisions = ($triples | group-by name
                    | transpose name rows
                    | where {|g| ($g.rows | length) > 1 })
                if ($collisions | length) == 0 {
                    null
                } else {
                    {file: $rel, collisions: $collisions}
                }
            }
        }
    } | where {|r| $r != null })

    if ($per_file_findings | length) == 0 {
        make-result "check-marimo-cell-collisions" "pass" [
            (make-evidence "exercises/" $"all ($notebooks | length) notebook\(s) free of cross-cell name collisions")
        ] [] | to json
    } else {
        let evidence = ($per_file_findings | each {|f|
            $f.collisions | each {|g|
                let cells = ($g.rows | each {|r| $"($r.cell):($r.line)" } | str join ", ")
                make-evidence $f.file $"name `($g.name)` is defined in multiple cells: ($cells)"
            }
        } | flatten)
        let suggestions = ($per_file_findings | each {|f|
            $f.collisions | each {|g|
                $"In ($f.file), rename cell-local occurrences of `($g.name)` to `_($g.name)` and remove them from the cell's return tuple; keep the one occurrence that another cell actually consumes"
            }
        } | flatten | uniq)
        make-result "check-marimo-cell-collisions" "fail" $evidence $suggestions | to json
    }
}
