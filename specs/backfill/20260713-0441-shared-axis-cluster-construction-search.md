# Shared-axis-cluster construction search

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-07-13T04:41:21 |
| Agent type | general-purpose |
| Model override | sonnet |
| Session | `c4196554-d37e-44f9-8da5-5d7210e1f156` |
| Tool-use id | `toolu_01QEHk5wRSx3hyy6RNLJQSHZ` |
| Files named | `shared_axis_search.py`, `shared_axis_search_report.md`, `six_cube_search_results.md`, `slide3_q2.py`, `symmetry_search.py`, `symmetry_search3.py` |
| Present in repo | `shared_axis_search.py`, `shared_axis_search_report.md`, `slide3_q2.py`, `symmetry_search.py`, `symmetry_search3.py` |
| Cited in LEDGER/RESULTS | `shared_axis_search.py`, `slide3_q2.py`, `symmetry_search.py`, `symmetry_search3.py` |

## Prompt as sent

```text
Working directory: /Users/dmi/carroll. Exact cube-compound region-counting project. Read first: PROJECT.md (self-contained overview), six_cube_search_results.md Postscripts 12, 16, 17 and the "17 addendum" (the DOF hierarchy + hub-and-spoke structure — READ these, they define the idea), symmetry_search.py / symmetry_search3.py (existing shared-axis/orbit machinery to reuse), slide3_q2.py. Tools: ./cube_regions_n --n K (fast exact rational counter; --quats 'q;q;...' → JSON bounded+by_depth). Records to reproduce/beat: n=4 183, n=5 393, n=6 723 (quats in the postscripts).

HYPOTHESIS TO TEST: the region maxima are "hub-and-spoke / shared-axis-cluster" configurations — a hub cube optimally paired to a cluster of SPOKE cubes that share a common axis (making mutual 9-pairs), where the SPOKE ANGLES about that axis are a CONTINUOUS, tunable degree of freedom. The known maxima are C₃-symmetric instances (spokes locked at 120°); the idea is that FREEING the spoke angles — searching that flexible 9-DOF directly — is the natural constructive family, and may reach or beat the records.

BUILD shared_axis_search.py:
1. Parameterize the family for n cubes: a common axis a (try (1,1,1), (0,0,1), (1,1,0)); a cluster of m SPOKE cubes each = Rot_a(φ_i)·B for a base orientation B and independent rational angles φ_i (tan half-angle = p/q); plus a HUB cube and/or free cubes (free integer quats). n = 1 + m + (free). For n=4 use hub+3 spokes (the 183 structure); n=5 hub+3 spokes+1 free and hub+4 spokes; n=6 hub+3 spokes+2 free and hub+4 spokes+1 free and 3 spokes+3 spokes (two clusters, the 723 structure). Everything rational so cube_regions_n applies.
2. GATE: confirm the family CONTAINS the records — that 183 and 723 are instances (build them from the parameterization, or verify their spoke-cubes share an axis and recover the C₃ special angles). If you can't express them in the family, say so and adjust the parameterization.
3. SEARCH the continuous DOF directly: sweep/grid the spoke angles φ_i (this is the flexible 9-DOF — the whole point) and the axis, plus hill-climb the hub/free integer quats. Because the spoke angles are the "right variables," a coordinate search over them should be far more effective than generic integer hill-climbing that falls off the shared-axis structure. Report whether freeing the angles (vs the C₃-locked 120°) reaches or beats 183/393/723.
4. Also test: does making the spokes' pairwise relation exactly 9 (shared axis) matter, vs generic? Compare cluster configs (9-paired spokes) against matched non-clustered controls at equal cube count.

HARD RULES: exact only (cube_regions_n); validate against the oracle on a couple configs first; do NOT modify validated files or six_cube_search_results.md; exact_search_results.jsonl read-only; ≤4 cores; run detached, write the report at the end (don't park on monitors); flag anything beating a record immediately. Deliverables: shared_axis_search.py, shared_axis_search.jsonl, shared_axis_search_report.md. Final message: does the family contain the records (gate), does searching the flexible spoke-angle DOF reach/beat 183/393/723, the best config found per n, and a verdict on whether "build from flexible 9-DOF clusters" is a productive construction principle.
```
