# Spec: symmetry-stratified search of the region-rich walls

For an implementation agent (Sonnet-level — this needs finite-group
computation, multi-engine dispatch, and exact arithmetic; not a Haiku
task). Read first: README.md, six_cube_search_results.md Postscripts
4–9, QFIELD_SPEC.md (field/wall taxonomy), golden_six.py + slide3_q2.py
+ qtower.py (the field engines you dispatch to), cube_regions.cpp (the
fast rational engine).

## 0. Goal

The all-time records (655, 681, 699) live on SYMMETRY walls, found ad
hoc. This program searches them systematically: enumerate the finite
catalog of symmetry-constrained subspaces and exact-count each. It does
NOT try to enumerate every accidental (non-symmetric) incidence — those
are conjectured sub-maximal (census/T2 evidence) — so "all region-rich
areas" here means "all symmetry walls," stated as a scoped claim, not a
theorem about the global maximum.

## 1. Setup (get this right)

A cube is invariant under its own octahedral group O (order 24), so a
cube ORIENTATION is a coset S·O in SO(3)/O; two rotation matrices S, S'
give the same cube iff S⁻¹S' ∈ O. A compound of 6 cubes = 6 distinct
cosets.

Fix a finite subgroup G ⊂ SO(3). A compound is G-invariant iff its set
of 6 cosets is closed under left-multiplication by G. It is therefore a
union of G-ORBITS. The orbit of a seed S has size
    |G| / |Stab(S)|,   Stab(S) = { g ∈ G : S⁻¹ g S ∈ O } = G ∩ S·O·S⁻¹,
i.e. the elements of G that happen to be symmetries of the seed cube in
that orientation. Generic seeds have trivial stabilizer (orbit size
|G|); seeds ALIGNED so a cube axis (2/3/4-fold) coincides with a G axis
have larger stabilizers and hence SMALLER orbits. The records use
aligned seeds (small orbits), so you MUST include aligned seeds, not
just generic ones.

Do not hand-derive stabilizers; COMPUTE orbits: build G as an explicit
matrix group, and for a candidate seed S form orbit(S) = O-dedup of
{ gS : g ∈ G } and read off its size. (O-dedup: gᵢS ≡ gⱼS iff
S⁻¹gᵢ⁻¹gⱼS ∈ O; test membership in O exactly.)

## 2. The catalog to enumerate

For each subgroup G, enumerate the ways 6 cubes decompose into G-orbits
(sizes summing to 6, orbits O-disjoint). Include the important mixed
form **"symmetric core + free remainder"**: a G-orbit of size m < 6
plus (6−m) cubes of lower or no shared symmetry, the remainder searched
separately — this is exactly how 681 (I-orbit of 5 + one free cube) and
699 (two C₃ orbits, = 3+3) arise.

Subgroups and the field each forces (dispatch target):

| G | \|G\| | orbit sizes ≤6 (aligned seeds) | field | engine |
|---|---|---|---|---|
| C₂,C₃,C₄,C₆ | 2,3,4,6 | n and its divisors; +free | ℚ | cube_regions (C++) |
| D₂,D₃,D₄,D₆ | 4,6,8,12 | 2,3,4,6,… ; +free | ℚ | cube_regions |
| T | 12 | 4,6,12→ use 4+free,6,3+3? (compute) | ℚ | cube_regions |
| O | 24 | 3,6,8,… (3-cube compound is an O-orbit of 3) | ℚ | cube_regions |
| C₅,C₁₀ | 5,10 | 5,10 → 5+free | ℚ(√5) | golden/exact |
| I | 60 | 5,15,20,… (stab ⊆ T); 6=5+free | ℚ(√5) | cube_compound_exact / golden_six |
| C₈,D₈ | 8,16 | 45° content → 2,4,8 | ℚ(√2) | slide3_q2 |
| C₁₂ | 12 | 30° content | ℚ(√3) | qtower(d=3) |
| mixed axes | — | two incommensurate G-axes | tower ℚ(√a,√b) | qtower |

(The cyclic tower Cₙ is formally infinite; bound it at n ≤ 12 — a cube
only "sees" rotations mod O, so higher folds add no distinct alignments
that a ≤12 case doesn't already probe. Note orbit sizes under I are
{5,15,20,30,60} because a cube shares only T-type elements with I — so
6 is never a single I-orbit; the golden family is 5+free.)

## 3. Construction & dispatch

For each (G, partition) family:
1. Parameterize the seed(s): each orbit needs one seed. Rational-G
   families parameterize seeds by INTEGER quaternions (cube_regions,
   ~ms/eval). Field-G families parameterize seeds in the field.
2. Build the 6 cube matrices = union of the orbits; assert exactly that
   you got 6 distinct cosets (O-dedup count == 6) — a collapsed family
   (fewer than 6) is degenerate, log and skip.
3. Exact-count via the dispatched engine. Verify the count is exact
   (no float predicate).

## 4. Within-family search

Each family is a low-D continuous space (1–6 seed parameters, minus
alignment constraints). Search:
- coarse grid over seed parameters (integer-quat grid for rational G;
  small field-parameter grid otherwise);
- exact greedy hill-climb from the best (reuse phase_b_hillclimb's move
  set: ±1/±2 on one integer component, re-gcd, |c| ≤ 512), respecting
  the family constraint (moves that break G-invariance are rejected —
  or, for "core + free" families, freely climb the FREE cubes while the
  core stays exact);
- log every eval with (G, partition, seeds, total, by_depth) to
  symmetry_search.jsonl.

## 5. Gates (hard, before trusting any family)

- Gᴀ: O-dedup and orbit machinery — a generic C₃ seed gives orbit size
  3; a seed with its 3-fold axis on the C₃ axis gives orbit size 1.
- Gʙ: reproduce 67 — the octahedral 3-cube compound is an O-orbit of
  size 3 (and equals a golden triple's count).
- Gᴄ: reproduce 699 — the (C₃, 3+3) family on the (1,1,1) axis contains
  quats [[3,1,0,0],[3,0,1,0],[3,0,0,1],[41,28,22,14],[41,14,28,22],
  [41,22,14,28]] at total 699.
- Gᴅ: reproduce 681 — the (I, 5+free) family (golden five + a sixth on
  the (1,1,1) axis) via golden_six.
- Gᴇ: a rational random 6-cube config still counts correctly through
  your dispatch path (cross-check one seed vs cube_regions).
If a gate fails, stop and debug; do not report family results.

## 6. Deliverables & priorities

Order: gates → Phase 1 (all RATIONAL G, the fast C++ sweep — this is
where a rational record >699 would surface, cheaply) → Phase 2 (ℚ(√5):
I and C₅ families) → Phase 3 (ℚ(√2), ℚ(√3), then towers for mixed axes,
only for the families Phase 1/2 flag as promising).

Write: symmetry_search.py (the enumerator + dispatcher + climber, module
docstring + "# Working principles: SYMMETRY_SEARCH_SPEC.md"),
symmetry_search.jsonl (all evals), and symmetry_search_report.md — a
catalog table (each (G, partition) family: best total + seeds, field,
whether it beats/ties/loses to 699, and the active alignment), the two
or three most promising families with the next move, and a "families
that collapse or lose" list. Do NOT edit six_cube_search_results.md
(the main session merges a postscript); exact_search_results.jsonl is
read-only.

## 7. Honest limits (state them in the report)

Accidental (non-symmetric) walls are out of scope; the claim is
"searched all symmetry walls up to Cₙ (n≤12), the quadratic-field
groups, and the listed towers," not "found the global maximum." Within
each family the continuous seed search can miss a narrow interior peak;
report the grid resolution and climb radius so coverage is auditable.
