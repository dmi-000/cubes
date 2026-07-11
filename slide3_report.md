# Two sliding 3-cube triples: overlay/slide/relative-rotate search

Executed per `SLIDE3_SPEC.md`. Read first: `six_cube_search_results.md`
Postscripts 4-8, `MULTIWALL_SPEC.md` + `multiwall_report.md`, `golden_six.py`,
`qtower.py`. Validated files (`certify_six.py`, `cube_compound_exact.py`,
`golden_rotations.py`, `exact_search_results.jsonl`, `six_cube_search_results.md`)
were read but never modified. New files: `slide3_q2.py` (Q(sqrt2) field +
generic exact counter, mirrors `qtower.py`'s pattern with d=2 instead of
d=3), `slide3_search.py` (quat/overlay library), `slide3_p1.py` /
`slide3_p2.py` / `slide3_p3.py` (search phase drivers), `slide3_search.jsonl`
(every eval, all phases).

> **NOTE (see ## V2 below):** The Section-0 congruence conclusion here was
> based on a test that is INVALID for cubes (raw pairwise traces of frames
> that were not all proper rotations, with no reduction by the cube's own
> 24-fold self-symmetry). V2 redoes it correctly and REVERSES the Check-D
> conclusion: the golden 3-cycle subset {1,3,4} IS a genuine 3-fold-
> symmetric triple and the correct family DOES connect the octahedral and
> dodecahedral compounds. The V1 flat-55-plateau / jump-to-67 result below
> is still correct **for the coordinate-axis family it tested** — that
> family just isn't the one the user meant. Everything in Section 0 stands
> as a finding about that (wrong) family; Sections 1-2 (the overlay search
> infrastructure) are reused unchanged by V2, which also finds the record.

## 0. The family premise — VERIFIED FALSE for the literal candidate, with an
exact and unexpected consolation prize

**User's premise**: "A family of maximal 3-cube configurations can
continuously slide between the octahedral compound of 3 cubes and 3 cubes
inscribed in a dodecahedron."

**Candidate family tested**: C(theta) = { Rx(theta).cube, Ry(theta).cube,
Rz(theta).cube }, i.e. the axis-aligned cube rotated by the SAME angle
theta about each of the 3 coordinate axes. Structurally this is a base
rotation Rx(theta) conjugated twice by B := 120deg-about-(1,1,1) (the cyclic
axis permutation x->y->z->x), which lies in BOTH the octahedral group O and
the icosahedral group I (`golden_rotations.py`'s O∩I = A4, order 12; B
itself has order 3, verified there): Ry(theta) = B.Rx(theta).B^-1,
Rz(theta) = B^2.Rx(theta).B^-2.

### Check O: the octahedral endpoint — PASSES, and exactly matches 67

At theta=45deg the family needs cos45=sin45=1/sqrt2, i.e. Q(sqrt2) exactly
(rational quaternions can only approach 45deg, never reach it — half-angle
22.5deg has tan(22.5deg)=sqrt2-1, irrational). Built exactly in a new
Q(sqrt2) field (`slide3_q2.py`, direct structural clone of `qtower.py`'s
Ext3/exact_count_tower pattern with d=2 instead of d=3) via the standard
45deg rotation matrices (cos=sin=sqrt2/2), orthonormality asserted exactly:

```
Rx(45deg), Ry(45deg), Rz(45deg) exact in Q(sqrt2):
  total = 67, by_depth = {1: 48, 2: 18, 3: 1}   (641 arrangement cells, 0.47s)
```

This is presumed to be (construction matches the standard definition) the
classical "compound of three cubes" with full octahedral symmetry.

### Check D: matching a golden 3-subset — FAILS, exactly and provably, for
the literal family AND every sign/orientation variant tried

The congruence test (spec): compare the multiset of pairwise
relative-rotation traces tr(Ri.Rj^T) (3 values for 3 cubes) between C(theta)
and a golden-five 3-subset.

**All 10 golden-five 3-subsets were checked exactly** (Q(sqrt5) arithmetic,
`cube_compound_exact.Q5`): every one of them gives total 67 with identical
histogram {1:48, 2:18, 3:1} (icosahedral transitivity — already implicit in
`golden_six.py`'s docstring, confirmed directly here), but their exact
pairwise-trace multisets are NEVER three equal values — every subset shows
either three distinct values (e.g. {3/4+3/4√5, 1/4+1/4√5, 1}) or exactly two
equal plus one different (e.g. {1, 1, -1}); the full table of all 10 exact
multisets is in the code log (`slide3_search.jsonl` gate section is silent
here — this was a pure verification computation, not a search eval; results
reproduced by re-running the check block, see "how to reproduce" below).

**C(theta) exactly has 3 EQUAL pairwise traces for every theta — a rigid
structural fact, not a coincidence at 45deg.** Verified exactly (rational
quaternion arithmetic, Q5 with b=0, no floats) at 5 unrelated rational
theta values (tan(theta/2) = 2/5, 3/7, 4/11, 1/3, 5/13): tr(Rx,Ry) =
tr(Ry,Rz) = tr(Rx,Rz) EXACTLY in every case (e.g. 1659/841 at the first).
An identity holding exactly at 5 algebraically independent rational points
of a bounded-degree trigonometric identity in cos(theta) is an identity for
ALL theta (dense rational agreement forces it) — closed form:
tr(Rx(theta),Ry(theta)^T) = cos(theta)^2 + 2cos(theta), and by the extra
S3 symmetry that permutes/reflects the 3 coordinate axes (present in O,
NOT generally present in I's action on an arbitrary 3-subset), all 3 pairs
share this one formula. **All 8 sign variants** (Rx(±theta), Ry(±theta),
Rz(±theta)) were also checked exactly at theta = atan(2·3/7 / (1-(3/7)^2))
[a representative rational angle]: every sign combination reproduces the
SAME three pairwise traces — sign flips do not break the equal-trace
structure, so the spec's suggested "alternating senses" fix does not exist
within this family.

**Conclusion: since no golden 3-subset ever has 3 equal pairwise traces,
and C(theta) always does (for every theta, every sign variant), C(theta) can
NEVER be congruent to a golden 3-subset up to a global rotation, for ANY
theta.** This is an exact, closed, negative result, not a search gap. The
"small variant" fixes the spec anticipated (sign/orientation) provably do
not rescue it; a genuine fix would need to break the extra octahedral-S3
symmetry, e.g. use a GENERIC (non-coordinate) base axis for the B-conjugated
triple — but then the theta=45deg endpoint would no longer be the standard
"compound of three cubes" (that compound's definition specifically needs
coordinate axes), so there is no small patch that keeps both endpoints intact.
This is flagged as an open question in Section 2, not silently dropped.

**The consolation prize**: even though C(theta) is never ISOMETRIC to a
golden triple, the octahedral endpoint (theta=45deg exactly) has the
IDENTICAL total AND histogram (67, {1:48,2:18,3:1}) as every golden
3-subset. Two non-congruent 6-plane arrangements sharing an exact region
count and depth profile is itself the kind of "combinatorial identity, not
just numerical equality" flagged as noteworthy in `multiwall_report.md`'s
section 3 for the n=6 (1,1,1) wall — the same phenomenon recurring one level
down, at n=3.

### Check M: is C(theta) "maximal" along the slide, and is it a genuine plateau?

Dense rational sampling, tan(theta/2)=p/q with q<=60 (1103 points spanning
theta in (0,90)) via the fast validated C++ engine
(`./cube_regions_n --n 3 --quats-stdin`, ~4.5ms/eval):

**C(theta) is a FLAT PLATEAU at exactly 55 (histogram {1:36,2:18,3:1}) for
EVERY rational theta strictly between 0 and 90 degrees** — no exceptions in
1101 sampled rational points, including points within 0.04deg of the 45deg
wall on both sides (e.g. q,p=(29,12) at 44.96deg and (41,17) at 45.04deg,
both exactly 55). At theta=0 and theta=90 the three cubes coincide exactly
(a cube is invariant under 90deg rotation about its own face axis) and the
"triple" collapses to total=1.

**The theta=45deg wall is a genuine, isolated, measure-zero JUMP, not a
limit the rational plateau approaches**: 55 -> 67 discontinuously, gaining
12 regions (+48 -> ... depth profile also reshapes: {1:36,2:18,3:1} at
55 becomes {1:48,2:18,3:1} at 67 — ALL the gain is in depth-1, exactly the
same "shallow-gain" signature `multiwall_report.md` found at the n=6
golden-wall gain from 635 to 681). This is a wall GAIN (T2-opposite
direction), like the n=6 (1,1,1)-diagonal wall.

**Context for "maximal"**: a matched-budget random-baseline check (3000
random rational n=3 triples via `cube_regions_n --seeds`, then 6
independent hill-climbs with +-1/+-2/+-3/+-4 component moves from the best
starts) tops out at 33-43, NEVER reaching the 55 plateau, let alone 67.
This matches the pre-existing record in `six_cube_search_results.md`
Postscript 2 exactly: "triples: winner's subsets 29..38 (median 33),
random max 38, golden subset 67" — independently reproduced here with a
different (climbed, not just sampled) random baseline. **C(theta)'s
constant-55 plateau sits well above the generic random ceiling (~38-43) for
its entire domain, and the golden/octahedral wall value 67 is (to the
resolution of this and the prior random search) the best n=3 value found
anywhere.** The family is "maximal" in the weaker, honest sense of "a
robust high plateau plus one isolated higher wall," not in the sense of
"count increases monotonically toward the golden endpoint" — it does not:
the plateau is completely flat right up to the wall, then jumps.

**Verdict on the premise**: the user's geometric intuition about a
continuous 3-cube slide connecting the two named compounds is confirmed at
one endpoint (octahedral, theta=45deg, exact Q(sqrt2)) but REFUTED at the
other — the literal family never reaches a golden-inscribed triple, exactly
and provably, for reasons that are about the wrong SYMMETRY TYPE (extra S3
vs the golden triple's coarser structure), not merely a numerical
near-miss. The values 55 (generic) / 67 (both endpoints, non-congruent
but count-identical) are the exact, load-bearing numbers for everything
that follows.

---

# V2 — the corrected family, and the overlay search (NEW OVERALL RECORD 699)

Executed per `SLIDE3_SPEC_V2.md` (supersedes Section 0's congruence
conclusion; reuses all V1 infra). New/used files: `slide3_q2.py` (Q(√2)),
`qtower.py` (Q(√3,√5), read), `golden_six.golden_five()` construction,
`./cube_regions` (n=6) and `./cube_regions_n --n 3`, `certify_six.exact_count_config`
(Q5 oracle). All evals in `slide3_search.jsonl`. Validated files untouched.

## V2.0 The congruence test, done correctly — Check D now PASSES

**V1's error (two compounded bugs).** (1) The golden frames from
`find_cubes` are built columns = axis-triple in combination order; **cubes
2 and 3 come out with det = −1** (improper frames — a reflection, not a
rotation). (2) V1 compared *raw* pairwise traces tr(Mi Mjᵀ), but a cube has
24-fold octahedral self-symmetry, so each orientation is only defined up to
right-multiplication by O(24); the meaningful invariant is the O-reduced
relative rotation (min bring-on angle / double-coset), not the raw trace.

**Corrected computation** (exact, Q(√5), all frames forced proper by one
column-sign flip; reduce R = Mi·u·Mjᵀ over u ∈ O(24), take max trace = min
angle):

- **All 10 pairs of the golden five give the IDENTICAL reduced relative
  rotation**: min angle **44.4775°**, exact trace 3/4+3/4√5 = 3φ/2. This is
  the icosahedral 2-transitivity (A5 acts 2-transitively on the 5 cubes) that
  V1's raw-trace test destroyed. Postscript-2's "five-compound pairs all 13,
  all equal" is the region-count shadow of this single reduced relation.
- **The golden 3-cycle subset is {1,3,4}** — the three cubes that the
  order-3 rotation C = 120°-about-(1,1,1) (= `golden_rotations.B`, the
  x→y→z cyclic permutation) three-cycles (it fixes cubes 0 and 2). Verified
  by the exact line-permutation of the 15 axes under B (1→3→4→1). Its three
  pairwise reduced relations are of course all 44.4775° — **a genuine
  3-fold-symmetric triple.** V1's "no golden 3-subset has three equal
  traces" is retracted: it was entirely the det=−1 + no-symmetry-reduction
  artifact.

So Check D is satisfied: the golden 3-cycle triple exists, is 3-fold
symmetric about (1,1,1), and (from V1's own Section 0) counts exactly 67 —
identical to every golden 3-subset and to the octahedral compound.

## V2.1 The correct family (built and validated exactly)

Fix C = B = 120° about (1,1,1) (rational matrix). A 3-fold triple is the
**left C-orbit** T(S) = { S, C·S, C²·S } of one seed cube S.

- **Octahedral seed S_oct = Rx(45°)** (exact in Q(√2), from `slide3_q2.py`).
  Verified: T(S_oct) counts **67** with histogram {1:48, 2:18, 3:1}, and
  equals the standard {Rx45, Ry45, Rz45} compound as a cube-set. (V1's
  family {Rx(θ),Ry(θ),Rz(θ)} is the CONJUGATION orbit {S, BSB⁻¹, B²SB⁻²};
  at θ=45° both orbits coincide as cube-sets, which is why V1 hit 67 there.)
- **Dodecahedral seed S_dod = golden cube 1** (Q(√5)). Verified: its left
  C-orbit is exactly the golden cubes {1,3,4} (B⁰S_dod=cube1, B¹=cube3,
  B²=cube4), count **67**.
- **The slide.** Δ = S_dod · S_octᵀ is a single rotation, **angle 40.31°
  about axis ≈ (−0.442, −0.829, 0.343)** — NOT a coordinate axis and NOT
  (1,1,1) (exactly as V2 predicted; V1's flat plateau came from the seed
  spinning about a *coordinate* axis). S(t) = R_â(t·δ)·S_oct,
  T(t) = { S(t), C·S(t), C²·S(t) }, t ∈ [0,1], T(0)=octahedral,
  T(1)=dodecahedral, 3-fold symmetric for all t by construction.

**Edge-crossing marker — validated at both endpoints (the user's decisive
test).** Computed all edge–edge crossings (exact segment closest-approach)
of cube S(t) with cube C·S(t):

- **t = 0 (octahedral): crossings at fractional position 0.5 — the
  MIDPOINT** ("the middle"), plus 0.293 = 1−√2/2 (the 45° edge crossing).
- **t = 1 (dodecahedral): crossings at fractional position 0.382 = 1/φ² —
  the GOLDEN-SECTION point** ("the corner"), plus 0.0 (shared dodecahedron
  vertices).

So the family provably connects the two named compounds and the crossing
moves middle → golden-corner, confirming the user's geometric picture at
the endpoints. **Honest caveat**: no *single* edge pair stays exactly
incident through the interior — the edge pair that is the midpoint crossing
at t=0 slides monotonically to a *vertex* (frac 0.5→0.0) with a small gap
(≤0.026) opening mid-slide, while the golden-section incidence at t=1 is a
*different* edge pair. Searched all 24×24 right-O gauge choices of
(S_oct, S_dod): none keeps an edge pair exactly incident for all t. The
exact edge incidences live only at the two symmetric endpoints; the interior
is generic. This is the same wall-vs-generic structure V1 found, one level
up: **two isolated count-67 walls connected through a generic sea.**

**Count profile T(t)** (rationalized seeds → `cube_regions_n --n 3`,
N=512): exact 67 at t=0 and t=1 (the walls); a generic plateau (≈37, hist
{1:18,2:18,3:1}) for all sampled interior t. Not monotone, not an interior
peak — flat generic interior with wall spikes at the ends. (Interior t are
transcendental angles t·δ, so no exact algebraic interior point exists to
tower-count; the rationalized bracket sees only the ambient chamber, as
expected.)

## V2.2 Overlay search — NEW OVERALL RECORD **699** (rational, cross-verified)

Configuration X(θ₁,θ₂,R) = triple₁ ∪ R·triple₂ where each triple is a
3-fold-symmetric-about-(1,1,1) triple. **Key point:** V1's coordinate-axis
triples {Rx(θ),Ry(θ),Rz(θ)} ARE 3-fold symmetric about (1,1,1) (they are
the B-conjugation orbit), so the V1 overlay infrastructure (`slide3_p1.py`
/ `slide3_p3.py`, half-angle-rational quats, integer relative-rotation quat
R, fast `./cube_regions`) is exactly the right tool — no rebuild needed.

**Gates (both pass).** S1: θ₁=θ₂, R=identity ⟹ coincident triples ⟹ 55
(single-triple value), for all interior θ. S2: the record config
cross-checked C++ vs `certify_six.exact_count_config` — identical total
and histogram.

**Landscape (P1 coarse 34,482 evals + P3 fine 32,893 evals, all logged).**
The (1,1,1)-diagonal R family dominates by a wide margin:

| R family (relative rotation) | best 6-cube total | field |
|---|---:|---|
| **R on the shared (1,1,1) 3-fold axis, quat (a,b,b,b)** | **699** | ℚ |
| R on a sibling body-diagonal (1,±1,∓1) | 671 | ℚ |
| near-icosahedral rational R | 657 | ℚ |
| random integer-quat R | 675 | ℚ |
| R = 90° face / 180° edge / identity (R ∈ O) | ≤ 407 | ℚ (degenerate) |

**THE RECORD — 699 bounded regions, fully rational:**

```
quats = [[3,1,0,0],[3,0,1,0],[3,0,0,1],
         [41,28,22,14],[41,14,28,22],[41,22,14,28]]
   (triple1 = C-orbit at tan(θ1/2)=1/3; triple2 = R·C-orbit,
    tan(θ2/2)=2/9, R = (5,2,2,2) = rotation about (1,1,1))
by_depth = {1:180, 2:216, 3:164, 4:102, 5:36, 6:1}   total 699
```

Independently re-counted by the Python Q5-capable oracle
(`certify_six.exact_count_config`): **699, identical histogram.** Three
distinct (θ₁,θ₂,R) cells realize 699 (also (9/5,12/7,R=(3,1,1,1)) and
(11/7,1/2,R=(5,2,2,2))); it is a plateau, and an 8-integer radius-2
hill-climb (all of q1,p1,q2,p2 and the 4 R-components) from every 699 start
is a **certified local maximum at 699**.

**699 beats every prior record**: overall 681 (+18), rational 655 (+44),
rational-random 635 (+64). Sanity: 699 ≡ 3 (mod 4) (generic parity, not a
wall exception like 681≡1); d3/d4/d5/d6 = 164/102/36/1 sit **exactly at the
established deep ceilings** (no violation); d6=1, total odd. **d2 = 216
exceeds the previously observed d2 ceiling of 214** and **d1 = 180**; both
are new depth-1/2 high-water marks (flagged as data from a wall-constrained
search, not a re-established generic ceiling). The entire gain over 681 is
shallow (d1+d2), exactly the golden-wall / T2 pattern from Postscript 7–8.

**Why it works (the active constraint).** Both triples are 3-fold symmetric
about the SAME axis (1,1,1), and R = (a,b,b,b) is a rotation about that same
(1,1,1) — so the full 6-cube compound retains a global 3-fold symmetry about
(1,1,1). The 9 cross-triple relative rotations fall into 3 cyclic classes of
3 (angles 63.26°/70.30°/78.84°, each appearing 3× under the shared 3-cycle).
This is the **same "shared 3-fold axis" constraint that built the 681 golden
wall** (Postscript 8: "ANY sixth-cube angle about the exact (1,1,1) axis
gives 681") — but here BOTH halves are 3-fold-symmetric triples on that
axis, not five golden cubes + one, and it is reachable with fully RATIONAL
rotations. Constraint-first wins again, and this time entirely inside ℚ.

**Dead / negative regions (skip these):**
- **R ∈ O (identity, 90°-face, 180°-edge): ≤ 407.** When R is a cube
  symmetry the two triples partially coincide (shared planes) and collapse —
  strict losers, and some rationalize to the engine's "outside not single
  region" degenerate flag (positive-codimension coincidence). ~3,270 of the
  P1 configs hit this; all far below record.
- **R = pure slide, same frame (identity):** total spectrum tops at 399.
- **Two GOLDEN (dodecahedral) triples overlaid, R rational (Q(√5) oracle):**
  clean NEGATIVE — R=identity 67 (gate), best over probed R only **673**
  (R=(5,1,2,3)), with R on (1,1,1) giving 595/361. Golden-triple overlays
  do NOT beat the coordinate-triple 699 and cost 3–30 s/eval vs 7 ms. The
  golden field buys nothing here; the rational (1,1,1)-3-fold construction
  is strictly better AND faster.
- **Sibling-diagonal / near-icosahedral R:** real but capped at 671/657.

## V2.3 Handover — first moves for a follow-on agent

The record 699 is a rational, certified-local-max plateau on the shared
(1,1,1) 3-fold wall. Resume from `slide3_report.md` + `slide3_search.jsonl`
(grep `RECORD_V2`, `"phase":"P3"`, `"phase":"P3b"`). Most promising next
moves, in order:

1. **Widen the (1,1,1)-diagonal θ-grid and R-angle.** P3 used Farey(12)²
   × 17 diagonal angles and found 699 at only 4 cells; a partial Farey(16)²
   × 12-angle sweep (`slide3_search.jsonl` phase P3b, ~12k of 75k done
   before being stopped for the core budget) still maxed at 699 but was not
   exhaustive. Finish it, and push θ finer (Farey(20)) around the four 699
   cells — the plateau's exact extent and whether a 5th/6th region breaks
   701+ is open. This is the single highest-value next step; it is pure
   `./cube_regions --quats-stdin`, ~7 ms/eval, embarrassingly parallel.
2. **Exact (1,1,1)-diagonal wall value.** All 699s are rational approximants
   with R on the (1,1,1) axis at a rational half-angle; the *exact* symmetric
   angles (e.g. R = exact 60°/90° about (1,1,1), and the two triples at
   golden or 45° content) live in Q(√3)/Q(√2)/Q(√3,√5) — verify with
   `qtower.py` / `slide3_q2.py` whether the on-wall count jumps above 699
   (as pair 4→13 did) or sits at 699 (as the 681 wall did). The tower engine
   is ready and fast enough (≤27 s/eval).
3. **Two 3-fold triples on the same axis but DIFFERENT internal content.**
   699 uses two coordinate-content (θ-slid) triples. Try triple₁ = octahedral
   (Q√2) and triple₂ = golden (Q√5), both C-orbits on (1,1,1), related by a
   (1,1,1)-axis R ⟹ Q(√2,√5) tower. Only a few tower verifications; chosen
   because the shared-axis constraint is what pays and mixing the two
   count-67 endpoints on that axis is untested.
4. **Climb 699 with radius-3/4 and two-component moves** (V1's `slide3_p2.py`
   only did radius-2 single-component); the d2=216/d1=180 highs suggest the
   basin may have a taller neighbor a jump away.

Open questions for a fresh agent: (a) is 699 the true max of the rational
(1,1,1)-3-fold wall, or a plateau below a finer-θ peak? (b) does the exact
algebraic wall point beat 699? (c) can a THIRD shared structure (edge-
crossing coincidence between the two triples, per the V2 marker) be imposed
on top of the shared axis for a higher-codimension win? The infrastructure
(`slide3_search.py`, `slide3_p1/p2/p3.py`, `slide3_q2.py`) is all reusable.

## V2 record table (all exact, cross-verified where noted)

| construction | total | field | notes |
|---|---:|---|---|
| **two 3-fold triples, shared (1,1,1) axis, R=(a,b,b,b)** | **699** | ℚ | NEW overall record; C++ + Q5-oracle verified; cert. local max; d1=180,d2=216 |
| golden five + sixth on (1,1,1) wall (prior overall) | 681 | ℚ(√5) | Postscript 8 |
| double 60°-diagonal pair wall (prior rational) | 655 | ℚ | Postscript 8 |
| sibling-diagonal R overlay | 671 | ℚ | this work |
| two golden {1,3,4} triples overlaid | ≤673 | ℚ(√5) | net loser vs 699 |
| single 3-fold triple (octahedral or dodecahedral endpoint) | 67 | ℚ(√2)/ℚ(√5) | n=3 wall |
| single 3-fold triple, generic interior of slide | ≈37 | — | generic n=3 |
