# Evaluation Strategies for Fine-Tuned LLMs

Evaluating a fine-tuned language model is fundamentally different from evaluating a classifier or a regression model. There is no single number that tells you whether your model is "good." This discussion explores why evaluation is difficult, what approaches exist, and how to develop judgment about model quality.

## Why Loss Alone Is Insufficient

During training, you watch the loss decrease and it feels like progress. The loss measures how well the model predicts the next token in the training data. A lower loss means the model's predictions are more aligned with the training examples.

The problem is that low training loss does not guarantee useful outputs. A model can achieve low loss by memorizing training examples rather than learning generalizable patterns. It can also achieve low loss on average while failing catastrophically on specific types of inputs that were underrepresented in the training data.

Validation loss (measured on held-out data) is better, but still limited. It tells you whether the model generalizes to unseen examples from the same distribution, but it does not tell you whether the model's outputs are actually helpful, accurate, or well-structured from a human perspective.

## The Challenge with Generative Models

For a classification model, evaluation is straightforward: the model either predicts the correct class or it does not. For a generative language model, there is no single "correct" output. Ask five people to answer the same question and you will get five different responses, all potentially valid.

This means evaluation for fine-tuned LLMs is inherently subjective, at least partially. The field has developed automated metrics to approximate human judgment, but none of them fully capture what makes a response "good."

## Automated Metrics and Their Limitations

**ROUGE** measures n-gram overlap between the model's output and a reference response. It is useful for summarization tasks where the expected content is well-defined. It is less useful for open-ended generation where many valid responses exist.

**BLEU** is similar to ROUGE but originated in machine translation. It measures precision of n-gram matches. Same limitations apply.

**Perplexity** is the exponential of the average loss. Lower is better. It measures how "surprised" the model is by a sequence of tokens. Useful for comparing models on the same test set, but the absolute number is hard to interpret.

**LLM-as-judge** is a more recent approach where a larger, more capable model (e.g., GPT-4, Claude) evaluates the fine-tuned model's outputs against criteria you define. This correlates well with human judgment for many tasks and scales better than manual evaluation. The limitation is that it introduces a dependency on an external model and may have its own biases.

None of these metrics replace looking at the actual outputs. The most reliable evaluation for a fine-tuned model involves generating responses to a diverse set of test prompts and reviewing them.

## Human Evaluation

The gold standard is human evaluation, but it is expensive and slow. A practical approach for local fine-tuning:

1. Create a set of 20-50 test prompts that cover the range of tasks you care about
2. Generate responses from both the base model and the fine-tuned model
3. Compare them side by side, scoring on criteria relevant to your use case (accuracy, helpfulness, format compliance, etc.)

This does not need to be rigorous psychometrics. Even an informal review of 20 outputs gives you more actionable information than any automated metric for most practical fine-tuning projects.

## Overfitting: What It Looks Like

Overfitting in fine-tuning manifests differently than in classical ML:

- The model parrots training examples verbatim when given similar prompts
- Outputs become formulaic -- every response follows the same structure
- The model fails on prompts that are slightly outside the training distribution, even if they are simple
- Validation loss increases while training loss continues to decrease

Overfitting is more likely with small datasets, high learning rates, many training epochs, and high LoRA rank. The primary defenses are: train for fewer epochs (often 1-3 is sufficient), use a validation set to monitor for divergence, and ensure your dataset is diverse enough for your use case.

## When to Stop: Diminishing Returns

Fine-tuning has diminishing returns. The first epoch produces the most dramatic improvement. The second epoch provides some additional refinement. Beyond that, improvements tend to be marginal and the risk of overfitting increases.

A pragmatic stopping criterion: if the validation loss has not improved for a full epoch, stop. For many tasks, a single epoch over a well-curated dataset is sufficient.

The broader principle is that fine-tuning is not a process you can throw more compute at indefinitely. If the model is not performing well after reasonable training, the issue is almost always the data (quality, quantity, or distribution) or the base model choice, not the number of training steps.

For hands-on evaluation practice, see the [Evaluate Model Tutorial](../tutorials/evaluate-model.md). For practical next steps when results are not satisfactory, see [How to Iterate on Results](../howto/iterate-on-results.md).
