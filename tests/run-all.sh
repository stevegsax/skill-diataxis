#!/usr/bin/env bash
# Run every per-topic fixture runner under tests/fixtures/. Each
# topic directory (e.g. `examples-section/`, `internal-links/`) owns
# its own `run.sh` that knows the expected status of each fixture it
# contains; this script just orchestrates them and reports overall
# pass/fail.
#
# Usage:
#   bash tests/run-all.sh
#
# Exits 0 when every topic runner exits 0, non-zero if any fails.

set -euo pipefail

here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
fixtures="$here/fixtures"

overall=0
topic_count=0
topic_failures=()

for runner in "$fixtures"/*/run.sh; do
    [ -e "$runner" ] || continue
    topic=$(basename "$(dirname "$runner")")
    topic_count=$((topic_count + 1))

    printf '=== %s ===\n' "$topic"
    if bash "$runner"; then
        :
    else
        overall=1
        topic_failures+=("$topic")
    fi
    printf '\n'
done

if [ "$topic_count" = "0" ]; then
    printf 'No fixture runners found under %s\n' "$fixtures" >&2
    exit 2
fi

if [ "$overall" = "0" ]; then
    printf 'All %d topic(s) passed.\n' "$topic_count"
else
    printf 'Failures in %d topic(s): %s\n' "${#topic_failures[@]}" "${topic_failures[*]}" >&2
fi

exit $overall
