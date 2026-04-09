#!/usr/bin/env nu
# Check that diataxis.toml exists and is valid TOML.
use mod.nu [make-result make-evidence]

def main [diataxis_dir: string] {
    let toml_path = ($diataxis_dir | path join "diataxis.toml")

    if not ($toml_path | path exists) {
        make-result "check-toml-valid" "fail" [
            (make-evidence "diataxis.toml" "file does not exist")
        ] [
            "Create a diataxis.toml file in the diataxis directory"
        ] | to json
        return
    }

    try {
        open $toml_path | ignore
        make-result "check-toml-valid" "pass" [
            (make-evidence "diataxis.toml" "valid TOML syntax")
        ] [] | to json
    } catch {|err|
        make-result "check-toml-valid" "fail" [
            (make-evidence "diataxis.toml" $"invalid TOML: ($err.msg)")
        ] [
            "Fix TOML syntax errors in diataxis.toml"
        ] | to json
    }
}
