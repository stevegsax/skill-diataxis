#!/usr/bin/env nu
# Check that content markdown files don't contain placeholder
# incompleteness markers — TODO, FIXME, XXX, TBD, "lorem ipsum" — in
# authored prose.
#
# These tokens are conventional developer shorthand for "I wasn't
# done." When they survive into a published doc, readers see them.
# Fenced code blocks and inline code are stripped before scanning so
# a tutorial that legitimately shows a code snippet containing a
# `# TODO` comment is not false-flagged.
#
# The token list is deliberately narrow: only markers that are
# essentially never legitimate in Diataxis prose. "placeholder" is
# omitted because it is a legitimate noun (e.g. "add a placeholder
# for the user's name") and the skill's own docs legitimately discuss
# "placeholder" as a concept. `check-exercise-content` already catches
# placeholder stubs in notebook cells.

use mod.nu [make-result make-evidence content-files]

const QUADRANTS = [tutorials howto reference explanation examples]

# Words to flag as incompleteness markers. Matched case-insensitively
# with word boundaries so "methodology" doesn't match "TBD".
const MARKER_TOKENS = ["TODO" "FIXME" "XXX" "TBD"]
# Phrase(s) to flag outside of word-boundary matching.
const MARKER_PHRASES = ["lorem ipsum"]

# Tag each line of content with whether it lies inside a fenced code
# block or TOML frontmatter. Fence and frontmatter delimiter lines
# themselves count as "in code"/"in frontmatter" so the delimiters
# don't leak into the scan. Frontmatter is treated as metadata, not
# prose — a fixture description or title that happens to contain
# "TODO" should not trip the check.
def tag-fenced-lines [content: string]: nothing -> list<record> {
    $content
    | lines
    | enumerate
    | reduce --fold {out: [], in_code: false, in_fm: false, fm_done: false, started: false} {|pair, acc|
        let trimmed = ($pair.item | str trim)
        let is_fence = ($trimmed | str starts-with '```')
        let is_fm_delim = ($trimmed == "+++")

        # Frontmatter only counts if it starts on the first non-blank
        # line. Once closed, subsequent `+++` are just literal text.
        let can_start_fm = (not $acc.started) and (not $acc.fm_done) and $is_fm_delim
        let in_fm_now = if $can_start_fm {
            true
        } else if $acc.in_fm and $is_fm_delim {
            true  # closing delimiter still counts as in-frontmatter so it is excluded
        } else {
            $acc.in_fm and not $is_fm_delim
        }
        let next_in_fm = if $can_start_fm {
            true
        } else if $acc.in_fm and $is_fm_delim {
            false
        } else {
            $acc.in_fm
        }
        let fm_done_next = $acc.fm_done or ($acc.in_fm and $is_fm_delim)
        let started_next = $acc.started or ($trimmed != "")

        let in_code_now = ($acc.in_code or $is_fence)
        let next_in_code = if $is_fence { not $acc.in_code } else { $acc.in_code }

        let entry = {
            line: ($pair.index + 1)
            text: $pair.item
            in_code: ($in_code_now or $in_fm_now)
        }
        {out: ($acc.out | append $entry), in_code: $next_in_code, in_fm: $next_in_fm, fm_done: $fm_done_next, started: $started_next}
    }
    | get out
}

# Gather every markdown file we care about: content files in the four
# quadrants + landing pages + root homepage + optional examples
# landing.
def gather-files [diataxis_dir: string]: nothing -> list<string> {
    let root = ($diataxis_dir | path join "index.md")
    let landings = ($QUADRANTS | each {|q|
        $diataxis_dir | path join $q | path join "_index.md"
    })
    let content = ($QUADRANTS | each {|q|
        content-files ($diataxis_dir | path join $q)
    } | flatten)

    ([$root] | append $landings | append $content | where {|p| $p | path exists })
}

# Return a list of problems for one line. Each problem is {token}.
def scan-line [text: string]: nothing -> list<record> {
    # Strip inline code spans so a word like `TODO` inside backticks
    # doesn't count.
    let cleaned = ($text | str replace --regex --all '`[^`]+`' '')

    # Combined pattern: case-insensitive, word-boundary tokens OR
    # literal phrase matches. Whitespace in phrases is normalized to
    # regex `\s+` via plain string concatenation so nu's quoting
    # doesn't double-escape the backslash.
    let token_alt = ($MARKER_TOKENS | str join "|")
    let phrase_alt = ($MARKER_PHRASES
        | each {|p|
            $p
            | split row " "
            | str join ('\s' + '+')
        }
        | str join "|")
    let pattern = ("(?i)(\\b(?:" + $token_alt + ")\\b|" + $phrase_alt + ")")

    $cleaned
    | parse --regex $pattern
    | each {|m| {token: ($m.capture0 | str trim)} }
}

def main [diataxis_dir: string] {
    let abs_dir = ($diataxis_dir | path expand)
    let files = (gather-files $abs_dir)

    if ($files | length) == 0 {
        print (make-result "check-todo-markers" "skip" [
            (make-evidence "diataxis.toml" "no markdown files under the project")
        ] [] | to json)
        return
    }

    let problems = ($files | each {|f|
        let rel = ($f | path relative-to $abs_dir)
        let tagged = (tag-fenced-lines (open $f --raw))
        $tagged | where {|e| not $e.in_code} | each {|e|
            scan-line $e.text | each {|hit|
                {file: $rel, line: $e.line, token: $hit.token}
            }
        } | flatten
    } | flatten)

    if ($problems | length) == 0 {
        make-result "check-todo-markers" "pass" [
            (make-evidence "content files" $"no TODO / FIXME / XXX / TBD / 'lorem ipsum' markers in prose across ($files | length) file\(s)")
        ] [] | to json
    } else {
        let evidence = ($problems | each {|p|
            make-evidence $p.file --line $p.line $"incompleteness marker '($p.token)' in prose"
        })
        let suggestions = ["Replace each incompleteness marker with finished prose, or delete the surrounding section"]
        make-result "check-todo-markers" "fail" $evidence $suggestions | to json
    }
}
