# Your First Git Hook

## Create the hook file

Open your terminal and navigate to a git repository. Create the pre-commit
hook:

```bash
touch .git/hooks/pre-commit
```

## Add a linting command

Open `.git/hooks/pre-commit` and add:

```bash
#!/bin/sh
echo "Running linter..."
ruff check .
```

## Make it executable

```bash
chmod +x .git/hooks/pre-commit
```

## Test it

Stage a Python file and commit:

```bash
git add example.py
git commit -m "test hook"
```

You should see `Running linter...` followed by ruff's output. If ruff finds
issues, the commit is blocked.

For the full list of hooks git supports, see the
[reference](../reference/hook-types.md).
