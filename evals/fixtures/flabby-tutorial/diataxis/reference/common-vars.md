# Common Environment Variables

| Variable | Purpose | Typical values | Set by |
|----------|---------|----------------|--------|
| `PATH` | Directories searched for executables | `/usr/bin:/usr/local/bin:...` | Shell profile |
| `HOME` | Current user's home directory | `/home/alice`, `/Users/alice` | Login process |
| `SHELL` | Path to the user's default shell | `/bin/bash`, `/bin/zsh` | Login process |
| `EDITOR` | Default text editor | `vim`, `nano`, `code --wait` | User config |
| `LANG` | System locale | `en_US.UTF-8` | System config |
| `LC_ALL` | Overrides all locale settings | `en_US.UTF-8`, `C` | User config |

For how to set or modify these, see the [how-to guide](../howto/dotenv-files.md).
For why configuration is stored in environment variables rather than code, see the
[explanation](../explanation/why-env-vars.md).
