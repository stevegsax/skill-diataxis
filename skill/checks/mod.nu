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

# Read the page title for a markdown file.
#
# Prefers TOML frontmatter (`title = "..."` inside a +++ delimited block at
# the top of the file); falls back to the first ATX H1 (`# Title`) in the
# body. Returns null if neither is present.
export def read-page-title [file: string]: nothing -> any {
    let content = (open $file --raw)
    let lines = ($content | lines)

    if ($lines | length) > 0 and ($lines | first) == "+++" {
        # TOML frontmatter — collect lines until the closing delimiter, parse, return title.
        let rest = ($lines | skip 1)
        let close_idx = ($rest | enumerate | where {|p| $p.item == "+++"} | first | get -o index)
        if $close_idx != null {
            let toml_text = ($rest | take $close_idx | str join "\n")
            let fm = (try { $toml_text | from toml } catch { null })
            if $fm != null {
                return ($fm | get -o title)
            }
        }
    }

    let heading = ($lines | where {|l| $l starts-with "# "} | first)
    if $heading == null { null } else { $heading | str replace "# " "" }
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
