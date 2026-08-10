# Methods that work, and why

The companion to [`FAILURE_MODES.md`](FAILURE_MODES.md). That file collects what
went wrong, organised by symptom; this one collects what to DO, each entry with
the measurement that earned it. Nothing here is a rule of thumb — every item
below was wrong in some earlier form and was corrected by a specific run.

---

## 1. Solve the line; do not sample it

The count and the per-label profile are constant BETWEEN consecutive wall
crossings on a line. So: build the base's W3/W4 catalogue, solve
`wall_params.w4_params` (a quadric in the line parameter) and `w3_params` (a
quartic) for every root, and evaluate the engine ONCE strictly between each
consecutive pair.

You get the exact chamber decomposition: ends named as roots rather than
bracketed, no chamber missed however narrow, and a dip distinguished from an end
by looking past it. A sampled chamber count is a lower bound; this one is not —
n = 7's 1217 has **exactly** 7 types, the 723 loop **exactly** 11.

`incidence2.base_catalogue` is hard-wired to the five-cube 393 base;
parametrising `FIVE` serves any base, which is what the n = 7 and n = 8 lines
need.

**Two limits.** The catalogue bounds triple points at |p| ≤ 4, so a wall from a
point outside that ball is missed. And a rational strictly between two roots
10⁻⁷ apart overflows even the wide engine — report those chambers as
unevaluated, never as count changes. Across six lines and 20 308 chambers, 8.5%
were unevaluable that way.

## 2. Report the MAXIMUM over a line, not the indicator of one value

This is how the n = 8 record was missed for eleven months. The sweep recorded
where 1891 held — "[0, 3/32] and again on [15/64, 3/8]" — so 1895, sitting in
the gap between those two intervals and inside the window already covered, read
as a dropout instead of a rise. **A plateau sweep must report the maximum over
the line.** Re-reading all six catalogue lines this way (20 308 chambers) found
no further omission, so the loss was one line even though the habit was general.

## 3. Decide wrapping at the point at infinity, in one call

A line's point at infinity is the half-turn about its direction, `(0, d)`. One
engine call there settles whether a family wraps; extending a sweep can only ever
suggest it. Of seven families tested, two wrap — n = 2's body-diagonal locus and
the n = 6 723 stratum, whose two "huge runs" turned out to be one arc joined
through infinity. Both wrapping families run along a symmetry axis of the base;
all five that terminate run in general directions.

## 4. Choose the control that is HARD for the method, not the one to hand

Three attempts at one direction scan, two of them void, and the controls passed
every time while the method was broken. The controls used — n = 2's (1,1,0) and
(1,1,1), 723's (1,1,1) — are the three easiest tangents in the project: they are
axis-parallel, so every chart agrees on them, AND they are the smallest integer
triples there are, so they sit inside any search set. Two independent defects
were invisible to them.

Rank the available controls by how far they sit from the easy case along the axis
the method could be wrong about, and use the extreme one:

    (1,1,1) at n=2 or 723    trivial: axis-parallel AND minimal
    (1,1,0) at n=2 mirror    axis-parallel
    (1,1,-4) on 727 arc B    general position, range 4
    (1,-3,-6) on 727 arc A   general position, range 6
    the n=6 record           two tangents at a node

Full account in `FAILURE_MODES.md` §13a.

## 5. A zero is only as good as the search set that produced it

Two questions to answer before believing any "0 of N":

* **Which chart?** A direction that is an integer triple in one chart is not one
  in another. Every tangent this project has verified — (1,1,0), (1,1,1),
  (1,−3,−6), (1,1,−4) — is integral in the CAYLEY chart and no other.
* **What range?** |uᵢ| ≤ 3 does not contain (1,−3,−6) or (1,1,−4), so two of the
  four known tangents were never candidates. |uᵢ| ≤ 6 contains both.

The working protocol: Cayley chart, 1 730 primitive directions |uᵢ| ≤ 6, three
ε scales, control 727 arc A. It returns ±(1,−3,−6) there, **2 of 1 730**, and
nothing else — that specificity is what makes its zeros elsewhere worth
something. A cube with w = 0 is at Cayley infinity and cannot be scanned at all;
say so rather than counting it as covered.

## 6. Coincidence count is a certificate, not a compass

Real edge-edge crossings — two edges from different cubes generically miss, so
each is a codimension-1 coincidence — track the region count closely and rank
candidates wrongly.

* **Globally it fails**: 723 carries 180 crossings and loses to 727's 150.
* **Locally it is nearly a function and still fails.** Over 290 directions from
  the n = 4 183, each region value has exactly one crossing value — but the map
  inverts once, at 78 crossings → 171 regions against 66 → 173. A local climb on
  coincidences picks 78 and loses two regions.
* **What holds**: at a maximiser both are strict local maxima. So "not a local
  coincidence maximum" rules a candidate out, while "more coincidences" never
  rules one in.
* **The extreme case**: the two n = 3 maximisers carry **30 and 72** crossings
  and both count exactly **67**. Coincidence structure and region count are not
  even close to determining one another across strata.

## 7. Every boundary is a coincidence boundary; most coincidences are not boundaries

W3 + W4 bracket every chamber wall observed on every 727 arc — 39 of 39 — while
only about a quarter of the interior crossings change anything. The converse
direction was assumed rather than tested by the chamber decompositions, which
evaluate one point per inter-root interval and so cannot see a wall inside one.
Tested directly (2026-08-06): 40 small-denominator samples inside each of the 12
widest chambers on the 723 line, **480 evaluations, every chamber single-valued**.
No boundary was found that the coincidence catalogue does not carry.

**But edge-edge crossings alone are NOT a complete boundary detector.** At the
lower end of the n = 9 continuum the count steps 2781 -> 2785 between k = 439/8
and k = 55 while the edge-edge crossing count is **294 on both sides**,
unchanged. The wall there is of a type the edge-edge count does not register — a
face-plane/triple-point event rather than an edge-edge one — so §6's "boundary
points are coincidence spikes" holds for the boundaries examined at n <= 8 and
must not be read as a test that can certify the absence of a wall. It also
breaks, at this scale, the local single-valued map from crossings to regions
found at n = 4: here 294 crossings corresponds to both 2781 and 2785.

## 8. Tell chamber values from wall values

On the lines examined, **every chamber count is ≡ 3 (mod 4) and the values ≡ 1
(mod 4) occur only ON walls** — 725, 717 and 705 never appear on an open
interval. A count ≡ 1 (mod 4) therefore means the configuration is sitting on a
wall rather than in a chamber, which is exactly what the 717 "dips" were. Not
universal: n = 4's neighbourhood shows chambers at both residues. Check it per
line before relying on it.

Related: a boundary point carries MORE coincidences than either side of it —
10 → 24 at the n = 2 edge-arc ends, 144 → 162 at 727 arc A's, 24 → 48 at the
diagonal punctures, 138 → 144 → 150 across an arc and its node. An arc ends by
running into a denser stratum, never by the geometry running out.

## 9. Search the pair-type multiset, not the rotation space

Crossings per cube PAIR are quantised: among the rational maximisers they take
only 24, 6 and 0, corresponding exactly to the pair labels 13, 9 and 4. (The
quantisation is real; the value set is not closed — the octahedral 67 is built
from 13-pairs carrying **10**, so a pair label does not fix a crossing count.)
Along the top of the tower the 9-pair count is frozen at nine:

    727    4x13   9x9    2x4
    1217   6x13   9x9    6x4
    1895   8x13   9x9   11x4

so both extensions added exactly **two 13-pairs, zero 9-pairs**, and 4-pairs for
the rest. Testing a candidate's pair types is an incidence test, far cheaper than
an arrangement count, so it prescreens at a rate region counting cannot reach.
Two data points: a heuristic to test, not a law.

**TESTED — and the answer depends on where you test it.** Read both parts.

**Within the near-symmetry family the rule DOES hold** (`n9_hunt2.py`, 178 000
candidates of the form k·S + P):

    0x13/1x9   n=71678  mean 2655.9   max 2779
    0x13/0x9   n=52114  mean 2752.1   max 2775
    3x13/0x9   n=16354  mean 2768.7   max 2777
    2x13/0x9   n=16454  mean 2775.7   max 2785    <- the rule, best mean AND best max

**On random quaternions it does not.** `n9_hunt.py` sampled ~1M
ninth cubes against the 1895 eight and counted all three neighbouring buckets
rather than only the hypothesis:

    1x13/0x9   n=761    mean 2726.4   max 2771
    2x13/0x9   n=3380   mean ~2729    max 2781      <- the rule
    3x13/0x9   n=930    mean 2732.0   max 2777

Means within 8 of each other and the rule bucket not the best of them. The three
profiles are also near-equally COMMON (2362 / 2322 / 2299 per million).

**So the rule is conditional, not absolute**: it discriminates once you are in
the productive stratum and says nothing outside it. The first test looked like a
refutation because it was run on a sample where almost nothing was any good —
comparing buckets inside a bad neighbourhood measures the neighbourhood, not the
rule. A conditional claim needs its condition sampled before it can be judged.

**What predicts a good extension instead: proximity to a cube symmetry.**
19 of the 20 best ninth cubes are `k*S + P` with S one of the 24 cube-symmetry
quaternions and **|P| = 1** — one unit step off a scaled symmetry:

    2781  (21, 22, 21, -21)  = 21*(1,1,1,-1) + (0,1,0,0)
    2781  (14,-14,-14,-15)   = 14*(1,-1,-1,-1) + (0,0,0,-1)
    2781  (74, 1, 0, -75)    = 74*(1,0,0,-1) + (0,1,0,-1)
    2781  (1, -91, 1, 1)     = 91*(0,-1,0,0) + (1,0,1,1)

Near a symmetry the new cube nearly coincides with a copy already present, which
is the mechanism that puts n = 2's 13 just off the body diagonal: many thin slabs
rather than few fat ones. `n9_hunt2.py` enumerates that family directly
(24 symmetries x k <= 400 x |P| <= 1, ~768 000 before dedup) instead of waiting
for random sampling to land in it.

**The methodological point outlives the rule.** v1 as first written screened only
the hypothesis, so it could find a record but could not falsify the rule — the
same shape as choosing a control for convenience (section 4). Adding the two
neighbouring buckets cost almost nothing, because the pair screen was the
bottleneck rather than the arrangement count, and it turned a confirmation
exercise into a measurement that overturned the claim.

## 10. Prune by the SUBSET SPECTRUM, not by subset maximality

Every (n−1)-subset of an n-record is *near*-maximal; almost none is maximal. The
full spectrum, dropping each cube in turn:

    2785 (n=9)  ->  1895, 1887, 1887, 1883, 1875, 1873, 1873, 1869, 1867
    1895 (n=8)  ->  1217, 1217, 1209, 1205, 1203, 1201, 1201, 1197

So the strong constraint — *all* (n−1)-subsets are known (n−1) configurations —
is false: only one subset of the 2785 reaches 1895, and two of the 1895 reach
1217. The rest are ordinary compounds nobody has catalogued.

**The weak form is real and quantitative.** Every subset lands in a narrow band
just under the level below:

    worst 8-subset of 2785 = 1867 = 98.5% of 1895
    worst 7-subset of 1895 = 1197 = 98.4% of 1217

Two levels agreeing to a tenth of a percent. As a pruning rule: a candidate
n-compound whose WORST (n−1)-subset falls below roughly 98% of the (n−1) record
is not a record. That is n cheap counts at level n−1 in place of one expensive
count at level n, and it prunes on the worst subset rather than the best — the
opposite of how extension search is usually organised, which only ever looks at
the subset it started from.

Two data points; test it before trusting the 98%.

## 11. The depth profile IS the face vector of the boundary spheres

For two convex bodies A, B the depth profile is not merely correlated with the
incidence data — it is an Euler characteristic of it, and the relation can be
derived rather than fitted.

**The object.** Γ = ∂A ∩ ∂B is a graph: its **vertices** are edge-face
incidences, its **edges** the segments (face i of A) ∩ (face j of B), and it has
**c** connected components. Γ embeds in ∂A ≅ S² and in ∂B ≅ S², so Euler gives
the same face count for each:

    F = E − V + c + 1

**The derivation.** Every face of Γ on ∂A lies inside or outside B; write I_A and
O_A for the counts, so I_A + O_A = F, and likewise on ∂B.

* ∂(A∩B) is a sphere tiled by the INSIDE faces of both, so **I_A + I_B = F**.
* ∂(A∪B) is a sphere too (A∪B is a ball when A∩B ≠ ∅), tiled by the OUTSIDE
  faces of both, so **O_A + O_B = F**.
* Each component of A∖B carries one outside face of ∂A, and likewise for B∖A, so

      d1 = O_A + O_B = F     and     d2 = 1  (A∩B is convex, hence connected)

So the depth-1 count is literally the face count of the union's boundary sphere,
and the total is F + 1.

**Both failure modes follow, and each is checkable before trusting the answer.**

* **Every vertex of Γ has EVEN degree** — it is a union of closed curves,
  crossing at 4 or 6. An odd degree means the extracted graph is not Γ (a segment
  lost its continuation across a face boundary), so Euler is being applied to the
  wrong object.
* **F ≤ 12 always.** A∖B lies in the union of A's six face-slabs, so O_A ≤ 6, and
  likewise O_B ≤ 6. A computed F above 12 means faces have PINCHED — one
  component of A∖B carrying more than one face, which is what a degree-6 triple
  crossing does — and the bijection in the third bullet fails.

Measured over 260 random pairs:

    even degree, F <= 12     229 correct     0 wrong
    odd degree,  F <= 12       0 correct    23 wrong
    even degree, F > 12        0 correct     8 wrong

229 of 229 inside the valid regime, and both failure classes are predicted rather
than observed. Compute the degrees and F first; the formula is then right or
silent, which is the only useful kind.

**How coincidences enter.** An edge-edge coincidence MERGES two vertices of Γ,
lowering V by one and raising F by one. That is the mechanism behind section 6:
coincidence count tracks region count without determining it, because V is one of
three terms and E and c move independently. The two kinds of 13-pair are visible
here as (V, E) = (8, 18) with 24 coincidences against (10, 20) with 10 — different
incidence data, identical F = 12.

### It generalises to every n — the identity, though not the bound

Nothing in the derivation used n = 2 except the shape of the union. For n cubes,
∂(A₁ ∪ … ∪ Aₙ) is still a sphere whenever the union is a ball, tiled by the faces
of each ∂Aᵢ lying outside every other body. The graph on it is the pairwise
intersection curves **clipped to the exterior of all the others** — and the new
endpoints created by that clipping are exactly the **triple points** where three
boundaries meet. Then, unchanged:

    d1 = E − V + c + 1

Tested at n = 3 (`euler3.py`) on random triples: **14 of 20** exact, and every one
of the six failures has c ≥ 2 — the relation holds in all 14 connected cases and
fails in none of them. The failing quaternions are half-turns and near-symmetries,
where the union stops being a ball and its boundary stops being a sphere. On the
60 highest-count samples: **60 of 60 connected, Euler exact on all 60**, so it is
reliable exactly in the regime that matters.

The validity conditions gain one entry per level:

    n=2    even degree everywhere;  F <= 12
    n=3    even degree everywhere;  F <= 48;  and c = 1

`c = 1` was invisible at n = 2 because two convex bodies' intersection curve is
essentially always connected; at n = 3 the outer graph disconnects readily.

### The bound reduces to a triple-point count

Counting the graph by vertex TYPE turns the identity into something sharper. The
outer graph has exactly two kinds of vertex, and their degrees were measured
rather than assumed (1 336 vertices over 24 triples):

    TRIPLE POINT           degree 3 in 500 of 554     mean 2.957
    edge-face incidence    degree 2 in 596 of 830     mean 2.643

Generically a triple point has **degree 3** — three surfaces meeting bound a
cone, whose boundary has three edges at the apex — and an edge-face incidence has
**degree 2**, being an ordinary vertex of a pairwise curve. All the excess
degree is coincidence: two curve branches crossing at one point raise it to 4,
three to 6. Substituting 2E = 3·V3 + 2·V2 with V = V3 + V2 into F = E − V + c + 1:

    d1  =  V3/2 + c + 1

**Verified on 23 of 23 coincidence-free configurations.** (With coincidences the
identity gains + excess/2, where the excess is exactly the extra degree the
merged vertices carry — section 11's mechanism, now as an explicit term.)

So generically **the depth-1 count is half the number of triple points on the
union's boundary, plus c + 1**, and the theorem d1 ≤ 48 becomes the purely
combinatorial statement

    V3  <=  92        triple points on d(A u B u C)

That is the reduction worth having: it moves the question off region counting and
onto counting which of the 6x6x6 = 216 plane-triples of three cubes can be
simultaneously real and on the outer boundary. It does not prove 92 — but it is
the same currency as `PROOF_67.md`'s vertex weight split of 32 + 60 between
triple points and pairwise intersection polytopes, which is a weighting on
exactly these two vertex types. The bridge is now a bound on V3, not a
reformulation.

### It holds at every n, and yields the project's first upper bounds above n = 3

Nothing in the vertex-degree argument mentions n. Tested on coincidence-free
configurations:

    n = 4    12 of 12        n = 5    8 of 8        n = 6    4 of 4

so **d1 = V3/2 + c + 1 at every n**, with V3 the triple points on the outer
boundary. A triple point needs one face-plane from each of three cubes, giving at
most 6³ = 216 per triple of bodies — a trivially provable cap — hence

    n=3   d1 <=  110        n=6   d1 <= 2162        n=8   d1 <= 6050
    n=4   d1 <=  434        n=7   d1 <= 3782        n=9   d1 <= 9074
    n=5   d1 <= 1082

**These are the first upper bounds this project has at n >= 4**, where `RESULTS.md`
records "none is proved". Their honest quality: very loose. Actual d1 is 92 at
n = 4 against 434, and 214 at n = 6 against 2162 — a factor of 4 to 10. Two
reasons, both identifiable:

* **216 is loose even at n = 3**, where the true cap implied by d1 <= 48 is
  V3 <= 92, so the plane-triple count over-estimates by 2.3x before n even
  enters;
* **it ignores mutual exclusion.** At n >= 4 a triple point must also lie
  OUTSIDE every other body, which is what actually keeps V3 small, and counting
  plane-triples per body-triple discards that entirely.

### The derivation the middle depths do not need: the TOTAL is one Euler count

The recursion was being built depth by depth because each depth looked like a
separate problem. It is not. The union U = A₁ ∪ … ∪ Aₙ is a topological ball
whenever it is connected, so χ(U) = 1, and the arrangement gives U a CW structure
whose 3-cells are exactly the bounded regions being counted:

    0-cells   cube vertices, edge-face incidences, edge-edge coincidences,
              and triple points
    1-cells   arcs of cube edges and of pairwise intersection curves, cut at 0-cells
    2-cells   pieces of each ∂A_i, cut by the curves AND by that cube's own edges
    3-cells   the bounded regions

χ = V − E + F − C = 1 gives

    C  =  V − E + F − 1

**the total count as a pure incidence quantity**, exact by Euler rather than
approximate — no region counting anywhere, and no depth-by-depth recursion. The
two results above are this restricted to layers: d1 = F is the same computation
on the outer sphere alone, and N(S) = c is it on ∂K_S.

**Why this is the objective every cheap proxy failed to be.** Coincidence count,
the pair-type multiset and d1 are all strong in bulk (r = +0.75 to +0.97) and
invert in the last few units, which is precisely where a record is decided. C is
not a proxy for the total; it IS the total, so it cannot invert. Maximising
V − E + F is maximising the count.

**What is not built.** The refinement. Every current script cuts ∂A_i by the
intersection curves only; the cell complex also needs each cube's own 8 vertices,
12 edges and 6 faces in the same subdivision, and the 2-cells are the common
refinement of the two. That is bookkeeping rather than new mathematics, but it is
the whole of the remaining work, and the formula should not be trusted until it
reproduces a known count — 13 for a body-diagonal pair is the control to use.

### Why the incidence identity does not yet give a fast screen

`C = V + E − M + Σᵢcᵢ + n − c` is exact and its terms are incidence counts, which
suggested a two-stage screen: compute the cheap part (the new cube's own curves)
for an upper bound, and pay for the dear part (cutting every cached base curve
against ∂q) only on survivors. **It fails, and the failure direction matters.**

The reasoning was that each new triple point on a base curve adds one 0-cell and
one 1-cell and at least 3 to M, hence contributes at most −1. But in V − E + F − c
the added vertex and arc cancel, while the cut SUBDIVIDES faces on both bodies
sharing that curve — so F grows and C grows with it. The cheap stage is a LOWER
bound, and a loose one: 121 against 723, 118 against 727, 124 against 717, about
a sixth of the truth.

A genuine cheap upper bound would have to bound the face growth, i.e. the number
of cut points — which is precisely the expensive computation. The only
q-independent cap (each base segment is cut at most 6 times by the new cube's six
planes) does not vary with the candidate and cannot screen.

**So the identity's value is not speed.** The C++ engine counts a sixth cube in
about 2 ms against 0.20 s here. What the identity provides is that the count is
now a signed sum of incidence quantities — objects one can solve for and bound —
and that is a different kind of tool from a faster counter. Making it fast needs
a different decomposition, not a cheaper first pass.

### A family's maximum can sit on its walls, where no sweep of it looks

**Demonstrated at n = 3.** Sweeping 119 rational members of the dihedral family —
the family that CONTAINS both 67s — tops out at **59**. Evaluating at the two
special parameters instead, ψ = arcsin(1/√3) in ℚ(√2) and tan ψ = φ² in ℚ(√5),
gives **67** twice. The family's maximum is attained at isolated parameter values,
walls of the family rather than chambers, so no refinement of a rational sweep
ever reaches it.

**And the n = 4 figure is a rational sweep.** `nfamily_common.py` says so in its
own docstring: *"When psi and every theta_k are Pythagorean angles (sin, cos
rational), every cube matrix is rational"*. So the ledger's family maximum of 175
at n = 4 (335 at n = 5, 615 at n = 6) is the maximum over RATIONAL members — the
same instrument that returns 59 at n = 3 where the truth is 67. **The n = 4
family has never been evaluated at its walls**, and the comparison "175 < 183, so
the family loses" was never actually made.

**The method.** Build the one-parameter family; solve for its wall parameters
(`wall_params` already returns W3/W4 roots on a line); evaluate AT the roots, in
whatever field they generate. Note that `exact_chambers.py` evaluates strictly
BETWEEN consecutive roots by design — on a family whose optimum is a wall, it
looks past the answer every time.

**A failed attempt worth recording.** Trying this at n = 4 with ψ = 45° and
Δ = 90° returned 13 for the whole C₄ orbit: the axis (1,1,0)/√2 is a 2-fold CUBE
symmetry axis, so R² is a cube symmetry and the four cubes collapse to two. The
usable ψ are those whose axis n(ψ) = (sin ψ, cos ψ, 0) is not a symmetry axis —
which is why the 67s sit at arcsin(1/√3) and arctan φ² — and a general such ψ
puts the quaternion in a TOWER ℚ(√2, √3) rather than a single quadratic field.
The project has tower arithmetic (README: "towers ℚ(√a,√b)"); the engine flag
does not.

### Extension search has a demonstrated blind spot

Every hunt in this project fixes the (n−1) record as a base and searches for one
more cube. **The tower does not actually nest that way at the bottom, and the
break is measured:**

    183's four triples:  63, 63, 63, 55        (the three 63s are one C3 orbit)
    the n = 3 record:    67

**183 contains no 67 and is not an extension of one** — its best triple is four
short — and 393, 727, 1217, 1895 and 2785 all inherit that same 63. The whole
tower stands on a 3-cube sub-configuration that is not the n = 3 record, and it
has never cost anything. So a record CAN decline the record below it. The nesting
from 393 upward is an observed property of the configurations found, not a
constraint imposed or proved.

**Two mechanisms could reproduce it higher up, and both are now testable.**

* **An isolated irrational optimum.** Rationality of a record proves nothing when
  the locus is a continuum — the 727 arcs carry members in every ℚ(√d), d ≤ 97,
  all counting 727, so rational points are dense along them and reach the maximum.
  What rational search cannot reach is an isolated irrational optimum, which is
  exactly n = 3: dimension 0, two classes, both irrational, rational search capped
  at 63 forever. The levels at risk are those with 0-dimensional maximisers —
  n = 3, 4, 5 — and the ℚ(√d) campaign was only ever run at n = 6, where continua
  make it least necessary. `irr4.py` tests n = 4; first pass over d = 2, 3, 10, 13
  reaches only 147–153 against 183, but by random sampling in small coefficient
  ranges, and the 67s themselves were never findable by sampling — they were
  derived from the dihedral family.
* **The wrong member of a continuum.** Which member of an (n−1) continuum to
  extend is a free parameter that no hunt here has ever varied: 727 was always
  taken as `BASE + (7,14,1,-5)`, a single point of arc D, though arcs A, B and C
  carry 727 too. n = 3 is the model for why this matters — the 67s are {I, R, R²}
  for a SPECIFIC R on the n = 2 13-continuum, so the third cube is determined by
  the second and the whole thing is a solve in one parameter, not a search in two.
  `which_member.py` sweeps arcs A/B/C; `member723.py` sweeps the 723 half-line,
  the largest continuum in the table.

**Result of the test (2026-08-09).** Extending five non-record n = 6 bases, 4 800
random seventh cubes each: 727 -> 1217 (the control), 723 -> 1209, 719 -> 1207,
717 -> 1201, 707 -> 1193. Monotone in the base, none reaching 1217. Sweeping ten
members of the 723 half-line instead of one arbitrary point: 1209-1211, again
none reaching 1217. So at n = 6 -> 7 the chain looks sound for bases NEAR it --
which says nothing about a record far from the chain, and 183 is nowhere near any
67.

**A control worth copying.** `offchain.py` extends non-record n = 6 bases and
includes the record base in the list. 4 800 random seventh cubes on the 727 base
find 1217, so the instrument demonstrably locates a record when one is reachable
— which is what makes its negatives on the other bases mean something. So far:
727 → 1217, 723 → 1209. (One row is mislabelled: a base recorded as "721"
actually counts 681, having been taken from memory rather than verified.)

**And at n = 4 the "which member" question has no content**, because 183's best
triple is isolated: 0 of 1 730 Cayley directions at three ε hold 63. There is no
continuum below 183 to choose from, so the n = 3 → 4 break is not explained by
picking the wrong member of anything.

### The recursion, at the top depth

A region of depth exactly k with membership S is a component of
K_S ∖ (∪ of the others), K_S = ∩_{i∈S} A_i being convex — so the face-vector
argument should apply with K_S in the role of a single body, on the sphere ∂K_S.
Built for |S| = n−1, where exactly one body A_j remains (`euler_k.py`). The graph
on ∂K_S is Γ_{iA_j} clipped to the inside of the other members of S, the parts
meeting at the triple points, and it turns out to have **E = V** — no crossings,
so it is a disjoint union of c closed curves. Then:

* c closed curves cut the sphere ∂K_S into **c + 1** faces;
* K_S ∩ A_j is convex, so exactly **one** face is inside;
* hence **N(S) = c**, the number of closed curves in which ∂K_S meets ∂A_j.

Verified on all three 2-subsets in **20 of 21** coincidence-free triples at n = 3.

**And that is the known theorem, rederived.** Summing over the n subsets of size
n−1 gives d_{n−1} = Σ c_S, and the largest c observed is **6** — so c_S ≤ 6 is
exactly `d_{n−1} ≤ 6n` (`RESULTS.md`, proved via the anchor lemma). The face-
vector route reaches it by a different mechanism: not "the radial envelope has
local minima only at the 6n face centres" but "∂K_S can meet one more cube in at
most 6 closed curves".

**Where the recursion stops.** At depth 1 the remaining bodies are MANY and their
union is not convex, so the inside part of ∂K_S is not one face and N(S) ≠ c —
which is why depth 1 needed the union-sphere argument and got d1 = F instead. The
middle depths, 1 < k < n−1, have both difficulties at once and are not built. So
the recursion currently covers the two ENDS of the depth profile — d1 by the
outer sphere, d_{n−1} by closed-curve counting — and nothing between.

**And they bound d1 only, not a record.** A record is Σ_k d_k, so bounding one
needs every depth. The same argument should recurse — d_k is a sum over k-subsets
S of the depth-1 count for the arrangement {∩_{i∈S} A_i} ∪ {the others}, with the
convex body ∩_{i∈S} A_i playing the role of a single cube — but that recursion is
not built, and until it is these bounds constrain one row of the depth profile
rather than the total.

**What this does NOT give is the bound.** At n = 2 the cap came from O_A ≤ 6 —
A∖B lies in the union of A's six face-slabs — and 6 is tight, which is why the
identity delivers max(2) = 13 outright. At n = 3 the same argument gives only
6 × 6 = 36 components per body, hence d1 ≤ 108, against the true d1 ≤ 48 of
`PROOF_67.md`. So the two arguments are **complementary, not identical**: this
framing supplies the identity d1 = F, and `PROOF_67.md`'s finer Euler argument —
with its vertex weight split 32 + 60 between triple points and pairwise
intersection polytopes — supplies the bound on F. The resemblance is real (that
split is exactly the two vertex kinds of the graph above) but the proof is
strictly stronger than anything derived here, and calling them the same statement
would be wrong.

**It reproves max(2) = 13.** O_A ≤ 6 and O_B ≤ 6 give d1 ≤ 12; d2 = 1 by
convexity; so the total is at most 13. That is the convex-cover proof of
`RESULTS.md` reached from the opposite side — the bound is a statement about how
many faces fit on the union's boundary sphere, not about covering A∖B with slabs.
Whether the same framing reaches the n = 3 bound d1 ≤ 48 of `PROOF_67.md`, which
is also an Euler argument, is open and looks worth trying.

## 12. Solve a coincidence to LOCATE; do not solve it to SCORE

Two uses of a coincidence condition, with opposite economics.

**Scoring a candidate is a loss.** Predicting the two-cube count from incidence
data alone — `total = E - V + c + 2`, section 11 — agrees with the engine on only
83% of random pairs and takes 0.800 s per 300 against the batched engine's
0.387 s. The compiled counter already wins at that job; nothing in Python beats
it, and the prescreen's cost was never the bottleneck anyway.

**Locating a locus is a large win.** A 13-pair between the ninth cube and base
cube b is not a predicate to test but a curve to write down: q = b·(1, t·a) for a
a body diagonal. Asking for two 13-pairs at once intersects two such curves, and
the system is 2 linear equations in one unknown — 28 base pairs x 16 axis pairs,
448 systems, solved exactly in seconds.

**The degenerate case is the whole point, and discarding it is the natural bug.**
448 systems give 12 transverse intersections — isolated points, 7 of them the
ninth cube duplicating one already present, best count 2737, WORSE than random
search had already found. But **3 of the 448 are coincident**: the two curves are
the same curve, so the conditions do not over-determine and a whole one-parameter
FAMILY survives. A solver that returns "no unique solution" throws those away.
They are where the maximiser lives:

    base cubes (1,4)  axis (-1,-1,1)   q(t) = b1*(1, t*(-1,-1,1))
    base cubes (2,6)  axis (-1,-1,1)
    base cubes (3,4)  axis (1,1,1)

The 2785 ninth cube (56,56,55,56) is q(227/889) on the first of them. So the
continuum that 429 272 sampled candidates discovered is derivable in closed form
from three linear systems, and the search space collapses from a 768 000-member
near-symmetry family to three curves.

**Run at every level, it derives most of the tower** (`solve13_all.py`, a coarse
t-scan at denominator 700 on each family, so these are lower bounds):

    n=4  183  -> 5th     0 of  96 systems coincident   NO family at all
    n=5  393  -> 6th     2 of 160    both reach 723
    n=6  727  -> 7th     2 of 240    reach 1213 and **1217**
    n=7 1217  -> 8th     3 of 336    reach 1887, 1879 and **1895**
    n=8 1895  -> 9th     3 of 448    one carries **2785**

**Every record from n = 7 upward falls out of a linear system on the base**, with
no search, along with 723 at n = 6. The one record it does NOT reach is **727** —
which is exactly the configuration the ledger describes as beating 723 by leaving
the corner-concurrence stratum. The method sees that stratum and nothing else, so
its one blind spot is the one documented departure from it. Restricting to
BODY-DIAGONAL 13-pairs is what draws that boundary; the edge-arc and isolated
half-turn families are excluded and are where an off-stratum record would have to
come from.

**And 183 admits no family at all** — 0 of 96 systems. That is a structural fact
about n = 4 measured for the first time, and it fits 183 being the one maximiser
that reads isolated under every probe (`MAXIMISER_TAXONOMY.md` section 3).

**The rule.** Use a coincidence to say WHERE to look, never to say how good a
place is. And when a solve reports no unique solution, check whether it means no
solution or an entire family — those are opposite answers and the second is the
interesting one.

## 13. Render the figure and look at it

Text extents cannot be estimated. Legend labels overflowed twice in one session
on arithmetic that looked right, and a near-tangency of 0.97px between two marks
in `shapes.svg` asserted an intersection between the two n = 2 components that
had just been disproved. Geometry in a figure acquires meaning as the mathematics
catches up with it, so inherited coordinates need re-checking against each new
result, not just the text.

---

## The tools

All in this directory, copied out of a session scratchpad on 2026-08-06 and
repointed to run from here. Each takes its imports from its own directory, so
`python3 <name>.py` works in place.

| file | what it does | section |
|---|---|---|
| `exact_chambers.py` | solve every W3/W4 root on a line, evaluate once per chamber, report the decomposition | §1 |
| `solve_ends.py` | the same catalogue rebuilt for an ARBITRARY base, not just the five-cube 393 | §1 |
| `maxline.py` | the maximum over a line, chamber by chamber | §2 |
| `cayleyscan6.py` | the working direction scan: Cayley chart, \|u\| ≤ 6, three ε | §5 |
| `edgecross.py` | edge-edge crossing sets, their Jacobian and null space, over ℚ | §6–9 |
| `qfield.py` | exact ℚ(√d) arithmetic with exact SIGN, and the crossing machinery over it | §6, §9 |
| `record_six.py` | decodes which tight conditions a tangent violates, by cube pair and type | Postscript 102 |
| `interior.py` | dense sampling inside chambers — the test that boundaries are coincidences | §7 |
| `localcorr.py` | region count against crossing count over a neighbourhood | §6 |
| `around.py` | the histogram of counts around a maximiser, all directions | §6 |
| `tight2.py`, `dirscan.py`, `cayleyscan.py`, `n78.py` | supporting: tight Step-A sets in the right chart, batched engine calls, the n=7/8 sweeps | — |

**They were nearly lost.** Everything above ran for a day out of
`/private/tmp/.../scratchpad`, which is volatile, while `METHODS.md` cited the
techniques as if the implementations were durable. `VIEWERS.md` records the same
failure for the n = 2 map's source — *"Artifact sources live nowhere durable
unless copied"* — so this is the second occurrence in the project. A method is
not written down until the code that performs it is in the repository.

## The paths worth taking next (2026-08-10)

Ranked, each arising from something established rather than from backlog.

1. **Sweep the RULINGS.** Every wall is a signature-(2,2) quadric, hence doubly
   ruled, and a straight line in Cayley space IS a one-parameter family of
   rotations -- exactly what every maximiser arc here has been. So each wall
   carries two natural families of arcs and **not one ruling has ever been
   swept**. Cheap: the rulings of a quadric are closed-form. Through a point p on
   the wall, a direction d rules it iff p^T Q d = 0 and Q(d) = 0 -- one linear and
   one quadratic condition, two real solutions for signature (2,2).
2. **BOUND C, do not search for it.** `C = V + E - M + sum c_i + n - c` is exact
   on every record and every term is an incidence count over face planes. A real
   upper bound needs them bounded JOINTLY, since E enters positively and M
   negatively -- a combinatorial question about how many plane-triples can be
   simultaneously real and mutually outside. This is the only route in the project
   to proving a record maximal; every search, including all of today's, produces
   lower bounds forever.
3. **Tower arithmetic Q(sqrt a, sqrt b), then re-evaluate the families at their
   walls.** Sweeping the dihedral family rationally gives 59; evaluating at its
   two wall parameters gives 67. `nfamily_common.py` states its own sweeps are
   Pythagorean, so the ledger's family maxima -- 175 at n=4, 335 at n=5, 615 at
   n=6 -- are maxima over RATIONAL members and none has been evaluated where its
   optimum would sit. `cellcomplex.py` is field-agnostic and works as soon as the
   arithmetic exists.
4. Postscript 102's non-circular binding test; the middle depths d_2..d_{n-2},
   still without identity or bound; the n = 9 continuum, characterised end to end
   and never extended by a single cube.
5. **A SECOND BASE.** Everything from 393 upward is the same five cubes. Whether
   wrapping strata, ruled walls and the coincidence ladder are properties of this
   problem or of this compound is untested, and a second base is the cheapest way
   to find out.

## Where to test whether these generalise

Everything above was learned on one base — the five-cube 393 and its extensions —
and mostly at n = 6. The honest next step is to run the same instruments
somewhere they have never been:

* **the 725 and 721 strata**, and other non-maximal totals. Every technique here
  was tuned on level sets that happen to be maxima; nothing about the methods
  requires that, and a non-maximal level set is a free control.
* **n = 9 and beyond**, against the §9 extension rule. Two 13-pairs, zero
  9-pairs, is a prediction that either finds a cube or fails cleanly.
* **a base that is not the 393**, to separate what is true of this problem from
  what is true of this compound.
* ~~n = 3's two 67s~~ — **DONE, and it paid immediately** (`qfield.py`, exact
  a + b√d with exact sign). First run overturned a claim made from rational-only
  data: maximisers were said to use only the 24-crossing kind of 13-pair, but the
  octahedral 67 is three 10-crossing ones. It also produced a new congruence
  invariant separating the two 67s, 30 crossings against 72, where the pair label
  and the per-label profile are identical for both. **The first excursion into
  untested territory broke a rule inferred from the tested part** — which is the
  argument for the other three below.
