import marimo

__generated_with = "0.13.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    mo.md(
        """
        # LLM Fine-Tuning Exercises

        Work through these exercises to practice each stage of the fine-tuning pipeline.
        Each section builds on the previous one. You do not need a GPU for the data
        preparation exercises -- only for the training and inference sections.

        **Prerequisites**: `pip install unsloth datasets marimo`
        """
    )
    return (mo,)


@app.cell
def _(mo):
    mo.md(
        """
        ---
        ## Part 1: Dataset Preparation

        The dataset is the most important factor in fine-tuning. In this section you will
        build a small Alpaca-format dataset, validate it, and convert it to the chat
        template format that the model expects.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ### Exercise 1.1: Create an Alpaca-Format Dataset

        Create a list of dictionaries in Alpaca format. Each dictionary needs three keys:
        `instruction`, `input` (can be empty string), and `output`.

        Pick a domain you know well (cooking, programming, finance, etc.) and write
        5-10 high-quality examples. Focus on consistency and accuracy.
        """
    )
    return


@app.cell
def _():
    # EXERCISE 1.1: Create your dataset here.
    # Replace the examples below with your own domain-specific data.

    my_dataset = [
        {
            "instruction": "Convert this temperature from Fahrenheit to Celsius.",
            "input": "212°F",
            "output": "212°F is equal to 100°C. The formula is: C = (F - 32) × 5/9, so (212 - 32) × 5/9 = 100.",
        },
        {
            "instruction": "What is the boiling point of water at sea level?",
            "input": "",
            "output": "Water boils at 100°C (212°F) at sea level (1 atm of pressure).",
        },
        {
            "instruction": "Explain what happens to the boiling point at high altitude.",
            "input": "",
            "output": "At higher altitudes, atmospheric pressure is lower, which means water boils at a lower temperature. For roughly every 150 meters (500 feet) of elevation gain, the boiling point drops by about 0.5°C. At the top of Mount Everest (8,849m), water boils at approximately 70°C.",
        },
    ]

    print(f"Dataset has {len(my_dataset)} examples")
    print(f"Keys in first example: {list(my_dataset[0].keys())}")
    return (my_dataset,)


@app.cell
def _(mo):
    mo.md(
        """
        ### Exercise 1.2: Validate Your Dataset

        Write a validation function that checks every example in your dataset for:

        - All required keys are present (`instruction`, `input`, `output`)
        - `instruction` is not empty
        - `output` is not empty
        - No duplicate instructions
        """
    )
    return


@app.cell
def _(my_dataset):
    def validate_alpaca_dataset(dataset: list[dict]) -> list[str]:
        """Validate an Alpaca-format dataset. Returns a list of error messages."""
        errors = []
        required_keys = {"instruction", "input", "output"}
        seen_instructions = set()

        for i, example in enumerate(dataset):
            # Check required keys
            missing = required_keys - set(example.keys())
            if missing:
                errors.append(f"Example {i}: missing keys {missing}")
                continue

            # Check non-empty fields
            if not example["instruction"].strip():
                errors.append(f"Example {i}: instruction is empty")
            if not example["output"].strip():
                errors.append(f"Example {i}: output is empty")

            # Check for duplicates
            instr = example["instruction"].strip().lower()
            if instr in seen_instructions:
                errors.append(f"Example {i}: duplicate instruction '{example['instruction'][:50]}...'")
            seen_instructions.add(instr)

        return errors

    # Run validation
    errors = validate_alpaca_dataset(my_dataset)
    if errors:
        print("Validation errors found:")
        for e in errors:
            print(f"  - {e}")
    else:
        print(f"Dataset is valid. {len(my_dataset)} examples passed all checks.")
    return (validate_alpaca_dataset,)


@app.cell
def _(mo):
    mo.md(
        """
        ### Exercise 1.3: Convert to Chat Template Format

        Models expect data in a specific chat template format. Convert your Alpaca data
        to the messages format used by `tokenizer.apply_chat_template()`.

        The target structure for each example:
        ```python
        [
            {"role": "user", "content": "<instruction + input>"},
            {"role": "assistant", "content": "<output>"},
        ]
        ```
        """
    )
    return


@app.cell
def _(my_dataset):
    def alpaca_to_messages(example: dict) -> list[dict]:
        """Convert a single Alpaca example to chat messages format."""
        # Combine instruction and input (if present) into the user message
        user_content = example["instruction"]
        if example.get("input", "").strip():
            user_content += f"\n\n{example['input']}"

        return [
            {"role": "user", "content": user_content},
            {"role": "assistant", "content": example["output"]},
        ]

    # Convert the full dataset
    messages_dataset = [alpaca_to_messages(ex) for ex in my_dataset]

    # Inspect the first converted example
    print("First example as chat messages:")
    for msg in messages_dataset[0]:
        print(f"  [{msg['role']}]: {msg['content'][:80]}...")
    print(f"\nConverted {len(messages_dataset)} examples total.")
    return (messages_dataset,)


@app.cell
def _(mo):
    mo.md(
        """
        ### Exercise 1.4: Save and Load with Hugging Face Datasets

        Save your dataset as a JSON file and load it back using the `datasets` library.
        This is how you will pass data to the trainer.
        """
    )
    return


@app.cell
def _(my_dataset):
    import json
    import tempfile
    from pathlib import Path

    from datasets import Dataset

    # Save to a temporary JSON file
    tmp_dir = Path(tempfile.mkdtemp())
    dataset_path = tmp_dir / "my_dataset.json"

    with open(dataset_path, "w") as f:
        json.dump(my_dataset, f, indent=2)

    print(f"Saved dataset to: {dataset_path}")

    # Load it back with Hugging Face datasets
    hf_dataset = Dataset.from_json(str(dataset_path))
    print(f"\nLoaded dataset: {hf_dataset}")
    print(f"Columns: {hf_dataset.column_names}")
    print(f"First example: {hf_dataset[0]}")
    return (hf_dataset,)


@app.cell
def _(mo):
    mo.md(
        """
        ---
        ## Part 2: Model Loading and Inspection

        These exercises require a GPU with at least 6 GB VRAM. If you do not have one,
        read through the code to understand the patterns -- you can run them later on
        appropriate hardware or use a free GPU on Google Colab.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ### Exercise 2.1: Check Your Hardware

        Before loading a model, verify your GPU is available and check how much VRAM
        you have. This determines which models you can fine-tune.
        """
    )
    return


@app.cell
def _():
    import torch

    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        vram_gb = torch.cuda.get_device_properties(0).total_mem / 1e9
        print(f"GPU: {gpu_name}")
        print(f"VRAM: {vram_gb:.1f} GB")
        print(f"CUDA version: {torch.version.cuda}")

        if vram_gb >= 12:
            print("\nYou can fine-tune 7-8B models with QLoRA.")
        elif vram_gb >= 6:
            print("\nYou can fine-tune 1-3B models with QLoRA.")
        else:
            print("\nVRAM is limited. Consider using Google Colab for a free GPU.")
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        print("Apple Silicon GPU detected (MPS backend).")
        print("MLX is recommended for fine-tuning on Apple Silicon.")
        print("Unsloth/CUDA workflows will not work here.")
    else:
        print("No GPU detected. You will need a GPU for training.")
        print("Options: Google Colab (free T4 GPU), or cloud GPU rental.")
    return


@app.cell
def _(mo):
    mo.md(
        """
        ### Exercise 2.2: Load a Quantized Model

        Load a 4-bit quantized model using Unsloth. This is the starting point for
        QLoRA fine-tuning.

        **Note**: This cell requires a CUDA GPU. Skip if running on CPU/MPS.
        """
    )
    return


@app.cell
def _():
    # Uncomment and run on a machine with a CUDA GPU:

    # from unsloth import FastLanguageModel
    #
    # model, tokenizer = FastLanguageModel.from_pretrained(
    #     model_name="unsloth/Meta-Llama-3.1-8B-bnb-4bit",
    #     max_seq_length=2048,
    #     load_in_4bit=True,
    # )
    #
    # # Inspect the model
    # total_params = sum(p.numel() for p in model.parameters())
    # trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    # print(f"Total parameters: {total_params:,}")
    # print(f"Trainable parameters (before LoRA): {trainable_params:,}")
    # print(f"Model dtype: {next(model.parameters()).dtype}")

    print("(Uncomment this cell to run on CUDA hardware)")
    return


@app.cell
def _(mo):
    mo.md(
        """
        ### Exercise 2.3: Add LoRA Adapters and Compare Parameter Counts

        After adding LoRA adapters, compare the number of trainable parameters to the
        total. This demonstrates why LoRA is so memory-efficient.
        """
    )
    return


@app.cell
def _():
    # Uncomment and run on a machine with a CUDA GPU:

    # from unsloth import FastLanguageModel
    #
    # model, tokenizer = FastLanguageModel.from_pretrained(
    #     model_name="unsloth/Meta-Llama-3.1-8B-bnb-4bit",
    #     max_seq_length=2048,
    #     load_in_4bit=True,
    # )
    #
    # model = FastLanguageModel.get_peft_model(
    #     model,
    #     r=16,
    #     lora_alpha=16,
    #     lora_dropout=0,
    #     target_modules=[
    #         "q_proj", "k_proj", "v_proj", "o_proj",
    #         "gate_proj", "up_proj", "down_proj",
    #     ],
    #     use_gradient_checkpointing="unsloth",
    # )
    #
    # total_params = sum(p.numel() for p in model.parameters())
    # trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    # print(f"Total parameters:     {total_params:,}")
    # print(f"Trainable parameters: {trainable_params:,}")
    # print(f"Trainable %:          {100 * trainable_params / total_params:.2f}%")
    #
    # # EXERCISE: Try changing r to 8, 32, 64 and observe how trainable params change.
    # # What is the relationship between r and trainable parameter count?

    print("(Uncomment this cell to run on CUDA hardware)")
    return


@app.cell
def _(mo):
    mo.md(
        """
        ---
        ## Part 3: Training

        This section walks through configuring and launching a training run.
        Requires a CUDA GPU.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ### Exercise 3.1: Configure Training Arguments

        Below is a training configuration with intentional gaps. Fill in the missing
        values based on what you learned in the guide. The comments provide hints.
        """
    )
    return


@app.cell
def _():
    # EXERCISE: Fill in the blanks (marked ???) with appropriate values.
    # Think about what each parameter does before choosing a value.

    training_config = {
        "per_device_train_batch_size": 2,       # How many examples per GPU per step
        "gradient_accumulation_steps": 4,        # ??? Hint: effective_batch = batch_size * this
        "warmup_steps": 10,                      # Steps before reaching full learning rate
        "num_train_epochs": 3,                   # ??? Hint: for < 1000 examples, keep this low
        "learning_rate": 2e-4,                   # ??? Hint: standard QLoRA starting point
        "logging_steps": 10,                     # Log metrics every N steps
        "save_strategy": "epoch",                # Save checkpoint every epoch
        "optim": "adamw_8bit",                   # 8-bit optimizer to save VRAM
    }

    # Verify your answers
    effective_batch_size = (
        training_config["per_device_train_batch_size"]
        * training_config["gradient_accumulation_steps"]
    )
    print(f"Effective batch size: {effective_batch_size}")
    print(f"Learning rate: {training_config['learning_rate']}")
    print(f"Epochs: {training_config['num_train_epochs']}")

    if effective_batch_size < 4:
        print("Warning: Effective batch size below 4 may cause unstable training.")
    if training_config["learning_rate"] > 5e-4:
        print("Warning: Learning rate above 5e-4 is aggressive for QLoRA.")
    if training_config["num_train_epochs"] > 5:
        print("Warning: More than 5 epochs risks overfitting on small datasets.")

    print("\nConfiguration looks reasonable." if effective_batch_size >= 4 else "")
    return


@app.cell
def _(mo):
    mo.md(
        """
        ### Exercise 3.2: Full Training Run

        This is a complete training script that ties together everything from Parts 1-3.
        Uncomment and run it on CUDA hardware with your own dataset.
        """
    )
    return


@app.cell
def _():
    # FULL TRAINING SCRIPT - Uncomment to run on CUDA hardware
    #
    # import torch
    # from unsloth import FastLanguageModel
    # from trl import SFTTrainer
    # from transformers import TrainingArguments
    # from datasets import Dataset
    #
    # # 1. Load model
    # model, tokenizer = FastLanguageModel.from_pretrained(
    #     model_name="unsloth/Meta-Llama-3.1-8B-bnb-4bit",
    #     max_seq_length=2048,
    #     load_in_4bit=True,
    # )
    #
    # # 2. Add LoRA
    # model = FastLanguageModel.get_peft_model(
    #     model,
    #     r=16,
    #     lora_alpha=16,
    #     lora_dropout=0,
    #     target_modules=[
    #         "q_proj", "k_proj", "v_proj", "o_proj",
    #         "gate_proj", "up_proj", "down_proj",
    #     ],
    #     use_gradient_checkpointing="unsloth",
    # )
    #
    # # 3. Load and format dataset
    # # Replace with your own dataset path
    # dataset = Dataset.from_json("my_dataset.json")
    #
    # def format_for_training(example):
    #     user_content = example["instruction"]
    #     if example.get("input", "").strip():
    #         user_content += f"\n\n{example['input']}"
    #     messages = [
    #         {"role": "user", "content": user_content},
    #         {"role": "assistant", "content": example["output"]},
    #     ]
    #     return {"text": tokenizer.apply_chat_template(messages, tokenize=False)}
    #
    # dataset = dataset.map(format_for_training)
    # split = dataset.train_test_split(test_size=0.1, seed=42)
    #
    # # 4. Train
    # trainer = SFTTrainer(
    #     model=model,
    #     tokenizer=tokenizer,
    #     train_dataset=split["train"],
    #     eval_dataset=split["test"],
    #     dataset_text_field="text",
    #     max_seq_length=2048,
    #     args=TrainingArguments(
    #         per_device_train_batch_size=2,
    #         gradient_accumulation_steps=4,
    #         warmup_steps=10,
    #         num_train_epochs=3,
    #         learning_rate=2e-4,
    #         fp16=not torch.cuda.is_bf16_supported(),
    #         bf16=torch.cuda.is_bf16_supported(),
    #         logging_steps=10,
    #         eval_strategy="steps",
    #         eval_steps=50,
    #         output_dir="./checkpoints",
    #         save_strategy="epoch",
    #         optim="adamw_8bit",
    #         seed=42,
    #     ),
    # )
    #
    # trainer.train()
    # print("Training complete!")
    #
    # # 5. Save
    # model.save_pretrained("./finetuned-lora")
    # tokenizer.save_pretrained("./finetuned-lora")

    print("(Uncomment this cell to run the full training pipeline on CUDA hardware)")
    return


@app.cell
def _(mo):
    mo.md(
        """
        ---
        ## Part 4: Evaluation

        After training, you need to evaluate whether the fine-tune actually improved
        the model for your use case.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ### Exercise 4.1: Build a Test Suite

        Create a set of test prompts for your domain. Include easy cases, hard cases,
        and edge cases. A good test suite has 20-50 prompts.
        """
    )
    return


@app.cell
def _():
    # EXERCISE: Create test prompts for your domain.
    # Each test case has a prompt and an expected_behavior description.
    # The expected_behavior is not an exact match -- it describes what a
    # good response should contain or how it should be structured.

    test_suite = [
        {
            "prompt": "Convert 98.6°F to Celsius.",
            "expected_behavior": "Should correctly calculate 37°C and show the formula.",
            "difficulty": "easy",
        },
        {
            "prompt": "What temperature does water boil at in Denver, Colorado?",
            "expected_behavior": "Should account for Denver's altitude (~1,600m) and give approximately 95°C.",
            "difficulty": "medium",
        },
        {
            "prompt": "Is -40 the same in both Fahrenheit and Celsius?",
            "expected_behavior": "Should confirm yes and explain that -40 is the intersection point of the two scales.",
            "difficulty": "hard",
        },
        {
            "prompt": "Convert absolute zero to Fahrenheit.",
            "expected_behavior": "Should know absolute zero is -273.15°C = -459.67°F.",
            "difficulty": "hard",
        },
    ]

    print(f"Test suite has {len(test_suite)} prompts:")
    for i, t in enumerate(test_suite):
        print(f"  {i+1}. [{t['difficulty']}] {t['prompt'][:60]}")

    # EXERCISE: Add at least 5 more test cases for your domain.
    return (test_suite,)


@app.cell
def _(mo):
    mo.md(
        """
        ### Exercise 4.2: Comparative Evaluation Framework

        This function runs test prompts through two models and formats the results
        for side-by-side comparison. On CUDA hardware, you would load the base model
        and fine-tuned model; here we demonstrate the evaluation structure.
        """
    )
    return


@app.cell
def _(test_suite):
    def evaluate_side_by_side(test_cases, model_a_fn, model_b_fn):
        """Run test cases through two model functions and return comparison results.

        Args:
            test_cases: List of dicts with 'prompt' and 'expected_behavior'
            model_a_fn: Callable that takes a prompt string and returns a response string
            model_b_fn: Callable that takes a prompt string and returns a response string

        Returns:
            List of result dicts with prompt, both responses, and expected behavior
        """
        results = []
        for case in test_cases:
            result = {
                "prompt": case["prompt"],
                "expected_behavior": case["expected_behavior"],
                "difficulty": case.get("difficulty", "unknown"),
                "model_a_response": model_a_fn(case["prompt"]),
                "model_b_response": model_b_fn(case["prompt"]),
            }
            results.append(result)
        return results

    # Demo with placeholder functions
    def mock_base_model(prompt):
        return f"[Base model would respond to: {prompt[:40]}...]"

    def mock_finetuned_model(prompt):
        return f"[Fine-tuned model would respond to: {prompt[:40]}...]"

    results = evaluate_side_by_side(test_suite, mock_base_model, mock_finetuned_model)

    print("Evaluation results (mock):")
    for r in results:
        print(f"\nPrompt: {r['prompt']}")
        print(f"  Expected: {r['expected_behavior']}")
        print(f"  Base:     {r['model_a_response']}")
        print(f"  Tuned:    {r['model_b_response']}")
    return


@app.cell
def _(mo):
    mo.md(
        """
        ---
        ## Part 5: Export and Deployment

        After a successful fine-tune, export your model for efficient local inference.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ### Exercise 5.1: Export to GGUF and Run with Ollama

        This is the final step: converting your fine-tuned model to the GGUF format
        used by llama.cpp and Ollama for fast CPU+GPU inference.

        ```python
        # Run on CUDA hardware after training:

        # Export to GGUF (Q4_K_M is a good default quantization)
        model.save_pretrained_gguf(
            "./finetuned-gguf",
            tokenizer,
            quantization_method="q4_k_m",
        )
        ```

        Then in your terminal:
        ```bash
        # Create Ollama Modelfile
        cat > Modelfile << 'MEOF'
        FROM ./finetuned-gguf/unsloth.Q4_K_M.gguf
        TEMPLATE \"\"\"{{ .Prompt }}\"\"\"
        PARAMETER temperature 0.7
        PARAMETER top_p 0.9
        MEOF

        # Import and run
        ollama create my-model -f Modelfile
        ollama run my-model "Your test prompt here"
        ```
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ---
        ## Summary and Next Steps

        You have practiced:

        1. **Dataset preparation** -- creating, validating, and formatting training data
        2. **Hardware assessment** -- checking GPU capabilities
        3. **Model loading** -- using Unsloth with 4-bit quantization and LoRA adapters
        4. **Training configuration** -- setting hyperparameters for QLoRA
        5. **Evaluation** -- building test suites and comparing model outputs
        6. **Deployment** -- exporting to GGUF for Ollama

        To continue learning:

        - Fine-tune on a real dataset for a task you care about
        - Experiment with different LoRA ranks (8, 16, 32, 64) and compare results
        - Try DPO (Direct Preference Optimization) for preference-based training
        - Explore Unsloth's GRPO for reinforcement learning fine-tuning
        """
    )
    return


if __name__ == "__main__":
    app.run()
