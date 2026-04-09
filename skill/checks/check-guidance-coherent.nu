#!/usr/bin/env nu
# Check that guidance fields read as coherent prose, not appended REVISION FEEDBACK blocks.
use mod.nu [load-structure all-file-entries make-result make-evidence]

def main [diataxis_dir: string] {
    let structure = load-structure $diataxis_dir
    let entries = all-file-entries $structure

    let markers = ["REVISION FEEDBACK:" "REVISION:" "FEEDBACK:" "USER FEEDBACK:"]

    let problems = ($entries | each {|e|
        let topic = ($structure | get topics | get $e.slug)
        let entry = ($topic | get $e.quadrant)
        let guidance = ($entry | get -o guidance | default "")
        let found_marker = ($markers | where {|m| $guidance | str contains $m } | first)
        if $found_marker != null {
            {file: $e.file, marker: $found_marker}
        }
    } | where {|r| $r != null})

    if ($problems | length) == 0 {
        make-result "check-guidance-coherent" "pass" [
            (make-evidence "diataxis.toml" "no REVISION FEEDBACK blocks found in guidance fields")
        ] [] | to json
    } else {
        let evidence = ($problems | each {|p|
            make-evidence "diataxis.toml" $"guidance for ($p.file) contains '($p.marker)' block"
        })
        let suggestions = ($problems | each {|p|
            $"Integrate revision feedback for ($p.file) into the guidance text as coherent prose, removing the '($p.marker)' label"
        })
        make-result "check-guidance-coherent" "fail" $evidence $suggestions | to json
    }
}
