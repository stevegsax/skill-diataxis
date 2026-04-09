#!/usr/bin/env nu
# Check that tutorials contain code blocks.
use mod.nu [make-result make-evidence content-files]

def main [diataxis_dir: string] {
    let tutorials_dir = ($diataxis_dir | path join "tutorials")
    let files = content-files $tutorials_dir

    if ($files | length) == 0 {
        make-result "check-code-examples" "skip" [
            (make-evidence "tutorials/" "no tutorial content files found")
        ] [] | to json
        return
    }

    let without_code = ($files | each {|f|
        let content = (open $f --raw)
        if not ($content | str contains "```") {
            "tutorials/" + ($f | path basename)
        }
    } | where {|r| $r != null})

    if ($without_code | length) == 0 {
        make-result "check-code-examples" "pass" [
            (make-evidence "tutorials/" $"all ($files | length) tutorial\(s) contain code blocks")
        ] [] | to json
    } else {
        let evidence = ($without_code | each {|f|
            make-evidence $f "does not contain any fenced code blocks"
        })
        let suggestions = ($without_code | each {|f|
            $"Add code examples to ($f) — tutorials should show concrete code"
        })
        make-result "check-code-examples" "fail" $evidence $suggestions | to json
    }
}
