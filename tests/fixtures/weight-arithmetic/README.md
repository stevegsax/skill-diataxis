# weight-arithmetic fixtures

Minimal fixtures exercising `skill/checks/check-weight-arithmetic.nu`.

The check reads every content file listed in `diataxis.toml` and
confirms its frontmatter `weight` equals
`topic.order * 10 + quadrant_weight`, where `quadrant_weight` is
`explanation=1, tutorials=2, howto=3, reference=4`. Drift between
`diataxis.toml`'s topic order and the on-disk frontmatter silently
rearranges the published nav.

## The fixtures

| Fixture                   | topic order | frontmatter weight | expected status | scenario tested                                          |
|---------------------------|-------------|--------------------|-----------------|----------------------------------------------------------|
| `pass/`                   | 1           | 12 (= 1×10 + 2)    | `pass`          | Frontmatter weight matches the arithmetic.               |
| `fail-content-weight/`    | 1           | 42 (expected 12)   | `fail`          | Author wrote the wrong weight on the file.               |
| `fail-topic-order/`       | 3           | 12 (expected 32)   | `fail`          | Topic `order` was changed in `diataxis.toml` without refreshing the frontmatter. |

`run.sh` asserts each status matches the table.

Landing pages (`_index.md`) are out of scope — they use the fixed
section weights 10/20/30/40/50 enforced by `check-quadrant-order`.
