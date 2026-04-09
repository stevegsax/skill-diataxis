#!/usr/bin/env nu
# Runner for diataxis documentation checks.
# Invokes each check script and collects results into a single JSON report.

use mod.nu [make-result]

const CHECKS = [
    # Structural checks
    check-toml-valid
    check-toml-topics
    check-purpose-field
    check-quadrant-files
    check-orphan-files
    check-status-consistency
    check-exercise-exists
    # Format checks
    check-marimo-format
    check-latex-math
    check-guidance-coherent
    # Quadrant rule checks
    check-howto-titles
    check-tables-in-reference
    check-step-by-step
    check-code-examples
    # Cross-linking checks
    check-cross-links
]

def main [diataxis_dir: string] {
    let abs_dir = ($diataxis_dir | path expand)
    let script_dir = ($env.FILE_PWD)

    let results = ($CHECKS | each {|check|
        let script = ($script_dir | path join $"($check).nu")
        try {
            nu $script $abs_dir | from json
        } catch {|err|
            make-result $check "error" [
                {file: $"($check).nu", line: null, detail: $"script error: ($err.msg)"}
            ] [
                $"Fix the check script ($check).nu"
            ]
        }
    })

    let summary = {
        pass: ($results | where status == "pass" | length)
        fail: ($results | where status == "fail" | length)
        skip: ($results | where status == "skip" | length)
        error: ($results | where status == "error" | length)
    }

    {
        diataxis_dir: $abs_dir
        timestamp: (date now | format date "%Y-%m-%dT%H:%M:%SZ")
        results: $results
        summary: $summary
    } | to json
}
