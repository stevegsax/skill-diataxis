# marimo-value-compare fixtures

Test cases for `check-marimo-value-compare`, which flags `.value == <literal>`
comparisons that test a dict-options widget's key (label) rather than its
mapped value. `mo.ui.radio` and `mo.ui.dropdown` take a key for the default
`value=` kwarg but return the mapped value from `.value` at runtime, so a
comparison written against the key silently evaluates to False — the widget
looks unresponsive in the browser with no error.

| Fixture               | Expected | What it tests |
|-----------------------|----------|---------------|
| `pass/`               | pass     | Dict options; comparison uses the mapped value. |
| `pass-seq-options/`   | pass     | Sequence options (no dict), so keys and values coincide. |
| `fail-key-not-value/` | fail     | Dict options; comparison uses the key, not the mapped value. |

Run with `bash run.sh`.
