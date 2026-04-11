# Scoring Rubric

Scoring evaluates documentation against both the Diataxis framework rules and the
project's own structure document (`diataxis.toml`). Scores are tracked over time
so changes can be measured as improvements or regressions.

## Table of Contents

- [Score Levels](#score-levels)
- [Project-Level Scoring](#project-level-scoring)
- [Structural Scoring](#structural-scoring)
- [Quadrant Scoring](#quadrant-scoring)
- [Output Format](#output-format)
- [Comparison](#comparison)

---

## Score Levels

All scores use a 1-5 scale:

| Score | Meaning |
|-------|---------|
| 5 | Fully meets criteria, no issues |
| 4 | Meets criteria with minor issues |
| 3 | Partially meets criteria, some notable gaps |
| 2 | Significant gaps or violations |
| 1 | Does not meet criteria |

Each score includes a justification explaining why that score was given and what
would need to change to improve it. Justifications should be specific and
actionable.

---

## Project-Level Scoring

Evaluates the documentation as a whole.

### Criteria

**Topic decomposition** (weight: high)
- Are topics appropriately scoped — neither too broad nor too narrow?
- Is the subject covered at the right level of detail for the audience?
- Are there gaps in coverage? Redundancies between topics?
- Does the topic hierarchy make logical sense?

**Quadrant balance** (weight: medium)
- Are the four quadrants used appropriately for this project type?
- Is any quadrant over- or under-represented relative to the audience's needs?
- A learning-path project should lean toward Tutorials and Explanation
- A project-docs project should lean toward How-to and Reference

**Audience alignment** (weight: high)
- Does the complexity match the stated audience?
- Are prerequisites reasonable for the stated audience?
- Is the language level appropriate?

**Completeness** (weight: medium)
- What percentage of planned files have status "draft" or better?
- Are there topics with no content at all?

---

## Structural Scoring

Evaluates each file against its entry in `diataxis.toml`.

### Criteria

**Coverage** (weight: high)
- For each item in `covers`: is it addressed in the file?
- Score: proportion of items addressed, weighted by importance
- An item is "addressed" if a reader could find the information by reading the file

**Detail compliance** (weight: medium)
- Does the file match the depth and format described in `detail`?
- If `detail` says "tabular", is it tabular?
- If `detail` says "step-by-step with visual examples", are there steps and visuals?

**Guidance adherence** (weight: high)
- Does the file follow the instructions in `guidance`?
- Does it avoid what `guidance` says to avoid?
- This is evaluated item by item when `guidance` contains distinct instructions

**Cross-linking** (weight: medium)
- Does the file link to sibling quadrant documents?
- Are the links relevant and correctly placed?

**Exercise presence** (weight: low, tutorials only)
- If `exercises` are listed, do the corresponding marimo notebooks exist?
- Are they referenced/linked from the tutorial content?

---

## Quadrant Scoring

Evaluates whether each file follows the rules for its quadrant type. These rules
come from the Diataxis framework itself (see `references/quadrants.md`).

### Tutorial scoring

| Criterion | What to check |
|-----------|---------------|
| Action-oriented | Does every section contain steps for the learner to take? |
| Results shown | Are results/output shown after steps (within every 3 steps)? |
| Narrative of expected | Does it say what the learner should see/notice? |
| Minimal explanation | Are explanations brief (1-2 sentences max) with links? |
| No choices | Does it avoid presenting alternatives or options? |
| Completable | Does it reach a satisfying, defined endpoint? |
| Concrete | Does it work with specific examples, not abstract concepts? |

### How-to scoring

| Criterion | What to check |
|-----------|---------------|
| Task-focused | Does the title state a task? Does the content stay on task? |
| No teaching | Does it avoid explaining fundamentals? |
| Assumes competence | Does it skip basics the reader should already know? |
| Actionable steps | Is every step something the reader can do? |
| Real-world | Does it handle edge cases and complexity? |

### Reference scoring

| Criterion | What to check |
|-----------|---------------|
| Description only | Is the content neutral description, free of instruction? |
| Consistent structure | Do all items follow the same format/pattern? |
| Mirrors subject | Does the doc structure reflect the structure of what it describes? |
| Complete within scope | Are all items in the declared scope documented? |
| Brief examples | Are examples short and illustrative, not tutorial-like? |

### Explanation scoring

| Criterion | What to check |
|-----------|---------------|
| Answers "why" | Does it address reasons, context, and motivation? |
| Makes connections | Does it relate concepts to each other or to broader context? |
| No instructions | Does it avoid step-by-step procedures? |
| Provides context | Does it give background, history, or design rationale? |
| Topic-scoped | Is it bounded to a clear topic? |

### Cross-contamination detection

The most common scoring issue. Check for:
- Tutorial paragraphs that explain "why" at length (should link to Explanation)
- Reference sections that walk through steps (should link to How-to)
- How-to guides that teach from scratch (should link to Tutorial)
- Explanation that includes code listings as reference (should link to Reference)

---

## Prose Quality Scoring

You generated this content. That means you are biased toward it — you will
read your own sentences as clearer and tighter than they are. Compensate by
reading every paragraph as a skeptical editor looking for fat to cut. Score
prose quality on every file using these criteria.

### Scoring stance

Score like a copy editor with a red pen, not a peer reviewer giving
encouragement. The goal is documentation that respects the reader's time. A
paragraph that "basically works" is a 3, not a 4. Reserve 5 for prose you
cannot shorten without losing meaning.

### Criteria

**Fluff and filler** (weight: high)

Flag and penalize:

- Throat-clearing openers: "It is important to note that", "As we mentioned
  earlier", "In this section we will discuss"
- Empty qualifiers: "very", "really", "quite", "just", "simply", "basically",
  "actually", "essentially"
- Hedging without purpose: "it can be said that", "one might consider",
  "it is worth noting"
- Redundant phrasing: "in order to" (use "to"), "due to the fact that" (use
  "because"), "at this point in time" (use "now"), "the way in which" (use "how")
- Self-referential narration: "Let's now look at", "We will explore",
  "The following section covers" — the reader can see what the section covers
  by reading it

Every instance costs points. A file with three or more filler phrases cannot
score above 3.

**Active voice** (weight: high)

Use active voice when the agent is known. Passive voice obscures who does what,
which is the opposite of what documentation should do.

- Bad: "The configuration file is read by the parser at startup"
- Good: "The parser reads the configuration file at startup"
- Bad: "An error will be thrown if the input is invalid"
- Good: "The function throws an error if the input is invalid"

Passive voice is acceptable when the agent genuinely does not matter ("The file
is stored in `/tmp`") or when the subject is the focus ("The results are sorted
by score"). But if you can name who or what performs the action, do it.

A file where more than a third of sentences use unnecessary passive voice
cannot score above 3.

**Sentence economy** (weight: medium)

Every sentence should earn its place. Check for:

- Sentences that can be cut in half without losing meaning
- Two sentences that say the same thing in different words
- Paragraphs that make one point but take five sentences to get there
- Introductory sentences that just announce what comes next

If you can delete a sentence and the paragraph still makes sense, the sentence
should not be there.

**Concrete over abstract** (weight: medium)

Flag vague claims that don't tell the reader anything actionable:

- Bad: "This feature is useful for many scenarios"
- Good: "Use this when you need to batch-process files without loading them all
  into memory"
- Bad: "Understanding this concept helps with debugging"
- Good: "When a query returns no rows, check the join condition first — this is
  the most common cause"

A claim is concrete if the reader knows what to do differently after reading
it. If a sentence could apply to any project or any feature, it is too vague.

### Calibration examples

**Score 3/5** (passable but loose):

> It is important to understand that fractions represent parts of a whole. When
> we talk about adding fractions, what we really mean is that we are combining
> these parts together. In order to do this, the fractions need to have the same
> denominator. This is because the denominator tells us what kind of parts we
> are working with.

Problems: "It is important to understand that" (throat-clearing), "what we
really mean is" (filler), "In order to" (wordy), "This is because" (could be
folded into the previous sentence), passive voice throughout.

**Score 5/5** (tight, direct):

> Fractions represent parts of a whole. Adding fractions combines these parts —
> but only when they are the same kind of part. The denominator names the kind,
> so both fractions need the same denominator before you can add the numerators.

Same information, half the words. Active voice. No filler. Each sentence
advances the explanation.

### How prose quality interacts with other scores

Prose quality is scored separately but compounds with other dimensions. A
tutorial can follow every quadrant rule perfectly but still score 3 on prose
quality if the instructions are buried in padding. Conversely, beautifully
tight prose does not rescue a reference doc that gives step-by-step
instructions. Both matter.

---

## Output Format

Scores are stored in `scores.toml` in the project root. Each scoring run is
a timestamped entry preserving history for comparison.

```toml
[[runs]]
timestamp = "2025-03-29T14:30:00Z"
description = "Initial scoring after first draft"

[runs.project]
topic_decomposition = { score = 4, justification = "Topics are well-scoped but 'Advanced Operations' is too broad — consider splitting into sub-topics." }
quadrant_balance = { score = 3, justification = "Heavy on tutorials, missing most how-to guides. Appropriate for a learning path but how-tos would help retention." }
audience_alignment = { score = 5, justification = "Language and complexity match the stated audience of adult learners refreshing high school math." }
completeness = { score = 2, justification = "Only 4 of 12 planned files have drafts." }

[runs.files."tutorials/basic-ops.md"]
coverage = { score = 4, justification = "Covers 4 of 5 items in 'covers'. Missing: dividing fractions by flipping and multiplying." }
detail_compliance = { score = 5, justification = "Step-by-step format with worked examples as specified." }
guidance_adherence = { score = 3, justification = "Contains a 4-paragraph explanation of why common denominators are needed. Guidance says to link to explanation doc instead." }
cross_linking = { score = 2, justification = "No links to sibling quadrant documents." }
quadrant_purity = { score = 3, justification = "Two sections drift into explanation territory. Paragraphs starting 'The reason this works...' should be replaced with links." }
prose_quality = { score = 3, justification = "Multiple throat-clearing openers ('It is important to understand that', 'Let us now look at'). Step 3 uses passive voice in 4 of 6 sentences where the agent is known. The intro paragraph can be cut from 5 sentences to 2 without losing content." }

[runs.files."reference/fraction-operations.md"]
coverage = { score = 5, justification = "All items in 'covers' are addressed." }
detail_compliance = { score = 4, justification = "Mostly tabular. One section uses narrative prose where a table would be more appropriate." }
guidance_adherence = { score = 5, justification = "Follows all guidance notes." }
cross_linking = { score = 4, justification = "Links to how-to guides present. Missing link to explanation." }
quadrant_purity = { score = 5, justification = "Pure reference — describes without instructing or explaining." }
prose_quality = { score = 4, justification = "Mostly tight. One paragraph in the 'Operations' section uses 'in order to' twice and 'it should be noted that' once — trim these." }
```

---

## Comparison

Comparison is a post-processing step, not a shortcut. Produce a complete
fresh set of scores first: re-read each file, re-apply the rubric, write new
justifications. Only then load the most recent previous run from
`scores.toml` and diff against it. Never populate a new run by copying
scores forward from a previous one — the comparison is meaningless if both
sides come from the same source, and the user loses the signal they asked
for when they requested a re-score.

Once the fresh scores are ready, compare against the most recent previous run:

- **Improved**: score went up. Report the delta and what changed.
- **Regressed**: score went down. Flag this prominently — the user needs to know.
- **Unchanged**: score stayed the same. Note if the justification changed even
  if the number didn't.
- **New**: file was scored for the first time (no comparison available).

Present comparison as a summary table:

```
File                              Coverage  Detail  Guidance  Quadrant  Prose  Overall
tutorials/basic-ops.md            4 → 5     5 → 5   3 → 4     3 → 4   3 → 4   +4
reference/fraction-operations.md  5 → 5     4 → 5   5 → 5     5 → 5   4 → 5   +2
howto/add-fractions.md            NEW       NEW     NEW       NEW     NEW    (new)
```

Follow the table with specifics on what improved and what regressed.
