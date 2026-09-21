# Session state — 2026-09-16

**Read [ORIENTATION.md](ORIENTATION.md) first** — one screen with the named objects and the
recurring traps. This file is the live state; that one is the frame.

**Read [RESULTS.md](RESULTS.md) §4's scope correction first, then this. Several claims made
EARLIER IN THIS SAME SESSION were later refuted; the corrections are propagated, but read the
refutation column below before quoting anything from P304–P321.**

## The single most important thing

**A cube's boundary is six SQUARES, not six planes.** `concurrency_walls.py` originally tested
only that four face planes meet, never that the meeting point is on the cubes. Most such points
are far outside the compound and are not walls of anything. This invalidated the mechanism of
[P304](LEDGER.md#p304) and several results built on it ([P322](LEDGER.md#p322),
[P323](LEDGER.md#p323)). **Fixed** — the family now carries `common_point_inside_cubes` per
root, and running the fix showed that even P304's own founding example, the `t = −2/9` wall,
is outside.

## What stands

| | |
|---|---|
| [P307](LEDGER.md#p307) | plateau dimensions **1, 2, 2** at n = 6, 7, 8 — equalities |
| [P308](LEDGER.md#p308) | boundary attributions audited and cleared; [P296], [P301]–[P303] stand |
| [P311](LEDGER.md#p311) | **the facet-centre lemma** — proved; depth is radially monotone on every facet ([METHODS 26](METHODS.md#26-the-facet-centre-lemma)) |
| [P312](LEDGER.md#p312) | `c_ell` is the WALL graph's, 43/43 against the engine |
| [P315](LEDGER.md#p315) | vertex taxonomy; **12 quadruple points in every record above n = 4**, forced by a shared body-diagonal axis |
| [P319](LEDGER.md#p319) | `c > 1` occurs **only at level 1** — 0 in 3382 deeper instances |
| [P321](LEDGER.md#p321) | a `c`-transition is a **pure reconnection**: `dV = dE = 0`, 8 of 8 |
| [P326](LEDGER.md#p326) | `holes <= 1` completes the bound for every n but barely tightens it |
| [P327](LEDGER.md#p327) | the frustration mechanism: every region is paid for by degree excess, and **every triple point is spent twice** |
| [P328](LEDGER.md#p328) | taxonomy completed; records buy **13–28 % of their regions with degeneracy** |
| [P330](LEDGER.md#p330) | `EE <= 6` per pair FALSE (max 10, at a FACE diagonal) — and **`sum EE <= 6*C(n,2)` is FALSE too**, at every n from 2 to 6 |

## What was refuted, by me, in this session

    P304's mechanism        four-plane concurrency does NOT explain the count drops   [P323]
    P309's +258 / 282       counted without containment                               [P323]
    P318's cost split       (b-1)(b-2) does not apply to CORNER concurrences           [P324]
    P321's concurrency      every concurrency wall at a c-transition is spurious       [P321 add.]
    EE <= 6 per pair        TRUE at q = (0,1,1,1); 18 of P329's 24 were corner incidences [P330]
    sum EE <= 6*C(n,2)      exceeded at every n from 2 to 6, and at a PROVED n = 2 maximiser [P330]
    P328's excess table     generic values, not invariants of the signature             [P330]

**The pattern, and it is long-standing, not mine alone ([METHODS 27](METHODS.md#27-a-cause-claim-needs-its-own-gate)):**
every CAUSE claim made this session fell; every MEASUREMENT stood. Across the whole ledger,
~40 of ~303 titles carry refutation language and about two thirds of those refute a cause, law
or mechanism. A sentence with *because* in it needs its own gate, and the gate must not share
the claim's model.

## Where to go next

**THE FOUNDING ASSUMPTION, and where it stands** ([P365](LEDGER.md#p365)). The project began as a
search for `max(6)` because `max(n <= 5)` was believed solved by subsets of UC09, the compound of
five cubes in a dodecahedron. Counted exactly, its subsets are `351 / 177 / 67 / 13`:

    n = 2   13 = max(2)   PROVED        n = 4   177  <  183   FAILS
    n = 3   67 = max(3)   PROVED        n = 5   351  <  393   FAILS ([P16])

Right at exactly the two proved sizes, wrong above them. **And the golden 177 of [P342] IS UC09's
4-subset** — which is why every one of its subsets is maximal, not a coincidence but a
consequence. This session reached that compound twice without recognising it: from the `A4`
symmetry ([P342]) and from a five-edge sharing graph forcing its sixth ([P351]). Three routes,
one object.

**So what this session added is not that complete corner-sharing loses — [P16] had that at n = 5
three months ago — but WHY:** the accounting that prices the loss to the unit ([P343]: 18
quadruple points at one region each, `195 - 18 = 177`), the mechanism producing them ([P358]:
pinned cubes cannot dodge), and the policy the records follow instead ([P364]: one hub saturated
at degree 4, every other cube left free).

**THE MANAGEMENT POLICY** ([P364](LEDGER.md#p364)) — measured on the records themselves, n = 4..7:

    n   sharings   structure              per-cube degree
    4       3      star, hub = cube 3     hub 3, others 1
    5       4      star, hub = cube 4     hub 4 SATURATED, others 1
    6       4      same star              hub 4, others 1, sixth cube shares NOTHING
    7       3+     same hub               hub 4, others 1 or 0

    1. ONE hub.   2. saturate it at degree 4 (a cube has four antipodal corner-pairs).
    3. every other cube gets AT MOST ONE shared axis, keeping its free rotation.
    4. never a second hub, never a cycle.   5. above n = 5, add cubes with NO sharing.

This is [P358]'s mechanism as a design rule: a cube with one shared axis can dodge a forced
coincidence (codimension 1 in its rotation); pinned cubes cannot. It predicts the n = 4 ladder —
star 176 > paw 168 > 4-cycle 162, with K4/golden at 134/170 — and it explains both sub-maximal
complete-sharing compounds, UC09 at n = 5 ([P363]) and the golden 177 at n = 4, which pin
everything.

**It is a policy, not a proof of optimality.** But it is actionable: it says what to build at a
given n and what not to. And it explains why the records stop growing their sharing structure
above n = 5 — the hub is capped at 4, and further sharings cost more than they return, which is
consistent with the n = 6 and n = 7 records falling 8 and 22 short of the triple budget
([P362]).

**Complete corner-sharing is sub-maximal at BOTH sizes where it exists** ([P363](LEDGER.md#p363)):

    n = 5   UC09, the compound of five cubes    351   believed max(5), beaten by 393 ([P16])
    n = 4   the golden 177                      177   every subset maximal, loses to 183

UC09 saturates the degree bound `2n = 10 = C(5,2)` exactly — 20 dodecahedron vertices in 10
antipodal pairs, one per cube-pair, verified: 10 of 10 pairs share, 0 axes on three cubes. **So
this session's n = 4 finding has a precedent at n = 5 that predates it**, and the pattern has two
independent instances rather than one.

**The failure chain is now complete and mechanistic** ([P354](LEDGER.md#p354),
[P357](LEDGER.md#p357), [P358](LEDGER.md#p358)):

    1. beating 183 needs  two-body - Q4 > 48
    2. EE <= 36 at B = 128 (measured), so two-body > 48 forces SC2 >= 8
    3. SC2 >= 8 needs >= 4 sharings: paw, 4-cycle, K4 (5 is EMPTY, [P351])
    4. four or more sharings pin EVERY cube with >= 2 axes -- except in the paw
    5. a cube with ONE shared axis keeps a free rotation, and a 4-fold coincidence is
       codimension 1 in it, so such a cube can AVOID it; a cube pinned by two cannot
    6. so the paw buys Q4 = 0 with its free cube and pays EE = 24 -> two-body = 40;
       every other route pins all four cubes and carries Q4 = 18

    configuration        per-cube shared axes   free parameters       Q4              objective
    K1,3 star (RECORD)   3 / 1 / 1 / 1          THREE cube rotations  0 generically      176
    paw                  3 / 2 / 2 / 1          ONE cube rotation     0 generically      168
    4-cycle              2 / 2 / 2 / 2          one AXIS parameter    18 always          162
    K4 (both)            3 / 3 / 3 / 3          none -- isolated      0 or 18         134/170

**Confirmed both ways**: the paw's `Q4` over 36 parameter values is `{0: 33, 2: 2, 32: 1}` —
codimension 1, generically zero; the 4-cycle's is 18 across all 608 members.

**The record is the extreme case** — three of its four cubes carry a single shared axis each, so
it has THREE free rotations, the most avoidance available, and that is why it holds `Q4 = 0`
while reaching `two-body = 48`. **Freedom to avoid quadruple points and freedom to raise
two-body are the same resource.**

**What remains for [OQ 39](OPEN_QUESTIONS.md#39).** One measured link stands between this and a
proof: **`EE <= 36` at `B = 128`**, step 2 of the chain, sampled over ~3 700 configurations
([P352]) and never derived.

## THE n = 8 PLATEAU, DELIMITED ([P385](LEDGER.md#p385))

    38 vertices, 72 facets, volume 0.1632
    inradius 0.059473   circumradius 0.859442   aspect ratio 14.5
    bounded by four contacts of pair (0,5), then six of pair (3,7)

First order — the tangent cone at the record. The same anisotropy as n = 4, whose arc ran
0.0517 one way and 0.6356 the other (ratio 12.3).

## PLATEAU DIMENSIONS, n = 3..8 ([P381](LEDGER.md#p381)-[P383](LEDGER.md#p383))

    n        3     4     5     6     7     8
    tangent  1     1     1     1     2     3
    plateau  0     1     ?     1     2     3      n=3 the maximiser is an ENDPOINT of its arc
                                                  n=8 CORRECTS [P307]'s 2

n = 4 and n = 6, 7 are controls and pass. [P307]'s `1, 2, 2` is `1, 2, 3`.

## THE 183 PLATEAU IS AN ARC OF LENGTH 0.687 ([P378](LEDGER.md#p378), [P379](LEDGER.md#p379))

    forward   0.0516797    EE drops 36 -> 30, twelve contacts leave at once
    backward  0.63560749   ONE contact reaches a corner; margin closed to 1.2e-17
    total     0.6872872    the record sits 7.5 % from the forward end

`B = 128` and `EE = 36` verified at every step of the backward walk, so the count is 183 along
the whole arc.

**And the two 183 classes are on DIFFERENT arcs** ([P380](LEDGER.md#p380)). Their gauge-free
distance is 0.06504; the forward arc is only 0.05168 long, and at arc 0.60 backward the distance
is 0.05072 with 0.0356 of arc left. Distance is 1-Lipschitz in arc length, so neither end can
reach it — **proved, not extrapolated.** [P136]'s predicted curve through both points is a
wall-system locus, a different object from the constant-count arc, which is what [P136] itself
said.

## (superseded detail) THE 183 PLATEAU IS A BOUNDED ARC (2026-09-20, [P378](LEDGER.md#p378))

The n = 4 record is **not isolated**. It lies on a curve along which the full vertex census is
preserved out to arc length 0.04, breaking before 0.06 where 12 of its 36 edge contacts slide
out of range (`EE` 36 -> 30, `(1,2)` 24 -> 36; `T3` and `SC2` untouched). Residuals stay at
`1e-46` throughout, so the break is combinatorial, not numerical.

    [P287] "isolated in both senses"          WRONG -- its 19 682 probes are all STRAIGHT LINES
    [P136] "the count is NOT constant along"  WRONG -- it is, for a finite arc
    [P136] the curve itself, rank 8 of 9      RIGHT, and five weeks earlier than [P377]

Both 183 classes have the identical local structure: 36 contacts, rank 8, one genuine direction.
Neither is isolated. Whether the two are joined is NOT settled — [P133] records them as
identical on every invariant, so no invariant can detect arrival.

## REFUTED 2026-09-20 — read this before anything below

**`EE <= 36` at `B = 128` is FALSE, and so is `EE + B <= 164`** ([P373](LEDGER.md#p373)).

    1,0,0,0 ; 0,2,-3,-2 ; 0,2,-3,2 ; -4,-2,-5,-6
    EE 38   SC2 0   T3 128   Q4 0   B 128   EE+B 166   173 regions (engine-confirmed)

Both were maxima over searches seeded from the record and the face-diagonal family. The refuter
is built from neither: it is the n = 3 `EE + B` extreme — two members of the `EE = 10` family
placed against each other — extended by an ordinary fourth cube. **`max(4) = 183` is again
unproved**; [P371]'s case analysis is withdrawn, and so is everything downstream of
`EE <= 36 at B = 128`, which includes [P354]'s chain step 2, the kill lists of [P366]/[P369],
and the band grid's conclusions.

**What still stands:** the proved box (`E_i <= 10`, `E_S <= 32`, hence
`EE + B <= 188 - 2*SC2` and `TOTAL <= 195 - Q4`); the golden attaining 164 at `SC2 = 12`, which
is exactly its box bound, so that one branch is closed BY PROOF; [P370]'s phantom-`K4`
correction; [P371]'s six-sharing enumeration; [P372]'s merge law and wall degrees; and the
record itself at 183.

**The open question is back to one line: what actually bounds `EE` at `B = 128`?** Two directed
searches have now certified a false answer to it. The proved answer is `EE <= 60` (from
`E_i <= 10` with `SC2 = 0`); the observed is 42.

**And the refuter's region has now been searched** ([P375](LEDGER.md#p375)): 5 136 compounds,
0 refusals, **best count 173**. It buys `EE` and pays in `SC2` — every high-`EE` compound there
has `SC2 = 0`, forfeiting the `2*SC2 = 12` that the record's corner sharing supplies. So the
region refutes the `EE` ceilings without threatening 183. A second `EE = 38` at `B = 128` turned
up there at different quaternions, so the refutation does not rest on one point.

**REGION COUNTS ARE ODD** ([P375]) — central symmetry pairs every region except the convex
depth-`n` core. So beating 183 means reaching **185**.

---

**THE BAND WAS EXPLORED, AND IT MOVED THE QUESTION** ([P368](LEDGER.md#p368),
[P369](LEDGER.md#p369)). Two results, one against this project and one for it.

**AGAINST: [P359]'s per-triple maximum of 20 is FALSE — it is 26**, verified two ways and then
settled by enumerating all 54 432 triples in the `EE = 10` family (0 unevaluable). [P360]'s
"combinatorial optimum 40" falls with it (`EE = 44` is realised at `B = 120`), and [P366]'s kill
list goes from 105 patterns to 3 995. What survives: `EE <= 36` at `B = 128` is measured
directly on 4-compounds and is untouched, as is the determinantal description.

**FOR: the band's frontier is a LINE.** `36 + 128 = 40 + 124 = 44 + 120 = 164`, with the record,
the golden, the 4-cycle and the band compound all exactly on it. Since
`TOTAL = 7 + EE + 2*SC2 + B - Q4`,

    EE + B <= 164   =>   TOTAL <= 171 + 2*SC2 - Q4     and the record is 171 + 12 - 0 = 183

One inequality across all twelve columns, holding over 3 730 compounds and five directed climbs.
`SC2 <= 6` is capped at 183 outright; the paw branch (`SC2 = 8, Q4 = 0`, needs `EE + B >= 160`)
is CLOSED across its exact one-parameter family at 152. **And the last branch is now CLOSED** ([P370](LEDGER.md#p370),
[P371](LEDGER.md#p371)): six sharings with `Q4 = 0` does not exist. [P334]'s `K4` with
`T3 = 74, Q4 = 0` **is the golden** — `74 = 56 + 18`, because its `count_T3` never checked the
fourth cube, and its gate on the record could not catch that since the record has
`Q4generic = 0`. Enumerating the branch exactly (96 inner-product solutions, 0 unevaluable)
returns 2 compounds, both the golden with `Q4 = 18`.

**SO THE CASE ANALYSIS IS COMPLETE.**

    SC2 <= 6            TOTAL <= 183     the RECORD attains it
    SC2 = 8  paw        <= 175           92 exact members swept
    SC2 = 8  4-cycle    <= 169           Q4 = 18 always
    SC2 = 10            EMPTY            [P351]
    SC2 = 12            <= 177           golden only

**`max(4) = 183` now rests on ONE measured inequality, `EE + B <= 164`**, instead of a chain
with a measured link, an unexplored band and two open branches. That inequality is still
measured, not proved.

**AND THE CHAIN COVERS ONE COLUMN OF TWELVE** ([P367](LEDGER.md#p367)). Enumerating every
subset profile that could beat 183 — `TOTAL = 7 + T + B - Q4`, so the target is
`T + B - Q4 >= 177` over 262 144 profiles — gives two consequences from the PROVED box alone:
**`Q4 <= 11`**, which closes the entire `Q4 = 18` branch (4-cycle, golden, UC09) by arithmetic,
and **`B >= 117`**, twelve values rather than one. [P354]'s step 2 conditions on `B = 128`,
which nothing proved forces; `B = 118..126` is live and has never had an `EE` ceiling measured
in it. A first scan finds it worse (best `TOTAL` 173 at `B = 124`) but never approaches the
required `EE`. **The sharpest target is `s = 6`**: the golden has `B = 128` with `Q4 = 18`, the
other `K4` has `Q4 = 0` with `B = 74`, and a compound holding both would count 195.

**And its shape is now known** ([P366](LEDGER.md#p366)). The per-pair route is dead — a compound
with all four `E_S = 32` and a pair at `EE = 10` exists, total `EE` 18; the record reaches 36
with every pair at 6. The ceiling is an ANTI-CORRELATION among the six pairs. What is new and
usable: `EE > 0` is codimension 1 (0 of 120 at quaternion height `10^6`, 103 of 120 at height 6),
the level sets are cut out by **144 quartics** (all degree exactly 4, none identically zero), and
the kill list is **105 pair-EE patterns**. The remaining work is an elimination, not a search.

**And the ceiling itself was challenged and held** ([P361](LEDGER.md#p361)): since the
UNCONDITIONAL `EE <= 36` was refuted in [P330] (the face-diagonal family reaches 42), the
conditional form deserved a hunt rather than a sampling maximum. Two directed climbs — hold
`B = 128` and maximise `EE` (reached 36); hold `EE >= 38` and maximise `B` (reached 84) — do not
meet. `B = 128` pins `EE` at 36; `EE >= 40` pins `B` at 84.

**The per-3-subset method does NOT reach it** ([P359](LEDGER.md#p359)). `B = 128` forces
`E_S = 32` on all four subsets, and each pair lies in two of them, so a per-subset bound
`sum EE <= m` gives `EE_total <= 2m`. The record and the golden both have `sum EE = 18`, which
would give exactly 36 — but the true maximum at `E_S = 32` is **20** (pairs `[10,6,4]`), so the
route yields only `EE <= 40`. A 3-subset can even hold `E_S = 32` together with a full `EE = 10`
pair; its neighbours collapse instead. **The residual 4 is invisible to any sum-over-subsets
argument, since summing discards which pairs sit in which subsets.** That is the open edge.
