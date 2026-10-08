# Proof check: what a machine has verified, and what still needs a reader

*Current as of 2026-10-04 ([P410](LEDGER.md#p410)); first pass 2026-09-28 ([P398](LEDGER.md#p398)). Regenerate the checks with
`python3 src/lean_status.py`; everything below that says "Lean" is re-proved on every run.*

A proof checker cannot see the cubes. Every proof here has two layers: **geometric lemmas**
(convexity, the radial picture, topology on the sphere) and a **counting assembly** that turns them
into a bound. Lean (4.34, core, in `lean/`) checks the assembly, with each lemma entering as a named
hypothesis, and checks that every non-proved hypothesis is actually needed. The lemmas themselves
are checked by nothing but reading. **This page is the list of what to read.**

## The results, as checked

| result | assembly | label from Lean | notes |
|---|---|---|---|
| max(2) = 13 | `max2_le_13` | PROVED | ANCHOR + FIB + a convex core |
| max(3) ≤ 67, Mayer–Vietoris route | `max3_le_67_MV` | PROVED | no transversality and no connectivity assumed ([P110](LEDGER.md#p110)) |
| max(3) ≤ 67, Euler route | `max3_le_67_Euler` | PROVED IF the top diagram is connected | found by this check ([P398](LEDGER.md#p398)) |
| triple points ≤ 32 (Lemma 1a) | `lemma1a_triple_le_32` | PROVED | Euler with `c` components: disconnection only helps |
| top weight `W ≤ 92` | `weight_le_92` | PROVED, scope: pairwise transversal | Step T and Part D |
| pair gain ≤ 10 | `pair_gain_le_10` | PROVED | uses `c ≥ 1` in the safe direction |
| `d₁ ≤ 108·C(n,3) + 10·C(n,2) + c₁ + 1` | `d1_bound_with_c` | PROVED | [P237] |
| the same with `+ 2` | `d1_bound` | PROVED IF `c₁ = 1` | found by this check ([P398](LEDGER.md#p398)) |
| Theorem S at n = 4 | `per_cube_n4`, `theoremS_n4` | PROVED | Lemmas 2 and 3 are pure combinatorics |
| one-cube increment | `increment` | PROVED | [P56] |
| `h(S) ≤ 47.5`, `TOTAL ≤ 195 − Q4` | `h_le`, `total_le_195…` | PROVED IF trivial holes | [P348], [P395] |
| tower bound (198 at n = 4) | `tower` | PROVED IF holes ≤ 1 | scope: no shared face plane; the accounting step proved by [P407](LEDGER.md#p407) ([P326], [P396]) |
| **`max(4) ≤ 261`**, and `d₁ ≤ 10n² − 14n` | `max4_le_261`, `depth1_ceiling` | PROVED | tightening of 285 (`max4_le_285`), [P401](LEDGER.md#p401) |
| `max(4) ≤ 285` | `max4_le_285` | PROVED | no hypothesis; anchored by an independent exact counter equal to the engine on 17 configurations ([P399](LEDGER.md#p399)) |
| **`max(4) ≤ 195`** | `max4_le_195` | DRAFT (PROVED until 2026-10-08; the band lemma's Lean binder is now `draft_`) | scope: no shared face plane (ties are then all crossings, [P412](LEDGER.md#p412)); the band lemma `c₂ − 1 ≤ Σ_S (c_S − 1)` ([P410](LEDGER.md#p410), [PROOF_BAND](PROOF_BAND.md)) replaces `c₂ = 1`; not yet externally reviewed |
| `max(4) ≤ 194 + c₂`, so 195 | `max4_le_195_charging` | PROVED IF `c₂ = 1` (and `c₂ = 2` occurs, [P408](LEDGER.md#p408)) | superseded 2026-10-04 by `max4_le_195`; scope: no shared face plane; `X = 0`, `W4u = 0` by the circle lemma ([P404](LEDGER.md#p404), [P405](LEDGER.md#p405)) |
| general-n bound, exact at n = 2, 3 | `per_set_closed_form` | PROVED | the induction on `|B|`; anchored at n = 5 ([P400](LEDGER.md#p400)) |
| `max(4) ≤ 953` | `total_le_953` | PROOF GAP | depth-2 premise refuted ([P274]) |
| every wall splits over ℚ | `Detq.lean`, 18 branches | identities kernel-checked | the wall polynomial is built in Lean from the rotation matrix; the matrix form, the exact division and the determinant are Lean's; three must-fail controls fail |
| 727's pattern isolated and unaugmentable | — | exact CAS re-run | `eliminate729.py`, sympy Gröbner, 2026-09-28: same result. Not kernel-checked (needs Gröbner cofactors) |

Every triple cap in the table carries its scope: no shared face plane ([P397](LEDGER.md#p397), widened from pairwise transversality by [P406](LEDGER.md#p406)).

## The review list: project lemmas Lean takes on trust

Standard facts are not listed (Euler's formula with `c` components, the handshake lemma, Euler for a
convex polytope, "a convex set is connected", "a union of k convex sets has at most k components").

| lemma | source | used by | what to check |
|---|---|---|---|
| **ANCHOR** (Theorem 1): every component of `S_C(R)` contains a face-centre direction of C, lying in `S_C` | max2_report.md §1, [P33], [P416] | max(2), max(3) both routes, Theorem S, `d_{n−1} ≤ 6n`, `d₃ ≤ 24` (261), `d₂(S) ≤ 18` (195), P413's shared-plane caps | the soft step ("q_t lands in U") TIGHTENED 2026-10-04 by [P416]: exact local cone, and an arc on the circle of active normals; checked on 788 instances incl. 290 with shared planes, with a must-fail control |
| **FIB**: depth-(k−1) regions biject with components of a spherical set | PROOF_67 §2, PROOF_FORMAL B1 | max(2), max(3), Theorem S | "routine" in the source; convexity and O interior |
| **six-slab cover** `a, b ≤ 6` | PROOF_FORMAL A2, [P110] | max(3) MV route | |
| **six convex sectors** `m ≤ 6` | [P110] Addendum 2 | max(3) MV route | that each sector piece of the complement is convex |
| **Mayer–Vietoris + Alexander duality** `s ≤ a + b + m − 2` | [P110] | max(3) MV route | the standing hypotheses `a, b ≥ 1`, `U, C ≠ ∅` and the degenerate cases |
| **Step T's local inequality (◆)** and its summation | PROOF_STEP_T.md | `W ≤ 92` (the triple cap no longer needs it, [P406]) | assumes pairwise transversality |
| **Part D1–D3**: contact degree = polytope vertex degree | PROOF_FORMAL Part D | `W ≤ 92` | assumes pairwise transversality |
| **triple points are bottom vertices** | PROOF_67 §5.3 | Lemma 1a | PROOF_67's caveat, tangential triple points: CLOSED for no shared face plane by [P417] (circle lemma; 6 252 triple points checked) |
| **[P237] steps 2–4**: three-body gain, two-body gain, "adding cubes only deletes outer vertices" | [P237] | `d₁` bound, the pair cap `E_i ≤ 10` everywhere | whether the weight form `EE + 2·SC2` assumes transversality ([P397]) |
| **[P56] (I)–(V)** | [P56] | increment | |
| **Theorem S, Lemmas 2 and 3** | PROOF_SUBSET.md | Theorem S | pure set and partition combinatorics: formalisable in full with Mathlib |
| **the level identity** `d_ℓ = E_ℓ − V_ℓ + c_ℓ + 1` | [P243] | tower, `d₁` bound | |
| **the excess accounting** `sum(E − V) ≤ T + two-body` | [P407] | tower | PROVED by the circle model; checked on 165 compounds, equality without four-fold points |
| **the wall polynomials** W4, W3 | [P104] | wall splitting | that they are the right geometric conditions |
| **DEPTH**: depth-A regions biject with components of `{max_A M < min_B M}` | [P399] | `max(4) ≤ 285` | the radial fibre argument, ties included; tested against the engine on 17 configurations |
| **LOCAL COINCIDENCE**: near a two-body vertex, or a triple point whose fourth cube does not contain it, the level-2 boundary equals a triple's bottom diagram | [P404] | `max(4) ≤ 194 + c₂ + …` | same degree; checked on every vertex of 210 configurations |
| **CIRCLE LEMMA**: at a point p, all active facet normals of all cubes project onto one circle; top-diagram switches inject into colour changes | [P405] | `X = 0`, `W4u = 0` | the exactness of the local model; the no-tie argument; tested with a must-fail control |
| **BAND LEMMA** `c₂ − 1 ≤ Σ_S (c_S − 1)` | [P410], PROOF_BAND | `max(4) ≤ 195` | G2: the region/component tree on S² (unicoherence); G3: the label changes across every arc of Γ; G4: the face-centre point; G5: the continuum step; G6: the one-colour rule; the transversality lemma ([P412]: without a shared face plane every tie crosses). The finite count (Lemma C) is checked exhaustively to 14 nodes with a must-fail control (`tree_lemma_check.py`) |
| **PATCH CHARGING (L)** `deg_G′ − 2 ≤ Σ_S (deg_{G′_S} − 2)` with tie patches | [P418], PROOF_SHARED §2, §4 | `max(4) ≤ 187` for exactly one sharing pair | the circle model with one shared point. The classification of direction ties: the only three-cube type is `a = b` tied on both sides with `c` crossing (corrected the same day from "never"). The two identities `deg τ + deg β = Σ deg π` and `Σ_S deg B_S = deg μ + 2·C12` hold at every direction type. `deg β ≥ 3` holds, or else `π_ab` is the whole circle. Sampled in the exact circle model with a must-fail control (`patch_charging_local.py`) and per compound (`shared_oracle.py`: 387 compounds, 0 violations) |
| **BAND LEMMA WITH PATCHES** | [P418], PROOF_SHARED §3 | `max(4) ≤ 187` for exactly one sharing pair | G3's patch case: each patch borders an arc of `∂P_d` (label `{c,d}`) and an arc of `∂(O ∩ P_c)` (another label). `j_Q ≤ 2` (a component of convex minus convex). `p_S = 2` (`O ∩ P_z` is convex). Euler on `G′` with patches as faces. 1D ties are crossings in the circle model |
| **(L), TWO OR MORE SHARING PAIRS** | [P419], [P420], PROOF_SHARED §5 | `max(4) ≤ 195` unconditional (draft, [P422]) | (a) Completeness of the direction types. Each tying cube's nearest point is left, right, both, the direction itself, or its antipode. Equal type means a shared point, and at most one "both". The enumeration is `direction_types.py`. (b) The residue: two cubes owning unshared points give `>= 3` innermost ends. (c) The cell argument: degrees depend only on the cyclic order of the critical directions, and the arrangement is sampled at every vertex, edge and both sides of each edge (`residue_exact.py`), with an order-type cross-check. (d) Corner patterns are empty, since they would need a forbidden triangle. (e) The eight realisable structures: two shared planes make one cube, and both the triangle and the 4-cycle force that |
| **GLUE LEMMA** (patch holes only along hub edges) | [P422], PROOF_SHARED §5 | `max(4) ≤ 195` unconditional | two proofs. (i) Algebra: a tie that fails across the glue arc puts it on a cube's edge circle `(n − m_x)·u = 0`, and equal values put it on a bisector `(n ∓ n′)·u = 0`. Their coincidence forces `n·n′ = 0` and `m_x = ±n′`. (ii) Exhaustive local check (`glue_check.py`, 32 patterns, every cell) with a positive hub control. Then the counts: `≤ 2` glue arcs per hub edge by convexity, which suffices everywhere (per-edge tolerance 2–6), and `−χ(Γ°) ≤ m` by Mayer–Vietoris |
| **χ_c CHAIN** `d2 ≤ Σ_S (d2(S) + χ(B_S°)) − 6 − χ(Γ°)` | [P422] | same | Alexander duality `d2 = 1 + b1(Γ)` with compactly supported χ, `χ(Γ) = V − E + χ(Γ°)`. The band lemma is used in the form `c(Γ) − 1 ≤ Σ_S (c(B_S) − 1)`. It reduces to [P418]'s chain for one pair |
| **PER-STRUCTURE `d3`** `d3 ≤ 24 − 2·(cube, shared normal) incidences` | [P413], [P416], [P422] | same | strengthened ANCHOR at n = 4: a shared face direction anchors nothing. It is attained by every structure's climbed best |
| **AXIS-PIECE G3** | [P422] | same | the ray argument: a single exit label on every ray would nest two distinct concentric congruent squares. It includes axis four and pieces merged at a hub |
| **SUBSET IDENTITIES AT n = 5** `Σ_tri X_S(2) = X₂ + X₄`, `Σ_4 X_S(3) = X₃ + X₄` (generic; slack otherwise) | [P425], [P427] | `max(5) ≤ 485` (no shared plane, draft, [P430]) | generic vertices are three-cube tie points (on levels s+1, s+2) and edge–edge crossings (one level); per-vertex bookkeeping reproduces the measured slack exactly on all 21 types. The margin identity built on them is algebra |
| **H1, PER VERTEX** | [P428], PROOF_N5 Part 1 | same | P's share is `Σ_θ Δ(θ)/2 − K(t, c)`; Δ ≥ ray pair counts (exhaustive, 742 weak orders); ray lemmas R1 (transversality), R2 (colour changes ≥ t), R3 (minimal bottom ⇒ next level ≥ t rays, by adjacent blocks); finite case table over (t, c). Inherits the circle model and transversality at n = 5 |
| **Lℓ, BAND LEMMA AT LEVEL ℓ** `c_ℓ − 1 ≤ Σ_{|S|=ℓ+1} (c(B_S) − 1)`, ℓ ≤ n − 2 | [P430], PROOF_N5 Part 2 | same | PROOF_BAND's G1–G6 and Lemma C with labels = top-ℓ sets. Lemma C rechecked with 4 colours (9.1 M instances, must-fail control). Inherits PROOF_BAND's G2 and G5 plane-topology steps |
| **TOP LEVEL BY ITS FACES** `d₄ ≥ 5`, `d₄ ≥ c₄ + 1` | [P430], PROOF_N5 Part 3 | same | each cube strictly innermost at its face centres; each component of Γ₄ borders two faces of different labels, so the face/component tree has `≥ 2c₄` edges. With `d₄ ≤ 30` (ANCHOR) this gives 485, and 457 when `d₄ ≥ 2c₄` |
| **PATCHES AT n = 5, ONE PAIR** `Σ_S p_S = 12`, `p₄ = 2`, `j_Q ≤ 2` | [P434], [P435], PROOF_N5 Part 4.1 | `max(5) ≤ 469` (one sharing pair, draft) | the subset patches are convex sets about `±f`. The level-2/3 patches are differences of star-shaped sets (unions of convex sets containing the centre), so each ray meets a patch in an interval and the complement has ≤ 2 components |
| **WHOLE-GRAPH RULE** (case (i), a and b own only s): `(S, ℓ)` is whole iff `S ∩ T = {a, b}` and `ℓ − |S ∩ C| = 1` | [P435], Part 4.2 | same | every other cube of T is above a = b at s and below it at its own point. Gives `K_i(t, c)` |
| **ISOLATED a–b TIES CROSS** | [P435], Part 4.2 R1 | same | a non-crossing tie needs a minimum of `d_a` there, hence `d_a = d_b = 0`: the tie is at s, where it is a sector |
| **CHECK 1′** (ends; (L, W, R) triples) | [P435], Part 4.2 | same | exhaustive (≈41 600 triples), injected-defect control fails on 118. Holds even with any pair tying on a side |
| **R2, R2_i** via the cut sequence: bottom ends ≥ t (ii), ≥ t+1 (iii), ≥ t−1 (i) | [P435], Part 4.2 | same | s's Voronoi cell is a bottom-level sector with 2 ends (only s and the neighbour are equidistant at its boundary); other colour changes are isolated rays |
| **R3″** (case (ii): bottom = t ⇒ next level ≥ 3 ends) | [P435], Part 4.2 | same | a sector of A_{t−2} starts at the boundary of s's cell with a non-a neighbour; along it `d_s` rises with slope 1, so it ends with a change of the bottom-two label; a cyclic label cannot change exactly once |
| **R3_i** (case (i), t ≥ 4: next level ≥ 4 ends) | [P435], Part 4.2 | same | N = number of cubes nearer than s; {N = 1} borders both ends of s's cell, and N ≥ 2 at a colour change of the cut sequence, so {N = 1} has ≥ 2 components |
| **G3 PATCH CASE AT LEVEL ℓ** | [P435], Part 4.3 | same | a patch reaches both `∂U_ℓ` (label U + z) and `∂(O ∩ U_{ℓ−1})` (label U + a, U + b or U − z + ab), so its neighbours carry two labels |
| **NO TOUCHING TIES** (any sharing): a pair tied at θ, strict on both sides, crosses | [P438] | multi-pair H1 (in progress) | a turn of `d_x − d_y` at θ needs both distances 0 there, i.e. a common point at θ, and then they tie on both sides |
| **ISOLATED TIES CHANGE THE LABEL** (any side ties) | [P438] | same | exhaustive over (L, W, R) with touching excluded: 50 272 isolated ties, 0 exceptions |
| **u ≥ 3 BOTTOM** `≥ u + m` ends | [P438] | same | runs of shared cells are sectors (2 ends each), and changes between unshared owners are rays |
| **u ≥ 3 MINIMAL BOTTOM ⇒ NEXT LEVEL ≥ 3** | [P438] | same | contiguous X, Y, Z; label {x, y} → {y, z}; case split on the shared cells next to X and Z; the only 2-end case forces a bottom switch |
| **PIECES**: those sets and their complements are unions of convex pieces, one per active face | [P399] | `max(4) ≤ 285` | convexity of `{M_a < t.u}` on a sector; pointedness |
<!-- reviewed 2026-09-28: cites the parts of P237, P243 and P326 that stand, with their conditions in the table -->

## What this pass found

1. **The Euler route to max(3) assumes a connected top diagram.** PROOF_67 §5: "for a cellular
   graph on S²". Not proved. max(3) = 67 is unaffected: the Mayer–Vietoris route needs no such
   assumption, and no transversality either.
2. **[P237]'s `+ 2` assumes `c₁ = 1`.** Its own step 1 carries `c`; the published bound dropped it.
3. **The triple cap lost its transversality scope when lifted to every n** ([P397](LEDGER.md#p397)); scope CORRECTED 2026-10-04: the circle lemma removed the need for it, leaving only "no shared face plane" ([P406](LEDGER.md#p406)).
4. **Stale labels**: PROOF_67's "CANDIDATE PROOF" for the contact bound (completed in
   PROOF_FORMAL); RESULTS filed the merge law, a verified identity, among the proofs.
5. **`detq_check.py` did not run** (a variable used before its definition); fixed, and it reproduces.
