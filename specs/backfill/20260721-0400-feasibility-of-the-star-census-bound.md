# Feasibility of the (star) census bound

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-07-21T04:00:16 |
| Agent type | default |
| Model override | sonnet |
| Session | `c4196554-d37e-44f9-8da5-5d7210e1f156` |
| Tool-use id | `toolu_01FAWL3LeZV1JWA85sFhE58G` |
| Files named | `census_bound.py`, `census_bound_report.md`, `census_extract.py`, `six_cube_search_results.md` |
| Present in repo | `census_bound.py`, `census_bound_report.md`, `census_extract.py` |
| Cited in LEDGER/RESULTS | `census_bound.py`, `census_bound_report.md`, `census_extract.py` |

## Prompt as sent

```text
Execute /Users/dmi/carroll/CENSUS_BOUND_SPEC.md in FEASIBILITY-FIRST mode — this is the last gap in max(3)=67, the inequality Σ_v(deg_v−2) ≤ 92 on the top diagram (equivalently d1 ≤ 48). Working directory /Users/dmi/carroll. Read the spec first, and READ PROOF_67.md §5 AND §5.1 (the reduction lead) — they are the analytic context.

Your PRIMARY deliverable this run is a feasibility verdict with concrete numbers, NOT a completed proof. Do NOT burn large compute on a full classification or 6-D certified covering before the estimates say it will terminate. Specifically produce:
- Approach 1 (Euler weight classification): count the realizable active-face triples (a,b,c) that can be simultaneously equi-projected + active + top, over a large random config scan — how far below the naive 3·3·3·2 does the activity/top restriction cut, and does it plausibly cap Σ(deg−2) at 92?
- Approach 2 (chamber enumeration): estimate the top-diagram combinatorial-chamber count on a pilot sub-domain; extrapolate whether full enumeration is tractable.
- Approach 4 (the anchor-reduction, PROOF_67 §5.1 — likely the shortest path): this is VERIFIED to give 24+24 at the octahedral maximizer. Over many random configs, classify each triple point as anchoring or non-anchoring via the cone condition e_i ∈ cone{e_x − e_i} for each incident cube, and test empirically whether "≤ 24 triple points anchor" holds with margin. Crucially: look for a clean GEOMETRIC criterion distinguishing the ~8 non-anchoring triple points from the ~24 anchoring ones — if one emerges, it may be the shortest route to (★). Report the anchoring-count distribution.

Gates: reuse census_extract.py's validated exact machinery for anything load-bearing (triple-point extraction, degrees, the cone/anchoring test); G1 reproduce Σ(deg−2)=92 at both maximizers and 32/32 bottoms; G2 your bound/enumeration returns exactly 92 (tight) at both maximizers; G3 ≤92 on ~10^4 random configs (a single >92 would REFUTE (★) — re-verify exactly and FLAG AT TOP). Empirical scans may use floats for speed; any claimed bound or equality-at-maximizer must be exact.

≤4 cores, detached for scans, don't idle on monitors (background tasks + end turn; you'll be re-invoked). Never edit six_cube_search_results.md or any validated/read-only file. Deliverables: census_bound_report.md (feasibility verdict FIRST, with the numbers above), census_bound.py, logs. Report honestly which approach is tractable and which is not — a well-estimated "route N needs a check of size M" is the success criterion for this run.
```
