#!/usr/bin/env nu
# Check that absolute-path markdown links in content files resolve to
# files that exist on disk.
#
# The skill's cross-linking guidance prefers absolute paths
# (`/tutorials/foo/`, `/exercises/bar/`, …) because Hugo rewrites them
# per page when `relativeURLs = true`. Those links are easy to check
# deterministically: strip the leading slash, convert the trailing
# slash to either `.md` (for content files) or `/_index.md` (for
# sections), or `.py` for `/exercises/…` WASM bundles, then test
# existence.
#
# This check complements `check-link-form`. That check lints the shape
# of relative links — whether `../` counts are right for Hugo pretty
# URLs. This check validates destinations, which `check-link-form`
# cannot do.
#
# Scope: only absolute-path targets (`](/…)`). Relative-path targets
# are left to `check-link-form` to shape; once the shape is right,
# their destinations overlap substantially with the absolute-path
# form authors should be using in the first place, so catching the
# absolute form is where the value is.
#
# Fragment identifiers (`#anchor`) are stripped before resolution;
# fragment-existence is a separate concern not yet checked.

use mod.nu [make-result make-evidence]

const QUADRANTS = [tutorials howto reference explanation examples]

# Tag each line with whether it lies inside a fenced code block. Fence
# lines themselves count as in-code so the ``` isn't scanned for links.
def tag-fenced-lines [content: string]: nothing -> list<record> {
    $content
    | lines
    | enumerate
    | reduce --fold {out: [], in_code: false} {|pair, acc|
        let trimmed = ($pair.item | str trim)
        let is_fence = ($trimmed | str starts-with '```')
        let in_code_now = ($acc.in_code or $is_fence)
        let next_in_code = if $is_fence { not $acc.in_code } else { $acc.in_code }
        let entry = {
            line: ($pair.index + 1)
            text: $pair.item
            in_code: $in_code_now
        }
        {out: ($acc.out | append $entry), in_code: $next_in_code}
    }
    | get out
}

# Gather every markdown file under diataxis_dir that may contain
# cross-section links: content files in the four quadrants plus
# examples/_index.md, each quadrant's _index.md, and the root
# index.md. Skips the five `_index.md` files only when they don't
# exist on disk.
def gather-files [diataxis_dir: string]: nothing -> list<string> {
    let root = ($diataxis_dir | path join "index.md")
    let landing_pages = ($QUADRANTS | each {|q|
        $diataxis_dir | path join $q | path join "_index.md"
    })
    let content = ($QUADRANTS | each {|q|
        let qdir = ($diataxis_dir | path join $q)
        if ($qdir | path exists) {
            glob ($qdir | path join "*.md") | where {|f|
                let name = ($f | path basename)
                $name != "_index.md" and $name != "index.md"
            }
        } else { [] }
    } | flatten)

    ([$root] | append $landing_pages | append $content | where {|p| $p | path exists })
}

# Resolve an absolute URL path (always starts with `/`) to a source
# filesystem path relative to diataxis_dir. Returns null if the URL
# form doesn't map to anything the skill produces on disk.
#
# The resolution rules mirror what the Makefile and hugo.toml produce:
#
#   /                         → index.md
#   /<quadrant>/              → <quadrant>/_index.md
#   /<quadrant>/<slug>/       → <quadrant>/<slug>.md
#   /exercises/<stem>/        → exercises/<stem>.py
#   /static/<path>            → static/<path>             (verbatim)
#
# Anything else (no leading slash, or a URL that mixes in extra
# segments) returns null and is treated as unresolvable.
def url-to-source [url: string]: nothing -> any {
    # Strip fragment and query; we only check the path part.
    let without_fragment = ($url | split row "#" | first)
    let path = ($without_fragment | split row "?" | first)

    if not ($path | str starts-with "/") { return null }

    # Normalize: strip leading slash, strip trailing slash (but remember
    # that it was there — trailing slash means "pretty URL" so a
    # content-file resolution of `<path>.md` is appropriate).
    let trimmed = ($path | str substring 1..)
    let had_trailing = ($trimmed | str ends-with "/")
    let body = if $had_trailing { $trimmed | str substring 0..(($trimmed | str length) - 2) } else { $trimmed }

    if $body == "" {
        # Root URL — resolve to root index.md.
        return "index.md"
    }

    let parts = ($body | split row "/")
    let first_seg = ($parts | first)

    # Exercises: /exercises/<stem>/ → exercises/<stem>.py
    if $first_seg == "exercises" and ($parts | length) == 2 {
        return $"exercises/($parts | get 1).py"
    }

    # Static assets: /static/foo/bar.png → static/foo/bar.png (verbatim)
    if $first_seg == "static" {
        return $body
    }

    # Quadrant: /<quadrant>/ → <quadrant>/_index.md
    if ($first_seg in $QUADRANTS) and ($parts | length) == 1 {
        return $"($first_seg)/_index.md"
    }

    # Quadrant + slug: /<quadrant>/<slug>/ → <quadrant>/<slug>.md
    if ($first_seg in $QUADRANTS) and ($parts | length) == 2 {
        return $"($first_seg)/($parts | get 1).md"
    }

    # Anything else (unknown top-level segment, deeper nesting) isn't
    # produced by the skill and we can't prove resolution. Signal
    # "unknown" so the caller can skip rather than false-fail.
    null
}

def main [diataxis_dir: string] {
    let abs_dir = ($diataxis_dir | path expand)
    let files = (gather-files $abs_dir)

    if ($files | length) == 0 {
        print (make-result "check-internal-links" "skip" [
            (make-evidence "diataxis.toml" "no markdown files under the project")
        ] [] | to json)
        return
    }

    let problems = ($files | each {|f|
        let rel = ($f | path relative-to $abs_dir)
        let content = (open $f --raw)
        let tagged = (tag-fenced-lines $content)

        $tagged | where {|e| not $e.in_code} | each {|e|
            # Strip inline code so links inside backticks aren't scanned.
            let cleaned = ($e.text | str replace --regex --all '`[^`]+`' '')
            # Extract every `](target)` target on this line.
            $cleaned | parse --regex '\]\((?P<target>[^)\s]+)\)' | each {|m|
                let target = $m.target
                # Skip non-absolute targets — they're covered by
                # check-link-form and not in this check's scope.
                if not ($target | str starts-with "/") { return null }
                # Skip protocol-relative URLs (`//example.com/…`).
                if ($target | str starts-with "//") { return null }

                let source_path = (url-to-source $target)
                if $source_path == null {
                    # URL shape doesn't map to anything the skill
                    # produces — treat as out-of-scope rather than
                    # broken. (Authors who invent a link form outside
                    # the documented set are on their own.)
                    return null
                }

                let abs_source = ($abs_dir | path join $source_path)
                if not ($abs_source | path exists) {
                    {file: $rel, line: $e.line, target: $target, source: $source_path}
                } else {
                    null
                }
            } | where {|x| $x != null}
        } | flatten
    } | flatten)

    if ($problems | length) == 0 {
        make-result "check-internal-links" "pass" [
            (make-evidence "content files" "every absolute-path markdown link resolves to a file on disk")
        ] [] | to json
    } else {
        let evidence = ($problems | each {|p|
            make-evidence $p.file --line $p.line $"link target ($p.target) resolves to ($p.source), which does not exist"
        })
        let suggestions = ($problems | each {|p|
            $"Either create ($p.source) or update the link in ($p.file):($p.line) to an existing target"
        } | uniq)
        make-result "check-internal-links" "fail" $evidence $suggestions | to json
    }
}
