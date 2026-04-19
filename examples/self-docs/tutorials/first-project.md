+++
title = "Your First Diataxis Project"
weight = 12
description = "Installation, first project, and the basic workflow"
topic = "getting-started"
covers = ["Installing prerequisites (uv, Hugo extended, Go)", "Asking the diataxis skill to scaffold a new project", "Reviewing the structure document the skill produces", "Building and viewing the rendered Hugo site", "Asking the skill for revisions"]
detail = "Step-by-step from an empty directory to a rendered page in the browser. Use a concrete example project throughout."
+++
In this tutorial, you will use the Diataxis Documentation Skill to create a
documentation project for an imaginary "Widget" Python library, then build
and view the rendered HTML site. **The skill writes all the files; your
job is to direct it.**

## Prerequisites

You need:

- Claude Code with the diataxis skill installed
- `uv`, Hugo extended, Go 1.21+, and `make` on your `PATH`

If anything is missing, see [How to Install and Set Up](../../howto/install-and-setup/).

You also need an empty directory for the project:

```bash
mkdir my-widget-docs
cd my-widget-docs
```

## Step 1: Ask the skill to scaffold the project

Open Claude Code in `my-widget-docs/` and ask:

> Use the diataxis skill to start a project documenting the Widget Python
> library. The audience is developers using the Widget API. Cover
> installation, basic usage, and reference for the public API.

Claude will:

1. Run `/grill-me` to clarify scope (audience, depth, prerequisites).
2. Draft `diataxis/diataxis.toml` with topics, quadrants, `covers`, and
   `guidance` fields.
3. Show you the structure for approval.
4. Generate the markdown for each entry, with Hugo frontmatter at the top.
5. Scaffold the publishing files (`Makefile`, `hugo.toml`, `go.mod`,
   `README.md`) alongside `diataxis.toml`.

Approve the structure when prompted. The skill writes the files; you
don't type them.

After Claude finishes, your project looks like:

```
my-widget-docs/
└── diataxis/
    ├── diataxis.toml          # editorial structure (drives everything)
    ├── hugo.toml              # Hugo config (yours to edit)
    ├── go.mod
    ├── Makefile
    ├── README.md
    ├── index.md
    ├── tutorials/
    ├── howto/
    ├── reference/
    └── explanation/
```

## Step 2: Review the structure document

Open `diataxis/diataxis.toml`. This is the file you edit (or ask Claude
to edit) when you want to change what the documentation covers. Each
quadrant entry has:

- `file` — where the markdown lives
- `covers` — the list of items the file must address (the scoring contract)
- `detail` — depth and format guidance
- `guidance` — notes for content generation and revision

The markdown files under `tutorials/`, `howto/`, etc. are derived from
these fields. **Hand edits to those markdown files will be overwritten
the next time the skill regenerates content.** Edit `diataxis.toml`
instead, or ask Claude to.

For the full schema, see the
[diataxis.toml Schema](../../reference/diataxis-toml-schema/) reference.

## Step 3: Build the site

From inside `diataxis/`:

```bash
cd diataxis
make build
```

The first build downloads the Hugo theme module (Hextra by default) and
renders the site. You should see something like:

```
hugo --cleanDestinationDir
Start building sites …
                  │ EN
──────────────────┼─────
 Pages            │   8
 Static files     │   0

Total in 200 ms
```

The rendered HTML is at `diataxis/public/`.

## Step 4: View the result

Start the live-reload Hugo server:

```bash
make serve
```

Open the URL `hugo server` prints (usually `http://localhost:1313`). You
should see the Widget documentation with sidebar navigation, search,
dark-mode toggle, and a page for each topic Claude generated.

Press Ctrl+C to stop the server.

## Step 5: Ask the skill for a revision

Suppose the installation how-to is too long. Ask Claude:

> The "Installation" how-to is too detailed for our audience. Simplify it
> to assume the reader knows pip and just needs the install commands.

Claude will:

1. Update the `guidance` field for that entry in `diataxis.toml`,
   integrating the new direction.
2. Regenerate the affected markdown file.
3. Re-score against the rubric.

Run `make build` again to see the change. Because the feedback was
captured in `guidance`, future regenerations of that file will preserve
the direction — it won't quietly revert.

## What you've built

You used the skill to produce a Diataxis documentation project with:

- A `diataxis.toml` structure document defining topics and content briefs
- Authored markdown for each topic and quadrant, written by the skill
- A working Hugo site with sidebar navigation and a default theme
- Rendered HTML at `diataxis/public/`, ready to deploy

The split is:

- **The skill owns** `diataxis.toml`, the markdown under `tutorials/`,
  `howto/`, `reference/`, `explanation/`, and any marimo notebooks.
  Hand-edits to those files get overwritten.
- **You own** `hugo.toml`, `go.mod`, `Makefile`, and anything you add
  under `layouts/`. The skill does not rewrite these after scaffolding.
- **Hugo owns** `public/` and `resources/` (regenerated each build,
  gitignored).

To see how `diataxis.toml` is structured field by field, see
[Writing diataxis.toml](../../tutorials/writing-diataxis-toml/) and
the [diataxis.toml Schema](../../reference/diataxis-toml-schema/) reference.

## Exercises

- [Build Your First Project](/exercises/build-your-first-project/)
