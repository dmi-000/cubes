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

## 4. Why 24 walls per added cube? — a WINDOW n = 6..9, broken at both ends

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

**No longer untried — [P182](LEDGER.md#p182) measured the shapes.** 1217, 1895 and
2785 are ALL continua, and so is 727 — on its four documented arcs A-D, with the
record at arc D's node ([P183](LEDGER.md#p183) corrects P182, which had claimed 727
showed no locus; that claim contradicted `RESULTS.md` and `METHODS.md` and was made
without reading them). **Every rung from 6 to 9 is a continuum.** More importantly,
in every interval containing a recorded configuration the recorded configuration is
an **ENDPOINT**, never interior:

    1217   [-59/315, -11/63]           recorded at the RIGHT end
    1895   [0, 11/12] along (0,0,0,1)  recorded at the LEFT end
    2785   [-227/889, -3278/13335]     recorded at the LEFT end
    2785   [-1/223, 97/28098]          recorded at the LEFT end

There is a mechanism, not a coincidence: a search reports the plateau member with the
smallest primitive representative, and height is smallest where the parametrisation is
simplest, which is at the boundary. [P178](LEDGER.md#p178) had already noticed 2785's
recorded member was "the last value giving 2785" and read it as luck.

**So the bias is systematic.** Every rung of the tower was built by extending a
BOUNDARY member of its predecessor's plateau, and the one rung where members were
compared (n=9 -> n=10) put the boundary member 8 below the best. Every rung above 727
may be low for the same reason.

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

## 13. Where does each continuum actually END? — one rung is solved, the rest are sampled

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

**Why it is filed rather than done:** it is a re-reading of three entries against a
new measurement, not a computation, and it should be done deliberately rather than
folded into a session that has already overturned four things.
