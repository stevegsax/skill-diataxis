#!/usr/bin/env nu
# Check that every absolute-path markdown image reference in content
# files points at a file that exists under `static/` (Hugo's
# convention for assets served verbatim).
#
# An image `![alt](/img/foo.png)` is published by Hugo as
# `/img/foo.png`; the source on disk must live at
# `static/img/foo.png`. Relative-path references (`./images/foo.png`
# co-located with a page bundle, `../shared/logo.svg` walking back
# up) are out of scope here — their resolution depends on where Hugo
# will place the compiled page, which the skill does not otherwise
# mechanize. The absolute-path form is the easy, high-signal case
# and the one a drifted link most commonly takes.

use mod.nu [make-result make-evidence content-files]

const QUADRANTS = [tutorials howto reference explanation examples]

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

def gather-files [diataxis_dir: string]: nothing -> list<string> {
    let root = ($diataxis_dir | path join "index.md")
    let landings = ($QUADRANTS | each {|q|
        $diataxis_dir | path join $q | path join "_index.md"
    })
    let content = ($QUADRANTS | each {|q|
        content-files ($diataxis_dir | path join $q)
    } | flatten)

    ([$root] | append $landings | append $content | where {|p| $p | path exists })
}

def main [diataxis_dir: string] {
    let abs_dir = ($diataxis_dir | path expand)
    let files = (gather-files $abs_dir)

    if ($files | length) == 0 {
        print (make-result "check-missing-static-assets" "skip" [
            (make-evidence "content files" "no markdown files under the project")
        ] [] | to json)
        return
    }

    let problems = ($files | each {|f|
        let rel = ($f | path relative-to $abs_dir)
        let tagged = (tag-fenced-lines (open $f --raw))
        $tagged | where {|e| not $e.in_code} | each {|e|
            # Strip inline code so `![img](/…)` in backticks doesn't count.
            let cleaned = ($e.text | str replace --regex --all '`[^`]+`' '')
            # Match `![alt](/abs/path/to/asset.ext)` — only absolute paths.
            $cleaned | parse --regex '!\[[^\]]*\]\((?P<target>/[^)\s]+)\)' | each {|m|
                let target = $m.target

                # Skip protocol-relative URLs.
                if ($target | str starts-with "//") { return null }

                # Strip fragment and query parts.
                let path = ($target | split row "#" | first | split row "?" | first)

                # Hugo serves anything under `static/` at the site
                # root, so `/img/foo.png` must come from
                # `static/img/foo.png`. WASM-bundle references to
                # `/exercises/<stem>/` are handled by
                # `check-internal-links`, not here — skip image
                # references that happen to use the same prefix.
                if ($path | str starts-with "/exercises/") { return null }

                let trimmed = ($path | str substring 1..)
                let source = ($abs_dir | path join "static" | path join $trimmed)
                if ($source | path exists) {
                    null
                } else {
                    {file: $rel, line: $e.line, target: $target, source: ($source | path relative-to $abs_dir)}
                }
            } | where {|x| $x != null}
        } | flatten
    } | flatten)

    if ($problems | length) == 0 {
        make-result "check-missing-static-assets" "pass" [
            (make-evidence "content files" "every absolute-path image reference resolves to a file under static/")
        ] [] | to json
    } else {
        let evidence = ($problems | each {|p|
            make-evidence $p.file --line $p.line $"image reference ($p.target) has no source at ($p.source)"
        })
        let suggestions = ($problems | each {|p|
            $"Either place the image at ($p.source), or update the reference in ($p.file) to an existing asset"
        } | uniq)
        make-result "check-missing-static-assets" "fail" $evidence $suggestions | to json
    }
}
