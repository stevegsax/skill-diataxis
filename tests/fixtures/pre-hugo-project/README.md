# pre-hugo-project fixture

A minimal `diataxis/` tree in the pre-Hugo format the skill used to
emit — before the migration to a Hugo-module site. It exists so the
skill's detection logic has something to identify. Nothing here is
meant to be published; the files are only large enough to carry the
signals the detector looks at.

## What makes it "pre-Hugo"

- No `hugo.toml`, `Makefile`, or `go.mod` at the project root.
- Every content markdown file starts with an ATX H1 (`# Title`)
  instead of a `+++`-delimited TOML frontmatter block.
- No `_index.md` landing page in any quadrant directory.
- One cross-quadrant link targets an `.html` file
  (`tutorials/first-tutorial.md` links to
  `../reference/basics-reference.html`), which the current Hugo
  configuration never produces.
- One explanation file uses dollar-delimited math (`$E = mc^2$`),
  which is the delimiter style every static-site generator outside
  Hugo reaches for.
- `diataxis.toml` declares `exercises = ["exercises/first-exercise.py"]`
  on the tutorial, the `.py` file exists, and no `examples/`
  directory exists yet — this is the state the new
  `missing_examples_landing` detection flag is for.

## Verifying detection

From the repository root, the detect-only mode of the upgrade script
should classify this fixture as needing an upgrade and name each of
the above signals:

```bash
python skill/scripts/upgrade_to_hugo.py \
    tests/fixtures/pre-hugo-project/diataxis --check
```

Exit status is `1` (upgrade needed) and the report lists
`missing_config`, `files_without_frontmatter`,
`missing_quadrant_landing_pages`, `dollar_delimited_math`, and
`missing_examples_landing`. If any of those signals stops being
reported after a change to the skill, the detector has regressed.

## Scope

The fixture is deliberately not a self-contained
`diataxis/` you can publish. Running the upgrade against it will
produce a tree that fails several downstream checks (e.g.
`check-cross-links` wants more than one content file per quadrant),
because keeping it minimal is more valuable than keeping it complete.
The broader end-to-end test of the upgrade lives in
`evals/fixtures/pre-hugo-project/`, which is driven by the
skill-creator evaluation loop.
