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
        # Adding and Subtracting Fractions: Practice Exercises

        These exercises progress from same-denominator addition through mixed-number
        subtraction. Each problem checks your answer immediately.
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
        ## Exercise 1: Same Denominator Addition

        When the denominators are the same, add the numerators and keep the denominator.

        **Compute 2/7 + 3/7.** Enter your answer as a fraction.
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
    if e1_num.value == 5 and e1_den.value == 7:
        mo.output.replace(mo.md("**Correct!** 2/7 + 3/7 = 5/7. We added the numerators (2 + 3 = 5) and kept the denominator (7)."))
    elif e1_num.value > 0 or e1_den.value > 0:
        mo.output.replace(mo.md("Not quite. With same denominators, add the numerators and keep the denominator unchanged."))
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Exercise 2: Different Denominator Addition

        **Compute 1/4 + 1/6.** Give your answer in lowest terms.

        Hint: Find the LCD of 4 and 6 first.
        """
    )
    return


@app.cell
def _(mo):
    e2_num = mo.ui.number(label="Numerator:", start=0, stop=100, step=1)
    e2_den = mo.ui.number(label="Denominator:", start=0, stop=100, step=1)
    mo.vstack([e2_num, e2_den])
    return e2_den, e2_num


@app.cell
def _(e2_den, e2_num, gcd, mo):
    # Correct answer: 1/4 + 1/6 = 3/12 + 2/12 = 5/12
    if e2_num.value > 0 and e2_den.value > 0:
        # Check if their answer equals 5/12
        user_simplified_num = e2_num.value // gcd(e2_num.value, e2_den.value)
        user_simplified_den = e2_den.value // gcd(e2_num.value, e2_den.value)
        if user_simplified_num == 5 and user_simplified_den == 12:
            mo.output.replace(mo.md(
                "**Correct!** 1/4 + 1/6 = 3/12 + 2/12 = 5/12. "
                "The LCD of 4 and 6 is 12. Convert: 1/4 = 3/12, 1/6 = 2/12. Add: 5/12."
            ))
        else:
            mo.output.replace(mo.md(
                "Not quite. The LCD of 4 and 6 is 12. Convert each fraction to twelfths, then add the numerators."
            ))
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Exercise 3: Subtraction with Different Denominators

        **Compute 3/4 - 1/3.** Give your answer in lowest terms.
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
def _(e3_den, e3_num, gcd, mo):
    # Correct: 3/4 - 1/3 = 9/12 - 4/12 = 5/12
    if e3_num.value > 0 and e3_den.value > 0:
        user_sn = e3_num.value // gcd(e3_num.value, e3_den.value)
        user_sd = e3_den.value // gcd(e3_num.value, e3_den.value)
        if user_sn == 5 and user_sd == 12:
            mo.output.replace(mo.md(
                "**Correct!** 3/4 - 1/3 = 9/12 - 4/12 = 5/12. "
                "LCD of 4 and 3 is 12. Convert: 3/4 = 9/12, 1/3 = 4/12. Subtract: 5/12."
            ))
        else:
            mo.output.replace(mo.md(
                "Not quite. Find the LCD of 4 and 3 (it is 12), convert both fractions, then subtract."
            ))
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Exercise 4: Subtracting from a Whole Number

        **Compute 5 - 2/3.** Give your answer as a mixed number (whole part + fraction in lowest terms).
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
    # 5 - 2/3 = 15/3 - 2/3 = 13/3 = 4 1/3
    if e4_whole.value == 4 and e4_num.value == 1 and e4_den.value == 3:
        mo.output.replace(mo.md(
            "**Correct!** 5 - 2/3 = 15/3 - 2/3 = 13/3 = 4 1/3."
        ))
    elif e4_whole.value > 0 or e4_num.value > 0 or e4_den.value > 0:
        mo.output.replace(mo.md(
            "Not quite. Write 5 as 15/3, then subtract: 15/3 - 2/3 = 13/3. Convert to a mixed number."
        ))
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Exercise 5: Adding Mixed Numbers

        **Compute 2 3/4 + 1 2/3.** Give your answer as a mixed number in lowest terms.
        """
    )
    return


@app.cell
def _(mo):
    e5_whole = mo.ui.number(label="Whole number part:", start=0, stop=100, step=1)
    e5_num = mo.ui.number(label="Fraction numerator:", start=0, stop=100, step=1)
    e5_den = mo.ui.number(label="Fraction denominator:", start=0, stop=100, step=1)
    mo.vstack([e5_whole, e5_num, e5_den])
    return e5_den, e5_num, e5_whole


@app.cell
def _(e5_den, e5_num, e5_whole, mo):
    # 2 3/4 + 1 2/3 = 11/4 + 5/3 = 33/12 + 20/12 = 53/12 = 4 5/12
    if e5_whole.value == 4 and e5_num.value == 5 and e5_den.value == 12:
        mo.output.replace(mo.md(
            "**Correct!** 2 3/4 + 1 2/3 = 11/4 + 5/3 = 33/12 + 20/12 = 53/12 = 4 5/12."
        ))
    elif e5_whole.value > 0 or e5_num.value > 0 or e5_den.value > 0:
        mo.output.replace(mo.md(
            "Not quite. Convert both to improper fractions first: 2 3/4 = 11/4, 1 2/3 = 5/3. "
            "Find the LCD (12), convert, add, then convert back to a mixed number."
        ))
    return


@app.cell
def _(mo):
    mo.md(
        """
        ---

        **Great work!** You have practiced adding and subtracting fractions with same
        and different denominators, subtracting from whole numbers, and adding mixed numbers.

        Next steps:

        - [Multiplying and Dividing Tutorial](../tutorials/multiplying-dividing.md)
        - [Fraction Operations Reference](../reference/fraction-operations.md)
        """
    )
    return


if __name__ == "__main__":
    app.run()
