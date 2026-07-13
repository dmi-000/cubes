# Six glass cubes: a week of experimental mathematics with a team of AIs

*An informal account, 2026-07-13. Self-contained, but every claim here has
a paper trail: `six_cube_search_results.md` (the dated ledger, Postscripts
1–21) is the primary record, `PROJECT.md` is the formal write-up, and
`README.md` maps all the code. Anyone with access to a mid-tier coding
model (Claude Sonnet or similar) and a laptop can reproduce everything —
a "how to reproduce" section is at the end.*

---

## The question

Take *n* identical cubes and stack them all at the same centre point, each
rotated to its own angle, like a die photographed mid-tumble with every
frame kept. Their faces slice space into cells. **How many bounded cells
can *n* cubes make, and which set of angles is best?**

For one cube the answer is 1. For two it's 13, and already non-obvious.
By six cubes the answer runs into the hundreds and — as far as we know —
nobody had mapped it. We ended the week at **723** for six cubes, with a
formula that seems to govern every size, three independent arguments that
723 is hard to beat, and a stack of conjectures that are begging for
proofs.

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

1. **Rigidity.** Sampling thousands of random pairs: 94% count 4
   (generic), 2% count 9, 0.1% count 13. The *optimal* pair is the
   rarest and most rigid thing in the space — an isolated wall. The
   9-pair, by contrast, is a continuous family: two cubes sharing a face
   axis count exactly 9 at *every* angle about that axis. The suboptimal
   configuration carries a knob; the optimal one doesn't. (Same one
   level up: the 67-triples are isolated points; a continuous family
   connecting the octahedral and golden 67s exists, but its interior
   sags to ~37.)

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
  into shared-axis clusters, which pairs are rigid 13s versus tunable
  9s, which cubes are free. Finite after symmetry: 391 raw blueprints
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
(E1 and E2 are measured envelopes, not theorems — clearly labelled as
such — and proving E1, likely via a zone-style bound on how many regions
six new faces can create, would make the cornering rigorous.)

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

## The collaboration, honestly described

This project was a four-layer collaboration, and the layering was not
decorative — each layer did something the others couldn't.

**The human** (with a friend, Chris Cole, kibitzing) supplied almost
every pivot: the sliding-triple family, the edge-vs-corner observation,
"try intersections between families," "is 177 wrong?", "are subsets of
records also records?", the building-blocks/frustration reframing, and
branch-and-bound. None of these were "requests to compute"; they were
acts of noticing. The pattern is worth stating: the human watched the
data for *meaning* while the machines watched it for *values*. Several
of the week's best results are literally the human's sentence turned
into a measurement.

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
./cube_regions --quats '4,1,1,-1;3,3,7,3;5,-1,-5,-5;2,1,1,1;1,1,1,1;5,2,2,2'   # → 723
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

1. **Prove the ceiling law** — via the trivalent-vertex census, or just
   its l=1 case, the no-extra-minima lemma (two-normal case done; three
   normals open).
2. **Beat 723 or corner it completely** — equivalent, by envelope E1,
   to finding any fundamentally new five-cube arrangement ≥ 388, or
   proving none exists.
3. **Prove envelope E1** (a zone-style bound: six new faces can create
   at most ~336 regions in a 30-plane arrangement?) — this makes the
   branch-and-prune a certified branch-and-bound.
4. **Why exactly does frustration switch on at four cubes?** The
   middle-layer mechanism is measured; a proof would likely fall out of
   the ceiling law.
5. **Unequal cube sizes** — off-centring provably hurts near the record,
   but size variation is untested (the record is so symmetric that every
   rational resize hits a degeneracy the current counters can't
   evaluate; a degeneracy-robust counter would settle it).
6. **The tower at scale** — does greedy extension stay within a constant
   of optimal as n grows? What is the asymptotic growth of max(n)? (The
   cap-sum bound gives O(n³); the records track it suspiciously well.)

*Files for the deeper dive: `six_cube_search_results.md` (ledger),
`PROJECT.md` (formal write-up), `C45_notes.md` (proof program),
`ALGEBRAIC_SEARCH.md`, `BLUEPRINT_SPEC.md`, `README.md` (all code +
commands). The interactive viewer:
https://claude.ai/code/artifact/044d34a6-3f36-43b2-9ec8-17fb5691c87c*
