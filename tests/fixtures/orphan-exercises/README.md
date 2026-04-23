# orphan-exercises fixtures

Minimal `diataxis/`-shaped directories that exercise
`skill/checks/check-orphan-exercises.nu`.

The check walks every `.py` file under `exercises/` and confirms at
least one tutorial's `exercises` list in `diataxis.toml` references
it. The inverse direction (tutorials referencing notebooks missing
on disk) is `check-exercise-exists`.

## The fixtures

| Fixture                  | on-disk notebooks   | referenced in diataxis.toml | expected status | scenario tested                                |
|--------------------------|---------------------|-----------------------------|-----------------|------------------------------------------------|
| `pass/`                  | `foo.py`            | `foo.py`                    | `pass`          | Every notebook is claimed by a tutorial.       |
| `fail-unreferenced/`     | `foo.py`, `bar.py`  | `foo.py`                    | `fail`          | `bar.py` has no tutorial pointing at it.       |

`run.sh` runs the check against each fixture and asserts the status
matches the table above.
