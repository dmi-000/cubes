# Six glass cubes: weeks of experimental mathematics with a team of AIs

*An informal account, updated 2026-08-02. This is the LONG version — for a
ten-minute, low-jargon tour that hits the same beats and links onward, read
[`OVERVIEW.md`](OVERVIEW.md) instead. Self-contained, but every claim
here has a paper trail: `RESULTS.md` is the recommended starting point —
every current claim tagged PROVED / VERIFIED / EXHAUSTED / CONJECTURE, with
superseded claims confined to one table. `LEDGER.md` (the
dated ledger, now Postscripts [1](LEDGER.md#p1)–[58](LEDGER.md#p58) with addenda) is the primary record beneath that,
`PROJECT.md` is the formal write-up, and `README.md` maps all the code.
Anyone with access to a
mid-tier coding model (Claude Sonnet or similar) and a laptop can
reproduce everything — a "how to reproduce" section is at the end. And a
note on authorship, since it matters for how to read this: this document,
like the project's code, searches, and analysis, was written by an AI
(Claude) working under human direction — see "The collaboration, honestly
described" below for what that division of labor actually looked like.*

---

## The question

Take *n* identical cubes and stack them all at the same centre point, each
rotated to its own angle, like a die photographed mid-tumble with every
frame kept. Their faces slice space into cells. **How many bounded cells
can *n* cubes make, and which set of angles is best?**

For one cube the answer is 1. For two it's 13, and already non-obvious.
By six cubes the answer runs into the hundreds and — as far as we know —
nobody had mapped it. The best known at six cubes is now **727**, with a
formula that seems to govern every size and a stack of conjectures begging
for proofs.

*A note on how to read this.* What follows is chronological, and the
record moved while it was being written. The narrative below spends its
middle third on **723** and on three independent arguments that 723 was
hard to beat — all of which were sound on the evidence available, and all
of which 727 later walked through, because every sweep behind them had
sampled only small quaternions. Later sections mark where each claim fell,
in dated brackets. If you want the current state rather than the story of
arriving at it, read [`RESULTS.md`](RESULTS.md) instead: every claim there
is tagged by how strongly it is established, with superseded ones confined
to a table at the end.

One rule made the whole project possible: **every count is exact**. A
configuration is given by *n* integer quaternions (four integers each —
any four integers encode a rotation whose matrix has exactly-representable
fractional entries), and the region count is computed with integer/
fraction arithmetic, no floating point in any decision. A reported number
is a theorem about that configuration. This mattered more than we knew
when we adopted it.

## Act I: the false start that set the rules

The project began with the obvious approach: voxelize space, flood-fill,
count components. It produced confident-looking numbers — one random
six-cube configuration showed a "stable plateau" around 1,340 regions
across three grid resolutions. The exact count of that configuration
turned out to be **567**. About 70% of the voxel "regions" were slivers
thinner than any grid we could afford; meanwhile other real regions were
being merged. Both failure directions were live at once, and resolution
"convergence" proved nothing.

So the voxel ranking was thrown away entirely — a day's work — and the
rule became: approximate methods may *suggest*, only exact counts
*decide*. The exact pipeline is conceptually simple: start with a big box,
cut it by all 6*n* face-planes into convex fragments (exact rational
arithmetic), then merge fragments that touch across "phantom" walls —
places where a fragment boundary lies on a face's infinite plane but
outside the actual bounded square of the face. Union-find does the
merging; a containment test labels each region by which cubes hold it. A
C++17 version (`cube_regions.cpp`, no dependencies) counts a six-cube
configuration in well under a second; a slower Python implementation
exists purely to disagree with it, and never has (200-seed validation,
zero mismatches). Every record below was verified on both engines.

Two exact anchors calibrate everything: six cubes fanned around a shared
axis give exactly (2·6−1)² = 121 (provable), and the classical compound
of five cubes inscribed in a dodecahedron — "the golden compound", built
on the golden ratio, coordinates in ℚ(√5) — gives exactly **351**, with
its sub-compounds at 1, 13, 67, 177. Hold those five numbers; four of
them have a surprise coming.

## Act II: the six-cube race

Random search hits a wall fast. About 278,000 random six-cube
configurations, counted exactly: the best is ~635, and more sampling
doesn't help, because the good configurations live on *walls* — measure-
zero surfaces in configuration space where cubes align exactly. You
never land on a wall by chance; you have to build it.

The record chain, each verified twice:

| record | what it is | how found |
|---|---|---|
| 635 | best generic-looking config | 278k campaign + local search |
| 655 | two pairs at an exact 60° body-diagonal relation | built by hand |
| 681 | golden five + a sixth cube on a shared axis | search in ℚ(√5) |
| 699 | two 3-fold triples sharing the (1,1,1) diagonal | overlaying symmetric triples |
| 705, 717 | same families, searched properly | symmetry catalog, better seeds |
| **723** | a 3-cube cluster about (1,1,1) + three "free" cubes | shared-axis family |

[The chain did not stop there. 723 held for weeks and is the subject of the
next several acts; it fell to **727** on 2026-07-29, and 1207/1879 at seven
and eight cubes became 1217/1891 in the same pass. See Act X onward.]

The 723 configuration, if you want to check it right now:

```
cube_regions --quats '4,1,1,-1;3,3,7,3;5,-1,-5,-5;2,1,1,1;1,1,1,1;5,2,2,2'
→ 723 bounded regions, depth profile {1:210, 2:216, 3:164, 4:96, 5:36, 6:1}
```

("Depth" = how many cubes contain a region; the profile is the count at
each depth. It becomes the main character of this story.)

A meta-lesson from this phase: the 705/717 jump happened because the
first systematic symmetry sweep was silently under-parameterized — its
seed grid couldn't even represent the then-record 699, and it "found"
that family capped at 399. The framework was validated, the coverage
wasn't. Since then every search states its coverage explicitly and must
re-derive the current record from its own machinery before its negatives
are believed. That gate caught several other would-be phantom results.

## Act III: the questions that broke the golden compounds

The best ideas in this project arrived as short human questions.

**"The octahedral 3-cube maximum uses edge concurrences where the
dodecahedral one uses corner concurrences."** True, and it's exact: both
three-cube maxima count 67, but one (three cubes at 45° about the three
coordinate axes, needing √2) achieves it with 4-plane points where cube
*edges cross*, at distance √2 from centre; the other (any three golden
cubes, needing √5) with 6- and 9-plane points where cube *corners
coincide*, at √3. A dedicated search then showed edge-dominated six-cube
configurations top out at 691 and that edge-richness *anti-correlates*
with the count (rank correlation ≈ −0.58): corners are simply the
stronger ingredient. Also measured: concurrence has a sweet spot. The
record's two 9-plane corner points (three cubes sharing a corner) are
near-optimal; forcing a 12-plane point (four cubes through one corner)
crashes a six-cube count into the 300s. More alignment is not better.
A useful fact fell out for free: "k cubes share a corner" is *the same
thing* as "k cubes related by rotations about the axis through that
corner" — corner-sharing IS shared-axis symmetry, which is why all the
record families have a 3-fold axis in them.

**"So 177 is wrong?"** (relayed from Chris Cole). The golden four-cube
compound counts 177 and every reference treats the golden compounds as
the natural optima. The n=4 search said otherwise: a plain-rational
four-cube configuration reaches **183** (`1,0,0,0; 0,5,3,2; 1,-4,-1,1;
1,1,-1,-4`, profile {92, 66, 24, 1}). The technique that found it —
climb to a local max, then make a *wide* multi-component jump and climb
again, repeatedly — became the workhorse; plain greedy search stalls
below the golden value and never sees 183.

**"Does this call 351 into question?"** Yes, and the answer was already
in our pocket: drop one cube from the 723 record and the remaining five
count **393** — beating the golden five-compound by 42. In fact *all six*
five-cube subsets of 723 beat 351. Meanwhile n=2 (13) and n=3 (67)
survived deliberate stress-testing; their configuration spaces are small
enough to search almost densely. So the golden compounds are the best
*symmetric* configurations, and the true maxima are asymmetric-ish
rational configurations that keep only a single 3-fold axis — order-3
symmetry, down from golden's order-60, but never zero.

**"Are subsets of record configurations also record configurations?"**
Strikingly, yes: the records **nest**. 723 contains the n=4 record 183
exactly, contains the new n=5 best 393, and its pairs hit the n=2 record
13. Nesting is generative, not just descriptive: taking 723 and bolting
on a seventh cube — 256 candidate orientations, no fine-tuning — gave
**1207** at n=7, beating a 50,000-seed random campaign's 1085 on the
first try. And it runs top-down too: no five-cube-native search ever
found 393; it is only reachable as a shadow of the better six-cube
configuration. The record tower 183 → 393 → 723 → 1207 has adjacent
floors related by adding/removing one cube.

## Act IV: frustration, and what makes a good building block

Here is the conceptual heart of the project, and it started from another
user observation: *golden N4 is built from optimal sub-configurations on
every subset, yet golden N4 is not the maximum.*

Verified exactly: the golden four-compound has **every** pair at the pair
maximum (13) and **every** triple at the triple maximum (67) — locally
perfect everywhere — and totals 177. The actual maximum, 183, has triples
of only 63 and half its pairs at 9. **You cannot make every part optimal
and maximize the whole.** Local perfection is globally *frustrated* from
four cubes onward (through three cubes the two coincide, which is why the
golden triple really is the n=3 maximum).

Why does the maximum deliberately use "worse" parts? Two measured facts
answer it:

1. **Rarity.** Sampling thousands of random pairs: 94% count 4
   (generic), 2% count 9, 0.1% count 13. The *optimal* pair is the
   rarest thing in the space, but it is not rigid: like the 9-pair
   (two cubes sharing a face axis count exactly 9 at *every* angle about
   that axis), 13 is also a continuous family — every angle about a
   shared body diagonal, plus a whole closed arc about a shared edge
   (face-diagonal) axis (see PROOF_67.md §3.2). Both loci are
   measure-zero in the space of random pairs; neither is a single knob-
   less point. [CORRECTED 2026-07-29: an earlier draft called the
   13-pair "rigid" / "an isolated wall" with "no knob" — that was wrong,
   and it originates in the ledger's Postscript [17](LEDGER.md#p17a) addendum, itself
   corrected by Postscript [44](LEDGER.md#p44).] (Same one level up: the 67-triples
   *are* isolated points; a continuous family connecting the octahedral
   and golden 67s exists, but its interior sags to ~37 — n=3, not n=2,
   is where rigidity actually lives.)

2. **What embedding conserves.** Compare the golden triple 67 =
   {48, 18, 1} with the 63-triples inside the 723 record, all of which
   are {44, 18, 1} with pairs [9, 13, 13]. Identical in the deep layers
   — and the deep layers are what a larger compound inherits, because
   new cubes' faces recut the shallow (depth-1) regions anyway. The
   golden triple's entire +4 advantage lives in the recuttable layer,
   and it pays for those four disposable regions with its last degree of
   freedom and its rational compatibility.

So: **a good building block is deep-saturated, shallow-detuned, and
keeps its knob.** The record is a hub-and-spoke assembly — one cube
optimally (13-)paired to a cluster of spokes that are mutually 9-paired
on a shared axis, whose angles are the tuning parameters the global
optimum spends. A targeted campaign confirmed the mechanics: searching
those spoke angles directly recovers every record (183, 393, 723) in a
few thousand counts each, while locking the angles to symmetric values
costs 15–45 regions and unstructured search trails by 20–30.

## Act V: the law

All week, certain depth-profile entries kept refusing to move. At n=6,
no configuration ever had depth-5 above 36, depth-4 above 102, depth-3
above 164 — while depth-1 and depth-2 grew freely with each record. The
deep layers looked *quantized*: each either hits its generic value or a
smaller degenerate one, never more. When the n=4 search showed the same
at 24, and profiles across n=2..7 were laid side by side, the caps
snapped into a single formula. For the layer *l* steps up from the
deepest:

**depth-(n−l) ≤ C(l, n) = (12l − 6)·n − 2(l² − 1)**

Slopes 6, 18, 30, 42 (arithmetic, step 12); intercepts −2(l²−1). The
evidence is threefold and each leg is independent:

- **Attainment.** Across roughly a million exactly-counted
  configurations, every testable cap for l ≤ 4 at n = 2..7 is attained
  exactly and exceeded never — 18 of 18 cells (12/18/24/30/36/42;
  66/84/102/120; 104/134/164/194; 180/222/264).
- **Golden's role explained.** The shallowest case l = n−1 gives
  depth-1 ≤ 10n² − 14n, and the golden compounds hit it exactly (48,
  104, 180 at n = 3, 4, 5). Golden is the *top-layer-cap* configuration;
  the records are the *deep-cap* configurations; the frustration is that
  nobody gets both. Summing all caps bounds the total: ≤ 801 at n=6
  (record 723 — the 78-point gap is the price of frustration made
  visible), ≤ 195 at n=4, ≤ 445 at n=5, ≤ 1343 at n=7.
- **A completely independent measurement agrees.** There's a
  reformulation on the direction-sphere: point outward in direction û;
  cube k extends to radius 1/‖Rₖᵀû‖∞; the deep layers count cells of
  "which cubes are innermost" diagrams whose boundaries are great-circle
  arcs. Early in the project those diagrams were built exactly for a few
  configurations and their vertex/edge counts recorded: V = 68, 200, 324
  at n=6. All the measured diagrams are trivalent (E = 3V/2), so Euler's
  formula forces cells = 2 + V/2 — and the law then *demands*
  V_l(n) = (24l−12)n − 4l², which evaluates to exactly 68, 200, 324.
  Numbers measured days before the formula existed.

The law is still a conjecture. But it reduces to one crisp combinatorial
claim (prove the swap-curves of a generic configuration have exactly
(24l−12)n − 4l² vertices, all trivalent; Euler does the rest, and a
separate semicontinuity argument handles degenerate configurations), and
its deepest case l=1 reduces further to a lovely elementary statement:
*the function "distance to the nearest face" on the direction-sphere has
no local minima except the 6n face-centre directions.* The two-normal
case of that is provable by hand. The three-normal case is the open
crux. Any reader who wants a genuinely attackable open problem: that's
the one.

## Act VI: closing the search like an optimization problem

Another user reframing: *"so our searches can now be over ways to
combine building blocks and trying frustration trade-offs — can it be
reduced to something like branch-and-bound?"* Almost exactly.

- **Branch**: a configuration's *blueprint* — how the cubes partition
  into shared-axis clusters, which pairs are 13s versus tunable 9s,
  which cubes are free. Finite after symmetry: 391 raw blueprints
  collapse to **67 canonical skeletons** at n=6.
- **Prune**: with justified rules only — geometric inconsistency, and
  frustration itself as a pruning rule (an all-13 triangle forces the
  golden wall, whose extensions provably lose).
- **Optimize**: each surviving skeleton over its continuous knobs (the
  spoke angles), which we know are the right variables.
- **Bound** (the part that needed new mathematics): measured from 532
  configurations with all their five-cube subsets exactly counted —
  **(E1)** a six-cube total never exceeds its best five-cube subset by
  more than 336, and **(E2)** if any five-cube subset misses its deep
  caps at all, the total is capped ~150+ below the record.

All 67 skeletons were searched (83,700+ exact counts). **Nothing beat
723.** Combined with E1, the situation is pleasantly cornered: any
configuration beating 723 must *contain* a five-cube arrangement
totalling ≥ 388 — and after ~171,000 five-cube configurations, the only
known members of that class are 723's own subsets. So the hunt for a
better six-cube arrangement is no longer a 15-dimensional needle search;
it is precisely the hunt for one new near-record five-cube arrangement.
(E1 and E2 were measured envelopes, not theorems — clearly labelled as
such. The *increment* half of E1 is now derived: Postscript [56](LEDGER.md#p56) proves
Delta_j = N − #components(G_j) ≤ B_j, where B_j is an Euler cell count of
the plane arrangement traced on the added cube's own surface, and it holds
on every configuration tested with at most 11% slack. What is still
measured rather than proved is the flat constant: the derivation's
universal ceiling at n = 6 is B_j ≤ 872, not 336, so "T ≤ S_max + 336"
remains an empirical envelope and max(6) ≤ 729 remains a conjecture.)

The same full apparatus — climb the record, enumerate blueprints, test
the caps, extend the tower, measure the envelope — was then run at n=7,
the theory's first outing on a size it hadn't been fitted to. Verdict:
1207 stood (certified against climbing, cube-swaps, and a 100-skeleton
blueprint catalog whose best was 1207's own blueprint); the law took
zero violations across 112,864 fresh counts, with the deep caps attained
exactly and depth-2 landing within 2 of its predicted 330; and one more
greedy extension produced the first eight-cube record, **1879**, whose
deep layers hug the law's n=8 predictions from below (48 attained,
then −2, −6, −4). The tower reads 183 → 393 → 723 → 1207 → 1879, every
level the best known at its size, each built from the one below it.

[UPDATED 2026-07-29, Postscript [46](LEDGER.md#p46): 723 itself — "cornered" above and
still standing through Postscript [45](LEDGER.md#p45)'s 1211/1889 round — has now fallen,
to **727**. Every earlier n≤6 sixth-cube sweep, including the one behind
the cornering argument, sampled only small quaternions; the winning
sixth cubes at high *n* are large (1879's eighth cube was
(55,7,−148,79)), and log-uniform sampling over component heights 4..512
found 727 — 393's five cubes plus a large-height sixth — immediately.
E1's envelope bound (six-cube total ≤ best five-cube subset + 336) held
exactly: 393 + 336 = 729, and 727 sits almost against that ceiling. The
same recipe run forward from the new floor gives **1217** at n=7 and
**1891** at n=8. The tower now reads 183 → 393 → 727 → 1217 → 1891.]

## Act VII: the dihedral family, or how a stray remark in a viewer became a closed-form theorem

This act started, like several of the best ones, with a human just
*looking* at something. The project's viewer had a "67 ↔ 67 slide" —
a hand-built path dragging the octahedral three-cube maximum over to the
golden one — and its midpoint showed a scatter of near-miss edge
crossings, close but not quite touching: "ghosts," in the project's own
language. Looking at the picture, the observation was that the ghost
edges all seemed to sit in a plane perpendicular to the direction
(1,1,1). That one remark is the entire origin of everything below.

Chasing it down turned up a genuine closed-form object: take a cube and
an axis n(ψ) = (sin ψ, cos ψ, 0) — one that lies *in* one of the cube's
own face planes — and rotate the cube by ±120° about it. Three cubes,
one parameter ψ. And for *every* ψ, not just special ones, the
corresponding edges of any two of the three cubes are exactly coplanar —
built-in coincidences everywhere, not just at isolated alignments. Both
of the project's two 67s turn out to be members: the octahedral one at
ψ = arcsin(1/√3), the golden one where tan ψ = φ² (φ the golden ratio) —
a condition that collapses to the tidy identity φ² + φ⁻² = 3. A brand
new point fell out for free at ψ = 45° exactly, the face-diagonal axis:
a compound with entries in the field ℚ(√6), counted exactly (a new
engine, `q6_count.py`, cloned from the project's existing √2 counter) at
**49 regions**, depth profile {30, 18, 1}.

Sweeping the whole family with exact arithmetic (Pythagorean angles give
rotations in ℚ(√3), so a sibling engine `q3_count.py` can count them
exactly too) produced a clean symmetric staircase around ψ=45°: 25, 31,
43, then a long plateau at 55 between the two golden points, with the two
67s as spikes at its ends — and 49 sitting, unexpectedly, as a *dip*
below the 55-plateau rather than a peak. That was the first real surprise
of this act: more coincidences do not automatically mean more regions.
The extra crossings at the octahedral and golden points *create* new
divisions; the extra crossings at the face-diagonal point happen to
*merge* regions that would otherwise be separate. Coincidence-richness,
again, cuts both ways — the same lesson the edge-versus-corner story
taught back in Act III, now visible inside a single continuous family.

The old ghost-gapped slide, it turned out, was simply not walking along
this surface — its path had a small nonzero component along (1,1,1)
where the family needs exactly zero, and that tiny miss is precisely
where the ghosts came from. A follow-up question — "is there a way to
slide while *maintaining* edge concurrences?" — led to the nicest single
finding of the act: the *same 18* interior edge crossings persist,
unbroken, across the entire open stretch between the two golden copies.
The 30s and 24 at the special points are momentary extras that vanish as
you leave them; the 18-core never opens a gap. Arriving at either golden
point, none of the 18 breaks — six stay interior (docking at a segment
position of 1/φ³, one more golden-ratio cameo) and twelve land exactly on
cube corners, becoming golden's own corner structure.

That success invited an obvious next question — can a path do *better*
than 18 all the way to golden? — and the answer, after a real search
(riding a curve of extra coincidences to hold 26 concurrences over part
of the range, then trying nine different corner "handoffs" at the wall
where that curve runs out, then working backwards from golden's own extra
curve), was no: 18 remains the best confirmed lower bound, with a
specific, locatable obstruction. Both the octahedral side's extra-
coincidence curve and golden's own extra-coincidence curve pass close to
ψ=45° — which is also the tetrahedral angle, arccos(−1/3), showing up in
disguise — but about 70° apart in phase, and neither curve bends around
to link the other. Not a proof that 18 is a ceiling, but a real, honestly
described wall, not just "we didn't find anything."

Four pieces of this got upgraded from "checked numerically to sixteen
decimal places" to actually proved: a mirror symmetry (ψ and 90°−ψ give
congruent compounds, for any n), an exact 90° periodicity, the
coincidence identity itself (proved for every ψ and every n by direct
vector computation, not just verified on samples), and — the one with a
genuine payoff — a theorem that any all-rational configuration has a
rational version of the pairwise invariant that both 67s' irrational
value rules out. Put together with the (unproven, but well-supported)
belief that the two known 67s are the *only* three-cube maxima, that
gives a striking conditional fact: three cubes would be the **one and
only irrational level** of the entire record tower — two cubes rational,
three cubes forced irrational, four and up rational again.

The family also turned out to explain something about the *records*
themselves, not just about three cubes. Generalized to n cubes on a
shared axis with independent phases, at Pythagorean angles every member
becomes an ordinary integer-quaternion configuration the fast C++ engine
can already count — so, for the first time, the family could be searched
exhaustively rather than just admired. As a search space on its own it
disappoints: the best pure single-axis family members found at n=4,5,6
are 175, 335, 615, falling further and further behind the true records
(183, 393, 723) as n grows. But checking every *pair* inside each record
against the family's own membership test told a completely different
story: all 6 pairs of the 183 record, all 10 pairs of 393, and 12 of the
15 pairs of 723 are in family position. The records are not single-axis
family members — they are **gluings of family cliques sitting on
different axes** (723, worked out exactly, is a 5-cube family clique —
which is exactly the embedded 393 record — plus one more cube linked to
two of the five). That is a genuinely new way to think about where the
records come from, and it reframes the search for anything beyond 723:
not a blind search over all rotations, but a search over how many
cliques, on which axes, glued how.

The viewer got a matching set of upgrades. The old ghost-gapped slide was
replaced outright by a slider along the real dihedral family — a ψ dial
from 0° to 90°, named tick marks (including a newly-recognized
mirror-golden point), a live ghost counter, and a "maintain concurrences"
lock that clamps dragging to a range where the crossing set is certified
constant. An opaque-surface mode was added alongside the old point cloud,
turning the compound's faces into solid, shaded, paintable polygons; on
top of that came live highlighting of exactly the faces about to split or
merge at the current ψ, mouse-wheel zoom, and one-sided clipping against
the cross-section plane so the solid interior can be inspected without
the near half in the way. All of it lives at the same published link as
before.

Two threads from this act are still open, deliberately unresolved rather
than oversold: a systematic search over gluings of family cliques on
different axes (has anyone actually tried to beat 723 this way yet — no),
and whether the n=4 record has its own irrational "resonance" point in
the family, the way n=3 has its two 67s, findable with the same kind of
algebraic solve that located those in the first place. Neither is
finished.

## Act VIII: the rational slice, and the first maximum actually proved

Act VIII is the act where the two loose threads of Act VII got run to
ground — one to a satisfying answer, one to a clean negative — and where,
almost as a side effect of tidying up the proof program, the project
proved its first honest maximum theorem.

The thread about *where the records live* resolved first, and it turned
on a distinction nobody had drawn carefully. The dihedral family's tilt ψ
had always been swept at "Pythagorean" angles — those with rational sine
and cosine, the ones a right triangle with integer sides gives you —
because those keep every rotation rational and countable by the fast
engine. But when the actual record configurations were dissected, their
internal cliques sat at tilts like tan ψ = 2/3: a rational *tangent* with
an irrational *sine*. That is a different slice of angles entirely, and
every prior sweep had been structurally blind to it — not under-resolved,
but pointed at the wrong locus. The fix is a small piece of arithmetic:
at a rational-tangent tilt, a phase step keeps the whole configuration
rational exactly when its parameters are a rational point on a certain
conic, and those points have a tidy one-parameter formula that closes
under addition. So even this "irrational-sine" slice is, after all,
searchable by the integer-only engine — you just have to know to walk the
conic. The 393 record's four-cube clique turned out to be exactly such a
conic chain, its phases landing at t-values −5/6, 3/4, −1/5 with the
remaining pairs falling into place with no further search: a clean
certificate that the record's own structure lives in this slice.

Searching the slice properly broke something that had looked like a law.
An earlier campaign had found that gluing family cliques together always
landed *exactly 8 regions* short of the record, at four cubes, five cubes,
and six cubes alike — a suspiciously constant deficit that begged to be
either a theorem or a coincidence. It was a coincidence, an artifact of
the gluing search's limited vocabulary. Taking the exact 393 clique and
attaching a fifth cube *on the same axis* at a conic phase gave **387**
regions at five cubes — beating the glue campaign's 385 and cutting the
deficit to 6. The "constant 8" was simply the best that a particular
restricted construction could do; a single-axis five-chain with
non-uniform phases, which that construction couldn't express, does better.
A related tidying-up found that the six-cube record is not one
configuration but a *plateau*: fixing the record's first five cubes and
sweeping a sixth over thousands of integer orientations turned up 27
distinct completions all counting exactly 723, in four different depth
profiles that trade middle-layer count at a fixed exchange rate — the
same shallow-for-deep conservation seen throughout the project, now
visible as an exact arithmetic law operating right at the summit. The
record *value* stands; "the 723 compound" is at least four compounds.

The second thread — the hunt for an n=4 "resonance" — resolved negative,
and cleanly. Using computer algebra to write down the exact conditions
under which extra cross-alignments appear at four cubes, then solving
those conditions and counting every resulting configuration exactly, the
verdict was uniform: every such resonance in the reachable number fields
*merges* regions rather than creating them. The best one counts 151 —
below even the family's own rational plateau of 175, nowhere near the 183
record. The +12 "spike" that irrationality buys at three cubes simply
does not recur at four; the extra coincidences there behave like the
face-diagonal dip, not like the octahedral peak. There is one honest
caveat kept in the ledger — a handful of higher-degree candidates remain
uncounted for want of a specialized exact-sign routine, one of them
sitting in the record's own number field — but the mechanism that made
irrationality *pay* at three cubes is, at four cubes, proven not to.

Put beside Act VII's conditional result, this hardens the tower's oddest
feature. Three cubes appears to be the **one irrational rung** of the
entire ladder — and the reason is now visible rather than mysterious.
Attaining the maximum at two or three cubes requires maxing every depth
layer at once, which pins the configuration to an isolated, algebraically
rigid point (irrational, for three cubes). [CORRECTED 2026-07-29: this
overstates the n=2 case — max(2) = 13 is attained on a positive-
dimensional continuum, not an isolated point (every angle about a body
diagonal, plus a closed arc about an edge axis; rational throughout).
Only n=3 is truly isolated and irrational; see PROOF_67.md §3.2.] From
four cubes on, *no*
configuration can max all layers simultaneously — the layers must be
traded — and trades happen on open sets, which always contain rational
points. The 387's tolerance for a whole interval of phases, and the 723
summit's plateau of 27-plus realizations, are that openness made visible.
Knife-edge maxima can force irrationality; wide maxima cannot, and past
three cubes the maxima are wide.

Then two delegated censuses, run to answer a completely different
question, turned out to interlock and explain a great deal at once. The
question was create-versus-merge: when a compound acquires an exact
coincidence, does the region count go up or down, and by how much? The
tempting guess — "plus or minus one region per coincidence" — is exactly
right for the pure interior-crossing events at three cubes, and wrong
everywhere else: it reaches +2 per contact at the golden point, and at
four cubes it fails *in sign*, coincidences increasing while the count
falls by 24. But a different law held on every one of the twelve events
examined: the entire count change lives in the shallowest depth layer,
with every deeper layer conserved to the exact integer. The reason
emerged from the second census, which mapped both three-cube maxima as
exact spherical diagrams. Every coincidence — every edge crossing, every
corner contact — appears as a vertex of the *top* diagram (the one that
controls the shallow layer) and never touches the *bottom* diagram (which
controls the deep layers); the bottom diagrams of even these maximally
special configurations are combinatorially generic. That is *why* the
depth-conservation law holds, and it turns the create-versus-merge
question from a mystery spread across mechanisms into a bookkeeping
question on a single diagram: does the vertex weight a coincidence adds
exceed the arc structure it consumes? The same census also delivered a
correction and a gift to the proof program: the shallow-layer bound of 48
is Euler-*tight* at both maxima — their top diagrams carry a total vertex
weight of exactly 92, split (contrary to an earlier projection) between
32 units on genuine triple points and 60 on the coincidence contacts
themselves.

Which set up the act's real prize. The proof program for "three cubes
make at most 67 regions" had been written out as a tree of lemmas with
two genuine gaps; the more fundamental gap — shared with the still-unproven
two-cube case — was ruling out "parasite" cells, a topological
possibility that local analysis couldn't exclude and that would have sunk
the whole second-deepest bound. It turned out to yield to a short
argument built from three rigidities the project already had in hand: at
any point where two faces tie for closest, their spherical gradients have
*equal length* (the length depends only on the shared value); the tie
curves are all arcs of great circles, and distinct great circles are
never tangent; and a linear-algebra alternative (Gordan's theorem) forces
the equal-length gradients either to admit a strictly-improving direction
— which the great-circle geometry guarantees stays inside the cell — or
to be exactly equal, which means two genuinely parallel faces, a
degeneracy that removes itself from the problem. No parasites, at any
number of cubes. The draft still wants an adversarial read before it is
called finished, and it is filed honestly as a draft. But if it holds, it
closes the two-cube case outright — **thirteen is proved maximal, the
project's first complete maximum theorem** — proves the second-deepest
ceiling depth-(n−1) ≤ 6n for *all* n (open problem number one, in both
write-ups, for months), and finishes the entire first half of the
three-cube proof. What remains for a full "67 is maximal" is now a single
finite classification of the top diagram — and the census just handed
over the exact numbers that classification has to reproduce.

So Act VIII closes the two threads Act VII left dangling (the records'
slice: found and searched; the n=4 resonance: proved not to pay), and
converts the project's oldest open problem and its first maximum theorem
from "measured, never proved" to "proved, pending one careful read." The
irrational-rung story, still resting on the unproved uniqueness of the
two 67s, is now the best-supported conjecture in the whole enterprise.

## Act IX: 67 is maximal (the last classification, and a false lemma)

What Act VIII left as "a single finite classification of the top diagram"
became a theorem. The shallow bound depth-1 ≤ 48 reduces, by Euler, to the
top diagram carrying vertex weight at most 92 — and the census had already
shown the two 67s hit exactly 92, split 32 (triple points) and 60
(contacts). The 60 fell to a clean idea the human's own intuition
prompted — *if the bound is independent of the cells' shape, there should
be one topological reason for it*: a contact is an edge-of-one-cube
crossing an edge-of-another, which is precisely a four-valent vertex of the
polytope where those two cubes intersect, and Euler on any convex polytope
caps its total vertex weight at 2F−4. Three pairwise intersections, twelve
faces each, twenty apiece: sixty.

The triple points nearly closed the same way, and here the story earned one
more wrong turn. The tidy claim was that the "farthest-cell" diagram can be
no more branched than the "nearest-cell" one, which depth-2 ≤ 18 already
caps at 32. It is false — and not subtly: a triple point with one cube at a
corner and two at thin blades has a *degree-eight* farthest-cell vertex
against a degree-four nearest-cell one, and it is buildable from honest
cubes, not an artifact of the model. Chasing it produced the last idea:
don't compare the two diagrams, *charge each triple point to both budgets
at once* — the nearest-cell diagram and the pairwise polytopes — and a
three-line case analysis (on how many cubes are ever nearest at the point)
shows even a degree-eight vertex takes no more than its share. With that,
the degenerate triple points are fully handled, and **max(3) = 67 is a
theorem** for all pairwise-transversal triples of convex six-faced cells,
cubes among them. The write-up is `PROOF_STEP_T.md`; the readable version,
missteps and all, is `PROOF_NARRATIVE.md`.

So the oldest concrete target of the whole enterprise — "three cubes make
at most 67 regions" — is proved, and it proved to be a statement not about
cubes but about convexity and Euler's formula. What remains genuinely open
is one level up: whether the two 67s are the *only* three-cube maxima, the
irrational-rung uniqueness that stays the best-supported conjecture here.

## Act X: from searching to proving — 727's structure, and the wall that ended the search

Postscript [47](LEDGER.md#p47) (2026-07-30) is where the week's centre of gravity shifted
from *finding* the record to *proving things about it* — and, true to
form for this project, it started from a plain comparison: what actually
changed between 723 and 727?

**The comparison.** Against the fixed five cubes of 393, 727's sixth cube
(7,14,1,-5) makes pair counts 9, 9, 9, 4, 4 with the other five, carrying
18 interior edge-edge crossings. 723's sixth cube (5,2,2,2) instead makes
4, 4, 4, 13, 13, carrying 48. The new record has *fewer* coincidences than
the old one, and no maximal 13-pair at all — it replaces two rigid
best-pairs with three tunable 9-pairs. This is Act IV's frustration
principle showing up concretely, one notch sharper than before: not just
"locally worse parts win," but "fewer, more flexible coincidences beat
more, more rigid ones." Two things that had quietly hardened into working
assumptions fell out of this comparison at the same time: that a 9-pair
means a shared face axis (727 has three 9-pairs and no two of its cubes
share a face axis), and that more coincidences mean a higher count (727
has 18 crossings to 723's 48, and wins anyway).

**Every search-shaped approach hit the same wall.** With the comparison in
hand, the obvious next move was to look for something past 727. Five
different methods were tried, and all five stopped in the same place: a
menu of about 100,000 random sixth cubes; a swap-completion from all six
five-cube bases of the record; a climb on the worst-subset objective; a
core-and-clique construction (build every extension of the 183 four-cube
core, then every clique above it — which reproduced 727 as an edge and
1217 as a triangle, cheaply, but found nothing new); and roughly 3,600
solution points of a new algebraic family described below. None went
above 727. That convergence — five unrelated searches, one wall — is what
motivated dropping the search framing and asking whether the wall could be
*proved*, not just failed to cross.

**The elimination.** Following the human's suggested programme —
constraints that individually have degrees of freedom may, taken together,
admit only finitely many solutions or none, and "none" means a whole
search direction can be skipped outright — the five cubes of 393 were held
fixed, leaving the sixth with three degrees of freedom, parameterised by
Cayley coordinates q = (1, a, b, c). Every possible coincidence between the
free cube and a fixed one is one polynomial equation in (a, b, c); there
are 720 of them altogether. Feeding these to a computer-algebra system: the
36 conditions that hold at the real 727 cube have a Gröbner basis with
exactly one real solution point — the 727 cube itself — and every one of
the other 684 conditions is inconsistent with those 36 (Gröbner basis {1},
each, all 684 checked). So on the 393 base, 727 is not just unbeaten, it
is *isolated*: no continuous family of sixth cubes passes through it, and
its coincidence pattern cannot be augmented by even one more condition.
Two things this does *not* show: a 729 configuration need not share 727's
coincidence pattern at all, so this is not a proof that 729 is
unreachable; and the Cayley chart used omits the 180° rotations, which
would need a second chart to cover.

**Why the wall has the shape it does.** A side-effect of writing out all
720 conditions was noticing they are all quadrics — degree 2 in (a, b,
c) — and that a 9-pair's locus is a codimension-1 surface. Bézout's
theorem then says three such surfaces, one against each of three fixed
cubes, meet in at most 2³ = 8 points. That is a small, structural
explanation for something the project had only observed empirically for
weeks: every record sits at the intersection of three "walls." It is a
determined system, not a coincidence of the search.

**Turning the geometry back into a search method.** The same Bézout
observation immediately suggests a better way to look for records: instead
of approaching a wall numerically (sweep and climb), solve one coincidence
condition against each of three fixed cubes directly, and count whatever
comes out. On a first trial this method reached 727 at roughly 30 times
the hit rate of random menus — about 6 hits per 3,600 solution points,
against roughly 1 hit per 20,000 random sixth cubes — and its solutions
come out rational with small enough components that the fast C++ engine
can count them without ever going through the slower algebraic machinery.
Run further, it turned up two more sixth cubes reaching 727,
(3,-51,-93,29) and (40,48,-11,45), both two-engine verified — but with a
depth profile of {1:216, 2:216, 3:160, 4:98, 5:36, 6:1} and pair structure
9, 5, 4, 9, 4, different from the original {1:214, 2:220, 3:156, 4:100,
5:36, 6:1} and 9, 9, 4, 9, 4. A differing histogram proves non-congruence
outright, so 727, like 723 before it, is a genuine plateau of at least two
distinct compounds — trading depth layers by (+2, −4, +4, −2) with
depth-1 through depth-4 summing to a conserved 690, the same exchange law
seen at 723's own plateau, one level up. An exhaustive enumeration of the
whole three-wall family is running as of this writing.

**A quiet engineering verdict, settled along the way.** With the algebraic
machinery now doing real work, the standing question of whether to port it
to C++ (for the same kind of speedup the integer engine already enjoys)
got measured properly: the C++ integer engine counts a six-cube
configuration in 0.11 s, the rational-arithmetic Python cross-check
(`certify_six.py`) takes 13.1 s, and the ℚ(√5) engine
(`cube_compound_exact.py`) takes about 20 s — a real 120–200× gap. But
porting is not the next move: the actual bottleneck is symbolic (Gröbner
bases via `wolframscript`, and the validated `algebraic_groebner.wl`
already exists), the coincidence conditions' solution fields reach degree
8, so a quadratic-field C++ port would only ever cover part of the cases,
and a cheaper 100× speedup is already sitting in the existing 3-tier
interval filter. Filed as a decision, not a task.

Nothing here has found a six-cube number bigger than 727. What changed is
the *kind* of confidence available. 723's fall (Act VI) was a search
result —
a bigger, better-shaped sweep found something a smaller one missed, and
nothing said a still-bigger sweep wouldn't do it again. 727's hold on the
393 base is, for the first time in this project's six-cube story, a
proof.

## Act XI: the wall that was actually two planes, and the record's first irrational face

Act X left the exhaustive three-wall enumeration running: three Gröbner
shards, about nine hours each, roughly twenty-seven hours of compute for
partial coverage, grinding through 1.3 million systems to log ~256,000
configurations and a four-class rational plateau at 727. That was the
state of things going into Postscript [49](LEDGER.md#p49) — and it took one question from
the human, not a bigger machine, to collapse it.

**The question was about an absence, not a number.** Every solution the
enumeration had found was rational; nothing irrational had ever turned up
anywhere in the three-wall family. The human asked whether that absence
might be an artifact of some restriction nobody had examined, rather than
a fact about the geometry. It was — and chasing the answer down happened
to also demolish the enumeration's cost by three orders of magnitude.

**The walls are pairs of planes.** Every edge-edge coplanarity condition
on the 393 base, written out in the sixth cube's Cayley coordinates, turns
out not to be the irreducible quadric everyone had been treating it as,
but a product of two rational linear forms. That single fact cascades: a
three-wall system stops being a job for a Gröbner basis and becomes eight
plain 3×3 linear solves — Bézout's bound of 8 turns out to be exactly the
eight ways of picking a plane out of each factored wall — and the 144
walls per fixed cube, which had looked like 144 independent surfaces,
collapse to 24 distinct planes. The whole three-wall family shrinks from
something that needed shards and hour budgets to 134,784 linear systems,
which a script (`locus_linear.py`) finished **in about four minutes**:
2,733 distinct configurations, exhausted, topping out at 727 — the same
answer the twenty-seven-hour Gröbner run was still chasing, arrived at
before that run would have finished even one more shard. Re-examined with
that lens, the Gröbner enumeration hadn't been slow because the problem
was hard; it had spent ~99% of its 1.3 million systems re-deriving the
same handful of plane triples over and over, blind to the fact that they
were planes at all.

**And the absence of irrational solutions turned out to be exactly the
artifact suspected.** Three rational planes always meet in a rational
point — that is linear algebra, not a property of cube compounds — so a
family built entirely out of factored-into-planes conditions cannot
contain an irrational configuration *by construction*. Every previous
report of "no irrational solutions found here" in this family had been
reporting a tautology. It said nothing about whether the problem itself
has irrational optima; it is already known to (max(3) = 67 is attained
only irrationally). It said only that this one family of conditions
happens to be the wrong place to look for them.

**So the search moved to a stratum that couldn't be planes.** Corner-on-
face incidence — a corner of one cube lying on another's face plane — is
a genuinely irreducible quadric, not a disguised pair of planes, and a
first pass showed why nobody had leaned on it before: 245 solved corner-
triple systems gave only 55 real roots, all rational, none above 719.
Pure corner strata are sparse, not rich. The interesting case turned out
to be the *mixture*: two edge-edge planes plus one corner quadric. Two
planes cut a rational line, and restricting an irreducible quadric to a
line collapses it to a quadratic in one parameter — so every solution in
this mixed family is either rational or lives in some ℚ(√d), the exact
field flavor of the two n=3 maximizers. Run exhaustively, that family
held 2,856 rational candidates (topping out at 725, still short of 727)
against **1,377,612 degree-2 irrational solutions** — a ratio of about
240 irrational configurations for every rational one. Every earlier
search this project had ever run, all the way back to Act I, sampled
integer quaternions — rational by construction — so this entire stratum,
the overwhelming majority of the family, had been invisible to the
project's whole history, not merely under-sampled.

**That volume reversed Act X's own engineering verdict.** The "not worth
porting to C++" call a few pages back rested on the coincidence
conditions' solution fields reaching degree 8 — true of the edge-edge
systems, which had just turned out to be all-rational anyway, and beside
the point for where the real volume lives. Degree-2 arithmetic, elements
p + q√d with integer p and q, costs about the same as the integer engine
already in hand. A ℚ(√d) engine, `cube_regions_q2.cpp`, generalizes the
scalar type of the validated integer engine to ℤ[√d] with d fixed at
runtime, touching nothing about the geometry or topology underneath, and
leaving `cube_regions.cpp` itself untouched. It passed its gates — exact
bit-for-bit agreement with the integer engine at d=0, the golden triple's
known 67 = {48,18,1}, scaling invariance — and ran roughly a hundred
times faster than the Python algebraic path that had been the only tool
for irrational counting until now.

**Run against everything its overflow budget could reach — 56 quadratic
fields, 82,458 configurations, every single one counted — the result was
nothing above 727.** The most populous field, ℚ(√5), the golden field
itself, tops out at 721. ℚ(√2) tops out at 713. Only one field reaches
727 at all: **ℚ(√13)**, which is not an arbitrary field but the 393
base's own tilt field, the same one carrying its unique 4-clique axis.
72 of its configurations hit 727 exactly, all with a depth profile that
also occurs rationally — but not congruently to it; the two differ in
their O-reduced pair invariants. That makes five known non-congruent
727 compounds now, four rational and one genuinely irrational, and it is
the **first irrational configuration this project has ever found by
search** rather than by symmetry — every earlier irrational result, at
n=3, came from recognizing the octahedron or the icosahedron already
sitting there, not from a search turning one up.

[UPDATED 2026-08-01, Postscript [51](LEDGER.md#p51) addendum 3: this is the second time
in the project's history that a property of the instrument got reported
as a property of the problem — the first was a few pages back, where the
three-wall family's all-rational solutions turned out to be a fact about
the edge-edge condition type, not about six-cube compounds in general.
Here, "56 quadratic fields" and "only one field reaches 727" were both
properties of the overflow guard: squarefree d ≤ 100 rejected every
wider field before it could even be counted. The guard is now a traced
per-configuration bound, and the full recount finds 727 reached in
**eight** fields — ℚ(√13) ×144, ℚ(√226) ×51, ℚ(√403) ×36, ℚ(√1093) ×9,
ℚ(√1614) ×6, ℚ(√1785) ×3, ℚ(√1930) ×3, ℚ(√2741) ×3 — 255 configurations
in only three depth profiles, all of which also occur rationally. By the
O-reduced pair-invariant multiset that is **at least twelve** congruence
classes, four rational and eight irrational, one per field: within a
field every 727 shares one signature, and the signatures differ across
fields, so the classes are indexed by field rather than merely counted.
Overall: 224,184 irrational configurations counted (up from 82,458),
284,634 rejected as genuinely exceeding the traced budget — still
nothing above 727.]

**Two smaller corrections closed out the arc.** Tracing the engine's
overflow behavior properly showed the natural guess for its invariant —
that the boundary scales as d times the component bound squared — is
simply wrong; the real boundary is not constant in that product at all,
and the flat version of the rule would have silently admitted unsafe
configurations at small d while needlessly rejecting safe ones at large
d. The engine now checks a traced bound at runtime instead of a guessed
formula. And a separate worry from Postscript [47](LEDGER.md#p47) — that the coordinate
chart used throughout can't represent 180° rotations, so might be hiding
whole configurations — dissolved on inspection: the missing rotations are
still reachable as *other* representatives of the same cube, via one of
the cube's own symmetries, so the chart was only ever missing quaternions,
never compounds.

The shape of this act is different from Act X's. Act X turned a search
into a proof by asking a structural question about a record already in
hand. Act XI started from a challenge to something the project had
started taking for granted — that the absence of irrational solutions
meant something — and that challenge did two things at once: it showed
the "something" was nothing, an accident of which condition type had been
enumerated, and it handed the project the tool (planes instead of
quadrics, then a ℚ(√d) engine instead of a Python fallback) to go find
the stratum the accident had been hiding. Nothing above 727 turned up
there either. But the record's fifth face, sitting in the base's own
number field, is the first thing in this project's history that a search
found rather than recognized.

## Act XII: the coordinates were the problem

*2026-08-17/18.*

The two n = 3 maximisers had been sitting outside every census for weeks, for a
reason that sounds like bookkeeping: they live in Q(sqrt2) and Q(sqrt5), and the
crossing machinery took Fractions. Porting it was a day's work, and the day
turned into something stranger — five separate failures, each looking unrelated,
each turning out to be the same mistake wearing different clothes.

**A step size is a representative.** The face enumeration around the golden 67
displaced each candidate direction by eps = 1/64, 1/256, 1/1024 and asked the
engine for a count. 333 of 2 196 faces disagreed across the three. The obvious
fix — halve until two consecutive values agree — resolved all 333 and was WRONG
on 36, inventing counts of 33, 34 and 35 that do not occur anywhere in the true
face set. Two steps can both land outside the intended cell, in the SAME wrong
one, and agree perfectly. Convergence and co-location are indistinguishable from
inside.

The real fix was not a smaller number but a different kind of number. Q(sqrt d)(eps),
elements ordered by the sign of the lowest-degree nonzero coefficient, is a
genuine ordered field in which eps is smaller than every positive rational. Every
predicate the counting engine performs is a sign test, so all of them stay exactly
decidable, and the answer returned IS the eps -> 0 limit. `cube_regions_eps.cpp`
was generated from the validated engine rather than hand-edited, its degree bound
of 8 traced through the multiply chain so that no product is ever truncated. The
gate that decides it is beautiful in its simplicity: scale a direction by 97 and
by 1/1000 and the count must not change. No finite-eps implementation can pass it.

**A point in a cone is a representative.** With the step size gone, the 727
neighbourhood enumeration still refused 10 of its 24 chambers — the engine's
overflow budget rejecting inputs with components up to 13 528. The reading was
obvious and wrong: we need a wider engine, 42% unmeasurable. Then the split by
input size turned out to be perfectly clean, 1-178 accepted against 2 865-13 528
refused, no overlap. A chamber is a CONE; any interior point represents it; and
Fourier-Motzkin had been taking the MIDPOINT of each bound pair, whose
denominators compound through the recursion. Replacing it with the simplest
rational in the interval dropped the maximum to 178 and every chamber evaluated.
The geometry was never the obstacle.

**A gauge is a representative.** The n = 4 record 183 contains a half-turn, which
sits at Cayley infinity, and was written up as unmeasurable. It is not: only the
PARAMETERISED cubes need finite coordinates, because the gauge cube is frozen and
never inverted. Reorder so the half-turn is the frozen one and 183 measures fine —
12 walls, rank 8, lineality 1, joining the pattern rather than breaking it.

**A class is a representative.** `census_variety_redo.json` held 26 records where
the ledger described 23 reruns. The three extra were not errors: three
`(n,k,count)` keys name TWO classes each. The same ambiguity, at a different
scale, is why the all-members census had to run 826 members instead of 221 class
representatives — a (count, profile) class is an equivalence by INVARIANT, not by
congruence. And when 1895 turned out to have two 1217-subsets, neither depth
profiles nor pair-count multisets could separate them; it took the TRIPLE-count
multisets, where the alternative carries a 37 the tower has nowhere.

**A chart origin is a representative.** Two n = 9 classes ran ten hours each with
no output. A stack sample put 2 078 of 2 287 samples inside Karatsuba
multiplication, 4.2 GB peak: coefficient explosion, not algorithmic shape. Six of
the eight charts had NO constant term, which means the chart origin — the basis
vector itself — already satisfies every polynomial. `sp.solve` was grinding
through a positive-dimensional system to find a solution sitting at the point it
started from. One evaluation replaced ten hours; 64 seconds and 123 seconds.

Five failures, one shape. In each, an object defined only up to an equivalence
was handed an arbitrary representative, and the arbitrary choice was mistaken for
a property of the object. None of the underlying mathematics was ever wrong.

---

What the week actually established, once the coordinates stopped lying:

**Both 67s are isolated points**, by enumerating every face of their local wall
arrangements — 728 and 2 196, none reaching 67, none unevaluated. Both sit atop a
cliff of exactly 4: nothing adjacent counts 64, 65 or 66, and the first step down
lands on 63, which is precisely the best triple inside any higher record.

**Region counts are odd**, and the proof is one line: every cube is centrally
symmetric and concentric, so the antipodal map permutes bounded regions as an
involution, and count = #self-antipodal (mod 2). The innermost region is always
self-antipodal. An EVEN count therefore detects a SHELL — a region wrapping the
origin without containing it. They are rare (6 of 826 census counts) and cluster
on the same few values.

**Isolation has two mechanisms.** Both 67s have walls of full rank: pinned at
first order, nothing survives even linearly. No rational record does — 727, 1217,
1895, 2785 keep tangent spaces of dimension 1, 2, 3, 4 and are isolated only
because the second-order variety is empty. That claim was made, withdrawn when it
emerged that the wall list structurally omits the (1,1,1,1) type, and reinstated
when the omitted walls were finally differentiated and added exactly zero rank.

**The tower breaks exactly once**, and arithmetic is the reason. 183 contains
three 13-pairs but no 67, because 67 needs irrational coordinates and every subset
of a rational compound is rational. One-cube extension from n = 3 cannot reach
183; two-cube extension from n = 2 can, three ways. Every record contains its
(n-2) record as well as its (n-1) record, so the rule is to extend from the
deepest arithmetically compatible level.

## The collaboration, honestly described

This project was a four-layer collaboration, and the layering was not
decorative — each layer did something the others couldn't. It is also
worth being explicit about this document's own place in that layering:
this write-up — like every line of code, every search, and every piece
of analysis in the project — was **written by an AI** (Claude), working
under human direction. The human side of the collaboration supplied
questions, corrections, and the occasional observation that turned out
to unlock an entire act of the story; the AI side did essentially all of
the designing, coding, computing, and writing, including the words you
are reading now.

**The human** (with friends — Chris Cole and Werner — kibitzing)
supplied almost every pivot: the sliding-triple family, the edge-vs-
corner observation, "try intersections between families," "is 177
wrong?", "are subsets of records also records?", the building-blocks/
frustration reframing, branch-and-bound, and — the origin of Act VII —
simply noticing, while looking at the viewer, that a scatter of near-miss
edges appeared to sit in a plane perpendicular to (1,1,1). None of these
were "requests to compute"; they were acts of noticing. The pattern is
worth stating: the human watched the data for *meaning* while the
machines watched it for *values*. Several of this project's best results
are literally a human sentence turned into a measurement — the
perpendicular-edges remark most dramatically of all, since it is the
entire seed of the closed-form family, the four theorems, and the
records-are-gluings finding described in Act VII.

**A frontier model** (Anthropic's Fable 5; an Opus 4.8 stint when weekly
limits hit) ran the main session: designing the exact algorithms and
validation gates, writing the specifications, spotting and naming the
regularities (the ceiling formula was found by staring at maxima tables
and fitting), catching errors — including its own. Concrete corrections
that made it into the ledger: an early claim that record configurations
trade deep count for shallow at a favourable "6-for-45" rate collapsed
under proper optimization to an exact 1:1 conserved exchange; a claimed
confirmation that "golden maximizes depth-1" turned out to be a broken
test (it never got near the golden value) and was re-labelled untested
until the formula later explained it; a "richness is mid-total"
misreading of early data was refuted by a cheap model's careful
correlation analysis. The ledger keeps all of these, deliberately.

**Mid-tier execution agents** (Claude Sonnet) did the heavy building:
the C++ engine, every campaign and search driver, the ℚ(√2)/ℚ(√5)/tower
arithmetic, the incidence analyzers. Two systematic failure modes
emerged, and both were manageable once named. First, *coverage
artifacts*: an agent's search can be perfectly implemented over an
accidentally-too-small parameter space — the fix was the hard gate
"your machinery must reproduce the current record before your negative
results count." Second, *premature parking*: agents would set up a long
computation, then stop to "wait for a monitor" instead of running it;
the fix was insisting every campaign be a single detached self-
sequencing script, with the agent only collecting results. With those
two guardrails, delegation worked extremely well — a dozen-plus agent
campaigns produced the record chain, and every "we found X" was
independently re-verified in the main session before being believed.

**A small model** (Claude Haiku) handled a pure data-analysis task —
the subset-richness census over 278k configurations — and notably
*overturned the frontier model's prior belief* (richness correlates
positively with totals; records are rich AND balanced). Cheap models
audit well.

**Non-LLM tools carried the actual mathematics**: the C++/Python twin
engines (never disagreed once in ~1M counts), Wolfram Engine via
`wolframscript` for the algebraic side (Gröbner-basis solves for
configurations satisfying multiple corner-coincidences at once — it
found exact configurations no numeric grid lands on, including the
depth-1 record-holder d1=224), and a small self-contained browser
visualizer (`depth_explorer.html` — depth-coloured cross-sections you
can sweep through the compound, a rotatable depth point-cloud, rings
marking edge/corner concurrences, presets for the golden and octahedral
compounds; also hosted online). The exports of every session, the
specification files, and the ledger's postscripts are what let the work
survive a dozen context resets and model switches: the *filesystem* was
the collaboration's long-term memory.

## Reproducing this (for a reader with a Sonnet-class assistant)

Everything can be rebuilt from the descriptions in this document, but
the fast path if you have the repository: build the counter and check
the anchors —

```
clang++ -O2 -std=c++17 -o cube_regions cube_regions.cpp
./cube_regions --selftest                    # axial-6 → 121
# the current six-cube record, 727:
./cube_regions --quats '4,1,1,-1;3,3,7,3;5,-1,-5,-5;2,1,1,1;1,1,1,1;7,14,1,-5'  # → 727
# its predecessor 723, for comparison — same five cubes, different sixth:
./cube_regions --quats '4,1,1,-1;3,3,7,3;5,-1,-5,-5;2,1,1,1;1,1,1,1;5,2,2,2'    # → 723
```

For configurations whose coordinates are not rational — the n=3 maxima, and
the irrational strata of Act XI — build the field engine instead, which
generalises the same counter to ℤ[√d]:

```
clang++ -O2 -std=c++17 -o cube_regions_q2 cube_regions_q2.cpp
./cube_regions_q2 --d 5 --quats '1:0,0:0,0:0,0:0;1:1,-2:0,1:-1,0:0;-1:1,0:0,1:1,2:0'  # golden triple → 67
```

From scratch, the essential recipe an assistant can implement in an
afternoon: (1) integer quaternion → exact rational rotation matrix;
(2) plane-cut a bounding box by the 6n face planes with Fraction
arithmetic, tracking convex cells; (3) merge cells across facets that
lie outside the owning face's square (union-find) — this phantom-facet
merge is the one subtle step; (4) label regions by containment, count by
depth. Validate on 121 and 351 before trusting anything. Then: random
campaign to see the 635 wall; wide-perturbation climbing to break golden
values (reproduce 183 from scratch!); shared-axis templates with free
spoke angles to reach the records; and test C(l,n) against everything
you count. All the record quaternions are in this document and the
ledger; every claimed number is checkable in seconds.

## Open questions

Act VIII resolved several of these; the list below marks what moved.
Items 1 and 2 are **CLOSED** — both were still listed as open long after
they were proved, which is exactly the staleness this list exists to
avoid; they are kept here, struck through, because the shape of what was
open is part of the story.

1. ~~**Finish "67 is maximal" for three cubes.**~~ **PROVED**
   (2026-07-21, Postscripts [41](LEDGER.md#p41)–[43](LEDGER.md#p43)). max(3) = 67 holds for any three
   concentric convex ≤6-facet cells meeting pairwise transversally —
   cubes included, an open dense set containing both maximizers. Three
   Euler arguments: depth-3 ≤ 1 and depth-2 ≤ 18 by convex cover, and
   depth-1 ≤ 48 from Euler on the top diagram with the vertex weight
   split 32 + 60 between triple points and pairwise intersection
   polytopes. The route this item proposed — "a single finite
   classification of the top diagram's vertices" — is not the route that
   worked; the marked step "deg_top ≤ deg_bot at triple points" turned
   out to be FALSE, and the proof goes through a two-budget local
   inequality instead. Write-up: [`PROOF_67.md`](PROOF_67.md) +
   [`PROOF_STEP_T.md`](PROOF_STEP_T.md). One caveat survives, inherited
   from the contact analysis: two cells meeting *tangentially* rather
   than transversally.
2. ~~**Harden the No-Parasites proof, then two cubes are done.**~~
   **PROVED** (2026-07-20, Postscript [33](LEDGER.md#p33)). max(2) = 13, and by a much
   cheaper argument than the draft this item describes: A∖B is a union of
   at most six convex pieces (one per face of B), likewise B∖A, plus one
   core — so the bound holds for *any* two convex cells with at most six
   faces, not just cubes. The same postscript's Theorem 1 gives
   depth-(n−1) ≤ 6n for all n, the project's oldest open problem, now
   closed. Correction recorded with it: the maximizer is not "45° about a
   face axis" but any angle about a body diagonal — a continuum, not the
   rigid point the project believed for weeks (Postscript [44](LEDGER.md#p44)).
3. **Beat 727 or corner it completely** — 723 fell on 2026-07-29 (Postscript
   46), and by envelope E1 the question is now equivalent to finding a
   fundamentally new five-cube arrangement ≥ 390, or proving none exists.
   On the 393 base the room left is exactly 729, and three independent
   lines now bound it: E1's cap, the elimination proving 727 isolated with
   an unaugmentable coincidence pattern (Postscript [47](LEDGER.md#p47)), and the three-wall
   enumeration (Postscript [48](LEDGER.md#p48)). The rational-tangent slice reached 387 at five cubes
   (breaking the old "constant-8 deficit") but has not passed a record.
   [CORRECTED 2026-08-01: this item previously described the *723* summit
   as "a plateau of ≥ 27 non-congruent realizations" — pre-727 text left
   under a rewritten heading, conflating 27 sixth-cube *completions* with
   the four non-congruent depth profiles among them. 727 is itself a
   plateau, and larger than any count so far has managed: the 183
   irrational 727 configurations alone carry 21 distinct per-label
   vectors, so at least 21 non-congruent compounds, plus the rational
   ones. An earlier figure of "twelve classes, eight irrational, one per
   field" undercounted, because the O-reduced pair invariant it used is
   only a NECESSARY condition for congruence. And the irrationality is
   incidental: every one of the eight fields is rationally shadowed —
   34 385 rational points sampled along the same 727-producing lines reach
   727 too — so n=3 remains the only level where irrationality is
   REQUIRED. Postscript [52](LEDGER.md#p52) addendum 2.]
4. **Prove envelope E1** (a zone-style bound making the branch-and-prune
   a certified branch-and-bound) — HALF DONE. The increment identity and
   its geometric bound are proved (Postscript [56](LEDGER.md#p56)): the one-cube increment
   equals N − #components of the bit-j adjacency subgraph, and is bounded
   by an Euler cell count B_j on the added cube's surface, slack ≤ 1.11 on
   every configuration measured. What remains is a good UNIVERSAL ceiling
   on B_j: the crude one, 2 vertices per plane pair, gives 872 at n = 6,
   far above the measured 336, so the branch-and-bound is not yet
   certified.
5. **Why exactly does frustration switch on at four cubes?** Act VIII
   gives the mechanism: attaining the maximum needs every depth layer
   maxed at once, which is possible only at n ≤ 3 (and forces
   irrationality at n = 3); from n = 4 the layers must be traded, and
   trades live on open — hence rational — sets. This is now an argument,
   not just a measurement, though not yet a theorem.
6. **Unequal cube sizes** — off-centring provably hurts near the record;
   size variation is still untested (resizing hits a degeneracy the
   current counters can't evaluate; a degeneracy-robust counter would
   settle it).
7. **The tower at scale** — does greedy extension stay within a constant
   of optimal as n grows, and what is the asymptotic growth of max(n)?
   (Cap-sum bound O(n³); the records track it suspiciously well.)
8. **Is three the *only* irrational rung?** — largely answered
   2026-08-01, and not the way this item expected. Once a ℚ(√d) engine
   existed, irrational configurations turned out to REACH the records at
   five and six cubes (393 in three fields, 727 in eight), so "three is
   the only level with irrational optima" is false. But every one of them
   is **rationally shadowed**: sampling rational points along the very
   lines that produced them reaches the same counts, so irrationality is
   doing no work there. At four cubes the irrational strata fall ten
   short of 183, across all four bases. So the surviving claim is
   narrower and sharper than the original: three cubes is the only level
   where irrationality is **required** (Theorem R), not the only level
   where it appears. Postscripts [51](LEDGER.md#p51)–[52](LEDGER.md#p52) and their addenda.
9. **A create-versus-merge criterion.** Coincidences are exactly the
   top-diagram vertices; whether a new one creates or merges regions is
   now a bookkeeping question — does its added vertex weight exceed the
   arc structure it consumes? — but no closed criterion is written down
   yet. The "±1 per coincidence" guess is dead; depth-conservation
   (all change in the shallow layer) held on all 12 events tested.
10. **More than 18 concurrences, octahedral to golden?** — 18 is a
    confirmed lower bound with a located obstruction (two extra-
    coincidence curves grazing ψ=45° about 70° apart, never linking),
    not a proven ceiling.

*Files for the deeper dive: `RESULTS.md` (current state, every claim
tagged by strength — start here), `LEDGER.md` (ledger,
now Postscripts [1](LEDGER.md#p1)–[52](LEDGER.md#p52) with addenda, indexed at the top),
`PROJECT.md` (formal write-up), `PROOF_67.md` + `PROOF_STEP_T.md` (the
max(3)=67 proof), `C45_notes.md` (proof program — the four
dihedral-family theorems in §12, the max(3)=67 lemma tree in §13),
`region_adjacency.py` (region adjacency graphs, for classifying
configurations beyond region counts), `census_report.md` (the two maxima as exact
diagrams), `events_report.md` (the create-vs-merge catalogue),
`rattan_report.md` (the rational-tangent sweep), `resonance4_report.md`
(the n=4 resonance verdict), `nfamily_report.md`, `handoff_report.md`,
`dihedral_slider_report.md`, `README.md` (all code + commands). The
interactive viewer (opaque surface mode + dihedral-family slider):
https://claude.ai/code/artifact/044d34a6-3f36-43b2-9ec8-17fb5691c87c*
