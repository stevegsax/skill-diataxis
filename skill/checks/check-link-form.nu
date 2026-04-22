#!/usr/bin/env nu
# Check that relative Markdown links in content files use the correct
# form for Hugo pretty URLs.
#
# Content files (non-_index.md, non-index.md) are served at
# /<quadrant>/<stem>/ — two URL segments deep. RFC 3986 resolves
# relative links against the trailing-slash URL, so one `../` only
# exits the page's pretty-URL directory, not the quadrant directory.
# Two authoring patterns look right in source-tree terms but resolve
# to the wrong URL:
#
#   1. `](../<same-quadrant>/foo/)` inside a file in that quadrant.
#      Resolves to /<quadrant>/<quadrant>/foo/. Drop the quadrant name
#      and use `](../foo/)` for a same-quadrant sibling.
#
#   2. `](../<other-quadrant>/foo/)` inside a content file.
#      Resolves to /<quadrant>/<other>/foo/ (404). Cross-quadrant links
#      need two `../` or an absolute path:
#      `](../../<other>/foo/)` or `](/<other>/foo/)`.
#
# The rules differ for `_index.md` (served at /<quadrant>/, one level
# shallower) and the root `index.md` (served at /) — this check skips
# those files and only lints content files.
#
# Fenced code blocks and inline code are stripped before scanning so
# illustrative Markdown examples don't trip the lint.

use mod.nu [make-result make-evidence]

const QUADRANTS = [tutorials howto reference explanation]

# Tag each line with whether it lies inside a fenced code block. The
# fence line itself is tagged "in code" so the opening/closing ``` is
# not scanned for links.
def tag-fenced-lines [content: string]: nothing -> list<record> {
    $content
    | lines
    | enumerate
    | reduce --fold {out: [], in_code: false} {|pair, acc|
        let trimmed = ($pair.item | str trim)
        let is_fence = ($trimmed | str starts-with '```')
        let in_code_now = ($acc.in_code or $is_fence)
        let next_in_code = if $is_fence { not $acc.in_code } else { $acc.in_code }
        let entry = {
            line: ($pair.index + 1)
            text: $pair.item
            in_code: $in_code_now
        }
        {out: ($acc.out | append $entry), in_code: $next_in_code}
    }
    | get out
}

def main [diataxis_dir: string] {
    let abs_dir = ($diataxis_dir | path expand)

    let problems = ($QUADRANTS | each {|q|
        let qdir = ($abs_dir | path join $q)
        let files = if ($qdir | path exists) {
            glob ($qdir | path join "*.md") | where {|f|
                let name = ($f | path basename)
                $name != "_index.md" and $name != "index.md"
            }
        } else { [] }

        $files | each {|f|
            let rel = ($q + "/" + ($f | path basename))
            let content = (open $f --raw)
            let tagged = (tag-fenced-lines $content)

            $tagged | where {|e| not $e.in_code} | each {|e|
                let cleaned = ($e.text | str replace --regex --all '`[^`]+`' '')
                $QUADRANTS | each {|target_q|
                    let marker = ("](../" + $target_q + "/")
                    if ($cleaned | str contains $marker) {
                        let same_detail = ("same-quadrant link uses `../" + $q + "/…` — resolves to /" + $q + "/" + $q + "/…; drop the quadrant name and use `../…/` for a same-quadrant sibling")
                        let cross_detail = ("cross-quadrant link uses `../" + $target_q + "/…` — resolves to /" + $q + "/" + $target_q + "/… (404); use `../../" + $target_q + "/…/` or absolute `/" + $target_q + "/…/`")
                        if $target_q == $q {
                            {file: $rel, line: $e.line, detail: $same_detail}
                        } else {
                            {file: $rel, line: $e.line, detail: $cross_detail}
                        }
                    }
                } | where {|x| $x != null}
            } | flatten
        } | flatten
    } | flatten)

    if ($problems | length) == 0 {
        make-result "check-link-form" "pass" [
            (make-evidence "content files" "relative links use the correct pretty-URL form: same-quadrant `../foo/`, cross-quadrant `../../<other>/foo/` or absolute `/<other>/foo/`")
        ] [] | to json
    } else {
        let suggestions = ($problems
            | each {|p| $p.detail }
            | uniq)
        make-result "check-link-form" "fail" $problems $suggestions | to json
    }
}
