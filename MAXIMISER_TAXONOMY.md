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
   WRAPS into a loop, and what its ends are. Two kinds of end are known and they
   are not the same phenomenon: a **wall end**, where the count steps to a
   neighbouring value (727 arc A ends at 723 and 721), and a **degeneracy
   puncture**, where the count collapses because cubes coincide (the n=2
   diagonal loop is punctured at three angles, each counting 1).

## 2. The table

| n | max | moduli dim | components | types | symmetry | arithmetic |
|---|---|---|---|---|---|---|
| 2 | 13 | **1** | **2 arcs + finitely many classes** | **1** on the diagonal arc | **D₆** (12) | rational dense on the arcs |
| 3 | 67 | **0** | **exactly 2** | 1 each | **O** (24) oct / **D₃** (6) golden | both irrational, ℚ(√2), ℚ(√5) |
| 4 | 183 | **≥3** | ≥1; all 5 climbs give ONE class | — | **C₃** | rational |
| 5 | 393 | **0** against single-cube moves | — | — | **C₃** | rational |
| 6 | 723 | **≥1** | **13** (orbit dedup) ; family is VAST — see below | **≥14** near the origin | **C₃** | rational |
| 6 | **727** | **1** | **≥4** — exactly **3** from the ℚ(√d) campaign (orbit dedup), plus the record's line | **≥10** on arc A | **trivial** | rational and irrational on ONE arc |
| 7 | 1217 | **≥1**, extent 1/32 | — | 1 | **trivial** | rational |
| 8 | 1891 | **≥2**, two directions | — | 1 | **trivial** | rational |

Type counts are LOWER bounds: several chambers are narrower than the sweep grid
and resolve to a single sample, so a finer grid can only split them further.

## 3. How to generate a member of each category

All commands run in this directory. `BASE` is the five-cube 393 compound:

    BASE="4,1,1,-1;3,3,7,3;5,-1,-5,-5;2,1,1,1;1,1,1,1"

### n = 2, max 13 — a one-parameter family

Body-diagonal arc, every member:

    ./cube_regions_n --quats "1,0,0,0;d,n,n,n"      any 0 < n < d, n/d ≠ 1

13 for every such (n,d); at n/d = 1 the rotation is a cube symmetry and the
count collapses to 1. One type along the whole arc. Off the diagonal: 9.
The edge arc is rotations about an edge axis through [arccos(1/3), arccos(−1/3)];
the extra classes are the half-turns about (1,2,3) and (1,1,2).

### n = 3, max 67 — two classes, so two members

    printf '1:0,0:0,0:0,0:0;1:0,1:0,0:1,0:0;-1:0,1:0,0:1,0:0\n' | ./cube_regions_q2 --d 2 --quats-stdin
    printf '1:0,0:0,0:0,0:0;2:0,1:1,-1:1,0:0;-2:0,1:1,-1:1,0:0\n' | ./cube_regions_q2 --d 5 --quats-stdin

Both {I, R, R²} with R a 120° turn about the dihedral axis; derivation in
`MAXIMISERS.md`. There is nothing else to generate — the set is these two.

### n = 4, max 183 — one known class

    ./cube_regions_n --quats "1,0,0,0;0,5,3,2;1,-4,-1,1;1,1,-1,-4"

### n = 5, max 393 — rigid against moving one cube

    ./cube_regions_n --quats "$BASE"

No single-cube perturbation preserves it (§4), so within that slice this is the
only member.

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

Free sixth cube at Cayley (2/5,2/5,2/5) + s·(1,1,1); as an integer quaternion,
`den, num, num, num` with num/den = 2/5 + s. 723 holds on a union of intervals,
the longest s ∈ [9/32, 35/32], punctured by dips to 711, 699, 687.

One representative per chamber, all counting 723 with distinct per-label:

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
| B | (4/35, 2/5, −41/35) | (1,1,−4) | s ≈ [0.42, 0.58] | 0.16 | 11 |
| A | (19/3, −7, −11) | (1,−3,−6) | s ∈ [≈2.063979, **19/6**] — SOLVED | 1.103 | 10 |
| C | (245/29, −295/29, 428/29) | (1,−3/2,9/4) | s ≈ [1.17, 47.75] | 46.6 | 12 |
| D | (2, 1/7, −5/7) — the record | two tangents, see below | widths 1/4 and 5/16 | — | — |

**Extent spans 300x** across three arcs that are otherwise indistinguishable —
same count, same profile, same dimension — so extent is an independent axis.
Chamber counts are comparable (10–12), so chamber DENSITY differs by the same
factor. Every end steps down to 723, except arc A's lower end at 721.

**Arc D is a crossing**: the record carries two independent tangents,
(−1,−1/7,3/14) and (−1,−4/21,2/7), whose combinations all fail — two arcs
meeting at a node, not a surface.

### n = 7 and n = 8

    ./cube_regions_n --quats "$BASE;7,14,1,-5;4,-3,-4,-4"            # 1217
    ./cube_regions_n --quats "$BASE;7,14,1,-5;4,-3,-4,-4;3,-3,3,-8"  # 1891

1217 moves along cube 6's Cayley x over an interval of extent 1/32. 1891 moves
along cube 6's x AND cube 7's z, two independent directions; along cube 7's z it
is fragmented, holding on [0, 3/32] and again on [15/64, 3/8].

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
* **183 ≥ 3** — aligned probe, 6 of 18 single-axis moves.
* **393 = 0 against single-cube moves** — 12 active walls giving **46** distinct
  rank-2 subset directions, not one preserving 393 at ε = 1/64 or 1/1024; plus
  548 in-plane directions at four ε scales down to 1/65536, the count dropping
  to 377 in every one.
* **723, 727 ≥ 1** — tangents (1,1,1) and (1,−3,−6), both from the null space,
  both walked.
* **1217, 1891** — aligned probe, engine-verified directions.

**Symmetry decays from the maximum possible**, and is named by GROUP, not order
— order alone is ambiguous, since 12 could be C₁₂, D₆ or T, 24 could be C₂₄,
D₁₂ or O, and 6 could be C₆ or D₃. Identified from element-order histograms:

    n=3  67 octahedral   O    {1:1, 2:9, 3:8, 4:6}   the FULL octahedral group
    n=2  13              D₆   {1:1, 2:7, 3:2, 6:2}   (not T, the other order 12)
    n=3  67 golden       D₃   {1:1, 2:3, 3:2}        (not C₆)
    n=4,5,6  183/393/723 C₃   {1:1, 3:2}
    n=6,7,8  727/1217/1891   trivial

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

Contrast 727 arc A, which does not wrap: it terminates at 723 and 721. Same
dimension, different topology, and the difference is invisible to every
dimension measurement.

## 5. Gaps, and the path to close each

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
* **Loop-versus-arc is unmeasured everywhere except n = 2.** Whether 723's
  intervals, 727's arcs B/C/D, or the n=7/n=8 families wrap has not been tested.
  Cheap: extend each sweep well past its ends and look for the value returning.
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
* **Chamber counts are lower bounds** — arc A reads 10 chambers at 1/32, ≥16 at
  denominator 256, and is capped at 49 by its interior crossings. Sample at FIXED
  small denominator: affine maps of awkward rationals overflow the engine and the
  rejections read as type changes. These wall types (Postscripts 57, 58) were never enumerated and
  are the ones that actually bound the arcs, govern chamber structure, and
  supply the constraints `tangent_finder.py` is missing. One computation unlocks
  arc bounds, chamber walls to full precision, and correct tangent tests. Path:
  mechanical, the same sweep as arc A. Their COUNT is now settled: the campaign's
  1,449 727-records give 216 chart lines that dedupe to exactly **3 arcs** under
  the 72-element group (base C₃ × the free cube's own 24 rotations), in three
  orbits of uniform size 72. With the record's rational line that is ≥4
  components, and any further ones must come from outside the mixed ℚ(√d) family.
* ~~723's family is larger than mapped~~ — **MEASURED**: over s ∈ [−50, 50],
  579 of 801 samples count 723, dominated by runs [−50, −4] and [53/2, 50] that
  both hit the sweep bounds and extend to at least |s| = 1000. The charted
  [9/32, 35/32] was a fragmented zone near the base point. Its point at infinity
  counts 717. Still open: where the two huge runs actually end.
* **Component counts for other totals** — 725 has 6 arcs, 723 has 13, by the
  same orbit dedup. Unmeasured for totals below 723 and for other n.
* **Types at n = 2's edge arc, and at 183** — unmeasured. Path: per-label sweeps
  once a tangent is in hand.
* **The two 67s' Jacobian rank** — would upgrade their isolation from a
  codimension heuristic to a computation. Representatives are in
  `MAXIMISERS.md`; the obstacle is that the walls must be differentiated in
  ℚ(√2) and ℚ(√5) rather than ℚ.
* **Lemma B** — max(3) = 67 reduces to one two-rotation statement, g(13,13) = 16
  and g ≤ 14 otherwise, measured but unproved. Two attack routes are in the
  ledger.
