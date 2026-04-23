#!/usr/bin/env nu
# Check that no two content files in the same quadrant declare the
# same frontmatter `weight`. Hugo orders pages within a section by
# weight ascending; when two pages tie, the order falls back to file
# name, which is non-obvious and silently rearranges the nav when
# titles change or files are renamed.
#
# Landing-page weights are fixed (10/20/30/40/50) and handled by
# `check-quadrant-order` — this check only looks at content files.

use mod.nu [make-result make-evidence content-files]

const QUADRANTS = [tutorials howto reference explanation examples]

def read-frontmatter-weight [path: string]: nothing -> any {
    let raw = (open $path --raw)
    let lines = ($raw | lines)
    if ($lines | length) == 0 or ($lines | first) != "+++" {
        return null
    }
    let rest = ($lines | skip 1)
    let close_idx = ($rest | enumerate | where {|p| $p.item == "+++"} | first | get -o index)
    if $close_idx == null { return null }
    let toml_text = ($rest | take $close_idx | str join "\n")
    let fm = (try { $toml_text | from toml } catch { null })
    if $fm == null { return null }
    $fm | get -o weight
}

def main [diataxis_dir: string] {
    let abs_dir = ($diataxis_dir | path expand)

    let per_quadrant = ($QUADRANTS | each {|q|
        let qdir = ($abs_dir | path join $q)
        let files = (content-files $qdir)
        let weighted = ($files | each {|f|
            let weight = (read-frontmatter-weight $f)
            if $weight != null {
                {quadrant: $q, file: ($f | path relative-to $abs_dir), weight: $weight}
            }
        } | where {|r| $r != null })
        $weighted
    } | flatten)

    # Group by (quadrant, weight); any bucket of size > 1 is a clash.
    # `group-by` takes a cell path, so we precompute a string key.
    let keyed = ($per_quadrant | each {|r|
        $r | insert key $"($r.quadrant):($r.weight)"
    })
    let buckets = ($keyed | group-by key --to-table)
    let clashes = ($buckets | where {|g| ($g.items | length) > 1 })

    if ($clashes | length) == 0 {
        make-result "check-duplicate-weights" "pass" [
            (make-evidence "content files" $"no two content files in the same quadrant share a weight across ($per_quadrant | length) file\(s)")
        ] [] | to json
    } else {
        let evidence = ($clashes | each {|g|
            let files_csv = ($g.items | get file | str join ", ")
            let sample = ($g.items | first)
            make-evidence $files_csv $"two or more content files in ($sample.quadrant)/ declare weight=($sample.weight) — Hugo's nav order between them falls back to file name"
        })
        let suggestions = ($clashes | each {|g|
            let sample = ($g.items | first)
            let quadrant = $sample.quadrant
            "Give each file in " + $quadrant + "/ a distinct weight, or move the duplicated file to a different topic. The canonical formula is topic.order * 10 + quadrant_weight."
        } | uniq)
        make-result "check-duplicate-weights" "fail" $evidence $suggestions | to json
    }
}
