# Open questions, and what has been RULED OUT

**Why this file exists, and why it is not a conjecture list.** `RESULTS.md`
already has a CONJECTURE tag; `JOURNEY.md` has an Open-questions section that
says of itself that items sat there "still listed as open long after they were
proved". A third list of open items would be a third thing to drift. What is
genuinely unrecorded is the ELIMINATION record: negative results are expensive to
produce, cheap to forget, and re-derived by the next person unless written down
where the question is asked.

**Every elimination cites the Postscript that established it**, so
`doc_audit.py` can flag an entry whose evidence a later Postscript revisited.
An entry with no citation is a hunch, and is labelled as one.

---

## 1. Why do SHELLS occur where they do?

A shell is a self-antipodal region wrapping the origin without containing it. An
EVEN region count detects one ([P121](LEDGER.md#p121)); counts are otherwise odd
by central symmetry.

**The puzzle.** The octahedral 67 has 0 even faces of 728; the golden 67 has 148
of 2 196. Both are 3-cube configurations.

| explanation | verdict | evidence |
|---|---|---|
| High symmetry forbids shells | **UNTESTABLE on current data** — all 826 census configurations have symmetry order 1, so there is no variation to correlate. Not refuted; unfalsifiable here. | [P127](LEDGER.md#p127) |
| Shells need small compounds | **PARTIALLY SUPPORTED, insufficient** — 5 of 6 even census counts are k=3, one k=4, none k≥5. But both 67s are 3-cube, so it cannot separate them. | [P127](LEDGER.md#p127) |
| Shells hide in narrow, high-codimension faces | **REFUTED** — exactly backwards. Golden's shells favour codimension 0 (16.7%) over codimension 2 (3.2%). | [P127](LEDGER.md#p127) |

**What this established instead:** shells are STABLE, occupying open chambers with
positive measure, so they are findable by generic search rather than by hunting
coincidences.

| The FIELD — ℚ(√2) vs ℚ(√5) | **REFUTED 2026-08-18** — 7 871 random 3-cube configurations: even rate 13.20% in ℚ(√2), 12.90% in ℚ(√5), ratio **0.98** where the hypothesis needs ≫ 1. | [P129](LEDGER.md#p129) |

**THE QUESTION WAS BACKWARDS.** Shells are ORDINARY — about one random
configuration in eight has one. It is the record-related configurations that are
anomalous, and the dominant effect is now measured: **counting well suppresses
shells, monotonically** — 19.6% at counts 20–29, 13.5% at 30–39, 6.2% at 40–49,
1.7% in the top decile. A shell must wrap the origin without being cut, and
high-count configurations cut space most finely; the two are in tension. This
explains the census (0.7%) and golden's 6.7%, which is near what its neighbours'
counts predict.

**DETECTOR CAVEAT — READ FIRST** ([P130](LEDGER.md#p130)). Parity detects an ODD
NUMBER of shells, not their presence: two shells restore odd parity, measured in 3
of 3 000 random configurations. So every "even rate" below is an
odd-shell-parity rate, and **the octahedral 67's shell-freedom was never measured**
— its 728 faces have an EVEN number of shells each, which may be 0 or 2. Measuring
shells directly needs region-level output from the engine (does a region equal its
own antipodal image?), not another statistical pass.

**THE SHARPENED QUESTION — NOT ESTABLISHED, pending the above.** The octahedral 67's faces span the same count range as
golden's, so the trend predicts ~10% — about **70 shells among its 728 faces**. It
has **ZERO**. Golden is at expectation; octahedral is the outlier. Symmetry
returns as a candidate in a form the census could not test: octahedral has
symmetry order 24 and 6 INDEPENDENT walls giving a simplicial 3⁶−1 arrangement, so
the group acts on faces in orbits, and an orbit-invariant property is all-or-
nothing rather than intermediate.

**Method requirement, learned the hard way 2026-08-18.** This must be tested by
computing the genuine group ACTION. Counting-based shortcuts are worthless:
"multiplicity is a sum of divisors of 24" is VACUOUS (1 divides 24, so every
integer qualifies — it passed on everything), and "multiplicity divisible by 24"
is IMPOSSIBLE (728 = 3⁶−1 = 24·30 + 8 forces small orbits). Neither can fail or
pass informatively; see [FAILURE_MODES 16a](FAILURE_MODES.md). The real test
needs, for each of the 24 symmetries, the induced signed permutation of the six
walls, then a decomposition of the 728 sign vectors into true orbits.

*Superseded framing, retained:* the FIELD — ℚ(√2) vs ℚ(√5). **Caveat that makes it hard:** with only
two data points, *any* binary property of the pair explains the difference
equally well (field, symmetry order 24 vs 6, 6 vs 9 walls). A third irrational
configuration, or a proof that none exists at n = 3, is what would make this
answerable rather than merely askable.

## 2. Does IRRATIONALITY force first-order rigidity? — **ANSWERED: NO**

**REFUTED 2026-08-18** ([P128](LEDGER.md#p128)). Four irrational maximisers on the
n = 2 13-continuum — including 1/φ — count 13 with **lineality 1**, in both
ℚ(√2) and ℚ(√5). Irrational, maximal, and not rigid.

The real pattern: the 67s are rigid because they are ISOLATED, and first-order
rigidity is what isolation means at first order. Irrationality rode along as a
coincidence of n = 3.

*Original statement, retained:*

Both 67s have walls of full rank — pinned at first order, lineality 0. **No**
rational record does: 727, 1217, 1895, 2785 keep tangent spaces of dimension
1, 2, 3, 4 ([P122](LEDGER.md#p122), [P124](LEDGER.md#p124)). The 67s are also the
only irrational rung of the tower. Three facts about irrationality that may be
one fact.

**Ruled out:** that the rank figures were an artefact of the omitted (1,1,1,1)
wall type — those walls were differentiated and add exactly **zero** rank
([P124](LEDGER.md#p124)).

**Blocked by the same two-data-point problem as question 1.**

## 3. Why is the glue deficit exactly −8?

Gluing as a search reached 175 / 385 / 715 against records 183 / 393 / 723 —
deficit **−8 at three separate levels** (`glue_report.md`, 319 141 configurations).

**Ruled out:** that simultaneous extension is itself obstructed — 1895 is a worked
instance, reachable by extending two NON-CONGRUENT 1217s
([P126](LEDGER.md#p126)). So −8 is a property of that glue construction, not of
the idea.

**Suggested by the project's own rule** (a census returning few distinct values
wants factoring, not more counting) and answerable from data already on disk.

## 4. Why 24 walls per added cube? — a WINDOW n = 6..8, broken at both ends

**CLOSED at the top end 2026-09-12 ([P300](LEDGER.md#p300)):** n = 10 is now measured —
480 tight, **100 distinct walls**, rank 21, lineality 6 — against the law's prediction of
123. The window is n = 6..8 on the current records, shut at both ends by measurement
rather than by inference.

**CORRECTED 2026-09-08 ([P290](LEDGER.md#p290)): the n = 9 rung belongs to 2785,
which is no longer the record.** 2785 reproduces `walls = 24n − 117`,
`tight = 84n − 288`, `rank = 2(n+1)`, `lineality = n − 5` exactly — 468 tight, 99
walls, rank 20, lineality 4. But **2787 superseded it**, and neither of 2787's
representatives does:

    n = 9                        tight  walls  rank  lineality
    fit / 2785 (superseded)        468     99    20      4
    2787 simplified (h 140)        420     83    20      4
    2787 original   (h 113 786)    396     76    19      5

So the window is three rungs over the current records, not four, and the n = 10
failure below is less of a surprise than it was. The heading and the table below
are left as written and corrected here rather than rewritten, so what the
question said before stays readable.

For n = 6..9: `walls = 24n − 117`, `tight = 84n − 288`, `rank = 2(n+1)`,
`lineality = n − 5` ([P122](LEDGER.md#p122)). The 24 is the order of the cube's
rotation group — one new wall per self-symmetry of the added cube, which is too
clean to be coincidence.

**Ruled out:** that it is a law of the family — the fit **FAILS at n = 5**
(predicted 3 walls, measured 18), so it is a regime beginning at n = 6
([P122](LEDGER.md#p122)).

**AND IT FAILS AT n = 10 (2026-08-31, [P185](LEDGER.md#p185)).** The regime is a
WINDOW of four rungs, closed at both ends, not a law with a starting point:

    quantity            formula        n=10 predicted   n=10 measured
    walls               24n - 117           123              101      FAILS
    tight conditions    84n - 288           552              482      FAILS
    rank                2(n+1)               22               22      holds
    lineality           n - 5                 5                5      holds

Zero conditions were discarded as degenerate at any rung, so the break is geometric,
not a filter artifact. **The question sharpens rather than closes:** why do rank and
lineality keep their linear growth into n = 10 while walls and tight conditions
break together? The "one new wall per self-symmetry of the added cube" reading has to
explain why the tenth cube contributed 14 tight conditions where each of the previous
three contributed 84 — and note the n=10 configuration is a much less coincident
object than the rungs below it, which [METHODS 6](METHODS.md#6-coincidence-count-is-a-certificate-not-a-compass)
forbids reading as evidence that 3913 is a poor record, but which is the obvious
place to look for the mechanism.

## 5. What surrounds the rational records?

Complete for both 67s (728 and 2 196 faces, best neighbour 63, a cliff of exactly
4). **Unmeasured for every rational record.**

**Ruled out as methods:** full face enumeration (27 walls in ambient 15 is a
nominal 3²⁷ ≈ 7.6 × 10¹² sign vectors; the run died on memory); and the
codimension-1 fallback, because only **1 of 27** walls at 727 can be crossed alone
— 26 are entangled, and the one crossable direction exceeds the engine's overflow
budget ([P122](LEDGER.md#p122)).

**What is known:** 727 is exactly locally maximal under perturbation of its sixth
cube — all 24 combinatorially distinct moves evaluated, best 715
([P125](LEDGER.md#p125)). That is a certificate for one cube's movement, not the
full neighbourhood.

**Needs:** directions crossing a MINIMAL SET of walls rather than one, plus
shorter directions or a wider engine.

## 6. Is 183 maximal at n = 4?

Certified a radius-4 local maximum (recurred 9/40 wide-restart climbs, never
exceeded) but **not proven maximal** ([P15](LEDGER.md#p15)).

**Ruled out as a route:** extension from the n = 3 record. 183 contains no 67 —
67 needs irrational coordinates and every subset of a rational compound is
rational; `extend67.py` confirms from the other side (11 927 configurations, best
177). **Two-cube extension from n = 2 does work**, three ways
([P126](LEDGER.md#p126)).

**Also ruled out:** that 183 is unmeasurable in Cayley coordinates. It contains a
half-turn, but only the PARAMETERISED cubes need finite coordinates — reorder so
the half-turn is the frozen gauge and it measures fine: 12 walls, rank 8,
lineality 1 ([P126](LEDGER.md#p126)).

## 7. How does one SEARCH for irrational records? — method, not conjecture

**Ruled out — sampling.** Random draws of `p + q√d` reach only 137–151 at n = 4
and 319 at n = 5 ([P131](LEDGER.md#p131)). Walls are codimension 1 and records sit
at wall intersections, so a sampler drawing from an open set hits a measure-zero
target with probability 0 ([P132](LEDGER.md#p132)). These numbers characterise the
sampler, not the space.

**Ruled out — three-wall solving against a RATIONAL base.** Every wall then has
rational coefficients, so every three-plane intersection is rational: irrational
solutions cannot arise. Measured: **0 irrational roots of 2 451** over 400 systems
(`irrational_probe.py`, [P49](LEDGER.md#p49)). Corollary, nearly a theorem: **a
cube on ≥ 3 independent walls against a rational base is necessarily rational, so
irrational candidates carry at most TWO coincidences.**

**The remaining construction:** TWO walls plus a QUADRIC. Two rational planes leave
a rational line; a quadric along it gives a quadratic in one parameter with roots
rational or in ℚ(√d). This is how every irrational 727 arose
([P60](LEDGER.md#p60)) and how the 67s arise. **Irrationality is an OUTPUT of wall
solving, not an input to sample over.**

**Untried at n = 4 and n = 5:** that construction against the 13-pair and 67 bases.

## 8. What POINTS toward records? — partially answered

**Refuted as pointers:** coincidence count ("more coincidences implies a higher
count" is in the REFUTED table — 727 has 18 interior crossings to 723's 48 and
counts more); and the SUBSET SPECTRUM, which anti-points — the maximal-spectrum
n = 4 configuration counts 177, six below the record ([P135](LEDGER.md#p135)).

**Partially confirmed:** WALL STRUCTURE ([P139](LEDGER.md#p139)). Over 36 retained
configurations, mean wall labels rise 96 → 107 from peak 175/177 to 179/183, and
overlap with the 183 wall set rises 86 → 96. So it correlates — but it
**SATURATES**: 179 and 183 are indistinguishable (106.9 vs 108.0 labels, 95.6 vs
95.3 overlap). A necessary condition, not a sufficient one; a filter, not a
discriminator.

**ANSWERED 2026-08-19** ([P141](LEDGER.md#p141)): the **CROSSABILITY PROFILE**.
Crossable pairs per configuration fall monotonically with rising count — 8.53
(175), 8.00 (177), 6.55 (179), **3.00** (183) — and do NOT saturate, while the
drop to the best neighbour inverts (2.73 at 179 against 12 at 183). The record is
the MOST DEGENERATE configuration: same wall set as a near-record, but a wall
system blocking more directions. Cheap: 66 exact solves per candidate at n = 4.

*Superseded framing:* what separates a record from a near-record. Nothing measured so far
does. Candidates untested: the wall system's RANK or dependency structure rather
than its size; the shared-wall locus ([P136](LEDGER.md#p136)); the depth-profile
trade ("grow the shallow layers, deep layers pinned", [P15](LEDGER.md#p15)).


## 9. Which member of a continuum extends best? — every rung is a continuum, and every recorded member is at its EDGE

**Measured twice, same answer, same size.** A plateau is one object by count and
many objects by extension:

- 723 continuum at n=7 ([`member723.log`](member723.log)): 8 members → four
  distinct maxima 1203/1205/1209/1211, **spread 8**, not monotone in the parameter.
- 2785 continuum at n=10 ([P181](LEDGER.md#p181)): 9 members → 3905…3913,
  **spread 8**, and the RECORDED member k=56 is the WORST tested, 8 below best.

**Why it matters beyond n=10.** Every rung of the tower was built by extending its
predecessor's *recorded* representative. If those predecessors are continua too,
each rung may be the best extension of an arbitrarily chosen base rather than the
best available — and the gap is 8 at both rungs where it has been measured.

**The shapes were measured, and the headline drawn from them was WRONG
([P182](LEDGER.md#p182), retracted by [P188](LEDGER.md#p188)).** What stands: every
rung from 6 to 9 is a continuum. What does not: the claim that the recorded member
sits at an ENDPOINT of its plateau. It is INTERIOR in every case examined — 1217's
sweep stepped twice the plateau's remaining width, 1895's sweep window began at the
record so nothing below it could be seen, and 2785's lower bound was a window edge.
The "mechanism" offered for the pattern (searches report the smallest primitive
representative, which sits at the boundary) was invented to explain an artifact.

**So the systematic-bias argument is gone entirely.** This section used to argue that
every rung was built by extending a BOUNDARY member of its predecessor's plateau, and
that boundary members extend worst. The first half is refuted ([P188](LEDGER.md#p188))
and the second half was never measured ([P186](LEDGER.md#p186)). Nothing links them.

**Tested, and the test was VOID — [P186](LEDGER.md#p186), 2026-08-31.**
`extend_1217.py` ran seven members of the 1217 plateau, 48 396 evaluations, and
returned **1891 from the recorded base, which provably reaches 1895**. Machinery that
cannot reproduce the known answer produces no valid negatives.

**And this section's own two measurements have the same defect.** `extend_n10.py`
(P181) and `member723.py` use the same random-menu shape and neither could gate on a
known answer — at n=10 there was none. So:

- each per-member number above is a LOWER bound, not that member's maximum;
- **"spread 8" is a difference between lower bounds, which bounds nothing**;
- heights along a continuum vary by two orders of magnitude (4 to 379 on the 1217
  curve), so a single fixed menu is not equally dense around every member, and the
  spread may measure menu fit rather than extension quality.

**Status of the whole question: UNMEASURED.** Both readings — "the recorded member
extends worst" (from P181) and "extends best" (which this campaign appeared to show,
scoring the recorded endpoint highest at 1891) — rest on the same unvalidated
instrument. P181's 3913 stands as a record, since a record needs only a lower bound;
the comparison between members does not.

**What a valid test needs:** a gate that the search reproduces 1895 from the recorded
base (now in `extend_1217.py`, and it would have failed in the first minute rather
than after 8 046 seconds); a menu matched per base; and better, a SOLVE — which
member extends best is a question about coincidences, as
[METHODS 12](METHODS.md) already solves for 13-pair curves.

**Solved, not sampled, would be better.** `twoparam.py` solves for continuum
members admitting a degenerate extension locus, and its answer at both 723 and 2785
was that degeneracy does NOT discriminate — universal along 723, and only cube
duplications at 2785 ([P177](LEDGER.md#p177)). So the selection criterion is
something else: higher-order coincidences, or coincidence types other than 13-pairs.

## 10. Why are the two n=3 maximisers isolated? — explanation WITHDRAWN

[P169](LEDGER.md#p169) offered: free arrangement ⇒ no entanglement ⇒ deficit 0 ⇒
isolated. [P175](LEDGER.md#p175) refuted the chain — the rational 63 is free WITH
deficit 1 — and [P171](LEDGER.md#p171) showed freeness belongs to n ≤ 3 generally,
not to maximality. So the observation stands and the mechanism does not.

**Their isolation is now MEASURED (2026-09-01, [P209](LEDGER.md#p209)):** both 67s are
0-dimensional — preserving rank 0 from a pool spanning the null space and every
cube-slice, 0 unevaluated, in ℚ(√2) and ℚ(√5) respectively. So "isolated" is no longer
a codimension heuristic. WHY they are isolated remains open; that they are is settled.

What survives as fact: both 67s have deficit 0 and every record n ≥ 4 has deficit
≥ 1; χ splits for 13, 63 and both 67s and never above; n=3 is the only irrational
rung and the only one the rational tower cannot reach (63 < 67).

**A version of the chain is back, with the threshold moved one (2026-08-31,
[P184](LEDGER.md#p184)).** Measured with ε a positive infinitesimal, the count-
preserving null directions form a hyperplane in the null space, of dimension
**max(0, deficit − 1)** — not `deficit`, as [P162](LEDGER.md#p162) had it, and not
`0`, as [P175](LEDGER.md#p175) had it. So the link P169 wanted is not "deficit 0 ⇒
isolated" but **deficit ≤ 1 ⇒ no infinitesimal freedom in the null space**, which
covers both 67s (deficit 0) AND the rational 63 (deficit 1) — the very case that
refuted the original chain. It first becomes nonzero at n = 7.

Note this does not conflict with 727 (deficit 1) being a plateau on arcs A–D: those
arcs LIE IN walls — `MAXIMISER_TAXONOMY.md` describes a maximiser arc as lying along
a ruling of the quadric wall it sits in — whereas the null space is the directions
crossing no wall. Two different ways for a count to survive, and only the second is
what deficit measures.

## 11. Does irrationality ever win above n = 3?

Never tested at n ≥ 6. [P138](LEDGER.md#p138) constructed irrational candidates
properly at n=4 and n=5 — 27 716 candidates across 249 fields, and 89 076 across
993 — and found 173 and 377, short by 10 and 16. But its stated scope is "one
rational base per target… other rational bases are untouched", and n ≥ 6 was never
attempted. n=3 proves irrationality can be the whole story (67 needs ℚ(√2) or
ℚ(√5); the rational ceiling is 63), so "never run above n=5" is a real gap — with
two data points already pointing the wrong way.

## 12. What geometric condition makes the clipper emit zero-volume cells?

[P180](LEDGER.md#p180) narrowed it hard and did not close it. Established: the
cells are 1- and 2-face slivers on the `[-4,4]³` box boundary; the trigger is a
property of a PAIR of cubes together with the box, since a rigid rotation of that
pair destroys it while replacing the other cubes entirely does not; the degenerate
set is locally ≥ 6-dimensional. Eliminated: complement disconnection (impossible),
shared face planes, common-line triples, vertex multiplicity — all intrinsic
measures, and the trigger is not intrinsic.

**Now low priority**: [P180 Addendum 5](LEDGER.md#p180) shows the engine's counts
are correct throughout and the guard refuses rather than miscounting, and a global
rotation recovers any refused count exactly. It is a tidiness question, not a
correctness one.

## 13. Where does each continuum actually END? — n=7,8,9 SOLVED; n=10 is a continuum with ends in progress; 183 shows no tangent

[P183](LEDGER.md#p183) audited every continuum in the project against the standard
727 set: through-point, direction, and extent SOLVED as roots of the wall equation
restricted to the arc's line. **Only 727 meets it** — six ends, two exactly rational
(19/6, 43/105) and four algebraic irrationals no grid could land on.

    continuum        path                                  endpoints
    n=2  13          body-diagonal family                  n/a, closed, no ends
    n=4  183         NONE - 2 congruence classes only      none
    n=6  727         arcs A-D, tangents given (D a node)   SOLVED, all six
    n=7  723         u*(1,1,1)                             valid range u>=55, u<=-7/2
    n=7  1217        SOLVED curve (P182)                   grid-sampled only
    n=8  1895        sampled direction, NOT solved         grid-sampled only
    n=9  2785        k-family + 2 solved 13-pair curves    upper measured, lower a WINDOW EDGE
    n=10 3913        none                                  none

> **CORRECTED 2026-08-31 ([P187](LEDGER.md#p187), [P188](LEDGER.md#p188)).** Three rows
> above are wrong. `n78_ends.py` had ALREADY solved both 1217 ends and 1895's upper end
> on 2026-08-08, so this audit missed existing work. n=9's two ends are now solved too.
> And P182's "13-pair curve" for 1217 is not a separate line: its Cayley direction is
> (1,0,0) — the same axis line n78_ends used. Current state:
>
>     n=7  1217   BOTH ENDS SOLVED (n78_ends, 2026-08-08), record INTERIOR
>     n=8  1895   BOTH ENDS SOLVED (P189 — the quartic factors over Q)
>     n=9  2785   BOTH ENDS SOLVED (P187), record INTERIOR, punctured at s=1/56
>     n=10 3913   CONTINUUM — tangent (15,220,86) verified with eps (P190); ends in progress


**Why it is not bookkeeping.** A grid endpoint is the last sampled point that held,
so it is simultaneously a LOWER bound on the plateau's extent and an UPPER bound on
where the wall is — and the gap between them is never zero. [P183](LEDGER.md#p183)
found one such artifact already: 2785's recorded lower end 220/889 is a window edge,
not a boundary, and the continuum runs past it. Endpoints also carry the structural
result — [OQ 9](#9) turns on recorded members being AT endpoints, and that is
measured against sampled ends everywhere except 727.

**The obstacle above n = 8, already on record.** [METHODS 7](METHODS.md) shows the
edge-edge crossing detector that bracketed 727's ends is incomplete at n = 9: the
count steps 2781 -> 2785 between k = 439/8 and k = 55 with the crossing count 294 on
BOTH sides, the wall being a face-plane/triple-point event it cannot see. So ends
above n = 8 need the wall equation itself.

**What it takes.** Nothing new — the computation that produced 727's six ends,
applied to 1217's curve, 1895's two directions, 2785's two 13-pair curves and its
k-family lower end. Establishing a path at all is the open part for 183 and 3913.

## 14. Are P173 and P174 salvageable? — retracted on a premise that has since been overturned

[P175](LEDGER.md#p175) retracted [P162](LEDGER.md#p162), [P173](LEDGER.md#p173) and
[P174](LEDGER.md#p174) on the grounds that "a direction crossing no wall still changes
the count". [P184](LEDGER.md#p184) showed that grounds is **false for n ≥ 7**: measured
with ε a positive infinitesimal rather than steps of 1/1000, the count-preserving null
directions form a hyperplane of dimension max(0, deficit − 1) — 0 of 1 at n=6, 1 of 2
at n=7, 2 of 3 at n=8, 3 of 4 at n=9.

**This does not reinstate them.** Removing the stated reason for a retraction is not
the same as re-verifying the content, and no one has re-checked what P173 and P174
actually claimed. What is suggestive is that P173's arithmetic — "each cube past the
sixth is loose in one direction" — matches max(0, n − 6) exactly.

**What settling it needs:** re-derive P173's and P174's claims against P184's
measurement, direction by direction. Specifically, P174's "the free axis is a body
diagonal" had its AXES computed correctly and only its interpretation withdrawn, so it
is the most likely to survive intact. P162's "the rank deficit IS the plateau
dimension" stays wrong either way — the preserving dimension is deficit − 1.

**UPDATED 2026-08-31, then CORRECTED the same day
([P195](LEDGER.md#p195) -> [P196](LEDGER.md#p196)):** a full-space measurement briefly
appeared to give dimension = deficit, reinstating P162. It did not — that entry counted
vectors without checking independence. By RANK the answer is **deficit - 1** at 1895,
2785 and 3917, confirming [P184](LEDGER.md#p184). P162 stays wrong, and P173 should be
re-read against dimension = deficit - 1 = n - 6.

**Why it is filed rather than done:** it is a re-reading of three entries against a
new measurement, not a computation, and it should be done deliberately rather than
folded into a session that has already overturned four things.

## 15. Why does an added cube contribute rank 2 instead of 3? — **ANSWERED 2026-08-31**

> **ANSWERED by [P206](LEDGER.md#p206), the same day this question was written.**
> `deficit = 1 + sum_j (3 - r_j)` with `r_j` the rank of the wall gradients on cube j's
> own three columns — verified at all eight records. The 727 core has r_j = 3 for every
> cube (fully constrained); every cube added beyond it has r_j <= 2. So the deficit is
> the count of per-cube free directions plus one universal coupling, and the "phase
> change at n = 7" is simply the first rung with an added cube. What remains open is
> the follow-on below.
>
> **Still open:** what determines whether an added cube gets r = 3, 2 or 1? Generic is
> r = 2 (6 of 6 sampled at n=6). The "less constrained wins" reading was REFUTED
> ([P207](LEDGER.md#p207)): the n=6 record is MORE constrained than generic while the
> n=9/10 records are LESS, so there is no consistent direction. What survives is only
> that records are NON-GENERIC in r — four of five off the generic value, and the two
> sitting at it are exactly the two superseded on 2026-08-31, which is confounded with
> their having been found by menu search.

**This is [P205](LEDGER.md#p205)'s reduction of the whole "phase change at n = 7".** A
cube has three degrees of freedom. Up to n = 6 each added cube raises the wall matrix's
rank by 3; from n = 7 it raises it by 2. Since `deficit = ambient - rank` and ambient is
always +3, that single drop is why deficit starts growing — and since
`locus dimension = deficit - 1` ([P184](LEDGER.md#p184)/[P196](LEDGER.md#p196)), it is
also why the maximiser loci stop being points. Three reported phase changes are this
one fact.

**It is NOT a property of n.** Two records at the same n differ in rank: 2785 has 20
and 2787 has 19; 3913 has 22 while 3917 and 3925 have 21. So the drop belongs to
particular configurations, and the records found on 2026-08-31 already violate the
pattern it was read off.

**What would settle it.** The drop means the added cube's wall gradients acquire a
linear dependency on the existing ones in exactly ONE direction. Name that dependency:
compute the wall matrix before and after adding a cube, find the vector in the new
gradients' span that lies in the old span, and read off what coincidence it expresses.
Then ask which added cubes produce it and which do not — 3913 versus 3917 at the same
n is a ready-made pair with different answers.

**Why it is worth doing:** it is concrete linear algebra on matrices already computed
and cached, it explains three observations at once, and nothing else in the file
currently attacks the mechanism rather than the pattern.

## 16. Why does modularity occur at exactly ONE rung?

`393 ⊂ 727` is modular; no other containment in the tower is
([P170](LEDGER.md#p170), proved over 1 192 678 flats). This has been cited as
established context for weeks — including repeatedly on 2026-08-31 — **without ever
being posed as a question**, which is why it is only now in this file.

**What would settle it.** Stanley's modular factorization says a modular flat splits
the characteristic polynomial. The measurement to make is which property of the 393/727
pair supplies the modularity and which property the other pairs lack — rank additivity
was already measured ([P159](LEDGER.md#p159): 11 violations at 727 ⊂ 1217, 0 at
393 ⊂ 727), so the question is what makes those 11 appear.

**Caution.** [P158](LEDGER.md#p158) was retracted after modularity was refuted four
ways at a different rung, so any new claim here needs the same four-way check before it
is believed.

---

*Added 2026-08-31, prompted by "are mysteries open questions?" — the answer being that
they become one only when someone states what would settle them. Of four long-standing
"mysteries" cited in this project, exactly one (§4, the wall law) had ever been
converted. These are two of the other three.*

## 17. Where might a higher record be? — one documented region never searched

*Added 2026-09-01, in answer to "does anything in our data suggest where there may be a
higher record we haven't found?"*

### The strongest lead is an omission, not a pattern

**The whole tower above n = 6 extends ONE POINT of ONE ARC of a four-arc node.** 727 is
a node where arcs A, B, C, D meet ([MAXIMISER_TAXONOMY](MAXIMISER_TAXONOMY.md) §2a);
every record from 1217 upward was built from `BASE + (7,14,1,-5)`, a single member of
arc D. Arcs A, B and C each carry 727 across SOLVED extents —

    A   s in [~2.063979, 19/6]        10 chambers
    B   s in [43/105, ~0.579411]     >=13 chambers
    C   s in [~1.167462, ~47.772089] >=13 chambers

— and **none has ever been used as an extension base**. `which_member.py` was written
on 2026-08-09 for exactly this two-parameter search ("every extension hunt in this
project fixed the (n-1) record at ONE point ... and varied only the new cube"), and its
log is **0 bytes**: never run.

**What would settle it:** run it. Extend members of arcs A, B and C to n = 7 and
compare against 1217. The extents are solved, so the members are enumerable rather than
sampled, and the chamber counts say how many genuinely distinct ones there are.

**Why it is credible rather than merely untried:** [P186](LEDGER.md#p186) established
that which member of a continuum you extend is a real variable — the 723 continuum's
eight members reached four distinct maxima — and [P191](LEDGER.md#p191)/[P198](LEDGER.md#p198)
showed that changing HOW you search beats searching harder. This changes WHERE.

### A quantitative lead, weaker

Ceiling gaps at the current records are 0, 12, 36, 74, 126, 192, 278, 384; second
differences 12, **14, 14, 14**, 20, 20. If the run of 14s were the law, n = 9 would
reach 2793 (+6 over 2787) and n = 10 would reach 3943 (+18 over 3925). The heuristic
flagged n = 9 as low BEFORE 2787 was found — predicting +8, with +2 so far — so it has
one partial hit. It is three-point fitting on a second difference, the exact shape of
[P172](LEDGER.md#p172)'s law that broke, and is OBSERVED at best.

### Where in the profile, and where NOT to look

91% of the ceiling slack is at depth 1 ([P197](LEDGER.md#p197)), and all four n = 10
records found on 2026-08-31 differ only in d1 and d2 with depths 3-10 FROZEN. So a
better record along the current path differs in the outermost layers; moving the
interior needs a different region.

Ruled out by measurement, not by intuition: **the current regions are exhausted** —
2787 and 3925 are locally maximal over saturated facet lists and vertex probes
([P199](LEDGER.md#p199), [P201](LEDGER.md#p201)), so the next record is not adjacent to
either. And **menu search** produced both records superseded on 2026-08-31;
[P186](LEDGER.md#p186) showed it cannot reach what the solved methods reach.

## 18. Is d1 <= 3n^2 + O(n)? — the one loose quadratic

*Stated as a PROPOSITION, not as the task "tighten the ceiling". A task can only be
done or abandoned; a proposition can be settled — by a proof, or by one configuration
exceeding it.*

The bound `1 + sum_l C(l,n)` is the only route to a maximality proof
([P208](LEDGER.md#p208)), and **91% of its slack is at depth 1**
([P197](LEDGER.md#p197)). The depth-1 ceiling is `C(n-1,n) = 10n^2 - 14n`. The records'
d1 is fitted exactly at n = 8, 9, 10 by `3n^2 + 25n - 42`, and within 2 at n = 5, 6, 7:

    n         3    4    5    6    7    8    9   10
    d1       44   92  156  214  278  350  426  508
    ceiling  48  104  180  276  392  528  684  860
    ratio  .917 .885 .867 .775 .709 .663 .623 .591

The ratio decays monotonically: the ceiling's leading coefficient is more than 3x too
large and gets worse with n.

**Caution on the fit.** It describes RECORDS, which are lower bounds, and being exact
at three consecutive rungs is the shape of [P172](LEDGER.md#p172)'s wall law that broke
at the fourth. Its value is naming the leading coefficient a proof should target — not
asserting the maximum.

### What would settle it

- **A proof using CONCENTRICITY.** A depth-1 point lies in exactly one cube and outside
  all others; but every cube contains the shared centre, so such points are necessarily
  far from it, near the corners and edges of a single cube. The present bound treats
  the other cubes' faces as generic planes cutting a cube and does not use the shared
  centre at all. This is the most specific unexploited constraint.
- **A counterexample:** any configuration with d1 above the claimed form.
- **BOTH live routes converge on CONCENTRICITY.** The depth-1 ceiling treats the other
  cubes' faces as generic planes cutting a cube; the increment bound
  ([MAXIMISER_TAXONOMY §5](MAXIMISER_TAXONOMY.md)) bounds the added cube's surface
  cells the same generic way. **Neither uses the one geometric fact peculiar to this
  problem: every cube shares a centre.** That is the single unexploited constraint
  behind both routes, and it is why they are not independent attacks.
- **Prerequisite either way:** `C(l,n)` is PROVED only for l = 1; l >= 2 is empirical
  over ~1M configurations. Until that is proved the sum is not an upper bound and any
  refinement of it refines a conjecture.

### Related, and NOT this question

Two other routes to a smaller bound are PLANS, and belong with their questions or in
[MAXIMISER_TAXONOMY §5](MAXIMISER_TAXONOMY.md) rather than here: replacing the sum of
independent per-depth maxima with a joint trade-off constraint (no linear relation
exists — the alternating sum runs 7, 27, 49, 77, 85, 97, 109, 111, 123, not constant),
and sharpening the recursion `max(n) <= max(n-1) + max Delta`, whose increment bound is
PROVED but currently looser than the depth sum.

---

*A note on this file, measured 2026-09-01: only **5 of 17** entries state what would
settle them, and all five were written in the two days after that test was articulated.
The other twelve are mysteries in question clothing — citable indefinitely, answerable
never. Converting one costs a paragraph; the conversion is what turns a standing
observation into something that can be closed.*

## 19. Is there an exchange rate between CONSTRAINTS and COUNT, and does it bound the record?

**The hope (user, 2026-09-01).** If some indicator of a count's rarity — the volume that
climbs to it, the height of its representatives, the number of conditions it satisfies —
varied with the count and ran out not far above the record, that would hint there is
little room to beat the record. And if beating a record demands several individually rare
conditions, their conjunction should be rarer still. Search yields lower bounds forever;
an indicator that runs out is an UPPER-bound argument, which is what this project cannot
obtain by searching.

**What was measured, and what it rules out.** `rarity.py` computed, for 20 distinct
terminal counts at n=4, the number of tight conditions, the null dimension, and the
eps-verified preserving rank. **The dimension is NOT a function of the count**: count 123
occurs at rank 7 and at rank 9; count 127 at rank 4 and at rank 7. So there is no curve
d(c) to extrapolate, and the naive form of the idea does not start.

**The form that does start.** Index by constraint rather than by count:

> **K(c) = the minimum codimension of any configuration achieving count ≥ c.**

Non-decreasing by construction. At n=4 both ends are measured: K(c) = 0 for c ≤ **136**
(full-dimensional configurations exist at 111, 120, 123, 128, 131, 132, 135, 136), and
K(183) = 9 = the ambient dimension, because 183 is 0-dimensional ([P204](LEDGER.md#p204)).
So K rises from 0 to the ambient over 47 counts — about **5.2 counts per constraint** —
and reaches the ambient exactly at the record.

**Why that is an upper bound if it holds.** A count needing codimension greater than
3(n−1) is over-determined: no configuration can satisfy the conditions. So the count at
which K reaches the ambient dimension bounds the record from above. At n=4 that is 183,
which IS the record.

**And it says n=9 has room.** 2787's region has rank 4 in ambient 24, so it is NOT
maximally constrained — four constraints of headroom remain. At the rate implied by its
own endpoints, (2787 − 2491)/20 ≈ 14.8 counts per constraint, that headroom is worth
about **+59**, suggesting ~2846 is reachable at n=9.

**To settle it, three things are needed and none is expensive:**

1. **K(c) in the middle.** Both measured points are at the extremes (codim 0 and codim
   ambient). The interior is unsampled because climbs terminate at low codimension. Needs
   configurations of intermediate codimension — the region boundaries of known records.
2. **Whether the rate 5.2 is n-dependent in a stable way.** Provisionally
   (record − GPD endpoint)/codim gives 5.2, 7.1, 7.8, 10.2, 14.8, 16.2 at n = 4, 6, 7, 8,
   9, 10 — roughly 1.5n — but each uses the endpoint estimate, which
   [P215](LEDGER.md#p215) says is the non-robust half of that fit.
3. **The counts ON the walls.** *Corrected 2026-09-01 — the first version of this item
   said "every walk steps ACROSS a wall, which lowers codimension". That is false for the
   climber that found the records, and the user caught it.* `climb.py` with `menu=None`
   takes its directions from the null space of the TIGHT walls, each `count_eps`-verified
   to PRESERVE the count, so it walks ALONG the stratum — along the walls it is already
   on — until the count changes at a wall WITHIN that stratum. The codimension is
   preserved across the move, measured twice independently: 3921 (deficit 6) → 3925
   (deficit 6). Only the BASIN climber (isotropic menu, no preservation) crosses
   transversally into near-generic chambers, and generalising from it was the error.

   What is true, and is the point: the accepted configuration is just PAST the wall, never
   ON it. A point on that wall has codimension one HIGHER than either cell beside it, and
   **no count in this project has ever been taken there** — yet that is where the
   constraint argument says records live, 183 being an intersection rather than a chamber.

   **And this explains the headroom.** Because the record climb preserves codimension by
   construction, it *structurally cannot* reach a more constrained configuration. That is
   why 2787 sits at rank 4 in ambient 24 with four constraints unspent while the climb
   reports local maximality over 36 of 36 rays: the headroom lies in the one direction the
   method cannot travel. Landing on the walls is the only way to spend it.

   `onwall.py` evaluates W4 walls exactly — their roots lie in ℚ(√d), so `count_at` needs
   no rational approximation; W3 walls are quartic and are skipped and counted as skipped.

**The conjunction half of the idea is untested.** If beating a record requires several
conditions that are individually rare, the joint rarity should be estimable from the
individual ones — but only if the conditions are near-independent, and
[P206](LEDGER.md#p206)'s `deficit = 1 + Σ_j (3 − r_j)` says the per-cube contributions add
exactly, which is evidence FOR independence and worth pressing.

## 20. Why does the engine refuse, when it refuses silently?

60 census refusals at n=4, **all producing no stderr at all**, so the degenerate-vs-budget
classifier in `census.py` never fired and every one is recorded as `other`. Heights run 6
to 1748 — far below any overflow threshold — which rules out the budget explanation and
leaves genuine degeneracy (coincident cubes, a non-generic plane triple) as the likely
cause. **ANSWERED 2026-09-05, and it is neither hypothesis.** The engine reports
`{"error": "outside must be a single region"}` in **stdout as JSON**, exiting 0, with
stderr empty — so the classifier, which read stderr, could never have fired. All 65 are
that one error. It is the engine's own internal consistency check (the unbounded exterior
should form a single region), not degeneracy and not overflow: heights are 78–108 and
duplicate cubes were tested directly and count fine (bounded = 63, exit 0).

So these configurations are unevaluated for a reason internal to the counter, which means
they could sit anywhere in the count distribution and the census cannot say. 65 of 556 746
is 0.012 %, small enough not to bias the measurements above, and worth reporting as an
engine issue rather than a property of the space. Classifier fixed to read the JSON error
field.

Rate by ensemble: `twoaxis` 25, `project` 23, `haar` 9, `axis` 2 — the more structured the
ensemble, the more it refuses, which is what makes the answer interesting rather than
housekeeping. If these are degeneracies then the census is discarding exactly the
high-coincidence tail that records inhabit; if they are something else, the ensembles are
generating malformed input and the sample is biased in an unknown direction.

## 21. Does the Möbius-weight predictor PAY, or only predict? — **CLOSED 2026-09-07: it does neither**

> **The question is void, not answered.** [P222](LEDGER.md#p222)'s predictor was computed
> from face normals taken as matrix ROWS rather than COLUMNS — the inverse rotation of every
> cube. Recomputed correctly it scores **r = −0.147** and orders **50.6 %** of 3 320 pairs: the
> correlation changes sign and the ordering is chance. There is nothing to make pay. See
> [P227](LEDGER.md#p227) and [FAILURE_MODES 27](FAILURE_MODES.md).
>
> **ANSWERED 2026-09-07 by [P231](LEDGER.md#p231), and the answer is yes.** All three were
> re-measured on the full 3.1M-row census. **Max plane-concurrence orders 61.1 % of pairs**
> (124 753 pairs, ~78σ from chance) — the one statistic nobody had re-measured. The raw real
> incidence count is marginal at 54.3 %; the Möbius weight, which [P222] crowned, is chance
> at 51.5 %. And it PAYS: [P223](LEDGER.md#p223) is reversed.
>
> *I wrote "there is no predictor" above on the strength of re-measuring one of the three.
> The other two were unevaluated, and I scored them as negatives.*

~~[P222](LEDGER.md#p222) established `Σ over real, face-bounded incidence points of
(m−1)(m−2)/2` as the best count predictor this project has (r = 0.562, orders 77.6 % of
arbitrary pairs, no engine call). It is characterised and **not yet used**.~~

The obvious use is a filtered census: generate cheaply, count only the top decile by
weight. But "no engine call" is not the same as "cheap" — the statistic needs C(6n,3)
exact 3×3 solves, which at n=4 is 2 024 of them, and the concurrence filter died on
exactly this arithmetic (0.050 s against a count's 0.043 s). **The cost must be measured
before the filter is built**, or this repeats [P222]'s mistake one level up.

~~If it is not cheaper than counting, the statistic still has a use that does not depend on
being cheap: as a **search objective**. A walk can hill-climb on Möbius weight with no
engine in the loop at all and count only its endpoints — which is a different economics
from filtering, and is the one place a 77.6 % predictor that costs a count could still pay.~~

*Struck 2026-09-07. Hill-climbing on a 50.6 % objective is a random walk with extra steps.
The idea itself — an engine-free search objective, counting only endpoints — survives the
statistic it was attached to, and is worth re-raising if any statistic ever clears chance.*

## 22. Does an n=5 base's own count predict how well it extends? — **CLOSED 2026-09-07: no, and nothing else measured here does either**

[OQ 9](#9) asks which member of a *continuum* extends best. This is the same question asked
across a *tier*, and the n=5 family makes it answerable exactly rather than by sampling:
[P228](LEDGER.md#p228) shows the 76 bases counting ≥385 are **11 congruence classes**, one at
393 and **ten at 387**. Ten distinct compounds with identical n=5 counts is a controlled
comparison that does not usually exist here.

Each is being extended against the same 43 707-cube menu ([P229](LEDGER.md#p229)). Partial,
4 of 11:

| base | n=5 | n=6 max | cubes at max | median | bulk top | escape |
|---|---|---|---|---|---|---|
| 0 | **393** | **727** | 6 (2 classes) | 689 | 723 | +4 |
| 1 | 387 | 725 | 3 (1 class) | 679 | 713 | **+12** |
| 2 | 387 | 717 | 199 | 681 | 717 | 0 |
| 3 | 387 | 717 | 246 | 681 | 717 | 0 |
| 4 | 387 | 723 | 3 (1 class) | 681 | 717 | +6 |

**Already visible, and it is not what I expected.** The ten 387s do **not** extend alike:
725, 717, 717, 723 so far — an 8-region spread among compounds that are indistinguishable by
their own count. So the n=5 count does not determine extension quality — which is the useful half
of the answer, since it means a search that ranks bases by their own count is discarding
information.

**Three things it may still turn out to be**, and the data will separate them:

1. **The shape of the top differs.** The record base's maximum is ISOLATED — 6 cubes, 2
   congruence classes — while bases 2 and 3 have 199 and 246 cubes tied at theirs, dropping
   to 12 and 3 at the next value down. Isolated peak vs. broad plateau may be the real
   distinction, not the peak's height.
2. **Peak and bulk disagree.** Base 1 has the higher peak (725) and the LOWER median (679);
   bases 2/3 have lower peaks and higher medians (681). "Extends best" is two questions.
3. **Escape above the bulk.** Defined as max minus the highest count reached by ≥100 menu
   cubes. *Two caveats, and the second is the more damaging.* First, the ≥100 threshold was
   chosen after seeing bases 0–3, so those four are in-sample and only bases 4–10 test it.
   Second — noticed at base 4 — **escape and isolation are very nearly the same
   measurement, not two.** If the maximum is attained by fewer than 100 cubes it cannot be
   the bulk top, so `escape > 0` follows almost mechanically from `cubes at max < 100`.
   Points 1 and 3 are therefore one observation counted twice, and the table's `cubes` and
   `esc` columns are not independent evidence. What is NOT mechanical is how far the escape
   goes once it happens (4, 12, 6 so far), and that is the part worth watching.
   The obvious theory — the record base is the one that escapes its plateau — is already
   refuted either way, since base 1 escapes by 12 against base 0's 4.

**A structural property that DOES separate them, and a prediction registered before its
test ran.** Each base's own symmetry group — the global rotations carrying the compound to
itself, computed exactly by the `congruent.py` construction — is:

    bases 0-6, 8, 9   order 3
    bases 7 and 10    order 12

Two of the ten 387-compounds are four times more symmetric than the rest, at identical n=5
count. **Prediction, written 2026-09-07 while bases 7 and 10 were still unrun:** their
winning cubes must come in orbits of the order-12 group, so the number of cubes at their
maximum should be a sum of divisors of 12 (12, 6, 4, 3, 2, 1) rather than the 3+1 pattern
seen everywhere else — and the ratio of cubes-at-max to congruence-classes-at-max should be
correspondingly larger. If instead they behave like the order-3 bases, the symmetry does not
reach the extension and this line is dead.

**CONFIRMED on base 7 — then REFUTED on base 10, which is why it was registered.**

Base 7 (order 12) put **12 cubes at its maximum of 721 in exactly ONE orbit, one congruence
class** — ratio 12:1 against the order-3 bases' 3:1. Base 10, also order 12, put **368 cubes
at its maximum of 717 in 90 orbits**, behaving like the low-symmetry wide-plateau bases 2 and
3 rather than like base 7. **One for two. The claim that higher symmetry concentrates the
maximum is dead.**

*And half of what I wrote as a prediction was not one.* "Orbit sizes are divisors of 12" is
Lagrange's theorem — forced, untestable, and it dressed a tautology as a result. The only
testable part was the non-obvious bit: that a more symmetric base would have a CONCENTRATED
maximum, few orbits. That is the part base 10 killed. A prediction whose confirming
observation could not have come out otherwise is [FAILURE_MODES 2](FAILURE_MODES.md), a gate
that cannot fail, wearing a prediction's clothes.

**What survives is narrower and is the reframing, not the prediction.** How many cubes attain the
maximum is mostly a statement about the base's symmetry, not about the extension. The
invariant quantity is **congruence classes at the maximum**, which is 1 or 2 for every base
measured so far. Stated that way the sweep says something much simpler than the raw counts
did: *each n=5 base has essentially ONE best sixth cube, up to congruence.*

*Orbit structure already confirms the mechanism on the order-3 bases: base 5 has 4 cubes at
its maximum in 2 classes, which is one C3 orbit of size 3 plus one cube FIXED by the C3 (its
axis is the base's own symmetry axis) — 3+1, not 2+2. I first guessed base 5's stabiliser
must differ from the others'. It does not; it is order 3 like them.*

## CLOSED 2026-09-07 — all eleven rows

| base | n=5 | n=6 max | cubes | orbits | median | bulk | esc | sym |
|---|---|---|---|---|---|---|---|---|
| 0 | **393** | **727** | 6 | 2 | 689 | 723 | 4 | 3 |
| 1 | 387 | 725 | 3 | 1 | 679 | 713 | 12 | 3 |
| 8 | 387 | 723 | 1 | 1 | 681 | 713 | 10 | 3 |
| 4 | 387 | 723 | 3 | 1 | 681 | 717 | 6 | 3 |
| 5 | 387 | 723 | 4 | 2 | 683 | 717 | 6 | 3 |
| 6 | 387 | 723 | 3 | 1 | 681 | 717 | 6 | 3 |
| 7 | 387 | 721 | 12 | 1 | 681 | 717 | 4 | **12** |
| 9 | 387 | 719 | 6 | 2 | 683 | 717 | 2 | 3 |
| 2 | 387 | 717 | 199 | 121 | 681 | 717 | 0 | 3 |
| 3 | 387 | 717 | 246 | 136 | 681 | 717 | 0 | 3 |
| 10 | 387 | 717 | 368 | 90 | 683 | 717 | 0 | **12** |

**480 777 configurations, zero refusals, and the duplicate-cube gate ([METHODS 24]) passes on
all eleven.**

**The answer, in three parts.**

1. **The n=5 count does not determine extension quality.** Ten compounds with identical n=5
   counts extend to 717, 717, 717, 719, 721, 723, 723, 723, 723, 725 — a spread of 8. A
   search that ranks bases by their own count is discarding information.
2. **But the record base is still the unique best extender here.** Only base 0 reaches 727,
   and it is the only one above 725. So at this rung the count *is* the right ranking at the
   top even though it is not a ranking in the middle — which is a sharper form of what
   [OQ 9](#9) asks along continua.
3. **Nothing measured here separates the ten 387s in a way that predicts their extension.**
   Symmetry order does not (bases 7 and 10 are both order 12 and land at 721 and 717, the
   best and the worst of the tier). Median does not (683 belongs to bases 5, 9 and 10, which
   reach 723, 719 and 717). `esc` and `cubes` are two views of one thing and both are
   downstream of the answer rather than upstream of it. **The tier is flat to every statistic
   tried, and extension quality is not yet predictable from the base.**

**What it does not cover.** The menu is a lattice quotient: every row is exhaustive over a
stated family and a sample of SO(3) ([METHODS 1](METHODS.md)). A base that extends badly here
may extend well elsewhere, and nothing here bounds n=6 above 727.

**What it cannot answer.** The menu is a lattice quotient, so every row is exhaustive over a
stated family and a sample of SO(3) ([METHODS 1](METHODS.md)). A base that extends badly here
may extend well elsewhere.

---

*Entries 23–28 were raised in conversation on 2026-09-07 and written here the same day,
because a question that lives only in a transcript is not an open question — it is a lost one.
Each names its target, why it matters, and what would close it.*

## 23. Is the depth profile itself gated? — the instrument under everything from [P236] on

Every identity of 2026-09-07 — the per-level Euler count, the two-body/three-body split, the
cross-level identity — is checked against `by_depth` from `cube_regions_n`. **That output has
never been gated independently of the engine producing it.** The region COUNT has two
independent engines agreeing; the per-depth breakdown does not.

Equally: `segments()` and `on_bdry_params` from `euler3`/`cellcomplex` underpin every arc and
vertex computed. They were written for a different purpose and were never checked against a
case with a known answer.

**What would close it.** A configuration whose depth profile is known by hand — the axial fan
(`(2N−1)²` bounded regions, proven) or two cubes about a body diagonal (13 = 12 + 1) — run
through the same pipeline. Cheap, and it is the anchor outside the procedure that this whole
line lacks.

## 24. Do the by-level identities survive n = 9 and n = 10?

[P243] and [P245] are verified at n = 4, 5, 6 only. The n = 9 and n = 10 records have height
415 and 6555 and arrangements an order of magnitude larger, and they are the coincidence-rich
cases where a generic-position argument is likeliest to fail — which is precisely how [P235]
found the published `d1` bound invalid at maximisers.

**What would close it.** Run `v3_outer.py`'s level decomposition on the n=7..10 records. The
prediction is that `d_ell = E_ell − V_ell + c_ell + 1` still holds exactly and the two-body term
is still zero for `ell >= 2`.

## 25. Is `m_v <= 3` real, or a four-configuration artifact?

[P245] reports that a vertex spans at most three depth levels, on the strength of **four
configurations**. That is the exact shape of the [P233] error — a small, partly nested sample
reported as a law — committed the same day it was documented. If `m_v` is unbounded the
cross-level identity still holds but its use as a constraint weakens.

**What would close it.** The census, which has 3.1M configurations and costs nothing to scan.
A derivation would be better: `m_v` should be bounded by how many distinct depths the regions
around one vertex can take, which is a local question about `b` bodies meeting at a point.

## 26. Does radius-signature injectivity survive a HARD control at n >= 3?

[P241] tested collisions densely on PAIRS (44 295, zero non-congruent collisions) and by two
constructions, one of which — chirality — is provably empty. But at n >= 3 the only test is
**600 random census draws**, the convenient control. Structured and near-degenerate
configurations are where collisions should be sought: shared axes, repeated angles, families
with equal pair multisets assembled differently.

**What would close it.** Either a collision, or a derivation that the radius multiset
determines the compound up to rotation. For pairs the latter is a concrete algebraic question
about separating double cosets.

## 27. Does the charging argument give a TIGHTER bound at depth >= 2?

[P243] shows the two-body term vanishes for `ell >= 2`, so `d_ell <= 108*C(n,3) + 2` is proved
there. But that constant was derived for depth 1, where a triple point need only be outside
every other body. At depth `ell` it must also lie INSIDE `ell−1` others — a strictly stronger
condition that the count `216*C(n,3)` ignores entirely.

**Why it matters.** The conjectured caps are far below the proved bound (`d2 <= 66` against
434 at n=4), and [P243] reduced that conjecture to `3-body gain <= C(n−ell,n) − 2`. Exploiting
the inside-`ell−1` condition is the obvious route and nobody has tried it.

## 28. What forces `m_v = 2`? — **ANSWERED 2026-09-07: `m_v = b_v − 1`, [P248](LEDGER.md#p248)**

> Not a bound but an equality, zero violations at n = 4, 5, 6 on records and Haar draws, with
> a local geometric reason. `TOTAL = E − Σ_v (b_v − 1) + 2L + 1`. The open question that
> replaces it: **is `E − V2 − 2·V3` boundable where `E` alone is not?**

`TOTAL = E − Σ_v m_v + Σ_ell (c_ell + 1) + 1` is exact. `E` is boundable by plane-triple
counting. Since `m_v >= 1`, this gives `TOTAL <= E − V + Σ(c+1) + 1` immediately — but that is
weak, because most vertices in practice have `m_v = 2` and the bound assumes none do.

**A lower bound on `Σ_v m_v` is the only missing piece between the identity and a real cap on
the total count** — the first route this project has to bounding a whole profile rather than
one layer. The question is local: given `b` bodies meeting at a vertex with `s` of them
containing it, how many distinct depths must the incident arcs realise?

*Related and now known: `c_ell = 1` is NOT universal — 47 of 1 500 level-instances have
`c_ell != 1`, up to 16 ([P245] correction). Any closed form substituting 1 is generic-only.*


## 29. Prove the ceiling law for l >= 2 — now an EQUALITY question, not a bound

[P250](LEDGER.md#p250) reframes it. The deep caps are attained by 577 of 658 configurations at
n=5 and 576 of 657 at n=7, so the conjecture is not "d_ell is bounded by C" but "**the generic
value of d_ell IS C, and coincidence only reduces it**".

**Two halves, both more tractable than a bound.** (a) In general position every level-ell
vertex is a simple triple point, so `d_ell = V3(ell)/2 + c + 1` — an exact count of triple
points inside exactly `ell-1` cubes. (b) Coincidence reduces: merging vertices consumes
plane-triples faster than it adds gain, the convexity [P237] already used.

**Worth:** collapses max(4) from [183, 953] to [183, 195]. **Caveat:** the bound stays loose at
ell = 1 (104 against a measured max of 96), so even a proof leaves 12 regions undetermined —
exactly the frustration of [P242].

**HALF THE ROUTE IS DEAD ([P252](LEDGER.md#p252)):** coincidence does NOT locally reduce V3 —
a coincident configuration can exceed a neighbouring perturbed one by +4 — so "check ΔV3 across
each wall type" cannot close it. The bound still holds (0 exceedances of the formula in 3 330 +
600 instances); the reason is global, not local. The generic computation below is unaffected.

**FIRST STEP TAKEN 2026-09-07 ([P251](LEDGER.md#p251)).** The conjecture is equivalent to
`V3(ell) = (24l-12)n - 4l^2` on the arrangement, l = n-ell. Never exceeded at any n or l, and
EXACT in general position for l = 1 (which is the already-proved case, so the restatement is
calibrated against a theorem) and for l = 2 (30/30 at n=7). **The next theorem to attempt is
`V3(l=2) = 36n - 16` in general position** — the first new one on this route.


## 30. Bound `c_ell` above — the last ingredient for a proved n=4 cap

[P258](LEDGER.md#p258): `TOTAL = T + two-body + Σ_ell (c_ell + 1) + 1`, with `T <= 32*C(n,3)`
PROVED (PROOF_67 Lemma 1a per 3-subset) and `two-body <= 10*C(n,2)` PROVED ([P237]). The only
unbounded term is `c_ell`, the number of connected components of the level-ell curve
arrangement.

**Observed:** `c_ell = 1` in 1 381 level-instances, `= 2` in 8, nothing higher on
non-degenerate configurations ([P245] correction, [P246] for why degenerate ones are excluded).

**Worth:** with `c_ell <= 2`, `max(4) <= 198`; with `c_ell = 1`, 195 — matching the ceiling law
but PROVED, and collapsing the interval from [183, 953] to [183, 198].

**REDUCED 2026-09-07 ([P259](LEDGER.md#p259)) to a connectivity claim.** Every cube is
centrally symmetric, so the arrangement is invariant under `x -> -x`, a fixed-point-free
involution that PERMUTES components. Measured: `c=1` in 1 924 instances (component always
self-antipodal), `c=2` in 8 (always an antipodal image pair), `c>2` never. So

    c_ell = (# self-antipodal components) + 2*(# antipodal pairs)

and the question becomes: **is the QUOTIENT arrangement, modulo the antipodal map,
connected?** If yes, `c_ell <= 2` follows and [P258] gives `max(4) <= 198` PROVED. That is a
connectivity claim about one object, not an enumeration — and connectivity of an arrangement
on a sphere is what Euler arguments are for.



**SHARPENED 2026-09-08 ([P268](LEDGER.md#p268)).** The dichotomy is NOT a parity fact and
must not be argued as one. Central symmetry gives `c_ell = (# self-antipodal) + 2·(# pairs)`
— verified on actual components with zero unmatched — and that permits `c = 3` (one
self-antipodal plus one pair), `c = 5`, and every odd value. So `c ∈ {1,2}` is precisely the
claim that the quotient level graph mod `±` is CONNECTED, and nothing weaker will do.

**AND NOT BY GENERAL POSITION ([P269](LEDGER.md#p269), 2026-09-08).** All 37 known valid
`c > 1` instances are NON-degenerate and identity-valid, with no shared face plane, no
perpendicular face normals, no face normal parallel to a body diagonal and no shared body
diagonal — `other coincidences: NONE` on every one. So **any argument of the form "assume
general position, therefore `c = 1`" is already refuted.** `c = 2` is a Z/2 monodromy fact
(the antipodal double cover being trivial), not a coincidence; on the degenerate locus the
Euler identity itself fails in 195 of 197 level-instances, so values read there are not
values of `c`.

**What the data narrows it to.** `c ≥ 3` occurs 0 times in 418 non-degenerate level-instances
(and 0 in [P245]'s 1 389), and every instance found on the plane-degenerate locus has the
shape `1 self-antipodal + 1 pair` with the detached pair TINY — 4 or 6 nodes against a main
component of 84 or 130. So the question to settle is: **can a small antipodal pair of
components detach from a level graph without two cubes sharing a face plane?** A proof should
target the smallness, not the count.

## 31. Prove `Σ_T d₂(T) ≤ 48 + d₃` at n=4 — **CLOSED 2026-09-07: PROVED, for all n ([P266](LEDGER.md#p266))**

[P262](LEDGER.md#p262): at n = 4 this single inequality implies `d1 <= 104`, `d2 <= 66`,
`d3 <= 24` — the entire ceiling law — and hence **max(4) <= 195**, collapsing the interval from
[183, 263] to [183, 195].

**Two independent routes both need exactly 84.** Through the level chain, `W_1 <= 44` is proved
so `V3(2) <= 128` needs `W_0 <= 84`. Through the two-body decomposition,
`d1 = V3(1)/2 + two-body + c + 1` with `two-body <= 60` proved gives `d1 <= 104` iff
`V3(1) <= 84`. The same constant in both, exactly.

**Evidence:** attained by the record, never exceeded in ~200 draws across three ensembles
([P254]), and 3.1M census configurations never exceeded d1 = 96 which is consistent.

**Convergence:** this is the quantity [P253] reached from the refinement side and [P254] from
the record side. Three lines, one inequality.

**SHARPENED 2026-09-07 ([P263](LEDGER.md#p263)):** `W_0 = budget - W_1` exactly, with
`budget <= 128` (PROOF_67 per 3-subset) and `W_1 <= 44` PROVED. Measured on 1 449
configurations having the full budget: `W_0 = 84` in 1 441, never above. **So the open part is
now a LOWER bound on `W_1`** — equivalently `d_3 >= 24`, the generic value, attained by 75 % of
the census. Raising `W_0` requires lowering `W_1`, which lowers the budget too: the route is
self-defeating, which is why no violation exists.


*(OQ 31 restated 2026-09-07 by [P264](LEDGER.md#p264): `V3(depth 1) <= 84` is equivalent to
`Σ over the four 3-subsets of d2(T) <= 48 + d3(full)`, a relation between subset region counts
and one number from the whole. Zero violations in 3 599 configurations, tight in 2 351, and
every configuration whose subsets all attain `d2 = 18` has `d3 = 24`. Both sides are counts the
engine computes directly.)*


## 32. What determines `W₀`? — **REFRAMED 2026-09-08 ([P272](LEDGER.md#p272)): `W₀ = budget − W₁`, and the target is deficit domination**

[P266](LEDGER.md#p266) proves `Σ_T d₂(T) ≤ 48 + d₃` (Theorem S) for all n. That was
[OQ 31]. But [OQ 31] existed to deliver `V3(depth 1) = W₀ ≤ 84`, and the conversion runs
through `W₀ = budget − W₁` ([P263]) with `W₁ = 2(d₃ − 2)` used as an EQUALITY.

**The equality fails.** `exceptions.log` records a configuration with `W₁ = 40` and `d₃ = 24`,
where `2(d₃ − 2) = 44`. The implication as written needs `W₁ ≥ 2(d₃ − 2)`, and there it is
false by 4. `W₀ = 82 ≤ 84` on that configuration anyway — because the budget dropped by more
than `W₁` did — so the CONCLUSION survives while the argument does not.

**Why this is narrower than what it replaces.** `W₁ = 2(d₃ − 2)` is `d₃ = V3(3)/2 + c₃ + 1`
with `V3(3) = W₁` and `c₃ = 1`: it is an instance of the per-level Euler identity ([P243]),
exact whenever the depth-3 level is generic and connected. It is exact on 1 441 of the 1 449
budget-attaining configurations of [P263]. So this is a degeneracy-and-connectivity question
about ONE level, overlapping [OQ 30], not a new inequality.

**What would settle it.** Either (a) prove `W̅₀ ≤ 84` directly from Theorem S without passing
through `W₁` — the budget and `W₁` drop together, which is the same coupling Theorem S is
about; or (b) bound the defect `2(d₃ − 2) − W₁` above by the budget's own defect. Both are
statements about coincident triple points, not about components.

**Status:** open, 2026-09-07. With [OQ 30], the last thing between the project and a proved
`max(4) ≤ 195`.


*(OQ 32 widened 2026-09-08, [P271](LEDGER.md#p271). The framing above — "a degeneracy-and-
connectivity question about ONE level", resting on `W₁ = 2(d₃−2)` being exact on 1 441 of
1 449 — was measured on [P263]'s BUDGET-ATTAINING slice, which is not generic. On 247 blind
non-degenerate n=4 configurations the step `W₁ ≥ 2(d₃−2)` fails ~~17 times, 6.9 %~~ — **that
rate was the POOL; corrected 2026-09-08 by [P272](LEDGER.md#p272) to 2 of 211 (0.9 %, worst
deficit −4) on genuinely simple configurations and 15 of 36 (41.7 %) on coincident ones.** It
still breaks from the genericity side, not the `c_ℓ` side, so it is not an [OQ 30] overlap.*

*The CONCLUSION is unharmed: `W₀ ≤ 84` was not violated once in those 247 draws, and is
exactly attained at the record alongside Theorem S. So the target stands and one route to it
is gone. What is needed is a derivation of `W₀ ≤ 84` from Theorem S that does not pass through
`W₁` — the budget and `W₁` fall together, which is the same coupling Theorem S is about.)*


*(OQ 32 reframed 2026-09-08, [P272](LEDGER.md#p272), after the user's redirection: "it may not
matter [what causes c>1] if we can find what determines W₀".)*

**What `W₀` is.** Exactly the `(3,3)` class of the level-1 graph — triple points on the outer
boundary where three cube boundaries meet transversally. `d₁ = W₀/2 + (n₂₄ + 2n₂₆) + c + 1`
exactly, which is [P243]'s identity with its vertex classes named.

**The reduction.** `W₀ = budget − W₁` holds directly (both sides raw triple-point counts, no
`d₂`/`d₃` conversion), and `W₁ = 44` — its proved cap — in 10 of 12 configurations checked.
**Whenever `W₁ = 44`, `W₀ ≤ 84` follows immediately from `budget ≤ 128` (PROOF_67 Lemma 1a).**
So the open part is only the case `W₁ < 44`, and it restates as

    Σ_T (32 − V₃(T))  ≥  44 − W₁

— the budget deficit dominates the swallowing deficit. **This is the same shape as Theorem S**
(`Σ_T (18 − d₂(T)) ≥ 24 − d₃`), one level down in the vertex/region correspondence, and
Theorem S is proved. Trying [P266]'s technique — a fixed witness set that survives
intersection, plus monotonicity — on the vertex version is the concrete next move.

**Status of the old framing.** The `W₁ ≥ 2(d₃−2)` step fails 2 of 211 on genuinely simple
configurations (worst −4) and 15 of 36 on coincident ones (worst −16). Rare but real. The
CONCLUSION `W₀ ≤ 84` was violated 0 times in all 247 and is attained at the record.


*(OQ 32 sharpened again 2026-09-08, [P274](LEDGER.md#p274).)*

**The last link dissolves, and what it dissolves into is false.** The level-3 anatomy gives
`W₁ = 2(d₃ − τ₃ − c₃ − 1)` exactly (τ₃ = the two-body weight at depth 3), so

    W₁ ≥ 2(d₃ − 2)   ⟺   τ₃ + c₃ ≤ 1   ⟺   τ₃ = 0 AND c₃ = 1

and **both conjuncts fail on real, simple, non-degenerate configurations** — `c₃ = 2` at the
[P271] witness, and `τ₃ = 2` in 3 of 263 (refuting [P243]'s "two-body term identically zero at
ℓ ≥ 2"; [P243] corrected in place). The two simple step-failures of [P272] are `τ₃ = 2` cases,
not `c₃` cases.

**What IS proved:** `W₀ ≤ 82 + 2(τ₃ + c₃)`, 0 violations in 263, equal to 84 exactly when
`τ₃ = 0, c₃ = 1` and attained there by more than the record.

**So the remaining task is a TRADE, not a conjunct:** show that whenever `τ₃ + c₃ ≥ 2` the
budget is depressed by at least the `2(τ₃ + c₃ − 1)` the bound gives away. Measured, it is
depressed by far more — at `τ₃ = 2` the bound permits 88 and `W₀` comes in at 56, 60, 60. Same
deficit-domination shape as Theorem S, with the source of the slack now named exactly.

## 33. Which walls bound the count plateau? — the question every dimensional claim rests on

**Opened 2026-09-12 by [P298](LEDGER.md#p298), and it is the most load-bearing open
question in the project.**

Every count-plateau tangent search here builds its candidates from the wall gradients,
assuming a first-order tangent must lie in every wall. **That premise is false.** At
n = 7 a direction crossing **7 of 51 walls** preserves the count; of the wall crossings
examined since, **4 of 6 leave the count unchanged** ([P303](LEDGER.md#p303)). A wall
is a COINCIDENCE condition — crossing one changes the coincidence structure, and need
not create or destroy a region.

**What this invalidates.** Every count-plateau dimension in this project is a LOWER
BOUND from a method whose candidate space cannot contain the answer:
`arc_eps.tangents_eps` (also restricted to the last-cube slice) and
`tangents_full.py` (which removed that restriction and kept the premise). The
published 0, 0, 2, 1, 1 at n = 4..8 are last-cube counts; n = 7 and n = 8 are known
≥ 2-dimensional, and **n = 4, 5, 6 are unresolved, not zero**.

**The question, precisely.** Given a configuration and a tight condition, does
crossing that condition change the region count? Equivalently: which subset of the
walls bounds the count plateau, and is there a readable criterion — from the group's
cube indices, from the condition type, from the deficit — that predicts membership?

**Why it is answerable.** The count change on crossing is what `cube_regions_inc`'s
`--base` path already models: it computes the arrangement with and without a cube.
[P265](LEDGER.md#p265) established that a count change is a statement about which
walls disappear. And every wall is now available as an exact polynomial
(`data/wall_polynomials.json`), so a wall can be crossed deliberately at a solved
parameter rather than stumbled over.

**A cheap first experiment.** Along one ray, solve every wall root, and for each root
count just inside and just outside. That has been done twice (P301, P303) and gives
4 of 6 unchanged. Doing it systematically over many rays at one record would give the
first census of count-changing versus count-preserving walls, and the group indices of
each are already recorded.

**Until it is answered**, no plateau dimension in this project is more than a lower
bound, and that includes every "ISOLATED" verdict whose sense is the count.
