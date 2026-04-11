#!/usr/bin/env nu
# Check that exercise files are valid marimo notebooks.
use mod.nu [load-structure all-file-entries make-result make-evidence]

def main [diataxis_dir: string] {
    let structure = load-structure $diataxis_dir
    let entries = all-file-entries $structure

    let all_exercises = ($entries | where {|e| ($e.exercises | length) > 0 }
        | each {|e| $e.exercises }
        | flatten
        | uniq)

    if ($all_exercises | length) == 0 {
        print (make-result "check-marimo-format" "skip" [
            (make-evidence "diataxis.toml" "no exercises declared")
        ] [] | to json)
        return
    }

    let existing = ($all_exercises | where {|ex|
        ($diataxis_dir | path join $ex | path exists)
    })

    if ($existing | length) == 0 {
        print (make-result "check-marimo-format" "skip" [
            (make-evidence "diataxis.toml" "no exercise files exist on disk")
        ] [] | to json)
        return
    }

    let invalid = ($existing | each {|ex|
        let full_path = ($diataxis_dir | path join $ex)
        let content = (open $full_path --raw)
        let has_marimo = ($content | str contains "marimo") or ($content | str contains "@app.cell")
        if not $has_marimo {
            $ex
        }
    } | where {|r| $r != null})

    if ($invalid | length) == 0 {
        make-result "check-marimo-format" "pass" [
            (make-evidence "diataxis.toml" $"all ($existing | length) exercise file\(s) are valid marimo notebooks")
        ] [] | to json
    } else {
        let evidence = ($invalid | each {|f|
            make-evidence $f "file does not contain marimo markers (marimo.App or @app.cell)"
        })
        let suggestions = ($invalid | each {|f|
            $"Convert ($f) to a marimo notebook or remove it from exercises in diataxis.toml"
        })
        make-result "check-marimo-format" "fail" $evidence $suggestions | to json
    }
}
