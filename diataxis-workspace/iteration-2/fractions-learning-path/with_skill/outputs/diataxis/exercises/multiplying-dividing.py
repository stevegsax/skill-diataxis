import marimo

__generated_with = "0.13.0"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(
        r"""
        # Multiplying and Dividing Fractions: Practice Exercises

        Practice multiplying and dividing fractions, including mixed numbers and
        cross-cancellation.
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
        ## Exercise 1: Multiply Two Fractions

        Compute $\frac{3}{5} \times \frac{2}{7}$ and simplify.
        """
    )
    return


@app.cell
def _(mo):
    e1_num = mo.ui.number(label="Numerator:", start=0, stop=200, step=1)
    e1_den = mo.ui.number(label="Denominator:", start=0, stop=200, step=1)
    mo.vstack([e1_num, e1_den])
    return e1_den, e1_num


@app.cell
def _(e1_den, e1_num, mo):
    if e1_num.value is not None and e1_den.value is not None:
        if e1_num.value == 6 and e1_den.value == 35:
            mo.md(
                r"""
                **Correct!**

                $\frac{3}{5} \times \frac{2}{7} = \frac{3 \times 2}{5 \times 7} = \frac{6}{35}$

                GCF of $6$ and $35$ is $1$, so this is already in lowest terms.
                """
            )
        elif e1_num.value != 0 or e1_den.value != 0:
            mo.md(
                r"""
                Not quite. Multiply numerators and denominators:

                $\frac{3}{5} \times \frac{2}{7} = \frac{3 \times 2}{5 \times 7} = \frac{6}{35}$
                """
            )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Exercise 2: Multiply with Cross-Cancellation

        Compute $\frac{5}{6} \times \frac{9}{10}$ using cross-cancellation first, then multiply.
        """
    )
    return


@app.cell
def _(mo):
    e2_num = mo.ui.number(label="Numerator:", start=0, stop=200, step=1)
    e2_den = mo.ui.number(label="Denominator:", start=0, stop=200, step=1)
    mo.vstack([e2_num, e2_den])
    return e2_den, e2_num


@app.cell
def _(e2_den, e2_num, mo):
    if e2_num.value is not None and e2_den.value is not None:
        if e2_num.value == 3 and e2_den.value == 4:
            mo.md(
                r"""
                **Correct!**

                Cross-cancel: $5$ and $10$ share factor $5$ ($5 \to 1$, $10 \to 2$).
                $9$ and $6$ share factor $3$ ($9 \to 3$, $6 \to 2$).

                $\frac{1}{2} \times \frac{3}{2} = \frac{3}{4}$
                """
            )
        elif e2_num.value == 45 and e2_den.value == 60:
            mo.md(
                r"""
                That is equivalent, but not in lowest terms. Simplify:
                $\frac{45}{60} = \frac{3}{4}$.

                Try cross-cancelling before multiplying to keep the numbers smaller.
                """
            )
        elif e2_num.value != 0 or e2_den.value != 0:
            mo.md(
                r"""
                Not quite. Cross-cancel first:

                - $5$ and $10$: divide both by $5$ → $1$ and $2$
                - $9$ and $6$: divide both by $3$ → $3$ and $2$

                $\frac{1}{2} \times \frac{3}{2} = \frac{3}{4}$
                """
            )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Exercise 3: Divide Two Fractions

        Compute $\frac{4}{5} \div \frac{2}{3}$.

        Remember: invert the second fraction and multiply.
        """
    )
    return


@app.cell
def _(mo):
    e3_whole = mo.ui.number(label="Whole number part (0 if none):", start=0, stop=100, step=1)
    e3_num = mo.ui.number(label="Fraction numerator:", start=0, stop=200, step=1)
    e3_den = mo.ui.number(label="Fraction denominator:", start=0, stop=200, step=1)
    mo.vstack([e3_whole, e3_num, e3_den])
    return e3_den, e3_num, e3_whole


@app.cell
def _(e3_den, e3_num, e3_whole, mo):
    if (
        e3_whole.value is not None
        and e3_num.value is not None
        and e3_den.value is not None
    ):
        if e3_whole.value == 1 and e3_num.value == 1 and e3_den.value == 5:
            mo.md(
                r"""
                **Correct!**

                $\frac{4}{5} \div \frac{2}{3} = \frac{4}{5} \times \frac{3}{2} = \frac{12}{10} = \frac{6}{5} = 1\frac{1}{5}$
                """
            )
        elif e3_whole.value == 0 and e3_num.value == 6 and e3_den.value == 5:
            mo.md(
                r"""
                $\frac{6}{5}$ is correct! As a mixed number: $1\frac{1}{5}$.
                """
            )
        elif e3_whole.value != 0 or e3_num.value != 0 or e3_den.value != 0:
            mo.md(
                r"""
                Not quite. Invert the second fraction and multiply:

                $\frac{4}{5} \div \frac{2}{3} = \frac{4}{5} \times \frac{3}{2} = \frac{12}{10} = \frac{6}{5} = 1\frac{1}{5}$
                """
            )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Exercise 4: Mixed Number Division

        Compute $2\frac{1}{4} \div 1\frac{1}{2}$.

        Convert to improper fractions first.
        """
    )
    return


@app.cell
def _(mo):
    e4_whole = mo.ui.number(label="Whole number part (0 if none):", start=0, stop=100, step=1)
    e4_num = mo.ui.number(label="Fraction numerator:", start=0, stop=200, step=1)
    e4_den = mo.ui.number(label="Fraction denominator:", start=0, stop=200, step=1)
    mo.vstack([e4_whole, e4_num, e4_den])
    return e4_den, e4_num, e4_whole


@app.cell
def _(e4_den, e4_num, e4_whole, mo):
    if (
        e4_whole.value is not None
        and e4_num.value is not None
        and e4_den.value is not None
    ):
        if e4_whole.value == 1 and e4_num.value == 1 and e4_den.value == 2:
            mo.md(
                r"""
                **Correct!**

                $2\frac{1}{4} = \frac{9}{4}$, $1\frac{1}{2} = \frac{3}{2}$

                $\frac{9}{4} \div \frac{3}{2} = \frac{9}{4} \times \frac{2}{3} = \frac{18}{12} = \frac{3}{2} = 1\frac{1}{2}$
                """
            )
        elif e4_whole.value == 0 and e4_num.value == 3 and e4_den.value == 2:
            mo.md(
                r"""
                $\frac{3}{2}$ is correct! As a mixed number: $1\frac{1}{2}$.
                """
            )
        elif e4_whole.value != 0 or e4_num.value != 0 or e4_den.value != 0:
            mo.md(
                r"""
                Not quite.

                Convert: $2\frac{1}{4} = \frac{9}{4}$ and $1\frac{1}{2} = \frac{3}{2}$

                Invert and multiply: $\frac{9}{4} \times \frac{2}{3} = \frac{18}{12} = \frac{3}{2} = 1\frac{1}{2}$
                """
            )
    return


if __name__ == "__main__":
    app.run()
