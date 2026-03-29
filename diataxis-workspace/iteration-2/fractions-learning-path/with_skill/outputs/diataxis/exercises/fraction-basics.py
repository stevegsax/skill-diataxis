import marimo

__generated_with = "0.13.0"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(
        r"""
        # Fraction Basics: Practice Exercises

        Work through these exercises to practice reading, writing, and converting fractions.
        Each exercise provides immediate feedback.
        """
    )
    return


@app.cell
def _():
    import marimo as mo
    import random
    return mo, random


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Exercise 1: Identify the Numerator and Denominator

        For the fraction $\frac{7}{12}$, enter the numerator and denominator below.
        """
    )
    return


@app.cell
def _(mo):
    numerator_input = mo.ui.number(label="Numerator:", start=0, stop=100, step=1)
    denominator_input = mo.ui.number(label="Denominator:", start=0, stop=100, step=1)
    mo.vstack([numerator_input, denominator_input])
    return denominator_input, numerator_input


@app.cell
def _(denominator_input, mo, numerator_input):
    if numerator_input.value is not None and denominator_input.value is not None:
        if numerator_input.value == 7 and denominator_input.value == 12:
            mo.md(
                r"""
                **Correct!** In the fraction $\frac{7}{12}$, the numerator is $7$
                (top, how many parts) and the denominator is $12$ (bottom, how many
                equal parts make the whole).
                """
            )
        elif numerator_input.value != 0 or denominator_input.value != 0:
            mo.md(
                r"""
                Not quite. Remember: the **numerator** is the top number and the
                **denominator** is the bottom number. In $\frac{7}{12}$, which number
                is on top?
                """
            )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Exercise 2: Classify the Fraction

        Classify each fraction as **proper**, **improper**, or a **mixed number**.

        - A **proper** fraction has numerator $<$ denominator (value $< 1$).
        - An **improper** fraction has numerator $\geq$ denominator (value $\geq 1$).
        - A **mixed number** combines a whole number with a proper fraction.
        """
    )
    return


@app.cell
def _(mo):
    fractions_to_classify = [
        (r"$\frac{3}{5}$", "proper"),
        (r"$\frac{9}{4}$", "improper"),
        (r"$2\frac{1}{3}$", "mixed number"),
        (r"$\frac{7}{7}$", "improper"),
        (r"$\frac{1}{8}$", "proper"),
    ]

    dropdowns = []
    for frac_str, _ in fractions_to_classify:
        dropdown = mo.ui.dropdown(
            options=["--select--", "proper", "improper", "mixed number"],
            label=f"{frac_str}:",
        )
        dropdowns.append(dropdown)

    mo.vstack(dropdowns)
    return dropdowns, fractions_to_classify


@app.cell
def _(dropdowns, fractions_to_classify, mo):
    results = []
    all_answered = True
    all_correct = True
    for i, (frac_str, correct_answer) in enumerate(fractions_to_classify):
        choice = dropdowns[i].value
        if choice == "--select--" or choice is None:
            all_answered = False
        elif choice == correct_answer:
            results.append(f"- {frac_str}: **Correct!**")
        else:
            results.append(
                f"- {frac_str}: Not quite. This is **{correct_answer}**."
            )
            all_correct = False

    if all_answered:
        if all_correct:
            results.append(
                "\nAll correct! You can distinguish proper, improper, and mixed numbers."
            )
        mo.md("\n".join(results))
    return all_answered, all_correct, results


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Exercise 3: Convert Improper Fraction to Mixed Number

        Convert $\frac{17}{5}$ to a mixed number.

        Remember: divide the numerator by the denominator. The quotient is the whole
        number, the remainder is the new numerator, and the denominator stays the same.
        """
    )
    return


@app.cell
def _(mo):
    whole_part = mo.ui.number(label="Whole number part:", start=0, stop=100, step=1)
    frac_numerator = mo.ui.number(
        label="Fraction numerator:", start=0, stop=100, step=1
    )
    frac_denominator = mo.ui.number(
        label="Fraction denominator:", start=0, stop=100, step=1
    )
    mo.vstack([whole_part, frac_numerator, frac_denominator])
    return frac_denominator, frac_numerator, whole_part


@app.cell
def _(frac_denominator, frac_numerator, mo, whole_part):
    if (
        whole_part.value is not None
        and frac_numerator.value is not None
        and frac_denominator.value is not None
    ):
        if (
            whole_part.value == 3
            and frac_numerator.value == 2
            and frac_denominator.value == 5
        ):
            mo.md(
                r"""
                **Correct!** $\frac{17}{5} = 3\frac{2}{5}$

                Check: $3 \times 5 + 2 = 17$ ✓
                """
            )
        elif whole_part.value != 0 or frac_numerator.value != 0 or frac_denominator.value != 0:
            mo.md(
                r"""
                Not quite. Divide $17 \div 5$:

                - Quotient: $3$ (this is the whole number part)
                - Remainder: $2$ (this is the new numerator)
                - Denominator stays $5$

                So $\frac{17}{5} = 3\frac{2}{5}$.
                """
            )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Exercise 4: Convert Mixed Number to Improper Fraction

        Convert $4\frac{3}{7}$ to an improper fraction.

        Remember: multiply the whole number by the denominator, add the numerator,
        and place over the original denominator.
        """
    )
    return


@app.cell
def _(mo):
    imp_numerator = mo.ui.number(
        label="Numerator of improper fraction:", start=0, stop=200, step=1
    )
    imp_denominator = mo.ui.number(
        label="Denominator of improper fraction:", start=0, stop=200, step=1
    )
    mo.vstack([imp_numerator, imp_denominator])
    return imp_denominator, imp_numerator


@app.cell
def _(imp_denominator, imp_numerator, mo):
    if imp_numerator.value is not None and imp_denominator.value is not None:
        if imp_numerator.value == 31 and imp_denominator.value == 7:
            mo.md(
                r"""
                **Correct!** $4\frac{3}{7} = \frac{31}{7}$

                Check: $4 \times 7 + 3 = 28 + 3 = 31$ ✓
                """
            )
        elif imp_numerator.value != 0 or imp_denominator.value != 0:
            mo.md(
                r"""
                Not quite. The conversion is:

                $4 \times 7 + 3 = 28 + 3 = 31$

                So $4\frac{3}{7} = \frac{31}{7}$.
                """
            )
    return


if __name__ == "__main__":
    app.run()
