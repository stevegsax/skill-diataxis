#!/usr/bin/env bash
# Run check-marimo-cell-display against every fixture here.
# Usage: bash tests/fixtures/marimo-cell-display/run.sh
# Exits non-zero if any fixture's status does not match expectation.

set -euo pipefail

here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
repo_root=$(cd "$here/../../.." && pwd)
check="$repo_root/skill/checks/check-marimo-cell-display.nu"

declare -A expected=(
    [pass]=pass
    [pass-no-display-intended]=pass
    [fail-if-else]=fail
    [fail-for-loop]=fail
)

overall=0

for name in "${!expected[@]}"; do
    fixture="$here/$name"
    want=${expected[$name]}

    output=$(nu "$check" "$fixture")
    got=$(printf '%s' "$output" | jq -r .status)

    if [ "$got" = "$want" ]; then
        printf '  ok    %-28s (status=%s)\n' "$name" "$got"
    else
        printf '  FAIL  %-28s (status=%s, want=%s)\n' "$name" "$got" "$want"
        printf '%s\n' "$output" | jq .
        overall=1
    fi
done

exit $overall
