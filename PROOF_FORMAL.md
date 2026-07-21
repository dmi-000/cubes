# max(3) = 67 — the cleanest proof path, formalized

Target for a Sonnet-class assistant to complete the few marked intermediate
steps. Self-contained. All region counts are of **face-bounded regions**
(connected components of constant cube-containment), which is what the
project's engines compute — NOT cells of the infinite-plane arrangement
(that distinction is the one hard-won correction; see PROOF_NARRATIVE.md).

**Theorem.** Let K₁, K₂, K₃ ⊂ ℝ³ be compact convex bodies, each with at
most 6 facets, each containing the origin O in its interior ("cells").
The number of bounded regions of their arrangement — components of
{x : x lies in a fixed nonempty subset of the K_i} — is at most **67**,
attained by the octahedral and golden cube compounds. In particular
max(3) = 67 for cubes.

Notation. R = total bounded regions = d₁ + d₂ + d₃, where d_m = # regions
of depth m (in exactly m cells). Reach r_i(û) = max{t≥0 : tû ∈ K_i} for
û ∈ S²; since O is interior and K_i convex, r_i is a well-defined positive
function and r_i = 1/M_i with M_i(û) = max over facets f of K_i of
(n_f·û)/h_f (facet f = {n_f·x = h_f}, h_f>0). "Cell i is active at û" for
facet f means f attains this max; the facets of K_i containing the point
r_i(û)û are exactly the active ones.

---

## Part A — the two easy layers (COMPLETE)

**A1. d₃ ≤ 1.** K₁∩K₂∩K₃ is convex, hence connected. ∎

**A2. d₂ ≤ 18 (convex-cover).** The depth-2 region "in K_i and K_j, not
K_k" equals (K_i∩K_j) ∩ K_kᶜ = ⋃_{f facet of K_k} (K_i∩K_j ∩ {n_f·x > h_f}).
Each term is convex (a convex set ∩ an open halfspace), and K_k has ≤ 6
facets, so this union has ≤ 6 components. Summing over the 3 choices of
the "outside" cell: d₂ ≤ 18. ∎ (Same argument gives d_{n−1} ≤ 6n for any
n; and it is shape-independent — works for any convex ≤6-faceted cells.)

---

## Part B — the radial / top-diagram reduction (COMPLETE, standard)

**B1. Fibration.** Depth-1 regions of cell i biject with connected
components of T_i = {û ∈ S² : r_i(û) > r_j(û) ∀ j ≠ i} (cell i uniquely
farthest). So d₁ = Σ_i #π₀(T_i) = number of faces of the **top diagram**,
the partition of S² by argmax_i r_i. [Proof: each radial fiber of a
depth-1 cell is a single interval since cells are convex and contain O;
a component of T_i sweeps one connected 3-D region; tie directions form
the measure-zero walls. Routine.]

**B2. Euler.** The top diagram is a graph on S² (vertices = directions
where ≥ 3 top-faces meet; edges = arcs of tie-curves r_i = r_j; faces =
the T_i components). With degree-2 vertices suppressed, V − E + F = 2 and
2E = Σ deg, so

    d₁ = F = 2 + ½ Σ_v (deg_v − 2)  =:  2 + ½ W,

where W = Σ_v(deg_v − 2) is the **top-diagram weight**. Thus d₁ ≤ 48 ⟺
W ≤ 92.

**B3. Vertex types.** A top-diagram vertex at direction û₀ corresponds to
the physical point x₀ = r(û₀)û₀ lying on ∂K_i for each cell i in the
"tied-farthest" set S(û₀) (|S| ≥ 2). Write a_i = # facets of K_i active
at û₀ (= # facets of K_i through x₀). Two families:
  • **triple points**: |S| = 3 (all three reaches equal at û₀);
  • **contacts**: |S| = 2 (two cells tied, the third strictly nearer in
    a neighborhood).
Split W = W_triple + W_contact accordingly (W_triple = Σ over triple
points of (deg−2); W_contact = Σ over |S|=2 vertices of (deg−2)).

---

## Part C — triple-point weight (COMPLETE for the generic/extremal case; one marked step for full generality)

**C1. W_triple ≤ 32 when all triple points are degree 3.** A degree-3
vertex is a triple point (three T-regions meet). Each triple point is
also a vertex of the **bottom diagram** (argmin_i r_i): at û₀ the three
reaches are equal, so both argmax and argmin cycle through all three
locally. The bottom diagram has F = d₂ ≤ 18 faces (B1 dual), so by B2's
Euler its vertex weight is 2(d₂−2) ≤ 32; every triple point is a
degree-≥3 bottom vertex, so #triple points ≤ 32. When each is degree 3
in the top diagram, W_triple = #triple points ≤ 32. ∎

**[INTERMEDIATE STEP T — for a Sonnet]** Show W_triple ≤ 32 even if some
triple point has top-degree > 3 (a "degenerate" triple point where
several cells are simultaneously at edges/corners). Suggested route: such
a point is a degenerate vertex of the *bottom* diagram too; show
deg_top ≤ deg_bot there (the argmin structure is at least as branched as
the argmax when all three reaches coincide), then W_triple ≤ Σ_{bottom
vertices}(deg_bot − 2) = 2(d₂−2) ≤ 32. This case is non-generic and does
NOT occur at either maximizer (their bottom diagrams are exactly generic,
32 degree-3 triple points), so it is not needed for attainment — only for
the universal statement. Verified: 0 occurrences in 130 sampled configs.

---

## Part D — contact weight (the crux; |S|=2 case COMPLETE)

Fix a contact û₀ with tied cells i, j (cell k strictly nearer nearby),
x₀ = r_i(û₀)û₀, a = a_i ≥ 1, b = a_j ≥ 1 active facets. Since cell k is
strictly nearer in a neighborhood, the top diagram near û₀ is exactly the
partition by which of r_i, r_j is larger, i.e. the swap curve
{M_i = M_j}. Near û₀, M_i = max over the a active facets ℓ_f(û)=(n_f·û)/h_f
(inactive facets are strictly smaller at û₀, hence nearby), similarly M_j.

**D1. A contact has a, b ≥ 2, so deg_top ≥ 4.** The a active facets of
cell i share the point x₀; their pairwise "sector boundaries"
{ℓ_f = ℓ_{f'}} are lines through û₀ dividing a neighborhood into a angular
sectors (a=1: no boundary, 1 sector; a=2: one line, 2 sectors; a=3: three
concurrent lines / a corner, 3 sectors). Overlaying cell i's a sectors and
cell j's b sectors and reading M_i − M_j (linear on each refined sector,
flipping sign once across each ray on which it vanishes), the number of
swap-arcs meeting û₀ is a + b **when a, b ≥ 2**, and is 2 (a smooth kink,
not a genuine vertex) if min(a,b) = 1. So genuine contact vertices have
a, b ≥ 2 and

    deg_top(û₀) = a + b   (= 4 edge–edge, 5 edge–corner, 6 corner–corner).

**D2. x₀ is a degree-(a+b) vertex of P_i∩P_j := K_i∩K_j.** Near x₀, K_i is
the intersection of the a halfspaces of its active facets (a "wedge" for
a=2, a "corner cone" for a=3), and K_j of its b active halfspaces; all
a+b bounding planes pass through x₀. So near x₀, K_i∩K_j is the polyhedral
cone C with apex x₀ cut by these a+b halfspaces. C is **pointed**: a line
ℝd ⊂ C needs n_f·d = 0 for all a+b active normals; the a normals of i span
(d_i)^⊥ and the b of j span (d_j)^⊥ where d_i, d_j are the edge/vertex
directions of i, j at x₀ — since i, j meet transversally at the isolated
point x₀ (else the tie set would be ≥1-dimensional and û₀ not a vertex),
(d_i)^⊥ ∪ (d_j)^⊥ spans ℝ³, so no such d exists. A pointed 3-cone with
a+b facets, each facet meeting exactly two others around the apex, has
exactly a+b edges. Hence deg_{P_i∩P_j}(x₀) = a + b.

**D3. Correspondence + Euler bound.** By D1–D2, deg_top(û₀) =
deg_{P_i∩P_j}(x₀) for every |S|=2 contact. Distinct contacts give distinct
directions hence distinct polytope vertices, and each contact of cells
{i,j} maps into the polytope P_i∩P_j. Therefore

    W_contact^{(|S|=2)} = Σ_{contacts}(deg_top − 2)
        = Σ_{contacts}(deg_{P_i∩P_j} − 2)
        ≤ Σ_{pairs {i,j}} Σ_{v vertex of P_i∩P_j}(deg_v − 2).

For any convex 3-polytope, Σ_v(deg_v − 2) = 2E − 2V = 2(V+F−2) − 2V =
**2F − 4**. Each K_i has ≤ 6 facets and every facet of P_i∩P_j lies on a
facet of K_i or K_j, so F(P_i∩P_j) ≤ 12 and 2F − 4 ≤ 20. Over the 3 pairs:

    W_contact^{(|S|=2)} ≤ 3 · 20 = **60.** ∎

**[INTERMEDIATE STEP S3 — for a Sonnet]** Bound the contribution of
|S|=3 *contacts* (degenerate triple points counted in W with top-degree
> 3, if any are classified as contacts rather than triple points — a
bookkeeping choice: put every |S|=3 vertex into Part C). Cleanest: define
W_triple to include ALL |S|=3 vertices (any # tied = 3) and W_contact only
|S|=2; then Step T (Part C) already covers them and Part D needs no change.
Confirm this partition is exhaustive (every top vertex has |S| ∈ {2,3}
since there are 3 cells) and that D1–D3 used only |S|=2. Both hold.

---

## Part E — assembly (COMPLETE given C and D)

W = W_triple + W_contact ≤ 32 + 60 = 92, so d₁ = 2 + ½W ≤ 48. With
d₂ ≤ 18 (A2) and d₃ ≤ 1 (A1):

    R = d₁ + d₂ + d₃ ≤ 48 + 18 + 1 = 67.

Attainment: the octahedral compound (cubes at 45° about x, y, z axes) and
the golden compound both give exactly {d₁,d₂,d₃} = {48,18,1}, two-engine
certified, and saturate every inequality above (T = 32, W_contact = 60,
F(P_i∩P_j) = 12 on all pairs, all contacts |S|=2 with a=b∈{2,3}). Hence
max(3) = 67. ∎

---

## Status of the marked steps

- **Step T** (degenerate triple points, W_triple ≤ 32 in full generality):
  non-generic, absent at both maximizers, reduces to deg_top ≤ deg_bot at
  coincident triple points. The clean partition in Step S3 (all |S|=3
  vertices → Part C) makes this the only place three-cell degeneracy is
  handled. LOW risk.
- **Step S3**: a bookkeeping confirmation, essentially immediate.
- Everything else (A, B, C1, D1, D2, D3, E) is complete and rigorous.

So the theorem is proved outright for the generic stratum and for both
maximizers (where the bound is tight), and up to the single non-generic
Step T for the universal statement over all convex ≤6-faceted cells.

## Reproduction / verification
`proof67_verify.py` (region counter, triple-point count, F(P_i∩P_j)) and
`proof67_pairpoly.py` (pairwise-polytope degree spectra) reproduce: the
inequality W_contact ≤ Σ_pairs(2F−4) on 130 configs (0 failures, tight at
both maximizers); the degree spectra {30·deg4} (octahedral) and
{18·deg4, 6·deg6} (golden) matching top-diagram and pairwise-polytope
counts; and 30 edge-edge crossings = 30 deg-4 contacts.
