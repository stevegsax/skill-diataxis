# Quadrant Rules

Each Diataxis quadrant has strict rules about what belongs in it. These rules govern both content generation and scoring. Content that violates these rules incurs scoring penalties.

## The Four Quadrants

|                            | Acquisition (study) | Application (work) |
|----------------------------|--------------------|--------------------|
| **Action** (doing)         | Tutorial           | How-to Guide       |
| **Cognition** (thinking)   | Explanation        | Reference          |

## Tutorial

**Purpose**: A lesson where the learner acquires skill by doing something meaningful under guidance.

### Must Do

| Rule | Description |
|------|-------------|
| Guide action | Every section contains steps for the learner to take |
| Show results | Results/output shown within every 3 steps |
| Narrate the expected | "You will notice that...", "The output should look like..." |
| Be reliable | Must work for every user, every time |
| Be completable | Reaches a satisfying, defined endpoint |
| Start with the goal | Open with where the learner will end up |

### Must Not Do

| Rule | Description |
|------|-------------|
| Explain why | Link to Explanation instead |
| Offer choices | Stay on one path; no alternatives or options |
| Present options/flags | No configuration exploration |
| Use abstract language | Concrete examples over abstract concepts |
| Include reference material | Link to Reference instead |

### Language Patterns

- First person plural: "We will...", "Let's..."
- Imperative for actions: "First, do X. Now, do Y."
- Narrative connectors: "Notice that...", "You should see..."
- Result statements: "You have built a..."

## How-to Guide

**Purpose**: Directions that guide the reader through a real-world problem to a result.

### Must Do

| Rule | Description |
|------|-------------|
| Address a real task | Defined by user need, not tool capability |
| Provide actionable steps | Each step is something the reader can do |
| Assume competence | Reader already knows the basics |
| Stay focused | No tangents from the task |
| Handle complexity | Address edge cases, not just the happy path |

### Must Not Do

| Rule | Description |
|------|-------------|
| Teach | Do not explain fundamentals; link to Tutorial |
| Explain why | Link to Explanation instead |
| Include exhaustive reference | Link to Reference instead |
| Wander | Stay on the task |

### Language Patterns

- Title starts with "How to..."
- "This guide shows you how to..."
- Conditional imperatives: "If you want X, do Y."
- "Refer to the X reference for a full list of options."

## Reference

**Purpose**: Technical description of the machinery.

### Must Do

| Rule | Description |
|------|-------------|
| Describe only | Neutral, factual, authoritative |
| Mirror structure | Documentation hierarchy matches the subject's hierarchy |
| Be consistent | Same format/pattern for every item in a section |
| Include brief examples | 1-3 lines, illustrative, not instructional |
| Be complete | Cover everything within the declared scope |

### Must Not Do

| Rule | Description |
|------|-------------|
| Instruct | Link to How-to or Tutorial instead |
| Explain | Link to Explanation instead |
| Contain opinions | No recommendations |
| Use narrative prose | Tables and structured descriptions |
| Deviate from pattern | Consistent formatting throughout |

### Language Patterns

- Declarative: "The function accepts two arguments."
- Factual lists: "Supported formats are: A, B, C."
- Warnings: "Must not be called before initialization."

## Explanation

**Purpose**: Discursive treatment that deepens and broadens understanding.

### Must Do

| Rule | Description |
|------|-------------|
| Answer "why" | Reasons, context, motivation |
| Make connections | Relate concepts to each other and broader context |
| Provide context | Background, history, design rationale |
| Discuss perspectives | Acknowledge alternatives and tradeoffs |
| Stay topic-scoped | Bounded to a clear topic |

### Must Not Do

| Rule | Description |
|------|-------------|
| Provide instructions | Link to Tutorial or How-to |
| Include technical specs | Link to Reference |
| Become a dumping ground | Only content that answers "why" |

### Language Patterns

- "The reason for X is because historically, Y..."
- "W is better than Z in this context because..."
- "An X in this system is analogous to a Y in..."

## Cross-Referencing Rules

Each document links to its siblings in other quadrants. The rule is: link, do not embed.

| From | Link to | Reason |
|------|---------|--------|
| Tutorial | Explanation | "For more on why this works, see..." |
| Tutorial | Reference | "For the full list of options, see..." |
| How-to | Reference | "See the X reference for all parameters." |
| How-to | Explanation | "For background on this approach, see..." |
| Reference | How-to | "For a guide on using X, see..." |
| Explanation | Tutorial | "To try this yourself, see the tutorial..." |
| Explanation | Reference | "For technical details, see..." |

## The Compass

Two questions classify any piece of content:

1. **Action or cognition?** Steps and procedures (action) vs. facts, concepts, and reasons (cognition).
2. **Acquisition or application?** The reader is learning (acquisition) vs. working (application).

Apply at any granularity -- a sentence, a paragraph, or a whole document. When a paragraph in a tutorial answers "why?", it has drifted into Explanation. When a reference page walks through steps, it has drifted into How-to.

## Further Reading

- For why these rules matter, see [Why Diataxis?](../explanation/why-diataxis.md)
- For how to address scoring findings related to these rules, see [How to Score and Revise Documentation](../howto/score-and-revise.md)
