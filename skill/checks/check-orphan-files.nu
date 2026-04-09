#!/usr/bin/env nu
# Check for markdown files on disk in quadrant dirs that are not listed in diataxis.toml.
use mod.nu [load-structure all-file-entries make-result make-evidence content-files]

def main [diataxis_dir: string] {
    let structure = load-structure $diataxis_dir
    let entries = all-file-entries $structure
    let declared_files = ($entries | get file)

    let quads = [tutorials howto reference explanation]
    let orphans = ($quads | each {|q|
        let dir = ($diataxis_dir | path join $q)
        content-files $dir | each {|full_path|
            let rel = ($q + "/" + ($full_path | path basename))
            if not ($rel in $declared_files) {
                $rel
            }
        }
    } | flatten)

    if ($orphans | length) == 0 {
        make-result "check-orphan-files" "pass" [
            (make-evidence "diataxis.toml" "no orphan files found")
        ] [] | to json
    } else {
        let evidence = ($orphans | each {|f|
            make-evidence $f "file exists on disk but is not listed in diataxis.toml"
        })
        let suggestions = ($orphans | each {|f|
            $"Add ($f) to diataxis.toml or remove it from disk"
        })
        make-result "check-orphan-files" "fail" $evidence $suggestions | to json
    }
}
