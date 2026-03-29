# About the Diataxis Framework

Diataxis is a framework for organizing technical documentation. The name comes from the Greek for "across arrangement" -- it arranges documentation across two axes to create four distinct types, each serving a different user need.

## The Problem Diataxis Solves

Most documentation fails not because it is poorly written, but because it tries to do too many things at once. A single page that explains a concept, walks through a tutorial, lists API parameters, and shows how to accomplish a task ends up serving none of these purposes well. The reader looking for a quick reference has to wade through tutorial steps. The learner following a tutorial gets lost in conceptual tangents. The practitioner trying to accomplish a task gets bogged down in theory.

Diataxis addresses this by separating documentation into types that have fundamentally different purposes and audiences. The separation is the framework's central insight: documentation that stays within its type is more useful than documentation that tries to be comprehensive on a single page.

## The Two Axes

The framework is built on two questions about any piece of documentation:

**Action or cognition?** Is this content about doing something (steps, procedures, hands-on work) or about understanding something (facts, concepts, reasons, context)?

**Acquisition or application?** Is the reader here to learn something new (study mode) or to get something done (work mode)?

These two binary axes produce four quadrants: tutorials (action + acquisition), how-to guides (action + application), explanation (cognition + acquisition), and reference (cognition + application).

## Why Separation Matters

The power of Diataxis comes not from the four types themselves -- most documentation systems recognize similar categories -- but from the insistence on keeping them separate.

A tutorial that pauses to explain why something works has shifted from action to cognition. The learner, who was in "doing" mode, is now being asked to switch to "thinking" mode. This is disorienting. The tutorial should instead link to an explanation document and keep moving.

A reference page that includes step-by-step instructions has shifted from application to acquisition. The practitioner, who came for a quick lookup, has to parse through instructional content to find the fact they need.

Cross-contamination is the most common documentation failure. Diataxis treats it as a defect to be detected and corrected, not a minor style issue.

## The Four Types in Practice

**Tutorials** are lessons. They guide a learner through a series of actions toward a meaningful result. The tutorial author controls the path -- there are no choices, no alternatives, no digressions. The goal is for the learner to succeed and build confidence. The analogy is teaching a child to cook: you choose the recipe, you prepare the ingredients, and you walk them through each step.

**How-to guides** are recipes. They address a specific real-world task and provide the steps to accomplish it. Unlike tutorials, they assume the reader already knows what they are doing and why. They handle real-world complexity rather than just the happy path. A how-to guide for "how to deploy to production" would cover rollback procedures and edge cases; a tutorial on deployment would not.

**Reference** is a map of the territory. It describes the machinery neutrally, factually, and completely. Reference material mirrors the structure of the thing it documents -- an API reference is organized the same way the API is organized, not by use case. It uses tables, consistent formatting, and short illustrative examples. It never instructs or explains.

**Explanation** is a discussion. It answers "why" questions, makes connections between concepts, and provides the background that makes the other three types more useful. It is the only type where opinions (clearly marked) are appropriate. Explanation passes the "bath test" -- it is worth reading away from the keyboard, without a code editor open.

## Diataxis in This Skill

The skill-diataxis project applies the Diataxis framework through a Claude Code skill. The skill manages the full documentation lifecycle: scoping what needs to be documented, structuring the content plan in a `diataxis.toml` file, generating content that follows the quadrant rules, scoring the result against both the framework rules and the project's own specifications, and revising based on scores and feedback.

The structure document (`diataxis.toml`) is the mechanism that connects the framework to practice. It translates the Diataxis quadrants into concrete file assignments with explicit coverage contracts, detail expectations, and guidance notes. Scoring then measures adherence to both the framework rules and the structure document, making documentation quality trackable and improvable over time.

## Further Reading

- [Quadrant rules reference](../reference/quadrant-rules.md) -- the specific rules for each documentation type
- [Scoring rubric reference](../reference/scoring-rubric.md) -- how documentation is evaluated against the framework
- [Tutorial: Creating your first Diataxis documentation project](../tutorials/getting-started.md) -- hands-on walkthrough
