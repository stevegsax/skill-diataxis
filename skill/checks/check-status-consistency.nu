#!/usr/bin/env nu
# Check that files with status draft/review/complete actually exist and are non-empty.
use mod.nu [load-structure all-file-entries make-result make-evidence FILE_EXPECTED_STATUSES]

def main [diataxis_dir: string] {
    let structure = load-structure $diataxis_dir
    let entries = all-file-entries $structure
    let expected = [draft review complete]

    let problems = ($entries | where {|e| $e.status in $expected } | each {|e|
        let full_path = ($diataxis_dir | path join $e.file)
        if not ($full_path | path exists) {
            {file: $e.file, detail: $"status is '($e.status)' but file does not exist"}
        } else if (open $full_path | str trim | is-empty) {
            {file: $e.file, detail: $"status is '($e.status)' but file is empty"}
        }
    } | where {|r| $r != null})

    if ($problems | length) == 0 {
        make-result "check-status-consistency" "pass" [
            (make-evidence "diataxis.toml" "all file statuses are consistent with disk")
        ] [] | to json
    } else {
        let evidence = ($problems | each {|p|
            make-evidence $p.file $p.detail
        })
        let suggestions = ($problems | each {|p|
            $"Update status for ($p.file) in diataxis.toml to 'planned', or create the file"
        })
        make-result "check-status-consistency" "fail" $evidence $suggestions | to json
    }
}
