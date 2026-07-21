# Step T, closed — degenerate triple points, rigorously

This completes the one gap in `PROOF_FORMAL.md`: the bound on the
triple-point weight in full generality, including degenerate triple points
where the earlier "deg_top ≤ deg_bot" route fails (that route is false;
see `PROOF_NARRATIVE.md` / ledger Postscript 42). The argument here is
elementary — two one-line lemmas and a three-case split — and needs **no
new hypothesis** beyond the pairwise transversality already used by the
contact analysis (Part D). Verified on 50 000 random configurations, 0
violations (`stepT_proof_verify.py`).

## Setup (local model, from PROOF_FORMAL Parts B, D)

Fix a top-diagram vertex at direction û₀, physical point x₀ = ρû₀, with
tied-farthest set S. In the tangent plane T_{û₀}S² ≅ ℝ², the top and
bottom diagrams near û₀ are governed by the leading homogeneous parts of
the reach functions: convex, positively-homogeneous, piecewise-linear
functions m_i(v) = h_{P_i}(v), the **support functions** of the polygons

    P_i = conv{ tangential gradients of the facets of K_i active at x₀ },

with a_i := #vertices of P_i = #active facets of K_i at x₀. On the unit
circle of tangent directions,

  • **top diagram** = argmin_i m_i (farthest cell), deg_top = #index-switches;
  • **bottom diagram** = argmax_i m_i (nearest cell), deg_bot = #index-switches.

For a tied pair {i,j}, x₀ is a vertex of the pairwise polytope
P_{ij} := K_i ∩ K_j; when the two cells meet transversally at x₀ (Part D2,
the pointed-cone argument — the same regularity the contact bound already
assumes), its degree there is d_{ij} := deg_{P_{ij}}(x₀) = a_i + a_j.

We prove, at **every** top-diagram vertex (|S| = 2 contact or |S| = 3
triple point), the local inequality

    (◆)   deg_top − 2 ≤ (deg_bot − 2)⁺ + Σ_{tied pairs {i,j}} (d_{ij} − 2).

For a triple point Σ_{pairs}(d_{ij}−2) = Σ(a_i+a_j−2) = 2σ − 6, where
σ := a + b + c is the total active-facet count; so (◆) reads

    deg_top − 2 ≤ (deg_bot − 2)⁺ + (2σ − 6).

(For a contact, (◆) is the Part D equality deg_top = a+b = d_{ij}, with
(deg_bot−2)⁺ = 0 since a contact is not a bottom-diagram vertex.)

## Two lemmas

Write z_{ij} for the number of sign changes of m_i − m_j around the circle,
and N := z_{ij} + z_{ik} + z_{jk}.

**Lemma A (crossing classification).**  deg_top = N − deg_bot.

*Proof.* Generically the pairwise crossings are simple and no three
m's coincide off û₀ (a three-way tie off û₀ would be another, isolated,
triple point, treated at its own vertex). At a crossing of the pair {i,j}
we have m_i = m_j =: v and m_k ≠ v. If m_k > v then i, j are the two
smallest, so the **argmin** (top) switches there and the argmax does not;
if m_k < v then i, j are the two largest, so the **argmax** (bottom)
switches and the argmin does not. Thus every crossing is exactly one of the
two kinds, and summing, deg_top + deg_bot = N. ∎

**Lemma B (alternation bound).**  z_{ij} ≤ 2·min(a_i, a_j).

*Proof.* z_{ij} = 2·(number of maximal arcs of the circle on which
m_i > m_j). On such an arc the support point of conv(P_i ∪ P_j) lies on
P_i (P_i strictly outreaches P_j in those directions); distinct arcs are
separated by P_j-arcs, so distinct m_i>m_j arcs use distinct vertices of
P_i. Hence their number is ≤ a_i, and symmetrically ≤ a_j. ∎

**Corollary.** N ≤ 2μ ≤ 2σ, where μ := min(a_i,a_j)+min(a_i,a_k)+min(a_j,a_k)
≤ a+b+c = σ.

Finally note deg_bot is a switch count on a circle, so deg_bot ∈ {0,2,3,4,…}
— a single switch cannot close up, so **deg_bot ≠ 1**.

## The triple-point inequality (◆), by cases on deg_bot

**Case 1: deg_bot ≥ 3.**  By Lemma A and the Corollary,
deg_top = N − deg_bot ≤ 2σ − deg_bot. Since deg_bot ≥ 3, i.e. 2·deg_bot ≥ 6,

    2σ − deg_bot ≤ deg_bot + 2σ − 6,   so   deg_top − 2 ≤ (deg_bot − 2) + (2σ − 6). ✓

(No use of deg_top ≤ deg_bot — the pairwise budget 2σ−6 absorbs the excess.
This already covers the realized counterexample a=3,b=c=2: deg_top=8,
deg_bot=4, σ=7, and 8 ≤ 4 + 8.)

**Case 2: deg_bot = 0.**  The argmax is a single constant cell k (uniquely
nearest in every direction). Then k is never farthest, so the top diagram
involves only i, j and deg_top = z_{ij}. By Lemma B and
min(a_i,a_j) ≤ a_i + a_j − 1 = σ − a_k − 1 ≤ σ − 2,

    deg_top = z_{ij} ≤ 2·min(a_i,a_j) ≤ 2σ − 4,   so   deg_top − 2 ≤ 2σ − 6. ✓

**Case 3: deg_bot = 2.**  Exactly two cells — say i, j — ever attain the
argmax; the third cell k is never nearest, i.e. m_k(θ) < max(m_i,m_j)(θ)
for all θ. Hence at every (i,j)-crossing (m_i = m_j =: v) we must have
v ≥ m_k (otherwise m_k > v would make k nearest there); every
(i,j)-crossing is therefore an argmax switch, so **z_{ij} = deg_bot = 2.**
Consequently, by Lemma A and Lemma B,

    deg_top = N − 2 = z_{ik} + z_{jk} ≤ 2·min(a_i,a_k) + 2·min(a_j,a_k).

Now min(a_i,a_k) + min(a_j,a_k) ≤ a_i + a_j = σ − a_k. If a_k ≥ 2 this gives
deg_top ≤ 2(σ − a_k) ≤ 2σ − 4. If a_k = 1 then deg_top ≤ 2·1 + 2·1 = 4, and
since the vertex is a genuine degenerate triple (not the all-ones generic
point, which has deg_bot = 3), a_i + a_j ≥ 3, whence
2σ − 4 = 2(a_i+a_j) − 2 ≥ 4 ≥ deg_top. Either way deg_top − 2 ≤ 2σ − 6. ✓

deg_bot ∈ {0,2,3,4,…} exhausts all cases, so (◆) holds at every triple point. ∎

## Global assembly (⟹ d₁ ≤ 48 ⟹ max(3) = 67)

Sum (◆) over all top-diagram vertices v. With W := Σ_v (deg_top(v) − 2),

    W ≤ Σ_{triple v} (deg_bot(v) − 2)⁺  +  Σ_v Σ_{tied pairs} (d_{ij}(v) − 2).

*First sum (bottom-diagram budget).* Only triple points with deg_bot ≥ 3
contribute, and those are genuine vertices of the bottom diagram, so this
is ≤ Σ_{bottom vertices}(deg_bot − 2) = 2(F_bot − 2) = 2(d₂ − 2) ≤ 2·16 = 32.

*Second sum (pairwise-polytope budget).* Distinct top vertices are distinct
directions, hence distinct points x₀, hence distinct vertices of the
pairwise polytopes, with matching degree d_{ij}. So the sum is
≤ Σ_{pairs {i,j}} Σ_{vertices of P_{ij}} (deg − 2) = Σ_{pairs}(2F_{ij} − 4).
Each P_{ij} = K_i ∩ K_j has ≤ 12 facets (≤ 6 + 6), so 2F_{ij} − 4 ≤ 20, and
the three pairs give ≤ 60.

Therefore W ≤ 32 + 60 = 92, so d₁ = 2 + ½W ≤ 48, and

    R = d₁ + d₂ + d₃ ≤ 48 + 18 + 1 = 67,

attained (two-engine certified) by the octahedral and golden compounds. ∎

## Status

This closes Step T for all three concentric convex ≤6-facet cells whose
boundaries meet **pairwise transversally** at their coincidence points —
the same regularity the contact bound (Part D) already requires, satisfied
on an open dense set of configurations and at both maximizers. No
assumption is placed on the triple points themselves: arbitrary degenerate
triple points (any a_i, any deg_top) are handled. The one earlier caveat
that remains is the pre-existing pairwise-tangency degeneracy of Part D
(two cells sharing a boundary tangentially), which is not a triple-point
phenomenon and is milder (higher codimension).

**Verification.** `stepT_proof_verify.py` checks Lemma B, the inequality
(◆), and the two structural facts used in Cases 2–3
(deg_bot = 0 ⟹ deg_top = z of the other pair; deg_bot = 2 ⟹ the two nearest
cells cross exactly twice) on 50 000 random triple-point models: 0
violations. The falsity of the superseded "deg_top ≤ deg_bot" route and
the realized 3-D counterexample are in `stepT_local.py`, `stepT_realize.py`,
`stepT_degcheck.py`.
