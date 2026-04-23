# internal-links fixtures

Minimal `diataxis/`-shaped directories that exercise
`skill/checks/check-internal-links.nu`.

The check walks every absolute-path markdown link target
(`](/…)`) in content files and landing pages and confirms it resolves
to a file the Hugo build will actually emit — a quadrant content
`.md`, a quadrant `_index.md`, a root `index.md`, or an
`exercises/<stem>.py` WASM-bundle source.

## The fixtures

| Fixture                    | link target                | expected status | scenario tested                                                          |
|----------------------------|----------------------------|-----------------|--------------------------------------------------------------------------|
| `pass/`                    | `/reference/bar/`, `/exercises/foo/` | `pass`  | Both targets exist on disk.                                               |
| `fail-missing-content/`    | `/reference/nonexistent/`  | `fail`          | Link points at a content page whose `.md` source is not on disk.          |
| `fail-missing-exercise/`   | `/exercises/missing/`      | `fail`          | Link points at an exercise whose `.py` source is not under `exercises/`.  |

## Running the check

```bash
nu skill/checks/check-internal-links.nu tests/fixtures/internal-links/pass
nu skill/checks/check-internal-links.nu tests/fixtures/internal-links/fail-missing-content
nu skill/checks/check-internal-links.nu tests/fixtures/internal-links/fail-missing-exercise
```

`run.sh` runs all three and asserts each status matches the table above.

## Scope

These fixtures only exercise absolute-path links, which is the form the
skill's cross-linking guidance prefers. Relative-path links are left to
`check-link-form` to shape; once the shape is right, their destinations
overlap with the absolute-path case this check already covers.
