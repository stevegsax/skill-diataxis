# Diataxis Quadrant Rules

These rules govern what belongs in each documentation type. They are used both
for generating content and for scoring adherence. Violations of these rules
are scoring penalties.

The four quadrants are presented in this order throughout the skill and the
rendered site: **Explanation → Tutorials → How-to Guides → Reference**.
Explanation frames the subject before readers act on it; Tutorials and How-to
Guides follow for readers ready to work; Reference is the lookup surface,
last because it presupposes the reader already knows what to look up.

## Table of Contents

- [Explanation](#explanation)
- [Tutorials](#tutorials)
- [How-to Guides](#how-to-guides)
- [Reference](#reference)
- [Cross-referencing](#cross-referencing)
- [The Compass](#the-compass)

---

## Explanation

**Purpose**: Discursive treatment that deepens and broadens understanding.

**Serves**: Acquisition of skill through cognition.

**Analogy**: An article on culinary social history.

### What explanation must do

- Answer "why?" and "can you tell me about...?"
- Make connections — to other concepts, to history, to alternatives
- Provide context: background, design decisions, constraints, tradeoffs
- Discuss the subject from a higher perspective
- Acknowledge that multiple perspectives or approaches exist

### What explanation must not do

- Provide instructions or steps (link to Tutorial or How-to)
- Include technical descriptions that belong in Reference
- Become a dumping ground for content that doesn't fit elsewhere

### Language patterns

- "The reason for X is because historically, Y..."
- "W is better than Z in this context because..."
- "An X in this system is analogous to a Y in..."
- "Some practitioners prefer W because Z. This can work, but..."

### Structural rules

- Each document has a clear topic (you could prefix the title with "About")
- Discursive prose, not lists or tables (those belong in Reference)
- Can contain opinions, clearly marked as such
- Links to Reference for factual details, to How-to for practical application
- Passes the "bath test": worth reading away from the keyboard

---

## Tutorials

**Purpose**: A lesson where the learner acquires skill by doing something
meaningful under guidance.

**Serves**: Acquisition of skill through action.

**Analogy**: Teaching a child to cook.

### What a tutorial must do

- Guide the learner through a series of concrete steps toward a meaningful result
- Show results early and often — never let more than 3 steps pass without visible
  output
- Maintain a narrative of the expected: "You will notice that...", "The output
  should look something like..."
- Point out what the learner should notice — close the loop between action and
  observation
- Be reliable: it must work for every user, every time
- Be completable: the learner reaches a satisfying endpoint
- Start with where the learner will end up: "In this tutorial we will create X.
  Along the way we will encounter Y."

### What a tutorial must not do

- Explain why things work (link to Explanation instead)
- Offer choices or alternatives (stay on the one path)
- Present options, configurations, or flags
- Use abstract language when concrete will do
- Generalize from the specific case
- Include reference material for completeness

### Language patterns

- First person plural: "We will...", "Let's..."
- Imperative for actions: "First, do X. Now, do Y."
- Narrative connectors: "Notice that...", "You should see..."
- Result statements: "You have built a..."

### Structural rules

- Open with a description of the goal and what the learner will encounter
- Each step produces a visible, comprehensible result
- End with a summary of what was accomplished
- Link to related Explanation, How-to, and Reference docs at the end

---

## How-to Guides

**Purpose**: Directions that guide the reader through a real-world problem to a
result.

**Serves**: Application of skill through action.

**Analogy**: A recipe in a cookbook.

### What a how-to guide must do

- Address a real-world problem or task (defined by user need, not tool capability)
- Provide a sequence of actionable steps
- Assume the reader already knows what they want and has basic competence
- Stay focused on the goal — no tangents
- Handle real-world complexity (not just the happy path)
- Start and end at practical boundaries (not necessarily end-to-end)

### What a how-to guide must not do

- Teach (this is not a tutorial — don't explain fundamentals)
- Explain why (link to Explanation instead)
- Include exhaustive reference material (link to Reference instead)
- Wander from the task at hand

### Language patterns

- Title starts with "How to..."
- "This guide shows you how to..."
- Conditional imperatives: "If you want X, do Y."
- "Refer to the X reference for a full list of options."

### Structural rules

- Title clearly states the task
- Brief introduction (1-2 sentences) stating what the guide achieves
- Numbered or ordered steps
- Each step is an action (possibly including judgment)
- Link to Reference for details, Explanation for context

---

## Reference

**Purpose**: Technical description of the machinery. A map of the territory.

**Serves**: Application of skill through cognition.

**Analogy**: Information on the back of a food packet.

### What reference must do

- Describe, and only describe — neutral, factual, authoritative
- Mirror the structure of the thing being documented (APIs documented in the same
  hierarchy as the code, for example)
- Adopt consistent, standard patterns throughout
- Provide brief examples that illustrate usage without becoming tutorials
- Be complete within its defined scope

### What reference must not do

- Instruct (link to How-to or Tutorial instead)
- Explain (link to Explanation instead)
- Contain opinions or recommendations
- Use narrative or discursive prose
- Deviate from the structural pattern established in the section

### Language patterns

- Declarative statements: "The function accepts two arguments."
- Factual lists: "Supported formats are: A, B, C."
- Warnings where needed: "Must not be called before initialization."

### Structural rules

- Structure mirrors the product/subject structure
- Consistent formatting throughout (if one function gets a parameters table,
  they all do)
- Tables for structured data (parameters, options, properties)
- Examples are short (1-3 lines) and illustrative, not instructional
- Link to How-to for "how do I use this" questions

---

## Cross-referencing

Each document should link to its siblings in other quadrants. The rule is:
**link, don't embed**.

| From | Link to | Why |
|------|---------|-----|
| Explanation | Tutorial | "To try this yourself, see the tutorial..." |
| Explanation | Reference | "For technical details, see..." |
| Tutorial | Explanation | "For more on why this works, see..." |
| Tutorial | Reference | "For the full list of options, see..." |
| How-to | Reference | "See the X reference for all parameters." |
| How-to | Explanation | "For background on this approach, see..." |
| Reference | How-to | "For a guide on using X, see..." |

A document that embeds content from another quadrant is violating boundaries.
For example, a tutorial that contains a long explanation of why something works
should instead link to the Explanation document.

---

## The Compass

Two questions classify any piece of content:

1. **Does this inform action or cognition?**
   - Action: steps, procedures, things to do
   - Cognition: facts, concepts, reasons, context

2. **Does this serve acquisition or application?**
   - Acquisition: the user is learning/studying
   - Application: the user is working/doing their job

Apply at any granularity — a sentence, a paragraph, or a whole document. When a
paragraph in a tutorial is answering "why?", it has drifted into Explanation
territory. When a reference document starts walking through steps, it has drifted
into How-to territory.
