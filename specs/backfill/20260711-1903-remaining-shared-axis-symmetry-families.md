# Remaining + shared-axis symmetry families

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-07-11T19:03:14 |
| Agent type | general-purpose |
| Model override | sonnet |
| Session | `c4196554-d37e-44f9-8da5-5d7210e1f156` |
| Tool-use id | `toolu_013HF3RCqSNgxjMUbpbgiPwR` |
| Files named | `six_cube_search_results.md`, `symmetry_search2.py`, `symmetry_search3_report.md` |
| Present in repo | `symmetry_search2.py`, `symmetry_search3_report.md` |
| Cited in LEDGER/RESULTS | `symmetry_search2.py`, `symmetry_search3_report.md` |

## Prompt as sent

```text
Working directory: /Users/dmi/carroll. Exact cube-compound region-counting project. Your complete brief is SYMMETRY_SEARCH_V3.md — read it and the files it lists (symmetry_search2.py, six_cube_search_results.md Postscripts 10–11 and the "11 addendum", README.md). REUSE symmetry_search2.py's validated build_blocks/orbit/O-dedup/dispatch/climber functions — do not rewrite them.

Record to beat: 717 (D₂:4+free2). Two parts. Part A: full-quaternion sweep + deep climb of the rational families V2 never re-swept properly — C₄, D₄, D₆ (orbit-of-6 partitions incl. "core+free"), plus re-confirm D₃/T with full-quat free cubes. Part B (the main event): shared-axis "intersection" families — build the 6 cubes as a UNION of two orbits under DIFFERENT cyclic/dihedral groups about a COMMON axis (try (1,1,1), (0,0,1), (1,1,0)); partitions C₂⊕C₄, C₃⊕C₃, C₂⊕C₂⊕C₂, C₄⊕C₂, C₃⊕C₂+free, and the D₂-cluster+free+aligned template; full-quat seeds for free blocks, ~50 starts each + deep climb; vary which cubes are on-axis vs free vs aligned. Also test the true "intersection" reading: where a shared-axis pair generates a polyhedral group (e.g. C₂+C₃ → T), check whether forcing the full T/O/I orbit beats the looser union.

Gate FIRST: reproduce 717 via the D₂-cluster+free+aligned shared-axis constructor and 699 via C₃⊕C₃-on-(1,1,1); if either fails the builder is wrong — stop and debug. Robustness: SKIP degenerate configs (build returns None) instead of asserting — that exact bug crashed the earlier deepclimb run twice. Fast C++ engine, ≤4 cores, log every eval to symmetry_search3.jsonl, flag any total>717 immediately and any deep-ceiling violation (d3>164/d4>102/d5>36/d6≠1 = construction bug, stop). Do NOT edit six_cube_search_results.md, symmetry_search2.py, or validated files; exact_search_results.jsonl read-only; exact predicates only; no flattery; honest negatives welcome.

IMPORTANT operational note: run your searches as self-contained scripts launched detached (nohup) that run ALL families and write symmetry_search3_report.md at the end — do NOT park waiting on probe/smoketest monitors (that repeatedly stalled prior agents). Write symmetry_search3.jsonl and symmetry_search3_report.md. Final message: did anything beat 717, the best shared-axis "intersection" family with its structure, and the Part-A per-family bests with coverage.
```
