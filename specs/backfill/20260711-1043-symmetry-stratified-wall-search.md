# Symmetry-stratified wall search

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-07-11T10:43:56 |
| Agent type | general-purpose |
| Model override | sonnet |
| Session | `c4196554-d37e-44f9-8da5-5d7210e1f156` |
| Tool-use id | `toolu_013MrhLUawfEHnmYXLXC8von` |
| Files named | `cube_regions.cpp`, `golden_six.py`, `qtower.py`, `six_cube_search_results.md`, `slide3_q2.py`, `symmetry_search.py`, `symmetry_search_report.md` |
| Present in repo | `cube_regions.cpp`, `golden_six.py`, `qtower.py`, `slide3_q2.py`, `symmetry_search.py`, `symmetry_search_report.md` |
| Cited in LEDGER/RESULTS | `cube_regions.cpp`, `golden_six.py`, `qtower.py`, `slide3_q2.py`, `symmetry_search.py`, `symmetry_search_report.md` |

## Prompt as sent

```text
Working directory: /Users/dmi/carroll. Exact cube-compound region-counting project. Your complete brief is SYMMETRY_SEARCH_SPEC.md — read it and the files it lists (README.md, six_cube_search_results.md Postscripts 4-9, QFIELD_SPEC.md, golden_six.py, slide3_q2.py, qtower.py, cube_regions.cpp). 

Build a systematic symmetry-stratified search of the region-rich walls: enumerate the finite catalog of symmetry-constrained 6-cube subspaces (finite subgroup G of SO(3) × orbit-partition of 6 × seed orientations), and exact-count each family in its proper field, dispatching to the fast C++ engine for rational G and the Python field engines (ℚ(√5), ℚ(√2), ℚ(√3), towers) otherwise. The goal is to cover the symmetry walls where records live (655/681/699 were all such walls, found ad hoc) and hunt a config beating 699.

Execute in the spec's order: gates Gᴀ–Gᴇ FIRST (orbit machinery; reproduce 67, 699, 681, and a rational cross-check) — if any fails, stop and debug, do not report family results. Then Phase 1 (all rational G — the fast C++ sweep, where a rational >699 would surface cheaply), then Phase 2 (ℚ(√5): I and C₅ families), then Phase 3 (other fields only for families Phase 1/2 flag promising). Key correctness points from the spec: a cube is a coset in SO(3)/O so compare/dedup orientations modulo the octahedral group O (order 24) exactly — this is the same O-reduction bug that derailed an earlier agent (find_cubes also returns improper det=-1 frames; force proper frames); compute orbits, don't hand-derive stabilizers; include ALIGNED seeds (small orbits), not just generic ones, since records use them; and assert exactly 6 distinct cosets per family.

Rules: ≤4 cores; write symmetry_search.py, symmetry_search.jsonl, symmetry_search_report.md; do NOT edit six_cube_search_results.md (the main session merges a postscript) or the validated files; exact_search_results.jsonl is read-only; exact arithmetic only in predicates; invariant comments (why not what); no flattery; honest negatives welcome. Final message: gate pass/fail, the catalog table (each (G, partition) family: best total + seeds, field, beats/ties/loses 699), whether anything beat 699, and the 2-3 most promising families with their next move.
```
