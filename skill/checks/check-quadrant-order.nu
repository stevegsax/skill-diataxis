#!/usr/bin/env nu
# Check that each quadrant has an _index.md section landing page with:
#   1. TOML frontmatter carrying the canonical weight that pins the
#      presentation order (explanation=10, tutorials=20, howto=30,
#      reference=40)
#   2. A `title` in frontmatter
#   3. At least one paragraph of introductory prose before the first list
#   4. A bulleted list of links to sibling content files in the same
#      directory
#
# The weights are the enforcement mechanism: Hugo orders top-level sections
# by the weight of their `_index.md`, so these four numbers determine the
# published order. Drift here produces a published site whose ordering does
# not match the skill's documented conventions.
use mod.nu [make-result make-evidence content-files]

# Canonical weight for each quadrant, in presentation order.
const QUADRANT_WEIGHTS = [
    {quadrant: explanation, weight: 10}
    {quadrant: tutorials,   weight: 20}
    {quadrant: howto,       weight: 30}
    {quadrant: reference,   weight: 40}
]

# Parse TOML frontmatter from a markdown file. Returns a record with the
# parsed frontmatter and the body text after the closing `+++`. Returns null
# frontmatter if the file has no `+++`-delimited block.
def parse-frontmatter [path: string]: nothing -> record {
    let lines = (open $path --raw | lines)
    if ($lines | length) == 0 or ($lines | first) != "+++" {
        return {frontmatter: null, body: (open $path --raw)}
    }
    let rest = ($lines | skip 1)
    let close_idx = ($rest | enumerate | where {|p| $p.item == "+++"} | first | get -o index)
    if $close_idx == null {
        return {frontmatter: null, body: (open $path --raw)}
    }
    let toml_text = ($rest | take $close_idx | str join "\n")
    let body = ($rest | skip ($close_idx + 1) | str join "\n")
    let fm = (try { $toml_text | from toml } catch { null })
    {frontmatter: $fm, body: $body}
}

# Return true if the body contains a markdown link-list (at least one line
# starting with `- [`). The landing page contract requires a bulleted list
# of links to content files.
def has-link-list [body: string]: nothing -> bool {
    ($body | lines | any {|l| ($l | str trim) starts-with "- ["})
}

# Return true if the body has at least one non-empty prose line before the
# first list item. Frontmatter is already stripped before this runs.
def has-intro-paragraph [body: string]: nothing -> bool {
    let trimmed_lines = ($body | lines | each {|l| $l | str trim})
    let before_list = ($trimmed_lines | take while {|l| not ($l starts-with "- ")})
    ($before_list | any {|l| $l != "" and not ($l starts-with "#")})
}

def main [diataxis_dir: string] {
    let issues = ($QUADRANT_WEIGHTS | each {|entry|
        let index_path = ($diataxis_dir | path join $entry.quadrant | path join "_index.md")
        let rel = ($entry.quadrant + "/_index.md")

        if not ($index_path | path exists) {
            [{file: $rel, detail: $"missing _index.md for quadrant '($entry.quadrant)'", suggestion: $"Create ($rel) with weight=($entry.weight), an introduction, and a bulleted list of links to content files"}]
        } else {
            let parsed = (parse-frontmatter $index_path)
            mut problems = []

            if $parsed.frontmatter == null {
                $problems = ($problems | append {file: $rel, detail: "file has no TOML frontmatter block", suggestion: $"Add a +++ frontmatter block with title and weight=($entry.weight)"})
            } else {
                let fm = $parsed.frontmatter
                let title = ($fm | get -o title)
                let weight = ($fm | get -o weight)

                if $title == null or ($title | describe) != "string" or ($title | str trim) == "" {
                    $problems = ($problems | append {file: $rel, detail: "frontmatter missing non-empty 'title'", suggestion: "Add a title field to the frontmatter"})
                }
                if $weight == null {
                    $problems = ($problems | append {file: $rel, detail: "frontmatter missing 'weight'", suggestion: $"Add weight=($entry.weight) to the frontmatter"})
                } else if $weight != $entry.weight {
                    $problems = ($problems | append {file: $rel, detail: $"weight is ($weight), expected ($entry.weight)", suggestion: $"Set weight=($entry.weight) to place '($entry.quadrant)' in the canonical presentation order"})
                }
            }

            let body = $parsed.body
            if not (has-intro-paragraph $body) {
                $problems = ($problems | append {file: $rel, detail: "no introductory paragraph before the link list", suggestion: "Add a short introduction (2-4 sentences) explaining the quadrant before the list of links"})
            }

            let content = (content-files ($diataxis_dir | path join $entry.quadrant))
            if ($content | length) > 0 and not (has-link-list $body) {
                $problems = ($problems | append {file: $rel, detail: "content files exist but _index.md has no bulleted list of links", suggestion: $"Add a bulleted list linking to every content file in ($entry.quadrant)/"})
            }

            $problems
        }
    } | flatten)

    # Also verify the relative ordering is strictly increasing if all four
    # weights are present. If any _index.md is missing or has a bad weight,
    # the issues above already flag it, so we only emit an ordering issue
    # when every file parses cleanly but the weights are out of order.
    let parsed_weights = ($QUADRANT_WEIGHTS | each {|entry|
        let index_path = ($diataxis_dir | path join $entry.quadrant | path join "_index.md")
        if ($index_path | path exists) {
            let fm = (parse-frontmatter $index_path).frontmatter
            if $fm != null {
                {quadrant: $entry.quadrant, weight: ($fm | get -o weight)}
            }
        }
    } | where {|r| $r != null and $r.weight != null})

    let order_issues = if ($parsed_weights | length) == 4 {
        let expected_order = ($QUADRANT_WEIGHTS | get quadrant)
        let actual_order = ($parsed_weights | sort-by weight | get quadrant)
        if $actual_order != $expected_order {
            [{file: "explanation/_index.md, tutorials/_index.md, howto/_index.md, reference/_index.md", detail: $"section weights sort to ($actual_order | str join ' -> '), expected ($expected_order | str join ' -> ')", suggestion: "Adjust weights so the sections render as Explanation -> Tutorials -> How-to -> Reference"}]
        } else { [] }
    } else { [] }

    let all_issues = ($issues | append $order_issues)

    if ($all_issues | length) == 0 {
        make-result "check-quadrant-order" "pass" [
            (make-evidence "diataxis.toml" "all four quadrants have _index.md landing pages with canonical weights (explanation=10, tutorials=20, howto=30, reference=40), an introduction, and a link list")
        ] [] | to json
    } else {
        let evidence = ($all_issues | each {|p| make-evidence $p.file $p.detail})
        let suggestions = ($all_issues | each {|p| $p.suggestion})
        make-result "check-quadrant-order" "fail" $evidence $suggestions | to json
    }
}
