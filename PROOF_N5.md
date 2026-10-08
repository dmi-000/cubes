# Five cubes: `max(5) ≤ 485` with at most one shared face plane

*Draft, 2026-10-05 ([P428](LEDGER.md#p428), [P430](LEDGER.md#p430)). Not yet externally reviewed.*

**Context.** [P425](LEDGER.md#p425) reduced `max(5) ≤ 457` to two hypotheses, H1 and H2. Its
explanation of the subset identities was CORRECTED by [P427](LEDGER.md#p427); the identities and the
reduction stand. The scope throughout is compounds of five cubes with no two cubes sharing a face
plane.
- **Part 1** proves H1, the charging inequality.
- **Part 2** proves the component lemma level by level at levels 2 and 3, by [PROOF_BAND](PROOF_BAND.md)'s
  argument with a different label.
- **Part 3** handles the top level and assembles the bound:

      total  ≤  457 + max(0, 2c4 − d4)  ≤  485,

  with 457 whenever `d4 ≥ 2c4`, in particular whenever the top-level graph has at most two
  components.

- **Part 4** (added 2026-10-07) extends the bound to compounds with exactly one pair sharing a face
  plane: `total ≤ 441 + 2c4′ − d4 ≤ 469`.

The bound with no scope condition at n = 5 stays 871 ([P401](LEDGER.md#p401)). Two or more sharing
pairs are not covered.

# Part 1: the charging inequality H1

**Claim (H1).** Let `X_ℓ = E − V` of the level-ℓ graph. Then

    Σ_{triples S} X_S(2)  +  Σ_{4-subsets S} X_S(3)   ≥   X2 + X3 + 2·X4.

## Notation

- Every term in the claim is a sum over points P of a weight `deg/2 − 1`, where `deg` is P's
  degree in that graph. Each point that lies on two or more cube boundaries is treated separately.
- At such a point P:
  - **T** is the set of cubes whose boundary contains P, and `t = |T| ≥ 2`;
  - **c** is the number of other cubes strictly containing P;
  - the remaining cubes do not contain P.
- **The circle model** ([P405](LEDGER.md#p405)). Near P, each cube of T is represented by the
  projections of its active face normals, which all lie on one circle: one point for a face, two
  for an edge, three for a corner.
  - In direction θ, cube x's reach rank among T is set by the angular distance from θ to x's
    nearest point. A larger distance means it reaches farther.
  - Cubes containing P reach farther than all of T in every nearby direction; the others reach
    less far.
  - With no shared face plane, distinct cubes never share a point.
- **Rays.** `e(T, r)` is the number of directions θ in which the r-th and (r+1)-th reach of T tie,
  for `1 ≤ r ≤ t − 1`. These are the arcs of T's local level-r graph leaving P.

## Step 1: the vertex's share is `Σ_θ Δ(θ)/2 − K(t, c)`

**When P lies on a subset's graph.** Take a subset S with level ℓ. Locally, S's level-ℓ graph is
T∩S's level `ℓ − |C∩S|` graph. So P lies on it exactly when `|T∩S| ≥ 2` and
`1 ≤ ℓ − |C∩S| ≤ |T∩S| − 1`. Otherwise no tie at that level occurs near P, and both the weight and
every tie indicator are 0.

**On the graph,** the weight is `(number of tie directions)/2 − 1`.

**Summing.** Collect the terms of the claim at P:
- `Δ(θ)` counts, at direction θ, the subset terms whose level ties at θ, minus the full terms
  (level 4 counted twice);
- `K(t, c)` counts the subset terms on which P lies, minus the full terms on which it lies (level
  4 twice). It depends only on t and c.

So P's share of the slack is `Σ_θ Δ(θ)/2 − K(t, c)`, and H1 follows if `Σ_θ Δ(θ) ≥ 2K(t, c)` at
every P.

## Step 2: a direction's count is at least its rays' pair counts

Let `Δpair(u)` be Δ for a single pair tie with u cubes ranked above it. It is 0, 0, 2, 4 for
u = 0, 1, 2, 3.

**Check 1.** For every weak order of T at θ (every pattern of ties):

    Δ(θ)  ≥  Σ over adjacent tied ranks r, r+1 of  Δpair(c + r − 1).

It is checked exhaustively: 742 weak orders over all `t ≤ 5`, `c ≤ 5 − t`, with 0 failures.
- 279 of them are tight with a positive bound.
- By the circle lemma ([P405]), three cubes cannot tie in one direction unless two share a
  point. So the only multi-tie directions that actually occur are disjoint double pair ties; the
  check covers more than is needed.

Summing over directions gives `Σ_θ Δ(θ) ≥ Σ_r e(T, r) · Δpair(c + r − 1)`.

## Step 3: ray counts

**(R1) `e(T, r) ≥ 2` for every r.**
- Going once round P, the set of T's r farthest-reaching cubes returns to where it started, so it
  cannot change exactly once.
- It cannot change zero times. If it never changed, P would be an isolated tie point. Point at
  one of the top-r cubes' own points: that cube becomes strictly innermost among T, which is the
  transversality argument of [P412](LEDGER.md#p412), applied within T.

**(R2) `e(T, t − 1) ≥ t`.** The bottom level's rays are the colour changes in the cyclic sequence
of points ([P405]). Each of the t colours appears, so there are at least t changes.

**(R3) If `e(T, t − 1) = t` and `t ≥ 3`, then `e(T, t − 2) ≥ t`.**
- Exactly t colour changes means each cube's points form one contiguous block around the circle.
- In any direction, the nearest point of another colour is the first such point clockwise or
  anticlockwise. That point lies in a neighbouring block, so the two innermost cubes are always a
  pair of neighbouring blocks.
- At the switch between blocks i and i+1, the two innermost cubes are i and i+1. So their set runs
  through all t adjacent pairs, which are distinct when `t ≥ 3`.
- Each change of that set is a tie between ranks t−2 and t−1, so there are at least t such
  directions.

## Step 4: the cases

Minimise `Σ_r Δpair(c + r − 1) · e(T, r)` subject to R1–R3, and compare with 2K:

| t | c | 2K | minimum | comment |
|---|---|---|---|---|
| 2 | 0–3 | 0, 0, 4, 8 | 0, 0, 4, 8 | equal: regular arc points carry no slack |
| 3 | 0 | 0 | 0 | |
| 3 | 1 | 6 | 6 | |
| 3 | 2 | 18 | 18 | tight at a three-cube tie point |
| 4 | 0 | 6 | 8 | |
| 4 | 1 | 22 | 24 | |
| 5 | 0 | 22 | 28 | |

The minimum is ≥ 2K in every row, so H1 holds at every point. ∎

## Evidence for Part 1

These are controls, not proof steps.
- **Real compounds.** The formula `Σ_r Δpair(c+r−1) e(T, r)/2 − K(t, c)` reproduces exactly the
  per-vertex slack measured on real compounds: all 21 vertex types in
  `data/vertex_types_n5_slack.json` ([P427](LEDGER.md#p427)). R1–R3 hold on their measured degrees.
- **Circle configurations.** 20 000 exact circle configurations with small-denominator angles,
  where multi-cube ties are frequent: 0 failures, and slack 0 is reached at t = 3.
- **Computer-assisted steps.** Check 1 and the case table (`src/probes/h1_local.py`,
  `data/h1_local.json`).
- **Inherited.** The circle model ([P405]) and transversality ([P412]) were written at n = 4. Both
  are local and do not depend on n; external review should confirm this.
- **Scope.** No shared face plane, as throughout the n = 5 reduction.
- **H2** is handled in Parts 2 and 3: proved at levels 2 and 3, and at the top level replaced by
  the bound of Part 3.

# Part 2: the component lemma at levels 2 and 3

**Claim (Lℓ).** For ℓ = 2 and ℓ = 3 (in general, any `ℓ ≤ n − 2`):

    c_ℓ − 1  ≤  Σ_{S, |S| = ℓ+1} (c(B_S) − 1),

where:
- `c_ℓ` is the number of components of the level-ℓ graph Γℓ (where the ℓ-th and (ℓ+1)-th reach
  tie);
- `B_S` is the bottom diagram of the subset S (where S's two smallest reaches tie).

For ℓ = 2 these are the triples' bottom diagrams; for ℓ = 3, the 4-subsets'. At n = 4, ℓ = 2 this is
the band lemma itself. The proof is [PROOF_BAND](PROOF_BAND.md)'s, written out with one
substitution: the label of a region is its **top-ℓ set** Q (the ℓ cubes reaching farthest), not a
pair.

**Notation.** The **label** of a point off Γℓ is its top-ℓ set Q (`|Q| = ℓ`); it is constant on each
region. A **band region** R has `j_R ≥ 2` complementary components. `X_Q` is the union of the band
regions labelled Q, and the `K_Q` are the components of `S² ∖ X_Q`. For a cube `z ∉ Q`, write
`R_z = {ρ_z > min_{q ∈ Q} ρ_q}`, an open set.

**G0 (scope).** With no shared face plane, every tie crosses, at every level and for any number of
cubes ([P412](LEDGER.md#p412)). So the label changes across every arc of Γℓ, and Γℓ and every `B_S`
are exactly the unions of their arcs.

**G1. Band regions miss the bottom diagrams above them.** On a band region labelled Q, every
`S = Q + z` has Q as its own top-ℓ set, with z strictly last. So `B_S ∩ X_Q = ∅`.

**G2. The region tree.** As in PROOF_BAND (unicoherence of S²):
`c_ℓ − 1 = Σ_Q (#K_Q − 1)`.

**G3. Every `K_Q` meets some `R_z`.** `K_Q` borders a band region labelled Q along an arc of Γℓ.
Across it the label changes (G0), and the far side lies in `K_Q`. There the label is not Q, so some
`z ∉ Q` reaches farther than Q's innermost member.

**G4. The face-centre point.** Take a face centre u of a cube `a ∈ Q`. There `ρ_a = 1` and every
other cube has `ρ > 1` (no shared plane). So a is innermost, u lies in every `R_z`, and u is not in
`X_Q`. The `K_Q` containing u meets all `n − ℓ` of the `R_z`. With G3, writing
`n_z = #{K_Q meeting R_z}`:

    Σ_{z ∉ Q} n_z  ≥  #K_Q + (n − ℓ − 1).

**G5. A `K_Q` meeting `R_z` contains an arc of `B_{Q+z}`.**
- `∂K_Q` lies in the closure of `X_Q`, where `ρ_z ≤ min_Q ρ`. So `K_Q` is not inside `R_z`.
- Being connected, `K_Q` meets `∂R_z ⊂ {ρ_z = min_Q ρ}`. There z and Q's innermost member are the two
  smallest reaches of `Q + z`, so the point is on `B_{Q+z}`.
- By G0 the point lies on an arc, by the same continuum step as in PROOF_BAND.
- So `n^Q_{Q+z} ≥ n_z`, where `n^Q_S` counts the `K_Q` meeting `B_S`. With G4:

      Σ_{z ∉ Q} (n^Q_{Q+z} − 1)  ≥  #K_Q − 1.

**G6. The one-colour rule.** Fix S with `|S| = ℓ + 1`. Let `Y_S` be the union of the `X_Q` with
`Q ⊂ S`, and let the L be the components of `S² ∖ Y_S`. By G1, `B_S` lies in their union, so `c(B_S)`
is at least the number of live L (those meeting `B_S`).
- Off `B_S`, S has a well-defined innermost cube. The sets `O_Q = {S's top-ℓ set is Q}` for
  `Q ⊂ S` are `ℓ + 1` disjoint open sets.
- A dead L lies in one `O_Q`.
- A band region r labelled Q′ that it touches lies in `O_{Q′}`, so `Q′ = Q`.
- So a dead L borders band regions of one label only.

**Lemma C** (PROOF_BAND, any number of colours). In the tree of regions and L's, with colours
`Q ⊂ S`: if every dead L has neighbours of one colour, then `#live − 1 ≥ Σ_Q (n_Q − 1)`. Here `n_Q` is
the number of pieces containing a live L once the colour-Q nodes are deleted, and `n_Q ≥ n^Q_S` as in
PROOF_BAND.
- The written proof does not use the number of colours.
- The exhaustive check was run with 3 colours (P410) and, for this level, with 4 colours; see
  Evidence.

**Assembly.** The pairs (Q, z) with `z ∉ Q` correspond one-to-one with the pairs (S, Q) with
`S = Q + z`. So

    Σ_S (c(B_S) − 1)  ≥  Σ_S Σ_{Q ⊂ S} (n^Q_S − 1)  =  Σ_Q Σ_{z ∉ Q} (n^Q_{Q+z} − 1)
                      ≥  Σ_Q (#K_Q − 1)  =  c_ℓ − 1.  ∎

**Why the top level is different.** At `ℓ = n − 1` the only subset of size `ℓ + 1` is the compound
itself, and `B_S = Γ_{n−1}`, so Lℓ says nothing. Part 3 pays for the top level another way.

**Inherited, and flagged for review:**
- PROOF_BAND's own unreviewed steps: G2's tree and G5's continuum step, both standard plane
  topology stated without citation;
- the transversality lemma ([P412]) at five cubes.

# Part 3: the top level, and the bound

[P425]'s margin identity (that entry's vertex-model explanation was CORRECTED by [P427]; the identity stands) is

    457 − total = (180 − d1) + (1 − d5) + X4 + slack2 + slack3
                  + Σ_tri (18 − d2(S)) + Σ_4 (24 − d3(S)) + cslack,

with `cslack = [Σ_tri (c_S − 1) − (c2 − 1)] + [Σ_4 (c′_S − 1) − (c3 − 1)] − (c4 − 1)`. The terms:
- `d1 ≤ 180` ([P401]) and `d5 ≤ 1`;
- `slack2 + slack3 ≥ 0` (Part 1);
- `d2(S) ≤ 18` and `d3(S) ≤ 24` (ANCHOR, [P33], unconditional, all n);
- the first two brackets of cslack are `≥ 0` by L2 and L3.

So

    457 − total  ≥  X4 − (c4 − 1)  =  d4 − 2c4,

using Euler for Γ4: `d4 = X4 + 1 + c4`.

**Two facts about the top level.** Let F = d4, the number of faces of Γ4.
1. **`d4 ≥ 5`.** Each cube is strictly innermost at its own face centres (no shared plane), so each
   cube is innermost on at least one face.
2. **`d4 ≥ c4 + 1`.** Every component of Γ4 borders at least two distinct faces, because the label
   changes across each of its arcs. In the bipartite tree of faces and components (G2), the edges
   number `F + c4 − 1 ≥ 2c4`.

**The bound.** `d4 ≤ 30` by ANCHOR (`d_{n−1} ≤ 6n`). So:

    total  ≤  457 + (2c4 − d4)  ≤  457 + (2(d4 − 1) − d4)  =  455 + d4  ≤  485,

and **total ≤ 457 whenever `d4 ≥ 2c4`**. That includes every compound with `c4 ≤ 2`, since then
`d4 ≥ 5 > 4`.

**Theorem (draft).** Five cubes, no two sharing a face plane: at most 485 bounded regions, and at most
457 when the top-level graph has at most two components (more generally when `d4 ≥ 2c4`). The record
is 393.

## Evidence for Parts 2 and 3

These are controls, not proof steps.
- **Per-level controls.** 3 420 distinct compounds, each re-measured and gated, 0 void (data:
  `data/band_n5_h2_controls.json`).
  - The L2 and L3 slacks are never negative, and both reach 0.
  - `d4 − 2c4 ≥ 18` on every row.
  - `c4` is 1 or 2 throughout; `c4 ≥ 3` has never been produced.
- **Lemma C with four colours** (`data/tree_lemma_check_c4.json`).
  - Every tree up to 13 nodes: 9 103 517 instances, 0 violations.
  - The must-fail control, with the one-colour rule dropped, fails as required (smallest at 5
    nodes).
- **Scope.** No shared face plane.


# Part 4: one shared face plane

*Draft, 2026-10-07 ([P434](LEDGER.md#p434), [P435](LEDGER.md#p435)). Not externally reviewed.*

**Scope.** Five cubes in which cubes a and b share the face plane with normal `f`, and no other
pair shares a plane.

**Result.** `total ≤ 441 + 2c4′ − d4 ≤ 469`, and `≤ 457` whenever `c4′ ≤ 10`. Here `c4′` is the
number of components of the top-level graph with its patch interiors removed.

**Notation with patches** ([PROOF_SHARED](PROOF_SHARED.md) §1).
- `O_±` is the octagon around `±f` where both cubes' `f`-faces are active. It is the only place
  where two cubes tie on an open set.
- In the gnomonic chart at `±f`, each other cube z gives `P_z`, the set where z reaches farther
  than a = b. `P_z` is convex and contains the centre.
- For each level graph and each subset's graph, `G′` is the tie set minus the interiors of its
  patches. Its count is

      d = X′ + 1 + c′ − p,

  where `X′ = E′ − V′`, `c′` is the number of components of `G′`, and `p` the number of patches.
  This is Euler for a plane graph; faces need not be disks.

## 4.1 Patches

Let `E_k` be the part of `int O` where exactly k of the three other cubes reach farther. Then
level ℓ's patches are the components of `E_{ℓ−1}`.
- **Subsets.** For the triple {a, b, z} at level 2 the patch set is `O ∩ P_z`. For the 4-subset
  {a, b, z, w} at level 3 it is `O ∩ P_z ∩ P_w`. Both are convex, with one component at `+f` and
  one at `−f`. Subsets not containing both a and b have no patches. So `Σ_S p_S = 6 + 6 = 12`.
- **Top level.** `E_3 = O ∩ P_c ∩ P_d ∩ P_e` is convex, so `p4 = 2`.
- **Levels 2 and 3: `j_Q ≤ 2`.**
  - Let `U_k` be the set where at least k of the `P` contain the point. It is a union of convex
    sets containing the centre, so it is star-shaped about the centre, and so is `O ∩ U_k`.
  - `E_k = (O ∩ U_k) ∖ U_{k+1}`. On each ray from the centre this is a half-open interval, from
    the boundary of `U_{k+1}` to the boundary of `O ∩ U_k`.
  - Every point of the complement of a component Q is therefore joined, along its ray, either to
    `U_{k+1}` (connected) or to the outside of `O ∩ U_k` (connected).
  - So `S² ∖ Q` has at most 2 components.

## 4.2 H1 at a shared point

**Claim (H1′).** `Σ_tri X′_S(2) + Σ_4 X′_S(3) ≥ X′2 + X′3 + 2X′4`.

Only points P where a and b own a common point are new: both are in T and both have the face f
active (P on the closure of O). Elsewhere no two tying cubes share a point, even when a and b
are both in T, and Part 1 applies verbatim. Near a new P, a and b own a common point s in the circle
model ([P418]). P's weight in a graph is:
- 0 if the graph's tie set is the whole circle (P is interior to a patch);
- otherwise `deg/2 − 1` if the graph ties at P, where `deg` counts the **ends** of its tie set:
  directions in it that do not have it on both sides. An isolated ray and a sector end count
  alike.

**Three cases.**
- (i) a and b own only s;
- (ii) exactly one of them owns more;
- (iii) both do.

Two cubes have the same distance function only if they own the same points. So whole-circle
graphs occur only in case (i).

**Step 1′.** If a graph does not tie at P, its ranks are strictly separated at P, and hence near
P. So it has no ends. Write `e_g(θ)` for the end indicator. Then

    2·slack(P)  =  Σ_θ Δ′(θ) − 2K*,       Δ′(θ) = Σ_g m_g e_g(θ),

where `m_g` is +1 for subset graphs and −1, −1, −2 for the full levels 2, 3, 4. `K*` is the
weighted number of graphs that tie at P and are not whole.
- In (ii) and (iii), `K* = K(t, c)` of Part 1.
- In (i), a graph (S, ℓ) is whole exactly when `S ∩ T = {a, b}` and `ℓ − |S ∩ C| = 1`. Every other
  cube of T is above a = b somewhere (at s) and below it somewhere (at its own point). So
  `K* = K_i(t, c)` is also determined by (t, c).

**Step 2′ (Check 1′).** At a direction θ, the local picture is a triple (L, W, R):
- W is T's weak order at θ;
- L and R are refinements of W, by continuity;
- on the open sides only a and b may tie, since every other tie is an isolated crossing
  ([PROOF_SHARED](PROOF_SHARED.md) §3).

For every such triple,

    Δ′(θ)  ≥  Σ_r e_{T,r}(θ) · Δpair(c + r − 1),

with `e_{T,r}` the end indicator of T's own level-r tie set. Checked exhaustively: every t ≤ 5,
c ≤ 5 − t, about 41 600 triples, 0 failures.
- An injected defect (Δpair shifted by one rank) makes it fail on 118 triples.
- It also holds when ANY pair may tie on a side. So the one-pair hypothesis is not used here; it
  enters through the ray lemmas and K*.

Summing over θ, `Σ_θ Δ′ ≥ Σ_r e(T, r) Δpair(c + r − 1)`, where `e(T, r)` counts ends.

**Step 3′: ray lemmas** (t ≥ 3; at t = 2 case (i) has every graph whole or off, so slack 0, and
cases (ii)/(iii) are Part 1's t = 2 rows).

- **R1: `e(T, r) ≥ 2`.**
  - *A_r is not empty.* For r = t − 1: at s, a and b tie as the two innermost. For r ≤ t − 2,
    suppose A_r were empty. Then the top-r set would be constant. At s, a and b are innermost,
    so the set lies in T ∖ {a, b}; take z in it. At z's own point, z has distance 0 and every
    other cube a positive one, since z shares no point. So z is innermost there and not in the
    top r, a contradiction.
  - *A_r is not the whole circle.* T's own levels are never whole when t ≥ 3.
  - So A_r has a component. A sector gives 2 ends. If A_r were a single isolated ray, the top-r
    label would be the same on both sides. But every isolated tie is a crossing, so the label
    changes there, and a cyclic label cannot change exactly once.
    - For a pair other than {a, b}, a non-crossing tie would need a shared point
      ([PROOF_SHARED](PROOF_SHARED.md) §3).
    - For a and b, it would need a minimum of `d_a` at the tie, so `d_a = d_b = 0`. The tie is
      then at s, where a and b tie on a sector.
- **The bottom level.** The two innermost cubes tie exactly where the nearest points of two
  different colours are equidistant. Give s the colour "ab".
  - The Voronoi cell of s is a sector of `A_{t−1}` (a = b innermost) with 2 ends. At its
    boundary with a neighbour p, only s and p are equidistant: on a circle, two points are at
    a given distance from a direction.
  - Every other boundary between consecutive points of different colours is an isolated ray.
  - Cut the cyclic sequence at s. With k distinct colours among the remaining points, there are
    at least k − 1 changes, so `e(T, t−1) ≥ k + 1`.
  - **R2** (ii): k = t − 1, so `e(T, t−1) ≥ t`. (iii): k = t, so `e(T, t−1) ≥ t + 1`.
    **R2_i** (i): k = t − 2, so `e(T, t−1) ≥ t − 1`.
- **R3″ (case (ii)): if `e(T, t−1) = t` then `e(T, t−2) ≥ 3`.**
  - Say a owns more than s and b owns only s. Equality means each colour other than "ab" forms
    one block in the cut sequence. Since t ≥ 3 there are at least 2 blocks, so some neighbour p
    of s has a colour x ∉ {a, b}.
  - Just past the s|p boundary, x is innermost and a = b are 2nd and 3rd innermost: a sector of
    `A_{t−2}` starts there. Just before it, inside s's cell, the two innermost are {a, b}, with
    x strictly above.
  - Follow the sector away from s. It lies where s is a's nearest point, a half-circle about s,
    so `d_s` increases with slope 1 and the innermost cube cannot rise through a = b. The
    sector therefore ends where a moves to another point, or where some cube w drops below
    a = b.
  - Either way, the two innermost after it are not {a, b}: they include a and the innermost
    cube, or w.
  - So the bottom-two label changes across this component. A cyclic label cannot change exactly
    once, so `A_{t−2}` has another component: at least 2 + 1 ends.
- **R3_i (case (i), t ≥ 4): `e(T, t−2) ≥ 4`.**
  - Let N(θ) be the number of other cubes of T nearer than s. N = 0 exactly on s's cell.
  - a = b sit at T-ranks `t − N − 1` and `t − N`, so the components of {N = 1} are sectors of
    `A_{t−2}`.
  - N = 1 just past both ends of s's cell, since only the neighbour is equidistant at a
    boundary.
  - With t ≥ 4 there are at least 2 other colours, so the cut sequence has a colour change.
    There both cubes are nearer than s (they are nearest overall), so N ≥ 2.
  - The region N = 1 therefore has at least 2 components: 4 ends.

**Step 4′.** Minimise `Σ_r Δpair(c + r − 1) e(T, r)` under these lemmas:

| t | c | (ii)/(iii) min | 2K | (i) min | 2K_i |
|---|---|---|---|---|---|
| 3 | 0 | 0 | 0 | 0 | 0 |
| 3 | 1 | 6 | 6 | 4 | 4 |
| 3 | 2 | 18 | 18 | 12 | 12 |
| 4 | 0 | 8 | 6 | 6 | 6 |
| 4 | 1 | 22 | 22 | 20 | 20 |
| 5 | 0 | 26 | 22 | 24 | 22 |

Every minimum is ≥ the corresponding 2K. So H1′ holds at every point. ∎

## 4.3 The component lemmas with patches

**Claim (L2′, L3′).** `c′_ℓ − p_ℓ − 1 ≤ Σ_{|S| = ℓ+1} (c′_S − 1)` for ℓ = 2, 3.

Part 2's argument, with [PROOF_SHARED](PROOF_SHARED.md) §3's changes:
- **G2.** The tree of faces and components now includes the patches as faces:
  `c′_ℓ − 1 = Σ_R (j_R − 1) + Σ_Q (j_Q − 1)`, and `j_Q ≤ 2` (4.1) gives
  `c′_ℓ − p_ℓ − 1 ≤ Σ_R (j_R − 1) = Σ_Q-labels (#K − 1)`. Grouping band regions by label is
  topology and unaffected by the patches.
- **G0** becomes: every 1D tie is a crossing (PROOF_SHARED §3; the argument is about pairs).
- **G3 gains a patch case.** A patch at level ℓ has a = b at ranks ℓ, ℓ+1, below a set U of ℓ − 1
  other cubes.
  - By 4.1, every patch component reaches both `∂U_ℓ` and `∂(O ∩ U_{ℓ−1})`.
  - Across the first, the label is U + z with z ∉ U. Across the second it is U + a, U + b or
    U − z + {a, b}.
  - These differ, so the regions next to a patch carry at least two labels. One of them is not
    the band label Q, and lies in the same `K_Q` as the patch.
  - G3's conclusion follows as before: a region whose label is not Q contains a cube outside Q
    that reaches farther than Q's innermost member.
- **G4.** Use a face centre other than `±f`: each cube keeps at least 4 at which it is strictly
  innermost.
- **G5.** A meeting point inside a patch of `B_{Q+z}` still lies in `B_{Q+z}`. Removing a patch
  interior does not disconnect, so `c(B_S) ≤ c′_S`.
- **G1, G6 and Lemma C** are unchanged.

## 4.4 Assembly

Write each level and subset count with Euler (4.0) and apply H1′, L2′ and L3′:

    d2 + d3 + 2·d4  ≤  Σ_tri d2(S) + Σ_4 d3(S) − 24 + (Σ_S p_S − 2p4) + 2c4′.

The patch term is `12 − 4 = 8`. The inputs:
- `d1 ≤ 180` ([P401], unconditional) and `d5 ≤ 1`;
- `d2(S) ≤ 14` and `d3(S) ≤ 20` for subsets containing the pair, and 18 and 24 otherwise ([P413]'s
  ANCHOR argument: `±f` anchor nothing for a or b).

So

    total  ≤  181 + (7·18 + 3·14) + (2·24 + 3·20) − 24 + 8 + 2c4′ − d4  =  441 + 2c4′ − d4.

**The top level.**
- `d4 ≥ 5`, since each cube is strictly innermost at some face centre.
- Every component of `G′4` borders at least two faces, counting patches as faces: 1D ties cross.
  The face/component tree gives `c4′ ≤ d4 + p4 − 1 = d4 + 1`.
- So `total ≤ 443 + d4 ≤ 469`, using `d4 ≤ 26` (ANCHOR), and `total ≤ 457` whenever
  `2c4′ − d4 ≤ 16`, in particular whenever `c4′ ≤ 10`.

**Theorem (draft).** Five cubes with exactly one pair sharing a face plane: at most 469 bounded
regions, and at most 457 when the top-level graph has at most 10 components. Together with
Part 3, **every five-cube compound with at most one sharing pair has at most 485.** Two or more
sharing pairs are not yet covered. For all five-cube compounds the bound remains 871.

## Evidence for Part 4

These are controls, not proof steps. Probes: `src/probes/h1_shared_proof.py` and
`src/probes/h1_shared_local.py`; data: `data/h1_shared_proof.json` and
`data/h1_shared_local*.json`.
- **H1′ per vertex, measured directly** on 175 702 exact circle configurations with a shared
  point: 0 negative slacks.
- **The weight code**, checked two ways:
  - without a shared point, it agrees with Part 1's implementation on 47 804 configurations;
  - with one, it agrees graph by graph with PROOF_SHARED's independent code at n = 4 on 16 625
    graphs, including 540 whole-circle ones.
- **The ray lemmas** (R1, R2, R2_i, R3″, R3_i), measured on 63 975 random configurations with
  t ≥ 3: 0 violations.
- **Step 1′'s identity**, with K* from the whole-graph rule, holds exactly on 58 735 configurations.
  Every observed (L, W, R) triple is inside Check 1′'s enumeration.
- **The budget's subset counts.** 48 recounted frame-free, all equal.
- **The chain's shape.** Measured on 600 shared-plane compounds ([P433]), with room: slack ≥ 10
  and ≥ 2.
- **Not checked** term by term on real compounds: the engine's level graphs are invalid with
  shared planes ([P246]).
