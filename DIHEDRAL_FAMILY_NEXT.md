# DIHEDRAL_FAMILY_NEXT — handoff for continuing Postscript 25 (Sonnet-ready)

Context: read Postscript 25 in LEDGER.md first. This file
lists the concrete next tasks, each self-contained. Ground rules as always:
LEDGER.md is edited only by the main session (write your
results to a separate report file); validated files (slide3_q2.py,
cube_compound_exact.py, certify_six.py, qtower.py, golden_rotations.py,
cube_regions.cpp, exact_search*.py, mt_sim.py) are READ-ONLY — clone, never
edit; exact_search_results.jsonl is read-only ground truth; <=4 cores.

## The family in one line

Cube [-1,1]^3 plus its +-120deg rotations about axis n(psi)=(sin psi, cos psi, 0):
compound {I, S, S^2}, S(psi) = -I/2 + (3/2) n n^T + (sqrt3/2) [n]_x.
Every psi has exact edge-line coincidences in all three edge classes.
psi=35.264deg (arcsin(1/sqrt3)) is the octahedral 67; tan(psi)=phi^2 is the
golden 67; psi=45deg (face diagonal) is new, entries in Q(sqrt6), exact
count 49 = {30,18,1} via q6_count.py.

## Task 1 — region counts along the family (main open question)

For sin=p/r, cos=q/r Pythagorean, S(psi) has entries in Q(sqrt3).
1. Clone slide3_q2.py -> q3_count.py exactly the way q6_count.py was made
   (six targeted literal replacements changing the field constant 2 -> 3;
   diff q6_count.py against slide3_q2.py to see the pattern; keep the
   identity-pair self-test).
2. GATE: count the shared-axis member psi=0 (S = rot((0,1,0),120deg) =
   [[-1/2,0,sqrt3/2],[0,1,0],[-sqrt3/2,0,-1/2]], entries in Q(sqrt3)) and
   record it; also reproduce 49 for psi=45 using q6_count.py unchanged
   (this is the cross-engine consistency anchor: same compound family,
   different field points).
3. Sweep Pythagorean psi across (0,90deg): triples (p,q,r) with r <= ~85
   give ~40 well-spread angles. For each: build S over Q(sqrt3), certify
   orthonormal + S^3=I, exact_count. Write results (psi, p/q/r, total,
   depth profile) to dihedral_family_counts.jsonl + a short report .md.
4. Questions the sweep answers: is 49 the maximum of the family away from
   the 67s? is the count constant on the 12/18/24 crossing plateaus?
   where does the count jump (compare against plateau boundaries at
   psi = 21deg-ish and 45.5deg-ish — locate these exactly if counts jump there)?

## Task 2 — second engine for the 49 claim

q6_count.py is a single engine. Verify 49 independently: express the same
compound in the seed frame (columns [c w + s s_hat | -s w + c s_hat | u],
u=(1,-1,0)/sqrt2, w=s_hat x u, c=s=1/sqrt2) — entries in Q(sqrt2,sqrt3) —
and count with a tower engine following qtower.py's pattern with
D_LIST=(2,3) (qtower itself is hardwired to (5,3): clone it, base field
Q(sqrt2) instead of Q5, outer sqrt3). Expected: total 49, {30,18,1}.

## Task 3 — formalize the coincidence theorem

The z-edge (u-edge) class is proven: all three cubes' u-edges lie in common
planes perp to (1,1,1) at heights +-(sin psi + cos psi), +-(cos psi - sin psi);
coplanar non-parallel lines meet. The x/y-edge classes were verified to
1e-16 at random (theta, psi) (dihedral_scratch/family_check.py) and the
hand derivation in the frame {w, s_hat, u} gives f_A = sin psi cos^2 psi *
[(Cw - w).(u - Cu)] = 0 via Cw.u = -sqrt3/2, w.Cu = +sqrt3/2, w.u = 0.
Write this up properly (C45_notes.md style, new section): a page of vector
algebra, no computer needed. Also state the D3 symmetry proof:
U = rot(u, pi) satisfies U s_hat = -s_hat, hence U C U^-1 = C^-1, and
U M = M H with H = rot(e3, pi) a cube symmetry.

## Task 4 — does the family extend to n > 3?

The height argument only needs "face-axis perp to the C_n axis". For n=4
(90deg orbit about (1,1,1)? no — C4 about (1,1,1) is not a symmetry
grouping; use C4 about the axis itself) consider n cubes in a C_n orbit
about a common axis a, each with a face-axis perp to a. Do the u-edge
coincidences persist for n=4, 6 (cube self-symmetry makes 90deg orbits
trivial — check mod-90 spacing)? Any relation to the shared-axis 9-family
(Postscript 17 DOF hierarchy)? Numeric first (adapt family_check.py),
exact only if something interesting appears.

## Task 5 — viewer preset (main session only publishes)

Add "dihedral family" preset/slider to depth_explorer.html analogous to the
67<->67 slide: psi in [0, 90deg], matrices from the closed form (seed-frame
columns above, theta=0). Endpoints label the two 67s, tick marks at
35.26/45/54.74/69.09. This one SHOWS the crossings staying exact the whole
way — the pedagogical counterpart of the ghost rings. Spec it like
OPAQUE_SPEC.md with gates (t=35.264deg must reproduce the octahedral 67
histogram chips; crossing rings must show 30/24/18 per the plateau table).

## State snapshot (2026-07-15)

- q6_count.py: written, self-test + 49 count reproduce in ~0.5 s.
- dihedral_scratch/: family_check.py (identities + crossing map),
  family_fine.py (plateaus, invariants, golden fit), golden_diag.py
  (tan psi = phi^2 exact checks, 54 corner contacts), perp_check.py,
  perp_curve.py, edge_close*.py (the numerical discovery path).
- Ledger: Postscript 25 appended.
- Nothing yet in PROJECT.md / JOURNEY.md about this (candidate additions
  once Task 1-2 land).
