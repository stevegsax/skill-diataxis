# Finding Equivalent Fractions and Simplifying

In this tutorial, we will generate equivalent fractions, simplify fractions to lowest terms, find the least common denominator of two fractions, and compare fractions. By the end, you will be able to determine whether two fractions represent the same value and put any fraction in its simplest form.

## What we need before starting

You should be comfortable with fraction notation (numerator, denominator) and the difference between proper and improper fractions. See the [Fraction Basics Tutorial](fraction-basics.md) if you need a refresher.

## Step 1: Generating equivalent fractions

Two fractions are **equivalent** if they represent the same value. We create an equivalent fraction by multiplying both the numerator and the denominator by the same nonzero number.

Let's start with $\frac{1}{2}$ and multiply top and bottom by $3$:

$$\frac{1}{2} = \frac{1 \times 3}{2 \times 3} = \frac{3}{6}$$

**Check**: $\frac{1}{2}$ and $\frac{3}{6}$ both represent half of a whole. The value has not changed.

Let's generate a few more equivalents of $\frac{1}{2}$:

$$\frac{1}{2} = \frac{2}{4} = \frac{3}{6} = \frac{4}{8} = \frac{5}{10}$$

You should notice that each fraction describes the same point on the number line.

## Step 2: Simplifying a fraction using the GCF

To simplify a fraction, we reverse the process: divide both numerator and denominator by their **greatest common factor (GCF)**.

Let's simplify $\frac{12}{18}$.

First, find the GCF of $12$ and $18$. The factors of $12$ are $1, 2, 3, 4, 6, 12$. The factors of $18$ are $1, 2, 3, 6, 9, 18$. The greatest common factor is $6$.

Now divide:

$$\frac{12}{18} = \frac{12 \div 6}{18 \div 6} = \frac{2}{3}$$

**Check**: $\frac{2}{3}$ cannot be simplified further because $2$ and $3$ share no common factors other than $1$. We say $\frac{2}{3}$ is in **lowest terms**.

## Step 3: Finding the least common denominator (LCD)

When we need to compare or add fractions with different denominators, we find a **common denominator** — ideally the **least common denominator (LCD)**.

Let's find the LCD of $\frac{3}{4}$ and $\frac{5}{6}$.

List multiples of each denominator:

- Multiples of $4$: $4, 8, 12, 16, 20, \ldots$
- Multiples of $6$: $6, 12, 18, 24, \ldots$

The smallest number that appears in both lists is $12$. The LCD is $12$.

Now convert both fractions to have denominator $12$:

$$\frac{3}{4} = \frac{3 \times 3}{4 \times 3} = \frac{9}{12}$$

$$\frac{5}{6} = \frac{5 \times 2}{6 \times 2} = \frac{10}{12}$$

**Check**: Both fractions now have denominator $12$, and we can compare them directly.

## Step 4: Comparing fractions

Now that $\frac{3}{4}$ and $\frac{5}{6}$ share a common denominator, we compare their numerators:

$$\frac{9}{12} \quad \text{vs} \quad \frac{10}{12}$$

Since $9 < 10$:

$$\frac{3}{4} < \frac{5}{6}$$

**Check**: $\frac{3}{4} = 0.75$ and $\frac{5}{6} \approx 0.833$, confirming that $\frac{3}{4}$ is indeed smaller.

## What we accomplished

You have learned to:

- Generate equivalent fractions by multiplying numerator and denominator by the same number
- Simplify fractions to lowest terms using the GCF
- Find the LCD of two fractions
- Compare fractions by converting to a common denominator

## Practice

Work through the interactive exercises: [Equivalent Fractions Exercises](../exercises/equivalent-fractions.py)

## Where to go next

- **Why does this work?** See [What Fractions Represent](../explanation/what-fractions-represent.md) for why multiplying top and bottom preserves the value.
- **Quick procedure**: See [How to Simplify a Fraction](../howto/simplify-a-fraction.md) for a concise reference you can use while working.
- **Next skill**: Continue to [Adding and Subtracting Fractions](adding-subtracting-fractions.md).
