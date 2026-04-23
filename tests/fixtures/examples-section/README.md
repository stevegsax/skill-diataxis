# examples-section fixtures

Minimal `diataxis/`-shaped directories that exercise each branch of
`skill/checks/check-quadrant-order.nu` as it relates to the optional
fifth `Examples` section. Each fixture contains only the files the
check inspects — four canonical quadrant landing pages at their
canonical weights plus the fixture-specific variation — so the
output is easy to reason about.

## The fixtures

| Fixture                             | has `exercises/*.py` | has `examples/_index.md` | expected status | scenario tested                                                 |
|-------------------------------------|----------------------|--------------------------|-----------------|-----------------------------------------------------------------|
| `with-exercises-ok/`                | yes                  | yes, weight 50            | `pass`          | Happy path: project ships exercises and the landing page matches. |
| `with-exercises-missing-landing/`   | yes                  | no                        | `fail`          | Project has exercises but no landing page — creation required.  |
| `with-exercises-wrong-weight/`      | yes                  | yes, weight 15            | `fail`          | Landing page present but at a weight that breaks the canonical ordering. |
| `no-exercises-ok/`                  | no                   | no                        | `pass`          | Correctly exerciseless project — Examples section is absent, which is the intended behavior. |
| `no-exercises-stray-landing/`       | no                   | yes                       | `fail`          | Landing page exists on a project with no exercises — check should flag for removal, not content fixes. |

## Running the check against each fixture

From the repository root:

```bash
for f in tests/fixtures/examples-section/*/; do
    echo "--- $f ---"
    nu skill/checks/check-quadrant-order.nu "$f" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["status"])'
done
```

`run.sh` in this directory does the same thing and prints the detailed
evidence for any fixture whose status does not match expectation.

## Scope

These fixtures are intentionally narrow: they exercise
`check-quadrant-order` only. They deliberately do not ship a valid
`diataxis.toml`, content files, or non-empty `exercises/foo.py` — other
checks would rightly complain about those, but this battery does not
run them. Add fixtures under a sibling directory
(`tests/fixtures/<check-name>/`) when you want coverage for another
check.
