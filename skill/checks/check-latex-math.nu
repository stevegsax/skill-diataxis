#!/usr/bin/env nu
# Check that math expressions use LaTeX notation, not plain text fractions.
use mod.nu [make-result make-evidence content-files]

def main [diataxis_dir: string] {
    let quads = [tutorials howto reference explanation]
    let all_md = ($quads | each {|q|
        content-files ($diataxis_dir | path join $q) | each {|f|
            {path: $f, rel: ($q + "/" + ($f | path basename))}
        }
    } | flatten)

    if ($all_md | length) == 0 {
        print (make-result "check-latex-math" "skip" [
            (make-evidence "diataxis.toml" "no content files found")
        ] [] | to json)
        return
    }

    # Find files with plain-text fractions outside code blocks that lack any LaTeX
    let problems = ($all_md | each {|entry|
        let content = (open $entry.path --raw)
        # Strip fenced code blocks
        let no_code = ($content | str replace --regex --all '(?s)```.*?```' '' | str replace --regex --all '`[^`]+`' '')
        # Look for plain fractions like 3/4 not part of a path or URL
        let has_plain = ($no_code | find --regex '\b\d+/\d+\b' | length) > 0
        # Look for LaTeX markers
        let has_latex = ($content | str contains "$") and ($content | find --regex '\$[^$]+\$' | length) > 0
        if $has_plain and (not $has_latex) {
            $entry.rel
        }
    } | where {|r| $r != null})

    if ($problems | length) == 0 {
        make-result "check-latex-math" "pass" [
            (make-evidence "diataxis.toml" "no plain-text math found without LaTeX")
        ] [] | to json
    } else {
        let evidence = ($problems | each {|f|
            make-evidence $f "contains plain-text fractions (e.g. 3/4) without LaTeX math notation"
        })
        let suggestions = ($problems | each {|f|
            $"Replace plain-text math in ($f) with LaTeX notation e.g. \\frac\\{3\\}\\{4\\}"
        })
        make-result "check-latex-math" "fail" $evidence $suggestions | to json
    }
}
