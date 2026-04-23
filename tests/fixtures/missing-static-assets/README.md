# missing-static-assets fixtures

Minimal fixtures exercising
`skill/checks/check-missing-static-assets.nu`.

The check walks every absolute-path markdown image reference
(`![alt](/path/to/asset.png)`) in content files and confirms the
corresponding source exists under `static/`, which is where Hugo
serves static assets from. Relative-path image references are out of
scope — their resolution depends on Hugo's per-page output location
and the skill does not otherwise mechanize it.

## The fixtures

| Fixture                  | reference                    | asset present at      | expected status |
|--------------------------|------------------------------|-----------------------|-----------------|
| `pass/`                  | `/img/widget.png`            | `static/img/widget.png` | `pass`          |
| `fail-missing-image/`    | `/img/missing.png`           | (nothing)             | `fail`          |

`run.sh` asserts each status matches the table.
