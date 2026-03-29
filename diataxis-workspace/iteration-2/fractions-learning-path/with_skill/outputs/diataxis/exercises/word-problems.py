import marimo

__generated_with = "0.13.0"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(
        r"""
        # Fraction Word Problems: Practice Exercises

        Apply your fraction skills to real-world scenarios. For each problem, identify
        the operation, set up the expression, and solve.
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
        ## Problem 1: Combining Distances

        You walk $\frac{3}{4}$ of a mile to the store and then $\frac{2}{5}$ of a mile
        to the park. What is the total distance you walked?

        **Step 1**: What operation does this require?
        """
    )
    return


@app.cell
def _(mo):
    p1_op = mo.ui.dropdown(
        options=["--select--", "addition", "subtraction", "multiplication", "division"],
        label="Operation:",
    )
    p1_op
    return (p1_op,)


@app.cell
def _(mo, p1_op):
    if p1_op.value is not None and p1_op.value != "--select--":
        if p1_op.value == "addition":
            mo.md(
                r"""
                **Correct!** We are combining two distances, so we add.

                **Step 2**: Compute $\frac{3}{4} + \frac{2}{5}$. Enter the answer as a
                mixed number in lowest terms.
                """
            )
        else:
            mo.md(
                r"""
                Not quite. We are combining two parts (distances walked). Combining
                means **addition**.
                """
            )
    return


@app.cell
def _(mo):
    p1_whole = mo.ui.number(label="Whole number part (0 if none):", start=0, stop=100, step=1)
    p1_num = mo.ui.number(label="Fraction numerator:", start=0, stop=100, step=1)
    p1_den = mo.ui.number(label="Fraction denominator:", start=0, stop=100, step=1)
    mo.vstack([p1_whole, p1_num, p1_den])
    return p1_den, p1_num, p1_whole


@app.cell
def _(mo, p1_den, p1_num, p1_whole):
    if (
        p1_whole.value is not None
        and p1_num.value is not None
        and p1_den.value is not None
    ):
        if p1_whole.value == 1 and p1_num.value == 3 and p1_den.value == 20:
            mo.md(
                r"""
                **Correct!**

                LCD of $4$ and $5$ is $20$.

                $\frac{3}{4} + \frac{2}{5} = \frac{15}{20} + \frac{8}{20} = \frac{23}{20} = 1\frac{3}{20}$ miles.
                """
            )
        elif p1_whole.value != 0 or p1_num.value != 0 or p1_den.value != 0:
            mo.md(
                r"""
                Not quite.

                LCD of $4$ and $5$ is $20$.

                $\frac{3}{4} = \frac{15}{20}$, $\frac{2}{5} = \frac{8}{20}$

                $\frac{15}{20} + \frac{8}{20} = \frac{23}{20} = 1\frac{3}{20}$ miles.
                """
            )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Problem 2: Recipe Scaling

        A recipe serves $4$ people and requires $1\frac{1}{2}$ cups of rice. You need to
        serve $6$ people. How much rice do you need?

        **Hint**: The scaling factor is $\frac{6}{4}$.
        """
    )
    return


@app.cell
def _(mo):
    p2_whole = mo.ui.number(label="Whole number part:", start=0, stop=100, step=1)
    p2_num = mo.ui.number(label="Fraction numerator:", start=0, stop=100, step=1)
    p2_den = mo.ui.number(label="Fraction denominator:", start=0, stop=100, step=1)
    mo.vstack([p2_whole, p2_num, p2_den])
    return p2_den, p2_num, p2_whole


@app.cell
def _(mo, p2_den, p2_num, p2_whole):
    if (
        p2_whole.value is not None
        and p2_num.value is not None
        and p2_den.value is not None
    ):
        if p2_whole.value == 2 and p2_num.value == 1 and p2_den.value == 4:
            mo.md(
                r"""
                **Correct!**

                Scaling factor: $\frac{6}{4} = \frac{3}{2}$

                $1\frac{1}{2} \times \frac{3}{2} = \frac{3}{2} \times \frac{3}{2} = \frac{9}{4} = 2\frac{1}{4}$ cups.
                """
            )
        elif p2_whole.value != 0 or p2_num.value != 0 or p2_den.value != 0:
            mo.md(
                r"""
                Not quite.

                Scaling factor: $\frac{6}{4} = \frac{3}{2}$

                Convert $1\frac{1}{2}$ to $\frac{3}{2}$, then multiply:

                $\frac{3}{2} \times \frac{3}{2} = \frac{9}{4} = 2\frac{1}{4}$ cups.
                """
            )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Problem 3: Remaining Material

        You have $5\frac{1}{3}$ yards of fabric. You use $2\frac{3}{4}$ yards for curtains.
        How much fabric remains?
        """
    )
    return


@app.cell
def _(mo):
    p3_whole = mo.ui.number(label="Whole number part:", start=0, stop=100, step=1)
    p3_num = mo.ui.number(label="Fraction numerator:", start=0, stop=100, step=1)
    p3_den = mo.ui.number(label="Fraction denominator:", start=0, stop=100, step=1)
    mo.vstack([p3_whole, p3_num, p3_den])
    return p3_den, p3_num, p3_whole


@app.cell
def _(mo, p3_den, p3_num, p3_whole):
    if (
        p3_whole.value is not None
        and p3_num.value is not None
        and p3_den.value is not None
    ):
        if p3_whole.value == 2 and p3_num.value == 7 and p3_den.value == 12:
            mo.md(
                r"""
                **Correct!**

                $5\frac{1}{3} - 2\frac{3}{4} = \frac{16}{3} - \frac{11}{4}$

                LCD of $3$ and $4$ is $12$:

                $\frac{64}{12} - \frac{33}{12} = \frac{31}{12} = 2\frac{7}{12}$ yards.
                """
            )
        elif p3_whole.value != 0 or p3_num.value != 0 or p3_den.value != 0:
            mo.md(
                r"""
                Not quite. Convert to improper fractions:

                $5\frac{1}{3} = \frac{16}{3}$, $2\frac{3}{4} = \frac{11}{4}$

                LCD of $3$ and $4$ is $12$:

                $\frac{64}{12} - \frac{33}{12} = \frac{31}{12} = 2\frac{7}{12}$ yards.
                """
            )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Problem 4: Dividing into Portions

        You have $3$ pounds of trail mix. Each snack bag holds $\frac{3}{8}$ of a pound.
        How many snack bags can you fill?
        """
    )
    return


@app.cell
def _(mo):
    p4_answer = mo.ui.number(label="Number of bags:", start=0, stop=100, step=1)
    p4_answer
    return (p4_answer,)


@app.cell
def _(mo, p4_answer):
    if p4_answer.value is not None:
        if p4_answer.value == 8:
            mo.md(
                r"""
                **Correct!**

                $3 \div \frac{3}{8} = \frac{3}{1} \times \frac{8}{3} = \frac{24}{3} = 8$ bags.
                """
            )
        elif p4_answer.value != 0:
            mo.md(
                r"""
                Not quite. This is a division problem: how many $\frac{3}{8}$'s fit into $3$?

                $3 \div \frac{3}{8} = \frac{3}{1} \times \frac{8}{3} = \frac{24}{3} = 8$ bags.
                """
            )
    return


if __name__ == "__main__":
    app.run()
