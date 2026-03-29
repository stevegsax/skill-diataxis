import marimo

__generated_with = "0.13.0"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(
        r"""
        # Adding and Subtracting Fractions: Practice Exercises

        Practice adding and subtracting fractions with like and unlike denominators.
        """
    )
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Exercise 1: Like Denominators

        Compute $\frac{3}{8} + \frac{1}{8}$ and simplify.

        Enter the final answer in lowest terms.
        """
    )
    return


@app.cell
def _(mo):
    e1_num = mo.ui.number(label="Numerator:", start=0, stop=100, step=1)
    e1_den = mo.ui.number(label="Denominator:", start=0, stop=100, step=1)
    mo.vstack([e1_num, e1_den])
    return e1_den, e1_num


@app.cell
def _(e1_den, e1_num, mo):
    if e1_num.value is not None and e1_den.value is not None:
        if e1_num.value == 1 and e1_den.value == 2:
            mo.md(
                r"""
                **Correct!**

                $\frac{3}{8} + \frac{1}{8} = \frac{4}{8} = \frac{1}{2}$
                """
            )
        elif e1_num.value == 4 and e1_den.value == 8:
            mo.md(
                r"""
                Almost! $\frac{4}{8}$ is correct but not in lowest terms.
                Simplify: $\frac{4}{8} = \frac{1}{2}$.
                """
            )
        elif e1_num.value != 0 or e1_den.value != 0:
            mo.md(
                r"""
                Not quite. Add the numerators, keep the denominator:

                $\frac{3}{8} + \frac{1}{8} = \frac{3+1}{8} = \frac{4}{8}$

                Simplify: GCF of $4$ and $8$ is $4$, so $\frac{4}{8} = \frac{1}{2}$.
                """
            )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Exercise 2: Unlike Denominators

        Compute $\frac{2}{3} + \frac{3}{4}$.

        Enter the final answer as a fraction or mixed number in lowest terms.
        """
    )
    return


@app.cell
def _(mo):
    e2_whole = mo.ui.number(label="Whole number part (0 if none):", start=0, stop=100, step=1)
    e2_num = mo.ui.number(label="Fraction numerator:", start=0, stop=100, step=1)
    e2_den = mo.ui.number(label="Fraction denominator:", start=0, stop=100, step=1)
    mo.vstack([e2_whole, e2_num, e2_den])
    return e2_den, e2_num, e2_whole


@app.cell
def _(e2_den, e2_num, e2_whole, mo):
    if (
        e2_whole.value is not None
        and e2_num.value is not None
        and e2_den.value is not None
    ):
        if e2_whole.value == 1 and e2_num.value == 5 and e2_den.value == 12:
            mo.md(
                r"""
                **Correct!**

                LCD of $3$ and $4$ is $12$.

                $\frac{2}{3} + \frac{3}{4} = \frac{8}{12} + \frac{9}{12} = \frac{17}{12} = 1\frac{5}{12}$
                """
            )
        elif e2_whole.value == 0 and e2_num.value == 17 and e2_den.value == 12:
            mo.md(
                r"""
                $\frac{17}{12}$ is correct! You can also write it as $1\frac{5}{12}$.
                """
            )
        elif e2_whole.value != 0 or e2_num.value != 0 or e2_den.value != 0:
            mo.md(
                r"""
                Not quite. Find the LCD of $3$ and $4$: it is $12$.

                $\frac{2}{3} = \frac{8}{12}$, $\frac{3}{4} = \frac{9}{12}$

                $\frac{8}{12} + \frac{9}{12} = \frac{17}{12} = 1\frac{5}{12}$
                """
            )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Exercise 3: Subtraction with Unlike Denominators

        Compute $\frac{7}{10} - \frac{1}{3}$.

        Enter the final answer in lowest terms.
        """
    )
    return


@app.cell
def _(mo):
    e3_num = mo.ui.number(label="Numerator:", start=0, stop=100, step=1)
    e3_den = mo.ui.number(label="Denominator:", start=0, stop=100, step=1)
    mo.vstack([e3_num, e3_den])
    return e3_den, e3_num


@app.cell
def _(e3_den, e3_num, mo):
    if e3_num.value is not None and e3_den.value is not None:
        if e3_num.value == 11 and e3_den.value == 30:
            mo.md(
                r"""
                **Correct!**

                LCD of $10$ and $3$ is $30$.

                $\frac{7}{10} = \frac{21}{30}$, $\frac{1}{3} = \frac{10}{30}$

                $\frac{21}{30} - \frac{10}{30} = \frac{11}{30}$

                GCF of $11$ and $30$ is $1$, so $\frac{11}{30}$ is already in lowest terms.
                """
            )
        elif e3_num.value != 0 or e3_den.value != 0:
            mo.md(
                r"""
                Not quite. LCD of $10$ and $3$ is $30$.

                $\frac{7}{10} = \frac{21}{30}$, $\frac{1}{3} = \frac{10}{30}$

                $\frac{21}{30} - \frac{10}{30} = \frac{11}{30}$
                """
            )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Exercise 4: Mixed Number Addition

        Compute $3\frac{1}{6} + 2\frac{3}{4}$.

        Enter the final answer as a mixed number in lowest terms.
        """
    )
    return


@app.cell
def _(mo):
    e4_whole = mo.ui.number(label="Whole number part:", start=0, stop=100, step=1)
    e4_num = mo.ui.number(label="Fraction numerator:", start=0, stop=100, step=1)
    e4_den = mo.ui.number(label="Fraction denominator:", start=0, stop=100, step=1)
    mo.vstack([e4_whole, e4_num, e4_den])
    return e4_den, e4_num, e4_whole


@app.cell
def _(e4_den, e4_num, e4_whole, mo):
    if (
        e4_whole.value is not None
        and e4_num.value is not None
        and e4_den.value is not None
    ):
        if e4_whole.value == 5 and e4_num.value == 11 and e4_den.value == 12:
            mo.md(
                r"""
                **Correct!**

                Whole parts: $3 + 2 = 5$

                Fractions: $\frac{1}{6} + \frac{3}{4}$. LCD is $12$.

                $\frac{2}{12} + \frac{9}{12} = \frac{11}{12}$

                Result: $5\frac{11}{12}$
                """
            )
        elif e4_whole.value != 0 or e4_num.value != 0 or e4_den.value != 0:
            mo.md(
                r"""
                Not quite.

                Whole parts: $3 + 2 = 5$

                Fractions: LCD of $6$ and $4$ is $12$.
                $\frac{1}{6} = \frac{2}{12}$, $\frac{3}{4} = \frac{9}{12}$

                $\frac{2}{12} + \frac{9}{12} = \frac{11}{12}$

                Answer: $5\frac{11}{12}$
                """
            )
    return


if __name__ == "__main__":
    app.run()
