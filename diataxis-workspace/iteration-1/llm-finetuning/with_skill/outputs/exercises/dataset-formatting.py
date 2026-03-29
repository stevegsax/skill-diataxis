import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")


@app.cell
def intro():
    import marimo as mo

    mo.md(
        """
        # Dataset Formatting Exercise

        In this exercise, you will practice converting raw data into instruction-tuning
        format, applying prompt templates, and inspecting the results. Each section
        has an interactive component where you write or modify code.
        """
    )
    return (mo,)


@app.cell
def sample_data():
    import marimo as mo

    # Create sample data that simulates what a user might have
    raw_data = [
        {
            "question": "What is the capital of France?",
            "answer": "The capital of France is Paris.",
        },
        {
            "question": "How do you reverse a list in Python?",
            "answer": "Use the .reverse() method or slicing: my_list[::-1].",
        },
        {
            "question": "Explain what an API is.",
            "answer": "An API (Application Programming Interface) is a set of rules that allows different software applications to communicate with each other.",
        },
        {
            "question": "What causes rain?",
            "answer": "Rain forms when water vapor in the atmosphere condenses into droplets that become heavy enough to fall.",
        },
        {
            "question": "Write a haiku about programming.",
            "answer": "Bugs hide in the code\nDebugging through the dark night\nTests finally pass",
        },
    ]

    mo.md(
        f"""
        ## Part 1: Explore the Raw Data

        We have {len(raw_data)} sample Q&A pairs. Here is the first one:

        ```python
        {raw_data[0]}
        ```

        The data has `question` and `answer` fields. Our goal is to convert this
        into the Alpaca instruction-tuning format.
        """
    )
    return (raw_data,)


@app.cell
def format_exercise(raw_data):
    import marimo as mo

    # Editable code cell for the user to write the formatting function
    code_editor = mo.ui.code_editor(
        value='''def format_to_alpaca(item):
    """Convert a raw Q&A item to Alpaca format.

    The output should have this structure:
    ### Instruction:
    {the question}

    ### Response:
    {the answer}
    """
    # TODO: Write the formatting code here
    formatted = ""
    return formatted
''',
        language="python",
        min_height=200,
    )

    mo.md(
        f"""
        ## Part 2: Write the Formatting Function

        Complete the function below to convert a raw Q&A item into Alpaca
        instruction-tuning format. The output should be a single string with
        `### Instruction:` and `### Response:` sections.

        {code_editor}
        """
    )
    return (code_editor,)


@app.cell
def run_format(code_editor, raw_data):
    import marimo as mo

    # Execute the user's code and test it
    local_ns = {}
    try:
        exec(code_editor.value, {}, local_ns)
        format_fn = local_ns.get("format_to_alpaca")
        if format_fn is None:
            mo.md("**Error**: Function `format_to_alpaca` not found. Make sure to define it.")
        else:
            result = format_fn(raw_data[0])
            has_instruction = "### Instruction:" in result
            has_response = "### Response:" in result
            has_question = raw_data[0]["question"] in result
            has_answer = raw_data[0]["answer"] in result

            checks = [
                ("Contains '### Instruction:'", has_instruction),
                ("Contains '### Response:'", has_response),
                ("Contains the question text", has_question),
                ("Contains the answer text", has_answer),
            ]

            check_rows = "\n".join(
                f"| {desc} | {'PASS' if ok else 'FAIL'} |" for desc, ok in checks
            )

            all_pass = all(ok for _, ok in checks)

            mo.md(
                f"""
                ### Result

                Your formatted output for the first example:

                ```
                {result}
                ```

                | Check | Status |
                |-------|--------|
                {check_rows}

                {"All checks passed. Your formatting function is correct." if all_pass else "Some checks failed. Review the expected format and try again."}
                """
            )
    except Exception as e:
        mo.md(f"**Error running your code**: {e}")
    return ()


@app.cell
def batch_format(raw_data):
    import marimo as mo

    # Show how to apply formatting to all items
    def reference_format(item):
        return (
            f"### Instruction:\n{item['question']}\n\n"
            f"### Response:\n{item['answer']}"
        )

    formatted_items = [reference_format(item) for item in raw_data]

    # Let user pick which example to view
    example_selector = mo.ui.dropdown(
        options={f"Example {i+1}": str(i) for i in range(len(formatted_items))},
        value="0",
        label="Select example to view",
    )

    mo.md(
        f"""
        ## Part 3: View All Formatted Examples

        Here are all {len(formatted_items)} examples formatted using the reference
        implementation. Select an example to inspect:

        {example_selector}
        """
    )
    return (formatted_items, example_selector)


@app.cell
def show_selected(formatted_items, example_selector):
    import marimo as mo

    idx = int(example_selector.value)
    text = formatted_items[idx]
    token_count = len(text.split())  # rough word count as proxy

    mo.md(
        f"""
        ### Example {idx + 1}

        ```
        {text}
        ```

        Approximate word count: {token_count} (actual token count depends on the tokenizer)
        """
    )
    return ()


@app.cell
def chatml_exercise():
    import marimo as mo

    chatml_editor = mo.ui.code_editor(
        value='''def format_to_chatml(item):
    """Convert a raw Q&A item to ChatML format.

    The output should look like:
    <|im_start|>user
    {the question}<|im_end|>
    <|im_start|>assistant
    {the answer}<|im_end|>
    """
    # TODO: Write the ChatML formatting code
    formatted = ""
    return formatted
''',
        language="python",
        min_height=200,
    )

    mo.md(
        f"""
        ## Part 4: Try ChatML Format

        Now try converting the same data to ChatML format. This is an alternative
        format used by some model families.

        {chatml_editor}
        """
    )
    return (chatml_editor,)


@app.cell
def run_chatml(chatml_editor, raw_data):
    import marimo as mo

    local_ns = {}
    try:
        exec(chatml_editor.value, {}, local_ns)
        format_fn = local_ns.get("format_to_chatml")
        if format_fn is None:
            mo.md("**Error**: Function `format_to_chatml` not found.")
        else:
            result = format_fn(raw_data[0])
            has_im_start = "<|im_start|>" in result
            has_im_end = "<|im_end|>" in result
            has_user = "user" in result
            has_assistant = "assistant" in result

            checks = [
                ("Contains '<|im_start|>'", has_im_start),
                ("Contains '<|im_end|>'", has_im_end),
                ("Contains 'user' role", has_user),
                ("Contains 'assistant' role", has_assistant),
            ]

            check_rows = "\n".join(
                f"| {desc} | {'PASS' if ok else 'FAIL'} |" for desc, ok in checks
            )

            all_pass = all(ok for _, ok in checks)

            mo.md(
                f"""
                ### ChatML Result

                ```
                {result}
                ```

                | Check | Status |
                |-------|--------|
                {check_rows}

                {"All checks passed." if all_pass else "Some checks failed. See the Dataset Formats Reference for the ChatML specification."}
                """
            )
    except Exception as e:
        mo.md(f"**Error running your code**: {e}")
    return ()


@app.cell
def token_analysis():
    import marimo as mo

    mo.md(
        """
        ## Part 5: Think About Token Lengths

        Before training, you need to choose a `max_seq_length`. This determines
        the maximum number of tokens per training example. Examples longer than
        this are truncated.

        Key considerations:

        - Setting it too short truncates valuable training data
        - Setting it too long wastes GPU memory on padding
        - A good rule of thumb: set it to the 95th percentile of your data's token lengths

        For our 5 short examples, 256 tokens would be more than sufficient.
        For real datasets, you would compute token statistics as shown in the
        [Dataset Preparation Tutorial](../tutorials/dataset-preparation.md).
        """
    )
    return ()


if __name__ == "__main__":
    app.run()
