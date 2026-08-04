# A taxonomy of maximisers, applied across all levels

Written 2026-08-04, from a user observation: the 727 work had accumulated many
ways to categorise a maximiser and had applied them all to one number. These are
the axes, and the same questions asked of 13, 67, 183, 393, 727, 1217 and 1891.

Terminology follows [`GLOSSARY.md`](GLOSSARY.md) §8.0 — no bare "point", "line",
"plane" or "isolated"; "dimension" always names its space.

---

## The axes

1. **Moduli dimension** — the dimension of the maximiser set in the space of
   CONGRUENCE CLASSES. 0 means finitely many maximisers; ≥1 means a continuum.
   The gauge dimension is always 3 (rotating the whole compound) and carries no
   information, so it is never quoted below.
2. **Components** — how many connected pieces the class set has. Finite, by
   semialgebraicity. This is the well-posed replacement for "how many
   maximisers are there".
3. **Combinatorial types per component** — a type is a chamber, identified by
   the 64-entry per-label profile; the count is constant across a whole
   component while the type changes finitely often along it.
4. **Symmetry** — the order of the maximiser's own rotation group. Equivalently
   the stabiliser, which divides the volume of its congruence class.
5. **Arithmetic** — whether the maximiser is rational, and whether that is
   structural or an artifact of where a search sampled.
6. **Boundary behaviour** — what the count drops to at the edges of the
   maximiser set. Where the information is, when the interior is uniform.
7. **Findability** — the basin size under climbing, which is a property of the
   maximiser plus a move set, not of the maximiser alone.

## The table

Measured values only; blanks are open, not zero.

| n | max | moduli dim | components (class space) | types | symmetry | arithmetic |
|---|---|---|---|---|---|---|
| 2 | 13 | **1** (tangent) | **2 arcs + finitely many classes** | **1** | **12** | rational points dense on the arcs |
| 3 | 67 | **0** (codimension) | **exactly 2, both 0-dimensional** | 1 each | **24** oct / **6** golden | both irrational, ℚ(√2) and ℚ(√5) |
| 4 | 183 | **≥3** (aligned) | ≥1; all 5 climbs give ONE class | — | **3** | rational |
| 5 | 393 | — (aligned reads 0) | — | — | **3** | rational |
| 6 | 723 | **≥1** (tangent (1,1,1)) | — ; locus along the tangent is a UNION of intervals | **13** in one interval | **3** | rational |
| 6 | **727** | **1** (tangent) | **≥4** | **9** on arc A | **1** | rational and irrational on ONE arc |
| 7 | 1217 | **≥1** (aligned) | — | — | **1** | rational |
| 8 | 1891 | **≥2** (aligned) | — | — | **1** | rational |

**Tangents can now be found rather than guessed** (`tangent_finder.py`). A curve
inside a maximiser locus lies inside the wall surfaces through its point, so its
tangent is orthogonal to every active wall's gradient; one active wall reduces
the search from a sphere of directions to a circle, which is a finite scan.
Validated by recovering arc A's known tangent (1,−3,−6) — 2 of 96 in-plane
directions — then applied to 723, whose tangent was unknown and is **(1,1,1)**:
the sixth cube sliding along the shared C₃ axis, the very family Postscript 12
built 723 from. Walking it shows 723 holds on a UNION of intervals
([9/32,35/32] the longest), punctured by dips to 711, 699 and 687. The method
sees only catalogue walls, so a point lying on none of the 119 is still out of
reach.

Two probes are in play and they are not interchangeable. **Aligned** = how many
of the 2k single-coordinate ±ε moves preserve the count; 2d of them survive for
a family aligned with d coordinate directions, so a positive reading is a valid
lower bound and a zero reading means only "not aligned" (FAILURE_MODES 11d).
**Tangent** = stepping along a structurally identified direction, which is the
only probe that detects a locus in general position. 393, 723 and 727 all read 0
on the aligned probe; 727 is nonetheless 1-dimensional, which is exactly why the
393 and 723 cells are blank rather than 0.

## The components, listed

**n = 2, max 13.** In CLASS space, two positive-dimensional components plus
finitely many extra classes:
* the **body-diagonal arc** — Cayley t·(1,1,1); 13 at every t measured
  (1/5, 1/4, 1/3, 2/5, 1/2, 3/5, 2/3, 3/4, 3/2, 2, 3) and **punctured at t = 1**,
  where the rotation is a cube symmetry and the count collapses to 1. Off the
  diagonal the count is 9 at ε = 1/64 in every direction tried.
* the **edge arc** — the closed range [arccos(1/3), arccos(−1/3)] about an edge
  axis (Postscript 44).
* isolated classes: the half-turns about (1,2,3) and (1,1,2).

The 4 body diagonals and 6 edge axes are single orbits under the cube's own
symmetry, so they are ONE component each in class space, not 4 and 6.

**n = 3, max 67.** Two components, both 0-dimensional: the octahedral class in
ℚ(√2) and the golden class in ℚ(√5).

**n = 6, max 727.** At least four components, pairwise non-intersecting:

| arc | direction | through | carries |
|---|---|---|---|
| A | (1,−3,−6) | (19/3, −7, −11) | d = 13, 1093, 2741; 727 on s ∈ [9/4, 3]; 9 types; 723/721 at the ends |
| B | (1,1,−4) | (4/35, 2/5, −41/35) | d = 1614, 25561 |
| C | (1,−3/2,9/4) | (245/29, −295/29, 428/29) | d = 1785, 5305 |
| D | the record's own wall line | (7,14,1,−5) | the original compound; on none of A, B, C |

**Each of these appears THREE times in the pinned slice.** The base's C₃ (120°
about (1,1,1), acting on Cayley coordinates by cycling them) carries arc A to
two further arcs, both verified to count 727. Pinning the base spends the global
rotation but NOT the base's own symmetry, so slice-arcs overcount class-space
components by a factor of 3 here. A, B and C lie in distinct C₃ orbits — none of
A's two images has B's or C's direction — so they remain ≥4 components after the
quotient.

## What the filled cells already say

**Symmetry decays with n, from the maximum possible, and dies exactly where the
record left the symmetric stratum.** 24 and 6 at n=3, 12 at n=2, then 3, 3, 3,
then 1, 1, 1. The octahedral 67 has the FULL cube rotation group, order 24 —
the largest a compound can have. Note also that symmetry SEPARATES the two 67s
(24 vs 6) where the per-label profile cannot: their profiles are identical, so
this is a congruence invariant independent of Theorem R. The break is at 723 → 727, which
Postscripts 52-55 independently describe as 727 beating 723 by LEAVING the
corner-concurrence stratum. Two descriptions of one event. Note also that
**183 is C₃-symmetric**, which appears not to have been recorded — it was found
by wide-perturbation hill-climbing, not by symmetry-stratified seeding, so its
symmetry was never the point of the search that found it.

**Only n = 3 has a finite maximiser set.** Everything else measured is a
continuum. By the semialgebraic dichotomy (Postscript 80 Addendum 2) a
maximiser set is finite or uncountable, never countably infinite — so "finite"
was the only alternative n = 3 could have had, and the question is why it takes
it. The ledger's answer: the cap-sum bound is tight only at n ≤ 3, so the
optimum must saturate every layer, which forces rigidity, which forces isolated
classes — and an isolated class over ℚ need not be rational, whereas a
positive-dimensional one has dense rational points. That single mechanism
explains the irrationality of the 67s AND the rationality of every other record.

**The n = 3 row was re-tested** — see the final section. Its 0 originally rested
on a measurement now known to be unreliable, and has been re-founded on Step B's
decomposition instead.

**The n = 4 record is ONE class.** All five independent climbs that reached 183
(from four different seed cells, plus the control) land on the same
configuration up to congruence: symmetry order 3, depth profile {92,66,24,1},
and an identical multiset of O-reduced pair angles — three at 43.004° and three
at 46.826°, the 3+3 split that C₃ forces. That is a finer invariant than the
per-label profile Postscript 74 used to say "all the same type", and it agrees.
The angle split matches the cell (9,9,9,13,13,13) exactly: three 9-pairs at one
angle, three 13-pairs at the other.

## Cheapest ways to fill the blanks

* **Moduli dimension at 393, 1217, 1891** — lattice probe for a lower bound
  (positive readings remain valid), then a tangent test if it reads 0.
* **Components and types at 727** — sweep the 727 locus inside each of the 119
  catalogue wall planes. One such sweep found exactly one arc in 272 sampled
  cells, so the locus is thin and the enumeration is realistic. Incomplete on
  its own: the measured arc lies in only ONE catalogue plane, its second wall
  being of the never-enumerated W3/W4 type that Postscript 58 identified as the
  one that actually governs chamber structure.
* **Symmetry at the two 67s** — the same stabiliser computation, in ℚ(√2) and
  ℚ(√5). Expected to be large, which would extend the decay pattern leftward
  and make it a statement about all n rather than about n ≥ 4.
* **Boundary behaviour** — known only at 727 (723 and 721 at the ends of the
  measured arc, 711-721 transversally). Unknown everywhere else.


---

## The n = 3 re-test

The "exactly two isolated 67s" rested on a lattice probe reading 0, which
FAILURE_MODES 11d shows cannot distinguish an isolated class from a curve in
general position. Re-running that probe would answer nothing, and a tangent test
needs a tangent, which is exactly what is unknown. So the claim was re-founded
on Step B (Postscript 78) instead, where it becomes a codimension count.

**The argument.** Step B decomposes the three-cube total exactly:

    T = 1 + sum_ij p_ij + sum_i s_i,   p_ij <= 6 unconditionally

so 67 = 1 + 18 + 48 forces **all three pair terms to 6 AND all three singleton
terms to 16, simultaneously**. And s_i = 16 was measured to require both pairs
at cube i to be 13-pairs (g(13,13) = 16; every other combination <= 14), on a
set of dimension **2** in the 6-dimensional space of the two rotations at that
cube — codimension 4.

The n = 3 moduli space is 6-dimensional (two free cubes, the third pinned,
spending the gauge). Each s_i = 16 is a codimension-4 condition on it. Two of
them already exceed the available dimension, 4 + 4 = 8 > 6; three of them give
12. The 67s exist only because the three conditions are strongly dependent, and
a solution set cut by conditions that overshoot the ambient dimension this
badly is expected to be **0-dimensional**.

**Status: supported, not proved.** It is a codimension heuristic, not a rank
computation — the honest next step is the Jacobian rank of the active conditions
at each 67, in ℚ(√2) and ℚ(√5) respectively. But it is independent of the broken
probe, and it draws on a decomposition that did not exist when the original
claim was made.

**Two corroborations already on record.** The best RATIONAL three-cube compound
is 63, exhaustively; a positive-dimensional locus defined over ℚ would be
expected to carry rational points, and none reaching 67 exists. And the
distinct-axis part of the (13,13,13) cell, where both 67s live, has every
rational member degenerate (N3_STRUCTURE §5).

**What this does NOT rescue.** The count of 67 classes — "exactly two" — is a
separate claim resting on Theorem R, not on any dimension measurement, and is
untouched either way.


## Types along the arcs — and a trend

A type is a chamber: the per-label profile is constant on it and the count is
constant across the whole component. Measured where a tangent is known:

| locus | types | over |
|---|---|---|
| n=2, 13, body-diagonal arc | **1** | 199 rational points, t = 1/2 … 24/25 |
| n=6, 727, arc A | **9** | s ∈ [9/4, 3], walls at 75/32, 19/8, 79/32, 5/2, 21/8, 85/32, 43/16, 89/32 |
| n=6, 723, longest interval of its tangent | **13** | s ∈ [9/32, 35/32], walls at 19/64, 3/8, 15/32, 1/2, 17/32, 37/64, 39/64, 47/64, 25/32, 31/32, 33/32, 69/64 |

**Type-richness grows with n while symmetry falls.** The n=2 maximiser is
combinatorially UNIFORM along its entire continuum — one chamber, no walls at
all — while the n=6 maximisers are cut into 9 and 13 chambers over comparable
stretches. Read with the symmetry column (12 → 3 → 1), the picture is that low n
gives a maximiser that is highly symmetric and combinatorially rigid, and high n
gives one with no symmetry and a finely chambered plateau. The count is the same
along all of it either way; what varies is how much internal structure the
plateau carries.

## Still blank, and why

* ~~Symmetry of the two 67s~~ — **DONE**: 24 (octahedral) and 6 (golden).
  Representatives derived and recorded in [`MAXIMISERS.md`](MAXIMISERS.md).
* **n = 5, 393** — `tangent_finder.py` works in the sixth-cube-on-393-base
  slice; 393 itself needs a catalogue of wall planes for a FIFTH cube on a
  four-cube base, which has not been enumerated.
* **Components at n ≥ 4** — each needs its own arcs found first. The 727 route
  (sweep the 727 locus inside each of the 119 catalogue planes) is the model.
* **n = 7, 1217 and n = 8, 1891** — the aligned probe found 1 and 2 aligned
  directions respectively, so tangents exist and are axis-aligned there; the
  sweeps are straightforward but the engine is slow at these n.
