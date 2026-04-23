#!/usr/bin/env bash
# Run check-quadrant-order against every fixture in this directory and
# verify each one's status matches the expectation encoded in its name.
# Prints the full evidence block for any fixture that fails the
# expectation, so a regression is easy to diagnose without re-running
# the check by hand.
#
# Usage: bash tests/fixtures/examples-section/run.sh
#        (or ./run.sh after chmod +x)
#
# Exits non-zero if any fixture's status does not match expectation.

set -euo pipefail

here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
repo_root=$(cd "$here/../../.." && pwd)
check="$repo_root/skill/checks/check-quadrant-order.nu"

declare -A expected=(
    [with-exercises-ok]=pass
    [with-exercises-missing-landing]=fail
    [with-exercises-wrong-weight]=fail
    [no-exercises-ok]=pass
    [no-exercises-stray-landing]=fail
)

overall=0

for name in "${!expected[@]}"; do
    fixture="$here/$name"
    want=${expected[$name]}

    output=$(nu "$check" "$fixture")
    got=$(printf '%s' "$output" | python3 -c 'import json, sys; print(json.load(sys.stdin)["status"])')

    if [ "$got" = "$want" ]; then
        printf '  ok    %-34s (status=%s)\n' "$name" "$got"
    else
        printf '  FAIL  %-34s (status=%s, want=%s)\n' "$name" "$got" "$want"
        printf '%s\n' "$output" | python3 -m json.tool
        overall=1
    fi
done

exit $overall
