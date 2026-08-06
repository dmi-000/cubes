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

## 7. Every boundary is a coincidence boundary; most coincidences are not boundaries

W3 + W4 bracket every chamber wall observed on every 727 arc — 39 of 39 — while
only about a quarter of the interior crossings change anything. The converse
direction was assumed rather than tested by the chamber decompositions, which
evaluate one point per inter-root interval and so cannot see a wall inside one.
Tested directly (2026-08-06): 40 small-denominator samples inside each of the 12
widest chambers on the 723 line, **480 evaluations, every chamber single-valued**.
No boundary was found that the coincidence catalogue does not carry.

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

Crossings per cube PAIR take only three values — 24, 6, 0 — corresponding exactly
to the pair labels 13, 9, 4. Along the top of the tower the 9-pair count is
frozen at nine:

    727    4x13   9x9    2x4
    1217   6x13   9x9    6x4
    1895   8x13   9x9   11x4

so both extensions added exactly **two 13-pairs, zero 9-pairs**, and 4-pairs for
the rest. Testing a candidate's pair types is an incidence test, far cheaper than
an arrangement count, so it prescreens at a rate region counting cannot reach.
Two data points: a heuristic to test, not a law.

## 10. Render the figure and look at it

Text extents cannot be estimated. Legend labels overflowed twice in one session
on arithmetic that looked right, and a near-tangency of 0.97px between two marks
in `shapes.svg` asserted an intersection between the two n = 2 components that
had just been disproved. Geometry in a figure acquires meaning as the mathematics
catches up with it, so inherited coordinates need re-checking against each new
result, not just the text.

---

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
* **n = 3's two 67s**, where the coincidence machinery needs ℚ(√2) and ℚ(√5)
  exact arithmetic rather than ℚ. Every crossing-based result here is rational-
  only, so the two most-studied maximisers in the project are the two this file
  has never touched.
