+++
title = "The Diataxis Framework"
weight = 34
description = "Understanding and applying the Diataxis quadrant rules"
topic = "quadrants"
covers = ["The two axes (action/cognition, acquisition/application)", "Why four quadrants and not three or five", "The most common mistake (confusing tutorials with how-to guides)", "How quadrant boundaries improve documentation quality"]
detail = "Discursive. Connect to the reader's experience of bad documentation — tutorials that explain too much, reference docs that try to teach."
+++
Diataxis is a framework for organizing documentation, created by Daniele
Procida. The name comes from the Ancient Greek for "across" and "arrangement."
It claims that all documentation falls into exactly four types, determined by
two independent axes.

## The two axes

The first axis is **action vs. cognition**. Some documentation helps you *do*
things (practical knowledge). Other documentation helps you *understand* things
(theoretical knowledge).

The second axis is **acquisition vs. application**. Some documentation serves
you when you're *learning* (studying, building skill). Other documentation
serves you when you're *working* (applying skill to accomplish a goal).

These two axes produce four quadrants:

|                        | Acquisition (study) | Application (work) |
|------------------------|--------------------|--------------------|
| **Action** (doing)     | Tutorial           | How-to Guide       |
| **Cognition** (thinking) | Explanation       | Reference          |

## Why exactly four?

The framework argues this isn't an arbitrary taxonomy. The two axes are
genuinely independent — you can be studying or working, and you can be focused
on doing or on understanding. Two binary axes produce exactly four
combinations. Adding a fifth type would require a third axis, and Procida
argues no third axis exists.

Whether you accept this claim or not, the practical result is useful: four
types are few enough to remember and apply, and the axes give you a diagnostic
tool (the "compass") for classifying content.

## The most common mistake

The single most common documentation problem, according to the framework, is
confusing tutorials with how-to guides. Both contain steps. Both are practical.
But they serve fundamentally different needs.

A tutorial serves someone who is *learning*. The teacher bears responsibility
for the learner's success. The path is carefully chosen, choices are eliminated,
and the learner follows along. The goal is to build skill.

A how-to guide serves someone who is *working*. They already know what they want
to achieve. They need directions, not lessons. The guide assumes competence and
focuses on the task.

When these blur — when a tutorial offers choices, or a how-to guide tries to
teach — both suffer. The tutorial becomes confusing (too many options for a
learner). The how-to guide becomes tedious (too much explanation for someone who
just wants to get something done).

## How boundaries improve quality

Each quadrant has strict rules about what belongs in it. A tutorial must not
explain at length — it should link to an Explanation document instead. A
reference doc must not contain step-by-step instructions — it should link to a
How-to guide.

These boundaries feel restrictive at first. The natural instinct when writing a
tutorial is to explain *why* something works. The framework says: resist.
Provide a brief note and link elsewhere. This keeps each document focused on its
purpose and gives readers a clear path to the content they actually need.

The result is documentation where every page has a clear job. Readers know what
to expect. Tutorials guide without overwhelming. How-to guides stay focused.
Reference material is findable. Explanations provide depth without interrupting
the flow of practical work.

For the specific rules governing each quadrant, see the
[Quadrant Rules](../reference/quadrant-rules.html) reference. To see the
framework applied in practice, try the
[Your First Project](../tutorials/first-project.html) tutorial.
