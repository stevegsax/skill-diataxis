# Why Structure First

The most distinctive aspect of this tool's workflow is the insistence that
`diataxis.toml` is updated before any content changes. This is a deliberate
design decision, not a bureaucratic hurdle.

## The problem: documentation drift

Documentation projects tend to drift in two ways. Content drifts from its
original purpose — a tutorial gradually accumulates explanation, a reference
doc starts including step-by-step instructions. And the project as a whole
drifts from its plan — topics get added ad hoc, gaps appear, some areas get
exhaustive treatment while others are neglected.

Both kinds of drift happen slowly. No single commit looks wrong. But over
time, the documentation becomes a patchwork that doesn't serve anyone well.

## The structure document as a contract

`diataxis.toml` addresses drift by making the plan explicit and machine-readable.
The `covers` field for each file is a contract: these are the things this file
must address. The `detail` field sets expectations about depth and format. The
`guidance` field carries forward lessons learned.

When you score documentation, you score it against this contract. A tutorial
that drifts into explanation will fail the quadrant purity check. A reference
doc that skips items in `covers` will fail the coverage check. The structure
document makes drift measurable.

## Why structure changes come first

When a user asks to revise content — "make this simpler," "add a section about
X," "don't use that analogy" — the tempting thing is to jump straight into the
file and start editing. But if you do, the structure document no longer matches
the content. The next time someone (or something) regenerates or scores that
file, the old guidance applies, and the user's feedback is lost.

By updating `diataxis.toml` first — rewriting the `guidance` field to
incorporate the feedback, adding items to `covers` if needed — the feedback
becomes part of the contract. It persists across regeneration. It gets checked
during scoring. It can't be silently undone.

## The revision cycle

The structure-first approach produces a clear cycle:

```mermaid
flowchart LR
    A[User feedback] --> B[Update diataxis.toml]
    B --> C[Revise content]
    C --> D[Score]
    D --> A
```

The structure document is always the first thing updated and the last thing
checked. Content changes flow from it, and scoring validates against it.

## The guidance field as institutional memory

The `guidance` field evolves over time. It starts as a brief for initial content
generation: "use a simple example," "keep it under 500 words." As the project
matures, it accumulates the lessons learned from user feedback and scoring
results: "users found the pizza analogy confusing — use number lines instead,"
"this section needs at least two worked examples."

The key rule: feedback is integrated into the existing guidance text, not
appended as a separate block. The guidance should always read as if it were
written from scratch with full knowledge of everything learned so far. This
prevents the field from becoming a changelog and keeps it useful as a
generation brief.

## Parallel generation

A secondary benefit of the structure-first approach: because each file's
requirements are fully specified in `diataxis.toml`, files can be generated
independently and in parallel. Each subagent receives the full structure
document (for cross-linking context) but only needs to write its assigned
file. This scales well for large documentation projects.

For the specific fields and their formats, see the
[diataxis.toml Schema](../reference/diataxis-toml-schema.html). To see the
structure document in action, try the
[Writing diataxis.toml](../tutorials/writing-diataxis-toml.html) tutorial.
