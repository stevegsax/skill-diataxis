import marimo

app = marimo.App()


@app.cell
def _setup():
    import marimo as mo
    return (mo,)


@app.cell
def intro(mo):
    mo.md("""
    ## Build Your First Project — Exercise

    This exercise walks you through creating a `diataxis.toml` structure
    document. Fill in each section and check your work.
    """)


@app.cell
def step_1(mo):
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
def step_1_result(mo, project_name, project_type, audience):
    _result = mo.md("*Fill in the fields above to see the TOML preview.*")
    if project_name.value and audience.value:
        _step_1_toml = f"""```toml
[project]
name = "{project_name.value}"
type = "{project_type.value}"
audience = "{audience.value}"
```"""
        _result = mo.md(f"""
        Your `[project]` section:

        {_step_1_toml}
        """)
    _result


@app.cell
def step_2(mo):
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
def step_2_result(mo, topic_slug, topic_title, complexity):
    _result = mo.md("*Fill in the fields above to see the TOML preview.*")
    if topic_slug.value and topic_title.value:
        _step_2_toml = f"""```toml
[topics.{topic_slug.value}]
title = "{topic_title.value}"
complexity = "{complexity.value}"
order = 1
```"""
        _result = mo.md(f"""
        Your topic definition:

        {_step_2_toml}
        """)
    _result


@app.cell
def step_3(mo):
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
def step_3_result(mo, topic_slug, covers, guidance_text):
    _result = mo.md("*Fill in the fields above to see the TOML preview.*")
    if topic_slug.value and covers.value:
        _step_3_items = [line.strip() for line in covers.value.strip().split("\n") if line.strip()]
        _step_3_covers_toml = ",\n    ".join(f'"{item}"' for item in _step_3_items)
        _step_3_guidance = guidance_text.value or "Keep it simple."

        _step_3_toml = f"""```toml
[topics.{topic_slug.value}.tutorials]
file = "tutorials/{topic_slug.value}.md"
status = "planned"
covers = [
    {_step_3_covers_toml},
]
detail = "Step-by-step walkthrough with visible results after each step."
guidance = \"\"\"{_step_3_guidance}\"\"\"
```"""
        _result = mo.md(f"""
        Your tutorial entry:

        {_step_3_toml}

        The `covers` list is the scoring contract — each item will be checked
        when evaluating the documentation.
        """)
    _result


if __name__ == "__main__":
    app.run()
