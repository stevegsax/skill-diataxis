# Why Diataxis?

Most documentation fails not because it is poorly written, but because it tries to do too many things at once. A single page walks you through setup steps, explains the design philosophy, lists every configuration option, and teaches you the fundamentals -- all interwoven. The reader looking for a quick answer has to wade through tutorials. The learner trying to build understanding keeps getting interrupted by reference tables.

Diataxis addresses this by recognizing that documentation serves four fundamentally different needs, and that mixing them degrades all of them.

## The Two Axes

Diataxis classifies documentation along two independent axes:

**Action vs. Cognition.** Some documentation guides the reader through doing something (action). Other documentation helps the reader understand something (cognition). These are different activities that require different writing styles, different structures, and different reader mindsets.

**Acquisition vs. Application.** Some documentation serves a reader who is learning (acquisition). Other documentation serves a reader who is working and needs to get something done (application). A learner needs different things than a practitioner, even when the subject is the same.

Crossing these two axes produces four quadrants:

- **Tutorial** (action + acquisition): Guided lessons where the learner does something meaningful under supervision. The reader is learning by doing.
- **How-to guide** (action + application): Task-focused directions for a reader who already knows the basics and needs to accomplish something specific.
- **Reference** (cognition + application): Technical descriptions of the machinery -- APIs, configuration options, specifications. The reader consults this while working.
- **Explanation** (cognition + acquisition): Discursive treatment that deepens understanding -- the "why" behind decisions, historical context, tradeoffs, and connections between concepts.

## Why Separation Matters

The power of Diataxis comes from keeping these quadrants distinct. When content bleeds across boundaries, it degrades the documentation in predictable ways:

A tutorial that pauses to explain theory breaks the learner's flow. They were building momentum through action, and now they are reading an essay. The explanation would be valuable in its own document, but embedded in a tutorial it becomes an obstacle.

A reference page that walks through "how to use this function" is no longer a reliable lookup resource. The reader scanning for a parameter type has to skip past instructional prose to find it. The how-to content would be useful in a guide, but in a reference it creates noise.

A how-to guide that teaches from scratch is frustrating for the competent reader who just needs the steps. They already understand the concepts -- they need the recipe, not the cooking lesson.

By keeping quadrants separate and linking between them, each document can do its one job well. The tutorial links to the explanation for readers who want the "why." The reference links to the how-to for readers who want practical guidance. Every reader finds what they need without wading through content meant for someone else.

## Project Documentation vs. Learning Paths

The Diataxis skill supports two project types that shift the emphasis across quadrants:

**Project documentation** (`type = "project-docs"`) documents a codebase or tool. It leans toward how-to guides and reference material because the audience is primarily practitioners who need to get work done. Tutorials help new users get started, and explanations provide context for design decisions, but the bulk of the content is practical.

**Learning paths** (`type = "learning-path"`) teach a subject. They lean toward tutorials and explanation because the audience is primarily learners who need to build both skills and understanding. Reference material supports the learning, and how-to guides help apply new knowledge, but the emphasis is on acquisition.

Choosing the right type shapes the structure document and guides both content generation and scoring toward the appropriate balance.

## The Structure Document as Source of Truth

Rather than letting documentation grow organically (which inevitably leads to the mixed-concerns problem), Diataxis projects start with a structure document (`diataxis.toml`) that defines every topic, every file, and what each file must cover. This is deliberate: the structure is designed before content is written, and any structural changes are made in the structure document before they are reflected in content.

This approach has a practical benefit beyond organization. Because each file's requirements are fully specified -- what it covers, at what level of detail, with what guidance -- files can be generated, scored, and revised independently. The structure document makes the documentation project manageable even as it grows.

## Further Reading

- To try creating a Diataxis project yourself, see the [Getting Started Tutorial](../tutorials/first-documentation-project.md)
- For the structure document schema, see the [Structure Document Reference](../reference/structure-document-schema.md)
- For the specific rules governing each quadrant, see the [Quadrant Rules Reference](../reference/quadrant-rules.md)
