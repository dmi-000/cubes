# The levels — what is known at each n, and how the levels connect

One section per number of cubes, stating **what is currently believed**, with the ledger entry
each claim rests on today. No history: how each fact was reached, and the claims that were
withdrawn on the way, are in [`LEDGER.md`](LEDGER.md) and [`JOURNEY.md`](JOURNEY.md). Exact
representatives with the commands that reproduce them are in [`MAXIMISERS.md`](MAXIMISERS.md).

*Written 2026-09-24. Every bracketed citation is tracked by `python3 src/claim_deps.py`: if a
postscript cited here later falls, the audit lists this file as a dependent.*

**The count.** For `n` unit cubes sharing a centre, the number of bounded regions their face
planes cut out, where a face plane only splits a region inside its own cube. `max(n)` is the
largest count over all rotations. Every count here is exact.

## At a glance

| n | best count | status | plateau (the set where the best count holds) | classes known |
|---|---|---|---|---|
| 1 | 1 | trivial | everything | 1 |
| 2 | **13** | **proved** | **1-dimensional**: a single arc in class space | 1 |
| 3 | **67** | **proved** | **isolated points** | 2 |
| 4 | 183 | unproved; `<= 195` unconditionally in draft ([P422](LEDGER.md#p422), unreviewed), `<= 261` on reviewed steps alone ([P401](LEDGER.md#p401)) | **1-dimensional**: an arc, in both classes | 2 |
| 5 | 393 | unproved; `<= 485` with at most one sharing pair, and `<= 457` when `d4 >= 2c4` (no sharing) or `c4′ <= 10` (one pair), in draft ([P430](LEDGER.md#p430), [P435](LEDGER.md#p435), unreviewed); `<= 871` for every compound ([P401](LEDGER.md#p401)) | tangent dimension 1; **plateau not measured** | 1 |
| 6 | 727 | unproved | **1-dimensional**: two branches crossing at the record, plus a separate arc | 1 structural class |
| 7 | 1217 | unproved | **2-dimensional**: two sheets crossing over the record | 1 |
| 8 | 1895 | unproved | **3-dimensional**: a 38-vertex polytope | 1 |
| 9 | 2787 | unproved | tangent dimension 4; one direction walked | 1 |
| 10 | 3925 | unproved | lineality 6; plateau not walked | 1 |
<!-- reviewed 2026-09-28: the n = 4 row states 198 as conditional; proved labels n = 2, 3 -->

**The pattern worth seeing first.** Apart from n = 3, the maxima and records are not isolated
points. Each
sits on a region where the count stays constant, and above n = 6 that region gains one dimension
per added cube. Wherever both have been measured (n = 4, 6, 7, 8), the plateau's dimension equals
the first-order tangent dimension ([P381](LEDGER.md#p381), [P383](LEDGER.md#p383)): every
direction that preserves the count to first order extends to an actual family.

## n = 2 — 13, proved

`max(2) = 13` for any two convex cells with at most 6 faces each ([`max2_report.md`](max2_report.md)).
**n = 2 is the one level mapped completely** ([P69](LEDGER.md#p69), [P70](LEDGER.md#p70),
[P390](LEDGER.md#p390)). Only five counts occur: 1, 4, 5, 9 and 13. The generic count is **4**
(98.8 % of rotations at height 1000); the rest live on lower-dimensional sets.
<!-- reviewed 2026-09-27: cites P70 for the complete count map, which stands; P390 states what changed -->

**In class space, 13 holds on a single arc.** A pair's class is its relative rotation up to each
cube's own 24 symmetries, so a rotation axis is not an invariant, and the arc shows up in the
axis-angle chart in many places: on body diagonals, on edge axes, on mirror planes ([P76](LEDGER.md#p76)),
and at special angles off every mirror plane. All of them are the same arc ([P390](LEDGER.md#p390)):

- it starts OPEN at the identity, where the cubes coincide and the count is 1;
- runs along rotations about a body diagonal up to **60°** ([P83](LEDGER.md#p83), [P86](LEDGER.md#p86));
- which is the same compound as the end of the edge family, and continues along rotations about an
  edge axis;
- to a CLOSED end at the **90° rotation about an edge axis**, which is irrational.

Nothing is isolated and there is no second component: every one of the 1 312 rational 13s with
components up to 5, on every axis, lies on this arc. The two n = 3 maxima are built from its
points. The octahedral 67's three pairs are its closed end, and the golden 67's three pairs sit at
44.48° on the body-diagonal part, `cos θ = (3√5 − 1)/8`.

The figure is [`viewers/n2map_standalone.html`](viewers/n2map_standalone.html). It draws the
axis-angle chart, where the one arc appears as many curves ([`VIEWERS.md`](VIEWERS.md) §1).

## n = 3 — 67, proved

`max(3) = 67` for three concentric convex cells meeting pairwise transversally
([`PROOF_67.md`](PROOF_67.md), [`PROOF_STEP_T.md`](PROOF_STEP_T.md)). The remaining caveat is
tangential contact, a higher-codimension degeneracy.

**Two classes, both irrational, not congruent:**
- **octahedral 67**, in ℚ(√2), a C₃ orbit;
- **golden 67**, in ℚ(√5): three of the five cubes of UC09, the compound of five cubes inscribed in
  a dodecahedron.

**Both are isolated** ([P118](LEDGER.md#p118), whose isolation verdict is unaffected by the
face-count detail later corrected in it), and n = 3 is the only level where this is true
of the maximum. The reason is specific ([P382](LEDGER.md#p382)). As at n = 4, each 67 lies on a
genuine curve along which all its contacts persist, but the count changes the moment it leaves
the point, on both sides: the stretch of that curve still counting 67 has zero length. Rigid
demands produce a spike; the trades the higher records make produce a plateau.

## n = 4 — 183, unproved

**Two classes, each lying on its own arc** ([P378](LEDGER.md#p378), [P380](LEDGER.md#p380)):
- **the tower's 183**: cubes {0, 1, 2, 4} of the 393 base below. This is the 183 that the higher
  records contain as a 4-subset. Its arc has length 0.6873, and the count is 183 along all of it.
- **the C₃-symmetric 183**, the representative in [`MAXIMISERS.md`](MAXIMISERS.md).

The two arcs are distinct: the distance between the classes exceeds the length of the arc, and
distance changes at most as fast as arc length ([P380](LEDGER.md#p380)).

**What bounds it, and how firmly.**

| claim | status |
|---|---|
| `max(4) <= 953` | **strong conjecture, with a gap in its proof**: the per-depth bounds summed ([P249](LEDGER.md#p249)), but the bound for depths >= 2 ([P243](LEDGER.md#p243)) omits two-body vertices that do occur there ([P274](LEDGER.md#p274)); true by a factor of about five wherever measured, and the repair looks mechanical but has not been made |
| if every level has `c_ell <= 2`, then `max(4) <= 198` | **proved** as a conditional ([P258](LEDGER.md#p258), [P326](LEDGER.md#p326)) |
| `c_ell <= 2` on every level | **strong conjecture**: never violated in about 3 700 level-instances, including directed attempts to break it, and reduced to one connectivity claim ([P259](LEDGER.md#p259), [`OPEN_QUESTIONS.md`](OPEN_QUESTIONS.md) §30); not proved |
| `max(4) <= 195` | **draft** for compounds with no shared face plane, 2026-10-04 (labelled proved until 2026-10-08, corrected because it is unreviewed; [P410](LEDGER.md#p410), [`PROOF_BAND.md`](PROOF_BAND.md); not yet externally reviewed). It does not need `c_ell = 1`: each extra component of the level-2 boundary is paid for by an extra component of a triple's bottom diagram. CORRECTED from "hope" |
<!-- reviewed 2026-09-24: the 953 row states its proof gap -->

The first bound that needs no hypothesis is **`max(4) <= 261`** ([P399](LEDGER.md#p399), [P401](LEDGER.md#p401), 2026-09-30), by Mayer–Vietoris at every depth; it proves `d1 <= 104` and `d3 <= 24`, so `max(4) <= 195` would follow from `d2 <= 66` alone. Here `c_ell` is the number of connected pieces of the curve arrangement at depth `ell`. An older
figure, 263 ([P261](LEDGER.md#p261)), rests on the same `c_ell = 1` and is dominated by 198 (scope
note in the ledger).

**Why `max(4) = 183` is unproved.** Three reductions to a few named statements have failed. The
third, resting on "T <= 48" (the two-body weight on the outer surface), fell to the golden 177
itself, which has `T = 60` ([P389](LEDGER.md#p389)). The other two attempts to reduce `max(4) = 183` to a single inequality were
both refuted by one compound, `1,0,0,0; 0,2,-3,-2; 0,2,-3,2; -4,-2,-5,-6`, which counts only 173 but
breaks both proposed ceilings ([P373](LEDGER.md#p373)). What holds is the per-pair and per-triple
box, `E_i <= 10` ([P237](LEDGER.md#p237)) and `E_S <= 32` ([`PROOF_67.md`](PROOF_67.md)).
From it, `TOTAL <= 195 - Q4` follows **only if the holes are trivial**, `c = 1` on every level
([P348](LEDGER.md#p348)): unproved, and `c = 2` occurs. CORRECTED 2026-09-28
([P395](LEDGER.md#p395)); this said the condition was the absence of `(1,1,2)`-type vertices, which
is the scope of a different formula ([P374](LEDGER.md#p374)). What bounds the edge-edge crossings at a full triple budget is open.

**The instructive loser.** The golden 177 is UC09's 4-subset. Every subset of it is at its
proved maximum (13 and 67), and it still loses to 183. It is the only compound in which all four
cubes pairwise share a corner, and it attains the two-body cap of 60 with the triple budget full,
yet pays for it with 18 four-fold points ([P370](LEDGER.md#p370)). **Subset-optimality does not give
the maximum.**

**What the records do instead** ([P364](LEDGER.md#p364)): one hub cube sharing an axis with up to
four others, and every other cube sharing at most one axis. A cube with a single shared axis
keeps a free rotation, which lets it dodge a forced coincidence; fully pinned cubes cannot
([P358](LEDGER.md#p358)).

## n = 5 — 393

The **393 base**, `4,1,1,-1; 3,3,7,3; 5,-1,-5,-5; 2,1,1,1; 1,1,1,1`, C₃-symmetric. It beats UC09
itself (351), which is where the belief that UC09's subsets are optimal first fails by a whole
level ([P16](LEDGER.md#p16)). Every record from n = 6 to n = 8 is this base plus added cubes.

Its tangent dimension is 1 ([P381](LEDGER.md#p381)). **Whether 393 lies on a 1-dimensional plateau,
like 183 and 727 on either side of it, has not been measured.** The old second-order verdict that
it is isolated came from a method that was wrong at n = 4, 6, 7 and 8 ([P117](LEDGER.md#p117)'s
note), so it is not evidence either way.

## n = 6 — 727

The 393 base plus `7,14,1,-5`. **The plateau is one-dimensional** ([P306](LEDGER.md#p306);
dimension from [P307](LEDGER.md#p307), whose n = 6 and n = 7 values stand while its n = 8 value was
corrected by [P383](LEDGER.md#p383)). **The record is a node where exactly two branches cross**, D1 and
D2, at a shallow 4.51°; each holds 727 alone and no combination does ([P94](LEDGER.md#p94),
[P102](LEDGER.md#p102)). The catalogued arcs B and C are those same two branches seen at the
record's other two spellings, through the 393 base's C₃ symmetry, and arc A is a separate piece
that meets no spelling of the record ([P391](LEDGER.md#p391)). Both branches are solved end to end:
D1 spans 7.04° of rotation and D2 8.43°, and B's and C's extents coincide with them exactly ([P392](LEDGER.md#p392)). All the arcs are one structural
class, and the record is a special POINT on them, not a special arc ([P293](LEDGER.md#p293)). Solving each arc's wall conditions finds nine special points, which are
six distinct compounds up to congruence ([P294](LEDGER.md#p294)). The arcs contain members in
every quadratic field tested as well as rational ones.

The **typology of this plateau**, meaning which structural routes reach 727, their depth profiles,
and the fingerprint that separates them, is worked out in [`TYPOLOGY.md`](TYPOLOGY.md). **This is
the only level whose plateau has been classified.**

The earlier record, 723, is the base plus `5,2,2,2`, and is also positive-dimensional: it holds on
a union of intervals along the shared C₃ axis.

## n = 7 — 1217

The 727 six plus `4,-3,-4,-4`. **A 2-dimensional plateau made of two sheets that CROSS along a
line over the record** ([P393](LEDGER.md#p393), [P394](LEDGER.md#p394); the dimension from [P307](LEDGER.md#p307), whose
n = 7 value stands, and whose n = 8 value was corrected). It is the n = 6 node carried up a level:
each sheet is spanned by moving the seventh cube within its fibre and moving the sixth along one of
the two branches.
- **Each sheet is a curved triangle** ([P394](LEDGER.md#p394)), bounded by three walls: its
  branch's lower 727 wall, a flat fibre wall at u = 0.00255 (the same on both), and one curved wall
  of degree 4 along the whole lower-right side, first found on the D1 sheet
  ([P299](LEDGER.md#p299), [P301](LEDGER.md#p301)). At u = 0 the D1 sheet runs from −2/19 to about
  0.0497, and the D2 sheet from −0.1358 to about 0.0702. Both contain the fibre segment over the
  record, u from −0.0453 to +0.00255, and extend to both sides of it, which is why they cross there.
- The pentagon [P301] described was that sheet cut off by the edges of a sampling grid, two of
  which it drew as walls. Two zero-width seams of lower count cross the sheets, u = −1/36 on both
  and t = −3/31 on D2 (the n = 6 723 puncture, lifted).

Only segments of the two branches extend with this seventh cube; arc A does not extend with it, and
the rest of D1 and D2 has not been tried with any other seventh cube.

## n = 8 — 1895

The 1217 seven plus `24,-24,24,-61`. **A 3-dimensional plateau**, and all three tangent directions
extend to actual families ([P383](LEDGER.md#p383)). Delimited exactly, it is a polytope with
**38 vertices and 72 facets**, inradius 0.0595 and circumradius 0.859, so it is long and thin
(aspect ratio 14.5). Its boundary is set by contacts between two cube pairs: four from the pair
(0, 5), then six from the pair (3, 7) ([P385](LEDGER.md#p385)).

## n = 9 — 2787

The 1217 seven plus **two** new cubes, `168,-168,168,-415` and `109,-11,91,140`
([P198](LEDGER.md#p198), [P218](LEDGER.md#p218)). It does not contain the 1895 eight: the eighth
cube is replaced. Its tangent dimension is 4, and the free directions sit in the same five
coordinates for both known representatives: one rotational component of the seventh cube, one of
the eighth, and all three of the ninth ([`CONTINUUM_MAP.md`](CONTINUUM_MAP.md), Map 4). One direction has been walked; that
all four extend to a family, as at n = 8, is expected but not checked.

## n = 10 — 3925

2787's nine plus `6555,6555,6497,6555` ([P200](LEDGER.md#p200)). Its 480 tight conditions give
lineality 6 ([P300](LEDGER.md#p300)), which continues 1, 1, 2, 3, 4 upward; the plateau itself has not been walked. **This works only from 2787's
ORIGINAL representative.** The simplified n = 9 representative has the same count and the same
depth profile at every depth, yet the same added cube gives 3921 on it
([P285](LEDGER.md#p285)). Two members of one plateau are not interchangeable as foundations.

## How the levels connect

**Downward: records nest.** The 393 base's four-cube subset {0, 1, 2, 4} is the tower's 183, and
the base is the five-cube subset of 727, 1217 and 1895 ([P16](LEDGER.md#p16)). Removing a cube from a
record tends to leave a strong compound of the level below, though not always the best one.

**Upward: records extend, with one break.** 393 → 727 → 1217 → 1895 each adds one cube and keeps
every cube before it. At n = 9 the tower keeps only the 1217 seven and replaces the eighth cube,
yet 2787's best 8-subset still counts 1895 ([P198](LEDGER.md#p198)): the new cube lies on the same
Cayley line as the old eighth, plausibly another member of the 1895 plateau.
At n = 10 the extension depends on which member of the 2787 plateau it starts from.

**The subset-to-whole inequality** (Theorem S, [`PROOF_SUBSET.md`](PROOF_SUBSET.md)) bounds a
level's deepest regions by the next-to-deepest regions of its subsets:
`sum over (n-1)-subsets T of d_(n-2)(T) <= 6n(n-2) + d_(n-1)(S)`, proved for all n.

**UC09 is optimal at n = 2 and n = 3 and loses from n = 4.** Its subsets count 13, 67, 177, 351.
The first two are the proved maxima; 177 < 183 and 351 < 393.

**Plateau boundaries partly carry up the tower** ([P303](LEDGER.md#p303)). Of the three walls
bounding the D1 sheet of the 1217 plateau, two reappear unchanged at n = 8 and n = 9 and cost exactly 4 regions
to cross at every level. The third is cut by a new wall from the added cubes, contracts about five
times, and is a different wall at n = 8 than at n = 9.

**Dimension grows.** Plateau dimension by level: n = 2: 1; n = 3: 0; n = 4: 1; n = 5: not measured; n = 6: 1;
n = 7: 2; n = 8: 3; n = 9: tangent 4 on the simplified representative, 5 on the original
([P290](LEDGER.md#p290)); n = 10, built on the original: lineality 6 ([P300](LEDGER.md#p300)).
From n = 6 on, each added cube contributes one new free direction, as far as it has been
measured; beyond n = 8 only the first-order count is known.

## What is open

- **`max(n)` for every n >= 4.** The records are lower bounds found by construction and search.
- **What bounds edge-edge crossings** at a full triple budget at n = 4; this is where both
  single-inequality reductions failed.
- **393's plateau**: 1-dimensional, like its neighbours, or isolated, like n = 3?
- **The typology of every plateau except 727's.** The 1217 plateau's two sheets, the 1895 polytope and the
  2787 region are shaped, but not classified into structural routes.
- **n = 9's other three directions**, and whether they extend.
- **Why the ninth cube is free in all three of its components** when the seventh and eighth are
  free in one each.

## Where the detail lives

- [`MAXIMISERS.md`](MAXIMISERS.md) — exact representatives and commands.
- [`CONTINUUM_MAP.md`](CONTINUUM_MAP.md) — the plateaus mapped in detail, and how they extend.
  Its "Map 0" still describes 183 as isolated; that is superseded by the n = 4 section above.
- [`TYPOLOGY.md`](TYPOLOGY.md) — the 727 plateau's classification.
- [`MAXIMISER_TAXONOMY.md`](MAXIMISER_TAXONOMY.md) — the older per-level working record. It predates
  the continuum results; where it disagrees with this file, this file is current.
- [`TOWER_DIAGRAM.html`](TOWER_DIAGRAM.html) — the tower drawn as a figure. It still shows 183 as
  isolated and needs redrawing to match the table at the top.
