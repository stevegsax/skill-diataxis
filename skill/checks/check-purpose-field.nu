#!/usr/bin/env nu
# Check that the [project] section has a purpose field.
use mod.nu [load-structure make-result make-evidence]

def main [diataxis_dir: string] {
    let structure = load-structure $diataxis_dir
    let purpose = ($structure | get -o project | default {} | get -o purpose | default "")

    if ($purpose | str trim | is-empty) {
        make-result "check-purpose-field" "fail" [
            (make-evidence "diataxis.toml" "project.purpose field is missing or empty")
        ] [
            "Add a purpose field to [project] in diataxis.toml explaining why the project exists and what problems it solves"
        ] | to json
    } else {
        make-result "check-purpose-field" "pass" [
            (make-evidence "diataxis.toml" "project.purpose field is present")
        ] [] | to json
    }
}
