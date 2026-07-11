# Spec: symmetry search re-run with full-quaternion seed grids

Refinement of SYMMETRY_SEARCH_SPEC.md. The first run (symmetry_search.py,
Postscript 10) validated the FRAMEWORK — gates GA–GE pass, reproducing
67/681/699 — but its per-family seed grids were too thin: the C₃:3+3
family, which provably contains the 699 record, was searched only to
399. This run fixes the search coverage, not the construction.

For a Sonnet agent. Read: symmetry_search.py (REUSE its validated
build_group / orbit / O-dedup / dispatch / count functions — do NOT
rewrite them), symmetry_search_report.md, six_cube_search_results.md
Postscript 10, README.md.

## The one change: seeds are FULL integer quaternions, not axis-angles

The first run parameterized many orbit seeds as a single half-angle
(q,p) rotation about a coordinate axis — a thin 2-parameter slice. The
699 record needs a GENERAL seed (its second triple is the C₃-orbit of
the quaternion [41,28,22,14], not any axis rotation). So:

- Each G-orbit's seed = a general integer quaternion (w,x,y,z),
  gcd-reduced, every |component| ≤ 512, mapped to a rotation by
  golden_rotations.rot_from_quat (rational G) or the field seed for
  ℚ(√5) families.
- A family with k orbits + f free cubes has 4(k+f) integer degrees of
  freedom. Search them jointly.

## Families to re-run (priority order) and how

Reuse the exact orbit CONSTRUCTION from symmetry_search.py for each;
only the seed sampler + climber change.

1. **C₃:3+3 (about (1,1,1)) — FIRST, it holds the record.**
   - Two full-quat seeds S₁,S₂; orbit each by C=120° about (1,1,1).
   - Gate this family: one climb start MUST be the known 699 seeds
     (S₁ from [3,1,0,0]-type, S₂=[41,28,22,14]); confirm the family
     search now reaches ≥ 699 (if it still caps below 699, the seed
     mapping is wrong — stop and debug).
   - Then random-restart search: ~30 random full-quat seed pairs +
     exact hill-climb (moves: ±1/±2 on any of the 8 components, re-gcd,
     |c| ≤ 512; reject moves breaking the C₃ construction). Hunt > 699.
2. **Core+free families** (their first-run bests are floors):
   T:4+free2 (661), D₃:3+3 (657), C₂:2+2+2 (653), D₂:4+free2 (651),
   C₆:6 (649). Re-search each with full-quat seeds for BOTH the orbit
   core and the free cubes, climb deeply from ~20 random starts each.
3. **Golden I:5+free / C₅:5+free (681)**: the free sixth cube already
   got a real search (that's how 681 was found); just confirm with a
   deeper radius-3/4 climb from the logged 681 point that nothing
   higher is adjacent. ℚ(√5) path (golden_six machinery), slower —
   budget a few hundred evals only.

## Method

- Fast C++ engine (./cube_regions) for all rational families, ≤4 cores.
- Log every eval to **symmetry_search2.jsonl** (don't clobber the first
  run) with (G, partition, full seed quats, total, by_depth).
- Flag immediately any total > 699 (record) or any deep-count violation
  (d3>164, d4>102, d5>36, d6≠1 — those would signal a construction bug,
  not a find).
- State per family: the seed-grid size, climb radius, and #restarts, so
  coverage is auditable (the first run's failure was exactly unstated
  thin coverage).

## Deliverables

symmetry_search2.jsonl, and symmetry_search_report2.md: for each
re-run family, the NEW best (vs the first run's floor and vs 699),
whether C₃:3+3 now reproduces ≥699 (the key correctness check), and any
config > 699 with quats. Do NOT edit six_cube_search_results.md (the
main session merges a postscript update) or the validated files;
exact_search_results.jsonl read-only. Honest negatives welcome: "with
full-quat grids the top families still cap at 699/681" is a much
stronger statement than the first run could make, and is the goal if no
new record appears. Final message: does C₃:3+3 now reach ≥699, did
anything beat 699, and the refreshed per-family bests.
