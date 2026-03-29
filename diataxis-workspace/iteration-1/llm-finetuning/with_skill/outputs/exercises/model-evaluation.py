import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")


@app.cell
def intro():
    import marimo as mo

    mo.md(
        """
        # Model Evaluation Exercise

        This exercise focuses on developing evaluation skills for fine-tuned LLMs.
        You will practice writing evaluation prompts, scoring model outputs, and
        making decisions about whether to iterate on your fine-tuning.
        """
    )
    return (mo,)


@app.cell
def evaluation_prompts():
    import marimo as mo

    mo.md(
        """
        ## Part 1: Designing Evaluation Prompts

        A good evaluation set covers the range of tasks your model should handle.
        The prompts below represent different categories. For each category, you
        will write one additional prompt.
        """
    )

    categories = {
        "Factual Q&A": "What is the difference between TCP and UDP?",
        "Code Generation": "Write a Python function that checks if a number is prime.",
        "Summarization": "Summarize the concept of supply and demand in economics.",
        "Creative": "Write a short metaphor explaining what machine learning is.",
        "Analysis": "What are the pros and cons of microservices architecture?",
    }

    return (categories,)


@app.cell
def prompt_writing(categories):
    import marimo as mo

    editors = {}
    for cat, example in categories.items():
        editors[cat] = mo.ui.text(
            value="",
            placeholder=f"Write a new {cat.lower()} prompt...",
            label=f"New {cat} prompt",
            full_width=True,
        )

    items = []
    for cat, example in categories.items():
        items.append(
            mo.md(
                f"""
                **{cat}** (example: "{example}")

                {editors[cat]}
                """
            )
        )

    mo.md(
        f"""
        ### Write One Prompt Per Category

        {"".join(str(item) for item in items)}
        """
    )
    return (editors,)


@app.cell
def prompt_quality_check(editors, categories):
    import marimo as mo

    filled = sum(1 for e in editors.values() if e.value.strip())
    total = len(editors)

    tips = []
    for cat, editor in editors.items():
        val = editor.value.strip()
        if val:
            if len(val) < 10:
                tips.append(f"- **{cat}**: prompt may be too short to be a meaningful test")
            elif "?" not in val and cat in ("Factual Q&A", "Analysis"):
                tips.append(f"- **{cat}**: consider phrasing as a question")

    tips_text = "\n".join(tips) if tips else "No issues detected."

    mo.md(
        f"""
        ### Prompt Review

        You have written {filled}/{total} prompts.

        {tips_text}

        A complete evaluation set should have at least 3-5 prompts per category
        (20-50 total). For this exercise, one per category demonstrates the approach.
        """
    )
    return ()


@app.cell
def scoring_practice():
    import marimo as mo

    mo.md(
        """
        ## Part 2: Scoring Model Outputs

        Below are three responses to the same prompt from models with different
        amounts of fine-tuning. Score each one.

        **Prompt**: "Explain what a database index is and when you should use one."
        """
    )

    responses = {
        "Model A (base, no fine-tuning)": (
            "Database indexes are a fundamental concept in computer science and "
            "database management systems. The history of database indexing goes back "
            "to the early days of relational databases in the 1970s when E.F. Codd "
            "first proposed the relational model. Since then, various indexing "
            "strategies have been developed including B-trees, hash indexes, and "
            "bitmap indexes. The choice of index type depends on many factors "
            "including the database engine being used, the type of queries being "
            "performed, and the characteristics of the data being stored..."
        ),
        "Model B (fine-tuned, 1 epoch)": (
            "A database index is a data structure that speeds up data retrieval. "
            "Think of it like a book's index — instead of reading every page to "
            "find a topic, you look it up in the index and go directly to the right "
            "page.\n\n"
            "Use an index when:\n"
            "- A column is frequently used in WHERE clauses\n"
            "- You need to speed up JOIN operations\n"
            "- You query a large table and only need a small subset of rows\n\n"
            "Avoid indexes when:\n"
            "- The table is small (full scan is fast enough)\n"
            "- The column has very few unique values\n"
            "- The table is write-heavy (indexes slow down inserts/updates)"
        ),
        "Model C (fine-tuned, 5 epochs, overfit)": (
            "A database index is a data structure that improves the speed of data "
            "retrieval operations on a database table at the cost of additional "
            "writes and storage space to maintain the index data structure. Indexes "
            "are used to quickly locate data without having to search every row in "
            "a database table every time a database table is accessed. A database "
            "index is a data structure that improves the speed of data retrieval "
            "operations on a database table at the cost of additional writes and "
            "storage space."
        ),
    }

    return (responses,)


@app.cell
def score_models(responses):
    import marimo as mo

    scoring_criteria = [
        "Directly answers the question",
        "Accurate and correct information",
        "Well-structured and readable",
        "Appropriate level of detail",
        "No repetition or padding",
    ]

    all_sliders = {}
    for model_name in responses:
        all_sliders[model_name] = mo.ui.array(
            [
                mo.ui.slider(start=0, stop=3, step=1, value=0, label=f"{c}")
                for c in scoring_criteria
            ]
        )

    sections = []
    for model_name, response_text in responses.items():
        sections.append(
            mo.md(
                f"""
                ### {model_name}

                > {response_text}

                {all_sliders[model_name]}
                """
            )
        )

    mo.md("\n".join(str(s) for s in sections))
    return (scoring_criteria, all_sliders)


@app.cell
def score_summary(scoring_criteria, all_sliders, responses):
    import marimo as mo

    model_totals = {}
    for model_name in responses:
        vals = [s.value for s in all_sliders[model_name].value]
        model_totals[model_name] = sum(vals)

    max_possible = len(scoring_criteria) * 3

    rows = []
    for model_name in responses:
        vals = [s.value for s in all_sliders[model_name].value]
        total = sum(vals)
        row_items = " | ".join(str(v) for v in vals)
        rows.append(f"| {model_name} | {row_items} | **{total}/{max_possible}** |")

    header_criteria = " | ".join(c[:15] for c in scoring_criteria)
    table = "\n".join(rows)

    best_model = max(model_totals, key=model_totals.get)

    mo.md(
        f"""
        ### Score Summary

        | Model | {header_criteria} | Total |
        |-------|{'|'.join(['---'] * len(scoring_criteria))}|-------|
        {table}

        **Highest scoring**: {best_model}

        Typical findings:
        - Model A (base) tends to ramble and not follow the instruction format
        - Model B (1 epoch) usually scores highest — clear, structured, on-topic
        - Model C (overfit) often shows repetition and formulaic structure
        """
    )
    return ()


@app.cell
def iteration_decision():
    import marimo as mo

    mo.md(
        """
        ## Part 3: Deciding What to Do Next

        Based on common evaluation patterns, match each observation with the
        correct action.
        """
    )

    scenarios = [
        {
            "observation": "The model gives correct answers but they are too verbose and include unnecessary background.",
            "options": {
                "Add more concise examples to the training data": "correct",
                "Train for more epochs": "wrong",
                "Increase LoRA rank": "wrong",
                "Switch to a larger model": "wrong",
            },
        },
        {
            "observation": "The model repeats itself in almost every response.",
            "options": {
                "Increase the learning rate": "wrong",
                "The model is likely overfit — reduce epochs or add more diverse data": "correct",
                "Increase the LoRA rank": "wrong",
                "Enable gradient checkpointing": "wrong",
            },
        },
        {
            "observation": "The model produces reasonable responses for most prompts but fails completely on code generation tasks.",
            "options": {
                "Train for more epochs": "wrong",
                "Switch to a larger model": "wrong",
                "Add more code-generation examples to the training data": "correct",
                "Increase the learning rate": "wrong",
            },
        },
    ]

    dropdowns = []
    for i, scenario in enumerate(scenarios):
        dd = mo.ui.dropdown(
            options=scenario["options"],
            label=f"Action for scenario {i + 1}",
        )
        dropdowns.append(dd)

    for i, (scenario, dd) in enumerate(zip(scenarios, dropdowns)):
        mo.md(
            f"""
            **Scenario {i + 1}**: {scenario["observation"]}

            {dd}
            """
        )

    return (scenarios, dropdowns)


@app.cell
def iteration_feedback(scenarios, dropdowns):
    import marimo as mo

    feedback_parts = []
    for i, (scenario, dd) in enumerate(zip(scenarios, dropdowns)):
        if dd.value is None:
            feedback_parts.append(f"**Scenario {i+1}**: Select an answer.")
        elif dd.value == "correct":
            feedback_parts.append(f"**Scenario {i+1}**: Correct.")
        else:
            correct_action = [k for k, v in scenario["options"].items() if v == "correct"][0]
            feedback_parts.append(
                f"**Scenario {i+1}**: Not quite. The best action is: *{correct_action}*"
            )

    mo.md("\n\n".join(feedback_parts))
    return ()


@app.cell
def merge_exercise():
    import marimo as mo

    mo.md(
        """
        ## Part 4: Understanding Adapter Merging

        When you are satisfied with your fine-tuned model, the final step is
        merging the LoRA adapter into the base model for deployment.

        **Why merge?**

        - Eliminates the need for the PEFT library at inference time
        - Produces a standard Hugging Face model that any tool can load
        - No runtime overhead from applying the LoRA correction

        **When NOT to merge:**

        - You want to swap between multiple adapters on the same base model
        - You want to further fine-tune with additional data
        - You are still iterating and may discard this adapter

        The merge process loads the base model in full precision (fp16), applies
        the LoRA correction (W_new = W + A * B), and saves the result. This
        requires enough RAM to hold the full fp16 model (e.g., ~16 GB for a 7B model).

        See the [Evaluate Model Tutorial](../tutorials/evaluate-model.md) for the
        merge code.
        """
    )
    return ()


@app.cell
def summary():
    import marimo as mo

    mo.md(
        """
        ## Summary

        In this exercise you practiced:

        - Designing evaluation prompts across categories
        - Scoring model outputs against criteria
        - Recognizing patterns that indicate specific problems (overfitting, data gaps)
        - Matching observations to the correct iterative action
        - Understanding when and why to merge LoRA adapters

        These evaluation skills are as important as the training itself. A model
        is only as good as your ability to assess it.
        """
    )
    return ()


if __name__ == "__main__":
    app.run()
