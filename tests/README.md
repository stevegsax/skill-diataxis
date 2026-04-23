# tests

Deterministic fixtures for the skill's `checks/` scripts. Each check
gets its own directory under `fixtures/` containing a minimal
`diataxis/`-shaped tree per scenario (typically `pass/` plus one or
more `fail-*/` variants) and a `run.sh` that encodes the expected
status per fixture. `run-all.sh` at this level invokes every
per-topic runner.

## Layout

```
tests/
├── README.md               (this file)
├── run-all.sh              (orchestrator)
└── fixtures/
    ├── duplicate-weights/
    │   ├── README.md
    │   ├── run.sh
    │   └── <fixture-dirs>
    ├── examples-section/
    ├── internal-links/
    ├── marimo-ast/
    ├── missing-static-assets/
    ├── orphan-exercises/
    ├── pre-hugo-project/   (corpus-only; no runner)
    ├── pyodide-imports/
    ├── todo-markers/
    └── weight-arithmetic/
```

Every fixture directory inside a topic is itself a minimal
`diataxis/`-shaped tree the check can run against. Fixtures
deliberately ship only the files the check inspects — content,
frontmatter, exercises — so a check failure is easy to reason about
and a regression in unrelated code does not ripple in.

## Adding a fixture for an existing check

1. Create a new directory under the topic folder. Name it `pass` if
   the check should return `"status": "pass"`, otherwise
   `fail-<reason>` with a short slug describing the scenario.
2. Populate the directory with only the files the check reads.
3. Add the expected status to the `expected` map in the topic's
   `run.sh`.

## Adding a new check

1. Write the check script under `skill/checks/check-<name>.nu`.
2. Register it in `skill/checks/run-checks.nu`.
3. Create `tests/fixtures/<topic>/` with `pass/` and `fail-*/`
   fixtures, a `run.sh` that asserts each fixture's expected status,
   and a `README.md` summarizing the scenarios.
4. `tests/run-all.sh` picks the new topic up automatically.

## Running

```bash
bash tests/run-all.sh                                  # whole battery
bash tests/fixtures/<topic>/run.sh                     # single topic
nu skill/checks/check-<name>.nu tests/fixtures/<topic>/<fixture>  # ad-hoc
```

## Related fixtures outside this tree

`evals/fixtures/` is a separate tree driven by the skill-creator
evaluation loop — those fixtures are whole-project inputs to Claude
runs, not direct inputs to the check scripts. The pre-Hugo corpus at
`tests/fixtures/pre-hugo-project/` is intentionally narrower and
exists only to exercise the detection logic in
`skill/scripts/upgrade_to_hugo.py --check`.
