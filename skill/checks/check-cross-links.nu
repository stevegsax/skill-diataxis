#!/usr/bin/env nu
# Check that content files cross-reference sibling quadrant documents.
use mod.nu [make-result make-evidence content-files]

def main [diataxis_dir: string] {
    let quads = [tutorials howto reference explanation]

    let all_files = ($quads | each {|q|
        content-files ($diataxis_dir | path join $q) | each {|f|
            {quadrant: $q, path: $f, rel: ($q + "/" + ($f | path basename))}
        }
    } | flatten)

    if ($all_files | length) == 0 {
        make-result "check-cross-links" "skip" [
            (make-evidence "diataxis.toml" "no content files found")
        ] [] | to json
        return
    }

    let without_links = ($all_files | each {|entry|
        let content = (open $entry.path --raw)
        let other_quads = ($quads | where {|q| $q != $entry.quadrant})
        let has_cross_link = ($other_quads | where {|oq| $content | str contains $oq} | length) > 0
        if not $has_cross_link {
            $entry.rel
        }
    } | where {|r| $r != null})

    let total = ($all_files | length)
    let linked = $total - ($without_links | length)

    if ($without_links | length) == 0 {
        make-result "check-cross-links" "pass" [
            (make-evidence "diataxis.toml" $"all ($total) file\(s) contain cross-references to other quadrants")
        ] [] | to json
    } else {
        let evidence = ($without_links | each {|f|
            make-evidence $f "does not reference any other quadrant directory"
        })
        let suggestions = ($without_links | each {|f|
            $"Add cross-references to sibling quadrant documents in ($f)"
        })
        make-result "check-cross-links" "fail" $evidence $suggestions | to json
    }
}
