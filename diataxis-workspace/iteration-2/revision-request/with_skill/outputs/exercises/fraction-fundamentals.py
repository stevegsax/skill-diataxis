# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
# ]
# ///

import marimo

__generated_with = "0.13.0"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(
        """
        # Fraction Fundamentals: Practice Exercises

        Work through these exercises to build confidence with the basics of fractions.
        Each section has problems that check your answer immediately.
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
        """
        ## Exercise 1: Identify the Parts

        For the fraction shown below, enter the numerator and denominator.
        """
    )
    return


@app.cell
def _(mo):
    mo.md("**What are the numerator and denominator of 7/9?**")
    return


@app.cell
def _(mo):
    e1_numerator = mo.ui.number(label="Numerator:", start=0, stop=100, step=1)
    e1_denominator = mo.ui.number(label="Denominator:", start=0, stop=100, step=1)
    mo.vstack([e1_numerator, e1_denominator])
    return e1_denominator, e1_numerator


@app.cell
def _(e1_denominator, e1_numerator, mo):
    if e1_numerator.value == 7 and e1_denominator.value == 9:
        mo.output.replace(mo.md("**Correct!** The numerator is 7 (top) and the denominator is 9 (bottom)."))
    elif e1_numerator.value > 0 or e1_denominator.value > 0:
        mo.output.replace(mo.md("Not quite. Remember: the numerator is the top number and the denominator is the bottom number."))
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Exercise 2: Equivalent Fractions

        Create an equivalent fraction by filling in the missing number.
        """
    )
    return


@app.cell
def _(mo):
    mo.md("**2/5 = ?/15**  (What number goes in place of the question mark?)")
    return


@app.cell
def _(mo):
    e2_answer = mo.ui.number(label="Missing numerator:", start=0, stop=100, step=1)
    e2_answer
    return (e2_answer,)


@app.cell
def _(e2_answer, mo):
    if e2_answer.value == 6:
        mo.output.replace(mo.md(
            "**Correct!** Since 5 * 3 = 15, we multiply the numerator by 3 as well: 2 * 3 = 6. So 2/5 = 6/15."
        ))
    elif e2_answer.value > 0:
        mo.output.replace(mo.md(
            "Not quite. Think about what you multiply the denominator by to get from 5 to 15, then apply the same multiplier to the numerator."
        ))
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Exercise 3: Simplify Fractions

        Simplify each fraction to its lowest terms.
        """
    )
    return


@app.cell
def _(gcd, mo):
    problems = [
        (4, 8),
        (6, 9),
        (10, 15),
        (12, 18),
        (8, 20),
    ]

    e3_inputs = []
    rows = []
    for num, den in problems:
        simplified_num = num // gcd(num, den)
        simplified_den = den // gcd(num, den)
        num_input = mo.ui.number(label="Num:", start=0, stop=100, step=1)
        den_input = mo.ui.number(label="Den:", start=0, stop=100, step=1)
        e3_inputs.append((num, den, simplified_num, simplified_den, num_input, den_input))
        rows.append(
            mo.md(f"**{num}/{den}** = ").center()
        )

    mo.md(
        """
        Simplify **4/8** to lowest terms.
        """
    )
    return e3_inputs, problems, rows


@app.cell
def _(mo):
    e3_num = mo.ui.number(label="Simplified numerator:", start=0, stop=100, step=1)
    e3_den = mo.ui.number(label="Simplified denominator:", start=0, stop=100, step=1)
    mo.vstack([
        mo.md("Simplify **4/8**:"),
        e3_num,
        e3_den,
    ])
    return e3_den, e3_num


@app.cell
def _(e3_den, e3_num, mo):
    if e3_num.value == 1 and e3_den.value == 2:
        mo.output.replace(mo.md("**Correct!** 4/8 = 1/2. The GCF of 4 and 8 is 4. Dividing both by 4 gives 1/2."))
    elif e3_num.value > 0 or e3_den.value > 0:
        mo.output.replace(mo.md("Not quite. Find the greatest common factor (GCF) of 4 and 8, then divide both the numerator and denominator by it."))
    return


@app.cell
def _(mo):
    e3b_num = mo.ui.number(label="Simplified numerator:", start=0, stop=100, step=1)
    e3b_den = mo.ui.number(label="Simplified denominator:", start=0, stop=100, step=1)
    mo.vstack([
        mo.md("Simplify **12/18**:"),
        e3b_num,
        e3b_den,
    ])
    return e3b_den, e3b_num


@app.cell
def _(e3b_den, e3b_num, mo):
    if e3b_num.value == 2 and e3b_den.value == 3:
        mo.output.replace(mo.md("**Correct!** 12/18 = 2/3. The GCF of 12 and 18 is 6. Dividing both by 6 gives 2/3."))
    elif e3b_num.value > 0 or e3b_den.value > 0:
        mo.output.replace(mo.md("Not quite. Find the GCF of 12 and 18 (hint: it is 6), then divide both parts by it."))
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Exercise 4: Mixed Numbers and Improper Fractions

        Convert between mixed numbers and improper fractions.
        """
    )
    return


@app.cell
def _(mo):
    mo.md("**Convert 7/3 to a mixed number.** Enter the whole number part and the fractional parts.")
    return


@app.cell
def _(mo):
    e4_whole = mo.ui.number(label="Whole number:", start=0, stop=100, step=1)
    e4_num = mo.ui.number(label="Fraction numerator:", start=0, stop=100, step=1)
    e4_den = mo.ui.number(label="Fraction denominator:", start=0, stop=100, step=1)
    mo.vstack([e4_whole, e4_num, e4_den])
    return e4_den, e4_num, e4_whole


@app.cell
def _(e4_den, e4_num, e4_whole, mo):
    if e4_whole.value == 2 and e4_num.value == 1 and e4_den.value == 3:
        mo.output.replace(mo.md("**Correct!** 7/3 = 2 1/3. Since 7 / 3 = 2 remainder 1, the mixed number is 2 1/3."))
    elif e4_whole.value > 0 or e4_num.value > 0 or e4_den.value > 0:
        mo.output.replace(mo.md("Not quite. Divide 7 by 3: the quotient is the whole number, the remainder is the new numerator, and the denominator stays 3."))
    return


@app.cell
def _(mo):
    mo.md("**Convert 3 2/5 to an improper fraction.** Enter numerator and denominator.")
    return


@app.cell
def _(mo):
    e4b_num = mo.ui.number(label="Numerator:", start=0, stop=100, step=1)
    e4b_den = mo.ui.number(label="Denominator:", start=0, stop=100, step=1)
    mo.vstack([e4b_num, e4b_den])
    return e4b_den, e4b_num


@app.cell
def _(e4b_den, e4b_num, mo):
    if e4b_num.value == 17 and e4b_den.value == 5:
        mo.output.replace(mo.md("**Correct!** 3 2/5 = 17/5. Multiply 3 * 5 = 15, add 2 = 17. Denominator stays 5."))
    elif e4b_num.value > 0 or e4b_den.value > 0:
        mo.output.replace(mo.md("Not quite. Multiply the whole number (3) by the denominator (5), then add the numerator (2). Keep the denominator as 5."))
    return


@app.cell
def _(mo):
    mo.md(
        """
        ---

        **Well done!** You have practiced identifying fraction parts, finding equivalents,
        simplifying, and converting between mixed numbers and improper fractions.

        Next steps:

        - [Adding and Subtracting Fractions Tutorial](../tutorials/adding-subtracting.md)
        - [Fraction Operations Reference](../reference/fraction-operations.md)
        """
    )
    return


if __name__ == "__main__":
    app.run()
