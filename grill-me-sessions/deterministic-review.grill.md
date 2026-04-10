# Grill Session: deterministic-review

Started: 2026-04-09
Last updated: 2026-04-09
Status: complete
Domain: software architecture / skill design

## Summary

Add a deterministic review capability to the diataxis skill that evaluates existing diataxis-structured documentation and suggests improvements. Fifteen nushell check scripts live in `skill/checks/`, each outputting JSON conforming to a shared schema. A runner invokes them via an explicit list and collects results. The checks run as part of Step 4 (scoring) — before LLM-based qualitative scoring. If any checks fail, the skill presents failures and suggestions to the user and waits for direction before proceeding. The checks are read-only reporters; the skill decides what to do with the results, asking the user when the fix isn't obvious.

## Decision Log

### DECIDED: Input scope
- **Decision**: Only review diataxis-structured documentation in a `diataxis/` directory with a `diataxis.toml`. Both project types (learning-path, project-docs) handled, but type-specific checks deferred.
- **Rationale**: The skill created the documentation, so we can assume the structure exists. Type-specific checks add complexity without broad value yet.
- **Date**: 2026-04-09

### DECIDED: Structural drift detection
- **Decision**: Check files listed in diataxis.toml that don't exist on disk, orphan files on disk not in the TOML, status/file consistency, and exercise path validity. When drift is found, the skill asks the user whether to update the .toml or revert the .md.
- **Rationale**: These are all deterministic filesystem checks that don't require LLM judgment.
- **Date**: 2026-04-09

### DECIDED: One nushell script per check
- **Decision**: Each check is a separate nushell script. Scripts output a JSON object conforming to a shared schema. A runner script invokes all checks via an explicit list and collects results.
- **Rationale**: Keeps checks independent, testable, and composable. Nushell gives native TOML parsing, typed structured data, and clean JSON output. Explicit list over glob for control over ordering and the ability to skip checks.
- **Date**: 2026-04-09

### DECIDED: Output schema
- **Decision**: Per-check output: `{check, status (pass|fail|skip|error), evidence: [{file, line?, detail}], suggestions: [string]}`. Runner output: `{diataxis_dir, timestamp, results: [...], summary: {pass, fail, skip, error}}`. Suggestions are machine-readable, co-located with detection logic in each script. JSON Schema validates script output. `error` status for when a check script itself breaks (runner wraps in try/catch and synthesizes an error result).
- **Rationale**: Structured evidence enables downstream tooling. Machine-oriented suggestions let the skill act on results. Schema contract keeps scripts honest. Error handling prevents one broken check from killing the run.
- **Date**: 2026-04-09

### DECIDED: Nushell over bash
- **Decision**: Write all check scripts and the runner in nushell. Shared functions live in a module (`mod.nu`).
- **Rationale**: Native TOML parsing, native JSON output, typed pipelines, module system for shared code. Eliminates jq/yq string-escaping complexity. nu is an acceptable dependency alongside uv, pandoc, mmdc.
- **Date**: 2026-04-09

### DECIDED: Checks are read-only reporters
- **Decision**: Check scripts only report findings. They never modify files. The skill reads the results and decides what to do — auto-fixing mechanical issues and asking the user when the fix isn't obvious.
- **Rationale**: Clean separation of concerns. Tests are pure functions from filesystem to JSON. The LLM is the actor with judgment about what's mechanical vs what needs user input.
- **Date**: 2026-04-09

### DECIDED: Integration with skill workflow
- **Decision**: Run deterministic checks as the first part of Step 4 (scoring), before LLM-based qualitative scoring. If any checks fail, present failures and suggestions to the user and wait for direction. User can fix and re-run, or say "score anyway."
- **Rationale**: Avoids wasting LLM scoring effort on docs with broken structure. Consistent with drift detection decision — skill surfaces issues and waits for user direction.
- **Date**: 2026-04-09

### DECIDED: No CLI integration
- **Decision**: Checks are invoked by the skill via `nu checks/run-checks.nu <diataxis_dir>` from the skill directory. Not exposed through the `diataxis` Python CLI.
- **Rationale**: The checks are skill-facing, not human-facing. The Python CLI is a build tool for humans. These are different consumers with different needs.
- **Date**: 2026-04-09

## Checks to Implement

### Structural checks
1. `check-toml-valid.nu` — TOML syntax validation
2. `check-toml-topics.nu` — at least one topic defined
3. `check-purpose-field.nu` — `purpose` field exists in `[project]`
4. `check-quadrant-files.nu` — all 4 quadrant dirs have content files
5. `check-orphan-files.nu` — files on disk in quadrant dirs not listed in TOML
6. `check-status-consistency.nu` — status says "draft"+ but file is empty/missing
7. `check-exercise-exists.nu` — exercise paths in TOML point to real files

### Format checks
8. `check-marimo-format.nu` — exercise files are valid marimo notebooks
9. `check-latex-math.nu` — math uses LaTeX, not plain text fractions
10. `check-guidance-coherent.nu` — no "REVISION FEEDBACK:" blocks in guidance

### Quadrant rule checks
11. `check-howto-titles.nu` — how-to titles start with "How to"
12. `check-tables-in-reference.nu` — reference docs use tables/structured lists
13. `check-step-by-step.nu` — tutorials have steps and show results
14. `check-code-examples.nu` — tutorials have code blocks

### Cross-linking checks
15. `check-cross-links.nu` — files link to sibling quadrant docs

## File Layout

```
skill/checks/
├── mod.nu                      # shared module
├── run-checks.nu               # runner with explicit check list
├── check-schema.json           # JSON Schema for per-check output
├── check-toml-valid.nu
├── check-toml-topics.nu
├── check-purpose-field.nu
├── check-quadrant-files.nu
├── check-orphan-files.nu
├── check-status-consistency.nu
├── check-exercise-exists.nu
├── check-marimo-format.nu
├── check-latex-math.nu
├── check-guidance-coherent.nu
├── check-howto-titles.nu
├── check-tables-in-reference.nu
├── check-step-by-step.nu
├── check-code-examples.nu
└── check-cross-links.nu
```

## Parking Lot

- Type-specific checks (learning-path vs project-docs)
- Content drift detection (covers items vs actual file content) — requires LLM, separate project
- Human-readable report formatting
- Exposing checks to humans via CLI or separate runner
