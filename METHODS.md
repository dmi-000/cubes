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

## 10. Render the figure and look at it

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
