#!/usr/bin/env nu
# Check that how-to guide titles start with "How to".
#
# Reads the title from TOML frontmatter if present (`title = "..."`), else
# falls back to the first ATX H1 in the body.
use mod.nu [make-result make-evidence content-files read-page-title]

def main [diataxis_dir: string] {
    let howto_dir = ($diataxis_dir | path join "howto")
    let files = content-files $howto_dir

    if ($files | length) == 0 {
        print (make-result "check-howto-titles" "skip" [
            (make-evidence "howto/" "no how-to content files found")
        ] [] | to json)
        return
    }

    let incorrect = ($files | each {|f|
        let title = (read-page-title $f)
        if $title == null {
            {file: ("howto/" + ($f | path basename)), title: "(no title found)"}
        } else if not ($title | str downcase | str starts-with "how to") {
            {file: ("howto/" + ($f | path basename)), title: $title}
        }
    } | where {|r| $r != null})

    if ($incorrect | length) == 0 {
        make-result "check-howto-titles" "pass" [
            (make-evidence "howto/" $"all ($files | length) how-to title\(s) start with 'How to'")
        ] [] | to json
    } else {
        let evidence = ($incorrect | each {|e|
            make-evidence $e.file $"title '($e.title)' does not start with 'How to'"
        })
        let suggestions = ($incorrect | each {|e|
            $"Rename the title in ($e.file) to start with 'How to' \(in TOML frontmatter or body H1)"
        })
        make-result "check-howto-titles" "fail" $evidence $suggestions | to json
    }
}
