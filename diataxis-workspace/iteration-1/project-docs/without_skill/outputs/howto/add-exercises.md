# How to Add Interactive Exercises to a Learning Path

This guide shows you how to add marimo notebook exercises to tutorials in a Diataxis learning-path project.

## Prerequisites

- A Diataxis documentation project with `type = "learning-path"` in `diataxis.toml`
- `marimo` and `uvicorn` installed in your Python environment
- At least one tutorial to attach exercises to

## Steps

1. **Update `diataxis.toml`.** Add an `exercises` field to the tutorial entry for the topic:

    ```toml
    [topics.basic-operations.tutorial]
    file = "tutorials/basic-operations.md"
    status = "draft"
    covers = ["Addition", "Subtraction", "Multiplication"]
    detail = "Step-by-step with worked examples"
    guidance = "Include exercises for each operation."
    exercises = ["exercises/basic-ops.py"]
    ```

2. **Create the marimo notebook.** Create the exercise file in the `exercises/` directory. Marimo notebooks are standard Python files with a specific structure:

    ```bash
    marimo edit diataxis/exercises/basic-ops.py
    ```

    This opens the marimo editor where you can build the interactive exercise. Each exercise file should be self-contained and focused on one concept.

3. **Reference the exercise from the tutorial.** Add a mention in the tutorial markdown so readers know the exercise exists. The build pipeline will insert the iframe automatically, but a textual reference provides context:

    ```markdown
    Now that you have completed the addition examples, try the interactive
    exercise below to practice on your own.
    ```

4. **Build the documentation.** Run the build pipeline:

    ```bash
    python -m scripts.build diataxis
    ```

    The build pipeline will detect the exercise entry in `diataxis.toml` and:

    - Generate a marimo ASGI configuration file (`_serve_exercises.py`)
    - Insert an iframe into the tutorial's HTML output pointing to `http://localhost:2718/exercises/basic-ops`

5. **Serve and verify.** Start both servers:

    ```bash
    python -m scripts.build diataxis --serve
    ```

    Navigate to the tutorial page. The exercise should appear as an embedded interactive notebook at the bottom of the page.

## Notes

- Exercise iframes are inserted before the closing `</body>` tag in the generated HTML.
- The marimo server runs on port 2718 by default. The static documentation server runs on port 8000.
- If you add multiple exercises to a single tutorial, each gets its own iframe block.

## See Also

- [Build pipeline reference](../reference/build-pipeline.md) -- technical details on how exercises are integrated
- [Structure document reference](../reference/structure-schema.md) -- the `exercises` field specification
