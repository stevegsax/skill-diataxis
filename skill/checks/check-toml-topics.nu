#!/usr/bin/env nu
# Check that diataxis.toml defines at least one topic.
use mod.nu [load-structure make-result make-evidence]

def main [diataxis_dir: string] {
    let structure = load-structure $diataxis_dir
    let topics = ($structure | get -o topics | default {})
    let count = ($topics | columns | length)

    if $count == 0 {
        make-result "check-toml-topics" "fail" [
            (make-evidence "diataxis.toml" "no topics defined")
        ] [
            "Add at least one [topics.<slug>] section to diataxis.toml"
        ] | to json
    } else {
        make-result "check-toml-topics" "pass" [
            (make-evidence "diataxis.toml" $"($count) topic\(s) defined")
        ] [] | to json
    }
}
