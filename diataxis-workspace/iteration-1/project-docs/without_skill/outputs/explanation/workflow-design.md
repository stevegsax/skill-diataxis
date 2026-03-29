# About the Documentation Workflow

The skill-diataxis workflow follows a strict sequence: scope, structure, generate, score, revise, build. This ordering is intentional and reflects lessons about how documentation projects fail.

## Why Scope Before Structure

Documentation projects commonly fail by starting with content. A developer sits down to write docs, opens a blank file, and begins typing. The result is documentation shaped by whatever the author thinks of first, rather than by what the audience needs.

The scoping step (via the `grill-me` sub-skill) forces a conversation about audience, depth, boundaries, and purpose before any content planning happens. This conversation produces constraints that shape the structure document. Without scoping, the structure document tends to mirror the codebase rather than the audience's needs -- a common failure mode for project documentation.

For learning paths, scoping is even more important. The author needs to understand the learner's starting point, their goals, and whether they want exercises. A learning path for "help me understand Kubernetes" looks completely different depending on whether the learner is a developer who has used Docker or a project manager trying to understand architecture diagrams.

## Why Structure Before Content

The structure document (`diataxis.toml`) exists because of a coordination problem. In a documentation project with multiple files across four quadrants, the content of any one file depends on what the other files cover. A tutorial can be brief about a concept if there is an explanation document that covers it in depth. A how-to guide can skip setup steps if there is a tutorial that covers them.

Without a structure document, each file is written in isolation and the documentation develops gaps, redundancies, and boundary violations. The structure document solves this by making the full plan visible before any content is written. It assigns each piece of content to a specific file, specifies what that file must cover, and provides guidance for how to cover it.

The structure also enables parallel generation. Because each file's requirements are fully specified in the structure document, multiple files can be generated at the same time without coordination. Each generator receives the full structure (for cross-linking context) but only produces its own file.

## Why Score After Generation

Scoring provides a feedback signal that makes documentation quality measurable rather than subjective. Without scoring, revision is driven by gut feeling -- "this doesn't feel right" -- which is hard to act on systematically.

The scoring rubric converts the Diataxis framework rules and the project's structure document into checkable criteria. A score of 3 on "quadrant purity" for a tutorial means something specific: the tutorial contains content that belongs in another quadrant. The justification says exactly where the violation is. This makes revision targeted rather than diffuse.

Scoring also serves as a regression check. When a file is revised -- especially if it is regenerated rather than edited -- the new version might fix one issue while introducing another. Score comparison catches this by flagging any criterion that got worse.

## The Revision Cycle

The revision cycle is: structure first, content second, score third. This ordering prevents a common failure: changing content without updating the specification, then losing the change on the next regeneration.

When a user says "make this simpler" or "add more about X", the first step is to update the `guidance` field in `diataxis.toml` to record that intent. Only then is the content changed. This way, if the file is ever regenerated or scored again, the user's feedback is preserved in the structure document rather than existing only in the content file.

## Build as a Separate Step

The build step (converting markdown to HTML) is deliberately separated from content generation. The skill generates markdown files; the build script transforms them. This separation means the content authoring process does not need to think about HTML, templates, or navigation. It also means the build is deterministic -- running it twice on the same input produces the same output, because it uses pandoc rather than LLM generation for the transformation.

## Further Reading

- [Tutorial: Creating your first Diataxis documentation project](../tutorials/getting-started.md) -- experience the workflow firsthand
- [Structure document reference](../reference/structure-schema.md) -- the specification that drives the workflow
- [Scoring rubric reference](../reference/scoring-rubric.md) -- how quality is measured
