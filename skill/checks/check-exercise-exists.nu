#!/usr/bin/env nu
# Check that exercise paths referenced in diataxis.toml exist on disk.
use mod.nu [load-structure all-file-entries make-result make-evidence]

def main [diataxis_dir: string] {
    let structure = load-structure $diataxis_dir
    let entries = all-file-entries $structure

    let all_exercises = ($entries | where {|e| ($e.exercises | length) > 0 }
        | each {|e| $e.exercises | each {|ex| {file: $e.file, exercise: $ex}} }
        | flatten)

    if ($all_exercises | length) == 0 {
        make-result "check-exercise-exists" "skip" [
            (make-evidence "diataxis.toml" "no exercises declared")
        ] [] | to json
        return
    }

    let missing = ($all_exercises | where {|e|
        let full_path = ($diataxis_dir | path join $e.exercise)
        not ($full_path | path exists)
    })

    if ($missing | length) == 0 {
        make-result "check-exercise-exists" "pass" [
            (make-evidence "diataxis.toml" $"all ($all_exercises | length) exercise path\(s) exist")
        ] [] | to json
    } else {
        let evidence = ($missing | each {|m|
            make-evidence $m.exercise $"referenced in ($m.file) but does not exist on disk"
        })
        let suggestions = ($missing | each {|m|
            $"Create ($m.exercise) or remove it from the exercises list in ($m.file)"
        })
        make-result "check-exercise-exists" "fail" $evidence $suggestions | to json
    }
}
