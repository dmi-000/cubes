# Deep-sacrifice / shallow-max search

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-07-12T14:50:08 |
| Agent type | general-purpose |
| Model override | sonnet |
| Session | `c4196554-d37e-44f9-8da5-5d7210e1f156` |
| Tool-use id | `toolu_01DHRQvSGEvEsy1DwJPvCJqw` |
| Files named | `deepsweep.py`, `deepsweep_report.md`, `groebner_solutions.json`, `phase_b_hillclimb.py`, `six_cube_search_results.md`, `symmetry_search2.py` |
| Present in repo | `deepsweep.py`, `groebner_solutions.json`, `phase_b_hillclimb.py`, `symmetry_search2.py` |
| Cited in LEDGER/RESULTS | `deepsweep.py`, `phase_b_hillclimb.py`, `symmetry_search2.py` |

## Prompt as sent

```text
Working directory: /Users/dmi/carroll. Exact cube-compound region-counting project. Read first: PROJECT.md (self-contained overview), six_cube_search_results.md Postscript 14 (the trade-off structure — READ THIS, it defines the objective), README.md. Use the fast exact counter ./cube_regions (rational, concentric; ./cube_regions --quats 'w,x,y,z;...' prints JSON with bounded + by_depth). Current record total 723, by_depth {1:210,2:216,3:164,4:96,5:36,6:1}.

REFRAMED OBJECTIVE (from Postscript 14): the deep layers d3/d4/d5 are CAPPED at 164/102/36 (quantized — a config either hits the cap or a lower merged value); the shallow layers d1/d2 are UNCAPPED and grow with complexity. The maximum total = saturate the deep caps AND maximize d1+d2, spending deep "sacrifices" only where they buy disproportionate shallow gain. 723 already sacrifices d4 (102→96) to gain ~45 in d1. YOUR TASK: map this deep-sacrifice trade-off surface and hunt configs beating 723.

Concretely, build deepsweep.py:
1. A hill-climber (reuse the move set from phase_b_hillclimb.py / symmetry_search2.py: ±1/±2 on one integer quaternion component, re-gcd, |c|≤512, exact eval via cube_regions) with a SELECTABLE objective: (a) d1+d2, (b) total, (c) d1 alone. Log every eval's full profile + total to deepsweep.jsonl.
2. Start climbs from: the 723 and 717 records; the Gröbner high-d1 configs in groebner_solutions.json (base5 + each Aquat → total 689, d1=224); and ~20 random restarts.
3. DEEP-SACRIFICE exploration: from 723, deliberately explore moves that LOWER d3 and/or d4 further (below their caps) while raising d1+d2 — does any (d3,d4,d5) profile with a sacrificed deep layer reach a total > 723? Test the strata (164,102,36), (164,96,36), (158,102,36), (158,96,36), (150,102,36), etc.
4. Trade-off surface: for each observed deep profile (d3,d4,d5), report the MAX d1+d2 (and max total) achieved at that stratum — this is the deliverable map.

HARD RULES: exact only (cube_regions); do NOT modify validated files or six_cube_search_results.md; exact_search_results.jsonl read-only; ≤4 cores; flag any total>723 immediately; run detached and write the report at the end rather than parking on monitors. Deliverables: deepsweep.py, deepsweep.jsonl, deepsweep_report.md. Final message: max total found vs 723, whether any deep-sacrifice profile beats 723, the best d1+d2 achieved, and the (deep-profile → max d1+d2) surface table.
```
