import marimo

app = marimo.App()


@app.cell
def intro():
    import marimo as mo

    mo.md("""
    ## Build Your First Project — Exercise

    This exercise walks you through creating a `diataxis.toml` structure
    document. Fill in each section and check your work.
    """)


@app.cell
def step_1():
    import marimo as mo

    project_name = mo.ui.text(
        placeholder="e.g., My Widget Library",
        label="Project name",
    )
    project_type = mo.ui.dropdown(
        options=["project-docs", "learning-path"],
        value="project-docs",
        label="Project type",
    )
    audience = mo.ui.text(
        placeholder="e.g., Python developers",
        label="Audience",
    )

    mo.md(f"""
    ### Step 1: Project metadata

    Every `diataxis.toml` starts with a `[project]` section. Fill in the fields:

    {project_name}
    {project_type}
    {audience}
    """)
    return project_name, project_type, audience


@app.cell
def step_1_result(project_name, project_type, audience):
    import marimo as mo

    if project_name.value and audience.value:
        toml_preview = f"""```toml
[project]
name = "{project_name.value}"
type = "{project_type.value}"
audience = "{audience.value}"
```"""
        mo.md(f"""
        Your `[project]` section:

        {toml_preview}
        """)
    else:
        mo.md("*Fill in the fields above to see the TOML preview.*")


@app.cell
def step_2():
    import marimo as mo

    topic_slug = mo.ui.text(
        placeholder="e.g., getting-started",
        label="Topic slug (lowercase, hyphenated)",
    )
    topic_title = mo.ui.text(
        placeholder="e.g., Getting Started",
        label="Topic title",
    )
    complexity = mo.ui.dropdown(
        options=["beginner", "intermediate", "advanced"],
        value="beginner",
        label="Complexity",
    )

    mo.md(f"""
    ### Step 2: Define a topic

    Topics group related content across quadrants. Define your first topic:

    {topic_slug}
    {topic_title}
    {complexity}
    """)
    return topic_slug, topic_title, complexity


@app.cell
def step_2_result(topic_slug, topic_title, complexity):
    import marimo as mo

    if topic_slug.value and topic_title.value:
        toml_preview = f"""```toml
[topics.{topic_slug.value}]
title = "{topic_title.value}"
complexity = "{complexity.value}"
order = 1
```"""
        mo.md(f"""
        Your topic definition:

        {toml_preview}
        """)
    else:
        mo.md("*Fill in the fields above to see the TOML preview.*")


@app.cell
def step_3():
    import marimo as mo

    covers = mo.ui.text_area(
        placeholder="One item per line, e.g.:\nInstalling the library\nCreating a first widget\nRendering output",
        label="What should the tutorial cover? (one item per line)",
    )
    guidance_text = mo.ui.text_area(
        placeholder="e.g., Use a simple example. Show output after every step.",
        label="Guidance notes for the content author",
    )

    mo.md(f"""
    ### Step 3: Add a tutorial entry

    Define what the tutorial should cover and how:

    {covers}
    {guidance_text}
    """)
    return covers, guidance_text


@app.cell
def step_3_result(topic_slug, covers, guidance_text):
    import marimo as mo

    if topic_slug.value and covers.value:
        items = [line.strip() for line in covers.value.strip().split("\n") if line.strip()]
        covers_toml = ",\n    ".join(f'"{item}"' for item in items)
        guidance_val = guidance_text.value or "Keep it simple."

        toml_preview = f"""```toml
[topics.{topic_slug.value}.tutorials]
file = "tutorials/{topic_slug.value}.md"
status = "planned"
covers = [
    {covers_toml},
]
detail = "Step-by-step walkthrough with visible results after each step."
guidance = \"\"\"{guidance_val}\"\"\"
```"""
        mo.md(f"""
        Your tutorial entry:

        {toml_preview}

        The `covers` list is the scoring contract — each item will be checked
        when evaluating the documentation.
        """)
    else:
        mo.md("*Fill in the fields above to see the TOML preview.*")


if __name__ == "__main__":
    app.run()
