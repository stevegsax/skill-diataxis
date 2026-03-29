import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")


@app.cell
def intro():
    import marimo as mo

    mo.md(
        """
        # Run and Evaluate Exercise

        This exercise walks you through simulating a training run (using mock data
        for environments without a GPU) and evaluating the results. If you have a
        GPU, you can replace the mock sections with real training code from the
        tutorials.
        """
    )
    return (mo,)


@app.cell
def mock_training_data():
    import marimo as mo
    import random

    random.seed(42)

    # Simulate a training run's log history
    num_steps = 60
    base_loss = 1.8
    losses = []
    for i in range(num_steps):
        progress = i / num_steps
        # Loss decreases with noise
        loss = base_loss * (1 - 0.5 * progress) + random.gauss(0, 0.05)
        losses.append(round(max(0.3, loss), 4))

    eval_losses = []
    for i in range(0, num_steps, 10):
        progress = i / num_steps
        eval_loss = base_loss * (1 - 0.45 * progress) + random.gauss(0, 0.03)
        eval_losses.append((i, round(max(0.4, eval_loss), 4)))

    mo.md(
        f"""
        ## Part 1: Interpreting Training Logs

        Below is simulated training output for a 1-epoch QLoRA fine-tuning run
        on 1000 examples. The loss values simulate what you would see with a
        Llama 3.1 8B model on the Alpaca dataset.

        Total steps: {num_steps}
        """
    )
    return (losses, eval_losses, num_steps)


@app.cell
def loss_display(losses, eval_losses, num_steps):
    import marimo as mo

    step_range = mo.ui.range_slider(
        start=0,
        stop=num_steps - 1,
        step=1,
        value=[0, num_steps - 1],
        label="Step range to view",
    )

    mo.md(
        f"""
        ### Training Loss Log

        Use the slider to focus on a range of steps:

        {step_range}
        """
    )
    return (step_range,)


@app.cell
def show_loss_range(losses, eval_losses, step_range):
    import marimo as mo

    start, end = step_range.value
    visible_losses = losses[start : end + 1]

    # Text-based loss visualization
    lines = []
    max_bar = 40
    max_loss = max(visible_losses) if visible_losses else 1.0
    for i, loss in enumerate(visible_losses):
        step = start + i
        bar_len = int((loss / max_loss) * max_bar)
        bar = "#" * bar_len
        # Mark eval steps
        eval_marker = ""
        for es, el in eval_losses:
            if es == step:
                eval_marker = f"  [eval: {el}]"
        lines.append(f"Step {step:3d} | {loss:.4f} | {bar}{eval_marker}")

    log_text = "\n".join(lines)

    first_loss = visible_losses[0] if visible_losses else 0
    last_loss = visible_losses[-1] if visible_losses else 0
    change = first_loss - last_loss

    mo.md(
        f"""
        ```
        {log_text}
        ```

        **Loss change in view**: {first_loss:.4f} -> {last_loss:.4f} (delta: {change:+.4f})

        {"Loss is decreasing — the model is learning." if change > 0.05 else "Loss is relatively stable — the model may have converged in this range."}
        """
    )
    return ()


@app.cell
def convergence_quiz():
    import marimo as mo

    q1 = mo.ui.dropdown(
        options={
            "Train for more epochs — loss is still decreasing": "reasonable",
            "Stop here — one epoch is sufficient": "correct",
            "Increase the learning rate to speed up": "risky",
            "The loss is too high, start over with different data": "premature",
        },
        label="Your answer",
    )

    mo.md(
        f"""
        ## Part 2: Decision Point

        **Question**: The training loss went from ~1.8 to ~0.9 over one epoch.
        The eval loss went from ~1.75 to ~1.0. What should you do next?

        {q1}
        """
    )
    return (q1,)


@app.cell
def convergence_feedback(q1):
    import marimo as mo

    feedback_map = {
        "correct": "Good judgment. For instruction tuning, one epoch is often sufficient. The model has learned the instruction-following pattern. Additional epochs risk overfitting, especially with a small dataset. Test the model's outputs before deciding whether more training is needed.",
        "reasonable": "This is not wrong, but monitor eval loss carefully. If eval loss starts increasing while train loss continues decreasing, you are overfitting. For most instruction-tuning tasks, 1-3 epochs is the sweet spot.",
        "risky": "Increasing the learning rate when the model is already learning well is risky. It could cause instability (NaN loss, loss spikes). The current learning rate is working — leave it alone.",
        "premature": "A loss decrease from 1.8 to 0.9 is good progress. The absolute value of the loss depends on the model and data — what matters is the trend. Evaluate the model's actual outputs before concluding the data is the problem.",
    }

    if q1.value is None:
        mo.md("Select an answer above.")
    else:
        mo.md(f"**Feedback**: {feedback_map.get(q1.value, 'Select an answer.')}")
    return ()


@app.cell
def comparison_exercise():
    import marimo as mo

    mo.md(
        """
        ## Part 3: Comparing Outputs

        Below are simulated outputs from a base model and a fine-tuned model
        on the same prompt. Evaluate which is better and why.
        """
    )

    prompt = "### Instruction:\nExplain what a REST API is in simple terms.\n\n### Response:\n"

    base_output = (
        "### Instruction:\n"
        "Explain what a REST API is in simple terms.\n\n"
        "### Response:\n"
        "In this article, we will explore the concept of REST APIs and how they "
        "are used in modern web development. REST stands for Representational "
        "State Transfer, and it was first described by Roy Fielding in his 2000 "
        "doctoral dissertation. The concept builds on earlier work in distributed "
        "systems and the architecture of the World Wide Web itself. To understand "
        "REST, we need to first understand the HTTP protocol and how client-server "
        "communication works..."
    )

    finetuned_output = (
        "A REST API is a way for different software applications to talk to each "
        "other over the internet. Think of it like a waiter in a restaurant: you "
        "(the client) make a request from the menu, the waiter (the API) takes "
        "your request to the kitchen (the server), and brings back what you "
        "ordered (the response). REST APIs use standard HTTP methods like GET "
        "(retrieve data), POST (send data), PUT (update data), and DELETE "
        "(remove data)."
    )

    mo.md(
        f"""
        **Prompt**: Explain what a REST API is in simple terms.

        ---

        **Base model output**:

        > {base_output}

        ---

        **Fine-tuned model output**:

        > {finetuned_output}
        """
    )
    return (base_output, finetuned_output)


@app.cell
def evaluation_rubric(base_output, finetuned_output):
    import marimo as mo

    criteria = [
        "Directly answers the question",
        "Uses simple terms as requested",
        "Stays concise and focused",
        "Does not repeat the instruction",
        "Provides accurate information",
    ]

    base_scores = mo.ui.array(
        [
            mo.ui.slider(start=0, stop=3, step=1, value=0, label=f"Base: {c}")
            for c in criteria
        ]
    )

    ft_scores = mo.ui.array(
        [
            mo.ui.slider(start=0, stop=3, step=1, value=0, label=f"Fine-tuned: {c}")
            for c in criteria
        ]
    )

    mo.md(
        f"""
        ### Rate Both Outputs

        Score each output on a 0-3 scale for each criterion
        (0 = fails completely, 3 = excellent).

        **Base model scores:**

        {base_scores}

        **Fine-tuned model scores:**

        {ft_scores}
        """
    )
    return (criteria, base_scores, ft_scores)


@app.cell
def score_comparison(criteria, base_scores, ft_scores):
    import marimo as mo

    base_vals = [s.value for s in base_scores.value]
    ft_vals = [s.value for s in ft_scores.value]

    rows = []
    for c, bv, fv in zip(criteria, base_vals, ft_vals):
        winner = "Base" if bv > fv else ("Fine-tuned" if fv > bv else "Tie")
        rows.append(f"| {c} | {bv}/3 | {fv}/3 | {winner} |")

    table = "\n".join(rows)
    base_total = sum(base_vals)
    ft_total = sum(ft_vals)

    mo.md(
        f"""
        ### Score Comparison

        | Criterion | Base | Fine-tuned | Winner |
        |-----------|------|------------|--------|
        {table}
        | **Total** | **{base_total}/{len(criteria)*3}** | **{ft_total}/{len(criteria)*3}** | **{"Base" if base_total > ft_total else "Fine-tuned" if ft_total > base_total else "Tie"}** |

        {"The fine-tuned model scores higher overall. This is the typical result — instruction tuning teaches the model to follow the request format." if ft_total > base_total else "Interesting scores. In practice, the fine-tuned model almost always performs better on instruction-following tasks." if base_total >= ft_total else ""}
        """
    )
    return ()


@app.cell
def overfitting_exercise():
    import marimo as mo

    mo.md(
        """
        ## Part 4: Spotting Overfitting

        Below are loss curves from three different training runs. Identify which
        one shows overfitting.
        """
    )

    scenarios = {
        "Run A": {
            "train": [1.8, 1.4, 1.1, 0.9, 0.8, 0.7, 0.65, 0.6],
            "eval":  [1.8, 1.5, 1.2, 1.0, 0.95, 0.9, 0.88, 0.87],
            "label": "healthy",
        },
        "Run B": {
            "train": [1.8, 1.2, 0.7, 0.3, 0.1, 0.05, 0.02, 0.01],
            "eval":  [1.8, 1.3, 1.0, 0.95, 1.0, 1.1, 1.3, 1.5],
            "label": "overfit",
        },
        "Run C": {
            "train": [1.8, 1.75, 1.72, 1.70, 1.69, 1.68, 1.68, 1.67],
            "eval":  [1.8, 1.76, 1.73, 1.71, 1.70, 1.69, 1.69, 1.68],
            "label": "underfit",
        },
    }

    for name, data in scenarios.items():
        train_str = " -> ".join(f"{v:.2f}" for v in data["train"])
        eval_str = " -> ".join(f"{v:.2f}" for v in data["eval"])
        mo.md(
            f"""
            **{name}**:
            - Train loss: {train_str}
            - Eval loss:  {eval_str}
            """
        )

    overfit_answer = mo.ui.dropdown(
        options={"Run A": "A", "Run B": "B", "Run C": "C"},
        label="Which run shows overfitting?",
    )

    mo.md(f"\n{overfit_answer}")
    return (overfit_answer, scenarios)


@app.cell
def overfit_feedback(overfit_answer, scenarios):
    import marimo as mo

    if overfit_answer.value is None:
        mo.md("Select an answer above.")
    elif overfit_answer.value == "B":
        mo.md(
            """
            **Correct.** Run B shows classic overfitting: training loss drops to near
            zero while eval loss starts increasing after epoch 3-4. The model is memorizing
            the training data rather than learning generalizable patterns.

            - **Run A** is healthy: both losses decrease together and converge.
            - **Run C** is underfitting: both losses barely decrease, suggesting the
              model is not learning effectively (learning rate may be too low, or the
              model needs more capacity).
            """
        )
    else:
        mo.md(
            f"""
            **Not quite.** Look at Run B: the training loss drops to near zero (0.01)
            while the eval loss starts *increasing* after epoch 3. That divergence
            between train and eval loss is the hallmark of overfitting.
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

        - Reading and interpreting training loss logs
        - Making decisions about when to stop training
        - Evaluating model outputs with a rubric
        - Identifying overfitting from loss curves

        For deeper discussion of evaluation, see
        [Evaluation Strategies](../explanation/evaluation-strategies.md).
        For practical next steps, see
        [How to Iterate on Results](../howto/iterate-on-results.md).
        """
    )
    return ()


if __name__ == "__main__":
    app.run()
