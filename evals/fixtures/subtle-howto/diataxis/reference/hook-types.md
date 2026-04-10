# Git Hook Types

| Hook | Trigger | Arguments | Common use |
|------|---------|-----------|------------|
| `pre-commit` | Before commit is created | None | Linting, formatting |
| `commit-msg` | After commit message is entered | Path to message file | Message format enforcement |
| `pre-push` | Before push to remote | Remote name, URL | Test suite, build verification |
| `post-merge` | After a merge completes | Squash flag (0 or 1) | Dependency install, migration |
| `pre-rebase` | Before rebase starts | Upstream branch, rebased branch | Warn on shared branches |
| `post-checkout` | After `git checkout` or `git switch` | Previous HEAD, new HEAD, branch flag | Env setup, submodule update |

All hooks live in `.git/hooks/`. Git runs them from the repository root.

For setup instructions, see the [how-to guide](../howto/pre-commit-linting.md).
For why automating checks at commit time matters, see the
[explanation](../explanation/why-hooks.md).
