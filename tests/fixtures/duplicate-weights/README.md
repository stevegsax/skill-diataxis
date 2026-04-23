# duplicate-weights fixtures

Minimal fixtures exercising `skill/checks/check-duplicate-weights.nu`.

Hugo orders pages in a section by frontmatter `weight` ascending.
When two content files in the same quadrant tie on weight, Hugo falls
back to file name — non-obvious ordering that silently rearranges the
nav any time a file is renamed. The check flags every such collision.

## The fixtures

| Fixture                                       | layout                                                                 | expected status | scenario tested                              |
|-----------------------------------------------|------------------------------------------------------------------------|-----------------|----------------------------------------------|
| `pass/`                                       | `tutorials/foo.md` (12), `tutorials/bar.md` (22)                       | `pass`          | Distinct weights in the same quadrant.        |
| `fail-same-quadrant/`                         | `tutorials/foo.md` (12), `tutorials/bar.md` (12)                       | `fail`          | Two files in tutorials/ tie on weight=12.     |
| `pass-same-weight-different-quadrants/`       | `tutorials/foo.md` (12), `reference/bar.md` (12)                       | `pass`          | Same weight across different quadrants is fine — Hugo orders each section independently. |

`run.sh` asserts each status matches the table. Landing pages
(`_index.md`) are out of scope and are checked by
`check-quadrant-order`.
