# todo-markers fixtures

Minimal fixtures exercising `skill/checks/check-todo-markers.nu`. The
check scans prose — everything outside fenced code, inline code, and
TOML frontmatter — for incompleteness markers: `TODO`, `FIXME`, `XXX`,
`TBD`, and the phrase "lorem ipsum".

## The fixtures

| Fixture                       | content                                              | expected status | scenario tested                                      |
|-------------------------------|------------------------------------------------------|-----------------|------------------------------------------------------|
| `pass/`                       | Clean prose, no markers.                             | `pass`          | Happy path.                                          |
| `fail-todo/`                  | Two lines with `TODO:` / `FIXME:` in body prose.     | `fail`          | Tokenized markers are detected.                      |
| `fail-lorem-ipsum/`           | A paragraph that opens with "Lorem ipsum dolor sit". | `fail`          | The phrase match fires with case-insensitive match.  |
| `pass-marker-in-code-block/`  | `# TODO` inside a fenced code block; `TODO` inside inline code. | `pass`          | Code spans are stripped, so markers inside code are not counted. |

`run.sh` runs the check against each fixture and asserts the status
matches the table above.

Frontmatter is also treated as metadata and skipped, so a `description`
or `title` field that legitimately mentions "TODO" in its copy doesn't
trip the check.
