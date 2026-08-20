# Blueprint branch-and-prune search

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-07-13T08:35:23 |
| Agent type | general-purpose |
| Model override | sonnet |
| Session | `c4196554-d37e-44f9-8da5-5d7210e1f156` |
| Tool-use id | `toolu_01QF4CzTVzgoQbT5MV4fNXcy` |
| Files named | `blueprint_enum.py`, `blueprint_search.py`, `blueprint_search_report.md`, `shared_axis_search.py`, `six_cube_search_results.md` |
| Present in repo | `blueprint_enum.py`, `blueprint_search.py`, `blueprint_search_report.md`, `shared_axis_search.py` |
| Cited in LEDGER/RESULTS | `blueprint_enum.py`, `blueprint_search.py`, `blueprint_search_report.md`, `shared_axis_search.py` |

## Prompt as sent

```text
Working directory: /Users/dmi/carroll. Exact cube-compound region-counting project. Your complete brief is BLUEPRINT_SPEC.md — read it and the files it lists (six_cube_search_results.md Postscripts 17–19 with addenda, shared_axis_search.py whose cluster/spoke machinery you must REUSE, PROJECT.md). Execute in order: (1) enumerate the n=6 blueprint catalog up to symmetry with pruning rules P1 (realizability), P2 (frustration: all-13 triangles force the golden wall, provably dominated), P3 (dominance), printing the catalog with per-blueprint prune reasons; (2) GATE: the 723 blueprint (3 spokes + 3 on-axis about (1,1,1)) must survive and its knob optimization must reproduce 723; (3) run the survivors' knob searches (spoke-angle grids + free-cube hill-climbs) detached and self-contained — do NOT park waiting on monitors, that has stalled several prior agents; (4) write blueprint_search_report.md with the catalog, per-blueprint bests vs 723, and the verdict. Flag any total > 723 immediately and verify it with certify_six.exact_count_config before claiming. Rules: exact arithmetic only via ./cube_regions; ≤4 cores; do NOT modify validated files or six_cube_search_results.md; exact_search_results.jsonl read-only. Deliverables: blueprint_enum.py, blueprint_search.py, blueprint_search.jsonl, blueprint_search_report.md. Final message: catalog size and prune breakdown, gate result, best per surviving blueprint, whether anything beat 723, and the coverage statement.
```
