# n=7 record program

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-07-13T12:48:17 |
| Agent type | general-purpose |
| Model override | sonnet |
| Session | `c4196554-d37e-44f9-8da5-5d7210e1f156` |
| Tool-use id | `toolu_013FqGHnjmKX7zmuJH22t3Js` |
| Files named | `blueprint_enum.py`, `blueprint_search.py`, `n4_search.py`, `n7_program.py`, `n7_program_report.md`, `shared_axis_search.py`, `six_cube_search_results.md` |
| Present in repo | `blueprint_enum.py`, `blueprint_search.py`, `n4_search.py`, `n7_program.py`, `n7_program_report.md`, `shared_axis_search.py` |
| Cited in LEDGER/RESULTS | `blueprint_enum.py`, `blueprint_search.py`, `n4_search.py`, `n7_program.py`, `n7_program_report.md`, `shared_axis_search.py` |

## Prompt as sent

```text
Working directory: /Users/dmi/carroll. Exact cube-compound region-counting project. Read first: six_cube_search_results.md Postscripts 16–21 (the record tower, ceiling law, envelope bounds, blueprint program — this brief applies that whole apparatus at n=7), PROJECT.md, shared_axis_search.py and blueprint_enum.py/blueprint_search.py (REUSE their machinery), n4_search.py (the wide-perturbation deep-climb that broke records). Counter: ./cube_regions_n --n 7 (exact, ~0.3-1s/config at n=7); oracle certify_six.exact_count_config for verification of any record claim.

STATE: n=7 record = 1207, found by greedy extension (723's six cubes + seventh [5,4,-4,-4]), NEVER hill-climbed. Campaign best from 50k random seeds = 1085. The ceiling law predicts C(l,7) = (12l−6)·7 − 2(l²−1) = 42, 120, 194, 264, 330, 392 for l=1..6, and the summed max-total bound 1343. The l≤4 caps (42/120/194/264) are already attained in logged n=7 data.

TASKS in order:
1. CLIMB 1207: wide-perturbation multi-restart deep-climb (greedy ±1/±2 to local max, then 5–12-move multi-component perturbation + re-climb, ~30+ restarts; the technique of n4_search.py). Also try swapping/re-optimizing the 7th cube. Flag any new record immediately, verify with the oracle before claiming.
2. BLUEPRINT SEARCH at n=7: enumerate cluster skeletons for 7 cubes (partitions of 7 into spoke-clusters/on-axis/free, axes (1,1,1)/(0,0,1)/(1,1,0), reusing blueprint_enum.py logic), prune P1/P2/P3 as at n=6, gate on the 1207-or-better config being expressible, knob-optimize survivors. Budget: this is the big compute item; prioritize blueprints resembling the n=6 winners (onaxis+spoke about (1,1,1)).
3. CEILING VERIFICATION: confirm no config anywhere violates C(l,7) for any l (a violation kills the general law — flag loudly); report which caps are attained (l=5: 330 and l=6: 392 are so far UNATTAINED — observed 306 and 158 — hunting configs that raise these tests the law's shallow end).
4. EXTENSION to n=8: take your best n=7 config, add an 8th cube (a few hundred candidate orientations + short climb) → first n=8 record. Ceiling predictions at n=8: C(l,8) = 48, 138, 228, 318, 408, 498, 588; deep caps 48/138/228 should be attained generically. Verify no violation.
5. ENVELOPE at n=7 (cheap version): for your top ~50 n=7 configs, count all seven 6-subsets; report max(T − S_max) — the E1 analog for the n=6→7 step (known point: 1207 − 723 = 484) — and whether every top config's 6-subsets saturate the n=6 deep caps (164/102/36).

RULES: exact arithmetic only; ≤4 cores; run detached and self-contained (do NOT park on monitors — write the report at the end); do NOT modify validated files or six_cube_search_results.md; exact_search_results.jsonl read-only. Deliverables: n7_program.py (or reuse+driver), n7_program.jsonl, n7_program_report.md. Final message: new n=7 record (if any) with quats + by_depth + oracle verification; blueprint catalog size and best per skeleton; ceiling status at n=7 incl. whether l=5/l=6 caps were approached; the first n=8 record; and the n=7 envelope constant.
```
