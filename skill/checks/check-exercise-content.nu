#!/usr/bin/env nu
# Check that exercise marimo notebooks have real content, not placeholder
# stubs. The existence check (`check-exercise-exists`) and the format
# check (`check-marimo-format`) pass for any file that imports marimo
# and defines at least one cell — even a stub like:
#
#   import marimo
#   app = marimo.App()
#
#   @app.cell
#   def _():
#       # TODO: write this exercise
#       pass
#
# That is exactly the pattern the skill has been producing when an
# exercise is listed in `diataxis.toml` but the generation step skips
# actually writing it. Real exercises have multiple cells because a
# single-cell notebook cannot be interactive (one cell for the UI
# element, another to react to its value), and they do not carry
# TODO/placeholder markers.
#
# This check flags any referenced-and-existing marimo exercise that:
#   1. Has fewer than 2 `@app.cell` definitions (one cell cannot drive
#      an interactive exercise — you need at least a widget cell and a
#      response cell), or
#   2. Contains explicit placeholder markers (`# TODO`, `# placeholder`,
#      `# not implemented`, or a cell body that is a bare `pass`).
#
# Remediation is deterministic: generate real exercise content per the
# tutorial's `covers`, `detail`, and `guidance` fields in `diataxis.toml`.
# See `references/exercises.md` for the shape of a real exercise.

use mod.nu [load-structure all-file-entries make-result make-evidence]

def main [diataxis_dir: string] {
    let structure = load-structure $diataxis_dir
    let entries = all-file-entries $structure

    let all_exercises = ($entries | where {|e| ($e.exercises | length) > 0 }
        | each {|e| $e.exercises }
        | flatten
        | uniq)

    if ($all_exercises | length) == 0 {
        print (make-result "check-exercise-content" "skip" [
            (make-evidence "diataxis.toml" "no exercises declared")
        ] [] | to json)
        return
    }

    let existing = ($all_exercises | where {|ex|
        ($diataxis_dir | path join $ex | path exists)
    })

    if ($existing | length) == 0 {
        print (make-result "check-exercise-content" "skip" [
            (make-evidence "diataxis.toml" "no exercise files exist on disk (see check-exercise-exists)")
        ] [] | to json)
        return
    }

    let problems = ($existing | each {|ex|
        let full_path = ($diataxis_dir | path join $ex)
        let content = (open $full_path --raw)
        let cell_count = ($content | find --regex '^\s*@app\.cell' | length)

        let has_todo_marker = (
            ($content | find --regex '(?i)#\s*(TODO|placeholder|not\s+implemented)' | length) > 0
        )
        let has_bare_pass_cell = (
            ($content | find --regex '(?m)^\s*pass\s*(#.*)?$' | length) > 0
        )

        if $cell_count < 2 {
            {
                file: $ex
                detail: $"only ($cell_count) `@app.cell` definition\(s); a real interactive exercise needs at least 2 cells \(a UI cell and a response cell)"
            }
        } else if $has_todo_marker {
            {
                file: $ex
                detail: "contains a placeholder marker (`# TODO`, `# placeholder`, or `# not implemented`); replace with real exercise content"
            }
        } else if $has_bare_pass_cell {
            {
                file: $ex
                detail: "contains a cell whose body is a bare `pass` statement; replace the stub with real exercise content"
            }
        }
    } | where {|p| $p != null})

    if ($problems | length) == 0 {
        make-result "check-exercise-content" "pass" [
            (make-evidence "diataxis.toml" $"all ($existing | length) exercise file\(s) have real content \(>= 2 cells, no placeholder markers)")
        ] [] | to json
    } else {
        let evidence = ($problems | each {|p|
            make-evidence $p.file $p.detail
        })
        let suggestions = ($problems | each {|p|
            $"Generate real content for ($p.file) per the tutorial's `covers`, `detail`, and `guidance` in diataxis.toml; see references/exercises.md for the shape of a real exercise"
        })
        make-result "check-exercise-content" "fail" $evidence $suggestions | to json
    }
}
