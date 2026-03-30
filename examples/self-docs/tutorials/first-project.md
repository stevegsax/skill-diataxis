# Your First Diataxis Project

In this tutorial, we will create a Diataxis documentation project from scratch,
add a topic with a tutorial, and build it into a browsable HTML site. Along the
way we will see how `diataxis.toml` drives the entire process.

## Prerequisites

You will need:

- `uv` (Python package manager)
- `pandoc` (document converter)
- The `skill-diataxis` project cloned locally

If you don't have these installed, see
[How to Install and Set Up](../howto/install-and-setup.html).

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

Notice the `covers` field — this is the list of things the tutorial must address.
It will be used later when scoring the documentation.

## Step 3: Write the tutorial

Create `diataxis/tutorials/hello-widget.md`:

```markdown
# Hello Widget

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

## Step 4: Build the HTML

Run the build command from your project root:

```bash
uv run diataxis build
```

You should see:

```
Building from /path/to/my-docs-project/diataxis
Copied standard assets.
Generating landing pages...
Converting markdown to HTML...
  index.md -> index.html
  hello-widget.md -> hello-widget.html
  index.md -> index.html
Build complete: /path/to/my-docs-project/diataxis/_build
```

## Step 5: View the result

Start the local server:

```bash
uv run diataxis serve-only
```

Open `http://localhost:8000` in your browser. You should see your Widget Handbook
with a sidebar showing the Tutorials section and a link to "Getting Started."

Press Ctrl+C to stop the server.

## What you've built

You have created a Diataxis documentation project with:

- A `diataxis.toml` structure document defining one topic
- A tutorial following Diataxis rules (action-oriented, shows results)
- HTML output with navigation and styling

To learn more about the structure document, see the
[Writing diataxis.toml](writing-diataxis-toml.html) tutorial. For the full
field reference, see the
[diataxis.toml Schema](../reference/diataxis-toml-schema.html).
