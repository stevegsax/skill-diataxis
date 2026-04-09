#!/usr/bin/env nu
# Check that all 4 quadrant directories have at least one content file.
use mod.nu [make-result make-evidence content-files]

def main [diataxis_dir: string] {
    let quads = [tutorials howto reference explanation]
    let missing = ($quads | where {|q|
        let files = (content-files ($diataxis_dir | path join $q))
        ($files | length) == 0
    })

    if ($missing | length) == 0 {
        make-result "check-quadrant-files" "pass" [
            (make-evidence "diataxis.toml" "all 4 quadrant directories have content files")
        ] [] | to json
    } else {
        let evidence = ($missing | each {|q|
            make-evidence $"($q)/" $"no content files in ($q) directory"
        })
        let suggestions = ($missing | each {|q|
            $"Add content files to the ($q) directory"
        })
        make-result "check-quadrant-files" "fail" $evidence $suggestions | to json
    }
}
