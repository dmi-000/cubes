# How many regions do overlapping cubes make? — a self-contained write-up

*Last updated 2026-07-16. This document is standalone: every term is
defined here, and no other file is required to follow it.*

---

## 1. The question

Take several identical cubes, all sharing the same centre point, each
turned to a different angle, and imagine them made of glass so you can
see all their faces at once. The faces slice space into many pieces. This
project asks a simple question with a surprisingly rich answer:

> With *n* cubes sharing a centre, how many bounded pieces can their faces
> cut space into, and which arrangement of angles achieves the most?

We insist on **exact** answers — whole numbers proven correct, not
measured approximately — and we search for the maximizing arrangement.

### Making it precise

- Each cube is the same: the axis-aligned cube whose corners are at
  (±1, ±1, ±1), then rotated about the common centre (the origin). So a
  configuration of *n* cubes is just a choice of *n* rotations.
- Each cube has 6 faces, each lying in a flat plane. With *n* cubes there
  are 6*n* planes. These planes divide all of space into cells.
- A cell is **bounded** if it is finite (enclosed on all sides) and
  **unbounded** if it stretches to infinity. There is exactly one
  unbounded outside region; we count only the bounded ones. "Total" =
  number of bounded pieces.
- Every bounded piece lies **inside** some number of the cubes. Its
  **depth** is that number, from 1 (inside just one cube) up to *n*
  (inside all of them). We track the whole profile, written
  `by_depth = {1: …, 2: …, …, n: …}`. The innermost piece — inside all
  *n* cubes at once — is always a single convex blob, so the depth-*n*
  count is always 1.

A worked feel for the numbers: one cube alone makes 1 bounded piece
(itself). Two generic cubes make 13. Three make up to 67, and so on. For
six cubes the count runs into the hundreds, and finding the true maximum
is hard.

### Specifying a rotation with four integers

A rotation in 3D can be encoded by four numbers called a *quaternion*,
written (w, x, y, z). The only facts needed here:

- Any four integers give a valid rotation, and — crucially — that
  rotation has **rational** entries (fractions), so it can be represented
  and computed with *exactly*, no rounding.
- Scaling all four by the same factor gives the same rotation, so we keep
  them as small whole numbers with no common factor.

Throughout, a configuration is written as a list of *n* integer
quaternions, e.g. `4,1,1,-1 ; 3,3,7,3 ; …` (one cube per group). Some
special maximizing arrangements need rotations built from √2 or √5
instead of plain fractions; those are handled with exact arithmetic in
the corresponding number system.

---

## 2. Why exact counting, and how it is done

**The cautionary tale.** The project began by counting pieces
approximately: chop space into tiny voxels (3D pixels) and flood-fill to
label connected pieces. This *cannot reliably rank arrangements*. One
random configuration showed an apparent stable count near ~1340 across
three resolutions — but about 70% of those "pieces" were unresolved
slivers thinner than the voxel grid; its true exact count is 567. Both
over-counting (one piece split into many) and under-counting (many pieces
merged into one) happen at once, and a stable-looking approximate number
is not proof of anything. Every result below therefore rests on exact
arithmetic.

**The exact method.** Because each rotation is rational, each of the 6*n*
face-planes has rational coefficients, and the entire arrangement of
pieces can be constructed with exact fraction arithmetic:

1. Start with a large box and repeatedly cut it by each plane, splitting
   every cell the plane crosses into two convex cells. This yields all
   the convex fragments exactly.
2. A cube's face is a bounded *square*, not an infinite plane. So some
   fragment boundaries lie on the plane but *outside* the actual square
   face — these "phantom" walls are not real separations. Fragments
   touching across a phantom wall are the same piece and get merged
   (tracked with a union-find bookkeeping structure).
3. For each resulting piece, record its depth (how many cubes contain a
   test point inside it) and tally the results.

No step ever compares a floating-point number to zero; all decisions are
exact comparisons of fractions (or of numbers of the form a + b√5, etc.,
when needed). A fast version written in C/C++ counts a six-cube
configuration in a fraction of a second; a slower reference
implementation in Python cross-checks it.

**Validation.** Before trusting any search, the counter must reproduce
known exact values: six cubes fanned around a shared axis must give
exactly (2·6−1)² = 121; the five-cube "golden" compound (below) must give
351; and the fast and slow counters must agree on hundreds of random
cases with zero disagreements.

---

## 3. Warm-up: the small cases

The richest reference arrangement is the **compound of five cubes
inscribed in a regular dodecahedron** — five cubes whose corners sit on
the 20 vertices of a dodecahedron. Its sub-compounds count exactly:

| number of cubes | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| bounded pieces  | 1 | 13 | 67 | 177 | 351 |

These arrangements involve the golden ratio and are represented exactly
using numbers of the form a + b√5. They are the best known for two and three cubes — but *not* for
four or five: the golden four-cube compound (177)
is beaten by a purely rational four-cube arrangement reaching **183**,
and the golden five-cube compound (351) is beaten by a rational five-cube
arrangement reaching **393** — which is, strikingly, a *sub-compound of
the best six-cube arrangement* (drop one of its six cubes). This is the
same surprise as at six cubes, where the best rational arrangement (723)
beats the golden-based one (681): the golden compound is the best
*symmetric* configuration, not the overall maximum. So the records for
four and five cubes are at least 183 and 393, and none of these is proven
maximal.

**The records nest.** The best six-cube arrangement (723) contains the
best four-cube one (183) as a sub-compound, contains a five-cube
sub-compound (393) that beats the old five-cube record, and its pairs
reach the two-cube record (13). Outstanding arrangements are built from
outstanding smaller ones — which suggests constructing a record for *n*
cubes by taking the best (*n*−1)-cube arrangement and adding one more cube
well. (Curiously the nesting is cleanest at even sizes: the three-cube
sub-compounds of 723 reach only 63, short of the golden 67, because that
maximum needs a symmetry 723's rational structure doesn't share.)

**Local perfection is globally frustrated past three cubes.** The golden
compound has a remarkable property: *every* one of its sub-compounds is
optimal — every pair is a best pair (13), every triple a best triple
(67). That is exactly what forces its high symmetry, and up to three cubes
it also makes it the overall maximum. But from four cubes on, the property
*backfires*: the golden four-compound has every subset optimal yet totals
only 177, while the true maximum (183) has to *detune* — its triples drop
to 63, half its pairs to 9 — to win. You cannot both make every part
optimal and maximize the whole; it's a frustration, like a magnet whose
neighbours all want to align but can't all be satisfied at once. The
reason it switches on at four cubes is the appearance of a *middle* depth
layer: golden loads the outermost layer (depth-1) heavily — more than the true maxima do — and maxes the
deep layers that are capped at 6n, but four cubes is the first size with a
depth layer that is neither — and there the maximum beats golden by
shifting count out of the outer layer into the middle. This one idea ties
together why golden loses, why the records keep only a modest 3-fold
symmetry instead of the full icosahedral one, and why building from a
record (which already carries this detuning) beats assembling from
perfect parts. At the level of the parts themselves the accounting is
exact: the record's three-cube pieces count 63 = {44, 18, 1} against the
perfect triple's 67 = {48, 18, 1} — *identical* in the deep layers
(which are what a larger arrangement inherits) and behind only in
depth-1, the layer the larger arrangement recuts anyway. The perfect
triple pays for those four disposable regions with its last tunable
degree of freedom. A good building block is deep-saturated,
shallow-detuned, and keeps its knob.

One observation here seeds a major theme. There are two *different*
three-cube arrangements that both reach the maximum of 67, and they
achieve it by different geometry:

- The **octahedral** three-cube compound (three cubes each turned 45°
  about a different coordinate axis), which uses √2.
- Any three cubes from the golden five, which uses √5.

They differ in *how their faces line up*, a distinction ("edges versus
corners") made precise in Section 6.

---

## 4. The six-cube search and the record chain

For six cubes the maximum is not known. Two facts shape the search.

First, **random angles are not enough.** If you pick six rotations at
random, you land in a "generic" arrangement — no special alignments — and
these top out around 635 bounded pieces no matter how many millions you
try. The record-setting arrangements are *special*: they sit on
lower-dimensional **walls** in the space of configurations, sets where
some cubes line up exactly. Walls are vanishingly rare (measure zero), so
random search never hits them. Every record beyond 635 came from
deliberately *constructing* an alignment, not from sampling.

Second, **the good walls are symmetric.** An arrangement that looks the
same after some rotation (has a symmetry) forces its cubes into related
families. The current chain of records, and how each was found:

| pieces | the arrangement | how it was found |
|---|---|---|
| 635 | a balanced generic-looking config | 278,000-config random campaign + local search |
| 655 | two pairs of cubes at a special 60° body-diagonal angle | built the alignment by hand |
| 681 | the golden five + a sixth cube on a shared axis | search among golden (√5) configurations |
| 699 | two three-cube groups sharing one diagonal axis | overlaying two symmetric triples |
| 705 | same family, searched more thoroughly | symmetry search with better coverage |
| 717 | four cubes in a symmetric cluster + two more | symmetry search |
| **723** | three cubes about a diagonal + three "free" cubes | shared-axis "intersection" family |

**723 is the current record.** Its depth profile is
`{1: 210, 2: 216, 3: 164, 4: 96, 5: 36, 6: 1}` (summing to 723). Its six
cubes, as integer quaternions:

```
4,1,1,-1 ; 3,3,7,3 ; 5,-1,-5,-5 ; 2,1,1,1 ; 1,1,1,1 ; 5,2,2,2
```

The searches that produced these fall into four kinds, each fixing a
blind spot of the previous:

1. **Mass random campaign.** Counting ~278,000 random configurations
   exactly mapped the generic behaviour and disproved some early guesses
   about the maximum (an earlier "record" of 623 turned out not even to
   be a local best).
2. **Hand-built walls.** Deliberately imposing a known alignment (the
   golden compound, or a special pair angle) and searching the leftover
   freedom — this found 655 and 681.
3. **Symmetry catalogue.** Every symmetric arrangement is a union of
   symmetric families of cubes ("orbits" of a rotation group). The
   rotation groups are a known finite list (cyclic, dihedral,
   tetrahedral, octahedral, icosahedral), so the symmetric arrangements
   form a *finite catalogue* one can walk through systematically. A first
   pass under-searched (its parameter grid was too coarse and missed its
   own best case), but re-run properly it produced 705, 717, and 723, and
   showed no other symmetry type beats them.
4. **Algebraic search** (Section 8): solve for the exact alignments
   directly with symbolic algebra instead of approaching them by trial.

---

## 5. Patterns that hold across every arrangement

Several exact regularities appear everywhere we look:

- **All the depth-layer caps obey one formula.** The ceiling for the
  layer l steps up from the deepest is C(l, n) = (12l−6)·n − 2(l²−1):
  the second-deepest layer is capped at 6n, the next at 18n−6, then
  30n−16, then 42n−30 — and the outermost layer at 10n²−14n. Across
  roughly a million exactly-counted arrangements (two to seven cubes),
  every testable cap is *attained exactly and never exceeded*. The golden
  compounds attain precisely the outermost-layer cap (48, 104, 180 at
  n = 3, 4, 5); the records attain the deep caps; no arrangement attains
  all caps at once (that is the frustration, and summing the caps gives
  an upper bound on the total — 801 at six cubes, against the record
  723). The same formula is confirmed by a completely independent
  measurement: the vertex counts of the sphere diagrams of Section 6
  match its prediction exactly. Proving it is now the project's central
  theory goal.

- **Deep layers are capped — and the second-deepest cap is exactly 6n.**
  The depth-3, depth-4, depth-5 counts of a six-cube arrangement never
  exceed 164, 102, 36, on any arrangement tried. (Depth-6 is always 1,
  provably — the innermost region is one convex blob.) The last of these,
  depth-5 ≤ 36, turns out to be one case of a clean law across all sizes:
  the **second-deepest layer, depth-(n−1), never exceeds 6n**, and equals
  6n generically — verified for every size from two to six cubes (12, 18,
  24, 30, 36). This unifies five separately-observed ceilings into one
  statement with a short proof sketch: the "which cube is innermost"
  pattern on the direction-sphere (Section 6) is anchored at each cube's
  six face-centre directions, giving at most six regions per cube, hence
  ≤ 6n. Making that rigorous reduces to a single lemma about how the
  face-normals' directions can overlap; the lemma holds in every case
  sampled but is not yet proven in general (Section 10). The 6n cap is
  also **hereditary**: removing any cube from a record drops depth-(n−1)
  from 6n exactly to 6(n−1) in the smaller arrangement.
- **Deep layers are "quantized," shallow layers grow — and records
  trade between them.** This is the central structural fact, visible
  across ~457,000 counted arrangements. As the total climbs, the deep
  layers fill to their caps *in order, deepest first, then freeze*:
  depth-5 reaches 36 (around total 475), then depth-4 reaches ~102
  (around 525), then depth-3 reaches ~164 (around 600). The reason is
  geometric (Section 6): a deep layer either realizes its one *generic*
  value (the cap) or a smaller degenerate value — it cannot exceed the
  cap, so it is effectively quantized. The shallow layers (depth-1,
  depth-2), by contrast, have no cap and keep growing with the
  arrangement's complexity. So once the deep layers are pinned, every
  further gain in the total comes from the shallow layers alone (depth-1
  climbs from ~120 to over 200; depth-2 from ~195 to ~215). Two kinds of
  trade-off result:
  - *At a fixed total*, regions shuffle between adjacent layers with the
    total conserved (in one family depth-2 + depth-3 stays exactly 368).
  - *To raise the total*, since the deep layers can't grow, the shallow
    layers do; and near the ceiling one can *give back* a little deep
    count to recover shallow count. The record's total 723 is reached
    along a whole ridge of profiles — with depth-4 at its cap of 102, or
    dropped to 96 with depth-1+depth-2 correspondingly higher — the trade
    being about one-for-one. Sacrificing deep count *beyond* that ridge
    loses (the shallow recovery falls short). Depth-1 has been pushed as
    high as 224 in some arrangements, so the shallow ceiling is high; the
    deep caps, not depth-1, are the true limit — but a search over 20,000
    configurations found this trade-off surface *peaks* at 723, evidence
    (not proof) that the record is a genuine optimum of the surface, not
    just a point on it.

  This reframes the whole optimization: the goal is not to maximize any
  single quantity but to find the best point on this trade-off surface —
  which deep layers to sacrifice, and by how much, to unlock the most
  shallow gain. Mapping that surface (the best shallow count reachable at
  each deep-layer profile) is the current line of attack on 723.
- **A parity rule.** For a generic arrangement of *n* cubes, the total is
  always congruent to 2*n*−1 modulo 4. (Reason: each cube is symmetric
  through the centre, so pieces pair up under the point reflection
  x → −x, forcing the count into a fixed residue.) Verified for *n* =
  4…7. Highly symmetric walls occasionally jump to the other allowed
  residue.
- **Richer sub-parts, higher total.** How many regions each individual
  cube (or pair) contributes correlates *positively* with the total
  (correlation ≈ +0.64 for single cubes). The record is both rich and
  balanced — in the 723 configuration every one of the six cubes
  individually contributes exactly 30 depth-1 regions.

---

## 6. The geometry of the maxima: edges versus corners

The maxima are organized by **incidence** — extra coincidences where more
face-planes than usual pass through a single point. In a generic
arrangement, planes meet three at a time at ordinary corners of the
pattern. A *concurrence* is a point where more than three meet. Two kinds
matter, and they are exactly the "edges versus corners" seen back in the
three-cube case:

- **Edge concurrence:** a point where **4 planes** meet, made of **2
  planes from one cube and 2 from another**. Two planes of a cube meet
  along one of its *edges*, so this is an edge of one cube crossing an
  edge of another. Such points sit at distance √2 from the centre (cube
  edge-midpoint distance). This is how the *octahedral* three-cube
  maximum is built.
- **Corner concurrence:** a point where **6 or 9 planes** meet, made of
  **3 + 3** or **3 + 3 + 3**. Three planes of a cube meet at one of its
  *corners*, so this is two (or three) cubes whose corners land on the
  same point, at distance √3 from the centre. This is how the
  *dodecahedral/golden* three-cube maximum is built.

A clean fact ties this to the whole search: "several cubes share a
corner" is exactly the same as "those cubes differ by rotations about the
axis through that corner." So corner-sharing *is* the shared-axis
symmetry — which is why the shared-axis families are where the records
live. The record 723 has two 9-fold corner concurrences (three cubes
meeting at a corner, twice), and is thus *corner-dominated*, though it
also contains about 180 lesser edge concurrences. (There are never any
*line* concurrences — three planes sharing a whole line — because that
would need three parallel-enough normals, which no arrangement realizes.)

**There is a sweet spot, not "more is better."** One might guess that
forcing even more planes through a point helps. It does not: forcing four
cubes to share one corner (a 12-fold concurrence) yields only 393 pieces
— far below the record. Over-concentrating the coincidence merges away
too many regions. The record's 9-fold concurrence is near the optimum.

**A question raised by this picture — now largely answered.** Every
six-cube record is corner-dominated. Could there be a six-cube maximum
built mainly on *edge* concurrences instead? A dedicated search (about
4,600 exact configurations across four strategies, including exact √2
arrangements) says no. The best edge-dominated arrangement reaches only
691 — an edge-*pure* configuration of two octahedral three-cube compounds
— which is 32 short of 723, and the entire gap is in depth-1 (174 versus
210). Moreover, edge-richness *anti-correlates* with the total (rank
correlation ≈ −0.58 across the structured families): the more edge
concurrences you force, the *fewer* pieces you get, and an
edge-maximizing search drives the total down. So corner concurrences are
genuinely the stronger ingredient, and substituting edges for corners
does not reach the record. This is strong evidence, not a proof — an
unsampled region of configuration space, or a wall needing numbers beyond
√2, is not excluded.

**Toward proving the caps.** There is a reformulation that turns the
whole problem into geometry on a sphere. Point in every direction û from
the centre; the cube *k* extends out to distance tₖ(û) = 1 / ‖Rₖᵀ û‖∞ in
that direction. The regions of a given depth correspond exactly to
connected zones on the direction-sphere where a particular set of cubes
are the "innermost." The boundaries of these zones are arcs of great
circles, and counting the zones becomes an exercise in counting cells of
a great-circle arrangement — for which there is an exact
vertex/edge/cell census. That census comes out to fixed numbers
(36, 102, 164 for depths 5, 4, 3) for generic arrangements, matching the
observed caps; making that rigorous, plus showing that special alignments
can only *merge* zones (never create extra ones), would prove the caps.
The first half is established; the second half is the remaining gap.

---

## 7. The dihedral family: a closed-form bridge between the two 67s

Section 6 showed the n=3 maximum (67) is reached in two geometrically
different ways — an *edge-dominated* octahedral compound (√2) and a
*corner-dominated* golden compound (√5). This section describes a
one-parameter family of three-cube compounds, found afterward, that
contains **both** 67s as special points and threads exact face-plane
coincidences through every point in between — answering, in closed form,
what kind of continuous path connects them. It was found by acting on a
concrete observation made while looking at the interactive viewer: the
near-miss edge crossings along the midpoint of an earlier, cruder
attempt at such a slide (Postscript 9 of the ledger) looked like they
were sitting in a plane perpendicular to the direction (1,1,1) — and
that observation turned out to identify the whole family.

**The family.** Take the cube [−1,1]³ and an axis n(ψ) =
(sin ψ, cos ψ, 0) that lies *in* one of the cube's own face planes,
through the centre. Rotating the cube by +120° and by −120° (i.e. +240°)
about n(ψ) gives two more cubes; together with the original (identity)
cube, this is a compound of three cubes, symmetric under 120° rotation
about n(ψ) (a *C₃ orbit*). Every member of the family has an extra
symmetry too: a 180° rotation about the cube's own horizontal face axis
maps the whole compound to itself (dihedral symmetry D₃), which is where
the name comes from. The parameter ψ ranges over [0°, 90°]; two exact
symmetries cut this down further:

- **Mirror symmetry.** Swapping the x- and y-coordinates carries the
  configuration at ψ into the configuration at 90°−ψ with all three
  phases negated — an isometry, so the two have identical region counts
  and depth profiles. (Proof: the coordinate swap P has det = −1 and
  sends n(ψ) to n(90°−ψ); conjugating a rotation by an improper
  orthogonal map reverses its sense, giving exactly the ψ ↔ 90°−ψ,
  phase-negation correspondence.)
- **90° periodicity.** ψ and ψ+90° give the identical compound (not just
  a congruent one) — rotating the *seed frame* by 90° about its own third
  axis is itself a symmetry of the cube. So the family's true, non-
  redundant parameter range is ψ ∈ [0°, 45°].

**The coincidence identity.** For *every* ψ (not just special values) and
every choice of phases, the corresponding edges of any two cubes in the
family — matched up by "same class" (there are three classes, one per
coordinate axis of the seed cube) — are guaranteed to lie in a common
plane, and non-parallel lines in a common plane always meet. So the
family has built-in exact edge concurrences everywhere, not only at
isolated points. (One class is elementary: all three cubes' relevant
edges lie at one of two fixed heights measured along (1,1,1), and any
two edges at the same height share a plane. The other two classes follow
from a short vector computation in the family's natural frame. This is
now a proved theorem, not just a numerical observation — see below.)
What *does* vary with ψ is only whether a given coincidence lands inside
the finite edge segment (making it a real crossing of the compound) or
outside it (making it geometrically real but physically absent) — that
is what produces the plateaus and spikes described next.

**Both 67s are members of this family.**
- The **octahedral** 67 sits at ψ = arcsin(1/√3) ≈ 35.264°, axis
  n ∝ (1, √2, 0). Its pairwise congruence invariant matches 1/2 + √2, as
  expected from the ℚ(√2) witness of Section 6.
- The **golden** 67 sits where tan ψ = φ², φ = (1+√5)/2 the golden ratio
  — equivalently sin ψ = φ/√3, cos ψ = 1/(φ√3), a consistency that boils
  down to the identity φ² + φ⁻² = 3. Its pairwise invariant is 3φ/2.
- A **new exactly-certified compound** sits at ψ = 45° exactly — the
  face-diagonal axis (1,1,0)/√2. Its rotation matrix has entries in the
  field ℚ(√6) (a new "field clone" engine, `q6_count.py`, was built to
  count it, following the same pattern as the project's other ℚ(√d)
  engines). Its exact region count is **49**, depth profile
  {1: 30, 2: 18, 3: 1} — verified on a single engine so far, not yet
  cross-checked by a second independent counter.

**The staircase.** Sweeping ψ across [0°, 90°] with exact ℚ(√3) arithmetic
(rational sin/cos pairs from Pythagorean triples give rotations in
ℚ(√3), which a new engine `q3_count.py` — again a field clone of the
project's validated counting code — can count exactly), the region count
forms a symmetric staircase around ψ = 45°:

| ψ range | count | depth profile |
|---|---|---|
| [0°, ≈9.6°), incl. shared-axis endpoint | 25 | {12, 12, 1} |
| (≈9.6°, ≈10.9°) | 31 | {18, 12, 1} |
| (≈10.9°, 20.905°) | 43 | {24, 18, 1} |
| **35.264° (octahedral)** | **67** | **{48, 18, 1}** |
| (20.905°, 69.095°), central plateau | 55 | {36, 18, 1} |
| **45° (face-diagonal, new)** | **49** | **{30, 18, 1}** |
| **69.095° (golden)** | **67** | **{48, 18, 1}** |
| … mirrored on the other side, 90° (shared axis) | 25 | {12, 12, 1} |

Two things stand out. First, the depth-3 count is always 1 and the
depth-2 count is 18 across the whole central plateau (dropping to 12 only
near the two shared-axis endpoints) — every bit of variation is in the
depth-1 (outermost) layer, an especially clean instance of the
"deep-structure-conserved, shallow layer is what varies" principle of
Section 5. Second, and more surprising: **the face-diagonal point is a
local *minimum*, not a local maximum** — its extra edge coincidences
(6 more than the plateau) happen to *merge* regions rather than *create*
new ones, while the extra coincidences at the octahedral and golden
points (12 more than the plateau) *do* create new ones. This is the
sharpest illustration yet, at n=3, of a theme from Section 6: what
matters is not how many face-planes concur at a point but exactly how
they concur — coincidence-richness cuts both ways.

**Why the earlier slide had ghosts.** The project's original attempt at
a continuous path between the two 67s (Postscript 9 of the ledger) does
connect them, but its interior points are *not* on this family surface —
its seed direction has a small but nonzero component along (1,1,1) where
the family requires exactly zero — so its near-miss crossings never quite
close ("ghosts": a visible near-alignment with a small but nonzero gap).
The dihedral family threads the same two endpoints through a path of
*exact* coincidences the entire way; the ghosts of the old slide are
precisely the cost of stepping off that surface.

**The persistent 18-core.** Restricting to the interval between the two
golden copies, ψ ∈ (20.905°, 69.095°), the *set* of interior edge
crossings — not just their count — is exactly the same 18 pairs of edges
for the whole open interval. The counts of 30 (at octahedral), 24 (at the
face-diagonal point), and 30 (at mirror-octahedral, ψ = 90°−35.264° =
54.736°) are momentary spikes: +12, +6, +12 *extra* coincidences that
exist only exactly at those isolated points and never open a gap in the
core 18. Arriving at either golden endpoint, nothing in the core breaks:
6 of the 18 stay interior (at segment position t = ±1/φ³ along the
edge — another golden-ratio appearance), and the other 12 land exactly on
cube corners, becoming golden's own corner-coincidence structure. So the
entire drag from octahedral to golden — through the face-diagonal point —
can be made while keeping all 18 core concurrences continuously intact;
the previous belief that the slide had two more unnamed transition points
near 21° and 69° was a misreading of where the near-miss "ghost bands"
begin and end, not real changes in the coincidence set. The exact
transition points are only 20.905°, 45°, and 69.095°.

**Chasing more than 18.** Can a path be found that preserves *more* than
the 18-core the whole way from octahedral to golden? A generalization of
the family (n cubes on a common axis, arbitrary phases, one shared tilt
ψ) has a *pair-curve identity*: the four "extra" coincidences of the
octahedral pair all vanish along one single curve in (phase, ψ)-space
through the octahedral point, not only at the octahedral point itself.
Riding this curve with a three-cube chain of phases achieves **26**
simultaneous concurrences over a sub-range of ψ (35.264° up to about
44.5°) — a genuine improvement over 18, but only locally: the curve's
valid segment closes before reaching golden, and a dedicated search for a
way past this wall (tracing all vertex-adjacent relabelings at the point
where the curve exits, and separately tracing golden's own analogous
extra-coincidence curve backwards) found no route that reaches golden
while carrying more than 18 physical concurrence points. The obstruction
has a specific location: both the octahedral-side curve and the
golden-side curve pass close to ψ = 45°, but at phase values roughly 70°
apart, and neither curve's far branch swings around to link them. So
**18 stands as the best confirmed lower bound for an end-to-end path**,
with a described local obstruction — not a proof that 18 is a ceiling.

**Four theorems.** Since this family was found, four of its properties
have been formally proved (not just checked numerically to machine
precision):

1. **Mirror symmetry** (stated above) — proved for every phase tuple and
   every n, not just n=3.
2. **90° periodicity** (stated above) — likewise general.
3. **The coincidence identity** — every same-class edge pair of any two
   family members is exactly coplanar, for every ψ and every phase tuple,
   proved by direct computation in the family's natural frame (one class
   is elementary; a second follows from a short vector identity; the
   third follows from the first two via the periodicity theorem). What
   is *not* yet proved is exactly which ψ-ranges keep a given coincidence
   inside the finite edge segment — that is a concrete, well-posed
   algebra problem (finitely many polynomial sign conditions), not yet
   carried out.
4. **A rational-invariant obstruction.** If every cube in a configuration
   has rational (integer-quaternion) coordinates, a certain pairwise
   congruence invariant is forced to be rational too. Both known 67
   witnesses have irrational invariants (1/2+√2 and 3φ/2), so **no
   rational configuration can be congruent to either** — the two known
   67s are provably not reachable by any rational arrangement. If they
   are also the *only* three-cube maximizers up to congruence (believed,
   supported by their isolation and by every search so far, but not
   proved), this yields a striking corollary: **n=3 is the unique
   irrational level of the whole record tower** — n=2's record (13) is
   rational, and so is every current record at n≥4, while n=3's maximum
   provably cannot be.

**Extending to n cubes, and what it reveals about the records.** The
family generalizes past n=3: n cubes with independent phases about the
same axis and the same shared tilt ψ, with the pairwise relative
rotation between any two members depending only on their phase
difference and ψ (a closed Rodrigues-rotation form). At Pythagorean ψ
this makes every member an **integer-quaternion** configuration,
countable directly by the project's fast C++ engine — turning the
family, for the first time, into something the record-search machinery
can search exhaustively and exactly. Two results:

- **As a search space by itself, the family loses ground as n grows.**
  The best purely-single-axis family members found (an exact sweep of
  over 9,000 configurations at n=4,5,6) reach only 175, 335, 615 —
  falling short of the true records 183, 393, 723 by 8, 58, and 108
  respectively, a deficit that *widens* with n. (This measures the
  family's Pythagorean-sampled plateau, a lower bound on the true
  family's supremum — the family's own irrational spikes, like the two
  67s at n=3, are invisible to a rational sweep and could in principle
  raise these numbers, an open question.)
- **But every current record is built almost entirely out of family
  pairs.** Checking every pair of cubes in each record against the
  family's own membership test: **all 6 pairs** of the 183 record, **all
  10 pairs** of the 393 record, and **12 of the 15 pairs** of the 723
  record are in family position (some shared axis and tilt — not
  necessarily the same axis for every pair). The 723 record's structure
  resolves exactly: five of its cubes form a complete family clique (this
  is exactly the embedded 393 record, consistent with the nesting
  property of Section 9), and the sixth cube is family-linked to two of
  the five and generic against the rest. So the records are **gluings of
  family cliques living on different axes**, not members of one common-
  axis family — which is exactly why a single-axis sweep falls behind:
  it searches a strict subset of the structure the records actually use.
  This reframes the record search itself: instead of a raw search over
  all rotations, it becomes a search over how many family cliques to use,
  on which axes, and how to glue them — a search that is still open and
  ongoing.
- The deep layers of the best family members match the corresponding
  record's deep layers *exactly* at every n tested (e.g. the n=4 family
  best has the same depth-3 and depth-4 counts as the 183 record, with
  its entire 8-point deficit sitting in the depth-2 layer alone) — the
  clearest demonstration yet that a good building block is deep-saturated
  and only ever detunes the shallow layers (Section 3's frustration
  principle, now traced through an entire new family at every size).

Files: `q3_count.py`, `q6_count.py` (the two new field-clone engines),
`nfamily_common.py`/`nfamily_sweep.py`/`nfamily_q3_records.py` (the
n-cube generalization and record-pair analysis), and
`dihedral_scratch/` (exploration and verification scripts). The formal
proofs are in `C45_notes.md`, section 12; the numerical exploration is
`six_cube_search_results.md`, Postscripts 25 and 26.

---

## 8. Solving for the alignments algebraically

The searches above *approach* the special walls numerically. A more
direct approach *solves* for them. Because a rotation about a fixed axis
can be written with a single rational parameter (keeping all coordinates
as exact fractions), the condition "this face passes exactly through that
point" becomes a polynomial equation, and the exact solutions can be
found with computer algebra (Gröbner bases and equation solving):

- **One-parameter sweep.** Sliding one symmetric group of cubes along its
  shared axis and solving where a new coincidence forms yields the finite
  list of exact "special angles" (126 of them along one such slide) — the
  exact walls, found without any grid. Counting them confirmed 723 is a
  genuine local maximum along that slide.
- **Multi-constraint solve.** Requiring a new cube to lock onto two
  existing cubes' corners at once is a small system of polynomial
  equations; solving it exactly produces configurations a numerical grid
  would never land on. This found a family reaching 689 with a
  record-high depth-1 of 224 (but a lower total, because the deep layers
  fell) — quantifying the same shallow-versus-deep trade-off, and
  confirming the deep caps as the true bottleneck.

Neither has beaten 723, but together they map the relationship between
coincidence structure and piece-count exactly, and can reach exact
algebraic (even irrational) configurations that trial-and-error cannot.

**From search to branch-and-prune.** The structural findings collapse the
search space into something almost combinatorial. Since a configuration's
worth is carried by its *blueprint* — how the cubes partition into
shared-axis clusters, which pairs are rigid best-pairs versus tunable
9-pairs, which cubes are free — the search becomes: enumerate the finite
catalog of blueprints, *prune* the ones that provably can't win (a
triangle of rigid best-pairs forces the golden wall, whose extensions are
known to lose; geometrically inconsistent labelings never existed), and
optimize the surviving blueprints over their continuous knobs. The prize
is a qualitatively stronger conclusion than any search so far: "no
blueprint beats 723," exhaustive at the skeleton level, rather than "we
didn't find one." This search has now run to completion: 391 raw blueprints collapse
to 67 canonical skeletons (plus two pruned with documented reasons —
the golden wall, whose extensions provably lose, and the
polyhedral-forcing family, tested and dominated); all 67 were
knob-optimized (over 83,000 exact counts) and none beats 723. What would upgrade it from
branch-and-*prune* to true branch-and-*bound* is one missing theorem — a
**deficit-propagation lemma**: a guarantee that if a partial assembly's
sub-compounds fall short of their deep caps by some amount, the completed
arrangement's total is capped below the global bound by a corresponding
amount. The empirical envelope for that lemma has now been measured
(every five-cube sub-compound of 532 arrangements spanning the whole
spectrum, counted exactly), and it is sharp on both fronts: adding a
sixth cube never gained more than 336 over the best five-cube part — so
any arrangement beating 723 must *contain* a five-cube arrangement of
at least 388, a class that only the record's own family is known to
occupy — and any arrangement whose parts miss their deep caps is capped
more than 150 below the record. Both statements are measured envelopes
awaiting proof, but together they nearly corner 723: the search for a
better six-cube arrangement reduces to the search for a new
near-record five-cube one.

---

## 9. More than six cubes, and the record tower

The counting method works for any *n*. Best arrangements found so far
(lower bounds on the true maxima):

| cubes *n* | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|
| best bounded pieces | 13 | 67 | 183+ | 393+ | 723 | 1207+ | 1879+ |

Several of these numbers are *corrections*: the golden compound gives 177
at four cubes and 351 at five, and both were long taken as the answers —
but a rational four-cube arrangement reaches 183 and a rational five-cube
one reaches 393. Golden is the best *symmetric* configuration, not the
maximum. This raised the question of whether even the small cases are
safe; thorough search in their low-dimensional spaces **confirms 13 and
67** (nothing beats them), and confidence rightly runs opposite to size:
near-certain at n=2, strong at n=3, down to "best found so far" at n=6,7.

**The records form a tower, and it is generative.** The best six-cube
arrangement *contains* the best four-cube one and a five-cube sub-compound
(393) that beats the old five-cube record; adjacent sizes differ by adding
or removing one cube. This is not just descriptive — it *builds* records:
taking the 723 six-cube record and adding a single seventh cube, over a
few hundred orientations and with no fine-tuning, already reaches **1207**
at seven cubes, beating a 50,000-arrangement random campaign (which topped
out at 1085). So the recipe "take the best (*n*−1)-cube arrangement and
add one cube well" outperforms searching from scratch.

**The tower is organized by a shared 3-fold symmetry.** Each
golden-beating record keeps exactly a single 3-fold rotation axis (a
symmetry group of order 3) — dropping all the way down from golden's
order-60 icosahedral symmetry, but never becoming fully asymmetric. That
surviving axis is the corner-sharing structure of Section 6, and it
organizes the tower: the cubes split into one 3-fold orbit plus a few
axis-fixed cubes, the orbit cubes are interchangeable (removing any gives
the same result), and it is the *axis-fixed* cubes that are added and
removed to climb between sizes. The parity rule, the 6n second-deepest
cap, and the shallow-gain / deep-cap structure all persist as *n* grows.

**The 3-fold orbit is a dihedral-family clique.** Section 7 sharpens this
picture: the surviving 3-fold orbit at every size is exactly a clique of
the dihedral family (Section 7), and the axis-fixed cubes attach to it in
family position too, wherever tested — the records are gluings of family
cliques on different axes, not one common-axis structure. That reframing
is what suggests the two-clique gluing search of the open problems below.

---

## 10. Open problems

1. **Prove the second-deepest cap, depth-(n−1) ≤ 6n.** This is the most
   tractable ceiling — it unifies depth-5 ≤ 36 (n=6) with the small cases,
   and reduces (Section 5) to one lemma: the direction-sphere function
   "distance to the nearest face" has local minima *only* at the 6n
   face-centre directions — no extra "shoulder" minima. The two-normal
   case of that lemma is provable; the open crux is whether three cube
   face-normals can ever conspire to make an extra minimum. Zero such
   cases in any sampled arrangement, but the general proof is a genuine
   research problem. (The deeper caps depth-3 ≤ 164 and depth-4 ≤ 102 at
   n=6 are separate, harder counting statements.)
2. **Beat 723 for six cubes, or prove it is the maximum.** In the
   trade-off language of Section 5, this means finding the best point on
   the deep-sacrifice surface: since the deep layers are capped and the
   shallow layers are not, the question is exactly *how much* deep count
   to give back to unlock the most shallow count. 723 sacrifices depth-4
   alone; whether sacrificing depth-3 and depth-4 together (or another
   combination) nets higher is open and is the active line of attack.
   Depth-1 can already reach 224, so there is shallow headroom.

3. **Can non-concentric or unequal-sized cubes do better?** Everything
   above keeps the cubes centred at a common point and equal in size.
   Both restrictions can be relaxed, and each only *adds* freedom, so
   neither maximum can be below the concentric-equal one — the question
   is whether either is strictly larger. Two experiments (with a counter
   built for the purpose, validated to reproduce the concentric-equal
   counts exactly): **off-centring the record strictly hurts** — every
   translation lowers the total (best 706, then monotonically worse), so
   concentric is at least a local optimum. **Unequal sizes are so far
   untested at the record**, because 723 is so symmetric that resizing
   any cube by a rational factor creates an exact face-coincidence the
   (non-robust) counter cannot evaluate; settling it needs a
   degeneracy-tolerant counter. Note that resizing *preserves* the
   central symmetry that off-centring destroys, so it is the gentler
   perturbation and the more plausible of the two to help — but there is
   no proof either way.
4. **Settle the edge-versus-corner question:** can an edge-dominated
   arrangement ever match a corner-dominated one at the maximum? Current
   evidence says no — edge-dominated arrangements top out at 691 and
   edge-richness anti-correlates with the total — but this is evidence
   from a finite search, not a proof. A related, sharper question raised
   by Section 7: can any path in the dihedral family carry more than 18
   physical edge concurrences continuously from the octahedral 67 to the
   golden 67? A dedicated search found a specific local obstruction (two
   different "extra-coincidence" curves that both graze ψ=45° but stay
   about 70° apart in phase) and no rescue past it — 18 is a confirmed
   lower bound with a described obstruction, not a proven ceiling.
5. **Special number-field walls:** whether any arrangement needing √2, √3,
   or a combination beats the best plain-fraction arrangement. (The golden
   √5 wall reaches 681; the overall record 723 is a plain-fraction
   arrangement.) Section 7 adds one more exactly-certified data point in
   this vein — the ℚ(√6) face-diagonal compound at 49 — well short of the
   record and, notably, a local *minimum* of its own family rather than a
   maximum.
6. **Growth with *n*** and the persistence of the structural laws at
   scale.
7. **The two-clique gluing search (in progress).** Section 7 showed every
   current record is a gluing of dihedral-family cliques living on
   different shared axes, rather than a single-axis family member. This
   reframes the record search as choosing how many cliques to use, on
   which axes, at what tilts and phases, and how to glue them — a search
   with a much smaller effective dimension than raw SO(3)ⁿ, but not yet
   carried out systematically. Whether it can find something beating 723
   (or reproduce it from first principles, strengthening the branch-and-
   bound case of Section 8) is open.
8. **The n=4 resonance, algebraically (in progress).** The two n=3
   maximizers sit at algebraically special, irrational points of the
   dihedral family (the octahedral and golden 67s). Whether the n=4
   record's family embedding (Section 7: all 6 pairs of the 183 record
   are in family position) similarly has an irrational "resonance" point
   that beats the rational family plateau of 175 is an open algebraic
   solve — the natural next target for the same symbolic-algebra approach
   (Section 8) that located the n=3 spikes, now pointed at the family's
   n=4 generalization instead of a blind search.

---

## 11. The code, briefly

The exact counter (`cube_regions`, C++), its slower cross-check
(`certify_six.py`), the search drivers, the symmetry catalogue, and the
algebraic-search scripts (which drive the computer-algebra system
`wolframscript`) all live in this directory; a companion `README.md` maps
each file and gives runnable commands, and `six_cube_search_results.md`
is the dated primary record of every result. Two further exact engines
support Section 7's dihedral family: `q3_count.py` (field ℚ(√3), for
Pythagorean-angle family members) and `q6_count.py` (field ℚ(√6), for the
face-diagonal point), both built as field-constant clones of the
project's earlier validated ℚ(√2) counter. A single configuration can
be counted directly, for example:

```
cube_regions --quats '4,1,1,-1;3,3,7,3;5,-1,-5,-5;2,1,1,1;1,1,1,1;5,2,2,2'
   →  723 bounded regions
```

Every record quoted here has been re-verified by an independent counter.

**Interactive depth explorer.** A browser-based tool renders any
configuration (paste six quaternions; prefilled with the record) two
ways: a draggable cross-section whose every pixel is coloured by depth —
sweep the cutting plane through the compound and watch the shallow shell
and white-hot core appear — and a rotatable 3D point cloud of the same
depth structure. Depth and per-cube filters isolate any layer or any
cube's contribution to cut clutter; a toggle recolours cells by *which*
cubes contain them (containment label) rather than how many.

Since the last update the viewer gained several features, all under the
same published URL:

- **Opaque mode.** A toggle renders the compound's faces as solid,
  shaded, depth- or containment-coloured polygons (each cube face split
  by every other selected cube's face-planes into its true convex
  pieces, painter's-algorithm sorted) instead of a point cloud —
  concretely showing the region boundaries as surfaces, not dust.
- **The dihedral-family slider**, which replaces the old, ghost-gapped
  "67 ↔ 67 slide" of Postscript 9 with a slider along the family of
  Section 7: a ψ readout and drag control from 0° to 90°, named tick
  marks (including the newly-added mirror-golden point), a live ghost
  (near-miss) counter, and a "maintain concurrences" lock that clamps
  dragging to stay within a range where the crossing set — the
  core-18, specifically — is certified constant.
- **Split/merge surface highlighting**, which outlines exactly the
  opaque faces involved in whatever near-miss coincidences ("ghosts")
  exist at the current slider position — a live, ψ-dependent view of
  which surfaces are about to split apart or merge together.
- **Zoom** (mouse-wheel, threaded through the same scale factor as every
  other overlay) and **one-sided clipping** of the opaque surface against
  the cross-section plane, so the solid interior can be inspected without
  the near side occluding it.

> https://claude.ai/code/artifact/044d34a6-3f36-43b2-9ec8-17fb5691c87c

(The link opens for anyone once the artifact is shared publicly from its
claude.ai page; until then it is visible only to its owner.)
