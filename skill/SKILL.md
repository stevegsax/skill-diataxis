---
name: diataxis
description: >
  ALWAYS use this skill if the user requests diataxis documentation. This includes
  creating, updating, reviewing, scoring, or publishing diataxis-structured content.
allowed-tools:
  - Bash(nu checks/run-checks.nu *)
  - Bash(nu checks/check-toml-structure.nu *)
  - Bash(python skill/scripts/upgrade_to_hugo.py *)
---

# Diataxis Documentation Skill

This skill manages documentation projects structured around the Diataxis framework.
It handles the full lifecycle: scoping, structuring, authoring, scoring, revising,
and publishing.

## Core Concepts

Diataxis organizes documentation into four quadrants based on two axes:

|                        | Acquisition (study) | Application (work) |
|------------------------|--------------------|--------------------|
| **Action** (doing)     | Tutorial           | How-to Guide       |
| **Cognition** (thinking) | Explanation       | Reference          |

Each quadrant serves a different user need and has strict rules about what belongs
in it. The power of Diataxis comes from keeping these quadrants distinct — content
that bleeds across boundaries degrades the documentation.

**A fifth, optional section — Exercises — appears** when the project includes
marimo notebooks. It sits alongside the four quadrants as a *showcase* surface:
an index of the project's interactive notebooks, grouped so a reader can find
them without first threading through the tutorials they attach to. Exercises is
conditional by design — a project with no marimo notebooks has no Exercises
section, and the top-level nav correctly reflects that. See "Exercises (optional
fifth section)" below for the full rule.

**Presentation order**: the published site presents the quadrants as
**Explanation → Tutorials → How-to Guides → Reference**, with **Exercises**
appended at the end when the project has marimo notebooks. Explanation comes
first so readers encounter the conceptual framing before the mechanics.
Tutorials and How-to guides follow for readers ready to act. Reference sits
after them as the lookup surface. Exercises, when present, comes last: it is
a browsing aid for readers who want to see the thing working before or after
committing to a tutorial. This ordering is enforced by the reviewer
(`nu checks/run-checks.nu`) via `_index.md` section weights.

Read `references/quadrants.md` for the detailed rules governing each quadrant
type, including the Exercises section.

### Exercises (optional fifth section)

When the project has any marimo notebooks under `exercises/`, create an
`examples/_index.md` landing page with `title = "Exercises"` and
`weight = 50`. Its body is a short introduction plus a bulleted,
topic-grouped list linking to every `/exercises/<stem>/` bundle in the
project. Give each entry a one-line description drawn from the tutorial
that owns it (its `covers` and `description`), so the landing page reads
as an answer to "what can I play with here?" rather than a raw directory
listing. The source directory stays named `examples/` (to avoid colliding
with the `exercises/*.py` source tree) while the nav label the reader
sees is "Exercises", matching the content type.

Two rules keep the section honest:

- **Conditional existence.** No `exercises/*.py` files → no `_index.md`
  under `examples/`, no top-nav entry. The reviewer treats the absence
  as correct in that case. This is why the Hugo mount for `examples/`
  is always present in `hugo.toml` but the landing page is not: an empty
  mounted directory does not render a section.
- **No separate per-example content files.** The marimo WASM bundles at
  `/exercises/<stem>/` are the content. The Exercises section is an index
  page, not a duplicate of the notebooks. Do not author
  `examples/<stem>.md` files — they would diverge from the notebooks and
  the tutorials, and the skill would have no way to keep all three in
  sync.

When a tutorial's `exercises` list changes (a new entry added, an old one
removed or renamed), regenerate `examples/_index.md` in the same change so
the landing page does not drift from reality.

## Relationship to Other Documentation

Diataxis documentation exists alongside — not instead of — any other project
documentation. A project may have technical specs, API docs generated from code,
architecture decision records, READMEs, or design documents. Those remain the
authoritative sources for development and design.

Diataxis documentation is a human-friendly output artifact derived from the
system. It teaches, guides, describes, and explains — but it is never the source
of truth for how the system works or how it should be built. If the code and the
Diataxis docs disagree, the code is right and the Diataxis docs need updating.

This output-only nature is why Diataxis content lives in its own `diataxis/`
directory. It is strictly an endpoint — produced for human consumption, never
consumed as input by any other process. No build step, CI pipeline, code
generator, or other tool should read from `diataxis/` as a source. Do not move,
replace, or consolidate existing developer documentation into the Diataxis
structure. The `diataxis/` directory is additive.

## Workflow

Every interaction with this skill follows this sequence. Steps can be skipped if
the user has already completed them, but the order matters.

### Step 1: Scope with Grill-Me

Before doing any work, invoke the `/grill-me` skill to clarify what the user wants.
This happens every time — even if the request seems clear. The goal is to establish:

- **Subject and audience**: What are we documenting, and for whom?
- **Depth**: Overview? Deep dive? Learning path with exercises?
- **Boundaries**: What's in scope and what's explicitly out?
- **Type**: Is this project documentation (documenting a codebase) or a learning
  path (teaching a subject)?
- **Prerequisites**: What does the audience already know?

If the user wants to move quickly, a single round of grill-me is fine. But the
scoping must happen — it directly shapes the structure document that drives
everything else.

For learning path requests ("help me learn X"), explore:
- What's their current level?
- What do they want to be able to do after?
- Do they want exercises? Interactive components?
- Any specific areas of focus or areas to skip?

### Step 2: Create or Update the Structure Document

The structure document (`diataxis.toml`) is the source of truth for the entire
project. All Diataxis content — the TOML file, all markdown files, exercises,
and build output — lives under `project-root/diataxis/`. The directory name is
always `diataxis`, not `docs` or any other name. This matters because the
published Hugo site builds against this directory. Do not create documentation
files in `docs/`, `documentation/`, or any other directory.

Read `references/structure-schema.md` for the full TOML schema.

**Detect the project state first.** Before touching anything, figure out which
of three states the target `diataxis/` directory is in — the path branches
from here:

1. **Absent or empty** — no `diataxis/` directory, or one that contains no
   `diataxis.toml`. This is a new project. Skip ahead to "Scaffolding a new
   project" below.
2. **Pre-Hugo format, or ported from another publishing tool** — a
   `diataxis/` directory authored under an earlier version of this skill,
   or imported from Jekyll, MkDocs, Docusaurus, GitBook, Sphinx, or
   similar. You will see one or more of: no `hugo.toml` alongside
   `diataxis.toml`; no `Makefile` or `go.mod`; quadrant markdown files
   that start with an ATX H1 (`# Title`) instead of a `+++`-delimited
   frontmatter block; no `_index.md` inside any quadrant directory;
   a stray `index.md` inside any quadrant directory (see "`_index.md` vs
   `index.md`" below); internal links targeting `.html` files.
   **Upgrade it before doing any other work** — see the next subsection.
3. **Current Hugo format** — `hugo.toml` is present, quadrant files begin
   with `+++` frontmatter, and each quadrant directory has an `_index.md`.
   Proceed with the normal add/update flow below.

Confirm the state by running the detection pass — it is fast and
deterministic:

```bash
python skill/scripts/upgrade_to_hugo.py <diataxis_dir> --check
```

Exit status `1` means a pre-Hugo project was detected; `0` means the
directory is already Hugo-format (or brand new).

**Upgrading a pre-Hugo project**: when detection reports a pre-Hugo
project, run the upgrade script before generating, scoring, or revising
any content:

```bash
python skill/scripts/upgrade_to_hugo.py <diataxis_dir>
```

The script is idempotent and only touches files that need migrating. It
scaffolds `hugo.toml`/`Makefile`/`go.mod` if missing, prepends TOML
frontmatter to every quadrant markdown file (title from the file's body
H1, weight from `topic.order * 10 + quadrant_weight`, `topic`/`covers`/
`detail` from the matching `diataxis.toml` entry), drops the body H1,
rewrites `.html` links to Hugo pretty-URL directory form, adds a
`[cascade]` table to `index.md`, renames stray `<quadrant>/index.md`
files to `_index.md` (preserving the body and adding frontmatter if
missing), and creates the four `_index.md` quadrant landing pages with
canonical section weights. Read `references/hugo-migration.md` for the
full catalog of what the upgrade does and does not do.

**`_index.md` vs `index.md`.** Hugo treats a section directory that
contains `index.md` (no underscore) as a *leaf bundle* — one page plus
attachments — and silently hides every other file in the directory. So
`tutorials/index.md`, the convention in Jekyll, MkDocs, Docusaurus, and
most wiki-style tools, will break the Tutorials section: every tutorial
file on disk stops appearing on the section page. The landing page in
a Hugo section must be `_index.md` (with the underscore). The upgrade
script detects stray `<quadrant>/index.md` files and renames them. The
rule only applies to subdirectories; the root `diataxis/index.md` is
correct — `hugo.toml` mounts it to `content/_index.md` at build time.

After the script finishes, do two things before you continue:

1. Read the retired-tool report it printed. `guidance` fields that
   mention `pandoc`, `mmdc`, `uv run diataxis build`, or
   `diataxis/_build/` need to be reworked through the skill's revision
   workflow (Step 5): integrate the new direction into the existing
   guidance text, then regenerate the affected file. Do not rewrite
   those guidance fields silently — the author's intent is encoded
   there, and the skill's feedback-integration rule still applies.
2. Run `nu checks/run-checks.nu <diataxis_dir>`. Every structural check
   should pass. If any fail, fix the underlying file and re-run — do
   not re-run the upgrade script expecting different output; it is
   idempotent and will not revisit files it already upgraded.

The structure document defines:
- Project metadata (name, audience, type)
- Topics, organized hierarchically
- For each topic and quadrant: the file path, what it covers, level of detail,
  and guidance notes for generation and scoring
- Exercise linkages (marimo notebooks)
- Status tracking per file

**Creating the initial structure**: After scoping, draft the `diataxis.toml` and
present it to the user for approval. Explain the topic decomposition and why you
organized it this way. The user should approve or adjust before any content is
generated.

**Validating the structure**: After writing or modifying `diataxis.toml`, run
the structural check immediately — do not hand-roll Python or `jq` invocations
to spot-check the file:

```bash
nu checks/check-toml-structure.nu <diataxis_dir>
```

This validates the file against `skill/assets/diataxis-schema.json` (a JSON
Schema) using `check-jsonschema`. It catches missing required fields, bad enum
values (`status`, `complexity`, `type`), unknown keys, malformed slugs, TOML
syntax errors, and labeled `REVISION FEEDBACK:` blocks in `guidance` in one
deterministic pass. If it fails, the output gives you the exact JSON path and
an actionable suggestion — fix the file and re-run until it passes before
asking the user to review the structure.

**Scaffolding a new project**: When creating a `diataxis/` directory for the
first time, do all of the following:

1. Create `diataxis/README.md` with this content:

```
# Diataxis Documentation

This directory contains human-facing documentation generated using the
Diataxis framework. It is an output artifact — not a source of truth.

These files are disposable and can be regenerated from the project's
actual source code, specs, and design documents. Do not use files in
this directory as input for design decisions, code generation, build
processes, or CI pipelines.

For the authoritative project documentation, see the project root.
```

2. Append a note to the project's `CLAUDE.md` (create the file if it does not
   exist). Before appending, check whether the note is already present to
   avoid duplicates. The note:

```
## Diataxis Documentation

The `diataxis/` directory contains generated, human-facing documentation.
It is an output artifact — disposable and never authoritative. Do not
use it as input for design decisions, code generation, or development
work. If the code and the diataxis docs disagree, the code is right.
```

3. Copy the publishing scaffolds from `skill/templates/` into the `diataxis/`
   directory so the user can run `make build` as soon as content is generated:
   - `skill/templates/Makefile` → `diataxis/Makefile` (no substitution)
   - `skill/templates/hugo.toml` → `diataxis/hugo.toml`; replace
     `{{PROJECT_NAME}}` and `{{PROJECT_DESCRIPTION}}` with the values from
     `[project]` in the structure document
   - `skill/templates/go.mod` → `diataxis/go.mod`; replace `{{MODULE_PATH}}`
     with `diataxis.local/<project-slug>` where the slug is the lowercased
     project name with non-alphanumeric runs collapsed to hyphens

   These are publishing config — user-owned from the first build onward. Once
   scaffolded, the skill must not rewrite them. If a file already exists at
   the target path, skip it.

4. Create an empty `diataxis/examples/` directory alongside the four
   quadrant directories. The mount for `examples/` in `hugo.toml` is
   always declared (so a project can add exercises later without editing
   config), and Hugo logs a warning if that mount points at a nonexistent
   source. An empty directory — with or without an `_index.md` inside —
   silences the warning and lets the presence of `_index.md` alone
   control whether the Exercises section renders. Adding the
   `_index.md` itself is Step 3's job, gated on whether the project has
   any `exercises/*.py`.

**Updating structure**: When the user asks to add, remove, or reorganize content,
update `diataxis.toml` first. Then update the affected files. The structure
document is always updated before the content files — never the other way around.

**Capturing revision intent**: When the user requests a specific content change
(e.g., "make this section simpler", "add more detail about X", "don't use that
analogy"), update the `guidance` field in `diataxis.toml` for the affected file(s)
to reflect this feedback before making the content change. Integrate the feedback
into the existing guidance text — rewrite the guidance so it reads as a coherent
whole that incorporates the new direction. Do not append the feedback as a
separate labeled block (e.g., don't add a "REVISION FEEDBACK:" section). The
guidance should always read as if it were written from scratch with full knowledge
of all feedback received so far. This prevents regressions — if the file is
regenerated or revised later, the guidance carries forward the user's intent.
Without this step, a future revision might undo the user's requested change
because nothing in the structure document recorded it.

### Step 3: Generate Content

Once the structure is approved, generate content for each file according to its
entry in `diataxis.toml`. The `covers`, `detail`, and `guidance` fields in the
structure document are the brief for each file.

**Introductory page**: Every Diataxis project gets an introductory page at
`diataxis/index.md`. This is the first thing a reader sees, so it needs to
answer two questions immediately: why does this project exist (what problems
does it solve), and what does it do? Draw on the `purpose` and `description`
fields from `diataxis.toml` for this content. Keep it concise — a few short
paragraphs at most. The introductory page is a signpost, not a destination.
It should link into the documentation (tutorials for getting started, explanation
for deeper understanding, reference for specifics) rather than providing detailed
explanations itself. A reader should leave the introductory page knowing whether
this project is relevant to them and where to go next.

Include a `## Sections` list on the homepage that links to every top-level
section: the four quadrant landing pages (`tutorials/`, `howto/`,
`reference/`, `explanation/`) and — when the project has any
`exercises/*.py` notebooks — the Exercises landing page (`examples/`).
The homepage list mirrors the sidebar nav; omitting Exercises when
notebooks exist leaves the main landing page out of sync with the
sidebar and hides the gallery from readers who arrive via the home
page. Use the same Hugo directory-form URLs as the sidebar
(`tutorials/`, not `tutorials/_index.md`).

**Parallel generation**: Because each file's requirements are fully specified in
the structure document, files can be generated independently and in parallel.
When spawning subagents for generation, provide each one with:
1. The full `diataxis.toml` (for cross-linking context)
2. The specific topic and quadrant they're responsible for
3. The quadrant rules from `references/quadrants.md`

**Quadrant rules are non-negotiable during generation**:
- Explanation: discuss why, make connections, provide context
- Tutorials: guide action, show results at every step, minimize explanation
- How-to guides: task-focused, no teaching, assume competence
- Reference: describe only, mirror product structure, use tables

**Cross-linking**: Every file should link to its sibling quadrant docs. A
tutorial should link to the relevant explanation and reference. A how-to
should link to reference. Link targets use Hugo pretty-URL directory form
(`/tutorials/first-project/`, never `.md` or `.html`).

The resolution rules are **not intuitive** because Hugo publishes
`tutorials/foo.md` at the URL `/tutorials/foo/` (one level deeper than
the source file), and the browser resolves every relative link against
that trailing-slash URL per RFC 3986. Writing cross-quadrant links
"the way the source tree looks" produces 404s. The guidance below gets
it right; `references/link-resolution.md` explains why.

**Prefer absolute paths for cross-quadrant links.** Because `hugo.toml`
sets `relativeURLs = true`, Hugo rewrites absolute URLs to the correct
form for each page at build time. Authors who use `/explanation/foo/`
do not need to count `../` segments at all, and the output is correct
everywhere.

Link patterns by source file location:

| Source file                    | Same-quadrant sibling | Cross-quadrant target                                     | Exercise bundle   |
|--------------------------------|-----------------------|-----------------------------------------------------------|-------------------|
| `tutorials/foo.md` (etc.)      | `../bar/`             | `/explanation/bar/` (preferred) or `../../explanation/bar/` | `/exercises/bar/` |
| `<quadrant>/_index.md`         | `bar/`                | `/explanation/bar/` (preferred) or `../explanation/bar/`  | `/exercises/bar/` |
| `index.md` (site homepage)     | —                     | `tutorials/bar/`, `explanation/bar/`, etc.                | `exercises/bar/`  |

Three patterns that look right but are wrong, in every content file:

- `](../explanation/bar/)` from a tutorial — resolves to
  `/tutorials/explanation/bar/`, not `/explanation/bar/`. Cross-quadrant
  links from content files need two `../`, or an absolute path.
- `](bar/)` with no `../` — resolves inside the current page's URL
  (`/tutorials/foo/bar/`). Same-quadrant siblings always need `../`.
- `](../tutorials/bar/)` from a tutorial — resolves to
  `/tutorials/tutorials/bar/`. Same-quadrant links must not repeat the
  quadrant name; use `../bar/`.

The `check-link-form` deterministic check catches these two patterns
(`](../<same-quadrant>/…)` and `](../<other-quadrant>/…)` inside
content files) before build. If a subagent generates links and you are
about to score or build, run `nu checks/run-checks.nu <diataxis_dir>`
first — link-form failures name file and line so they are cheap to
fix.

**Hugo frontmatter**: Every generated markdown file starts with a TOML
frontmatter block (`+++` delimiters) containing at least `title`, `weight`,
and `description`, plus `topic`, `covers`, and `detail` as page params
derived from the matching `diataxis.toml` entry. Do not repeat the title as
an `# H1` heading in the body — the Hugo theme renders the title from
frontmatter, and a body H1 produces a duplicate. Compute `weight` as
`topic.order * 10 + quadrant_weight`, where quadrant_weight is 1 for
explanation, 2 for tutorials, 3 for howto, 4 for reference. This matches
the presentation order (Explanation → Tutorials → How-to → Reference)
and groups content by topic within each section. Example frontmatter for
the first tutorial in the first topic:

```toml
+++
title = "Your First Project"
weight = 12
description = "First steps with the Widget library"
topic = "getting-started"
covers = ["Installing the library", "Creating a first widget"]
detail = "Step-by-step with code examples."
+++
```

**Homepage frontmatter**: `diataxis/index.md` gets `title`, `description`,
and a `[cascade]` table setting `type = "docs"` so every child page inherits
the theme's docs layout (relevant to Hextra and similar themes).

**Quadrant landing pages**: Each of the four quadrant directories gets an
`_index.md` that acts as the section landing page. These pages enforce the
presentation order and give readers an orientation before they drill into a
specific file. Create one per quadrant with this exact shape:

- Frontmatter with `title`, `description`, and a fixed `weight` that pins the
  section order: **explanation = 10, tutorials = 20, howto = 30,
  reference = 40**, plus **examples = 50** on projects that have marimo
  exercises (see "Exercises landing page" below). These weights match the
  presentation order the skill requires; the reviewer fails if any are
  missing or out of order.
- A short introductory paragraph (2-4 sentences) explaining what this
  quadrant is and when a reader should consult it. Write this for a reader
  who has landed on the section page and is deciding whether to stay.
- A bulleted list of links to every content file in that quadrant, each with
  a one-line description of what the page covers. Use the Hugo pretty-URL
  directory form (`filename/`), not `filename.md`. Order the list by the
  content file's `weight` so the landing page mirrors the in-section
  ordering.

Example for the explanation quadrant:

```markdown
+++
title = "Explanation"
weight = 10
description = "Background, context, and deeper understanding."
+++
Explanation documents discuss the why — the reasoning, design rationale,
and trade-offs behind the project. Read these to deepen understanding,
not to accomplish a task.

- [The Diataxis Framework](diataxis-framework/) — what Diataxis is, the
  two axes that produce the four quadrants, and why the boundaries
  improve documentation quality.
- [Why Structure First](why-structure-first/) — why `diataxis.toml` is
  updated before any content change, and how the `guidance` field
  prevents revision regressions.
```

When a content file is added, removed, or renamed, update the corresponding
quadrant `_index.md` in the same change so the link list does not drift.

**Exercises landing page**: When the project has any marimo notebooks under
`exercises/`, author `examples/_index.md` so the fifth top-level section
appears in the nav. Skip this file entirely when no exercises exist —
adding it to an exerciseless project creates a phantom section that
disappoints the reader who clicks into it. Shape:

- Frontmatter with `title = "Exercises"`, `weight = 50`, and a
  `description` explaining the section in one line. No `type` override —
  the landing page is a normal content page, not a leaf bundle.
- A short introductory paragraph (2-4 sentences) framing what the section
  is: an index of interactive notebooks the reader can run in their
  browser. Make clear that each link opens a standalone WASM page and
  that the full tutorial context lives in the matching tutorial.
- One bulleted list per topic, with a topic heading (`### <Topic Title>`)
  preceding each list. Within a topic, order exercises by the tutorial's
  `weight`, then by file name. Each list item is
  `- [<tutorial title>](/exercises/<stem>/) — <one-line description>`.
  Draw the description from the tutorial's `description` field in
  `diataxis.toml`, narrowed to what the reader will actually *do* in
  the notebook (not what the tutorial as a whole teaches).
- Absolute URLs (`/exercises/<stem>/`) because the source file lives at
  `examples/_index.md` and the relative form would be brittle.

Example skeleton, for a project whose exercises cover two topics:

```markdown
+++
title = "Exercises"
weight = 50
description = "Interactive notebooks you can run in your browser."
+++
Every notebook below is a self-contained Pyodide bundle — no install,
no server. Click through to play with the concept; the matching
tutorial explains what it teaches and when to reach for it.

### Getting Started

- [Build Your First Project](/exercises/build-your-first-project/) —
  scaffold a `diataxis.toml` interactively and watch the structure
  update as you edit.

### Authoring Content

- [Drafting Quadrant Files](/exercises/drafting-quadrant-files/) —
  classify sample paragraphs and see immediate feedback on quadrant
  fit.
```

Regenerate this file whenever an `exercises` list anywhere in
`diataxis.toml` is added, removed, or renamed. The landing page is the
project-wide view — a change in one topic's exercises still requires
refreshing it.

**Exercises linking**: When a `diataxis.toml` entry lists exercises, append
an `## Exercises` section at the end of the generated markdown with links
to each exercise's standalone page (`/exercises/<stem>/`). The exercise stem
is the file name without the `.py` extension. These bundles are produced by
`make exercises` and served as standalone pages with their own look and feel.
Both authoring paths are deliberate: inline links keep the exercise adjacent
to the tutorial that sets it up, while the Exercises landing page (above)
gives readers a project-wide index that does not require picking the right
tutorial first.

**Math notation**: All mathematical expressions must use LaTeX notation.
Use `\(...\)` for inline math and `\[...\]` for display math. These are
LaTeX's canonical delimiters and do not collide with literal dollar
signs in prose. The Hugo theme renders them at build time (KaTeX in the
default Hextra theme).

The TeX-derived `$...$` / `$$...$$` form that most other static-site
generators use (and that an earlier version of this skill accepted) is
also rendered by KaTeX, but the skill canonicalizes on the backslash
form for authoring. When `upgrade_to_hugo.py` runs on a project
imported from the old pipeline or from Jekyll, MkDocs, Docusaurus,
etc., it rewrites dollar-delimited math to the backslash form; new
content should be written that way from the start.

Never write math as plain text like `3/4 + 1/2` when it can be
expressed as `\(\frac{3}{4} + \frac{1}{2}\)`.

**Diagrams**: Use mermaid format for all diagrams (flowcharts, sequence diagrams,
entity-relationship diagrams, etc.). Write them as fenced code blocks with the
`mermaid` language tag in the markdown source. The Hugo theme renders them
client-side at view time.

**Exercises**: For tutorials in learning-path projects, create marimo `.py`
notebooks under `diataxis/exercises/`. Every exercise listed in a
tutorial's `exercises = [...]` entry in `diataxis.toml` must exist as a
real, interactive notebook — placeholder stubs (one cell, `# TODO`
bodies, bare `pass`) are not acceptable. If a tutorial lists an
exercise, authoring the notebook is part of that tutorial's generation
task, not a follow-up. A subagent generating `tutorials/foo.md` with
`exercises = ["exercises/foo-practice.py"]` must produce both files
before the task is done.

Read `references/exercises.md` for the shape of a real exercise — at
minimum, a setup cell plus a UI cell plus a response cell that reads
the UI's value and renders something based on it. The deterministic
checks `check-exercise-exists` and `check-exercise-content` enforce
existence and non-placeholder content; both run during scoring.

The Makefile exports each notebook to a self-contained WASM HTML
bundle (via `marimo export html-wasm`) at
`diataxis/static/exercises/<stem>/` that runs in the browser via
Pyodide — no marimo server is required to view the published output.
Every imported package must be Pyodide-compatible; when in doubt,
stick to the standard library.

**Deterministic transforms**: When a task is purely mechanical (converting markdown
to HTML, formatting tables, validating structure), use the appropriate tool — not
LLM generation. Specifically:
- Markdown to HTML: `hugo` (via `make build`)
- HTML tidying: `tidy` or `htmlq`
- Validating `diataxis.toml` structure: `nu checks/check-toml-structure.nu <dir>` (do not write ad-hoc Python or `jq` scripts for this — the check is pre-approved and covers required fields, enums, and syntax in one pass)
- Markdown linting: `textlint`
- XML transforms: `xmlstarlet`

### Step 4: Score the Documentation

**Every scoring pass starts fresh.** This rule is load-bearing — skip it and
scoring becomes theater. When the user asks for a score:

1. Re-run `nu checks/run-checks.nu <diataxis_dir>`. Do this even if you
   already ran it earlier in the same conversation. Files may have changed
   since. The runner embeds a current timestamp in its output — that
   timestamp is how you prove to yourself (and to the user) that the
   result reflects the state of the files right now, not an old run.
2. Re-read every file you intend to score. Do not rely on your memory
   of a file from earlier in the conversation, and never substitute
   recollection for reading. Files change; your recollection does not.
3. Score against `diataxis.toml` as it exists right now. The `covers`,
   `detail`, and `guidance` fields may also have changed, and they are
   the rubric.
4. Only after you have produced a complete fresh set of scores should
   you open `scores.toml` to compare. Previous entries exist for
   comparison only — never as a source to copy scores from. Copying
   forward makes the delta zero by construction and the feature provides
   no signal: the user asked for a score because they want to know the
   current state of the documentation, not a recap of the last pass.

Scoring has two phases: deterministic checks, then qualitative LLM evaluation.

**Phase 1: Deterministic checks.** Run the check suite before qualitative
scoring:

```bash
nu checks/run-checks.nu <diataxis_dir>
```

This outputs JSON with pass/fail/skip/error results for structural, format,
quadrant rule, and cross-linking checks. If any checks fail, present the
failures and their suggestions to the user and wait for direction before
proceeding to Phase 2. The user may ask you to fix issues, or they may say
"score anyway." Do not proceed to qualitative scoring silently when checks fail.

**Exercise-check failures are a deterministic remediation, not a user
decision.** When `check-exercise-exists` or `check-exercise-content`
fail, the cause is that the skill's generation step listed an exercise
in `diataxis.toml` but did not produce the corresponding marimo file
(or produced a placeholder stub). The fix is the same as writing the
exercise in the first place: read the tutorial's `covers`, `detail`,
and `guidance`, then author a real interactive notebook per
`references/exercises.md`. Do this in the scoring follow-up rather
than presenting it as a choice — the user asked for a score; giving
them a list of missing exercises they need to approve generating is
making them do the skill's job. Generate the missing notebooks, then
re-run the checks, then proceed with scoring. If an entry in the
`exercises` list is outdated and the user no longer wants an exercise
there, they will tell you — treat that as feedback and update
`diataxis.toml`.

**Phase 2: Qualitative scoring.** Once deterministic checks pass (or the user
explicitly says to continue), evaluate the documentation qualitatively.

Read `references/scoring.md` for the full scoring rubric and output format.

**Scoring mindset**: You are the same model that generated this content. That
makes you a biased grader — you will read your own prose as clearer and
tighter than it actually is. Counteract this by adopting the stance of a
skeptical editor, not a supportive colleague. Assume every paragraph has fat
to trim. A paragraph that "works fine" is a 3, not a 4. Reserve high scores
for prose you cannot improve. When in doubt, score lower and explain what
would earn a higher score — that gives the user actionable direction.

Scoring operates at four levels:

**Project level**: Is the topic decomposition sound? Are the four quadrants
represented appropriately? Are there gaps or redundancies?

**Structural level**: Does each file match what `diataxis.toml` says it should
contain? Coverage completeness, detail level, guidance adherence.

**Quadrant level**: Does each file follow the rules for its quadrant type?
Cross-contamination detection (tutorial that explains, reference that instructs).

**Prose quality**: Is the writing tight, direct, and active? Check every file
for fluff, passive voice, vague claims, and sentences that can be cut without
losing meaning. See the Prose Quality Scoring section in `references/scoring.md`
for the full criteria and calibration examples.

The scoring output is a structured TOML file (`scores.toml`). Each pass
appends a new timestamped `[[runs]]` entry so the user can see whether
changes improved or degraded the documentation over time. Previous entries
are read-only historical records used only for the diff after a fresh pass
has been produced — they are never a source to read scores from, and you
must not populate a new entry by copying values from an earlier one.

### Step 5: Revise

Based on scores and user feedback, revise the documentation:

1. Update `diataxis.toml` if the structure needs to change
2. Regenerate or edit affected files
3. Re-score to verify improvement

The revision cycle is: **structure first, content second, score third**. Always
update the structure document before touching content files. Always score after
making changes.

When the user gives feedback like "add more exercises about X" or "this is too
hard, add introductory material":
1. Identify where in the topic hierarchy the change belongs
2. Update `diataxis.toml` with new or modified entries
3. Generate the new content
4. Re-score the affected sections and the project as a whole

### Step 6: Build

The skill does not build the site — [Hugo](https://gohugo.io/) does. The
`diataxis/` directory is a plain Hugo site: the scaffolded `hugo.toml` mounts
each quadrant into Hugo's content tree, `diataxis.toml` is exposed as a data
file, and marimo WASM bundles live under `static/exercises/`. Presentation is
**theme-driven**, not skill-driven: the default theme is
[Hextra](https://imfing.github.io/hextra/), and users swap it by editing
`hugo.toml`.

Read `references/build-pipeline.md` for the technical details.

Users run the build with `make`, which preprocesses marimo notebooks and
then invokes `hugo`:

```bash
cd diataxis
make build           # export exercises + hugo
make serve           # export exercises + hugo server (live reload)
make exercises       # export exercises only
make clean           # remove public/ and resources/
```

The Makefile exists because Hugo cannot export marimo notebooks on its own;
that is the only preprocessing step. Everything else — markdown rendering,
navigation, styling, math, mermaid, search — is Hugo's job (or the theme's).

The authored markdown files already carry Hugo frontmatter (written during
Step 3), so `hugo` can build the site directly. No staging step, no custom
CLI. A user who prefers not to use `make` can run `hugo` directly inside
`diataxis/` after ensuring exercises are exported.

Marimo notebooks are **standalone pages** at `/exercises/<stem>/`. They bypass
Hugo's theme entirely and keep their own look and feel. Parent tutorials/howtos
link to them via the `## Exercises` section appended during content generation.

Content uses **generic semantic HTML5** only — no skill-specific CSS classes.
Any Hugo theme renders the content correctly.

**Deploying**: the deployable site is `diataxis/public/`. Deploy it using any
Hugo workflow (`hugo deploy`, Netlify, GitHub Pages, rsync, etc.).

## Directory Layout

A Diataxis project looks like this:

```
project-root/
├── README.md
├── src/                           # Project source code, etc.
└── diataxis/                      # All Diataxis content lives here
    ├── diataxis.toml              # Source of truth (editorial)
    ├── hugo.toml                  # Hugo config (user-owned after scaffold)
    ├── go.mod                     # Hugo module manifest (user-owned)
    ├── Makefile                   # `make build`, `make serve` (user-owned)
    ├── README.md                  # Guard file ("this is generated output")
    ├── index.md                   # Homepage (signpost)
    ├── scores.toml                # Scoring history
    ├── tutorials/
    │   └── basic-operations.md    # authored markdown with Hugo frontmatter
    ├── howto/
    │   └── add-fractions.md
    ├── reference/
    │   └── fraction-operations.md
    ├── explanation/
    │   └── why-fractions-work.md
    ├── examples/                  # Hugo section dir for the Exercises nav entry;
    │   │                          # optional — appears only if exercises exist
    │   └── _index.md              # Landing page indexing all marimo notebooks
    ├── exercises/
    │   └── basic-ops.py           # marimo notebook
    ├── static/exercises/          # WASM bundles (generated by `make exercises`)
    └── public/                    # Hugo output — the rendered site
```

The `diataxis/` directory is a plain Hugo site plus `diataxis.toml` as the
editorial source of truth. All paths in `diataxis.toml` are relative to the
`diataxis/` directory. `hugo.toml`, `go.mod`, `Makefile`, and `layouts/` (if
added) are user-owned. Everything else under `diataxis/` is skill-generated
or Hugo-generated output.

## Reference Files

These files contain detailed specifications. Read them when you need the details:

- `references/quadrants.md` — Rules for each Diataxis quadrant (generation + scoring)
- `references/structure-schema.md` — Full `diataxis.toml` schema with all fields
- `references/scoring.md` — Scoring rubric, output format, and comparison logic
- `references/build-pipeline.md` — Build and serve pipeline technical details
- `references/link-resolution.md` — Why cross-quadrant links need two `../` (or absolute), with the per-source-location table
- `references/exercises.md` — What a real marimo exercise looks like (template + guidance), for generation and for remediation when `check-exercise-content` fails
- `references/hugo-migration.md` — Detecting pre-Hugo projects and what the upgrade script does
- `scripts/upgrade_to_hugo.py` — Detect (`--check`) and migrate pre-Hugo projects to the current Hugo format
- `checks/run-checks.nu` — Deterministic check runner (invoke with `nu checks/run-checks.nu <dir>`)
- `checks/check-schema.json` — JSON Schema for individual check output
