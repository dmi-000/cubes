# Symmetry re-run, full-quat grids

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-07-11T12:23:57 |
| Agent type | general-purpose |
| Model override | sonnet |
| Session | `c4196554-d37e-44f9-8da5-5d7210e1f156` |
| Tool-use id | `toolu_01RAh4dx2h4VX7AbtuWpy84T` |
| Files named | `six_cube_search_results.md`, `symmetry_search.py`, `symmetry_search_report.md`, `symmetry_search_report2.md` |
| Present in repo | `symmetry_search.py`, `symmetry_search_report.md`, `symmetry_search_report2.md` |
| Cited in LEDGER/RESULTS | `symmetry_search.py`, `symmetry_search_report.md`, `symmetry_search_report2.md` |

## Prompt as sent

```text
Working directory: /Users/dmi/carroll. Exact cube-compound region-counting project. Your complete brief is SYMMETRY_SEARCH_V2.md — read it and the files it lists (symmetry_search.py, symmetry_search_report.md, six_cube_search_results.md Postscript 10, README.md).

This is a targeted re-run fixing a search-coverage gap in the first symmetry sweep. The first run's FRAMEWORK is validated (gates GA–GE pass, reproducing 67/681/699), but its per-family seed grids were too thin — the C₃:3+3 family, which provably contains the 699 record, was searched only to 399 because it used thin axis-angle seeds instead of general quaternions. REUSE symmetry_search.py's validated construction/orbit/O-dedup/dispatch/count functions unchanged; only replace the seed sampler and climber so seeds are FULL integer quaternions (w,x,y,z), gcd-reduced, |component|≤512.

Execute in the spec's priority order: (1) C₃:3+3 FIRST — gate it by starting one climb from the known 699 seeds and CONFIRM the family search now reaches ≥699 (if it still caps below 699, the seed mapping is wrong — stop and debug, don't paper over it); then random-restart + deep hill-climb to hunt >699. (2) The core+free families whose first-run bests are floors (T:4+free2=661, D₃:3+3=657, C₂:2+2+2=653, D₂:4+free2=651, C₆:6=649) with full-quat seeds for both core and free cubes, ~20 restarts each. (3) Confirm golden I/C₅:5+free=681 with a deeper radius-3/4 climb (ℚ(√5), budget limited).

Use the fast C++ engine for rational families, ≤4 cores. Log every eval to symmetry_search2.jsonl (do NOT clobber the first run). Flag any total>699 immediately, and any deep-count violation (d3>164/d4>102/d5>36/d6≠1 — that's a construction bug, not a find). State per family the seed-grid size, climb radius, and #restarts so coverage is auditable. Write symmetry_search2.jsonl and symmetry_search_report2.md; do NOT edit six_cube_search_results.md or validated files; exact_search_results.jsonl read-only; exact arithmetic only in predicates; no flattery; honest negatives welcome. Final message: does C₃:3+3 now reach ≥699 (the key correctness check), did anything beat 699, and the refreshed per-family bests with the stated coverage.
```
