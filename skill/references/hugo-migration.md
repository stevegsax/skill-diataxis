# Upgrading Pre-Hugo Projects

Earlier versions of this skill shipped a custom Python build pipeline; the
current skill targets a plain Hugo site. The `diataxis.toml` schema has not
changed, but everything around it has. When the skill is pointed at a
project authored under the old pipeline, the quadrant markdown, the
homepage, and the publishing config all need to change shape before any
new work — generation, scoring, or revision — can run.

The mechanical half of that migration is handled by
`skill/scripts/upgrade_to_hugo.py`. This reference explains what the old
projects look like, what the upgrade does (and does not) do, and how to
verify the result.

## How to tell you have a pre-Hugo project

Any one of the following is enough to conclude the project predates the
Hugo migration:

- `diataxis/` has no `hugo.toml` alongside `diataxis.toml`.
- `diataxis/` has no `Makefile` or `go.mod`.
- Quadrant markdown files (e.g. `tutorials/first-project.md`) start with an
  ATX H1 (`# Title`) instead of a `+++`-delimited TOML frontmatter block.
- Quadrant directories have no `_index.md` section landing page.
- Internal links point at `.html` targets (`tutorials/index.html`) instead
  of Hugo pretty URLs (`tutorials/`).
- Guidance or prose references retired tools: `pandoc`, `mmdc`,
  `uv run diataxis build`, or an output directory of `diataxis/_build/`.

Run the detection pass directly:

```bash
python skill/scripts/upgrade_to_hugo.py <diataxis_dir> --check
```

Exit status is `0` when the directory is already in Hugo format and `1`
when pre-Hugo artifacts are present. Add `--json` for machine-readable
output.

## Shape differences at a glance

| Concern               | Pre-Hugo                                    | Hugo                                              |
|-----------------------|---------------------------------------------|---------------------------------------------------|
| Publishing config     | None (Python CLI)                           | `hugo.toml`, `Makefile`, `go.mod`                 |
| Content file header   | `# Title` body H1                           | `+++ title = "…" weight = … … +++` frontmatter    |
| Homepage              | `index.md` with body H1                     | `index.md` with frontmatter + `[cascade] type`    |
| Quadrant landing page | Not present                                 | `_index.md` per quadrant with fixed section weight|
| Internal link form    | `tutorials/foo.html`, `.../index.html`      | `tutorials/foo/` (directory-form pretty URL)      |
| Exercise bundles      | `uv run diataxis build` → `_build/exercises`| `make exercises` → `static/exercises/<stem>/`     |

`diataxis.toml` itself is structurally unchanged between the two eras.
`scores.toml` is unchanged as well. Neither is migrated.

## What the upgrade script does

Running `python skill/scripts/upgrade_to_hugo.py <diataxis_dir>`:

1. **Scaffolds publishing config** from `skill/templates/`. `hugo.toml` gets
   `{{PROJECT_NAME}}` and `{{PROJECT_DESCRIPTION}}` filled in from
   `[project]` in `diataxis.toml`; `go.mod` gets a
   `diataxis.local/<slug>` module path. Any file that already exists is
   left untouched — these templates become user-owned at scaffold time.
2. **Adds frontmatter to every quadrant content file** listed in
   `diataxis.toml`. The title is taken from the body H1 when present,
   else derived from the file stem. Weight is
   `topic.order * 10 + quadrant_weight` (explanation=1, tutorials=2,
   howto=3, reference=4). `topic`, `covers`, and `detail` are copied from
   the matching `diataxis.toml` entry; `description` is the parent topic's
   `description`.
3. **Strips the body H1** after capturing it as the title. Hugo themes
   render the title from frontmatter; a surviving body H1 would produce a
   duplicate heading.
4. **Rewrites Markdown links** whose targets end in `.html` or
   `/index.html` to Hugo's pretty-URL directory form. External links,
   anchors, and absolute paths are left alone.
5. **Upgrades the homepage** (`index.md`) if it exists and has no
   frontmatter: prepends `title`, `description`, and a `[cascade]` table
   setting `type = "docs"` so every child page inherits the theme's docs
   layout.
6. **Creates `_index.md`** in every quadrant directory that is missing
   one. Each landing page carries the canonical section weight
   (explanation=10, tutorials=20, howto=30, reference=40), a short
   introduction describing the quadrant, and a bulleted list of links to
   every content file in that quadrant sorted by weight.
7. **Flags `diataxis.toml` guidance** that references retired tools
   (`pandoc`, `mmdc`, `uv run diataxis build`, `_build/`). These are
   reported in the script's output but **not** rewritten — guidance
   encodes the author's editorial intent and must be updated through the
   skill's revision workflow (re-run the structure step, integrate the
   updated direction into the `guidance` field, then regenerate).

The script is idempotent. Re-running it on a directory that has already
been upgraded is a no-op. Files with existing frontmatter are never
rewritten; existing publishing-config files are never overwritten.

## What the upgrade does not do

- **Rewrite `guidance` text.** Retired-tool references are surfaced in the
  report so a human (or the skill on a subsequent pass) can integrate the
  new direction — typically by following Step 5 of the workflow: update
  guidance, then regenerate the affected file.
- **Add exercise sections.** If a tutorial in `diataxis.toml` lists
  `exercises` but the body has no `## Exercises` section, the script
  leaves the body alone. Exercise authoring is part of content generation,
  not the mechanical migration.
- **Touch `scores.toml`.** The scoring schema has not changed. Prior runs
  are preserved as historical records; the next scoring pass will append
  a new entry.
- **Renormalize `diataxis.toml`.** The upgrade script reads
  `diataxis.toml` but does not modify it. If the file fails
  `nu checks/check-toml-structure.nu`, fix it first — the upgrade needs a
  valid structure document to map files to metadata.

## After the upgrade — verify

1. Run `nu checks/run-checks.nu <diataxis_dir>`. Every structural check
   should pass: quadrant landing pages are present with canonical weights,
   cross-links use the directory form, frontmatter-based title lookups
   succeed.
2. Run `make build` (or `hugo` directly from inside `diataxis/`). The
   site should build with no errors. Inspect `public/` to confirm the
   section order renders Explanation → Tutorials → How-to → Reference.
3. Review the retired-tool report from the script. For each flagged
   guidance field, update `diataxis.toml` through the skill's revision
   workflow (integrate the change into the existing `guidance` text; do
   not append a labeled feedback block), then regenerate the affected
   files.
4. Regenerate any tutorial whose `diataxis.toml` entry lists `exercises`
   but whose body has no `## Exercises` section. The skill's content
   generation step appends these links; the upgrade does not.

## Rollback

The script edits files in place and does not snapshot. Before running it,
commit the pre-Hugo state (or stage it with `git add`) so `git restore .`
can revert the working tree. For a project that is not already under
version control, copy the directory aside first.
