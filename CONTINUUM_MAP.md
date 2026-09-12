# Continuum map — the shapes records live on, and how they extend

Records are not points. Several sit on positive-dimensional regions where the count is
constant, and this file maps those regions: their extent, the walls **inside** them, and which
sub-region extends well. Established 2026-09-08 ([P286](LEDGER.md#p286)); the discovery that
forced it is [P285](LEDGER.md#p285).

**The one-line reason this file exists.** A continuum is a plateau in the COUNT, not a set of
interchangeable configurations. Two members can agree on count and on `by_depth` at every depth
and still extend to different counts. Choosing a representative by cheapness — which every
campaign has done, because height drives cost — silently chooses a point along a parameter that
matters.

**The measured boundaries are recorded in [`data/continuum_boundaries.json`](data/continuum_boundaries.json)**
— parameterisation, fixed cubes, sampled range, and every boundary as an explicit BRACKET
between two sampled values. **No boundary here has been solved for exactly.** The true boundary
is a wall, an algebraic condition, and quoting a bracket endpoint as the boundary would be
wrong. The tables below are the readable form of that file; the file is the record.

## The three objects, and why they are different

| object | definition | constant along the continuum? |
|---|---|---|
| **count plateau** | where `total` is constant | yes, by definition |
| **increment plateau** | where `total(base + c)` − `total(base)` is constant, for a fixed added cube `c` | **NO** |
| **safe base region** | the intersection of the two — bases that extend to the record | **NO** |

The count plateau and the increment plateau have boundaries in **different places**. That is the
whole phenomenon.

## Map 1 — the n = 9 continuum (2787), and its n = 10 extension

Line: `q(t) = (12−t)·A + t·B`, cleared to integers, with

    A = (88787, -9061, 74275, 113786)     the ORIGINAL representative
    B = (88726,  -8954, 74074, 113960)    the SIMPLIFIED one (109,-11,91,140) scaled by 814

The two are 0.2 % apart. Base is the n = 7 record's seven cubes plus `168,-168,168,-415`.

```
t        -24 … -15  -12 … -9   -6 … -3    0 … 3     6 … 24    27 …
n=9         2775       2779      2783      2787      2787      2783
n=10        3913       3917      3921      3925      3921      3917
increment   1138       1138      1138      1138      1134      1134
                                        └ SAFE ┘
                                  └──── count plateau ────┘
```

| boundary | position | what changes |
|---|---|---|
| count plateau, lower | between `t = −3` and `0` | n=9: 2783 → 2787 |
| **increment wall** | between `t = 3` and `6` | increment 1138 → 1134 |
| count plateau, upper | between `t = 24` and `27` | n=9: 2787 → 2783 |

**Safe base region ≈ 22 %** of the continuum along this line. The published n = 10 record's base
sits at `t = 0` — on the count plateau's own lower edge, because [P200] found it by an
"automated boundary climb" that stopped at a boundary.

### Which added cubes see the wall

| tenth cube | n=10 count | walls along the arc |
|---|---|---|
| `6555,6555,6497,6555` | **3925** | 3–6 |
| `1000,-997,13,5` | 3881 | 3–6 |
| `5,-2,3,1` | 3791 | **0–3 and 6–9** |
| `41,17,-23,9` | 3845 | none — flat |
| `3,1,-2,1` | 3835 | none — flat |
| `7,0,0,-3` | 3483 | none — flat |

The continuum carries an **arrangement** of walls; each cube activates a subset. **The
high-scoring extensions are the sensitive ones** — rich interaction with the base means
sensitivity to its geometry, so base position matters exactly where it is most costly to ignore.

## Map 2 — the 727 arc (n = 6), and its n = 7 extension

`P(s) = (1, 19/3 + s, −7 − 3s, −11 − 6s)` cleared to integers — the arc mapped in
[MAXIMISERS.md](MAXIMISERS.md), Cayley direction `(1,−3,−6)` through `(19/3, −7, −11)`.
Verified: `s = 5/2 → (6,53,−87,−156)` and `s = 3 → (3,28,−48,−87)`, both as listed there.

| s | 7/3 | 5/2 | 8/3 | 17/6 | 3 |
|---|---|---|---|---|---|
| n = 6 | 727 | 727 | 727 | 727 | 727 |
| n = 7 with `4,-3,-4,-4` | **1213** | 1209 | 1209 | 1209 | 1209 |

Wall **inside** the arc, between `s = 7/3` and `5/2`; one of five sampled points is the good
one. The same structure at an independent level, on an arc whose bounds come from the existing
record rather than from this construction. (1213 < 1217 is expected — the tower's own sixth
cube `7,14,1,-5` is not on this arc.)

**OBSERVED, not concluded.** MAXIMISERS records 727 for `s ∈ [9/4, 3]`, but measurement gives
725 at `s = 19/6`, **727 again at `s = 10/3`**, 719 at `s = 7/2`. The region may extend past the
documented bound and may not be one interval — or the sampled rationals may sit on coincidence
values. Needs a finer walk before it amends MAXIMISERS.

## What does NOT identify a safe substitution

| criterion | sufficient? | evidence |
|---|---|---|
| same count | no | — |
| same count + full `by_depth` | **no** | [P285]: 3925 vs 3921 |
| same continuum | **no** | same failure; both are on one |
| same outer-vertex count | **no** | 1126 on both sides of the flip |
| same radius signature | **useless** | differs at *every* point, so never says "safe" |
| congruence, base only | no | `B = gA` gives `B + c ≅ A + g⁻¹c`, not `A + c` |
| congruence, base **and** extension | yes | — |

## Consequences for method

1. **Arc position is a search dimension.** No campaign has varied it. Bases were chosen by
   height, i.e. by cost.
2. **Map the increment field, not the count.** The count is constant by construction; the
   increment is what the tower consumes and what carries the structure.
3. **Project downward, not upward.** A base's count constrains nothing above it — the added cube
   meets structure the base count never saw. But an n+1 region projects down to bound its bases.
4. **Re-verify a simplified representative at the level things are built on.** The n = 9
   simplification was verified at n = 9 and silently broke the n = 10 chain.

## Two different dimensions, which must not be conflated

`isolate183.py`'s own docstring states the distinction:

> the n = 2 maximiser 13 is a continuum, the 67s are isolated points, and **727 is isolated
> while sitting in an uncountable plateau. Plateau membership and local isolation are
> independent facts.**

| | what it measures | test |
|---|---|---|
| **coincidence variety** | can the configuration move while keeping ALL its tight coincidence conditions? | `isolate183.py` — second-order variety at the point |
| **count plateau** | can it move while keeping the COUNT? | probe every signed direction; `3^d - 1` survivors means dimension `d` |

Measured, the two disagree sharply:

| record | coincidence variety | count plateau |
|---|---|---|
| 183 (n = 4) | **0** — isolated | **0** — the apparent 3 was a no-op artefact, see Map 0 |
| 727 (n = 6) | **0** — isolated | uncountable — the arcs below |
| 2787 (n = 9) | not measured | ≥ 1 measured here; 4 per RESULTS |

**AND "dimension" is not always the right word.** `runs/dim2785.log` on the 727 arc D:

    v1 (14,2,-3)   +eps 727  -eps 727   holds
    v2 (21,4,-6)   +eps 727  -eps 727   holds
    v1+v2          +eps 721  -eps 721   CHANGES
    v1-v2          +eps 721  -eps 721   CHANGES

Two directions each hold the count and **no combination does** — a **NODE**, two arcs crossing
at the record, not a 2-dimensional surface. A single dimension number would misdescribe it.

## Map 0 — the 183 (n = 4): ISOLATED in BOTH senses

`runs/isolate183.log`:

    183 class 1 (canonical)    count 183 | 108 tight | lineality 1 of 9
                               second-order variety: empty, 0 directions -> ISOLATED
    183 class 2 (wide climb)   count 183 | 108 tight | lineality 1 of 9
                               second-order variety: empty, 0 directions -> ISOLATED

Both 183s are isolated **in the coincidence sense** (lineality 1 = the global-rotation gauge).
The count plateau was believed to be 3-dimensional from `runs/n4_183_dim.out`:

    step 1/32    probed 19682, still 183:  26     (3^d - 1:  d=3 -> 26)

**That reading is an ARTEFACT and is withdrawn.** The probe perturbs Cayley coordinates as
`x*den + d*w`, and cube 1 of the 183 is a HALF-TURN with `w = 0` — so its three deltas are
multiplied by zero and change nothing. Verified directly: of the 19 682 probes, exactly **26 are
byte-identical to the record**, and they are exactly the 26 directions touching only cube 1
(`3^3 - 1 = 26` no-ops). `26 = 3^3 - 1` and `26 = 27 - 1` are the same number by coincidence.

**No genuine neighbour retains 183.** The count plateau is 0-dimensional, agreeing with
`isolate183.log`, with the straight-line walk leaving 183 at the first step, and with an
independent quaternion-axis probe (`src/map_all_shapes.py`) finding 0 of 12 axes holding at two
step sizes.

**RESULTS' phrase "183 is a PLATEAU, not a point" means MORE THAN ONE configuration reaches
183** — two congruence classes — not that a continuum was demonstrated.

Extension is per-pair even between these two: with the same five candidate fifth cubes, class 1
reaches 369 / 355 / 359 / 367 and class 2 reaches 363 / 371 / 353 / 375 — **neither dominates**,
different cubes prefer different bases. So the per-pair structure of [P286] is a property of
EXTENSION, not of continua, and shows up between isolated points too.

## Where the walls themselves are recorded — and one correction (2026-09-08)

A boundary in this map is a BRACKET. The object that ends a bracket is the wall's polynomial,
and until 2026-09-08 nothing recorded one. `data/record_walls.json` records wall GRADIENTS,
which are linearisations at the record point and cannot be solved for a locus.

`data/wall_keys.json` (code: `src/wall_keys.py`) closes that. A wall is completely determined by

    (frame i, group ((j,k,sgn),...), sig, c0)   +   the record quaternions

and that tuple is the whole argument list of `dimension.branch_numerator`, which returns the
exact polynomial `P` with `f = 1  <=>  P = 0`. **The key is the polynomial.** Recorded for
n = 4..8 (12 / 18 / 27 / 51 / 75 distinct walls) and arcA (20). `n4_183` is recorded as
UNEVALUABLE rather than skipped — cube 1 is a half-turn, so the record sits at Cayley infinity
and this chart has no point for it ([P287](LEDGER.md#p287)).

Two restrictions are provided, and the second is the one this map needs:
`W.on_line` restricts a wall to a **Cayley** line; `W.on_quat_line` restricts it to a
**quaternion** line, which is the form every bracket in this document actually takes
(`solve_wall.py` moves a cube along `q(t) = (12-t)A + tB`). A quaternion line is a Möbius curve
in Cayley coordinates, not a line, so the first does not substitute for the second. Demonstrated
on the n = 6 record: `P(0) = 0` on 27/27 walls, degrees 2 and 4, 8 walls carrying a nonzero
rational root. **The n = 9 wall therefore needs no new machinery — only the cost of building
conditions at a 10-cube configuration, which has never been done.**

**CORRECTION, dated 2026-09-08.** Gating that export found `branch_numerator` wrong whenever a
condition's two normals come from different cubes ([P288](LEDGER.md#p288),
[FAILURE_MODES 32](FAILURE_MODES.md)). The consumer, `variety_incremental`, answers **ISOLATED**
when over-constrained, so the bug's generic effect is a false ISOLATED. *(Corrected 2026-09-09:
`wrong_P = correct_P + m1[c0](d1 − d2)`, so the wrong polynomial can also have FALSE ZEROS on a
codimension-1 set, which would admit a direction not in the wall. The bias is generic, not
guaranteed — I first wrote "could only ever", which is a claim about all points drawn from an
argument about typical ones.)*

- **Map 0 below is UNCHANGED.** n = 4 has zero cross-cube conditions, so the fix is
  bit-identical there; both 183s were re-confirmed ISOLATED under the fixed code, as was 393.
- **The n = 6 and n = 7 verdicts were withdrawn and re-run the same day. n = 7 CHANGED.**

      n =           4    5    6    7    8
      lineality     1    1    1    2    3      (unaffected -- from gradients)
      2nd-order     0    0    0    1    2      directions surviving
      verdict     ISO  ISO  ISO  NOT  NOT

  The 1217 record is **not** an isolated point of the coincidence variety; it lies on a curve,
  and the pre-fix run said the opposite. n = 8 had never been reached and reads 2 directions.
  The tower's coincidence-variety dimension is a rising sequence beginning at n = 7, not the
  flat "isolated everywhere" it appeared to be.

  **This does not overturn [P117](LEDGER.md#p117), and the distinction is exactly the one this
  document is about.** The n = 7 curve was confirmed by an independent route — `branch_value`,
  which never performs the cancellation that was wrong — with all 300 conditions exactly tight
  at `t = 0, 1/64, 1/8, 1/2, 1, −3/7`. But the count does not follow it:

      t      0     1/64   1/8    1/2    1
      count  1217  1213   1209   1203   1177

  The curve holds the **tight set** and loses the **count** immediately. P117 engine-verified
  its directions, which is a count check. So: the coincidence variety is corrected; records as
  maximisers are untouched. `solve_shapes.py` prints `NOT isolated` from the variety alone with
  no engine step, and its label should be read as the weaker claim.
- **The count-plateau results in this document are unaffected**: `arc_eps.tangents_eps` reaches
  `dimension` only through `cached_conditions`, `nullspace` and `count_at`. So are all lineality
  numbers, which come from gradients.

## Map 3 — the level anatomy, and why nothing happens "at n = 7"

This was listed as unmapped: *why does the coincidence variety start having dimension at
n = 7?* Tabulating every level answers it, and the answer is that the threshold belongs to a
different sequence ([P289](LEDGER.md#p289)).

      n   ambient  tight  walls  rank  lineality  surviving directions
      4       9     108     12      8      1          0    ISOLATED
      5      12     168     18     11      1          0    ISOLATED
      6      15     216     27     14      1          0    ISOLATED
      7      18     300     51     16      2          1    not isolated
      8      21     384     75     18      3          2    not isolated
      9      24     420     83     20      4         11    not isolated

**CORRECTED — `variety = lineality − 1` is REFUTED.** It was recorded as a prediction of 3 at
n = 9 and the measurement came back **12** — of which 11 are distinct up to scale, the twelfth being a
chart-union duplicate (n = 7 and n = 8 re-checked and clean). Worse, the column is not a dimension at all:
`variety_incremental` returns "finitely many points" of `P(null(J))`, so `0, 0, 0, 1, 2, 12`
counts isolated DIRECTIONS and the variety is 0-dimensional everywhere measured. The fit was
two small numbers across three levels, two of which were identically zero.

What survives is the verdict — zero versus nonzero — and the threshold: nothing distinguishes
n = 7 except that lineality reaches 2, which is where a `P(null(J))` first has room for a point
to survive. Where the freedom lives is legible even though the count is not: the surviving directions occupy
coordinates `[15]` at n = 7, `[15, 20]` at n = 8, and `[15, 20, 21, 22, 23]` at n = 9 — the same
two single axes, plus the ninth cube in **all three** of its components. The jump from 2 to 11
comes from that one cube, not from a change in the older ones, which turns the open question
from a sequence into a question about a single cube.

**The event is the rank increment.** Each added cube brings 3 coordinates and adds rank

      3, 3, 2, 2, 2       (n = 4→5, 5→6, 6→7, 7→8, 8→9)

so from n = 7 a new cube's walls pin only two of its three degrees of freedom. That happens at
n = 6→7, and *why* it happens there is the sharper form of the question and is still open.

The n = 9 entry was a **prediction of 3**, recorded in P289 before the solve returned so that
agreement would be a test. It came back 12, which is what refuted the pattern and, with it, the
reading of that column as a dimension.

## Map 4 — the n = 9 region: 4-dimensional, confirmed, and a discrepancy worth chasing

The region's dimension was asserted in the RESULTS n = 9 row; it is now measured. On the
**simplified** representative (`109,-11,91,140`, height 140):

    count 2787 | ambient 24 | 420 tight (0 degenerate, 10 164 loose) | 83 distinct walls
    lineality 4

**RESULTS records 99 walls at n = 9**, and the direct comparison ([P290](LEDGER.md#p290))
resolved that differently from how it was framed here. The 99 is real but belongs to **2785**,
the record 2787 superseded:

    configuration                   count   tight   walls   rank  lineality   directions
    2785 (superseded)                2785     468      99     20      4         --
    2787 original,   h = 113 786     2787     396      76     19      5         15
    2787 simplified, h = 140         2787     420      83     20      4         11

Both 2787 representatives are NOT isolated, and they disagree on how many directions survive —
11 against 15 — so even that count is representative-dependent at n = 9. But the directions
occupy **the same five ambient coordinates in both**, `15, 20, 21, 22, 23`: cube 6 in one
component, cube 7 in one, cube 8 in all three. Where the freedom lives is a property of the
tower, not of the representative, even though every count differs.

Two consequences. **`walls = 24n − 117` is a window over n = 6..8**, not n = 6..9 — its last
rung was measured on a configuration that no longer holds the level, and never re-measured when
it was superseded. And **the two 2787 representatives are structurally different points**: 396
vs 420 tight, 76 vs 83 walls, lineality 5 vs 4. That is the observable [P285](LEDGER.md#p285)
looked for and could not name — they agree in count and in `by_depth` at all nine depths and
agree in nothing else. A 4-dimensional region contains many points with the same count; calling
one a "simplification" of the other treated two of them as one.

*Still only one line of the four dimensions has been walked; the region's extent is unmapped.*

## Map 5 — the 67 ↔ 67 dihedral family

The family is parameterised by an angle ψ, with the two n = 3 maximisers at the octahedral
angle `arcsin(1/√3) = 35.264°` and the golden angle `69.095°`. Both are **irrational**, so no
rational scan lands on either: they are punctures in a uniform region, not peaks on a slope
(`climb_limit.py` — the count is 55 at every rational approach over twelve orders of magnitude).

`region_shape.py` sampled two hand-placed windows. Re-running it shows its **lower window is not
an edge at all** — all nine points return 55, so the window was placed where the edge was
believed to be and missed it. Its upper window does bracket something: 55 below, 43 from
ψ ≈ 69.222 up, with the golden 67 at 69.095 just inside the lower side.

**Both 67s are now in `data/wall_keys.json`**, over ℚ(√2) and ℚ(√5):

    octahedral  count 67 | 60 tight, 0 degenerate | 6 distinct walls | rank 6 | lineality 0
    golden      count 67 | 72 tight, 0 degenerate | 9 distinct walls | rank 6 | lineality 0

6 and 9 walls is exactly what RESULTS records, and rank 6 = ambient with lineality 0 is the
"pinned at first order" account arrived at independently of [P118](LEDGER.md#p118)'s face
enumeration. The polynomial route needed one fix to run over a field — `sympify` cannot parse
`1/2+1/2√5`, and `dimension`'s own converter `_sp = qf_to_sp` handles both Fractions and QF —
after which `P(record) = 0` on all 60 and all 72 conditions. **Gate G2 does not apply over a
field** (its probe line is rational) and is recorded as unevaluated, not as a pass.

**The extension to n = 4 is not unmapped either.** [P134](LEDGER.md#p134) caps it at **177** by
three methods with different biases — 11 927 configurations from `extend67.py`, 960 candidates
exhausted in the two-67-triple family, 15 663 counted across seven fields — where the rational
record is 183, and the 177 is the golden four-cube compound. All three sample or enumerate
around the 67s and none solves a wall system, so it is a convergent ceiling with a stated shared
bias, not a bound.

`src/map_dihedral.py` replaces the two windows with a full scan (1 278 distinct ψ, 1.29° to
88.71°) and reports every count change, so edges are found rather than confirmed
([P291](LEDGER.md#p291)):

    count  31   ψ ∈ [ 1.28749,  9.72903]   139 samples
    count  43   ψ ∈ [ 9.79818, 20.87495]   158 samples
    count  55   ψ ∈ [20.98295, 69.01705]   684 samples
    count  43   ψ ∈ [69.12505, 80.20182]   158 samples
    count  31   ψ ∈ [80.27097, 88.71251]   139 samples

Every mirrored edge pair sums to **exactly 90.000000** under ψ → 90 − ψ — a check the scan had
to pass, and the reason both 67s cannot be generic points of the family.

**The two maximisers do not sit alike.** The octahedral 67 (35.264°) is 14° inside the 55 run.
The golden 67 (69.095°) is **not inside it**: it falls in the 55 → 43 boundary bracket. That
bracket was then closed rather than left as one — `src/golden_edge.py` approaches from both
sides with triples up to r = 60 000 and gets **55 on all six approaches below** (closest gap
0.0045°) and **43 on all six above** (closest 0.0019°). The counts differ across the angle, so
**the golden 67 sits ON the 55/43 wall**, bracketed to (69.09032984, 69.09673411), width 0.0064°.

Not claimed: that the wall passes *exactly* through the golden angle. Sampling locates the
transition inside a bracket containing it; proving the algebraic locus meets it needs the wall
condition solved, which the wall-key index now makes possible over both fields. And no rational
scan lands on either angle — both are irrational, which is what makes them punctures.

This is a candidate explanation for the neighbourhood asymmetry [P121](LEDGER.md#p121) recorded
as a bare fact (728 faces vs 2 196): a point on a wall and a point deep inside a uniform region
are different objects. Candidate, not derivation.

## Map 6 — the 727 four-arc node: ONE structural class

[P293](LEDGER.md#p293). Representatives are the simplest rational strictly inside each solved
extent, each gated on counting 727:

    arc   s      count   walls   lineality   variety
    D     0       727      27        1       empty          <- s = 0 IS the record
    A     3       727      20        2       2 directions
    B     1/2     727      20        2       2 directions
    C     2       727      20        2       2 directions

Read naively this says arc D is the constrained arc. It does not: D's representative is the
record itself while the others are interior points, so the table confounds *which arc* with
*where on the arc*. The control settles it — arc D at s = 1/8 and s = −1/16, both inside its own
extent, gives **20 / 2 / 2, identical to A, B and C**.

**So the node has one structural class, and the record is the special POINT, not the special
ARC.** That predicted arcs A, B and C each hold their own special points.

**They do, and the prediction's payoff was negative — [P294](LEDGER.md#p294).** Solving each
arc's wall polynomials (rather than walking `s`) gives nine special points, with arc D's `s = 0`
rediscovered as the control. `congruent.py` collapses the nine to **six compounds**:

    class 0   725   D@-2/19,  B@43/105
    class 1   727   D@0,      B@16/35,   C@132/29      <- the record
    class 2   713   D@2/9
    class 3   725   A@13/6
    class 4   725   A@19/6
    class 5   723   C@164/87

**The record lies on three of the four arcs** — which is what makes the node a node: the arcs
cross there. Arc A does not reach it (the record's sixth cube would sit at `s = -13/3`, far
outside A's extent) and carries two compounds found on no other arc.

So there is **no new extension base here**: every 727 among the special points is the record
respelled. [OQ 17](OPEN_QUESTIONS.md)'s extension question stays open, and is now sharper —
the tower extends one point of one arc because the other arcs' special points are either that
same compound or count less.

## Map 7 — the 1217 plateau, and how boundaries travel up the tower

Solved 2026-09-12. The n = 7 plateau is **2-dimensional** — a pentagon, not the parallelogram
its two directions span ([P299](LEDGER.md#p299), [P301](LEDGER.md#p301)):

- one direction inside the **fibre** (moves the added 7th cube), bracketed (1/512, 1/266) up and
  (4/89, 1/22) down;
- one along the **base** (the arc D lift, moving the 6th cube);
- a **third wall** aligned with neither, solved as a curve of total degree 4 — the straight line
  first inferred from two grid points was wrong by 17% of the region's width.

**Boundaries inherit selectively** ([P303](LEDGER.md#p303)). Carrying the same three brackets to
n = 8 and n = 9 — the latter keeps the 1217 seven while replacing n = 8's eighth cube:

    boundary          n = 7          n = 8          n = 9        inherited?
    fibre +e15      1217->1213    1895->1891    2787->2783      yes, exactly
    third wall      1217->1213    1895->1891    2787->2783      yes, exactly
    base (arc D)    wall at -2/19  (-1/50,-1/25) (-1/50,-1/25)  NO, contracts ~5x

The two inherited boundaries cost **exactly 4 regions** to cross at every level, while the record
climbs 1217 → 1895 → 2787. The contracting one is cut by a new wall from the added cubes — and
n = 8's and n = 9's contracting walls are **different** (frames 7 and 2, different groups,
different cubes); the shared bracket was coarseness. **Criterion:** a boundary is inherited iff
no new condition is crossed earlier in that direction, readable from the group's cube indices.

**And most walls crossed change nothing.** Of the wall crossings solved along these rays,
**4 of 6 leave the count unchanged** — which is why the plateau's boundary had to be found by
counting rather than by asking which walls are crossed, and is the substance of
[OQ 33](OPEN_QUESTIONS.md).

> **SCOPE, for everything dimensional in this document** ([P298](LEDGER.md#p298)): count-plateau
> tangent counts here are LOWER BOUNDS. The searches build candidates from wall gradients,
> assuming a tangent lies in every wall; a direction crossing 7 of 51 walls holds the count at
> n = 7. n = 4, 5, 6 are unresolved rather than zero.

## Not yet mapped

Everything listed here on 2026-09-08 is now mapped (Maps 3–6). What remains is what those maps
opened:

- **why the rank increment drops from 3 to 2 at n = 6 → 7.** Map 3 locates the event and does
  not explain it. The fitted law that looked like an explanation was refuted
  ([P289](LEDGER.md#p289)).
- **why the ninth cube is free in all three components** when the seventh and eighth are each
  free in one. A question about one cube, not about a sequence.
- **the n = 9 region's other three dimensions.** One line is walked; the region is 4-dimensional.
- **the dihedral family's exact edges.** The scan gives brackets. Whether the 55/43 wall passes
  exactly through the golden angle needs the wall condition solved, which the wall-key index now
  permits over ℚ(√5).
- **the dihedral family's extension to n = 4** beyond [P134](LEDGER.md#p134)'s sampled ceiling
  of 177 — no wall system has been solved there.
- **do arcs A, B, C hold special points of their own?** Map 6 predicts they should; nothing has
  looked.
- **wall keys** are recorded for n = 4..8, arcA and both 67s. The 727 arcs A–C and the n = 9
  region have their keys in `data/arc_node_map.json` and `data/n9_region_map.json` but are not
  folded into `data/wall_keys.json`.
