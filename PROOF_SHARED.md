# The shared-face-plane case: charging with tie patches

*Draft, 2026-10-04/05 ([P418](LEDGER.md#p418)–[P422](LEDGER.md#p422)). Not externally reviewed.
Companion to [PROOF_BAND.md](PROOF_BAND.md), whose notation it uses.*

**Goal.** Plan item 2 needs `d2 <= 70` for compounds in which two cubes share a face plane. With
the unconditional `d1 <= 104` and [P413]'s `d3 <= 20`, that gives `max(4) <= 195`.

**Result of this draft.**
- For exactly one sharing pair: `d2 <= 62`, so `max(4) <= 104 + 62 + 20 + 1 = 187` there (§1-4).
- For every sharing structure: `max(4) <= 187` (§5).
- With [PROOF_BAND](PROOF_BAND.md)'s no-shared-plane case, **`max(4) <= 195` with no hypothesis.**
- Two compounds with identical cubes count as a 3-compound (`<= 67`): every `D(A)` holding exactly
  one of the two is empty.

## 1. The objects with patches

Let `a`, `b` share the face plane with normal `f`; no other pair shares a plane.
- Near `+f`, work in the plane `f·u = 1`. The cross-sections of `a` and `b` are their `f`-faces,
  two unit squares about the same centre. Their intersection is an octagon `O`, on which
  `M_a = M_b = f·u`.
- The cross-sections `P_c`, `P_d` of the other two cubes are convex polygons. Each contains the
  centre in its interior, because neither cube has a face plane through `f`.
- Off `O_±`, two cubes tie only along curves: a 2D tie needs a common nearest point in the circle
  model, which is a shared plane.

Let `Γ` be the closed set where reach ranks 2 and 3 tie, and `Γ°` its interior (the **patches**).
Write `G' = Γ ∖ Γ°`, a finite graph, with `p` the number of components of `Γ°`.
- `Γ°` is the part of `int O_±` where exactly one of `c`, `d` is outer: `O ∩ (P_c Δ P_d)`.
- For a triple `S`, `B_S`, `B_S°`, `G'_S` and `p_S` are defined the same way. `B_S°` is nonempty only for
  `S ⊃ {a, b}`. There it is `int O ∩ P_z`, where `z` is the third cube: convex, containing the
  centre. So `p_S = 2` for the two triples containing the pair, and 0 for the other two.

**Euler.** `S² ∖ G'` is the disjoint union of `S² ∖ Γ` (whose components are the `d2` regions) and
`Γ°` (the `p` patches). So

    d2  = E' − V' + 1 + c' − p,          d2(S) = E'_S − V'_S + 1 + c'_S − p_S,

with `c'`, `c'_S` the component counts of the graphs.

## 2. The charging, reduced to a local inequality (L)

`E − V = Σ_v (deg v / 2 − 1)` for any finite graph. So

    E' − V'  <=  Σ_S (E'_S − V'_S)

follows from two things:

    (L)  at every vertex v of G':   deg_G'(v) − 2  <=  Σ_{S : v ∈ G'_S} (deg_{G'_S}(v) − 2),

and every `G'_S` having minimum degree at least 2, so that vertices of `G'_S` not charged cost
nothing.

The minimum-degree condition holds, for every sharing structure:
- **Never empty.** Through `v`, a diagram's tie set is not empty around `v`. No cube is strictly
  innermost in every direction: at another tying cube's own point, that cube is at distance 0.
- **Never exactly one end.** Isolated ties are crossings (§3), and a label on a circle cannot
  change exactly once.
- **The face-centre case.** At `F = 1`, a shared face centre, the circle has radius 0 and the
  model degenerates. There `σ ≡ 0` exactly, so the tying cubes tie on a neighbourhood: `v` is
  interior to a patch and not on `G'`.

For one sharing pair, it also follows directly:
- In the circle model, `B_S`'s tie set around `v` is the set of directions whose nearest point
  carries two or more of `S`'s colours. Its degree is the number of colour-set changes around the
  circle.
- That is at least 2 unless all of `S`'s tying points carry the same set. In that case `v` is
  interior to a patch and is not on `G'_S`.

## 3. The band lemma survives with patches, at no loss

**Tree.** By G2, applied to `G'`, whose faces are the regions and the patches:

    c' − 1 = Σ_R (j_R − 1) + Σ_Q (j_Q − 1).

A patch `Q` is a component of `K1 ∖ K2` with `K1 = O ∩ P_c` and `K2 = P_d` convex (or with `c`
and `d` swapped), so `j_Q <= 2`.

**G1, G2, G4, G5, G6 and Lemma C carry over unchanged.**
- G1, G2 and G6 are topology.
- For G4, use a face centre of the pair's cube other than `±f`. It is strictly innermost there.
- For G5, a meeting point in a patch of `B_{P∪z}` still lies in `B_{P∪z}`, so it is in a live `L`.
- `c(B_S) <= c'_S`, since removing a patch's interior keeps its boundary.
- Isolated points do not occur: in the circle model a tie is a crossing or a 2D sector, never
  isolated.

**G3 needs one new case.** A `K_P` adjacent to a band region `R` (label `P`) along an arc of `G'`
reaches across the arc either:
- a region: a 1D tie is always a crossing (below), so that region's label is not `P`, and G3
  holds as before; or
- a patch `Q`.

For a patch, list its boundary arcs and the label on their far side. Take `c` outer and `d`
inner on `Q`:

    ∂O where b leaves face f    {c, a}
    ∂O where a leaves face f    {c, b}
    ∂P_c (c turns inner)        {a, b}
    ∂P_d (d turns outer)        {c, d}

`Q` is a component of `K1 ∖ K2` with both sets containing the centre. So `∂Q` contains an arc of
`∂K2` (label `{c, d}`) and an arc of `∂K1` (some other label). Hence the regions next to `Q` carry at least two labels.
- One of them is not `P` and lies in `K_P` together with `Q`.
- A region with a label other than `P` lies in `R_c ∪ R_d`, by the cube it contains outside `P`.

So G3 holds for every `K_P`, and

    Σ_R (j_R − 1)  <=  Σ_S (c'_S − 1).

**1D ties are crossings.** In the circle model, `d_x − d_y` has slopes in `{−2, 0, 2}`. A
non-crossing isolated zero needs a slope change from −2 to +2. That forces a point of both `x`
and `y` at that direction, a shared point, which ties on a whole sector instead.

## 4. Assembly, and the status of (L)

    d2  <=  Σ_S (d2(S) + p_S − 1 − c'_S) + 1 + c' − p
        =   Σ_S d2(S) + Σ_S p_S − 6 + Σ_Q (j_Q − 2) − Σ_S (c'_S − 1) + Σ_R (j_R − 1)
        <=  Σ_S d2(S) + Σ_S p_S − 6
        <=  (14 + 14 + 18 + 18) + 4 − 6  =  62.

Each step:
- `d2(S) <= 14` for the two triples containing the pair: strengthened ANCHOR, [P413], [P416].
  [P416]'s proof does not use the no-shared-plane scope. Coincident projected points only remove
  directions from the strict cone, and its strengthened form addresses shared face directions
  directly.
- `j_Q <= 2`, so `Σ_Q (j_Q − 2) <= 0`.
- The last bracket is `<= 0` by §3.

**(L), by case.** Here `T` is the set of cubes tying at `v`, and `k` the number of strictly outer
cubes. Only these cases put `v` on `Γ`:
- **`k = 1`, `|T| = 2`:** `Γ = B_{T ∪ outer}` near `v`, as sets. Equal degrees.
- **`k = 0`, `|T| = 3`:** `Γ = B_T` as sets. Equal degrees.
- **`k = 1`, `|T| = 3`:** `Γ` is `T`'s top diagram `τ`. Proof below.
- **`k = 0`, `|T| = 4`:** `Γ` is the middle diagram `μ`. Proof below.

**Degrees as sums of ends.** For a closed tie set `A` on the circle of directions and a direction
`θ`, let `e_A(θ) = 1` if `θ ∈ A` and `A` does not contain both sides of `θ`; otherwise 0.
Then `deg A = Σ_θ e_A(θ)`, counting an isolated tie and an arc end alike.

**Which directions can three cubes tie in (one sharing pair).**
*(CORRECTED 2026-10-04, same day, at the advisor's catch. The first draft said "never". Its step
2 placed the common nearest point at `θ0 − δ`, but it can be on either side.)*
1. Suppose three cubes have equal distance `δ` in direction `θ0`. Each distance function has slope
   ±1 on each side.
2. Two of the three share a slope on the left. Equal values and equal slopes mean the same
   nearest point, at `θ0 − δ` or at `θ0 + δ`, so a shared point. The same holds on the right.
3. With one sharing pair, the same-slope pair on each side is `{a, b}`, at their shared point `s`.
   - If `s` were on opposite sides of `θ0` for the two sides, then `δ = 0` or `δ = 180°`. That
     would put the third cube's point(s) at `s`, a second sharing.
   - So `s` is on ONE side, and `a`, `b` tie on both sides of `θ0`.
   - The third cube `c` has a point `q` on the other side, at the same distance: `θ0` is the
     bisector of `s` and `q`. `c` crosses the tied pair there.
4. The fourth cube cannot also tie at `θ0`: it would need to own `s` or `q`.

These directions are generic. Every end of a `B_abc` patch is one.
- `src/probes/patch_charging_local.py --direction-ties` finds them in 911 and 1100 of 1 500
  sampled configurations (general and realisable).
- Every one is of this type, with 0 of any other type.

Elsewhere the ties are pairs: one pair, or two disjoint pairs at different values. Near such a
direction, every level diagram either coincides with the tying pair's tie set or misses it.

**Case `k = 1`, `|T| = 3`.** At a pair-only direction, a tying pair is either the top two or the
bottom two.
- At the three-cube direction above (`a = b` on both sides, `c` crossing), both sides of the
  identity are 2: `e_τ = e_β = 1`, while `e_π` is 0, 1 and 1.
- So

    deg τ + deg β  =  Σ_{pairs π ⊂ T} deg π        (exactly, patches included),

where `β` is `B_T`. The right side of (L) has `B_T` and the three triples `{outer} ∪ π`, whose
tie sets near `v` are the `π`. Let `#on` be the number of `π` that are not the whole circle;
those are the ones with `v ∈ G'`. Then

    right − left  =  (deg β − 2) + Σ_{π on} (deg π − 2) − (deg τ − 2)  =  2 deg β − 2·#on.

- `deg β` is the number of colour-set changes around the circle.
  - It is ≥ 3 if three colour sets occur.
  - With `T`'s three cubes and one shared point, only two colour sets means `{a,b}` and `{c}`.
    Then `a` and `b` both own only `s`, so `π_ab` is the whole circle and `#on <= 2`.
- `β` is never the whole circle (three cubes cannot all own one point).
- `τ` is never empty: where the outermost cube changes, the top two tie, and no cube is strictly
  outermost all the way round (at its own point its distance is 0).

So right − left ≥ 0.

**Case `k = 0`, `|T| = 4`.** For a pair `{x, y}` tying at `θ`, with the other two strictly above
or below:
- `μ` meets `θ` only if exactly one of them is above.
- `B_{xyz}` meets it only if `z` is above.

So `e_μ = e_π·[#above = 1]` and `Σ_S e_{B_S} = e_π·#above`.
- At the three-cube direction, with `d` the cube not tying there, checked directly:
  - `d` outer: `Σ_S e_{B_S} = 3 = e_μ + 2·e_{C12} = 1 + 2`;
  - `d` inner: `1 = 1 + 0`.
- Summing,

    Σ_S deg B_S  =  deg μ + 2·C12,

with `C12` the degree of the four cubes' innermost diagram ([P404]'s identity, now with patches).
- `C12` is the number of colour-set changes. It is at least 3, since `c`, `d` and some set
  containing `a` all occur.
- Then right − left `= 2·C12 + 2 − 2·#on >= 0` for `#on <= 4`.

**(L) is therefore proved for exactly one sharing pair.** Without sharing, the same argument
re-proves [P404]/[P405]'s `X = 0`, `W4u = 0` without the top-versus-bottom lemma.

**Checked.**
- **Exact circle model** (`src/probes/patch_charging_local.py`, `data/patch_charging_local.json`).
  - Integer angles, with every critical direction sampled.
  - Shared-point patterns: none, a pair, two disjoint pairs, a hub, three on an axis.
  - Point sets either general or realisable for cubes. Realisable means one common value `F`,
    with two-point cubes `θ(F)` apart.
  - **Excess 0 in every sampled configuration** (3 000 per row, 10 rows).
  - The two identities above hold in every applicable case with zero or one shared point. They
    fail only with two or more, as the three-cube-tie step predicts.
  - No isolated points.
  - The must-fail control ([P405]'s blades: one radius per cube) produces violations.
  - Two weaker controls fired too rarely and were replaced, as recorded in the docstring.
- **Per compound** (`src/probes/shared_oracle.py`, `data/shared_oracle.json`).
  - The chain before the band and patch terms are dropped predicts `d2 <= Σ_S d2(S) − 2` for one
    sharing pair.
  - **0 violations in 387 compounds, minimum slack 5.** Every multi-pair structure also satisfies
    its analogue `Σ_S d2(S) + Σ_S p_S − 6` (436 rows).

## 5. Two or more sharing pairs ([P419](LEDGER.md#p419)–[P422](LEDGER.md#p422))

**Structures.**
- Two cubes sharing two planes are one cube.
- A triangle of three distinct planes forces that: its normals are orthonormal.
- A 4-cycle forces an identical pair.
- So the realisable structures are eight: one pair, two disjoint pairs, hub, axis triple, axis
  four, star, path of four, and axis triple plus a pair.

**Budgets.**
- A class of `m` cubes on one plane, with `k >= 2` members in a triple `S`, costs `S` `2k`
  anchors (strengthened ANCHOR). It adds at most 2 patch faces: per `±n`, one convex or
  star-shaped piece, and merging only lowers `p_S`.
- So `Σ_S (d2(S) + p_S) <= 72` minus 4 per pair class, 10 per axis triple, 16 for axis four.
- With §4's chain, before the excess, band and hole terms:

      pair 62   two disjoint 58   hub 58   axis3 56   axis4 50   star 54   path 54   axis3+pair 52

  The target is 70.

**The local inequality (L).**
- Per direction, exhaustively (`direction_types.py`): `Σ_S e_{B_S} − e_μ >= 2 e_C12` and
  `Σ e_π − e_τ − e_β >= 0`, for any sharing.
- So (L) can fail only at vertices with few ends (`C12 <= 2`, or bottom degree `<= 2`), where
  nearly every active point is shared.
- Summed, (L) at a four-fold vertex is exactly `deg λ + ΣW/2 >= #on − 1` (`λ` innermost). At a
  triple vertex it is `deg β + ΣD/2 >= #on_π − [β = whole circle]`.
- The residue is SETTLED exactly ([P420](LEDGER.md#p420), `residue_exact.py`).
  - At a residue vertex every point is shared except one cube's.
  - That gives 49 owner placements, in at most two parameters (`θ`, an offset). Corners give
    none.
  - Every cell of each arrangement was evaluated in an exact rational circle model: 0 failures,
    with tight cases present.
  - Earlier targeted sampling (`lowend_check.py`, 36 948 vertices) agrees.
- **So (L) holds for every sharing structure.**

**The chain with holes.** Alexander duality gives `d2 = 1 + b1(Γ)`. With compactly supported χ,
`χ(Γ) = V − E + χ(Γ°)`, and likewise per triple. The band lemma in the form
`c(Γ) − 1 <= Σ_S (c(B_S) − 1)` then gives

    d2  <=  Σ_S (d2(S) + χ(B_S°)) − 6 − χ(Γ°),

with `χ(B_S°) <= 2` per sharing class in `S`. For one pair this is §4's chain.

**The glue lemma: patch holes arise only along hub edges.**
- `Γ°` is the union of class pieces. Per class and per `±n`, a piece is simply connected
  (axis: star-shaped) or an annulus (pair: convex minus convex).
- The pieces are glued along arcs. Every glue arc lies on an edge, between the two classes'
  faces, of a cube belonging to BOTH classes.
- **Algebra.** Some tie fails across the arc, so its cube leaves face `n`, and the arc is on the
  circle `(n − m_x)·u = 0`. All tying cubes share one value there, so the arc is also on a
  bisector `(n ∓ n′)·u = 0`. The two circles coincide only if `n·n′ = 0` and `m_x = ±n′`.
- **Exhaustively** (`glue_check.py`). With disjoint classes, Γ's tie set is never the whole
  circle: 32 patterns, every cell, with a positive hub control.
- *(Corrected 2026-10-05: [P421] first said disjoint classes could glue in a degenerate case.
  Solving that case shows it is impossible.)*

**Counting.**
- Along a hub edge, each other cube's status is cut out by convex conditions, so there are at
  most 2 glue arcs per edge.
- Each pair of classes through a hub has 4 such edges, which gives `m`:

      hub 8    axis3 + pair 8    path 16    star 12 (<= 1 per edge: the third cube is
                                                     strictly inner along the whole edge;
                                                     not needed)

- Mayer–Vietoris gives `−χ(Γ°) <= m − (simply connected pieces) <= m`.

**G3 for every patch.**
- A pair piece borders, across `∂P_w`, a region labelled by the complement of its tying pair.
  That neighbour is always a region, never a patch.
- A merged patch contains pieces with different tying pairs.
- An axis piece is star-shaped, and a single exit label on every ray would nest two distinct
  concentric congruent squares.
- G4 uses a strictly innermost face centre of some cube in `P`. Only the star's hub lacks one.

**Per-structure `d3`.** Strengthened ANCHOR at `n = 4` gives
`d3 <= 24 − 2·(cube, shared normal) incidences`, attained by every structure's climbed best. So
`195` needs `d2 <= 90 − d3`:

    structure     d3   d2 needed   d2 bound (budget + m)   max(4) <=
    pair          20      70             62                  187
    two disjoint  16      74             58                  179
    hub           16      74             66                  187
    axis3         18      72             56                  179
    axis4         16      74             50                  171
    star          12      78             66                  183
    path          12      78             70                  187
    axis3+pair    14      76             60                  179

Per-edge tolerance (room / hub edges) is 4, 3, 2 and 6 for hub, path, star and axis3 + pair, so
the crude bound of 2 suffices everywhere.

**Measured.** The `d2` ceilings, lower bounds from climbs: two disjoint 44, hub 42, axis3 42,
axis4 16, star 30, path 28, axis3 + pair 30. The per-compound oracle has minimum slack 4 to 34
([P421](LEDGER.md#p421)).

## 6. For the external read

- The computer-assisted steps:
  - the direction-type enumeration ([P419]);
  - the residue's cell enumeration ([P420]);
  - the local glue check.
  The reductions that make each one finite are in PROOF_CHECK.
- The topology: the χ_c chain, Mayer–Vietoris for glued pieces, and G2/G5 as in PROOF_BAND.
- The glue lemma's algebra, and the per-edge interval count.
