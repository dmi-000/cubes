# The band lemma: a depth-2 band is paid for by the triples

*Draft, 2026-10-04 ([P410](LEDGER.md#p410)). Not yet externally reviewed.*

**Claim.** At n = 4, consider compounds with no two cubes sharing a face plane (see the
scope). For these,

    c2 − 1  ≤  Σ_S (c_S − 1),

where:
- `c2` is the number of components of the level-2 boundary Γ of the compound;
- `c_S` is the number of components of the bottom diagram `B_S` of the triple `S`;
- the sum runs over the four triples.

With [P404](LEDGER.md#p404)'s charging (`X = 0`, `W4u = 0` by [P405](LEDGER.md#p405)), this gives

    d2  ≤  1 + c2 + Σ_S (E_S − V_S)  =  Σ_S d2(S) − Σ_S c_S + c2 − 3  ≤  Σ_S d2(S) − 6  ≤  72 − 6  =  66,

using `E_S − V_S = d2(S) − 1 − c_S` (Euler) and ANCHOR's `d2(S) ≤ 18`. Then, with the proved
`d1 ≤ 104` and `d3 ≤ 24` ([P401](LEDGER.md#p401)) and `d4 ≤ 1`:
`max(4) = d1 + d2 + d3 + d4 ≤ 104 + 66 + 24 + 1 = 195`.
The margin of [P408] splits as

    margin = Σ_S (18 − d2(S))  +  [ Σ_S (c_S − 1) − (c2 − 1) ]
             ANCHOR slack, ≥ 0      component slack, ≥ 0 by this lemma

## Notation

- **Reach.** Reach `ρ_x(u) = 1/M_x(u)` is how far cube `x` extends in direction `u`. The face
  centres of `x` are the six directions where `ρ_x = 1`, its minimum.
- **Labels.** Away from Γ, the compound's two largest reaches are strictly larger than the other
  two. That pair is the **label** of the point; the label is locally constant off Γ.
  - Within a triple `S`, `B_S` is the set where the second and third largest reach tie.
  - Off `B_S`, the triple has a **triple label**: the pair `Q ⊂ S` reaching farther than `S∖Q`.
- **Regions.** A **region** is a component of `S² ∖ Γ`. `j_R` is the number of components of
  `S² ∖ R`. A region is a **band region** if `j_R ≥ 2`.
- **Band regions of a pair.** For a pair `P`, `X_P` is the union of the band regions labelled `P`.
  The `K_P` are the components of `S² ∖ X_P`.

## Scope (G0)

- **No shared face plane.** This is [P404]'s scope, and the only condition.
- **Every tie is then a crossing** (the transversality lemma, [P412](LEDGER.md#p412)). Wherever
  cubes reach equally far, the reach difference changes sign across the tie. Two consequences are
  used:
  - The label changes across every arc of Γ (G3).
  - As closed sets, Γ and each `B_S` are exactly the union of the arcs of their level graphs
    (`level_s1`), with no isolated points (G5, G6).
- **Why the lemma holds.**
  - A tie that does not cross means one cube's tangent cone contains the other's.
  - For congruent origin-centred cubes, every such containment forces a shared face plane. For
    example, an edge lying in a face plane `f` gives `f = αn1 + βn2` with `α + β = 1` and
    `α² + β² = 1`, so `f = n1` or `n2`.
  - Ties of three or more cubes cross by the circle lemma.
  - *(CORRECTED 2026-10-04, same day: a first draft listed "transversal ties" as a second
    assumption.)*

## The geometric inputs (G)

**G1. Each region has one label.** A region is connected and avoids Γ, so its label is constant.
- On a band region `R` labelled `P = {a, b}`, every triple `S ⊃ P` has triple label `P`, with
  `S ∖ P` strictly third.
- Hence `B_S ∩ X_P = ∅` for every `S ⊃ P`.

**G2. The region tree.** Take a finite graph on S² with `c` components. Then
`c − 1 = Σ_R (j_R − 1)` over the components `R` of its complement.

The same holds for any family of pairwise disjoint open connected sets `R` in S² (here, the band
regions inside a union `Y`) and the components `L` of `S² ∖ Y`.
- The bipartite adjacency graph between the sets `R` and the components `L` is a tree.
- Each `R` is adjacent to exactly `j_R` of the `L`s. This uses the fact that each complementary
  component of a connected open set in S² has connected boundary: S² is unicoherent.
- Applied to Γ: `c2 − 1 = Σ_P G_P`, where `G_P = Σ_{R ⊂ X_P} (j_R − 1) = #K_P − 1`.

**G3. Every `K_P` meets `R_c ∪ R_d`.** Let `P = {a, b}`, with `c` and `d` the other two cubes. Write
`R_z = {ρ_z > min(ρ_a, ρ_b)}`, an open set disjoint from `X_P`.
- `K_P` is adjacent to some band region `R` along an arc of Γ.
- By G0 the label changes across that arc. The region on the far side is not in `X_P`, so it
  lies in `K_P`.
- There the label is not `P`, so `c` or `d` beats `min(ρ_a, ρ_b)`.

**G4. The face-centre point.** Take a face centre `u` of `a`. There `ρ_a = 1`, and every other cube
has `ρ > 1`; otherwise the two cubes would share a face plane.
- So `a` is innermost at `u`, and `u ∈ R_c ∩ R_d`.
- `u ∉ X_P`, because on `X_P` the cube `a` is in the label.
- So the `K_P` containing `u` meets both `R_c` and `R_d`.
- With G3: `n_c + n_d ≥ #K_P + 1`, where `n_z = #{K_P meeting R_z}`.

**G5. Each `K_P` that meets `R_z` contains an arc of `B_{P∪z}`.**
- The boundary `∂K_P` lies in the closure of `X_P`, where `ρ_z ≤ min(ρ_a, ρ_b)`. So `K_P` is not
  contained in `R_z`.
- `K_P` is connected and meets both the open set `R_z` and its complement, so it meets `∂R_z`.
- `∂R_z` lies in `{ρ_z = min(ρ_a, ρ_b)}`, and that set lies in `B_{P∪z}`.
- With G0 the meeting point lies on a graph arc. (A component of `R_z ∩ K_P` has a boundary
  continuum with more than one point: on S², no open set other than `S² ∖ {pt}` has a one-point
  boundary.)
- Let `n^P_S` be the number of `K_P` meeting `B_S`. Then `n^P_{P∪z} ≥ n_z`.

**G6. The one-colour rule.** Fix a triple `S`. Let `Y_S = ∪_{P ⊂ S} X_P`, and let the `L` be the
components of `S² ∖ Y_S`.
- By G1, `B_S ⊂ S² ∖ Y_S`, so `c_S ≥ #{L meeting B_S}`. Call such an `L` **live**, and the
  others **dead**.
- **A dead `L` is adjacent only to band regions of a single pair.**
  1. A dead `L` misses `B_S`, so it lies in the union of the three disjoint open sets
     `O_Q = {triple label Q}`.
  2. Being connected, it lies in one of them, `O_Q`.
  3. If `L` touches a band region `r` labelled `P`, at a point `x` in `∂r ∩ L`, then `x ∈ O_Q`, an
     open set. So `O_Q` contains points of `r`, and `r ⊂ O_P`. Hence `Q = P`.

## The count (C), finite combinatorics

Fix `S`. Let 𝒯 be the tree of G2 for `Y_S`:
- region nodes are coloured by their pair `P ⊂ S`;
- `L` nodes are live or dead, and at least one is live (`c_S ≥ 1`).

Let `n_P` be the number of components of 𝒯 minus its colour-`P` nodes that contain a live `L`.

**Lemma C.** If every dead `L` has neighbours of only one colour, then
`#live − 1 ≥ Σ_P (n_P − 1)`.

*Proof.*
1. Let 𝒯′ be the subtree spanning the live nodes. Its leaves are live, and region nodes have
   degree at least 2 in it.
2. In a bipartite tree, `#L(𝒯′) − 1 = Σ_r (δ_r − 1)`, the sum over the region nodes `r` of 𝒯′,
   where `δ_r` is the degree of `r` in 𝒯′.
3. Deleting the colour-`P` nodes of 𝒯′ leaves `1 + Σ_{r of colour P} (δ_r − 1)` pieces.
4. Each dead node of 𝒯′ with neighbours of colour `P` becomes a piece with no live node. So
   `n_P − 1 ≤ Σ_{r of colour P} (δ_r − 1) − #dead_P`.
5. Summing over `P`: `Σ_P (n_P − 1) ≤ Σ_r (δ_r − 1) − #dead = #live − 1`. ∎

Lemma C is checked by exhaustive enumeration in `src/probes/tree_lemma_check.py`. That check
includes a must-fail control with the one-colour rule dropped.

**Linking `n_P` to `n^P_S`.**
- A `K_P` with `P ⊂ S` is a union of `L`s and of band regions of the other colours. Different
  `K_P`s give different pieces after the colour-`P` nodes are deleted.
- A `K_P` meeting `B_S` contains a live `L`.
- So `n_P ≥ n^P_S`.

## Assembly

    Σ_S (c_S − 1)  ≥  Σ_S Σ_{P ⊂ S} (n^P_S − 1)                      (G6, Lemma C)
                   =  Σ_P [ (n^P_{P∪c} − 1) + (n^P_{P∪d} − 1) ]      (each pair lies in two triples)
                   ≥  Σ_P (n_c + n_d − 2)                            (G5)
                   ≥  Σ_P (#K_P − 1)                                 (G3, G4)
                   =  c2 − 1                                         (G2)

A pair `P` without a band region has `#K_P = 1`, so its terms are `≥ 0`. Since `n_c, n_d ≤ #K_P`
and `n_c + n_d ≥ #K_P + 1`, both are at least 1.

## Evidence and open items

- **Data.** All 8 known bands have `c2 = 2` and component slack exactly 1 (`data/band_components.json`).
  In each, the two disconnected triples share a pair, as G4 predicts for one band pair.
- **Uncovered case.** Two band pairs sharing a cube is covered by the argument, but no instance has
  been observed. `c2 ≥ 3` has not been observed either.
- **Open item 1.** The shared-face-plane case (plan item 2). A perturbation argument cannot
  settle it: [P69], [P411].
- **Open item 2.** G2's tree and G5's continuum step are standard plane topology, but they are
  stated here without a citation. External review is wanted for those, for G6, and for the
  transversality lemma ([P412]) behind G0.
- **Inherited.** ANCHOR (`d2(S) ≤ 18`, its soft step flagged in PROOF_67), LOCAL COINCIDENCE
  ([P404]) and the circle lemma ([P405]).
