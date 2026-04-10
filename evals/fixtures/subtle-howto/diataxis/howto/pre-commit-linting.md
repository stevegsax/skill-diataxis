# How to Set Up Pre-commit Linting

## Install the pre-commit framework

The pre-commit framework can be installed using pip. This tool is helpful
for managing and maintaining multi-language pre-commit hooks.

```bash
pip install pre-commit
```

The installation can be verified by running:

```bash
pre-commit --version
```

## Configure your hooks

A configuration file needs to be created at the root of your repository.
The file should be named `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.3.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

This configuration is useful because it provides a good starting point that
covers many common linting needs across different file types.

## Install the git hook

Once the configuration has been set up, the hook needs to be installed into
your repository's `.git/hooks/` directory:

```bash
pre-commit install
```

After this step has been completed, the hooks will be run automatically
every time a commit is made.

## Run hooks manually

It is sometimes useful to run hooks against all files, rather than just
the staged changes. This can be accomplished by running:

```bash
pre-commit run --all-files
```

This is particularly useful when hooks are first being added to an
existing project, as there may be many existing issues that need to be
addressed.

## Skip hooks when needed

In certain situations, it may be necessary to bypass the hooks. This can
be done by passing the `--no-verify` flag:

```bash
git commit --no-verify -m "emergency fix"
```

This should be used sparingly, as it defeats the purpose of having hooks
in the first place.

## Share hooks across the team

The `.pre-commit-config.yaml` file should be committed to the repository.
New team members can then install the hooks by running:

```bash
pre-commit install
```

It is also possible to configure CI to run `pre-commit run --all-files`
as a safety net. This ensures that even if someone skips the hooks locally,
the issues will be caught in CI.

For background on why hooks are valuable, see the
[explanation](../explanation/why-hooks.md). For a complete list of hook
types, see the [reference](../reference/hook-types.md).
