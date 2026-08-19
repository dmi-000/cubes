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

## 4. Why 24 walls per added cube, and why lineality = n − 5?

For n = 6..9: `walls = 24n − 117`, `tight = 84n − 288`, `rank = 2(n+1)`,
`lineality = n − 5` ([P122](LEDGER.md#p122)). The 24 is the order of the cube's
rotation group — one new wall per self-symmetry of the added cube, which is too
clean to be coincidence.

**Ruled out:** that it is a law of the family — the fit **FAILS at n = 5**
(predicted 3 walls, measured 18), so it is a regime beginning at n = 6
([P122](LEDGER.md#p122)).

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

