# How to Iterate on Fine-Tuning Results

This guide shows you how to diagnose problems with your fine-tuned model and take the right next step to improve it.

## How to Identify Underfitting vs Overfitting

1. Plot or print both training loss and validation loss:

    ```python
    log_history = trainer.state.log_history
    train_losses = [(e["step"], e["loss"]) for e in log_history if "loss" in e]
    eval_losses = [(e["step"], e["eval_loss"]) for e in log_history if "eval_loss" in e]

    print("Step | Train Loss | Eval Loss")
    for (ts, tl), (es, el) in zip(train_losses[::10], eval_losses):
        print(f"{ts:5d} | {tl:.4f}     | {el:.4f}")
    ```

2. Interpret the pattern:

    - **Both losses high and decreasing together**: underfitting. Train longer or increase model capacity (higher LoRA rank).
    - **Train loss low, eval loss increasing**: overfitting. Reduce training duration, add dropout, or increase dataset size.
    - **Both losses plateaued**: training has converged. More epochs will not help.

## How to Adjust Training Duration Based on Loss Curves

1. If loss is still decreasing at the end of training, increase epochs:

    ```python
    num_train_epochs = 3  # up from 1
    ```

2. If eval loss starts increasing partway through, use early stopping:

    ```python
    from transformers import EarlyStoppingCallback

    trainer = SFTTrainer(
        ...,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=3)],
    )
    ```

3. Alternatively, resume from the checkpoint where eval loss was lowest:

    ```python
    # Find the best checkpoint
    best_checkpoint = min(eval_losses, key=lambda x: x[1])
    print(f"Best checkpoint at step {best_checkpoint[0]} with loss {best_checkpoint[1]:.4f}")
    ```

## How to Improve Results by Curating the Dataset

1. **Increase data quality**: Remove low-quality, repetitive, or irrelevant examples. Quality matters more than quantity for fine-tuning.

2. **Add more task-specific examples**: If the model fails on certain prompt types, add 50-100 high-quality examples of that type.

3. **Balance the distribution**: Ensure the training data covers the range of tasks you care about. See [How to Prepare a Custom Dataset](prepare-custom-dataset.md) for balancing techniques.

4. **Review bad outputs**: When the model produces a bad response, check if similar instruction/response patterns exist in the training data. Often the issue is data quality, not model capability.

## How to Export and Share the Fine-Tuned Model

1. Merge and save in Hugging Face format:

    ```python
    merged_model = model.merge_and_unload()
    merged_model.save_pretrained("./my-finetuned-model")
    tokenizer.save_pretrained("./my-finetuned-model")
    ```

2. Push to Hugging Face Hub:

    ```python
    merged_model.push_to_hub("your-username/my-finetuned-model", private=True)
    tokenizer.push_to_hub("your-username/my-finetuned-model", private=True)
    ```

3. Convert to GGUF format for use with llama.cpp or Ollama:

    ```bash
    pip install llama-cpp-python
    python -m llama_cpp.convert ./my-finetuned-model --outfile model.gguf
    ```

For background on evaluation methodology, see [Evaluation Strategies](../explanation/evaluation-strategies.md).
