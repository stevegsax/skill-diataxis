#!/usr/bin/env nu
# Validate diataxis.toml against the JSON Schema at skill/assets/diataxis-schema.json.
#
# This is a deterministic structural check. It subsumes the old parse-validity,
# topics-present, purpose-field, and guidance-coherence checks: one schema defines
# what a valid diataxis.toml looks like, and this wrapper calls check-jsonschema
# to do the actual validation.
use mod.nu [make-result make-evidence]

def main [diataxis_dir: string] {
    let abs_dir = ($diataxis_dir | path expand)
    let toml_path = ($abs_dir | path join "diataxis.toml")
    let schema_path = ($env.FILE_PWD | path dirname | path join "assets" "diataxis-schema.json")

    let result = if not ($toml_path | path exists) {
        make-result "check-toml-structure" "fail" [
            (make-evidence "diataxis.toml" "file does not exist")
        ] [
            "Create diataxis.toml in the diataxis directory"
        ]
    } else if not ($schema_path | path exists) {
        make-result "check-toml-structure" "error" [
            (make-evidence $schema_path "schema file not found")
        ] [
            "Restore skill/assets/diataxis-schema.json from git"
        ]
    } else {
        validate $toml_path $schema_path
    }

    $result | to json
}

# Run check-jsonschema and translate its output into a check-result record.
def validate [toml_path: string, schema_path: string]: nothing -> record {
    let raw = (^uv run check-jsonschema --output-format json --schemafile $schema_path $toml_path | complete)

    # Exit 0 = ok, 1 = validation or parse failure. Anything else is a crash.
    if $raw.exit_code not-in [0 1] {
        return (make-result "check-toml-structure" "error" [
            (make-evidence "diataxis.toml" $"check-jsonschema crashed with exit ($raw.exit_code): ($raw.stderr | str trim)")
        ] [
            "Run 'uv sync' to install check-jsonschema, or verify uv is on PATH"
        ])
    }

    let parsed = try {
        $raw.stdout | from json
    } catch {
        null
    }

    if $parsed == null {
        return (make-result "check-toml-structure" "error" [
            (make-evidence "diataxis.toml" $"check-jsonschema returned unparseable output: ($raw.stdout)")
        ] [
            "Run 'uv sync' and retry; if the problem persists, run check-jsonschema manually to diagnose"
        ])
    }

    if $parsed.status == "ok" {
        return (make-result "check-toml-structure" "pass" [
            (make-evidence "diataxis.toml" "matches diataxis.json schema")
        ] [])
    }

    let parse_errors = ($parsed | get -o parse_errors | default [])
    let validation_errors = ($parsed | get -o errors | default [])

    let parse_evidence = ($parse_errors | each {|e|
        make-evidence "diataxis.toml" $"TOML parse error: ($e.message)"
    })
    let parse_suggestions = (if ($parse_errors | length) > 0 { ["Fix TOML syntax errors in diataxis.toml before re-running checks"] } else { [] })

    let validation_evidence = ($validation_errors | each {|e|
        let path = ($e | get -o path | default "$")
        let msg = ($e | get -o message | default "unknown error")
        make-evidence "diataxis.toml" $"($path): (format-message $msg)"
    })
    let validation_suggestions = ($validation_errors | each {|e|
        let path = ($e | get -o path | default "$")
        let msg = ($e | get -o message | default "")
        suggestion-for $path $msg
    })

    let evidence = ($parse_evidence | append $validation_evidence)
    let suggestions = ($parse_suggestions | append $validation_suggestions | uniq)

    make-result "check-toml-structure" "fail" $evidence $suggestions
}

# Shorten schema error messages so the evidence reads cleanly.
def format-message [msg: string]: nothing -> string {
    if ($msg | str contains "should not be valid under") and (contains-revision-marker $msg) {
        "guidance contains a labeled revision block (REVISION FEEDBACK:, FEEDBACK:, etc.) — integrate feedback into the guidance prose instead"
    } else {
        $msg
    }
}

# Translate a schema error into an actionable suggestion.
def suggestion-for [path: string, msg: string]: nothing -> string {
    if (contains-revision-marker $msg) {
        $"Rewrite guidance at ($path) as coherent prose that incorporates revision feedback — do not use labeled REVISION FEEDBACK: blocks"
    } else if ($msg | str contains "is a required property") {
        $"Add the missing required field at ($path) — see skill/references/structure-schema.md"
    } else if ($msg | str contains "is not one of") {
        $"Use one of the allowed enum values at ($path) — see skill/references/structure-schema.md"
    } else if ($msg | str contains "does not match") {
        $"Fix the value at ($path) to match the expected pattern — see skill/references/structure-schema.md"
    } else if ($msg | str contains "Additional properties are not allowed") {
        $"Remove the unknown key at ($path) — see skill/references/structure-schema.md for valid fields"
    } else {
        $"Fix the value at ($path): ($msg)"
    }
}

def contains-revision-marker [msg: string]: nothing -> bool {
    ($msg | str contains "REVISION FEEDBACK:") or ($msg | str contains "USER FEEDBACK:") or ($msg | str contains "'REVISION:") or ($msg | str contains "'FEEDBACK:")
}
