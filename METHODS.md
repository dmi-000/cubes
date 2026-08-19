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

**And the member sweeps were answering the wrong question.** Given the near-
symmetry search, the 1217-arc member s = -9/200 reached only 1887 in 52 800
candidates over two hours. SOLVED instead -- the coincident-curve systems of
section 12 -- the same base reaches **1895 in seconds**, from three closed-form
families scanned at 500 points each. So that member is not deficient; the
shortfall was the instrument. Two lessons: solve a base before searching it, and
treat "member X falls short" as a claim about the search until a solve agrees.

**The coincident-curve structure is INVARIANT along the arc.** The three
degenerate systems on the s = -9/200 member are the same three as on the record
member -- cube 1 and cube 2 on axis (-1,-1,1), cube 3 on (1,1,1) -- reaching
1887 / 1879 / 1895 in both cases. Moving the seventh cube within its plateau does
not change which systems degenerate. That is why members are interchangeable,
stated in linear algebra rather than inferred from comparing search outcomes.

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

## 14. Displace by an INFINITESIMAL, not by a small number

Every displaced count in this project was `count(base + eps*d)` for a finite eps
chosen by hand or by halving. A finite eps is a SAMPLE of the cell you meant to
measure, and it can miss: the walls through the vertex are the tight conditions,
but the LOOSE conditions are walls too, sitting at positive distance, and a step
large enough to cross one measures the wrong cell. Halving until two steps agree
does not fix it (FAILURE_MODES 14).

The fix is arithmetic, not a smaller number. Q(sqrt D)(eps), elements truncated
polynomials ordered by the sign of the lowest-degree nonzero coefficient, is a
genuine ordered field -- non-Archimedean, so 0 < eps < every positive rational.
The count returned IS the eps -> 0 limit. There is no step size to choose and
none to defend.

**When this transfers.** Any predicate-based geometric computation qualifies if
(a) every decision is a SIGN TEST, and (b) the multiply chain has a BOUNDED
degree, so the truncation is exact rather than approximate. Here the chain is
quaternion 1 -> plane 2 -> minor 4 -> det3/vertex 6 -> predicate 8, hence degree
8 and no product is ever truncated. Check (b) before trusting it: if a truncation
could discard a nonzero leading term, the sign predicate returns 0 for a nonzero
quantity and you get a wrong ANSWER rather than a crash.

Cost: the overflow budget picks up the convolution length at each stage, ~2592
overall, costing a factor ~2.2 in admissible component magnitude. Cheap.
Implementation: `make_eps_engine.py` generates `cube_regions_eps.cpp` from the
validated q2 engine -- a generator, not a hand-edited copy, so the derivation
from the validated engine stays re-runnable. Gate: `eps_gate.py`, whose decisive
control is that scaling a direction by 97 and by 1/1000 must not change the
count. No finite-eps implementation can pass that.

## 15. Choose the CHEAPEST valid representative, not the obvious one

An object defined up to an equivalence has no canonical representative, so the
one you pick is a free variable — and picking badly can cost you the measurement
outright.

Concretely, for Fourier-Motzkin witnesses: back-substitution naturally takes the
MIDPOINT between the induced bounds, and midpoints of rationals with unrelated
denominators compound through the recursion. Take the SIMPLEST RATIONAL in the
interval instead (continued-fraction descent: if an integer lies strictly inside
it is simplest; otherwise both ends share a floor, and the answer is that floor
plus the reciprocal of the simplest point of the reciprocal interval). Measured
on the 727 extension chambers: witness heights fell from 13 528 to 178, and the
count of chambers the engine could evaluate went from 14 of 24 to 24 of 24.

Verify such a routine against BRUTE FORCE, not against itself: 300 random
intervals, each result checked to be strictly inside AND minimal in denominator
over all smaller denominators. The property is cheap to check exhaustively at
small size, which makes it a real oracle rather than an agreement between two
spellings of one idea.

Where else the same free choice appears here: a direction's scale (`normalize_dir`
exists for exactly this reason -- an unscaled null-space vector routinely lands
outside the engine's budget), a cone's interior point, a class representative, a
chart. See [FAILURE_MODES](FAILURE_MODES.md) 16.

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
| `record_six.py` | decodes which tight conditions a tangent violates, by cube pair and type | Postscript [102](LEDGER.md#p102) |
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

## Cache the expensive step — before the first run, not after the second

Established 2026-08-13, at a cost of two hours.

**Every campaign here has ONE expensive step and many cheap ones**, and the
expensive one is almost always shared by analyses that have not been written yet.
`census_dimension` spent ~5 minutes per class building tight conditions
symbolically, used the gradients once for a dimension, and discarded them. When
the boundary cone and the wall classification turned out to need the SAME
gradients, 27 completed classes had to be recomputed from scratch. Cached on disk
keyed by configuration, the repeat run costs **0.3 s**.

    identify the one expensive step
    cache it keyed by its input, on disk, in the repository
    do this BEFORE launching, not when the second analysis wants it

**The reason it is not premature optimisation:** the value is not speed, it is
RESTARTABILITY. A campaign that caches can be killed, corrected and relaunched at
the cost of the correction alone, which is what makes it safe to fix a method
mid-run. This project has interrupted campaigns for a spec bug, a scale bug, a
strictness bug and a wrong direction set — every one of those interruptions was
cheap or expensive depending on nothing but whether the intermediate had been
kept.

It pairs with the two rules already here: **write results incrementally** so an
interrupted run leaves data, and **write deliverables to the repository** so they
survive the session. Incremental output protects what a run has produced; the
cache protects what it had to compute to produce it. A spec that asks for a long
campaign should require both.

## Where work is allowed to live

Third occurrence, 2026-08-11, so it is now a rule rather than an anecdote.

**Deliverables are written straight to the repository. Scratch is only for output
you will never cite.** The delegated rulings run got this mostly right — code,
data, log and report all landed in the repo — but its INDEPENDENT CONTROL did
not. `rulings_report.md` rests three ways on a check that rebuilt the wall
quadric from scratch, sharing no code with the program under test; that check was
written to `/private/tmp/.../scratchpad` and would have died with the session,
leaving the report asserting a verification that nothing in the repo could
perform. It is now `rulings_control.py` and runs in place. So:

* **A control is a deliverable.** If the negative or independent check lives only
  in scratch, the gate it supports is not reproducible, whatever the report says.
* **Write it where it belongs the first time.** Scratch-then-copy is the step that
  gets skipped; there is no reason to take it for anything you intend to cite.
* **A spec names its deliverable paths**, so "did the agent save its work" is a
  check rather than a judgement call.

**And name files by their PATH in a report, not by their basename.** This one cost
a false alarm the same day: `handoff_report.md` cites ten bare filenames, eight of
which live in `dihedral_scratch/`, so a root-level existence check reported the
whole Postscript [25](LEDGER.md#p25)–[29](LEDGER.md#p29) dihedral chase as unreproducible. It is not — the scripts
are archived, just not where the report implies. Of 29 reports, 24 have a
same-stem script and four more name their producers under other names; the only
artifacts genuinely absent anywhere on disk are `handoff_witness.jsonl` and
`clip.html`.

## Every postscript names its program AND its output data

A postscript is a claim; the reproduction path has to be findable from it. Measured
2026-08-19: of 142 postscripts, 70% named a program somewhere in the prose and only
28% carried a structured reference — and seven of this session's postscripts,
including the ones establishing the crossability discriminator and the validated
irrational construction, named no program at all.

**Nothing else closes that gap.** `data_inventory.py` maps data -> producer,
`.prov.json` stamps map data -> script + content hash, `DATA_MANIFEST.md` judges
which data is current. All of them run from the DATA. Nothing ran from the CLAIM.

**A bare filename is not enough**, and this project has the scar: `census_variety.py`
was edited in place across four generations, so a postscript naming it would now
point at code producing different numbers. The ledger is append-only; programs are
living; a filename in an immutable record rots silently.

**So cite the chain, preferring the OUTPUT DATA as the authoritative reference:**

    postscript  ->  names its output data file (immutable)
    data file   ->  .prov.json carries argv and the script's CONTENT HASH at run time
    hash        ->  a cheap SCREEN, not a verdict
    re-run      ->  the actual test

**EDITING A PROGRAM IN PLACE IS FINE**, as long as it still reproduces the cited
output from the same parameters. Comments, refactoring and added features all
change the hash while preserving behaviour, so a changed hash means UNKNOWN, not
broken. `provenance.verify()` said "rerunning will not reproduce it" on any hash
change -- an overclaim, corrected 2026-08-19. It now reports:

    hash unchanged  ->  reproduces, no re-run needed
    hash changed    ->  UNKNOWN; re-run and compare
    `provenance.reproduce(path)` re-runs the recorded argv and compares, restoring
    the cited data afterwards so the record is never clobbered by its own check

What `census_variety.py` actually lost was not the edits but the PARAMETERS: no
argv was recorded, so there is nothing to re-run generations 1-3 with. Record the
command and the output; then in-place edits stay harmless and checkable.

**Hash the LOGIC, not the bytes.** `provenance.semantic_sha1` hashes the AST with
docstrings stripped, so comments, whitespace and reformatting do not trigger a
flag -- and adding a comment that records WHY an invariant holds is routine here,
so a byte hash would fire constantly and then be ignored, which is worse than no
check at all. Verified: comment/format/docstring edits leave the logic hash
unchanged; `x+1 -> x+2` changes it.

**Renaming is NOT canonicalised away, deliberately.** Alpha-renaming could be
hashed around, but the fallback is already cheap and correct: a flag means "run
`reproduce()`", not "this is broken", so a rename costs one re-run rather than a
false verdict. Engineering the hash to ignore renames buys nothing the fallback
does not already give.

**Prefer names you will not want to change; where one turns out badly, add a
comment rather than rename.** A rename is a semantic act -- it changes what a
reader believes the name means, and it silently invalidates every log line,
postscript and transcript using the old one. Draw the line by AUDIENCE: names in
the record (output keys, cited functions, data fields) are interface and should
not move; purely local variables are private and may be renamed freely, at the
cost of one re-run.

Citing `two_plus_quadric.json` gives the exact command AND a check on whether the
script has changed since. Citing `two_plus_quadric.py` gives today's file, which
may not be what ran.

Form: a final line `Files: <programs> -> <outputs>`. Where a result was computed
inline with no file retained, SAY SO — "computed inline, no output file retained"
is a fact about reproducibility, not an omission.

## The documents, and which kind each one is

The old rule — UPPERCASE = hand-authored, lowercase = named after its script,
`LEDGER.md` excepted — encoded PROVENANCE and nothing else, so 24 one-shot work
orders sat under the same convention as the standing references. Revised
2026-08-11, on three axes that were previously implicit:

**Lifetime.** `specs/` holds work orders written for a delegated agent; they are
spent when the run finishes and are kept only so a result's instructions can be
re-read. Everything uppercase in the root is a standing document. The 24 specs
were moved and all 229 references in authored files swept the same day
(`specs/MOVE_LOG.json` records exactly what moved and what was rewritten). The
precedent is the `six_cube_search_results.md` → `LEDGER.md` rename: **consistent
renaming is data-preserving**, so authored documents get swept — including this
one and the ledger, whose append-only discipline governs CLAIMS, not paths. Two
kinds of thing are exempt, for two different reasons: **verbatim records** —
session transcripts and `bak/` — are what was actually said or held at the time,
so a sweep would falsify them; and `github/` is a **separate git repository,
maintained by hand**, so a sweep there is a publication act rather than
bookkeeping. Export timing between the two is deliberately out of scope: expect
`github/` to lag, and do not treat a difference between it and the root as
a defect to fix automatically.

**Structure.** Chronological — `LEDGER.md` (by write time), `JOURNEY.md`, every
`*_report.md`, the transcripts. Logical — `RESULTS.md` (by claim), this file,
`FAILURE_MODES.md` (by symptom), `GLOSSARY.md` (grouped by meaning),
`MAXIMISER_TAXONOMY.md` (by axis). The pairing is deliberate and each side links
to the other; do not merge them.

**Mutability, and how an immutable record survives it.** A `.md` is LIVING: when
it is found wrong it is corrected in place, with the correction marked and dated
rather than silently absorbed. Its data siblings — `.json`, `.jsonl`, `.log`,
`.out` — are IMMUTABLE and are never edited, so the original numbers stay
derivable from the run's own artifacts. That is what makes a living report safe:
`rulings_report.md` was corrected the morning after its run (17 entries → 8
distinct rulings, "5 constant" → 2 and both vacuous) while `rulings_data.json`
went untouched and still proves both readings. A report whose script is missing
from the repo breaks this, and 15 of 29 currently do.

Every standing document opens by saying what it is and who should read it. If a
new one cannot, it does not yet know what it is.

## Corrections propagate INSIDE the record and not out of it

Measured 2026-08-17: `LEDGER.md` holds 118 postscripts with **389
cross-references between them and 1 link back out to `RESULTS.md`**. Supersession
therefore propagates perfectly within the ledger and not at all into the summary
that actually gets read. A correction arrives as a new postscript, which is a
complete act in the ledger's own terms, while the current-beliefs document keeps
the superseded claim.

Two claims were stale for two weeks: "(2,1,1) and (1,1,1,1) wall types never
enumerated" (they were enumerated the same week -- 2 544 W4 and 4 320 W3 walls
against the 393 base, all verified), and "rulings are NOT constant-count lines",
whose headline stands but whose quoted evidence is the window-based statistic
[Postscript 108](LEDGER.md#p108) retired. The first survived longest in the
SUPERSEDED-CLAIMS TABLE -- the mechanism built to stop stale claims propagating
propagated one.

**The check, and its limits.** `doc_audit.py` flags every RESULTS claim whose
cited postscript a LATER postscript revisits, and separately lists claims citing
nothing. It is TRIAGE: a later reference is usually an ordinary citation, not a
refutation, so it produces candidates and not verdicts, and a claim it does not
flag is one it has said nothing about. Of 64 claim blocks it flagged 30; review
found 2 genuinely stale and 7 substantive claims resting on no traceable source
at all. Before asserting a "we have / have not done X" claim from a summary
document, check the ledger for later postscripts AND check whether the code
already exists -- `detq_check.py` answered the wall question in one command.

## The paths worth taking next (re-ranked 2026-08-12)

Ranked, each arising from something established rather than from backlog. The
2026-08-10 ranking led with the rulings; that path was executed and demoted
itself, so this is the revision, with the old order kept visible below.

1. **PROVE s ≤ a + b + m − 2.** The Step B singleton term is a component count on
   the sphere, and the whole of max(3) now rests on this one inequality:
   a, b ≤ 6 is proved (the six-slab convex cover, the max(2) = 13 argument) and
   m ≤ 6 is FREE (C is a cone; cutting by which coordinate attains ‖u‖∞ gives six
   convex polygons), so s ≤ 16 and T ≤ 1 + 18 + 48 = 67. Since χ_c(X) ≤ comp(X)
   for any open surface, the other three sets need no hypothesis at all.
   **CORRECTED 2026-08-12:** the target is NOT "every component of K ∩ L is simply
   connected" — that is FALSE, and the project's own parity data says so. When s is
   odd, central symmetry forces a self-antipodal component of K ∩ L, and an open
   disk admits no fixed-point-free involution (Brouwer), so that component is not
   simply connected; yet the inequality still held there. Writing χ_c(X) =
   comp(X) − D(X) with D(X) = Σ(kᵢ − 1) over components and their boundary circles,
   the identity is exact and the target is

       s ≤ a + b + m − 2   ⟺   D(K ∩ L)  ≤  D(K) + D(L) + D(C),

   an inequality about EXCESS BOUNDARY CIRCLES — submodularity-flavoured, true in
   1 930 of 1 930 pairs, and not requiring any set to be a disk. Equality holds
   exactly when a, b, m, s are all even, which includes the maximiser.
   [Postscript 106](#p106), [107](#p107).

2. **TEST 12F − 5 AT F ≠ 6, by climbing.** The bound generalises to congruent
   centrally symmetric F-facet cells as T ≤ 12F − 5, giving 67 at F = 6 — so the
   cube's number is one case of a family, not a coincidence. `cells.py` computes
   a, b, m, s for any such cell exactly and measures m = F in every configuration
   tested. Nobody has ever climbed a non-cube family: is 91 approached at F = 8?
   If yes the whole Step B picture is shape-generic; if the maximum sits far below,
   cubes are special and the reason is worth finding. Cheap, and it is the only
   item here that could falsify yesterday's result rather than extend it.

3. **BOUND C, do not search for it.** `C = V + E − M + Σ cᵢ + n − c` is exact on
   every record and every term is an incidence count over face planes. A real
   upper bound needs them bounded JOINTLY, since E enters positively and M
   negatively. This is still the only route in the project to proving a record
   maximal at n ≥ 4; every search produces lower bounds forever, as
   [Postscript 105](#p105) cost 30 hours to demonstrate again.

4. **Tower arithmetic ℚ(√a, √b), then re-evaluate the families at their walls.**
   Sweeping the dihedral family rationally gives 59; evaluating at its two wall
   parameters gives 67. The ledger's family maxima — 175 at n=4, 335 at n=5, 615
   at n=6 — are maxima over RATIONAL members and none has been evaluated where its
   optimum would sit. Still the likeliest place an actual RECORD moves.
   `cellcomplex.py` is field-agnostic and works as soon as the arithmetic exists.

5. **A SECOND BASE**, and [Postscript 102](#p102)'s non-circular binding test; the middle depths
   d₂…d_{n−2}, still without identity or bound; the n = 9 continuum, characterised
   end to end and never extended by a single cube.

**SPENT — the rulings (was #1 on 2026-08-10).** Executed 2026-08-11/12. Every
wall is a signature-(2,2) quadric and doubly ruled, and det(Q) is a perfect
square identically — `(|p|²−1)²` for W4, `16(|m×q|²−2|m|²)²` for W3 — so every
wall SPLITS over ℚ and none of its ruled structure is hidden from rational search
([Postscript 104](#p104)). But rulings are not constant-count lines, the premise the ranking
rested on ([Postscript 103](#p103)), and two passes measured it with a window-dependent criterion
before that was noticed. What survives is a question, not a path: at the arc-A
terminus a ruling holds 725 across 99 consecutive chambers and then ends, so the
right statistic is the longest constant RUN, and whether rulings beat generic
directions through the same point is being measured by `rulings3.py`.

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
