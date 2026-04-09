#!/usr/bin/env nu
# Check that tutorials have step-by-step structure with visible results.
use mod.nu [make-result make-evidence content-files]

def main [diataxis_dir: string] {
    let tutorials_dir = ($diataxis_dir | path join "tutorials")
    let files = content-files $tutorials_dir

    if ($files | length) == 0 {
        make-result "check-step-by-step" "skip" [
            (make-evidence "tutorials/" "no tutorial content files found")
        ] [] | to json
        return
    }

    let result_indicators = ["you should see" "output" "result" "you will" "you now have" "you have"]

    let problems = ($files | each {|f|
        let content = (open $f --raw)
        let content_lower = ($content | str downcase)
        let has_steps = ($content | find --regex '(?im)^##\s+step|^##\s+\d' | length) > 0
        let has_results = ($result_indicators | where {|kw| $content_lower | str contains $kw} | length) > 0
        let rel = ("tutorials/" + ($f | path basename))
        if (not $has_steps) and (not $has_results) {
            {file: $rel, detail: "missing both step headings and result indicators"}
        } else if not $has_steps {
            {file: $rel, detail: "missing step headings (e.g. '## Step 1:')"}
        } else if not $has_results {
            {file: $rel, detail: "missing result indicators (e.g. 'you should see')"}
        }
    } | where {|r| $r != null})

    if ($problems | length) == 0 {
        make-result "check-step-by-step" "pass" [
            (make-evidence "tutorials/" $"all ($files | length) tutorial\(s) have step-by-step structure with results")
        ] [] | to json
    } else {
        let evidence = ($problems | each {|p| make-evidence $p.file $p.detail})
        let suggestions = ($problems | each {|p|
            $"Add step-by-step headings and result indicators to ($p.file)"
        })
        make-result "check-step-by-step" "fail" $evidence $suggestions | to json
    }
}
