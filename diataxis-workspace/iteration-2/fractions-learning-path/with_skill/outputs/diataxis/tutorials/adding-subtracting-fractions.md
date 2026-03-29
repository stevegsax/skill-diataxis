# Adding and Subtracting Fractions

In this tutorial, we will add and subtract fractions step by step — starting with same-denominator cases, then moving to different denominators, and finally handling mixed numbers. By the end, you will be able to add or subtract any pair of fractions and simplify the result.

## What we need before starting

You should be comfortable with equivalent fractions and finding the LCD. See the [Equivalent Fractions Tutorial](equivalent-fractions.md) if you need a refresher.

## Step 1: Adding fractions with the same denominator

When two fractions share a denominator, we add the numerators and keep the denominator:

$$\frac{2}{7} + \frac{3}{7} = \frac{2 + 3}{7} = \frac{5}{7}$$

**Check**: We started with $\frac{2}{7}$ and $\frac{3}{7}$, both in sevenths. Adding $2$ parts and $3$ parts gives $5$ parts, so $\frac{5}{7}$.

## Step 2: Adding fractions with different denominators

Let's add $\frac{1}{3} + \frac{1}{4}$.

First, find the LCD. The LCD of $3$ and $4$ is $12$.

Convert each fraction:

$$\frac{1}{3} = \frac{1 \times 4}{3 \times 4} = \frac{4}{12}$$

$$\frac{1}{4} = \frac{1 \times 3}{4 \times 3} = \frac{3}{12}$$

Now add:

$$\frac{4}{12} + \frac{3}{12} = \frac{7}{12}$$

**Check**: $\frac{1}{3} \approx 0.333$ and $\frac{1}{4} = 0.25$, so the sum should be about $0.583$. And $\frac{7}{12} \approx 0.583$. Correct.

## Step 3: Subtracting fractions

Subtraction works the same way. Let's compute $\frac{5}{6} - \frac{1}{4}$.

The LCD of $6$ and $4$ is $12$.

$$\frac{5}{6} = \frac{5 \times 2}{6 \times 2} = \frac{10}{12}$$

$$\frac{1}{4} = \frac{1 \times 3}{4 \times 3} = \frac{3}{12}$$

$$\frac{10}{12} - \frac{3}{12} = \frac{7}{12}$$

**Check**: $\frac{5}{6} \approx 0.833$ and $\frac{1}{4} = 0.25$, so the difference should be about $0.583$. And $\frac{7}{12} \approx 0.583$. Correct.

## Step 4: Adding mixed numbers

Let's add $2\frac{1}{3} + 1\frac{3}{4}$.

**Method**: Add the whole number parts and the fraction parts separately.

Whole numbers: $2 + 1 = 3$.

Fractions: $\frac{1}{3} + \frac{3}{4}$. The LCD is $12$:

$$\frac{1}{3} + \frac{3}{4} = \frac{4}{12} + \frac{9}{12} = \frac{13}{12}$$

Since $\frac{13}{12}$ is improper, convert it: $\frac{13}{12} = 1\frac{1}{12}$.

Combine with the whole number sum:

$$3 + 1\frac{1}{12} = 4\frac{1}{12}$$

**Check**: $2\frac{1}{3} \approx 2.333$ and $1\frac{3}{4} = 1.75$. Their sum is about $4.083$, and $4\frac{1}{12} \approx 4.083$. Correct.

## Step 5: Simplifying the result

Always check whether your answer can be simplified. Let's compute $\frac{3}{8} + \frac{1}{8}$:

$$\frac{3}{8} + \frac{1}{8} = \frac{4}{8}$$

Now simplify. The GCF of $4$ and $8$ is $4$:

$$\frac{4}{8} = \frac{4 \div 4}{8 \div 4} = \frac{1}{2}$$

**Check**: $\frac{3}{8} = 0.375$ and $\frac{1}{8} = 0.125$. Sum is $0.5 = \frac{1}{2}$. Correct.

## What we accomplished

You have learned to:

- Add and subtract fractions with the same denominator
- Add and subtract fractions with different denominators by finding the LCD
- Add and subtract mixed numbers
- Simplify the result after each operation

## Practice

Work through the interactive exercises: [Adding and Subtracting Exercises](../exercises/adding-subtracting.py)

## Where to go next

- **Why do we need common denominators?** See [Why Common Denominators?](../explanation/why-common-denominators.md)
- **Rules at a glance**: See the [Addition and Subtraction Rules Reference](../reference/fraction-addition-subtraction-rules.md)
- **Quick procedure**: See [How to Add Fractions with Unlike Denominators](../howto/add-fractions-with-unlike-denominators.md)
- **Next skill**: Continue to [Multiplying and Dividing Fractions](multiplying-dividing-fractions.md)
