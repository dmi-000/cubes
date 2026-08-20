# n>6 cube engine + campaigns

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-07-10T14:28:37 |
| Agent type | general-purpose |
| Model override | sonnet |
| Session | `c4196554-d37e-44f9-8da5-5d7210e1f156` |
| Tool-use id | `toolu_01HQnFyLrRbAya1j656sKV3E` |
| Files named | `certify_six.py`, `cube_regions.cpp`, `exact_search.py`, `mt_sim.py`, `phase_b_hillclimb.py`, `phase_b_hillclimb_n.py`, `run_campaign.py`, `run_campaign_n.py`, `six_cube_search_results.md` |
| Present in repo | `certify_six.py`, `cube_regions.cpp`, `exact_search.py`, `mt_sim.py`, `phase_b_hillclimb.py`, `phase_b_hillclimb_n.py`, `run_campaign.py`, `run_campaign_n.py` |
| Cited in LEDGER/RESULTS | `certify_six.py`, `cube_regions.cpp`, `exact_search.py`, `phase_b_hillclimb.py`, `run_campaign.py` |

## Prompt as sent

```text
Working directory: /Users/dmi/carroll. This is the exact cube-compound region-counting project.

Your task: implement NPLUS_SPEC.md — generalize the exact search to n > 6 intersecting cubes. Read these first, in order: NPLUS_SPEC.md (your spec), CPP_SPEC.md (the engine design you're extending), and Postscripts 3–5 of six_cube_search_results.md (project state and methodology).

Hard operational constraints:
1. A campaign is CURRENTLY RUNNING using the binary ./cube_regions (seeds 260000–360000, ~1 hour). Do NOT overwrite that binary. Edit cube_regions.cpp freely, but compile to a NEW binary name: `clang++ -O2 -std=c++17 -o cube_regions_n cube_regions.cpp`. Use ./cube_regions_n for everything you run.
2. Before launching your own multi-worker campaign, check `pgrep -f run_campaign`. If the n=6 campaign is still running, cap yourself at 4 workers; once it's gone you may use 8.
3. exact_search_results.jsonl is the user's ground truth: READ-ONLY.
4. Do not modify the validated Python files (certify_six.py, exact_search.py, mt_sim.py, run_campaign.py, phase_b_hillclimb.py). For the campaign driver, make a generalized copy run_campaign_n.py with an --n passthrough per the spec (campaign_n7.jsonl etc.; leave campaign_results.jsonl alone).
5. Validation gates are HARD and come before any campaign, exactly as the spec says: G1regression (--n 6 must reproduce seeds 0..199 from exact_search_results.jsonl with zero mismatches on totals AND depth histograms), G2cross (n in {2,3,4,5,7,8}, 3 seeds each vs the Python oracle `python3 -c "from certify_six import ...; from mt_sim import sim_quats..."` — k=7 seeds 777/778/779 must give 973, 993, 873), G3 (axial selftest + timing per n). If any gate fails, STOP campaigning and debug; report honestly.
6. The Python oracle is slow at n=7 (~11 s/config) — that's fine for 3-seed cross-checks; never use it for bulk.

Science program after gates pass (see spec section 4): campaign_n7.jsonl ~50k seeds, campaign_n8.jsonl ~10k seeds; hill-climb n=7 from its top-20 (adapt phase_b_hillclimb.py into a copy phase_b_hillclimb_n.py, moves ±1/±2 one component, re-gcd, |c|<=512); analyze per n: record totals, which deep depth-sums freeze at the top (at n=6, every config >=625 has (d3,d4,d5,d6)=(164,102,36,1) exactly), depth histograms of records, mod-4 law (bounded ≡ 2n−1 mod 4) exception rate, top-spectrum gaps (633 never occurs at n=6). If time allows, measure the T1 census analog: at n=6 the generic swap-curve counts are (V,E) = (68,102)/(200,300)/(324,486) for Sigma_1/2/3 — the n-dependence of these numbers is the empirical input the general proof needs; you can get the depth-side numbers (which bottom-l cell counts are generic per n) from the campaign per_label data alone, no spherical code needed.

Deliverables: cube_regions.cpp with --n (binary cube_regions_n), run_campaign_n.py, phase_b_hillclimb_n.py, campaign_n7.jsonl, campaign_n8.jsonl, and Postscript 6 appended to six_cube_search_results.md with the cross-n table (per n: record total + quats, frozen deep sums, generic bottom-diagram values, mod-4 exceptions). Honest negatives welcome. Style: exact arithmetic only in predicates, invariant comments in source (why, not what), no flattery, concise.

Final message: per-gate pass/fail, then the cross-n record table and the one or two most surprising structural findings, with key numbers inline.
```
