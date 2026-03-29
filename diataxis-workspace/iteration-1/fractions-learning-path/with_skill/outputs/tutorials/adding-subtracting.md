# Tutorial: Adding and Subtracting Fractions

In this tutorial, we will learn to add and subtract fractions step by step. We
will start with the simplest case --- same denominators --- and work our way up
to mixed numbers with different denominators. By the end, you will be able to
combine any two fractions confidently.

We will use a cooking context throughout: imagine you are combining measured
ingredients.

## What we will need

- Comfort with fraction fundamentals (numerator, denominator, equivalent
  fractions, simplifying). If you need a refresher, start with the
  [Fraction Fundamentals Tutorial](fraction-fundamentals.md).

## Step 1: Adding fractions with the same denominator

Suppose you pour 1/4 cup of oil into a bowl, then add another 2/4 cup.

The denominators are the same (both fourths), so we simply add the numerators:

```
1/4 + 2/4 = (1 + 2)/4 = 3/4
```

You should see that we kept the denominator at 4 and only added the tops.

**Result**: 3/4 cup of oil in the bowl.

## Step 2: Why different denominators are a problem

Now suppose we need 1/3 cup of water and 1/4 cup of lemon juice. How much
liquid is that in total?

We cannot write 1/3 + 1/4 = 2/7. That would be wrong --- we would be adding
pieces of different sizes.

The rule is: **we can only add fractions when the pieces are the same size**,
meaning the denominators must match. We need a common denominator.

## Step 3: Finding the Least Common Denominator (LCD)

To add 1/3 + 1/4, we need a denominator that both 3 and 4 divide into evenly.

List multiples:

- Multiples of 3: 3, 6, 9, **12**, 15...
- Multiples of 4: 4, 8, **12**, 16...

The smallest shared multiple is **12**. That is our LCD.

## Step 4: Converting and adding

Now convert each fraction to twelfths:

```
1/3 = ?/12    -->   1 * 4 = 4,  3 * 4 = 12   -->   4/12
1/4 = ?/12    -->   1 * 3 = 3,  4 * 3 = 12   -->   3/12
```

Now add:

```
4/12 + 3/12 = 7/12
```

**Result**: 1/3 + 1/4 = 7/12 cup of liquid.

Notice that we multiplied each fraction's numerator and denominator by the same
number --- this creates equivalent fractions (same value, different
representation).

## Step 5: Subtracting fractions

Subtraction follows the exact same process. Suppose you have 3/4 cup of flour
and use 1/3 cup. How much is left?

1. Find the LCD of 4 and 3: **12**
2. Convert:
    - 3/4 = 9/12
    - 1/3 = 4/12
3. Subtract:
    - 9/12 - 4/12 = 5/12

**Result**: 5/12 cup of flour remains.

## Step 6: Adding and subtracting mixed numbers

You have 2 1/2 cups of broth and add 1 2/3 cups more. What is the total?

**Method**: Convert to improper fractions, then add.

1. Convert:
    - 2 1/2 = (2 * 2 + 1)/2 = 5/2
    - 1 2/3 = (1 * 3 + 2)/3 = 5/3

2. Find the LCD of 2 and 3: **6**

3. Convert:
    - 5/2 = 15/6
    - 5/3 = 10/6

4. Add:
    - 15/6 + 10/6 = 25/6

5. Convert back to a mixed number:
    - 25 / 6 = 4 remainder 1
    - 25/6 = 4 1/6

**Result**: 2 1/2 + 1 2/3 = 4 1/6 cups of broth.

## What we accomplished

In this tutorial, we:

- Added fractions with the same denominator by adding numerators
- Found the LCD to add fractions with different denominators
- Added fractions with different denominators using equivalent fractions
- Subtracted fractions using the same LCD method
- Added mixed numbers by converting to improper fractions first

## Where to go next

- For a concise, task-focused reference, see
  [How to Add and Subtract Fractions](../howto/add-subtract-fractions.md)
- For the complete rules table, see
  [Fraction Operations Reference](../reference/fraction-operations.md)
- For the conceptual background on why common denominators are needed, read
  [About Fraction Fundamentals](../explanation/fraction-fundamentals.md)
- To practice with interactive exercises, try the
  [Adding and Subtracting Exercises](../exercises/adding-subtracting.py)
