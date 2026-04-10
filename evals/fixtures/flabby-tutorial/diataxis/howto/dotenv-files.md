# How to Use .env Files

## Create the .env file

Create a file called `.env` in your project root:

```
DATABASE_URL=postgres://localhost:5432/myapp
SECRET_KEY=your-secret-key-here
DEBUG=true
```

## Install python-dotenv

```bash
pip install python-dotenv
```

## Load variables in your code

```python
from dotenv import load_dotenv
import os

load_dotenv()
db_url = os.environ["DATABASE_URL"]
```

`load_dotenv()` reads `.env` and adds each line to `os.environ`.

## Keep .env out of git

Add `.env` to your `.gitignore`:

```
echo ".env" >> .gitignore
```

Commit a `.env.example` with placeholder values so collaborators know which
variables to set. See the [tutorial](../tutorials/getting-started.md) if you
need background on environment variables.
