# Quadrant Rules Reference

The Diataxis framework organizes documentation into four quadrants based on two axes.

## Quadrant Map

|                    | Acquisition (study) | Application (work) |
|--------------------|--------------------|--------------------|
| **Action** (doing) | Tutorial           | How-to Guide       |
| **Cognition** (thinking) | Explanation  | Reference          |

## Tutorial

**Purpose**: A lesson where the learner acquires skill by doing.

| Rule | Description |
|------|-------------|
| Guide action | Every section contains concrete steps toward a meaningful result |
| Show results | Visible output within every 3 steps |
| Narrate expectations | State what the learner should see: "You will notice that..." |
| Minimize explanation | 1-2 sentences max; link to Explanation for depth |
| No choices | Stay on one path; do not present alternatives or options |
| Completable | Reach a satisfying, defined endpoint |
| Concrete | Use specific examples, not abstract concepts |

**Language**: First person plural ("We will..."), imperative for actions ("First, do X"), narrative connectors ("Notice that...").

**Links to**: Explanation (for why), Reference (for full details), How-to (for related tasks).

## How-to Guide

**Purpose**: Directions that guide the reader through a real-world task.

| Rule | Description |
|------|-------------|
| Task-focused | Title states the task; content stays on that task |
| No teaching | Do not explain fundamentals; link to Tutorial |
| Assume competence | Skip basics the reader should already know |
| Actionable steps | Every step is something the reader can do |
| Real-world | Handle edge cases and complexity, not just the happy path |

**Language**: Title starts with "How to..."; conditional imperatives ("If you want X, do Y"); references to other docs ("Refer to the X reference for...").

**Links to**: Reference (for details), Explanation (for context).

## Reference

**Purpose**: Technical description of the machinery.

| Rule | Description |
|------|-------------|
| Describe only | Neutral, factual, authoritative; no instruction |
| Mirror subject | Structure reflects the structure of what it documents |
| Consistent format | All items get the same treatment (tables, headings, etc.) |
| Complete within scope | All items in the declared scope are documented |
| Brief examples | 1-3 lines, illustrative, not instructional |

**Language**: Declarative statements ("The function accepts two arguments"), factual lists, warnings where needed.

**Links to**: How-to (for usage guidance), Explanation (for rationale).

## Explanation

**Purpose**: Discursive treatment that deepens and broadens understanding.

| Rule | Description |
|------|-------------|
| Answer "why" | Address reasons, context, and motivation |
| Make connections | Relate concepts to each other, to history, to alternatives |
| No instructions | Do not provide steps or procedures |
| Provide context | Background, design decisions, constraints, tradeoffs |
| Topic-scoped | Bounded to a clear topic (title could be prefixed with "About") |

**Language**: "The reason for X is...", "W is better than Z in this context because...", "An X in this system is analogous to...".

**Links to**: Tutorial (for hands-on practice), Reference (for factual details).

## Cross-Referencing Rule

Link, do not embed. A document that contains extended content from another quadrant is violating boundaries.

| From | Link to | Pattern |
|------|---------|---------|
| Tutorial | Explanation | "For more on why this works, see..." |
| Tutorial | Reference | "For the full list of options, see..." |
| How-to | Reference | "See the X reference for all parameters." |
| How-to | Explanation | "For background on this approach, see..." |
| Reference | How-to | "For a guide on using X, see..." |
| Explanation | Tutorial | "To try this yourself, see the tutorial..." |
| Explanation | Reference | "For technical details, see..." |

## The Compass

Two questions classify any content:

1. **Action or cognition?** Steps and procedures vs. facts, concepts, and reasons.
2. **Acquisition or application?** Learning/studying vs. working/doing a job.

Apply at any granularity -- a sentence, a paragraph, or a whole document. When content drifts across a boundary, it should be moved or replaced with a link.
