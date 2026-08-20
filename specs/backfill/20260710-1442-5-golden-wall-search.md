# ℚ(√5) golden-wall search

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-07-10T14:42:33 |
| Agent type | general-purpose |
| Model override | sonnet |
| Session | `c4196554-d37e-44f9-8da5-5d7210e1f156` |
| Tool-use id | `toolu_013irkS4jM5x3EKj7VQ1Y2xm` |
| Files named | `certify_six.py`, `cube_compound_exact.py`, `exact_search.py`, `golden_six.py`, `golden_wall_report.md`, `mt_sim.py`, `six_cube_search_results.md` |
| Present in repo | `certify_six.py`, `cube_compound_exact.py`, `exact_search.py`, `golden_six.py`, `golden_wall_report.md`, `mt_sim.py` |
| Cited in LEDGER/RESULTS | `certify_six.py`, `cube_compound_exact.py`, `exact_search.py`, `golden_six.py`, `golden_wall_report.md` |

## Prompt as sent

```text
Working directory: /Users/dmi/carroll. Exact cube-compound region-counting project. Read first: six_cube_search_results.md Postscripts 4–5 (state: record 635 for six congruent concentric unit cubes under RATIONAL rotations; deep ceilings d3≤164/d4≤102/d5≤36), cube_compound_exact.py (Q5 = exact ℚ(√5) arithmetic; build_axes/find_cubes give the compound-of-five-cubes orientations as 5 orthonormal triples of exact unit Q5 vectors; run(5) counts 351), certify_six.py (exact_count_config already computes over CN-wrapped Q5 internally; takes objects R with R.m a 3×3 matrix of Q5 entries, columns = face normals).

Goal: extend the 6-cube maximum search to ℚ(√5) rotations by searching the neighborhood of the golden wall: configurations = the five golden cubes (fixed) + a sixth congruent cube, exactly counted. Does anything here beat 635?

Implementation (new file golden_six.py; do NOT modify the validated files cube_compound_exact.py, certify_six.py, exact_search.py, mt_sim.py):
- Build the five golden rotation matrices from build_axes()/find_cubes(): each triple of orthogonal unit axes = the columns; wrap in a minimal object with .m so exact_count_config accepts them (check exactly what element type .m[i][j] must be — plane_key reads x.a/x.b Q5 components off CN leaves; follow how certify_six wraps rot_from_quat outputs and mirror it).
- Sixth cube, two families, both parameterized by an integer quaternion (a,b,c,d), gcd-reduced, |component| ≤ 512, rational rotation Q via golden_rotations.rot_from_quat: family A: sixth = Q itself (rational columns, embedded in Q5); family B: sixth = Q·G1 (rational rotation applied to golden cube 1's matrix; columns land in Q5). These are genuinely different orbits; search both.
- Global rotation invariance means golden5+rational-6th already covers rationally-rotating the whole compound relative to the sixth; no need for more parameters.

HARD validation gates before any search:
- V1: the five golden cubes alone through exact_count_config give total 351, and sub-compounds of the first 1/2/3/4 cubes give 1/13/67/177 (matching cube_compound_exact.run).
- V2: six all-rational cubes through your same shim path reproduce a known seed exactly (pick seed 0 from exact_search_results.jsonl — READ-ONLY file — and match total + depth histogram via the standard rationalize path).
- V3: golden five + an exact duplicate of golden cube 1 (family B with identity quat) must give total 351 — this exercises the coincident-plane machinery (owners_of classes); if it asserts or miscounts, stop and debug, do not weaken the invariant.
If any gate fails, report honestly and stop.

Search protocol (log every evaluation with its family, quat, total, by_depth to golden_search.jsonl; measure per-eval time first and budget accordingly — expect several seconds to ~30 s per config in Python):
1. Symmetric candidates first, both families: identity (A: axis-aligned sixth; B: duplicate = gate), 90°/180° about coordinate axes, 60°/120° about (1,1,1) (rational rotations — Rodrigues gives rational matrices there), and a few quats near icosahedral symmetries of the compound (these may coincide with symmetries — coincidences are informative, log them).
2. Random integer quats (use mt_sim.py's chain or plain reproducible RNG — state your seeds), ~100–200 evals split across families.
3. Exact greedy hill-climb from the best few starts (moves: ±1/±2 on one quat component, re-gcd, |c| ≤ 512), as long as your time budget allows.
Report per config: total, by_depth, and specifically whether d1/d2 exceed 118/214 or d3/d4/d5 deviate from 164/102/36 — near-wall deep-count behavior is scientifically interesting even if totals are low.

Deliverables: golden_six.py, golden_search.jsonl, and a report written to golden_wall_report.md (do NOT edit six_cube_search_results.md — another agent appends there; the main session will merge). Report: gate results, timing, best total per family with quats, depth histograms of the top configs, and the answer to: does the golden wall region beat, match, or fall short of the rational record 635, and does it boost any single depth beyond its rational record? Honest negatives welcome. Style: exact arithmetic only in predicates, invariant comments (why, not what), concise, no flattery.
```
