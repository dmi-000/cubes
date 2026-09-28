# Current results

**What this file is.** What the project believes now, each claim tagged by how firmly it is
established and citing the ledger entry it rests on today. It is organised by strength, not by
date. The same picture organised by number of cubes is [`LEVELS.md`](LEVELS.md); open questions
and what has been ruled out are in [`OPEN_QUESTIONS.md`](OPEN_QUESTIONS.md); how each result was
reached, and what was believed on the way, is in the ledger, [`LEDGER.md`](LEDGER.md), and told as
a story in [`JOURNEY.md`](JOURNEY.md). Which data files are current: [`DATA_MANIFEST.md`](DATA_MANIFEST.md).

*Rebuilt 2026-09-27 from the version last updated 2026-09-12, which the published copy holds.
Pruned in the rebuild, and still true: the wall catalogues and ruling statistics (in
[`MAXIMISER_TAXONOMY.md`](MAXIMISER_TAXONOMY.md) and [P57](LEDGER.md#p57)–[P112](LEDGER.md#p112)),
the chamber-fill arithmetic ([P151](LEDGER.md#p151)), and per-search enumeration detail (the
ledger). Dropped as superseded: the second-order isolation census and every 2785-era figure.
This is a current-knowledge document ([`DOCUMENTS.md`](DOCUMENTS.md)): corrected by rewriting,
and every bracketed citation is tracked by `src/claim_deps.py`.*

| tag | meaning |
|---|---|
| **PROVED** | a theorem, with the proof written down and its hypotheses stated |
| **PROVED IF** | a proved implication from a NAMED hypothesis, which is graded separately in §4 |
| **PROOF GAP** | stated as proved, but the proof has a hole; it may well be true |
| **VERIFIED** | an exact count of a specific configuration, agreed by two independent engines, or an exact measurement |
| **EXHAUSTED** | a search complete over a stated family, not a sample |
| **STRONG CONJECTURE** | not proved; supported by evidence aimed at breaking it, or reduced to a single clean claim |
| **WEAK CONJECTURE** | not proved; supported only by samples, or by tests that could not reach a known kind of counterexample |
| **HOPE** | wanted, with no support, or with evidence against |
| **OBSERVED** | a pattern noticed and not yet tested beyond the data that produced it |

The distinction between STRONG and WEAK matters here more than anywhere: three statements that
were maxima over directed searches have been refuted this month, each by a compound from outside
the searched family ([P373](LEDGER.md#p373), [P389](LEDGER.md#p389)).

---

## 1. The problem

Given *n* congruent unit cubes sharing a centre, each independently rotated, count the bounded
regions their surfaces cut space into. A region is a connected component of constant
**cube-containment**: you cross a real face iff the set of containing cubes changes. Crossing the
*infinite extension* of a face plane, where that cube is absent, does not split a region. Every
count uses this definition and exact arithmetic; no floating point enters any decision.

## 2. Proved

- **max(2) = 13**, for any two convex cells with ≤ 6 faces each. PROVED
  ([`max2_report.md`](max2_report.md)). A∖B is a union of at most 6 convex pieces, likewise B∖A,
  plus one core. Equivalently, by Euler on the intersection curve, `d₁ ≤ 12` (`METHODS.md` §11).
- **max(3) = 67**, for three concentric convex ≤ 6-facet cells meeting pairwise transversally, an
  open dense set containing both maximisers. PROVED ([`PROOF_67.md`](PROOF_67.md),
  [`PROOF_STEP_T.md`](PROOF_STEP_T.md)): `d₃ ≤ 1`, `d₂ ≤ 18`, `d₁ ≤ 48`, the last with the
  triple-point weight ≤ 32 in full generality, degenerate triple points included. Remaining
  caveat: tangential rather than transversal contact, a higher-codimension case. An elementary
  second route: the singleton term obeys `s ≤ a + b + m − 2` by Mayer–Vietoris and Alexander
  duality, giving `max(3) ≤ 1 + 18 + 3·16` with no measured input ([P110](LEDGER.md#p110)).
- **The per-pair and per-triple caps, at every n.** PROVED. Each pair contributes two-body weight
  `E_i = EE_i + 2·SC2_i ≤ 10` ([P237](LEDGER.md#p237), from max(2) = 13), and each triple a
  triple-point weight `≤ 32` (PROOF_67 Lemma 1a with PROOF_STEP_T). Hence the two-body total
  `≤ 10·C(n,2)` and the triple total `≤ 32·C(n,3)`.
- **d₁ ≤ 108·C(n,3) + 10·C(n,2) + 2**, for every n and every configuration. PROVED
  ([P237](LEDGER.md#p237)): 494 at n = 4, 2 312 at n = 6.
- **d_{n−1} ≤ 6n**, the l = 1 ceiling law. PROVED ([P24](LEDGER.md#p24), [P33](LEDGER.md#p33)):
  the radial envelope has local minima only at the 6n face centres.
- **Theorem S.** For n ≥ 3, `Σ over (n−1)-subsets T of d_{n−2}(T) ≤ 6n(n−2) + d_{n−1}(S)`.
  PROVED ([P266](LEDGER.md#p266), [`PROOF_SUBSET.md`](PROOF_SUBSET.md)); exactly tight at the
  183 record (72 = 72). It does NOT by itself give `max(4) ≤ 195`: that conversion needs links
  still open ([OQ 32](OPEN_QUESTIONS.md), [OQ 30](OPEN_QUESTIONS.md)).
- **The counting identity.** `TOTAL = 1 + L + Σ holes + ½ Σ_v excess(v)`, exact
  ([P327](LEDGER.md#p327), [P328](LEDGER.md#p328)): every region is paid for by degree excess at a
  vertex, and every triple point is spent on two consecutive levels. Its level form,
  `d_ℓ = E_ℓ − V_ℓ + c_ℓ + 1` ([P243](LEDGER.md#p243)), stands. **The named-signature shortcut
  `TOTAL = 7 + T + B − Q4` at n = 4 is a bound, not this identity**, and not even a bound for
  compounds with `(1,1,2)`, `(1,2,2)` or `(2,2,2)` vertices ([P374](LEDGER.md#p374)).
- **The merge law.** `EE = Σ_pairs EE_pair − Σ_v C(m(v), 2)` over vertices where several pairs'
  crossings merge; verified 60 of 60 ([P372](LEDGER.md#p372)). Edge-edge walls are degree-4
  forms in one relative quaternion (144 of them); triple-budget walls are bidegree (2,2) in two
  (54 of 54) ([P372](LEDGER.md#p372)).
- **The facet-centre lemma.** Every facet centre lies inside every other cube, so depth never
  increases along a ray from it. PROVED ([P311](LEDGER.md#p311)).
- **The one-cube increment** is bounded by the cell count of the arrangement the other cubes trace
  on the added cube's surface: `Δ_j ≤ B_j = 1 + c + Σ_v (deg(v)/2 − 1)`. PROVED
  ([P56](LEDGER.md#p56)); measured slack 1.00–1.11.
- **Every wall splits over ℚ.** PROVED ([P104](LEDGER.md#p104)): `det(Q) = (|p|² − 1)²` for a
  four-cube wall through triple point p, `16(|m × q|² − 2|m|²)²` for a three-cube wall, squares for
  every rational base datum.
- **727's 36-condition coincidence pattern is realised at one point and is unaugmentable.** PROVED
  by elimination ([P47](LEDGER.md#p47)). The COUNT is not isolated there: see §3.
- **PROVED IF `c_ℓ ≤ 2` on every level: `max(n) ≤ 1 + 32·C(n,3) + 10·C(n,2) + 3(n−1)`**, which is
  198 at n = 4, 433 at n = 5, … 4 318 at n = 10, with the records at a steady 90–92 % of it
  ([P258](LEDGER.md#p258), [P326](LEDGER.md#p326)). The hypothesis is graded in §4.
- **PROOF GAP: `max(n) ≤ 953` at n = 4**, 3 377 at n = 5, … 104 207 at n = 10
  ([P249](LEDGER.md#p249)), the sum of per-depth bounds. The bound for depths ≥ 2
  ([P243](LEDGER.md#p243)) omits two-body vertices, which do occur there
  ([P274](LEDGER.md#p274)). Almost certainly true, since it exceeds every measurement fivefold, and
  the repair (a two-body term per depth, as [P237] supplied at depth 1) looks mechanical. **Until
  it is made, no upper bound on max(n) for n ≥ 4 holds without a hypothesis.**

## 3. Measured

**The records**, with exact representatives and reproducing commands in
[`MAXIMISERS.md`](MAXIMISERS.md):

| n | best known | status |
|---|---|---|
| 2 | 13 | PROVED maximum ([`max2_report.md`](max2_report.md)) |
| 3 | 67 | PROVED maximum ([`PROOF_67.md`](PROOF_67.md)); two classes, octahedral in ℚ(√2) and golden in ℚ(√5) |
| 4 | 183 | VERIFIED; two classes ([`n4_search_report.md`](n4_search_report.md), [P133](LEDGER.md#p133)) |
| 5 | 393 | VERIFIED; the "393 base" ([P16](LEDGER.md#p16)) |
| 6 | 727 | VERIFIED; the base plus one cube ([P46](LEDGER.md#p46)) |
| 7 | 1217 | VERIFIED; the 727 six plus one ([P46](LEDGER.md#p46)) |
| 8 | 1895 | VERIFIED; the 1217 seven plus one ([P101](LEDGER.md#p101)) |
| 9 | 2787 | VERIFIED; the 1217 seven plus TWO new cubes ([P198](LEDGER.md#p198), [P218](LEDGER.md#p218)) |
| 10 | 3925 | VERIFIED; 2787's nine in its ORIGINAL representative plus one ([P200](LEDGER.md#p200), [P285](LEDGER.md#p285)) |

From n = 4 on these are lower bounds found by construction and search, not claimed maxima (§4).
At n = 10 the same added cube gives 3921 on the simplified n = 9 representative: two members of
one plateau, identical in count and depth profile, are not interchangeable as foundations
([P285](LEDGER.md#p285)).

**The shape of the set where each best count holds** (detail per level in [`LEVELS.md`](LEVELS.md)):

- **n = 2**: in class space a SINGLE arc, open at the identity, running along body-diagonal
  rotations to 60° and on along edge rotations to a closed, irrational end at the 90° edge
  rotation; every rational 13 up to height 5, on any axis, lies on it ([P390](LEDGER.md#p390)).
  The octahedral 67's pairs are its closed end, the golden 67's an interior point. Only counts 1,
  4, 5, 9, 13 occur, generic 4 ([P69](LEDGER.md#p69)).
- **n = 3**: two isolated points. VERIFIED by enumerating every face of each local wall
  arrangement, 728 and 2 196 faces, none reaching 67 ([P118](LEDGER.md#p118)). Each 67 lies on a
  curve preserving its contacts, but the count changes on both sides at once
  ([P382](LEDGER.md#p382)). The two sit differently: the octahedral 67 lies 14° inside the
  uniform 55 region, the golden 67 exactly ON the 55/43 wall ([P291](LEDGER.md#p291)).
- **n = 4**: each of the two 183 classes lies on its own arc; the tower's arc has length 0.6873,
  and the arcs are distinct ([P378](LEDGER.md#p378), [P380](LEDGER.md#p380)).
- **n = 5**: tangent dimension 1; the plateau itself has not been measured
  ([P381](LEDGER.md#p381)).
- **n = 6**: one-dimensional; the record is a node where exactly two branches cross, D1 and D2 at
  4.51°, arcs B and C being those branches again under the base's C₃ symmetry, and arc A a separate
  piece ([P391](LEDGER.md#p391)); the record is a special point, not a
  special arc ([P293](LEDGER.md#p293), [P306](LEDGER.md#p306)). Nine special points are six
  compounds ([P294](LEDGER.md#p294)). The 727s are uncountably many non-congruent compounds, in
  every quadratic field tested as well as ℚ ([P79](LEDGER.md#p79), [P80](LEDGER.md#p80)). Arc
  D's extent is solved exactly, `s ∈ (−2/19, 10695/1007 − 7√2248773/1007)`, the first plateau
  boundary carried from bracket to wall to polynomial to root ([P296](LEDGER.md#p296)).
- **n = 7**: two-dimensional, two sheets crossing along the fibre over the record, the n = 6 node
  carried up ([P393](LEDGER.md#p393)). Each sheet is a curved triangle with three walls, the same
  three on both: the branch's lower 727 wall, a flat fibre wall, and one curved wall of degree 4
  ([P301](LEDGER.md#p301), [P394](LEDGER.md#p394)). The earlier "pentagon" was a grid's box.
- **n = 8**: three-dimensional, a polytope with 38 vertices and 72 facets, inradius 0.0595,
  circumradius 0.859 ([P383](LEDGER.md#p383), [P385](LEDGER.md#p385)).
- **n = 9**: tangent dimension 4, one direction walked ([`CONTINUUM_MAP.md`](CONTINUUM_MAP.md), Map 4).
- **n = 10**: lineality 6 from its 480 tight conditions ([P300](LEDGER.md#p300)); the plateau has
  not been walked.
<!-- reviewed 2026-09-27: P118 cited for its isolation verdict, which stands; P70 for the mirror-plane structure P76 left standing -->

**Tangent dimension equals plateau dimension** wherever both are measured, n = 4, 6, 7, 8, and
n = 3 is the exception, tangent 1 and plateau 0 ([P381](LEDGER.md#p381), [P382](LEDGER.md#p382),
[P383](LEDGER.md#p383)). The lineality column of the older rank computation, 1, 1, 2, 3 at
n = 5..8, is the same quantity from a different wall list ([P122](LEDGER.md#p122),
[P124](LEDGER.md#p124)).
<!-- reviewed 2026-09-27: P122 cited for its lineality numbers, which stand -->

**Plateau boundaries partly carry up the tower.** Two of the three walls bounding the
D1 sheet of the 1217 plateau recur at n = 8 and n = 9 and cost exactly 4 regions to cross each time; the third is cut
by a new wall and contracts about fivefold ([P303](LEDGER.md#p303)).

**Other exact measurements.**
- The two-body weight on level 1 is 48 at the n = 4 record and **60 at the golden 177**, the
  proved cap, all on the outer surface ([P389](LEDGER.md#p389)).
- `c_ℓ` is the wall graph's component count (43 of 43, [P312](LEDGER.md#p312)); `c > 1` has been
  seen only at level 1, zero times in 3 382 deeper level-instances ([P319](LEDGER.md#p319)); a
  change in `c` is a pure reconnection, `ΔV = ΔE = 0` ([P321](LEDGER.md#p321)).
- Every record above n = 4 carries exactly 12 quadruple points ([P315](LEDGER.md#p315)).
- Records buy 13–28 % of their regions with degenerate vertices, 26 % at n = 4
  ([P327](LEDGER.md#p327)).
- Edge-edge contact strata have codimension 0 at `EE = 0`, 1 at `EE = 4`, and 2 at 6, 8 and 10
  (exact Jacobian rank, [P376](LEDGER.md#p376)).
- Chamber counts of the coincidence arrangement near the records: 1 712 (183), 74 544 (393),
  4 621 728 (727), and 727's is exactly 62 times 393's ([P148](LEDGER.md#p148),
  [P152](LEDGER.md#p152), [P153](LEDGER.md#p153)). These are chambers of the COINCIDENCE walls,
  which do not bound the count on their own ([P305](LEDGER.md#p305)).

## 4. Not proved, graded

| claim | grade | evidence, and what it rests on |
|---|---|---|
| `max(4) ≤ 953` | PROOF GAP | §2 |
| `c_ℓ ≤ 2` on every level ([OQ 30](OPEN_QUESTIONS.md)) | **STRONG CONJECTURE** | never violated in about 3 700 level-instances including a directed attempt to break it ([P325](LEDGER.md#p325)); reduced to one connectivity claim about the antipodal quotient ([P259](LEDGER.md#p259)). Gives `max(4) ≤ 198` |
| `max(4) = 183` | **WEAK CONJECTURE** | never exceeded, and reached by 7.3 % of wide-perturbation restarts ([P131](LEDGER.md#p131)); but three reductions to a few named statements have failed ([P373](LEDGER.md#p373) twice, [P389](LEDGER.md#p389)), and no argument now connects 183 to any bound below 198 |
| W: `W₀ ≤ 84` at n = 4 ([OQ 32](OPEN_QUESTIONS.md)) | **WEAK CONJECTURE** | 0 violations in 247 blind configurations, attained at the record ([P275](LEDGER.md#p275)); all rational, the blind spot that let T stand |
| C: `c₁ = c₂ = 1` at the maximiser | **WEAK CONJECTURE** | `c = 2` occurs on ordinary configurations ([P269](LEDGER.md#p269)); directed climbing under `c = 2` stalled far below the record ([P270](LEDGER.md#p270)) |
| given W and C, `max(4) ≤ 195` | PROVED IF | the anatomy `d₁ = W₀/2 + T + c₁ + 1` ([P272](LEDGER.md#p272)) with the proved `T ≤ 60`. The version with `T ≤ 48`, which gave 183, fails because T is false ([P389](LEDGER.md#p389)) |
| the ceiling law for l ≥ 2, `C(l,n) = (12l−6)n − 2(l²−1)` | **WEAK CONJECTURE** | never exceeded in about a million sampled configurations; proved only for l = 1. Its caps provably cannot all be attained together ([P258](LEDGER.md#p258)) |
| `max(6) ≤ 729` | **WEAK CONJECTURE** | the envelope bound on the 393 base, whose constant 336 is still measured, not derived ([P56](LEDGER.md#p56)) |
| the records at n ≥ 5 are maxima | not conjectured | lower bounds; no search above n = 4 has been complete over more than a stated family (§6) |
| no third 67 exists anywhere | **WEAK CONJECTURE** | isolation is local ([P118](LEDGER.md#p118)); nothing rules out a 67 elsewhere. Theorem R's "the n = 3 maximum needs irrational coordinates" ([P26](LEDGER.md#p26)) depends on it |
| the frustration deficit is `6(n−3)(n−2)` | **HOPE** | a three-point fit, two of the points records rather than proved maxima; not derived anywhere in the ledger. The frustration PRINCIPLE, that levels cannot maximise independently, is well attested ([P17](LEDGER.md#p17), [P258](LEDGER.md#p258)) |

**Refuted this month, and what each took with it.** Hypothesis T, `T ≤ 48` at n = 4: false, the
golden has 60 ([P389](LEDGER.md#p389)), and with it `max(4) = 183` lost its conditional proof.
`EE ≤ 36` at `B = 128` and `EE + B ≤ 164`: false ([P373](LEDGER.md#p373)).

## 5. Structure

- **What the records do** ([P364](LEDGER.md#p364)): one hub cube sharing an axis with up to four
  others, every other cube sharing at most one. A cube with one shared axis keeps a free rotation
  and can dodge a forced coincidence; fully pinned cubes cannot ([P358](LEDGER.md#p358)). Above
  n = 5 the records add cubes with no sharing at all.
- **Subset-optimality does not give the maximum.** The golden 177, UC09's 4-subset, has every
  subset at its proved maximum and still loses to 183, because complete corner-sharing forces 18
  four-fold points ([P370](LEDGER.md#p370)). Complete corner-sharing is sub-maximal at both sizes
  where it exists, n = 4 and n = 5 ([P363](LEDGER.md#p363)).
- **The tower nests, by count, at every level except n = 3.** Each record from 183 to 1895
  contains the one below as a subset ([P44](LEDGER.md#p44), made exhaustive on those records by
  [P111](LEDGER.md#p111)), and 3921's best 9-subset is 2787, whose best 8-subset is 1895
  ([P198](LEDGER.md#p198)), although 2787 replaced the recorded 1895's eighth cube. The tower's
  183 is cubes {0, 1, 2, 4} of the 393 base, and every record from n = 4 to 8 contains exactly
  ONE 4-subset counting 183 ([P283](LEDGER.md#p283)). The break at n = 3: the best triple inside
  any rational record is 63, since 67 needs irrational coordinates ([P126](LEDGER.md#p126)).
- **Extend from the deepest compatible level.** Because 67 is irrational, one-cube extension from
  n = 3 cannot reach 183, while two-cube extension from a 13-pair can ([P126](LEDGER.md#p126)).
  1895 has two non-congruent 1217-subsets, separated only by their triple counts.
- **Irrationality does no work at n = 6.** An irrational 727 and its rational shadow are the same
  combinatorial object at nearby parameters of one rational family: two edge-edge conditions are
  rational planes meeting in a rational line, and a corner-on-face quadric's root on that line
  supplies the irrationality ([P60](LEDGER.md#p60), [P61](LEDGER.md#p61)).
- **Walls.** Coincidence conditions are quadrics in the free cube's Cayley coordinates, so three
  walls meet in at most 8 points ([P57](LEDGER.md#p57)). Edge-edge conditions factor into pairs of
  rational planes; corner-on-face conditions are irreducible. Every wall is doubly ruled; the two
  rulings through a rational point are both rational or a conjugate irrational pair, never one of
  each, and all 63 432 found were rational ([P103](LEDGER.md#p103)). The count varies along a
  ruling. Corner-corner coincidence and edge-in-face are codimension 2, not walls.
- **The coincidence walls do not bound the count by themselves.** Crossing one often leaves the
  count unchanged (13 of 21 on one ray at 727, [P304](LEDGER.md#p304)), and a count can change
  where no coincidence wall is crossed. What changes it there is **unknown**: the four-plane
  concurrences once proposed lie outside the compound ([P323](LEDGER.md#p323)).
- **Constraint-guided enumeration reaches irrational space; sampling does not.** Two families were
  solved rather than sampled at n = 4: two 67-triples caps at 177, reproducing the golden
  ([P131](LEDGER.md#p131)), and irrational completions of one rational base per target cap at 173
  (n = 4) and 377 (n = 5) ([P138](LEDGER.md#p138)). Each is a result about its base, not about
  irrational compounds in general.
<!-- reviewed 2026-09-27: P304 cited for its surviving 13-of-21 measurement; P60 for the rational-shadow mechanism P61 left standing -->

## 6. What searching has covered

- **Extension beats native search.** Every record from n = 6 up was found by extending the one
  below; improvements propagate in both directions ([P46](LEDGER.md#p46)).
- **Filtering before counting pays.** Keeping candidates whose maximum plane concurrence is 6, 8
  or 9 skips 69.6 % of them, loses none counting ≥ 170, and nets 1.81× on held-out data
  ([P231](LEDGER.md#p231)). It is a search filter, not a cause: those concurrence points lie
  outside the compound ([P331](LEDGER.md#p331)).
- **Menu shape matters more than size.** 727's sixth cube was inside the old norm bound all along;
  log-uniform component heights to 512 found it at once ([P46](LEDGER.md#p46)).
- **Three-wall intersection** is the best search method found, about 30 times the hit rate of
  random menus ([P48](LEDGER.md#p48)): the family is 134 784 linear systems giving 2 733
  configurations, EXHAUSTED in four minutes, maximum 727 ([P49](LEDGER.md#p49)).
- **Nothing above 727 at n = 6** in: random menus (100 000 sixth cubes), swap-completion from every
  five-cube base, the worst-subset climb, core-and-clique construction, the exhausted three-wall
  family, pure corner-wall triples (best 719), the rational mixed family (best 725), and 508 818
  irrational configurations across the fields the engine admits ([P59](LEDGER.md#p59),
  [P79](LEDGER.md#p79)).
- **n = 4 by restarts**: 55 wide-perturbation restarts, 264 794 engine calls, 183 four times and
  never exceeded ([P131](LEDGER.md#p131)); 5 136 compounds from the region that refuted the `EE`
  ceilings, best 173 ([P375](LEDGER.md#p375)).

## 7. Beliefs overturned

Listed only where knowing the old belief is dead is itself useful. The history of each is in the
ledger; the full list of the project's corrections is in [`FAILURE_MODES.md`](FAILURE_MODES.md).

| once believed | now |
|---|---|
| the records are isolated points | from n = 4 they lie on plateaus of dimension 1, 1, 2, 3 at n = 4, 6, 7, 8 ([P378](LEDGER.md#p378), [P306](LEDGER.md#p306), [P301](LEDGER.md#p301), [P383](LEDGER.md#p383)); only the n = 3 maxima are isolated |
| 727 is isolated on the 393 base | its coincidence pattern is; the count holds along a line through it ([P293](LEDGER.md#p293)) |
| `max(4) = 183` follows from T, W and C | T is false ([P389](LEDGER.md#p389)) |
| `max(4) ≤ 953` is proved | proof gap ([P274](LEDGER.md#p274)) |
| the n = 8 plateau is 2-dimensional | 3 ([P383](LEDGER.md#p383)) |
| region counts are always odd | only `TOTAL ≡ (self-antipodal regions) mod 2`; even counts occur, and 184 is not excluded ([P375](LEDGER.md#p375)) |
| four face planes through a point are a second wall family | those points lie outside the compound ([P323](LEDGER.md#p323)) |
| `Σ EE ≤ 6·C(n,2)` | exceeded at every n from 2 to 6 ([P330](LEDGER.md#p330)) |
| the plane-incidence signature predicts the count | it measured the quaternion spelling: rows were read as normals ([P227](LEDGER.md#p227)) |
| UC09's subsets are the maxima up to n = 5 | only up to n = 3 ([P16](LEDGER.md#p16), [P370](LEDGER.md#p370)) |
| the n = 2 maximum is rigid | it is one arc in class space ([P44](LEDGER.md#p44), [P390](LEDGER.md#p390)) |
| the n = 2 maximum is two unrelated arcs plus isolated classes | the arcs join end to end and the "extra classes" lie on them ([P390](LEDGER.md#p390)) |
| off-centred cubes and general hexahedra beat the records | an artefact of counting cells of the infinite planes ([P38](LEDGER.md#p38)) |
