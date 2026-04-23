#!/usr/bin/env bash
# Run check-pyodide-imports against every fixture here.
# Usage: bash tests/fixtures/pyodide-imports/run.sh
# Exits non-zero if any fixture's status does not match expectation.

set -euo pipefail

here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
repo_root=$(cd "$here/../../.." && pwd)
check="$repo_root/skill/checks/check-pyodide-imports.nu"

declare -A expected=(
    [pass]=pass
    [fail-torch]=fail
    [fail-psycopg2]=fail
)

overall=0

for name in "${!expected[@]}"; do
    fixture="$here/$name"
    want=${expected[$name]}

    output=$(nu "$check" "$fixture")
    got=$(printf '%s' "$output" | jq -r .status)

    if [ "$got" = "$want" ]; then
        printf '  ok    %-20s (status=%s)\n' "$name" "$got"
    else
        printf '  FAIL  %-20s (status=%s, want=%s)\n' "$name" "$got" "$want"
        printf '%s\n' "$output" | jq .
        overall=1
    fi
done

exit $overall
