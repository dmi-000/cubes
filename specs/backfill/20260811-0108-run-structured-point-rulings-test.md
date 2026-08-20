# Run structured-point rulings test

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-08-11T01:08:33 |
| Agent type | general-purpose |
| Model override | sonnet |
| Session | `833a739b-86d7-4754-94e1-446688dfcac3` |
| Tool-use id | `toolu_01LE57VMV7Rv1SAtsr8yAu7X` |
| Files named | `detq_check.py`, `exact_chambers.py`, `rulings.py`, `rulings_report.md`, `step_b4.py` |
| Present in repo | `detq_check.py`, `exact_chambers.py`, `rulings.py`, `rulings_report.md`, `step_b4.py` |
| Cited in LEDGER/RESULTS | `detq_check.py`, `rulings.py`, `rulings_report.md`, `step_b4.py` |

## Prompt as sent

```text
Work in /Users/dmi/cube-compounds (mathematics research repo; python3 with sympy/numpy; run scripts in place).

Read /Users/dmi/cube-compounds/specs/STRUCTURED_RULINGS_SPEC.md and implement it exactly. Before writing code also read: rulings.py (you wrote it — reuse its enumeration, ruling-solve and normalize_dir), specs/RULINGS_SPEC.md §3 for the four line parameters, exact_chambers.py (call decompose, do not rewrite), rulings_report.md §1 (the corrected findings you are extending), and detq_check.py (the split-over-Q theorem — take it as given).

Hard requirements:
- Exact rational arithmetic; no float decides anything.
- The arc-A terminus s=19/6 regression must reproduce 725 across 11 chambers. If it does not, STOP and report — do not adjust the expectation.
- A window crossing 0 or 1 walls is VACUOUSLY constant. Count those separately, never in the constant tally. This is the exact error that inflated your first report.
- Catch the known exact_chambers IndexError per ruling, record as crashed, continue, and report the crash count.
- Add files only. Write results incrementally so an interrupted run still leaves data.
- Budget 40 minutes of compute. Report real coverage.
- Report negatives plainly. "Rulings are not a generator of maximiser arcs" is a valid and useful result.

When done, reply with: the regression result, the constancy-vs-multiplicity table with sample sizes, multiplicity at the arc termini, whether any ruling holds a record value along its length, the crash count, and anything in the spec that was wrong or impossible.

Note: four step_b4.py shards are running on this machine — do not kill them or launch heavy parallel work.
```
