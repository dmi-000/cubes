# Extended n=4 maximum search

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-07-12T22:56:31 |
| Agent type | general-purpose |
| Model override | sonnet |
| Session | `c4196554-d37e-44f9-8da5-5d7210e1f156` |
| Tool-use id | `toolu_011eoLUKvt6U7nSetXzsLKXR` |
| Files named | `certify_six.py`, `cube_compound_exact.py`, `cube_regions.cpp`, `exact_search.py`, `golden_six.py`, `n4_search.py`, `n4_search_report.md`, `phase_b_hillclimb_n.py`, `run_campaign_n.py`, `six_cube_search_results.md` |
| Present in repo | `certify_six.py`, `cube_compound_exact.py`, `cube_regions.cpp`, `exact_search.py`, `golden_six.py`, `n4_search.py`, `n4_search_report.md`, `phase_b_hillclimb_n.py`, `run_campaign_n.py` |
| Cited in LEDGER/RESULTS | `certify_six.py`, `cube_compound_exact.py`, `cube_regions.cpp`, `exact_search.py`, `golden_six.py`, `n4_search.py`, `n4_search_report.md` |

## Prompt as sent

```text
Working directory: /Users/dmi/carroll. Exact cube-compound region-counting project. Read first: PROJECT.md (self-contained overview), six_cube_search_results.md Postscripts 4-8 (the n=6 methodology this mirrors), README.md. Tools: ./cube_regions_n --n 4 (fast exact rational counter for 4 cubes; ./cube_regions_n --n 4 --seed S or --quats 'w,x,y,z;w,x,y,z;w,x,y,z;w,x,y,z' → JSON with bounded + by_depth), cube_compound_exact.py (golden ℚ(√5) engine; run(4) gives the golden four-cube compound = 177), certify_six.py exact_count_config (Python oracle, any n), phase_b_hillclimb_n.py, run_campaign_n.py.

BACKGROUND: The best known 4-cube configuration is the golden four-cube sub-compound (4 of the 5 cubes inscribed in a dodecahedron) = 177 exactly, by_depth {1:104,2:48,3:24,4:1} (ℚ(√5)). A prior rational-only search topped out at "135+", far below 177, because rational rotations can't reach the golden wall — the growth table was corrected to n=4 ≥ 177. OPEN QUESTION: is 177 the true 4-cube maximum, or can it be beaten? (At n=6, the best rational config 723 beat the golden-based 681, so 177 is not obviously the ceiling.)

YOUR TASK: establish the n=4 record and hunt above 177.
1. Confirm the golden four-cube = 177 via cube_compound_exact.run(4) and re-verify by feeding those four rotations through certify_six.exact_count_config. Record its exact quats/matrices.
2. Rational campaign + hill-climb with ./cube_regions_n --n 4: a broad seed campaign (say 50k-200k seeds via run_campaign_n.py --n 4, or a direct loop) to map the generic n=4 distribution and its max; then exact hill-climb (phase_b_hillclimb_n.py adapted to n=4, or your own: ±1/±2 on one quaternion component, re-gcd, |c|≤512) from the best seeds and from any structured starts. Does any rational 4-cube config reach or beat 177?
3. Structured/symmetry attempts: the golden four-cube (177) and its ℚ(√5) neighborhood (perturb the free cube(s) like the golden_six.py approach did for n=6 — a golden 3-subset + a fourth cube, hill-climbed); small symmetry families for 4 cubes (e.g. shared-axis pairs, an octahedral-type quad). Count exactly (rational via cube_regions_n; ℚ(√5)/√2 via the field engines).
4. mod-4 check: n=4 generic totals should be ≡ 2·4−1 = 7 ≡ 3 (mod 4); note any wall exceptions.

HARD RULES: exact arithmetic only in predicates; validate the counter first (a couple of cross-checks between cube_regions_n --n 4 and certify_six oracle must agree); do NOT modify validated files (certify_six.py, cube_compound_exact.py, exact_search.py, cube_regions.cpp) or six_cube_search_results.md; exact_search_results.jsonl read-only; ≤4 cores; run searches detached and write the report at the end rather than parking on monitors; flag anything > 177 immediately. Deliverables: n4_search.py, n4_search.jsonl, n4_search_report.md. Final message: confirmed golden n=4 = 177 (yes/no), the best rational n=4 total found, whether anything beat 177 (with quats/by_depth if so), and your best estimate of the n=4 maximum with honest coverage.
```
