# Extended n=5 search — test 351

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-07-13T03:12:59 |
| Agent type | general-purpose |
| Model override | sonnet |
| Session | `c4196554-d37e-44f9-8da5-5d7210e1f156` |
| Tool-use id | `toolu_01EgytgwcG7e4BYQd1HpnvNn` |
| Files named | `certify_six.py`, `cube_compound_exact.py`, `golden_six.py`, `n4_search.py`, `n4_search_report.md`, `n5_search.py`, `n5_search_report.md`, `phase_b_hillclimb_n.py`, `run_campaign_n.py`, `six_cube_search_results.md` |
| Present in repo | `certify_six.py`, `cube_compound_exact.py`, `golden_six.py`, `n4_search.py`, `n4_search_report.md`, `n5_search.py`, `n5_search_report.md`, `phase_b_hillclimb_n.py`, `run_campaign_n.py` |
| Cited in LEDGER/RESULTS | `certify_six.py`, `cube_compound_exact.py`, `golden_six.py`, `n4_search.py`, `n4_search_report.md`, `n5_search.py` |

## Prompt as sent

```text
Working directory: /Users/dmi/carroll. Exact cube-compound region-counting project. Read first: n4_search_report.md and n4_search.py (the n=4 search that just beat the golden 177 with a rational 183 — mirror its methodology), six_cube_search_results.md Postscript 15, PROJECT.md. Tools: ./cube_regions_n --n 5 (fast exact rational counter; --seed S or --quats 'q;q;q;q;q' → JSON bounded + by_depth), cube_compound_exact.py (golden ℚ(√5); run(5)=351), certify_six.py exact_count_config (oracle, any n), phase_b_hillclimb_n.py, run_campaign_n.py, golden_six.py (golden+extra-cube machinery).

MOTIVATING QUESTION (from Chris Cole): the golden four-cube compound (177) turned out NOT to be the n=4 maximum — a rational config reaches 183. Does the same hold for FIVE cubes? Is the golden five-cube compound (351, the complete icosahedral compound) the true n=5 maximum, or can it be beaten?

Note n=5 may differ from n=4: the golden FIVE-compound is the COMPLETE, maximally-symmetric icosahedral compound (not a sub-compound), so it may be genuinely optimal where the 4-sub-compound was not. Test it, don't assume.

TASK (mirror n4_search.py):
1. Confirm golden n=5 = 351 via cube_compound_exact.run(5) AND certify_six oracle; record its exact form. by_depth {1:180,2:80,3:60,4:30,5:1}.
2. Rational campaign + hill-climb with ./cube_regions_n --n 5: broad seed campaign (map generic n=5 max) then exact hill-climb from top seeds.
3. THE KEY TECHNIQUE that broke n=4: wide-perturbation multi-restart deep-climb (greedy ±1/±2 to a local max, then WIDE multi-component perturbation + re-climb to escape into richer basins; n=4 went 159→...→183 this way while plain greedy stalled below 177). Apply it from structured seeds: the golden 5 itself and its ℚ(√5) neighborhood (perturb via golden_six-style machinery), octahedral-type, shared-axis, and C-orbit families for 5 cubes.
4. mod-4: n=5 generic ≡ 2·5−1 = 9 ≡ 1 (mod 4); note wall exceptions.
5. Check the deep-layer structure: n=4 had d3 ≤ 24 = 6·4 held across ~300k configs. For n=5, the analog is depth-(n−1)=d4 ≤ 6·5 = 30 (golden hits 30). Confirm d4 ≤ 30 holds and report the deep profile of the best configs.

HARD RULES: validate cube_regions_n --n 5 vs the oracle on a few seeds first; exact arithmetic only; do NOT modify validated files or six_cube_search_results.md; exact_search_results.jsonl read-only; ≤4 cores; run detached, write the report at the end (don't park on monitors); flag anything > 351 immediately. Deliverables: n5_search.py, n5_search.jsonl, n5_search_report.md. Final message: golden n=5 = 351 confirmed (yes/no); best rational and best overall n=5 total found; did anything beat 351 (quats/by_depth if so); whether d4 ≤ 30 held; and your best estimate of the n=5 maximum with honest coverage.
```
