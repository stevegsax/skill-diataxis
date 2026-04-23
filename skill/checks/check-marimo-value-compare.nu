#!/usr/bin/env nu
# Check that `<widget>.value == <literal>` comparisons in marimo
# notebooks compare against the widget's mapped value, not its key.
#
# `mo.ui.radio(options={label: mapped})` and `mo.ui.dropdown(...)`
# have an asymmetric API: `value=` passed at construction is a
# **key** (label), but `.value` read at runtime returns the **mapped
# value**. An author who writes `widget.value == "Attack Roll"`
# (the label) produces a comparison that is always False — a silent
# bug that makes the widget look unresponsive in the browser with
# no error to debug.
#
# `_list_value_miscompares.py` statically detects the narrow case
# where this is certainly wrong: literal dict passed to `options=`,
# literal string on the other side of `== .value`, literal is a key
# but not also a value. Anything more ambiguous is skipped — a
# false positive on this check is worse than a miss, because
# authors start ignoring noisy checks.

use mod.nu [make-result make-evidence]

def main [diataxis_dir: string] {
    let abs_dir = ($diataxis_dir | path expand)
    let exercises_dir = ($abs_dir | path join "exercises")
    let helper = ($env.FILE_PWD | path join "_list_value_miscompares.py")

    if not ($exercises_dir | path exists) {
        print (make-result "check-marimo-value-compare" "skip" [
            (make-evidence "exercises/" "directory does not exist")
        ] [] | to json)
        return
    }

    let notebooks = (glob ($exercises_dir | path join "*.py"))

    if ($notebooks | length) == 0 {
        print (make-result "check-marimo-value-compare" "skip" [
            (make-evidence "exercises/" "no .py files under exercises/")
        ] [] | to json)
        return
    }

    let findings = ($notebooks | each {|nb|
        let rel = ($nb | path relative-to $abs_dir)
        let result = (^python3 $helper $nb | complete)
        if $result.exit_code != 0 {
            null
        } else {
            let parsed = (try { $result.stdout | from json } catch { null })
            if $parsed == null {
                null
            } else {
                let mis = ($parsed | get -o miscompares | default [])
                if ($mis | length) == 0 {
                    null
                } else {
                    {file: $rel, miscompares: $mis}
                }
            }
        }
    } | where {|r| $r != null })

    if ($findings | length) == 0 {
        make-result "check-marimo-value-compare" "pass" [
            (make-evidence "exercises/" $"all ($notebooks | length) notebook\(s) compare `.value` against mapped values, not keys")
        ] [] | to json
    } else {
        let evidence = ($findings | each {|f|
            $f.miscompares | each {|m|
                let values_str = ($m.values | each {|v| $"\"($v)\""} | str join ", ")
                (make-evidence $f.file --line $m.line
                    $"`($m.var).value == \"($m.literal)\"` compares against a dict key; `.value` returns the mapped value — expected one of [($values_str)]")
            }
        } | flatten)
        let suggestions = ($findings | each {|f|
            $f.miscompares | each {|m|
                $"In ($f.file), replace `($m.var).value == \"($m.literal)\"` with a comparison against the mapped value — or read `($m.var).selected_key` if the intent is to match the label"
            }
        } | flatten | uniq)
        make-result "check-marimo-value-compare" "fail" $evidence $suggestions | to json
    }
}
