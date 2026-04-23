#!/usr/bin/env nu
# Check that every marimo notebook under `exercises/` is referenced
# from at least one tutorial's `exercises` list in `diataxis.toml`.
#
# The inverse direction — notebooks listed in `diataxis.toml` but
# missing on disk — is covered by `check-exercise-exists`. This check
# catches the opposite drift: a `.py` file is present but no tutorial
# knows about it, which means the Examples landing page won't include
# it, `make exercises` will still export a WASM bundle for it, and the
# reader has no way to discover it.
#
# The `exercises` field accepts two forms — a bare path string or a
# table `{ file = "…", title = "…", height = N }` — so we normalize
# both to file paths before comparing.

use mod.nu [load-structure all-file-entries make-result make-evidence]

# Normalize one `exercises` list entry to a file path. Returns null
# when the entry has no recognizable `file` key.
def entry-to-path [entry: any]: nothing -> any {
    let ty = ($entry | describe)
    if $ty == "string" {
        $entry
    } else if ($ty | str starts-with "record") {
        $entry | get -o file
    } else {
        null
    }
}

def main [diataxis_dir: string] {
    let abs_dir = ($diataxis_dir | path expand)
    let exercises_dir = ($abs_dir | path join "exercises")

    if not ($exercises_dir | path exists) {
        print (make-result "check-orphan-exercises" "skip" [
            (make-evidence "exercises/" "directory does not exist")
        ] [] | to json)
        return
    }

    let on_disk = (glob ($exercises_dir | path join "*.py")
        | each {|p| $p | path relative-to $abs_dir })

    if ($on_disk | length) == 0 {
        print (make-result "check-orphan-exercises" "skip" [
            (make-evidence "exercises/" "no .py files under exercises/")
        ] [] | to json)
        return
    }

    let structure = (load-structure $abs_dir)
    let entries = (all-file-entries $structure)
    let referenced = ($entries
        | each {|e|
            $e.exercises | each {|raw| entry-to-path $raw }
        }
        | flatten
        | where {|p| $p != null })

    let orphans = ($on_disk | where {|p| not ($p in $referenced) })

    if ($orphans | length) == 0 {
        make-result "check-orphan-exercises" "pass" [
            (make-evidence "exercises/" $"all ($on_disk | length) notebook\(s) are referenced from a tutorial in diataxis.toml")
        ] [] | to json
    } else {
        let evidence = ($orphans | each {|p|
            make-evidence $p "no tutorial's `exercises` list references this file"
        })
        let suggestions = ($orphans | each {|p|
            $"Either add '($p)' to a tutorial's exercises list in diataxis.toml or delete the file"
        })
        make-result "check-orphan-exercises" "fail" $evidence $suggestions | to json
    }
}
