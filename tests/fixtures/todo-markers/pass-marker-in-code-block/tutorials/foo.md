+++
title = "Foo"
weight = 12
description = "Tutorial whose only TODO is inside a code block — should still pass."
+++
Here is what a placeholder cell in marimo looks like. The check must
ignore markers inside fenced code, since an example is doing the
flagging for you.

```python
@app.cell
def step_one():
    # TODO: fill this in when the user gets here
    pass
```

And a marker inside inline code — `TODO` — should also not count.
