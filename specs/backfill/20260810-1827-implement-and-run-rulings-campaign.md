# Implement and run rulings campaign

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-08-10T18:27:11 |
| Agent type | general-purpose |
| Model override | sonnet |
| Session | `833a739b-86d7-4754-94e1-446688dfcac3` |
| Tool-use id | `toolu_01AYaqwtUr1XMu28bYpMUN1p` |
| Files named | `base_points.py`, `exact_chambers.py`, `incidence2.py`, `rulings.py`, `rulings_data.json`, `rulings_report.md`, `solve_ends.py`, `wall_params.py`, `wall_stratum.py` |
| Present in repo | `base_points.py`, `exact_chambers.py`, `incidence2.py`, `rulings.py`, `rulings_data.json`, `rulings_report.md`, `solve_ends.py`, `wall_params.py`, `wall_stratum.py` |
| Cited in LEDGER/RESULTS | `base_points.py`, `incidence2.py`, `rulings.py`, `rulings_data.json`, `rulings_report.md`, `wall_params.py` |

## Prompt as sent

```text
Work in /Users/dmi/cube-compounds (a mathematics research repo; run scripts in place, python3 with sympy 1.14 and numpy available).

Read /Users/dmi/cube-compounds/RULINGS_SPEC.md and implement it exactly. It is a complete specification: formulas, enumeration, gates, budget, and the report contents. Also read these existing files before writing code, and REUSE them rather than reimplementing: wall_params.py (the M/N entry layout and the W3 edge enumeration), exact_chambers.py (decompose — call it, do not rewrite it), solve_ends.py (catalogue, q_of, BASE), wall_stratum.py (how an active W4 condition at a parameter value is identified), base_points.py, incidence2.py. Skim METHODS.md §1 and §5 and FAILURE_MODES.md before starting.

Hard requirements:
- Exact rational arithmetic everywhere; no float decides anything.
- Run the gates in RULINGS_SPEC.md §5 FIRST and print PASS/FAIL for each. G1 is a regression against a result obtained yesterday and its expected numbers are given exactly — if it fails, stop and report the discrepancy rather than adjusting the expectation to match your output. Do not weaken or skip a gate to make progress.
- Add new files only (rulings.py, rulings_data.json, rulings_report.md, rulings.log). Do not edit any existing file.
- Respect the 40-minute compute budget in §6, write results incrementally, and report actual coverage.
- Negative or boring results are fine and must be reported as they are. If a count above a record appears, verify it with both engines before claiming it.

When done, reply with: gate results, how many (wall, point) pairs you enumerated and how many rulings you actually solved, the answers to the four report questions in §7 with numbers, and anything in the spec that turned out to be wrong or impossible.
```
