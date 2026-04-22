# Upgrading Pre-Hugo Projects

Earlier versions of this skill shipped a custom Python build pipeline; the
current skill targets a plain Hugo site. The `diataxis.toml` schema has not
changed, but everything around it has. When the skill is pointed at a
project authored under the old pipeline — or at a documentation set
ported from another publishing tool (Jekyll, MkDocs, Docusaurus, GitBook,
Sphinx, etc.) — the quadrant markdown, the homepage, and the publishing
config all need to change shape before any new work — generation,
scoring, or revision — can run.

The mechanical half of that migration is handled by
`skill/scripts/upgrade_to_hugo.py`. This reference explains what the old
projects look like, what the upgrade does (and does not) do, and how to
verify the result.

## The `_index.md` rule

Hugo distinguishes *section* directories (which list their children) from
*leaf bundle* directories (a single page with its attachments) by the
name of the landing file:

- `_index.md` (with the underscore) turns a directory into a **section**.
  Hugo renders its contents and lists every child page.
- `index.md` (no underscore) turns a directory into a **leaf bundle**.
  Hugo renders the page and silently suppresses every other page in the
  same directory — the section listing disappears.

Most other documentation tools (Jekyll, MkDocs, Docusaurus, older
versions of this skill with hand-written landing pages) use `index.md`
as the section landing page. Ported straight across, an imported
`tutorials/index.md` will break the Tutorials section: the individual
tutorials exist on disk and pass link checks, but they will not appear
on the section page and their URLs may not resolve. This is a silent
failure — Hugo does not warn about it — so the upgrade script detects
and fixes it (see below).

The rule only applies to *subdirectories*. At the root of
`diataxis/`, the homepage is authored as `index.md`; `hugo.toml` mounts
it to `content/_index.md` at build time. Do not rename the root
`diataxis/index.md`.

## How to tell you have a pre-Hugo project

Any one of the following is enough to conclude the project predates the
Hugo migration:

- `diataxis/` has no `hugo.toml` alongside `diataxis.toml`.
- `diataxis/` has no `Makefile` or `go.mod`.
- Quadrant markdown files (e.g. `tutorials/first-project.md`) start with an
  ATX H1 (`# Title`) instead of a `+++`-delimited TOML frontmatter block.
- Quadrant directories have no `_index.md` section landing page.
- Any quadrant directory contains an `index.md` (the other-tool convention
  — will silently break the section, see "The `_index.md` rule" above).
- Internal links point at `.html` targets (`tutorials/index.html`) instead
  of Hugo pretty URLs (`tutorials/`).
- Math expressions use `$...$` / `$$...$$` delimiters. The skill
  canonicalizes on the LaTeX `\(...\)` / `\[...\]` form (see the Math
  notation section of SKILL.md); the upgrade rewrites dollar-delimited
  math to the backslash form.
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

| Concern               | Pre-Hugo / other tool                       | Hugo                                              |
|-----------------------|---------------------------------------------|---------------------------------------------------|
| Publishing config     | None (Python CLI)                           | `hugo.toml`, `Makefile`, `go.mod`                 |
| Content file header   | `# Title` body H1                           | `+++ title = "…" weight = … … +++` frontmatter    |
| Homepage              | `index.md` with body H1                     | `index.md` with frontmatter + `[cascade] type`    |
| Quadrant landing page | Missing, or `quadrant/index.md`             | `_index.md` per quadrant with fixed section weight|
| Internal link form    | `tutorials/foo.html`, `.../index.html`      | `tutorials/foo/` (directory-form pretty URL)      |
| Math delimiters       | `$...$` / `$$...$$`                         | `\(...\)` / `\[...\]`                             |
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
6. **Renames stray `<quadrant>/index.md` files** to
   `<quadrant>/_index.md`. If the file already has TOML frontmatter it
   is renamed as-is; if not, canonical section frontmatter is prepended
   (`title` from the first body H1 when present, `weight` set to the
   canonical section weight, `description` set to a short default) and
   the body is preserved with `.html` links rewritten. If both
   `<quadrant>/index.md` and `<quadrant>/_index.md` already exist, the
   script refuses to guess which the user wants to keep — it surfaces
   the collision in the report and leaves both files alone.
7. **Creates `_index.md`** in every quadrant directory that is still
   missing one after the rename step. Each landing page carries the
   canonical section weight (explanation=10, tutorials=20, howto=30,
   reference=40), a short introduction describing the quadrant, and a
   bulleted list of links to every content file in that quadrant
   sorted by weight.
8. **Rewrites math delimiters.** `$...$` becomes `\(...\)` and
   `$$...$$` becomes `\[...\]` everywhere in content bodies. Fenced
   code blocks and inline code are preserved verbatim. Inline dollar
   spans are only converted when the content looks like math — a
   LaTeX command, a sub/superscript, a lone variable, or a short
   expression with math operators — so prose mentions of currency
   ("costs $5 and $10") are not clobbered. Review the diff after
   upgrade; the heuristic is conservative but not infallible, and any
   prose that matched the "looks like math" criteria will need to be
   restored manually. (One common case: a sentence like "the variable
   `$foo` in Bash is …" inside plain prose would be rewritten, but
   the same line written with `` `$foo` `` as inline code would not.)
9. **Flags `diataxis.toml` guidance** that references retired tools
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
- **Resolve `index.md` / `_index.md` collisions.** When both files exist
  in the same quadrant, the script leaves them alone and flags the
  conflict. Delete whichever file is stale (the imported `index.md` is
  usually it), then re-run the upgrade so the remaining file ends up
  correctly named with frontmatter.

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
