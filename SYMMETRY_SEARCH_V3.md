# Spec: remaining symmetry families + shared-axis "intersection" families

For a Sonnet agent. Extends symmetry_search2.py (REUSE its validated
build_blocks / orbit / O-dedup / dispatch / climber — do NOT rewrite).
Read: symmetry_search2.py, six_cube_search_results.md Postscripts 10–11
(+ the 11 addendum), README.md. Record to beat: 717 (D₂:4+free2).

## Part A — rational families V2 never re-swept with full-quat grids

V2 only full-quat-swept C₃/C₂/D₂ (the payoff families) and confirmed
T/D₃ on their alignment loci. Do the rest at FULL integer-quaternion
resolution (orbit sizes computed, not assumed; include "core + free"
partitions of 6):
- C₄ (generic orbit 4 → 4+free2, 4+2 variants), D₄, D₆, and re-confirm
  D₃ / T with full-quat FREE cubes even where the orbit core is aligned.
- ~40 random full-quat starts per family + deep climb (single ±1..±6,
  two-component ±1/±2), reusing the V2/deepclimb climber.

## Part B — shared-axis "intersection" families (the main event)

The records live where TWO sub-symmetries share an axis: 699 = two C₃
orbits about (1,1,1); 717 = a D₂ 4-cluster of (1,1,1)-diagonal-related
cubes + the axis-aligned cube. Generalize: build the 6 cubes as a UNION
of two orbits under DIFFERENT groups about a COMMON axis n.

- Common axes to try (exact, rational): body-diagonal (1,1,1), face
  axis (0,0,1), edge axis (1,1,0). (Golden/√5 axes are Part C, deferred.)
- Orbit-pair partitions of 6 about the shared axis n, each block a
  full-quat seed orbited by its group Gₐ or G_b about n:
    C₂⊕C₄ (2+4), C₃⊕C₃ (3+3, the 699 family — GATE with it),
    C₂⊕C₂⊕C₂ (2+2+2), C₄⊕C₂ (4+2), C₃⊕C₂+free (3+2+1),
    D₂-cluster+free+aligned (the 717 family — GATE with it),
    C₆ (6) already done — skip.
- Also mixed "core + free": one shared-axis orbit (size 2/3/4) + the
  remaining cubes as free full-quat cubes climbed independently (this
  is the 717 template; try every orbit size for the core).
- Full-quat seeds for every free block; ~50 random starts per family +
  deep climb. Vary which cubes sit on the axis vs free vs aligned.

Intersection reading (do this too, cheaply): a config in TWO families at
once is fixed by ⟨Gₐ,G_b⟩ — often T/O/I. Where a shared-axis pair's
groups generate a polyhedral group (e.g. C₂ and C₃ about compatible
axes → T), test whether forcing that FULL symmetry (a single T/O orbit)
beats the looser shared-axis union. Report both.

## Gates (before trusting results)

- Reproduce 717 via the D₂-cluster+free+aligned shared-axis constructor
  (quats 5,2,2,2;-2,-2,2,5;-2,5,-2,2;-2,2,5,-2;2,1,1,1;1,0,0,0).
- Reproduce 699 via the C₃⊕C₃-on-(1,1,1) constructor.
- If either fails, the shared-axis builder is wrong — stop and debug.

## Rules & deliverables

Fast C++ engine ./cube_regions, ≤4 cores. Log every eval (family, shared
axis, full seed quats, total, by_depth) to symmetry_search3.jsonl. Flag
any total > 717 immediately (new record) and any deep-ceiling violation
(d3>164/d4>102/d5>36/d6≠1 = construction bug, stop). Do NOT edit
six_cube_search_results.md (main session merges a postscript),
symmetry_search2.py, or validated files; exact_search_results.jsonl
read-only; exact predicates only; honest negatives welcome. Robustness:
skip degenerate configs (build returns None) instead of asserting — that
bug already bit the deepclimb run. Write symmetry_search3.jsonl and
symmetry_search3_report.md: per-family best vs 717 with coverage, any
config > 717 with quats, and whether shared-axis "intersection" families
beat the single-family bests. Final message: did anything beat 717,
the best shared-axis family + its structure, and the Part-A family bests.
