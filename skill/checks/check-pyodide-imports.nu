#!/usr/bin/env nu
# Check that every marimo notebook under `exercises/` imports only
# top-level packages known to work in the Pyodide runtime that the
# skill's Makefile ships to the browser.
#
# The WASM export path is `marimo export html-wasm`, which bundles
# the notebook with Pyodide and loads it in a browser. Many common
# Python packages are Pyodide-compatible (numpy, pandas, matplotlib,
# scipy, scikit-learn, …). A smaller, well-known set is NOT —
# packages that wrap C or C++ libraries without a WASM build, or
# that assume a GPU, or that reach out to native network stacks.
# Authors sometimes reach for these reflexively and don't discover
# the breakage until the deployed page refuses to load.
#
# The deny list is intentionally short. Being narrow keeps the check
# trustworthy: an overbroad deny list would reject legitimate
# notebooks and train authors to ignore it. Add to it only when a
# package is demonstrably broken in Pyodide.

use mod.nu [make-result make-evidence]

# Packages that will never work under Pyodide as it ships today.
# Sources: Pyodide's documented unsupported list plus packages the
# skill has seen tripped on by authors.
const DENY_LIST = [
    "psycopg2"
    "psycopg2_binary"
    "lxml"
    "torch"
    "torchvision"
    "torchaudio"
    "tensorflow"
    "grpcio"
    "mysqlclient"
    "pycurl"
]

def main [diataxis_dir: string] {
    let abs_dir = ($diataxis_dir | path expand)
    let exercises_dir = ($abs_dir | path join "exercises")
    let helper = ($env.FILE_PWD | path join "_list_imports.py")

    if not ($exercises_dir | path exists) {
        print (make-result "check-pyodide-imports" "skip" [
            (make-evidence "exercises/" "directory does not exist")
        ] [] | to json)
        return
    }

    let notebooks = (glob ($exercises_dir | path join "*.py"))

    if ($notebooks | length) == 0 {
        print (make-result "check-pyodide-imports" "skip" [
            (make-evidence "exercises/" "no .py files under exercises/")
        ] [] | to json)
        return
    }

    let violations = ($notebooks | each {|nb|
        let rel = ($nb | path relative-to $abs_dir)
        let result = (^python3 $helper $nb | complete)
        if $result.exit_code != 0 {
            # Syntax errors are caught by check-marimo-ast; we skip
            # them here rather than double-reporting.
            null
        } else {
            let parsed = (try { $result.stdout | from json } catch { null })
            if $parsed == null { return null }
            let imports = ($parsed | get -o imports | default [])
            let bad = ($imports | where {|i| $i in $DENY_LIST })
            if ($bad | length) > 0 {
                {file: $rel, bad: $bad}
            } else {
                null
            }
        }
    } | where {|r| $r != null })

    if ($violations | length) == 0 {
        make-result "check-pyodide-imports" "pass" [
            (make-evidence "exercises/" $"all ($notebooks | length) notebook\(s) import only Pyodide-compatible packages")
        ] [] | to json
    } else {
        let evidence = ($violations | each {|v|
            let joined = ($v.bad | str join ", ")
            make-evidence $v.file $"imports package\(s) not available in Pyodide: ($joined)"
        })
        let suggestions = ($violations | each {|v|
            let joined = ($v.bad | str join ", ")
            "Replace " + $joined + " in " + $v.file + " with a Pyodide-compatible alternative, or move the logic out of the notebook"
        } | uniq)
        make-result "check-pyodide-imports" "fail" $evidence $suggestions | to json
    }
}
