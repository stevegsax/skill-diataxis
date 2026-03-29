import marimo

__generated_with = "0.13.0"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(
        r"""
        # Equivalent Fractions and Simplifying: Practice Exercises

        Practice generating equivalent fractions, simplifying, and finding the LCD.
        """
    )
    return


@app.cell
def _():
    import marimo as mo
    from math import gcd
    return gcd, mo


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Exercise 1: Generate an Equivalent Fraction

        Find a fraction equivalent to $\frac{2}{5}$ with denominator $20$.

        Since $5 \times 4 = 20$, multiply the numerator by the same factor.
        """
    )
    return


@app.cell
def _(mo):
    equiv_num = mo.ui.number(
        label="Numerator (denominator is 20):", start=0, stop=100, step=1
    )
    equiv_num
    return (equiv_num,)


@app.cell
def _(equiv_num, mo):
    if equiv_num.value is not None:
        if equiv_num.value == 8:
            mo.md(
                r"""
                **Correct!** $\frac{2}{5} = \frac{2 \times 4}{5 \times 4} = \frac{8}{20}$
                """
            )
        elif equiv_num.value != 0:
            mo.md(
                r"""
                Not quite. We need $\frac{2}{5} = \frac{?}{20}$.

                Since $5 \times 4 = 20$, multiply the numerator by $4$ as well:
                $2 \times 4 = 8$.

                So $\frac{2}{5} = \frac{8}{20}$.
                """
            )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Exercise 2: Simplify to Lowest Terms

        Simplify $\frac{24}{36}$.

        Find the GCF of $24$ and $36$, then divide both by it.
        """
    )
    return


@app.cell
def _(mo):
    simp_num = mo.ui.number(label="Simplified numerator:", start=0, stop=100, step=1)
    simp_den = mo.ui.number(
        label="Simplified denominator:", start=0, stop=100, step=1
    )
    mo.vstack([simp_num, simp_den])
    return simp_den, simp_num


@app.cell
def _(mo, simp_den, simp_num):
    if simp_num.value is not None and simp_den.value is not None:
        if simp_num.value == 2 and simp_den.value == 3:
            mo.md(
                r"""
                **Correct!** The GCF of $24$ and $36$ is $12$.

                $\frac{24}{36} = \frac{24 \div 12}{36 \div 12} = \frac{2}{3}$
                """
            )
        elif simp_num.value != 0 or simp_den.value != 0:
            mo.md(
                r"""
                Not quite. The GCF of $24$ and $36$ is $12$.

                $\frac{24}{36} = \frac{24 \div 12}{36 \div 12} = \frac{2}{3}$

                Make sure you divide by the **greatest** common factor to reach lowest terms.
                """
            )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Exercise 3: Find the LCD

        Find the least common denominator (LCD) of $\frac{5}{6}$ and $\frac{3}{8}$.

        List multiples of $6$ and multiples of $8$ until you find the smallest one in common.
        """
    )
    return


@app.cell
def _(mo):
    lcd_answer = mo.ui.number(label="LCD of 6 and 8:", start=0, stop=200, step=1)
    lcd_answer
    return (lcd_answer,)


@app.cell
def _(lcd_answer, mo):
    if lcd_answer.value is not None:
        if lcd_answer.value == 24:
            mo.md(
                r"""
                **Correct!** Multiples of $6$: $6, 12, 18, 24, \ldots$
                Multiples of $8$: $8, 16, 24, \ldots$

                The LCD is $24$.
                """
            )
        elif lcd_answer.value != 0:
            mo.md(
                r"""
                Not quite. List the multiples:

                - Multiples of $6$: $6, 12, 18, 24, 30, \ldots$
                - Multiples of $8$: $8, 16, 24, 32, \ldots$

                The smallest number in both lists is $24$.
                """
            )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Exercise 4: Compare Two Fractions

        Which is larger: $\frac{4}{7}$ or $\frac{3}{5}$?

        Convert to a common denominator, then compare numerators.
        """
    )
    return


@app.cell
def _(mo):
    compare_answer = mo.ui.dropdown(
        options=["--select--", "4/7 is larger", "3/5 is larger", "they are equal"],
        label="Which is larger?",
    )
    compare_answer
    return (compare_answer,)


@app.cell
def _(compare_answer, mo):
    if compare_answer.value is not None and compare_answer.value != "--select--":
        if compare_answer.value == "3/5 is larger":
            mo.md(
                r"""
                **Correct!** Using LCD $= 35$:

                $\frac{4}{7} = \frac{20}{35}$ and $\frac{3}{5} = \frac{21}{35}$

                Since $20 < 21$, we have $\frac{4}{7} < \frac{3}{5}$.
                """
            )
        else:
            mo.md(
                r"""
                Not quite. Convert to LCD $= 35$:

                $\frac{4}{7} = \frac{4 \times 5}{7 \times 5} = \frac{20}{35}$

                $\frac{3}{5} = \frac{3 \times 7}{5 \times 7} = \frac{21}{35}$

                Since $20 < 21$, $\frac{3}{5}$ is larger.
                """
            )
    return


if __name__ == "__main__":
    app.run()
