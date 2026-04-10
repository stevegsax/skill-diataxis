# Getting Started with Environment Variables

## Introduction

It is important to understand that environment variables are an essential and
fundamental concept in modern software development. In this tutorial, we will
explore the basics of environment variables and learn how they can be used to
configure applications in a variety of different scenarios. By the end of this
tutorial, you will have gained a solid understanding of what environment
variables are and how they work.

## What Are Environment Variables?

Before we dive in, it is worth noting that environment variables have been
around for quite a long time — they were actually introduced in Unix systems
back in the 1970s. Essentially, an environment variable is basically a
key-value pair that is stored in the operating system's environment. They are
used by applications to read configuration values that might change between
different environments.

As we mentioned earlier, environment variables are really quite simple at
their core. Let's now look at how to set one.

## Setting Your First Variable

In order to set an environment variable, you will need to open your terminal.
The following command can be used to set a variable:

```bash
export GREETING="Hello, World"
```

It should be noted that the `export` keyword is what makes the variable
available to child processes. If `export` is not used, the variable will only
be available in the current shell session.

You can verify that the variable was set by running:

```bash
echo $GREETING
```

You should see:

```
Hello, World
```

## Reading Variables in Python

At this point in time, we will now look at how environment variables can be
read from within a Python script. The way in which this is accomplished is
through the use of the `os` module, which provides a very convenient function
for this purpose.

Create a file called `read_env.py`:

```python
import os

greeting = os.environ.get("GREETING", "No greeting set")
print(f"The greeting is: {greeting}")
```

The reason we use `os.environ.get()` rather than simply accessing
`os.environ["GREETING"]` directly is due to the fact that the `get()` method
allows us to specify a default value. This is important because if the
environment variable has not been set, an error would be thrown by the direct
access approach, which could potentially cause issues in your application.

Run the script:

```bash
python read_env.py
```

You should see:

```
The greeting is: Hello, World
```

## Summary

In this tutorial, we have explored the fundamentals of environment variables.
We have learned that they are basically key-value pairs that are stored in the
operating system, and we have seen how they can be set in the terminal and
read from Python scripts. It is important to remember that environment
variables are a very useful tool for managing configuration in your
applications.

For a deeper understanding of why environment variables matter, see the
[explanation](../explanation/why-env-vars.md). For a complete list of common
variables, see the [reference](../reference/common-vars.md).
