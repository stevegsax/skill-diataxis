#!/usr/bin/env nu
# Check that every content file's frontmatter `weight` equals
# `topic.order * 10 + quadrant_weight`, where the per-quadrant
# increments match the Explanation → Tutorials → How-to → Reference
# presentation order (explanation=1, tutorials=2, howto=3, reference=4).
#
# These weights drive Hugo's intra-section ordering: within a quadrant,
# two files with weights 12 and 22 belong to different topics (order 1
# vs order 2) and render in that order. Drift between `diataxis.toml`
# (which carries `topic.order`) and the frontmatter weight silently
# rearranges the published nav, usually in a way that confuses readers
# and that nobody notices until they hit the site.
#
# Landing pages are out of scope — they use the fixed section weights
# 10/20/30/40/50 and `check-quadrant-order` already validates them.

use mod.nu [load-structure all-file-entries make-result make-evidence]

const QUADRANT_INCREMENTS = {
    explanation: 1
    tutorials: 2
    howto: 3
    reference: 4
}

# Parse the `weight` out of a markdown file's TOML frontmatter.
# Returns null if the file has no `+++` block or no `weight` field.
def read-frontmatter-weight [path: string]: nothing -> any {
    let raw = (open $path --raw)
    let lines = ($raw | lines)
    if ($lines | length) == 0 or ($lines | first) != "+++" {
        return null
    }
    let rest = ($lines | skip 1)
    let close_idx = ($rest | enumerate | where {|p| $p.item == "+++"} | first | get -o index)
    if $close_idx == null {
        return null
    }
    let toml_text = ($rest | take $close_idx | str join "\n")
    let fm = (try { $toml_text | from toml } catch { null })
    if $fm == null {
        return null
    }
    $fm | get -o weight
}

def main [diataxis_dir: string] {
    let abs_dir = ($diataxis_dir | path expand)
    let structure = (load-structure $abs_dir)
    let entries = (all-file-entries $structure)

    if ($entries | length) == 0 {
        print (make-result "check-weight-arithmetic" "skip" [
            (make-evidence "diataxis.toml" "no content files declared")
        ] [] | to json)
        return
    }

    let topics = ($structure | get -o topics | default {})

    let problems = ($entries | each {|e|
        let topic = ($topics | get -o $e.slug)
        if $topic == null { return null }

        let order = ($topic | get -o order | default 0)
        let increment = ($QUADRANT_INCREMENTS | get -o $e.quadrant)
        if $increment == null { return null }

        let expected = ($order * 10 + $increment)

        let file_path = ($abs_dir | path join $e.file)
        if not ($file_path | path exists) { return null }

        let actual = (read-frontmatter-weight $file_path)
        if $actual == null { return null }

        if $actual != $expected {
            {file: $e.file, slug: $e.slug, quadrant: $e.quadrant, expected: $expected, actual: $actual}
        } else {
            null
        }
    } | where {|r| $r != null })

    if ($problems | length) == 0 {
        make-result "check-weight-arithmetic" "pass" [
            (make-evidence "content files" $"all content-file weights match topic.order * 10 + quadrant_weight")
        ] [] | to json
    } else {
        let evidence = ($problems | each {|p|
            make-evidence $p.file $"weight is ($p.actual), expected ($p.expected) \(topic '($p.slug)', quadrant '($p.quadrant)')"
        })
        let suggestions = ($problems | each {|p|
            $"Set weight=($p.expected) in ($p.file), or update the topic 'order' field in diataxis.toml if the topic should actually move"
        } | uniq)
        make-result "check-weight-arithmetic" "fail" $evidence $suggestions | to json
    }
}
