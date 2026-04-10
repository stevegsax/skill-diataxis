# Why Git Hooks?

## Catch problems before they spread

A linting error caught at commit time costs 10 seconds to fix. The same error
caught in CI costs a context switch — you've moved on to another task, the CI
notification arrives 5 minutes later, and now you need to reload the original
context. Studies on interruption cost put this at 15-25 minutes of lost focus.

Hooks move the feedback loop to the moment you're already thinking about the
code.

## Hooks vs CI: complementary, not competing

Hooks and CI serve different purposes:

- **Hooks** catch fast, local issues: formatting, lint errors, type errors,
  commit message format. They run in seconds on the files you changed.
- **CI** catches integration issues: test failures across the full suite,
  cross-platform builds, dependency conflicts. These need a clean environment
  and the full codebase.

Running your full test suite as a pre-commit hook is counterproductive — slow
hooks train developers to skip them with `--no-verify`.

## The right hooks are invisible

Well-configured hooks feel like nothing. They run in under 2 seconds, fix
what they can automatically (formatting, trailing whitespace), and only block
the commit for real issues. If developers are routinely skipping hooks, the
hooks are too slow or too noisy — fix the hooks, not the developers.

For setup steps, see the [how-to guide](../howto/pre-commit-linting.md).
