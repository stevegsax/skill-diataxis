# Shared module for diataxis check scripts.

# The four quadrant directory names.
export const QUADRANT_DIRS = [tutorials howto reference explanation]

# Status values that imply a file should exist on disk.
export const FILE_EXPECTED_STATUSES = [draft review complete]

# Load and parse diataxis.toml from the given directory.
export def load-structure [diataxis_dir: string]: nothing -> record {
    open ($diataxis_dir | path join "diataxis.toml")
}

# List content markdown files in a directory, excluding index.md.
export def content-files [dir: string]: nothing -> list<string> {
    if not ($dir | path exists) { return [] }
    glob ($dir | path join "*.md")
    | where {|f| ($f | path basename) != "index.md"}
}

# Build a check result record.
export def make-result [
    check: string
    status: string
    evidence: list<record>
    suggestions: list<string>
]: nothing -> record {
    {
        check: $check
        status: $status
        evidence: $evidence
        suggestions: $suggestions
    }
}

# Build a single evidence entry.
export def make-evidence [
    file: string
    detail: string
    --line: int
]: nothing -> record {
    {
        file: $file
        line: (if $line != null { $line } else { null })
        detail: $detail
    }
}

# Collect all file entries from all topics in the structure.
# Returns a list of records with: slug, quadrant, file, status, covers, exercises.
export def all-file-entries [structure: record]: nothing -> list<record> {
    let topics = ($structure | get -o topics | default {})
    let quads = [tutorials howto reference explanation]
    $topics | columns | each {|slug|
        let topic = ($topics | get $slug)
        $quads | each {|q|
            let entry = ($topic | get -o $q)
            if $entry != null {
                {
                    slug: $slug
                    quadrant: $q
                    file: ($entry | get -o file | default "")
                    status: ($entry | get -o status | default "planned")
                    covers: ($entry | get -o covers | default [])
                    exercises: ($entry | get -o exercises | default [])
                }
            }
        }
    } | flatten | where {|r| $r.file != ""}
}
