# Maximiser taxonomy — results

What is known about each maximiser, how to generate members of each category,
why each cell reads what it does, and what would fill the gaps. **No chronology
here** — the running record is [`LEDGER.md`](LEDGER.md); exact canonical
representatives are [`MAXIMISERS.md`](MAXIMISERS.md).

Terminology follows [`GLOSSARY.md`](GLOSSARY.md) §8.0 — no bare "point", "line",
"plane" or "isolated"; "dimension" always names its space.

---

## 1. The axes

1. **Moduli dimension** — dimension of the maximiser set in the space of
   CONGRUENCE CLASSES. 0 means finitely many maximisers, ≥1 a continuum. The
   gauge dimension is always 3 (rotating the whole compound) and is never quoted.
2. **Components** — connected pieces of the class set. Finite, by
   semialgebraicity. The well-posed replacement for "how many maximisers".
3. **Types** — a type is a chamber: the 64-entry per-label profile is constant
   on it, while the count is constant across a whole component.
4. **Symmetry** — order of the maximiser's own rotation group; equivalently its
   stabiliser, which divides the volume of its congruence class.
5. **Arithmetic** — rational or not, and whether that is structural.
6. **Boundary behaviour** — what the count drops to at the edges.
7. **Findability** — basin size under climbing; a property of the maximiser plus
   a move set, not of the maximiser alone.
8. **Topology, and the KIND of boundary** — whether a component is an arc or
   WRAPS into a loop, and what its ends are. THREE kinds of end are known and
   they are not the same phenomenon:
   * a **wall end**, where the count steps to a neighbouring value and stays
     there (727 arc A ends at 723 and 721);
   * a **degeneracy puncture**, where the count collapses because cubes coincide
     (the n=2 diagonal loop is punctured at three angles, each counting 1);
   * a **wall dip**, where the count drops exactly ON the wall and recovers on
     the far side, so the locus is not cut at all. Measured 2026-08-05: the 723
     line dips to 717 at u = −4, u = 39, u = 56 and at its point at infinity,
     with 723 on both sides of every one. A dip is invisible to any sweep whose
     grid misses it and fatal to any sweep whose grid lands on it — a sampled
     "end" at a nice rational should be suspected of being a dip until the
     chamber on the far side is evaluated.

   **All three are the same event seen three ways: a COINCIDENCE SPIKE.**
   Counting the real edge-edge crossings on each side of a boundary and at it
   (2026-08-06) — two edges from different cubes generically miss, so every
   crossing is a codimension-1 coincidence:

       n=2 edge arc, t = 1/2 and t = 1     interior 10  ->  END 24  ->  outside 8
       n=6 727 arc A, s = 19/6             interior 144 ->  END 162 ->  beyond 142
       n=2 diagonal arc, t = 1 (puncture)  interior 24  ->  END 48  ->  outside 24

   Every boundary point carries MORE coincidences than either side. An arc ends
   because its line runs into a more degenerate stratum, never because the
   geometry runs out. What distinguishes the three kinds is only what the count
   does at the spike: it HOLDS (13 at both edge-arc ends, so the end is in the
   set and the arc is closed), it DROPS to a value of its own (725 at arc A's
   end, between the 727 inside and the 723 beyond, so the arc is open), or it
   COLLAPSES because the cubes coincide (1 at the diagonal puncture, where the
   crossings double to 48 and the rotation is a cube symmetry).

   The two edge-arc ends are worth a second look: 24 crossings is exactly what
   the body-diagonal 13-pair carries along its whole length, and the rotation
   there has every entry a third — (1/3)[[2,1,2],[1,2,−2],[−2,2,1]] at t = 1/2,
   angle arccos(1/3). So the edge arc runs from one maximally-coincident
   configuration to another across a 10-crossing interior, and is closed at both
   ends because the count survives the spike.

## 2. The table

| n | max | moduli dim | components | types | symmetry | arithmetic |
|---|---|---|---|---|---|---|
| 2 | 13 | **1** | **2 arcs + finitely many classes** | **1** — one profile (1,6,6,1) on BOTH arcs | **D₆** (12) | rational dense on the arcs |
| 3 | 67 | **0**, but see §4 | **exactly 2** | 1 each | **O** (24) oct / **D₃** (6) golden | both irrational, ℚ(√2), ℚ(√5) |
| 4 | 183 | **0 by every probe**, not proved | ≥1; all 5 climbs give ONE class | 1 | **C₃** | rational |
| 5 | 393 | **0** against single-cube moves | ≥1 | 1 | **C₃** | rational |
| 6 | 723 | **≥1** | **13** (orbit dedup) ; family is VAST — see below | **≥11** exact on the wrapping line | **C₃** | rational |
| 6 | **727** | **1** | **≥4** — exactly **3** from the ℚ(√d) campaign (orbit dedup), plus the record's line | **≥10** on arc A | **trivial** | rational and irrational on ONE arc |
| 7 | 1217 | **≥1**, extent 2.64° | ≥1 | **exactly 7** | **trivial** | rational |
| 8 | **1895** | **≥2**, two directions | ≥1 | **≥8** | **trivial** | rational |

Type counts from a SWEEP are lower bounds: several chambers are narrower than
the grid and resolve to a single sample, so a finer grid can only split them
further. The n=7 count and the 723 count are not sweeps — they come from solving
for every wall crossing on the line and evaluating once between consecutive
roots (§3a), which cannot miss a chamber and so is exact.

**n = 8 is 1895, not 1891** (2026-08-05). See §3 for the configuration and §7
for how it was found and where it has been propagated.

## 2a. The wall signature — which coincidences meet at each maximiser

A maximiser is never in the interior of a chamber: no direction preserves the
count except along a tangent (0 of 580 at n = 4, 0 of 1160 at n = 5, down to
ε = 1/512), so it lies on an intersection of walls. **Which** walls is a
categorisation in its own right, and it is discrete. Counting real edge-edge
coincidences per cube PAIR:

| n | max | 13-pairs (24 crossings) | 9-pairs (6) | 4-pairs (0) | total | rank of the crossing Jacobian |
|---|---|---|---|---|---|---|
| 2 | 13 diagonal | 1 | – | – | 24 | 2 of 3 |
| 2 | 13 edge arc, interior | 1 (but **10** crossings) | – | – | 10 | 3 of 3 |
| 2 | 13 edge arc, ends | 1 | – | – | 24 | 2 of 3 |
| 4 | 183 | 3 | 3 | 0 | 90 | 8 of 9 |
| 5 | 393 | 4 | 6 | 0 | 132 | 11 of 12 |
| 6 | 723 | 6 | 6 | 3 | 180 | 13 of 15 |
| 6 | 727 arc A | 4 | 8 | 3 | 144 | 13 of 15 |
| 6 | **727 record** | 4 | 9 | 2 | 150 | 14 of 15 |
| 7 | 1217 | 6 | 9 | 6 | 198 | 16 of 18 |
| 8 | **1895** | 8 | 9 | 11 | 246 | 18 of 21 |

**Crossings per pair take only three values, 24, 6 and 0, and they correspond
exactly to the project's existing pair labels 13, 9 and 4** — verified pair by
pair at n = 5, 6 and 8. So at n ≥ 4 this axis re-derives the pair label from
geometry rather than from counting, and it reproduces the ledger's
`6x13 9x9 6x4` at n = 7 and `8x13 9x9 11x4` at n = 8 exactly.

**But it is strictly FINER than the pair label**, and n = 2 shows where. A
13-pair in isolation carries 24 crossings **or 10** — the diagonal family and the
edge arc's two ends carry 24, the edge arc's interior carries 10 — and a 9-pair
carries 8 in isolation but 6 inside every maximiser. The pair label cannot see
either distinction. Maximisers use only the 24-kind of 13-pair and only the
6-kind of 9-pair.

### What it suggests for finding maxima

**The 9-pair count is frozen at 9 along the top of the tower.** 727, 1217 and
1895 all carry exactly nine 9-pairs while the 13-pairs run 4 → 6 → 8 and the
4-pairs run 2 → 6 → 11. Both extensions therefore added **exactly two 13-pairs,
zero 9-pairs, and 4-pairs for the rest** — 6 new pairs at n = 7 (2 + 0 + 4) and 7
at n = 8 (2 + 0 + 5). That is a precise extension rule to search against: look
for a cube forming exactly two 13-pairs with the existing compound and no
9-pairs, rather than sampling rotations and counting.

**Locally the relation is nearly a function, and still not monotone.** Taking
all 290 primitive Cayley directions at ε = 1/64 from the n = 4 183 and recording
both counts, each region value corresponds to ONE crossing value exactly — the
range is zero within every row:

    crossings   54    58    60    64    66    78   |   90
    regions    161   163   167   169   173   171   |  183
    directions 174    41    65     4     2     4   |  the maximiser

Pearson r = **+0.927**, and the map crossings → regions is single-valued. But it
inverts once: the 78-crossing direction gives **171**, while the 66-crossing
direction gives **173**. A local climb on coincidences picks 78 and loses two
regions. So coincidence count is a strong predictor and a broken objective at
every scale — globally it prefers 723 over 727, locally it prefers 171 over 173.
(Cubes 2 and 3 give identical tables, which is 183's C₃ acting.)

What does hold at the maximiser itself: 90 crossings and 183 regions are both
strict local maxima, every one of the 290 neighbours being lower in both. So the
two agree AT a maximiser and disagree in how they rank the configurations around
it — which is exactly the wrong way round for a search that has to navigate by
comparing non-maximal candidates.

**Do NOT maximise coincidences.** 723 carries the richest structure in the table
— 180 crossings, six 13-pairs — and loses to 727's 150 crossings and four
13-pairs. The record beat 723 by trading two 13-pairs for three 9-pairs, which is
the pair-language version of "the record left the corner-concurrence stratum".
Crossing count is therefore not a usable surrogate objective for a climb; the
pair-type MULTISET is the thing to target, not its total.

## 3. How to generate a member of each category

All commands run in this directory. `BASE` is the five-cube 393 compound:

    BASE="4,1,1,-1;3,3,7,3;5,-1,-5,-5;2,1,1,1;1,1,1,1"

### n = 2, max 13 — a one-parameter family

Body-diagonal arc, every member:

    ./cube_regions_n --quats "1,0,0,0;d,n,n,n"      any 0 < n < d, n/d ≠ 1

13 for every such (n,d); at n/d = 1 the rotation is a cube symmetry and the
count collapses to 1. One type along the whole arc. Off the diagonal: 9.

The edge arc, now measured exactly, is rotations about an edge axis:

    ./cube_regions_n --quats "1,0,0,0;d,n,n,0"      exactly 1/2 <= n/d <= 1

— that is θ ∈ [arccos(1/3), arccos(−1/3)], since for t = n/d the rotation angle
satisfies tan(θ/2) = t√2, so the two ends tan(θ/2) = 1/√2 and tan(θ/2) = √2 are
exactly t = 1/2 and t = 1. **The interval is CLOSED**: t = 1/2 and t = 1 count
13, while t = 1/2 − 1/1024 and t = 1 + 1/1024 count 9. So the ends are wall ends
where the level set is closed, not punctures. The negative half t ∈ [−1, −1/2]
is the inverse rotation and the same congruence class.

**The two arcs carry the SAME type.** Both count 13 with per-label (1, 6, 6, 1)
at every sampled point of both, so the n=2 type column is 1 globally, not 1
per arc — an invariant that does not separate the two components even though
they are geometrically unrelated. The edge arc does NOT wrap: t → ∞ is the
half-turn about (1,1,0), which counts 1, and t = 3/2, 3, 10, 100 all count 9.

The extra classes are the half-turns about (1,2,3) and (1,1,2).

### n = 3, max 67 — two classes, so two members

    printf '1:0,0:0,0:0,0:0;1:0,1:0,0:1,0:0;-1:0,1:0,0:1,0:0\n' | ./cube_regions_q2 --d 2 --quats-stdin
    printf '1:0,0:0,0:0,0:0;2:0,1:1,-1:1,0:0;-2:0,1:1,-1:1,0:0\n' | ./cube_regions_q2 --d 5 --quats-stdin

Both {I, R, R²} with R a 120° turn about the dihedral axis; derivation in
`MAXIMISERS.md`. There is nothing else to generate — the set is these two.

### n = 4, max 183 — one known class, and every probe reads isolated

    ./cube_regions_n --quats "1,0,0,0;0,5,3,2;1,-4,-1,1;1,1,-1,-4"

Two probes, one of which took three attempts to make meaningful:

* **The aligned probe**: 18 single Cayley-axis moves at ε = 1/64, 1/256, 1/1024
  plus the four quaternion-component moves of the half-turn cube — **0 of 20
  hold**, and the neighbouring counts (161–173) do not even depend on ε. Per
  `FAILURE_MODES.md` 11d this means "not aligned", never "isolated".
* **The direction scan, third attempt and the first that carries information**:
  1 730 primitive integer directions |uᵢ| ≤ 6 in the **Cayley** chart, both free
  cubes with w ≠ 0, ε = 1/32, 1/128, 1/512 — **0 of 3 460 hold**. Its control is
  727 arc A, whose tangent (1,−3,−6) is in general position: the same protocol
  returns exactly ±(1,−3,−6) there, **2 of 1 730**, and nothing else.

**The first two attempts were void, for two independent reasons, and both are
worth keeping.** (a) CHART: the scan ran in the quaternion charts q → q·(1,εu)
and (1,εu)·q. A direction that is an integer triple in one chart is not one in
another, and every tangent this project has verified — (1,1,0), (1,1,1),
(1,−3,−6), (1,1,−4) — is integral in the CAYLEY chart and no other. (b) RANGE:
the direction set was |uᵢ| ≤ 3, which does not contain (1,−3,−6) or (1,1,−4) at
all, so two of the four known tangents were never candidates in any chart.

**Both slipped through because of how the controls were chosen**, which is the
part that generalises. The controls used were n = 2's (1,1,0) and (1,1,1) and
723's (1,1,1) — the three easiest tangents in the project. They are axis-parallel,
so every chart agrees on them and (a) is invisible; and they are the smallest
integer triples there are, so they sit inside any search set and (b) is invisible
too. **A control has to be chosen because it is hard for the method, not because
it is to hand.** See `FAILURE_MODES.md` 13a.

One defect no chart fixes: cube 2 is the half-turn (0,5,3,2), whose Cayley point
is at infinity, so a Cayley scan cannot reach it. A third of n = 4's moduli space
is unscannable this way, and the cell's zero is partial by construction.

### n = 5, max 393 — rigid against moving one cube

    ./cube_regions_n --quats "$BASE"

No single-cube perturbation preserves it (§4), so within that slice this is the
only member. The 393 cell rests on the 46 rank-2 wall directions and the 548
in-plane directions of §4, plus, from 2026-08-05, sweeping each of the 12 Cayley
axes over s ∈ [−1/2, 1/2] at step 1/64: 393 appears at exactly one sample of each
of the 12 sweeps, its own, and is never exceeded anywhere on them.

And from the same date, the repaired direction scan of §3 n = 4 — 1 730 Cayley
directions |uᵢ| ≤ 6 at three ε — reads **0 of 6 920** here. Unlike n = 4 every
free cube at n = 5 has w ≠ 0, so the Cayley chart reaches all four and this
covers the whole single-cube slice, with a control that recovers a
general-position tangent 2 of 1 730. It is the strongest negative reading in the
table. (The earlier 290-direction quaternion-chart scans, which also read 0
here, are void — see n = 4.)

### n = 6, max 723 — a one-parameter stratum, filtered

**The family has a one-line generator.** Every member is the sixth cube rotated
about the shared C₃ axis, so the candidates are exactly

    ./cube_regions_n --quats "$BASE;d,n,n,n"        any coprime (n, d)

— one parameter instead of three, the same shape as the n=2 generator. But 723
is NOT universal on it: over 14 573 coprime (n,d) the counts are 723 (46.8%),
699 (30.7%), 711 (18.9%), 687 (3.0%), and no tested parameter — denominator or
|t| — predicts which. So the stratum generates the CANDIDATES for free; deciding
membership still needs a count per member. The chamber table below lists
verified members near the origin.

Free sixth cube at Cayley u·(1,1,1) (the file previously wrote this as
(2/5,2/5,2/5) + s·(1,1,1), i.e. u = 2/5 + s); as an integer quaternion,
`den, num, num, num` with num/den = u. Near the origin 723 holds on a union of
short intervals, the longest u ∈ [0.68, 1.50], punctured by dips to 711, 699,
687. **That fragmented zone is the small part of the family.**

**THE 723 STRATUM WRAPS** (2026-08-05, and the only wrap known outside n = 2).
Solving every wall crossing on the line rather than sampling it:

    723 on u in (26.883566786478..., +infinity] U [-infinity, -7/2)

and the two are ONE arc, joined through the point at infinity. Both ends are
solved, not bracketed: the lower is the exact rational **u = −7/2**, a W4
crossing; the upper is a W3 crossing, the quartic irrational 26.883566786478….
There are 743 wall roots on the whole line, none outside [−200.91, 680.48], and
evaluating once between every consecutive pair shows 723 in **every** chamber
from 26.8836 up through infinity and back down to −7/2 — **11 type-chambers**,
exact rather than a lower bound (one wall-chamber, between two roots 6·10⁻¹⁵
apart, overflows the engine and is unevaluated; it is flanked by 723).

The point at infinity is the half-turn about (1,1,1). It counts **717**, and so
do u = −4, u = 39 and u = 56: all four are wall dips, 723 on both sides. So the
locus is a circle punctured at four points, not two arcs — and the older reading
"two huge runs that extend to at least |s| = 1000" was those runs seen from
inside, with the join at infinity never tested.

Measured as rotation angle the loop spans **21.19°**, against 3.99–8.43° for the
727 arcs: the 723 family is not merely larger than the record's, it is larger by
2.5× than the widest 727 arc. The 1/32-grid picture of a fragmented zone near
the origin described a different part of the same line.

One representative per chamber of the near-origin zone, all counting 723 with
distinct per-label. These ranges are in the OLD parameter s = u − 2/5, so the
table's [9/64, 11/64] is u ∈ [0.5406, 0.5719]; the quaternions are the
authoritative form:

| s-range | member (append to BASE) |
|---|---|
| [9/64, 11/64] | `160,89,89,89` |
| [9/32, 9/32] | `160,109,109,109` |
| [19/64, 23/64] | `320,233,233,233` |
| [3/8, 29/64] | `640,521,521,521` |
| [15/32, 31/64] | `640,561,561,561` |
| [1/2, 33/64] | `640,581,581,581` |
| [17/32, 9/16] | `320,303,303,303` |
| [37/64, 19/32] | `640,631,631,631` |
| [39/64, 23/32] | `640,681,681,681` |
| [47/64, 49/64] | `20,23,23,23` |
| [25/32, 61/64] | `640,811,811,811` |
| [31/32, 65/64] | `640,891,891,891` |
| [33/32, 17/16] | `320,463,463,463` |
| [69/64, 35/32] | `640,951,951,951` |

### n = 6, max 727 — an arc, with rational and irrational members alike

Arc A: sixth cube at Cayley (19/3, −7, −11) + s·(1, −3, −6). 727 for s across
roughly [2.11, 3.05]; 721 at s = 2, 723 at s = 13/4.

One representative per chamber:

| s-range | member (append to BASE) |
|---|---|
| [67/32, 69/32] | `24,203,-321,-570` |
| [35/16, 37/16] | `12,103,-165,-294` |
| [75/32, 75/32] | `96,833,-1347,-2406` |
| [19/8, 39/16] | `96,839,-1365,-2442` |
| [79/32, 79/32] | `96,845,-1383,-2478` |
| [5/2, 83/32] | `192,1705,-2811,-5046` |
| [21/8, 21/8] | `24,215,-357,-642` |
| [85/32, 85/32] | `96,863,-1437,-2586` |
| [43/16, 11/4] | `96,869,-1455,-2622` |
| [89/32, 101/32] | `96,893,-1527,-2766` |

**A member in ANY quadratic field** — take s = 5/2 + √d/100, inside the arc for
every d ≤ 97, giving a distinct congruence class per squarefree d:

    printf '4:0,1:0,1:0,-1:0;3:0,3:0,7:0,3:0;5:0,-1:0,-5:0,-5:0;2:0,1:0,1:0,1:0;1:0,1:0,1:0,1:0;300:0,2650:3,-4350:-9,-7800:-18\n' \
      | ./cube_regions_q2w --d 3 --quats-stdin

The other three arcs, now measured. All pairwise skew with A; none wraps.

| arc | through | along | 727 extent | width | chambers |
|---|---|---|---|---|---|
| B | (4/35, 2/5, −41/35) | (1,1,−4) | s ∈ [**43/105**, ≈0.579411] — SOLVED | 0.1699 | ≥13 |
| A | (19/3, −7, −11) | (1,−3,−6) | s ∈ [≈2.063979, **19/6**] — SOLVED | 1.103 | 10 |
| C | (245/29, −295/29, 428/29) | (1,−3/2,9/4) | s ∈ [≈1.167462, ≈47.772089] — SOLVED | 46.605 | ≥13 |
| D | (2, 1/7, −5/7) — the record | two tangents, see below | widths 1/4 and 5/16 | — | — |

**All bounds are now solved, not swept** — each is a root of a wall equation on
the arc's line (quadratic for W4, quartic for W3). Two are exactly rational,
19/6 and 43/105; the rest are algebraic irrationals no grid could land on.
**Five of the six ends are W4**, only arc C's lower end being W3. And W3+W4
bracket every chamber wall observed on every arc — 15/15, 12/12, 12/12, i.e.
**39 of 39** — though only about a quarter of the interior crossings (48, 62, 77)
change anything, so a bracket containing a crossing must be split, not reported.

**Extent is roughly UNIFORM**, contrary to what this file said until Postscript
97. The 300–500× spread was Cayley-chart length; measured as rotation angle the
arcs are A 3.99°, B 7.04°, C 8.43°, D1 5.91°, D2 7.31° — a spread of 2.1×. Arc C
looked vast only because it runs toward a half-turn, where tan(θ/2) diverges.
Chamber counts are comparable (10–12), so chamber DENSITY differs by the same
factor. Every end steps down to 723, except arc A's lower end at 721.

**Arc D is a crossing**: the record carries two independent tangents,
(−1,−1/7,3/14) and (−1,−4/21,2/7), whose combinations all fail — two arcs
meeting at a node, not a surface. Both were re-verified exactly on 2026-08-05
(727 at s = ±1/64, ±1/32, ±1/16 along each; their sum drops to 721 at ±1/64).
Neither is axis-aligned, and correspondingly no single Cayley axis of any of the
five free cubes holds 727 anywhere on s ∈ [−1/2, 1/2] except at s = 0 itself.

**None of the four 727 arcs wraps.** Each line's point at infinity is the
half-turn about its direction, and those count 699 (A), 693 (B), 689 (C), 693
and 691 (D's two tangents); the tails at |s| = 100 … 10⁶ count 691–715. So all
four terminate, and 723 is the only wrapping family known above n = 2.

### n = 7, max 1217 — an arc, both ends solved

    ./cube_regions_n --quats "$BASE;7,14,1,-5;4,-3,-4,-4"

The free direction is **cube 7's Cayley x** — the (4,−3,−4,−4) cube at Cayley
(−3/4,−1,−1), not the sixth cube as this file said until 2026-08-05. Exactly
**1 of 36** single-axis moves preserves 1217, at ε = 1/64 and 1/256 alike, and
it is one-sided (x− holds, x+ does not), so the record sits near an end.

Solved, not swept — every W3/W4 crossing on the line, evaluated once between
consecutive roots:

    1217 on s in (-0.045258752093..., +0.002550224044...)

**both ends W4**, 32 wall-chambers carrying **exactly 7 types**. Cayley extent
0.0478, which as rotation angle is **2.64°** — two thirds of 727 arc A and an
eighth of the 723 loop. The earlier figure "extent 1/32" was a sweep artefact, 35% low.
Does not wrap: the half-turn about x counts 727 and the tails 1209.

### n = 8, max 1895 — a NEW RECORD, and the same shape

    ./cube_regions_n --quats "$BASE;7,14,1,-5;4,-3,-4,-4;24,-24,24,-61"

**1895, beating the 1891 that stood since Postscript 46.** by_depth
{1:350, 2:454, 3:382, 4:302, 5:222, 6:136, 7:48, 8:1}; reproduced by both
engines; a local maximum against every ±1, ±2 move of every quaternion
component. Its 7-cube subsets give exactly 1217, its 6-cube 727, its 5-cube 393,
so the tower is now **13 / 67 / 183 / 393 / 727 / 1217 / 1895**.

It was found by continuing the sweep that the 1891 write-up had stopped: 1891's
own eighth cube is (3,−3,3,−8) at Cayley (−1,1,−8/3), and the old report gave
"1891 on [0,3/32] and again on [15/64,3/8]" along z. At z-offset **s = 1/8**,
just past the first interval and inside the reported gap, the count is 1895.
See §7.

Two independent directions hold 1895 — **2 of 42** single-axis moves, cube 7's
Cayley x and cube 8's Cayley z — so its moduli dimension is ≥ 2, as 1891's was.
Along cube 8's z, solved:

    1895 on s in (-0.025621839667..., +0.101360157756...)

lower end **W3**, upper end **W4**, 29 wall-chambers carrying **≥ 8 types** — 28
evaluated, and the 29th overflows the wide engine and is flanked by 1895 on both
sides, so it is reported as unevaluated rather than as a gap. Cayley
extent 0.127, rotation angle **2.72°**. Does not wrap: the half-turn about z
counts 1217 and the tails 1887.

### 3a. How the extents and chamber counts above were obtained

Not by sweeping. A sweep gives an interval accurate to its step, a chamber count
that is only a lower bound, and no way to tell a wall dip from an end. The count
and the per-label profile are constant BETWEEN consecutive wall crossings on a
line, so:

1. build the base's W3/W4 catalogue — `incidence2.base_catalogue` is hard-wired
   to the five-cube 393 base, so for the n = 7 and n = 8 lines it is rebuilt for
   an arbitrary base (`catalogue(cubes)`, same code with `FIVE` parametrised);
2. solve for every root on the line — `wall_params.w4_params` (a quadric in the
   line parameter) and `w3_params` (a quartic);
3. evaluate the engine ONCE strictly between each consecutive pair of roots.

The result is the exact chamber decomposition: ends named as roots rather than
bracketed, no chamber missed however narrow, and a dip distinguished from an end
by looking at the chamber on the far side. Costs of the three lines used above:
743 roots (723 line), 3 997 (n = 7), 5 985 (n = 8), and one engine call per
chamber in the window. `exact_chambers.py` in the session scratch.

Two caveats. The catalogue bounds triple points at |p| ≤ 4, so a wall from a
point outside that ball is missed. And a rational strictly between two roots
that are 10⁻⁷ apart has a denominator large enough to overflow even the wide
engine — one chamber of the n = 8 line and one of the 723 line came back as
rejections, and are reported as unevaluated rather than as count changes.

## 4. Why the cells read what they do

**Moduli dimension** is measured two ways, and they are not interchangeable.
The *aligned* probe counts how many of the 2k single-coordinate ±ε moves
preserve the count; 2d survive for a family aligned with d coordinate
directions, so a positive reading is a valid lower bound and **a zero reading
means only "not aligned"** — it cannot distinguish an isolated class from a
curve in general position (`FAILURE_MODES.md` 11d). The *tangent space* is the
null space of the active wall normals, exact over ℚ. **Rank 2 gives a CANDIDATE
tangent, to be verified; rank 3 proves only that no direction is orthogonal to
every catalogue wall — NOT isolation**, since most coincidence crossings do not
change the count. Test rank-2 subsets and verify each (`tangent_finder.py`).

* **13 = 1** — tangent along the body diagonal; perpendicular the count is 9.
* **67 = 0** — 67 = 1 + 18 + 48 forces all three pair terms to 6 and all three
  singleton terms to 16 at once; s_i = 16 needs both pairs at cube i to be
  13-pairs, on a set of codimension 4 in the 6-dimensional moduli space. Two
  such conditions already overshoot (4+4 > 6), three give 12. A codimension
  heuristic, not a rank computation — the honest finish is the Jacobian rank at
  each 67. Corroborated: the best rational triple is 63, and every rational
  member of the distinct-axis part of (13,13,13) is degenerate.
* **183 = 0 by every probe** — this cell read "≥ 3, aligned probe, 6 of 18
  single-axis moves" until 2026-08-05 and **that figure is withdrawn**: it is
  sourced nowhere in the ledger, and re-running the probe gives 0 of 20 at three
  ε and 0 of 870 integer directions at three scales (§3). What can be said is
  that no single-cube direction of the tested kind holds 183 — not that 183 is
  isolated, which needs a method that survives its controls.
* **393 = 0 against single-cube moves** — 12 active walls giving **46** distinct
  rank-2 subset directions, not one preserving 393 at ε = 1/64 or 1/1024; plus
  548 in-plane directions at four ε scales down to 1/65536, the count dropping
  to 377 in every one; plus the 1160-direction scan and the 12 axis sweeps of §3.
  **Note the scope of the 377**: those 548 directions were restricted to a wall
  plane. Over all 290 primitive Cayley directions the neighbourhood of 393 takes
  **14 distinct counts** and its best neighbour is **391**, not 377 — so 393
  stands only 2 above its surroundings, not 16.
* **723, 727 ≥ 1** — tangents (1,1,1) and (1,−3,−6), both from the null space,
  both walked.
* **1217 ≥ 1, 1895 ≥ 2** — aligned probe, engine-verified directions: 1 of 36 at
  n = 7 (cube 7 Cayley x), 2 of 42 at n = 8 (cube 7 x and cube 8 z, different
  cubes and so independent).

**A third method exists and it FAILS ITS CONTROL** — recorded here because
Postscript 100 rests on it. `tight_set.py` takes the null space of the gradients
of the TIGHT Step-A conditions (those holding with equality), and its zeros at
the two 67s are the current basis for "exactly two 67s". Run on the five
configurations with independently verified tangents (2026-08-05):

    n=2 mirror-plane 13     null dim 1   known tangent recovered  1.0000  PASS
    n=2 body-diagonal 13    null dim 1   known tangent recovered  1.0000  PASS
    n=6 723 at u = 9/10     null dim 2   known tangent recovered  1.0000  PASS
    n=6 727 arc A midpoint  null dim 2   known tangent recovered  1.0000  PASS
    n=6 727 RECORD          null dim 1   D1 0.6018, D2 0.6194     FAIL

The record carries two verified tangents, so any correct linearisation must have
null dimension ≥ 2 there; it returns 1, and neither tangent lies in it. **So the
method's zeros are not upper bounds on the moduli dimension**, and its 0 at the
two 67s is evidence, not proof.

The natural repair is refuted too. A tight quantity sits exactly at 1, where the
slab is degenerate and bounds no open region, which suggests the count-preserving
set is the CONE {J·v ≤ 0} rather than the null space {J·v = 0}. It is not: at the
record, J·D1 and J·D2 each have **6 strictly positive components** out of 204 and
the count holds regardless. The failure is that some tight conditions are tight
but not BINDING — the degenerate incidence is not where a bounded region would
open.

**The offending conditions are now identified by name** (2026-08-06,
`record_six.py`). Decoding each violated row of the Jacobian:

    D1 violates 12 rows: cubes (1,5) and (5,1), all SLAB-PAIR conditions
    D2 violates 12 rows: cubes (0,5) and (5,0), all SLAB-PAIR conditions

Three facts fall out, and together they explain the node.

* **Every violated condition is a slab-PAIR condition.** Not one single-slab
  ‖n‖₁ = 1 condition is violated by either tangent. The two halves of Step A are
  not equally binding: the singletons hold the count, the pair minima need not.
* **Each tangent's violations are confined to ONE base cube against the free
  cube** — cube 1 for D1, cube 0 for D2, six quantities each, twice over because
  the quantity is emitted for both orders of the pair.
* **The two tangents release DIFFERENT cubes.** That is what arc D's crossing is:
  the record sits where the free cube can give up its pair conditions with cube 1
  (one arc) or with cube 0 (the other), and a combination gives up both at once,
  which is why every combination fails.

Dropping exactly those 24 rows takes the rank from 14 of 15 to **12 of 15**, null
dimension 3, and **both tangents project 1.0000** into it. So the repair is real
and the method is recoverable; what is missing is a NON-CIRCULAR rule for
identifying a tight-but-not-binding pair condition, since "drop the rows the
known tangent violates" uses the answer. The candidate rule is geometric rather
than algebraic — a pair tangency that does not bound a region — and testing it
needs the arrangement, not the ℓ¹ norms.

Consequently, the null-space dimensions this method reports at the untested
cells are candidates only, and are recorded as such rather than as table
entries: n=4 183 → 1, n=5 393 → 1, n=7 1217 → 2, n=8 1891 → 3. None of their
directions survives an engine walk.

**Symmetry decays from the maximum possible**, and is named by GROUP, not order
— order alone is ambiguous, since 12 could be C₁₂, D₆ or T, 24 could be C₂₄,
D₁₂ or O, and 6 could be C₆ or D₃. Identified from element-order histograms:

    n=3  67 octahedral   O    {1:1, 2:9, 3:8, 4:6}   the FULL octahedral group
    n=2  13              D₆   {1:1, 2:7, 3:2, 6:2}   (not T, the other order 12)
    n=3  67 golden       D₃   {1:1, 2:3, 3:2}        (not C₆)
    n=4,5,6  183/393/723 C₃   {1:1, 3:2}
    n=6,7,8  727/1217/1895   trivial

O → D₆ → D₃ → C₃ → trivial. The octahedral 67 carries the full cube rotation
group, the largest a compound can have. Note the two 67s differ in group TYPE,
O against D₃, not merely in order.
The collapse to trivial is exactly at 723 → 727, which the ledger independently
describes as the record leaving the corner-concurrence stratum. Symmetry also
**separates the two 67s (24 vs 6) where per-label cannot** — their profiles are
identical — so it is a congruence invariant independent of Theorem R. And 183
is C₃-symmetric, though it was found by hill-climbing, not symmetry seeding.

**Type-richness rises as symmetry falls.** The n=2 maximiser is combinatorially
uniform along its entire continuum — one chamber, no walls — while the n=6
maximisers are cut into ten and fourteen chambers over comparable stretches.

**Finite or uncountable, never countably infinite.** Every level set is
semialgebraic, so it has finitely many components, each a class or of dimension
≥1. Hence the isolated maximisers are finite in number and any infinite
maximiser set contains a continuum. "Finite" was the only alternative n=3 could
have had.

## 4a. The epsilon-neighbourhood as a recursive stratification

The dimension figures above all come from probing an epsilon-neighbourhood, and
the probes are steps of one recursion rather than separate tricks:

1. The neighbourhood of a configuration is **3(n−1)-dimensional** (the moduli
   space, gauge already spent).
2. Probe it. Two probes that **DIFFER** imply a boundary between them. Two that
   **AGREE** suggest a continuum through the centre in that direction.
3. **Extend an agreeing direction.** It must either reach a boundary or **wrap**
   — and wrapping is a distinct topological category, not a failure to find the
   end.
4. A boundary is a stratum of **lower dimension**. Recurse into it.
5. Terminate at point transitions, dimension 0.

Seen this way the tools line up: the *aligned probe* is step 2 by sampling; the
*null space of the active wall normals* is step 2 done exactly, returning every
agreeing direction at once and proving when there is none; the *sweep* is step 3;
and step 4 is the part not yet built.

**The loop case is real, not hypothetical.** The n=2 13-locus about a body
diagonal wraps: in Cayley coordinates the family is t·(1,1,1), and t → ∞ is the
half-turn (0,1,1,1), which counts 13. Verified at t = 1/1000, 1/10, 2, 10, 1000,
∞, −1/1000, −10, −2 — all 13. So the locus is a **circle**, punctured at t = 0,
+1 and −1 (the identity and the two 120° cube symmetries), each counting 1. The
three punctures are one C₃ orbit, so the C₃ about that axis permutes the three
resulting arcs cyclically and they are ONE arc in class space.

**And the 723 stratum wraps too** (§3), which makes the loop case the rule
rather than the curiosity: of the seven families now tested for it, two wrap.
Both wrapping families run along a symmetry axis of the base — the body diagonal
at n = 2, the shared C₃ axis at n = 6 — and both have their point at infinity a
half-turn about that axis. The five that terminate (727 arcs A–D, n = 7, n = 8)
run in general directions. That is a testable prediction rather than a proved
statement, and the cheapest test is the next family found along an axis.

Contrast 727 arc A, which does not wrap: it terminates at 723 and 721. Same
dimension, different topology, and the difference is invisible to every
dimension measurement.

**Before trusting any dimension figure below**, see FAILURE_MODES 13: a method
that reports 0 must first recover a known tangent, or its zeros are void.

## 5. Gaps, and the path to close each

* **Multi-cube directions at n = 3 — REOPENED.** Postscript 100 closed this with
  `tight_set.py`, on the strength of one control at n = 2. Run against all five
  controls it fails the fifth, the n = 6 record, returning null dimension 1 where
  two independent tangents are verified (§4). Its rank 6 of 6 at the two 67s is
  therefore evidence and not proof, and "exactly two 67s" is back to resting on
  the codimension heuristic. Path: find which tight conditions are tight but not
  binding — at the record, exactly 6 of 204 tight gradients are violated by each
  surviving tangent, a small enough set to characterise by hand.
* **Multi-cube directions at n = 4,5,6,7,8 — still open**, and now without a
  method believed at n = 3 either. Candidate null dimensions are in §4; none of
  their directions survives an engine walk.
* **Multi-cube directions are untested at every n.** All dimension figures come
  from moving ONE cube. A locus can be positive-dimensional via directions that
  move several cubes together, and nothing here excludes that — including at
  n = 3, where "exactly two 67s" would be affected. **This is the largest
  standing gap in the table.** Path: extend the null-space method to the full
  moduli space, which needs wall normals in all 3(n−1) coordinates rather than 3.
* **Components at n ≥ 4** — each needs its arcs found first. Path: the 727
  route, sweeping the maximiser locus inside each catalogue wall plane. Note
  arc A lies in only ONE catalogue plane, so a complete enumeration also needs
  the unenumerated W3/W4 walls.
* **Step 4 of the recursion is not built.** Nothing yet descends INTO a boundary
  and stratifies it. That is the general machine the one-off measurements above
  are hand-worked instances of, and it would deliver components, types and
  boundary kinds in one pass instead of one datum at a time.
* ~~Loop-versus-arc is unmeasured everywhere except n = 2~~ — **MEASURED for all
  seven families** (2026-08-05), by evaluating each line's point at infinity —
  the half-turn about its direction — rather than by extending a sweep, which
  can only ever suggest an answer. **723 WRAPS**; 727 arcs A, B, C and both of
  D's tangents terminate, as do n = 7 and n = 8. The decisive test is one engine
  call per line: the half-turn (0, d) for line direction d.
* ~~Arcs B, C, D~~ — **MEASURED**: extents 0.16, 46.6 and (two crossing arcs of
  width 1/4 and 5/16), chambers 11 and 12, all ends stepping to 723 bar arc A's
  721, none wrapping. Still open: chamber walls to full precision, which needs
  the wide engine — bisection past ~2^-8 overflows the integer engine and
  returns rejections that read as count changes. **Better: solve for them.** An
  arc bound is a root of a wall equation on the line — exactly rational for a
  catalogue plane (arc B's lower end is exactly s = 43/105, verified). Most ends
  are NOT on catalogue walls, so this needs W3/W4 enumerated first.
* ~~Enumerate W4~~ — **DONE** (`wall_params.py`): solved as crossings on a line,
  where the condition is a quadratic in the line parameter. 929 crossings on arc
  A's line, and BOTH of its ends are W4 crossings — upper exactly 19/6, lower the
  quadratic irrational ≈2.063979. This corrected arc A's extent, which the 1/32
  sweep had underestimated by 17% with both ends misplaced; every swept extent in
  this file is suspect to the same degree.
* ~~Enumerate W3~~ — **DONE** (`wall_params.w3_params`): the edge-meets-crossing-
  line determinant is degree 4 in the line parameter; 2 989 crossings on arc A's
  line. **W3+W4 bracket every chamber wall on arc A, 15 of 15**, closing the
  Postscript 58 gap. Only 15 of the 48 interior crossings change the type, so a
  wall crossing is necessary but not sufficient for a chamber boundary.
* ~~Chamber counts are lower bounds~~ — **no longer, where the line is solved**
  (§3a). Evaluating between consecutive W3/W4 roots gives the exact count:
  n = 7's 1217 has exactly **7** types over 32 wall-chambers, the 723 loop
  **11**. Arc A still reads a sweep bound (10 at 1/32, ≥16 at denominator 256,
  capped at 49 by its interior crossings) and should be redone the same way.
* ~~723's family is larger than mapped~~ — **SOLVED**, and it is a LOOP:
  723 on u ∈ (26.883566786478…, +∞] ∪ [−∞, −7/2), one arc through the point at
  infinity, 11 types, angular extent 21.19°. The lower end is exactly −7/2 (W4),
  the upper a W3 quartic root. The "two huge runs" were the two sides of one arc.
* **Component counts for other totals** — 725 has 6 arcs, 723 has 13, by the
  same orbit dedup. Unmeasured for totals below 723 and for other n. Note the 13
  arcs of 723 were counted before the wrap was known, so any two of them joined
  at a point at infinity are one component and the figure may be an overcount.
* ~~Types at n = 2's edge arc~~ — **MEASURED**, and there is only one type in all
  of n = 2: (1, 6, 6, 1) on both arcs (§3). **Types at 183** is not a gap but a
  consequence: no direction holds 183, so its type count is 1 by default.
* **The two 67s' Jacobian rank** — would upgrade their isolation from a
  codimension heuristic to a computation. Representatives are in
  `MAXIMISERS.md`; the obstacle is that the walls must be differentiated in
  ℚ(√2) and ℚ(√5) rather than ℚ.
* **Lemma B** — max(3) = 67 reduces to one two-rotation statement, g(13,13) = 16
  and g ≤ 14 otherwise, measured but unproved. Two attack routes are in the
  ledger.


## 6. Added 2026-08-05

* **Translation buys nothing, measured.** A 13-configuration loses the count
  under EVERY tested shift, at every scale down to 1/1000 — 7 along a coordinate
  axis, 5 along (1,1,0), 6 along (1,1,1). The 24 edge-edge crossings a 13-pair
  carries are destroyed wholesale: all 24 by a shift along the rotation axis,
  23 of 24 perpendicular in the mirror plane, 19 of 24 perpendicular out of it.
  So the maximiser locus does not extend into the translation directions at all,
  and the moduli space worth probing stays rotational. This sharpens Postscript
  38, which showed off-centring cannot BEAT 13; it cannot even HOLD it.
* **Translation can partially compensate a forced rotation, and the best
  direction is solvable.** Fixing a rotation δω, each crossing survives to first
  order iff aᵢ·δt = −bᵢ·δω, so the optimal δt is the solution of some 3-subset of
  24 equations — enumerable exactly. An in-plane rotation keeps 8 crossings
  unaided and 14 with the best shift; an out-of-plane rotation keeps 0 unaided
  and 9 with a shift. Never 24, so no compensated motion holds the count.
* **The mirror-plane 13 component IS a continuum** — corrected twice in one
  session. Probing x, y, z and (1,−1,0) from Cayley (−12,−11,0) gave 9/5/4 and
  was read as isolation; solving the crossing-condition Jacobian instead gave a
  rank-5 image with a one-dimensional null space along **(1,1,0)**, and sweeping
  it holds 13 for 129 of 129 samples across s ∈ [−8,8], hitting both bounds. A
  578-direction scan at two scales finds exactly ±(1,1,0) and nothing else, so
  the component is 1-dimensional here. The 784 rational members found earlier are
  points ON this curve, which is why rational search finds so many.
* ~~whether the count-13 locus and the all-24-crossings locus coincide~~ —
  **THEY DO NOT** (2026-08-06). Counting real edge-edge crossings across the
  whole n = 2 maximiser set:

      diagonal-arc member (4,1,1,1)      13   24 crossings
      (1,1,1) half-turn, the wrap point  13   24
      half-turn about (1,2,3)            13   24   isolated class
      half-turn about (1,1,2)            13   24   isolated class
      edge-arc ENDS, t = 1/2 and t = 1   13   24
      edge-arc INTERIOR, t = 3/4         13   **10**
      (1,1,0) half-turn                   1   48   a cube symmetry

  Every 13 in the table sits at 24 crossings **except the interior of the edge
  arc, which reaches 13 with only 10**. So the count does not require those
  particular incidences, exactly as the six-disjoint-slabs argument suggested,
  and the edge arc is the one part of the n = 2 maximiser set that is not
  maximally coincident. Its two ends are where it climbs back to 24 — which is
  why they are closed ends rather than open ones (§1).
* **The two n = 2 arcs do not intersect.** Under the 24 cube rotations the
  edge-arc endpoint's axis orbit is edge-type only, never a body diagonal, so no
  edge-arc member is congruent to any diagonal-arc member however the angles are
  matched — and the endpoint's angle arccos(1/3) IS also attained on the diagonal
  arc, so equal angle and equal crossing number still do not make them meet.
  n = 2 has two disjoint components and no node; the n = 6 record's crossing of
  arc D remains the only intersection known anywhere in the table.
* **Still open:** the dimension by SOLVING the Step A slab conditions rather than
  scanning directions.

## 7. The n = 8 record, and what still says 1891

**1895.**

    ./cube_regions_n --quats "$BASE;7,14,1,-5;4,-3,-4,-4;24,-24,24,-61"

**How it was found, because the method generalises.** 1891's write-up recorded
its eighth cube as free along Cayley z, "1891 on [0, 3/32] and again on
[15/64, 3/8]". 1895 occupies (0.1016, 0.2227) — precisely the gap BETWEEN those
two intervals, inside the window the original sweep had already covered. It was
missed because the sweep recorded where 1891 held rather than what the line
carried, so the gap read as a dropout instead of a rise. **A plateau sweep should record the
maximum over the line, not the indicator of one value.** Three other lines were
re-swept the same way on 2026-08-05 (every Cayley axis of every free cube at
n = 5, 6, 7, 8 over s ∈ [−1/2, 1/2] at step 1/64) and none beat its record, so
this was an omission on one line rather than a systematic one.

**Confidence.** Both engines agree; by_depth sums correctly; a local maximum
against all 128 single-component ±1, ±2 lattice moves; its 7-, 6- and 5-cube
subsets give exactly 1217, 727 and 393, so it sits on the known tower rather
than beside it.

**The omission was confined to that one line — audited, 2026-08-06.** If a sweep
reporting the indicator of a known value rather than the maximum could hide 1895,
every other line in the catalogue could be hiding something too. All six were
re-read for their MAXIMUM by the solve of §3a — roots, then one evaluation
strictly between each consecutive pair:

| line | chambers | unevaluable | max | known |
|---|---|---|---|---|
| 723, u·(1,1,1), the middle stretch u ∈ (−7/2, 26.88) | 705 | 14 | **723** | 723 |
| 727 arc A, s ∈ (−20, 20) | 3 808 | 255 | **727** | 727 |
| 727 arc B, s ∈ (−20, 20) | 3 805 | 123 | **727** | 727 |
| 727 arc C, s ∈ (−20, 60) | 4 411 | 894 | **727** | 727 |
| 727 arc D1, s ∈ (−20, 20) | 3 767 | 207 | **727** | 727 |
| 727 arc D2, s ∈ (−20, 20) | 3 812 | 234 | **727** | 727 |

**20 308 chambers, nothing above the known value on any line.** The 723 line is
now read end to end — both tails, the point at infinity and this middle stretch,
which had only ever been sampled. Scope: 1 727 chambers (8.5%) are unevaluable,
their midpoints between roots too close together for even the wide engine, and
arc C is the worst at 20%. So this is "no record in 91.5% of the chambers on six
lines", not a proof.

**And the counts are arithmetically stratified.** Listing every chamber value and
every wall value separately over a window of each line:

    arc A, s in (2, 3.5)    chambers 727, 723, 719      walls 727, 725, 723
    723,   u in (-6, -3)    chambers 723, 711           walls 717, 705

**Every chamber count is ≡ 3 (mod 4); the values ≡ 1 (mod 4) occur only ON
walls** — 725, 717, 705 never appear on an open interval. That gives a free
diagnostic on these lines: a count ≡ 1 (mod 4) means the configuration is on a
wall, not in a chamber, which is exactly what the 717 dips were. It connects to
the project's existing mod-4 thread (`mod4_check.py`; 183 ≡ 3 mod 4). It is NOT
universal — n = 4's own neighbourhood shows chambers at 161, 163, 167, 169, both
residues — so it is a property of these lines, not of the problem.

**Propagated 2026-08-05**, once a 33 060-configuration hunt around 1895 found
nothing above it: `LEDGER.md` (appended as Postscript 101, not edited — it is a
chronological record), `MAXIMISERS.md`, `RESULTS.md`, `OVERVIEW.md`, `README.md`
and `shapes.svg`. What still says 1891 by design: `README.md`'s summary of
Postscripts 22–52, which describes what those postscripts said at the time.
