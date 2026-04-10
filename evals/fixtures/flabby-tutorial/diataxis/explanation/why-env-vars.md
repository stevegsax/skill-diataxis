# Why Environment Variables?

## Configuration Belongs Outside the Code

A web application needs a database URL. Hardcode it and you have a problem:
the development database is `localhost:5432`, staging is `staging-db.internal`,
production is `prod-db.internal`. Three environments, three different values,
one codebase. Environment variables solve this by moving configuration out of
the code and into the environment where the code runs.

This separation has a name — the twelve-factor app methodology calls it
"strict separation of config from code." The test: could you open-source the
codebase right now without exposing any credentials? If yes, your config is
properly externalized.

## The Security Dimension

Hardcoded secrets are the most common source of credential leaks in public
repositories. An API key committed to git lives in the history forever, even
if you delete the file. Environment variables keep secrets out of the codebase
entirely — they exist only in the runtime environment and never touch version
control.

This is not just good practice. Compliance frameworks (SOC 2, PCI-DSS) require
that secrets are not stored in source code. Environment variables are the
simplest mechanism that satisfies this requirement.

For the practical steps, see the [how-to guide on .env files](../howto/dotenv-files.md).
For a list of common variables, see the [reference](../reference/common-vars.md).
