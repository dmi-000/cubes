# How many regions do overlapping cubes make? — a self-contained write-up

*Last updated 2026-07-12. This document is standalone: every term is
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
using numbers of the form a + b√5.

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
4. **Algebraic search** (Section 7): solve for the exact alignments
   directly with symbolic algebra instead of approaching them by trial.

---

## 5. Patterns that hold across every arrangement

Several exact regularities appear everywhere we look:

- **Deep layers are capped.** The depth-3, depth-4, depth-5 counts never
  exceed 164, 102, 36 respectively, in any arrangement tried, on any
  wall. (Depth-6 is always 1, which is provable — the innermost region is
  one convex blob.) These three caps are conjectures, with a proof
  program sketched in Section 6.
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

## 7. Solving for the alignments algebraically

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

---

## 8. More than six cubes

The counting method works for any *n*. Best arrangements found so far
(lower bounds on the true maxima):

| cubes *n* | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|
| best bounded pieces | 13 | 67 | 177+ | 351 | 723 | 1085+ |

(The "+" cases are still being searched.) The parity rule and the
shallow-gain / deep-cap structure persist as *n* grows; charting how the
maximum grows with *n* is an ongoing thread.

---

## 9. Open problems

1. **Prove the deep-layer caps** (depth-3 ≤ 164, depth-4 ≤ 102, depth-5 ≤
   36) via the sphere reformulation of Section 6.
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
   from a finite search, not a proof.
5. **Special number-field walls:** whether any arrangement needing √2, √3,
   or a combination beats the best plain-fraction arrangement. (The golden
   √5 wall reaches 681; the overall record 723 is a plain-fraction
   arrangement.)
6. **Growth with *n*** and the persistence of the structural laws at
   scale.

---

## 10. The code, briefly

The exact counter (`cube_regions`, C++), its slower cross-check
(`certify_six.py`), the search drivers, the symmetry catalogue, and the
algebraic-search scripts (which drive the computer-algebra system
`wolframscript`) all live in this directory; a companion `README.md` maps
each file and gives runnable commands, and `six_cube_search_results.md`
is the dated primary record of every result. A single configuration can
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

> https://claude.ai/code/artifact/044d34a6-3f36-43b2-9ec8-17fb5691c87c

(The link opens for anyone once the artifact is shared publicly from its
claude.ai page; until then it is visible only to its owner.)
