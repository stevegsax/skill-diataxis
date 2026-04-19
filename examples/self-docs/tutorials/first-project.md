+++
title = "Your First Diataxis Project"
weight = 11
description = "Installation, first project, and the basic workflow"
topic = "getting-started"
covers = ["Installing prerequisites (uv, Hugo extended, Go)", "Creating a diataxis/ directory and diataxis.toml", "Adding a first topic with a tutorial file", "Building the site with `make build` and viewing it"]
detail = "Step-by-step from an empty directory to a rendered page in the browser. Use a concrete example topic throughout."
+++
In this tutorial, we will create a Diataxis documentation project from scratch,
add a topic with a tutorial, and build it into a browsable Hugo site. Along the
way we will see how `diataxis.toml` drives the content and how Hugo handles the
publishing.

## Prerequisites

You will need:

- `uv` (Python package manager)
- Hugo extended (https://gohugo.io/installation/)
- Go 1.21+ (Hugo uses Go modules to fetch themes)
- `make` (already installed on most Unix systems)
- The `skill-diataxis` project cloned locally

If you don't have these installed, see
[How to Install and Set Up](../howto/install-and-setup/).

## Step 1: Create the project directory

Create a new directory for your project and a `diataxis/` subdirectory inside
it:

```bash
mkdir my-docs-project
cd my-docs-project
mkdir -p diataxis/tutorials
```

You should now have:

```
my-docs-project/
└── diataxis/
    └── tutorials/
```

## Step 2: Create the structure document

Create `diataxis/diataxis.toml` with your project metadata and a first topic:

```toml
[project]
name = "Widget Handbook"
description = "Documentation for the Widget library"
purpose = """Building UIs from scratch means reinventing layout, rendering, and \
event handling every time. The Widget library provides composable building blocks \
so developers can assemble interfaces without writing boilerplate."""
type = "project-docs"
audience = "Developers using the Widget API"

[topics.getting-started]
title = "Getting Started"
description = "First steps with the Widget library"
complexity = "beginner"
order = 1

[topics.getting-started.tutorials]
file = "tutorials/hello-widget.md"
status = "draft"
covers = [
    "Installing the Widget library",
    "Creating your first widget",
    "Rendering a widget to the console",
]
detail = "Step-by-step with code examples. Show output after every step."
guidance = "Use a simple text widget for the first example. Keep it to three steps."
```

The `covers` field is the list of things the tutorial must address. It is also
used later when scoring the documentation.

## Step 3: Add the publishing scaffolds

Copy three files into `diataxis/` from the skill's templates — a `Makefile`,
a `hugo.toml`, and a `go.mod`:

```bash
cp <skill-dir>/skill/templates/Makefile diataxis/
cp <skill-dir>/skill/templates/hugo.toml diataxis/
cp <skill-dir>/skill/templates/go.mod diataxis/
```

Edit `diataxis/hugo.toml` and replace `{{PROJECT_NAME}}` and
`{{PROJECT_DESCRIPTION}}` with your values. Edit `diataxis/go.mod` and
replace `{{MODULE_PATH}}` with a unique module path — for a local project,
`diataxis.local/widget-handbook` is fine.

These three files are yours to edit from here on. The skill will never
rewrite them.

## Step 4: Write the tutorial

Create `diataxis/tutorials/hello-widget.md` with Hugo frontmatter at the top
followed by the tutorial body:

```markdown
+++
title = "Hello Widget"
weight = 11
description = "First steps with the Widget library"
topic = "getting-started"
covers = ["Installing the Widget library", "Creating your first widget", "Rendering a widget to the console"]
detail = "Step-by-step with code examples. Show output after every step."
+++
In this tutorial, we will install the Widget library, create a simple text
widget, and render it to the console.

## Installing the Widget library

Install with pip:

    pip install widget-lib

You should see output ending with:

    Successfully installed widget-lib-1.0.0

## Creating your first widget

Open a Python shell and create a text widget:

    >>> from widget_lib import TextWidget
    >>> w = TextWidget("Hello, world!")
    >>> w
    <TextWidget text='Hello, world!'>

## Rendering a widget to the console

Call the render method:

    >>> w.render()
    ┌─────────────────┐
    │ Hello, world!   │
    └─────────────────┘

You have created and rendered your first widget.
```

Notice the file body has no `# Hello Widget` heading — Hugo's theme renders
the title from the frontmatter, and repeating it in the body would show a
duplicate.

## Step 5: Build the site

From `diataxis/`:

```bash
cd diataxis
make build
```

`make build` does two things: it exports any marimo notebooks to
self-contained WASM bundles under `static/exercises/`, and it runs `hugo`.
You should see something like:

```
hugo --cleanDestinationDir
Start building sites … 
                  │ EN
──────────────────┼─────
 Pages            │   4
 ...
```

The rendered site lands at `diataxis/public/`.

## Step 6: View the result

Start the live-reload Hugo server:

```bash
make serve
```

Open the URL `hugo server` prints (usually `http://localhost:1313`). You
should see your Widget Handbook with the Hextra theme — sidebar navigation
auto-built from your section, dark-mode toggle, search, and a tutorials
section listing "Hello Widget."

Press Ctrl+C to stop the server.

## What you've built

You have created a Diataxis documentation project with:

- A `diataxis.toml` structure document defining one topic
- A tutorial following Diataxis rules (action-oriented, shows results)
- A plain Hugo site with a default theme, a Makefile, and a Go module manifest
- Rendered HTML at `diataxis/public/`, ready to deploy

The `diataxis/` directory is a normal Hugo site. You can swap themes by
editing `hugo.toml`, add layout overrides under `layouts/`, or run `hugo`
directly after `make exercises`. Anything the skill generates (markdown,
marimo notebook sources) lives in the quadrant directories; anything Hugo
generates (`public/`, `resources/`) is gitignored. The publishing scaffolds
(`Makefile`, `hugo.toml`, `go.mod`, `layouts/`) are yours.

To learn more about the structure document, see the
[Writing diataxis.toml](../tutorials/writing-diataxis-toml/) tutorial. For
the full field reference, see the
[diataxis.toml Schema](../reference/diataxis-toml-schema/).

## Exercises

- [Build Your First Project](/exercises/build-your-first-project/)
