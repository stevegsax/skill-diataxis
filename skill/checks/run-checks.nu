#!/usr/bin/env nu
# Runner for diataxis documentation checks.
# Invokes each check script and collects results into a single JSON report.

use mod.nu [make-result]

const CHECKS = [
    # Structural checks
    check-toml-structure
    check-quadrant-files
    check-quadrant-order
    check-orphan-files
    check-status-consistency
    check-exercise-exists
    # Format checks
    check-marimo-format
    check-exercise-content
    check-latex-math
    # Quadrant rule checks
    check-howto-titles
    check-tables-in-reference
    check-step-by-step
    check-code-examples
    # Cross-linking checks
    check-cross-links
    check-link-form
]

def main [diataxis_dir: string] {
    let abs_dir = ($diataxis_dir | path expand)
    let script_dir = ($env.FILE_PWD)

    # Invoke each check as a subprocess. Use `complete` so we can detect three
    # distinct failure modes: nonzero exit, empty output, and unparseable JSON.
    # Without this, an empty stdout is silently turned into null (nu's `""
    # | from json` returns null, not an error) and then `each` drops the null
    # from the result list — so a broken check would vanish from the report.
    let results = ($CHECKS | each {|check|
        let script = ($script_dir | path join $"($check).nu")
        let proc = (^nu $script $abs_dir | complete)

        if $proc.exit_code != 0 {
            make-result $check "error" [
                {file: $"($check).nu", line: null, detail: $"script exited with code ($proc.exit_code): ($proc.stderr | str trim)"}
            ] [
                $"Fix the check script ($check).nu"
            ]
        } else if ($proc.stdout | str trim | is-empty) {
            make-result $check "error" [
                {file: $"($check).nu", line: null, detail: "script produced empty output — check for an early-return branch that drops its result (use print to emit)"}
            ] [
                $"Fix the check script ($check).nu so every code path prints its result"
            ]
        } else {
            try {
                $proc.stdout | from json
            } catch {|err|
                make-result $check "error" [
                    {file: $"($check).nu", line: null, detail: $"unparseable JSON output: ($err.msg)"}
                ] [
                    $"Fix the check script ($check).nu"
                ]
            }
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
