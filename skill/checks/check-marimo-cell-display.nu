#!/usr/bin/env nu
# Check that no `@app.cell` function ends with a compound control-flow
# statement — such cells display None in the browser, regardless of
# what their branches produce.
#
# Marimo's cell compiler (see `marimo/_ast/compiler.py`) treats a
# cell body's *last* top-level statement as the display expression,
# but only if it is an `ast.Expr`. Any other statement type causes
# the compiler to hardcode the display to `None`. A cell that ends
# with:
#
#     if mode.value == "attack":
#         mo.md("Roll the die.")
#     else:
#         mo.md("Hold the die.")
#
# renders as nothing — the `mo.md` calls live inside branches, and
# the *last* top-level statement is the If itself. This is the
# specific pattern the skill has been bitten by. The fix is to
# hoist a default, mutate it inside the branches, and end with a
# bare expression referencing the local:
#
#     _result = None
#     if mode.value == "attack":
#         _result = mo.md("Roll the die.")
#     else:
#         _result = mo.md("Hold the die.")
#     _result
#
# The helper is intentionally narrow. Cells that end with an
# assignment or an import (setup cells, pure compute cells) are
# *supposed* to have no display, and flagging them would produce
# noise that trains authors to ignore the check.

use mod.nu [make-result make-evidence]

def main [diataxis_dir: string] {
    let abs_dir = ($diataxis_dir | path expand)
    let exercises_dir = ($abs_dir | path join "exercises")
    let helper = ($env.FILE_PWD | path join "_list_silent_cells.py")

    if not ($exercises_dir | path exists) {
        print (make-result "check-marimo-cell-display" "skip" [
            (make-evidence "exercises/" "directory does not exist")
        ] [] | to json)
        return
    }

    let notebooks = (glob ($exercises_dir | path join "*.py"))

    if ($notebooks | length) == 0 {
        print (make-result "check-marimo-cell-display" "skip" [
            (make-evidence "exercises/" "no .py files under exercises/")
        ] [] | to json)
        return
    }

    let findings = ($notebooks | each {|nb|
        let rel = ($nb | path relative-to $abs_dir)
        let result = (^python3 $helper $nb | complete)
        if $result.exit_code != 0 {
            null
        } else {
            let parsed = (try { $result.stdout | from json } catch { null })
            if $parsed == null {
                null
            } else {
                let silent = ($parsed | get -o silent | default [])
                if ($silent | length) == 0 {
                    null
                } else {
                    {file: $rel, silent: $silent}
                }
            }
        }
    } | where {|r| $r != null })

    if ($findings | length) == 0 {
        make-result "check-marimo-cell-display" "pass" [
            (make-evidence "exercises/" $"all ($notebooks | length) notebook\(s) end each cell with an expression that marimo can display")
        ] [] | to json
    } else {
        let evidence = ($findings | each {|f|
            $f.silent | each {|s|
                (make-evidence $f.file --line $s.last_line
                    $"cell `($s.cell)` ends with a `($s.last_type)` — marimo displays None instead of the branch results")
            }
        } | flatten)
        let suggestions = ($findings | each {|f|
            $f.silent | each {|s|
                $"In ($f.file), hoist a default `_result = None` before the `($s.last_type)` in cell `($s.cell)`, assign to `_result` inside each branch, and end the cell with a bare `_result` expression"
            }
        } | flatten | uniq)
        make-result "check-marimo-cell-display" "fail" $evidence $suggestions | to json
    }
}
