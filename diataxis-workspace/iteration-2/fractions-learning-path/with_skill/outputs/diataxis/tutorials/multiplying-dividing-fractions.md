# Multiplying and Dividing Fractions

In this tutorial, we will multiply and divide fractions step by step — including whole numbers and mixed numbers. By the end, you will be able to handle any fraction multiplication or division problem and simplify the result.

## What we need before starting

You should be comfortable with fraction notation and simplifying fractions. See the [Fraction Basics Tutorial](fraction-basics.md) if you need a refresher.

## Step 1: Multiplying two fractions

To multiply fractions, multiply the numerators together and the denominators together:

$$\frac{2}{3} \times \frac{4}{5} = \frac{2 \times 4}{3 \times 5} = \frac{8}{15}$$

**Check**: $\frac{2}{3} \approx 0.667$ and $\frac{4}{5} = 0.8$. Their product is about $0.533$, and $\frac{8}{15} \approx 0.533$. Correct.

## Step 2: Multiplying a fraction by a whole number

Write the whole number as a fraction with denominator $1$, then multiply as usual:

$$5 \times \frac{3}{4} = \frac{5}{1} \times \frac{3}{4} = \frac{15}{4} = 3\frac{3}{4}$$

**Check**: $5 \times 0.75 = 3.75 = 3\frac{3}{4}$. Correct.

## Step 3: Simplifying before multiplying (cross-cancellation)

We can simplify before multiplying to keep numbers small. Let's compute $\frac{4}{9} \times \frac{3}{8}$.

Look for common factors between any numerator and any denominator:

- $4$ and $8$ share factor $4$: divide $4 \to 1$ and $8 \to 2$
- $3$ and $9$ share factor $3$: divide $3 \to 1$ and $9 \to 3$

$$\frac{\cancel{4}^{\,1}}{\cancel{9}_{\,3}} \times \frac{\cancel{3}^{\,1}}{\cancel{8}_{\,2}} = \frac{1 \times 1}{3 \times 2} = \frac{1}{6}$$

**Check**: $\frac{4}{9} \approx 0.444$ and $\frac{3}{8} = 0.375$. Product $\approx 0.167 = \frac{1}{6}$. Correct.

## Step 4: Dividing fractions using the reciprocal

To divide by a fraction, multiply by its **reciprocal** (flip the second fraction):

$$\frac{2}{3} \div \frac{4}{5} = \frac{2}{3} \times \frac{5}{4} = \frac{10}{12} = \frac{5}{6}$$

**Check**: $\frac{2}{3} \approx 0.667$ divided by $\frac{4}{5} = 0.8$ gives about $0.833$, and $\frac{5}{6} \approx 0.833$. Correct.

## Step 5: Multiplying and dividing mixed numbers

Convert mixed numbers to improper fractions first, then proceed.

Let's compute $1\frac{1}{2} \times 2\frac{2}{3}$:

Convert: $1\frac{1}{2} = \frac{3}{2}$ and $2\frac{2}{3} = \frac{8}{3}$.

$$\frac{3}{2} \times \frac{8}{3}$$

Cross-cancel: $3$ and $3$ share factor $3$, and $2$ and $8$ share factor $2$:

$$\frac{\cancel{3}^{\,1}}{\cancel{2}_{\,1}} \times \frac{\cancel{8}^{\,4}}{\cancel{3}_{\,1}} = \frac{1 \times 4}{1 \times 1} = 4$$

**Check**: $1.5 \times 2.667 \approx 4$. Correct.

Now let's divide: $3\frac{1}{4} \div 1\frac{1}{2}$.

Convert: $3\frac{1}{4} = \frac{13}{4}$ and $1\frac{1}{2} = \frac{3}{2}$.

Flip the second fraction and multiply:

$$\frac{13}{4} \times \frac{2}{3} = \frac{13 \times 2}{4 \times 3} = \frac{26}{12} = \frac{13}{6} = 2\frac{1}{6}$$

**Check**: $3.25 \div 1.5 \approx 2.167$, and $2\frac{1}{6} \approx 2.167$. Correct.

## What we accomplished

You have learned to:

- Multiply two fractions by multiplying across
- Multiply a fraction by a whole number
- Use cross-cancellation to simplify before multiplying
- Divide fractions by multiplying by the reciprocal
- Handle mixed numbers in multiplication and division

## Practice

Work through the interactive exercises: [Multiplying and Dividing Exercises](../exercises/multiplying-dividing.py)

## Where to go next

- **Why does invert-and-multiply work?** See [Why Invert and Multiply?](../explanation/why-invert-and-multiply.md)
- **Quick procedure**: See [How to Divide Fractions](../howto/divide-fractions.md)
- **Next skill**: Continue to [Fraction Word Problems](fraction-word-problems.md)
