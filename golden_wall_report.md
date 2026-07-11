# Golden wall report: golden five-cube compound + one rational sixth cube

Question: can the golden five-cube compound (exact 351 regions, Q(√5)
coordinates) plus a sixth congruent cube under a RATIONAL rotation beat the
rational six-cube record of 635? **Answer: yes — 681, beating 635 by 46.**
All counts below are exact (certify_six.exact_count_config, Q(√5)/CN
arithmetic, no floats in any predicate). Implementation: `golden_six.py`
(+ follow-up sweeps `golden_sweep.py`, `golden_sweep2.py`); full log of all
539 evaluations (425 unique configs): `golden_search.jsonl`.

## (a) Validation gates — all three PASS (run before any search)

- **V1 PASS.** Golden sub-compounds N=1..5 through BOTH paths
  (cube_compound_exact.run(N) and this project's wrapper path into
  certify_six.exact_count_config): 1 / 13 / 67 / 177 / 351, identical on
  both paths, matching the expected series exactly.
- **V2 PASS.** First record of exact_search_results.jsonl (seed 40,
  total 575, by_depth {1:90, 2:184, 3:162, 4:102, 5:36, 6:1}) reproduced
  exactly through this project's shim (rationalize N=512 →
  exact_count_config): total 575, identical depth histogram. 35.7 s.
- **V3 PASS.** Golden five + exact duplicate of golden cube 1 (identity
  rotation) = 351, as required — the coincident-plane bookkeeping
  (plane_key / owners_of coincidence classes in certify_six.py) handles six
  fully doubled planes correctly; by_depth {1:144, 2:84, 3:56, 4:42, 5:24,
  6:1} (regions relabel one depth deeper, count unchanged). Additionally
  verified on an IRRATIONAL coincident stack: duplicate of golden cube 2
  (√5-bearing plane normals) also gives exactly 351.

Reference values verified against six_cube_search_results.md Postscripts
4–5 (not from memory): rational record total 635 with by_depth
{1:118, 2:214, 3:164, 4:102, 5:36, 6:1}; observed rational ceilings
d1 ≤ 118, d2 ≤ 214 (the older 112/208 were falsified); conjectured
d3 ≤ 164, d4 ≤ 102, d5 ≤ 36, d6 = 1. The numbers 112/208 in the task
brief were the superseded pre-falsification ceilings.

## Structural discovery: families A and B as specified are IDENTICAL

Golden cube 1 is the axis-aligned cube — build_axes() lists the standard
basis first, so find_cubes()'s first triple is (e_x, e_y, e_z) and G1's
matrix is the identity. Hence family B as specified (sixth = Q·G1) is
literally family A (sixth = Q). Confirmed empirically: all 114 quaternions
evaluated in both families pre-fix have identical totals and identical
depth histograms (first 228 log lines). Family B was therefore re-anchored
on golden cube 2 (sixth = Q·G2, G2 genuinely irrational); post-fix B
records carry `"anchor": "G2"` in the log, pre-fix B records (no anchor
field) duplicate their A partner.

## (b) Timing and budget

Measured per-eval wall clock (single process): 8–36 s, typically 15–25 s
(6-cube exact arrangement, ~5–7k cells). All searches ran on an 8-worker
multiprocessing pool: ~0.3–0.5 eval/s aggregate. 539 logged evaluations
total ≈ 40 min of pool time, spread over: symmetric candidates (~45 quats
× 2 families), 75 random quaternions × 2 families (Python `random.Random`,
**seed 1729**, components uniform in [-512, 512], gcd-reduced — matching
exact_search.py's N=512 quaternion scale), greedy hill-climbs (±1/±2 on one
component, gcd-reduce, |c| ≤ 512), and two targeted angle sweeps motivated
by the early results (rotations about (1,1,1) and about x).

## (c) Best total per family

| family | best | quaternion | by_depth |
|---|---:|---|---|
| A (sixth = Q) | **681** | (2,1,1,1) and 27 others, see below | {1:234, 2:192, 3:128, 4:90, 5:36, 6:1} |
| B (sixth = Q·G2) | **679** | (8,3,0,0), also (19,7,0,0), (21,8,0,0) | {1:238, 2:192, 3:122, 4:90, 5:36, 6:1} |

Both hill-climbs terminated at radius-2 local maxima (all 64 evaluated
neighbor moves of (2,1,1,1) ≤ 681; likewise around (8,3,0,0)).

## (d) Top configurations and structure

**The 681 plateau is the generic rotation about a body diagonal.** All 28
configs found at 681 are family A with quaternions on or adjacent to the
(a,b,b,b) line = rotation of the sixth cube about (1,1,1), which is
simultaneously a 3-fold axis of golden cube 1 AND of the icosahedral
compound. Every one of them has the IDENTICAL histogram
{1:234, 2:192, 3:128, 4:90, 5:36, 6:1} — a θ-independent combinatorial
plateau, the same phenomenon as the six6 family's constant 355. Exact
sweep of θ (family A, rotation about (1,1,1); values exact, angles float
for display only):

- θ ≈ 8–10°: 681 — (18..22, 1,1,1)
- θ ≈ 20–60°: 657 (669 island at θ=38.2°, (5,1,1,1)); θ=60° (3,1,1,1),
  an EXACT rational rotation, gives 657
- θ ≈ 64–112°: 681 (669 dips at 95.6°/98.2°)
- θ = 120° (1,1,1,1): 351 — sixth cube coincides with golden cube 1
  (120° about a diagonal is a cube symmetry)

The task brief's "√3-convergent" candidates (2,1,1,1), (7,4,4,4),
(12,7,7,7), (26,15,15,15) — w/x → √3, limiting rotation 90° about
(1,1,1), which is NOT rational (cos 45° ∉ ℚ) — all sit inside the 681
band. Note 60° about (1,1,1) IS exactly rational ((3,1,1,1)), contrary to
the brief's assumption; it lands on the lower 657 chamber.

**Symmetric coincidences ("stuck at 351"):** 30 evaluated quaternions give
exactly 351 (18 in A, 12 in B) — precisely the cases where the rational
rotation maps the sixth cube onto one of the five golden cubes (e.g. all
cube-group rotations in family A: 90°/180° about coordinate axes, 120°
about diagonals). The sixth cube then contributes zero new geometry, only
depth relabeling — the coincident-plane invariant of gate V3 exercised 30
more times, all consistent.

**Family B's peak** is a rotation about the x-axis — a RATIONAL 2-fold
axis of the icosahedral compound — by θ ≈ 40.3–41.9°: 679 with
d1 = 238. Flanking chambers give 675; generic random B quats top out at
665. B's diagonal-axis sweep is everywhere ≤ 665 (and drops to 533 at the
exact 60° points (3,±1,±1,±1)).

**Random baseline:** the 150 random-quaternion evals (75 quats × both
families, seed 1729) ranged **637–665**, median 648 — i.e. EVERY random
rational sixth cube attached to the golden five beat the all-rational
record of 635. The sub-635 totals in the log (533/547/551/…) all come
from symmetric wall candidates (near-coincidences), never from the random
batch. The targeted symmetric axes, not the random search, found both
family peaks (random max: 665).

**Depth records within this search** (vs rational-record values):

| depth | max here | config | rational record/ceiling |
|---|---:|---|---:|
| d1 | **238** | B (8,3,0,0), total 679 | 118 (observed max) — **exceeded by 120** |
| d2 | 198 | A (2,3,3,3), total 681 | 214 — not reached |
| d3 | 132 | A (-158,424,81,440), total 649 | 164 (conjectured ceiling) — not reached |
| d4 | 90 | many (all top configs) | 102 — never attained here |
| d5 | 36 | all non-degenerate configs | 36 — matches the 6-per-cube law |
| d6 | 1 | always | 1 (theorem) |

The d1 = 238 (and 234 in every 681 config) is the standout: the golden
five alone carries d1 = 180 (36 per cube — each golden cube's surface is
cut into 36 depth-1 pieces by the other four), and a well-placed sixth
cube pushes this to 238, double the all-rational-configuration record of
118. This does NOT falsify conjecture C2 of the campaign (that conjecture
is about all-rational configurations; the golden five is not rational) —
it shows the golden wall carries far more shallow-depth structure than any
generic rational configuration found. Conversely the deep counts are
POORER than generic rational configs: d3 ≤ 132 < 164 and d4 = 90 < 102
everywhere here, while random rational seeds hit d4 = 102 in 82.6% of
cases. The golden symmetry concentrates regions at depth 1–2 and starves
depth 3–4; the +46 total win comes entirely from the shallow end.

## (e) Verdict

- **Golden five + rational sixth BEATS the rational six-cube record: 681
  vs 635 (+46).** Best configuration: family A, quaternion (2,1,1,1) —
  the sixth cube rotated ~81.9° (any angle in the ~64–112° or ~8–10°
  chambers) about the (1,1,1) diagonal. Exact, certified, and locally
  maximal under ±1/±2 quaternion-component moves.
- **It boosts depth 1 far beyond its known rational record: d1 = 238 vs
  118.** No other depth is boosted: d2/d3/d4 all fall short of their
  rational records, d5/d6 match the universal laws (36, 1).
- The result is consistent with (and does not test) the C4/C5/C6 ceilings,
  which concern rational configurations.

## Open items

- Family C (sixth = G2·Q, right-composition) was not explored — a third
  genuinely distinct orbit.
- The 681 plateau's boundary in the full 3-parameter quaternion
  neighborhood is only sampled (64 neighbor moves), not mapped.
- Whether 681 is optimal over ALL Q(√5)-compatible sixth cubes (not just
  rational-rotation ones, i.e. allowing √5-bearing rotations outside the
  golden compound's own symmetry) is open — the search space here was
  rational quaternions only, per the task scope.
