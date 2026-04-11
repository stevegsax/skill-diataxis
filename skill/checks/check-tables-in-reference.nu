#!/usr/bin/env nu
# Check that reference docs use tables or structured lists.
use mod.nu [make-result make-evidence content-files]

def main [diataxis_dir: string] {
    let ref_dir = ($diataxis_dir | path join "reference")
    let files = content-files $ref_dir

    if ($files | length) == 0 {
        print (make-result "check-tables-in-reference" "skip" [
            (make-evidence "reference/" "no reference content files found")
        ] [] | to json)
        return
    }

    let without_structure = ($files | each {|f|
        let content = (open $f --raw)
        let has_table = ($content | str contains "|") and ($content | str contains "---")
        let has_list = ($content | find --regex '(?m)^[-*] ' | length) > 0
        if (not $has_table) and (not $has_list) {
            "reference/" + ($f | path basename)
        }
    } | where {|r| $r != null})

    if ($without_structure | length) == 0 {
        make-result "check-tables-in-reference" "pass" [
            (make-evidence "reference/" $"all ($files | length) reference file\(s) contain tables or structured lists")
        ] [] | to json
    } else {
        let evidence = ($without_structure | each {|f|
            make-evidence $f "does not contain tables or structured lists"
        })
        let suggestions = ($without_structure | each {|f|
            $"Add tables or structured lists to ($f) — reference docs should use tabular formats"
        })
        make-result "check-tables-in-reference" "fail" $evidence $suggestions | to json
    }
}
