#!/usr/bin/env nu
# Check that every marimo notebook under `exercises/` parses as a
# syntactically valid Python module.
#
# `check-marimo-format` is pattern-based — it greps for `import
# marimo` and `app = marimo.App()` and declares victory. Pattern
# matches are cheap but miss real syntax errors: a missing paren, an
# unclosed string, a stray colon. Those notebooks still "look right"
# at a glance and will pass the format check, then fail silently when
# the build runs `marimo export html-wasm`. A syntax error caught at
# check time is one less bad build.
#
# Runs `python3 -c 'import ast; ast.parse(...)'` per file, one
# subprocess per notebook. Not a performance concern — projects
# typically ship under a dozen exercises and each parse is tens of
# milliseconds.

use mod.nu [make-result make-evidence]

def main [diataxis_dir: string] {
    let abs_dir = ($diataxis_dir | path expand)
    let exercises_dir = ($abs_dir | path join "exercises")

    if not ($exercises_dir | path exists) {
        print (make-result "check-marimo-ast" "skip" [
            (make-evidence "exercises/" "directory does not exist")
        ] [] | to json)
        return
    }

    let notebooks = (glob ($exercises_dir | path join "*.py"))

    if ($notebooks | length) == 0 {
        print (make-result "check-marimo-ast" "skip" [
            (make-evidence "exercises/" "no .py files under exercises/")
        ] [] | to json)
        return
    }

    let failures = ($notebooks | each {|nb|
        let rel = ($nb | path relative-to $abs_dir)
        let result = (^python3 -c $"import ast, sys; ast.parse\(open\('($nb)').read\(\))" | complete)
        if $result.exit_code != 0 {
            let stderr_line = ($result.stderr | lines | last | default "unknown syntax error")
            {file: $rel, detail: $stderr_line}
        } else {
            null
        }
    } | where {|r| $r != null })

    if ($failures | length) == 0 {
        make-result "check-marimo-ast" "pass" [
            (make-evidence "exercises/" $"all ($notebooks | length) notebook\(s) parse as valid Python")
        ] [] | to json
    } else {
        let evidence = ($failures | each {|f|
            make-evidence $f.file $f.detail
        })
        let suggestions = ($failures | each {|f|
            "Fix the Python syntax error in " + $f.file + " — running it through `python3 -m py_compile` locally shows the full traceback"
        } | uniq)
        make-result "check-marimo-ast" "fail" $evidence $suggestions | to json
    }
}
