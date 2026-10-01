import CubeBounds.Basic
/-!
# The counting skeletons of the PROVED results (RESULTS §2), with geometric inputs named

Same convention as `Basic.lean`: every geometric or topological fact enters as a hypothesis whose
prefix records its status (`proved_`, `argued_`, `hyp_`, `refuted_`), and `src/lean_status.py`
derives the label.  What Lean checks here is the COUNTING: that the stated inputs imply the stated
bound, and which inputs each proof actually needs.

**Euler is always written with `c` components**: for a graph on the sphere, `V - E + F = 1 + c`.
The version `V - E + F = 2` is the case `c = 1`, and a proof that uses it must say so.  That
convention is how this file found that the Euler route to max(3) = 67 and [P237]'s `d1` bound both
assume a connected diagram (P398).
-/

namespace Cube

/-! ## max(2) = 13  (max2_report.md: Theorem 1 = ANCHOR, plus FIB) -/

theorem max2_le_13 (total d1 d2 c1 c2 : Nat)
    (proved_depth_sum : total = d1 + d2)
    (proved_A1_intersection_convex : d2 ≤ 1)
    (proved_FIB_depth1 : d1 = c1 + c2)
    (proved_ANCHOR_Theorem1_each : c1 ≤ 6 ∧ c2 ≤ 6) :
    total ≤ 13 := by
  omega

/-! ## max(3) <= 67, route 1: Mayer–Vietoris + Alexander duality ([P110]) -/

/-- `s_i` = components of `T_i` (cell i uniquely farthest), `a_i, b_i` = components of the two
pairwise sets `{r_i > r_j}`, `{r_i > r_k}`, `m_i` = components of their complement. -/
theorem max3_le_67_MV (total d1 d2 d3 s1 s2 s3 a1 b1 m1 a2 b2 m2 a3 b3 m3 : Nat)
    (proved_depth_sum : total = d1 + d2 + d3)
    (proved_A1_triple_intersection_convex : d3 ≤ 1)
    (proved_A2_ANCHOR_depth2 : d2 ≤ 18)
    (proved_B1_FIB_depth1 : d1 = s1 + s2 + s3)
    (proved_P110_MV_Alexander : s1 + 2 ≤ a1 + b1 + m1 ∧ s2 + 2 ≤ a2 + b2 + m2 ∧ s3 + 2 ≤ a3 + b3 + m3)
    (proved_six_slab_cover : a1 ≤ 6 ∧ b1 ≤ 6 ∧ a2 ≤ 6 ∧ b2 ≤ 6 ∧ a3 ≤ 6 ∧ b3 ≤ 6)
    (proved_P110_six_convex_sectors : m1 ≤ 6 ∧ m2 ≤ 6 ∧ m3 ≤ 6) :
    total ≤ 67 := by
  omega

/-! ## max(3) <= 67, route 2: Euler on the top diagram (PROOF_FORMAL.md Parts B–E) -/

/-- Lemma 1a (PROOF_67 §5.3): triple points `<= 32`, from Euler on the BOTTOM diagram.  Written
with `c` components; the bound only improves when `c > 1`, so no connectivity is needed. -/
theorem lemma1a_triple_le_32 (V E F c sumdeg triples : Nat)
    (proved_Euler_sphere : V + F = E + 1 + c)
    (proved_handshake : sumdeg = 2 * E)
    (proved_suppressed_deg_ge_3 : 3 * V ≤ sumdeg)
    (proved_components_pos : 1 ≤ c)
    (proved_A2_faces_are_depth2 : F ≤ 18)
    (proved_transversal_triple_points_are_bottom_vertices : triples ≤ V) :
    triples ≤ 32 := by
  omega

/-- The top-diagram weight `W = sum (deg - 2) <= 92`: Step T's local inequality (◆), summed, draws
from the bottom diagram's weight and the three pairwise polytopes' weights. -/
theorem weight_le_92 (W Wbot Vb Eb Fb cb P1 P2 P3 F1 F2 F3 : Nat)
    (proved_transversal_StepT_diamond_summed : W ≤ Wbot + P1 + P2 + P3)
    (proved_Euler_bottom : Vb + Fb = Eb + 1 + cb)
    (proved_bottom_weight : Wbot + 2 * Vb = 2 * Eb)
    (proved_components_pos : 1 ≤ cb)
    (proved_A2_faces_are_depth2 : Fb ≤ 18)
    (proved_polytope_Euler_weight : P1 + 4 = 2 * F1 ∧ P2 + 4 = 2 * F2 ∧ P3 + 4 = 2 * F3)
    (proved_pair_polytope_faces : F1 ≤ 12 ∧ F2 ≤ 12 ∧ F3 ≤ 12) :
    W ≤ 92 := by
  omega

/-- The route's last step, `d1 = F_top = 2 + W/2`.  Euler on the top diagram gives
`2 d1 = 2 + 2c + W`; PROOF_67 §5 writes it for "a cellular graph on S²", i.e. `c = 1`, and
nothing in PROOF_67 or PROOF_FORMAL proves the top diagram connected. -/
theorem max3_le_67_Euler (total d1 d2 d3 W c : Nat)
    (proved_depth_sum : total = d1 + d2 + d3)
    (proved_A1_triple_intersection_convex : d3 ≤ 1)
    (proved_A2_ANCHOR_depth2 : d2 ≤ 18)
    (proved_B2_Euler_top_with_components : 2 * d1 = 2 + 2 * c + W)
    (proved_transversal_weight_le_92 : W ≤ 92)
    (hyp_top_diagram_connected : c = 1) :
    total ≤ 67 := by
  omega

/-! ## [P237] `d1 <= 108 C(n,3) + 10 C(n,2) + 2` -/

/-- Step 1 of [P237] is exact with the component count: `d1 = gain + c + 1`.  The published
`+ 2` is `c = 1`.  `c1` is odd by [P311] and 1 in every instance measured, but not proved 1. -/
theorem d1_bound (n d1 g3 g2 c : Nat)
    (proved_P237_step1_Euler : d1 = g3 + g2 + c + 1)
    (proved_P237_step2_three_body : g3 ≤ 108 * C n 3)
    (proved_P237_step3_two_body : g2 ≤ 10 * C n 2)
    (hyp_OQ30_c1_eq_1 : c = 1) :
    d1 ≤ 108 * C n 3 + 10 * C n 2 + 2 := by
  omega

/-- The same chain with `c` kept: this much IS proved for every configuration. -/
theorem d1_bound_with_c (n d1 g3 g2 c : Nat)
    (proved_P237_step1_Euler : d1 = g3 + g2 + c + 1)
    (proved_P237_step2_three_body : g3 ≤ 108 * C n 3)
    (proved_P237_step3_two_body : g2 ≤ 10 * C n 2) :
    d1 ≤ 108 * C n 3 + 10 * C n 2 + c + 1 := by
  omega

/-- [P237] step 3: a pair's two-body gain `<= 10`, from max(2) = 13 and `d2(pair) >= 1`.
Here `c >= 1` is used in the SAFE direction, so no connectivity is assumed. -/
theorem pair_gain_le_10 (count d1 d2 c gain : Nat)
    (proved_depth_sum : count = d1 + d2)
    (proved_max2 : count ≤ 13)
    (proved_core_nonempty : 1 ≤ d2)
    (proved_Euler_pair : d1 = gain + c + 1)
    (proved_components_pos : 1 ≤ c) :
    gain ≤ 10 := by
  omega

/-! ## Theorem S at n = 4 (PROOF_SUBSET.md) -/

/-- The per-cube theorem for `|R| = 3`, from Lemma 2 (anchor loss subadditive), Lemma 3 (sharing
monotone) and ANCHOR (`c <= k <= 6`).  `mR, sR` for R, `m1..s3` for `R \ {m_i}`. -/
theorem per_cube_n4 (cR c1 c2 c3 mR sR m1 s1 m2 s2 m3 s3 : Int)
    (proved_split : cR = 6 - mR - sR ∧ c1 = 6 - m1 - s1 ∧ c2 = 6 - m2 - s2 ∧ c3 = 6 - m3 - s3)
    (proved_ANCHOR_nonneg : 0 ≤ m1 ∧ 0 ≤ s1 ∧ 0 ≤ m2 ∧ 0 ≤ s2 ∧ 0 ≤ m3 ∧ 0 ≤ s3)
    (proved_Lemma2_loss_subadditive : mR ≤ m1 + m2)
    (proved_Lemma3_sharing_monotone : sR ≤ s1) :
    c1 + c2 + c3 ≤ 12 + cR := by
  omega

/-- Theorem S at n = 4, `sum_T d2(T) <= 48 + d3`, summing the per-cube theorem over the four
cubes and regrouping by FIB. -/
theorem theoremS_n4 (sumT_d2 d3 : Int) (lhs rhs : Fin 4 → Int)
    (proved_per_cube : ∀ C, lhs C ≤ 12 + rhs C)
    (proved_FIB_regroup_left : sumT_d2 = lhs 0 + lhs 1 + lhs 2 + lhs 3)
    (proved_FIB_right : d3 = rhs 0 + rhs 1 + rhs 2 + rhs 3) :
    sumT_d2 ≤ 48 + d3 := by
  have h0 := proved_per_cube 0; have h1 := proved_per_cube 1
  have h2 := proved_per_cube 2; have h3 := proved_per_cube 3
  omega

/-! ## [P56] the one-cube increment -/

/-- `Delta_j <= B_j = 1 + c + sum(deg/2 - 1)`: the chain (I)–(V), with Euler written with `c`
components on the cube's own surface. -/
theorem increment (Delta N comps edgesGj Wj Kj Bj c gain : Nat)
    (proved_I_merge_identity : Delta + comps = N)
    (proved_II_graph_edges : N ≤ comps + edgesGj)
    (proved_III_to_V_refinement : edgesGj ≤ Wj ∧ Wj ≤ Kj ∧ Kj ≤ Bj)
    (proved_Euler_with_components : Bj = 1 + c + gain) :
    Delta ≤ 1 + c + gain := by
  omega

/-! ## [P399] max(4) <= 285, with no hypothesis

Every depth reduces to components of `D(A) = {max_A M < min_B M}` on the sphere (DEPTH), and each
such set, and each complement below, is a union of convex pieces, one per choice of active face
(PIECES).  Mayer–Vietoris with Alexander duality, as in [P110], then bounds each intersection.
`sT` is cube i's depth-1 set, `sP` pair {i,j}'s depth-2 set. -/
theorem max4_le_285 (total d1 d2 d3 d4 : Nat)
    (sT aT bT mT : Fin 4 → Nat) (sP aP bP mP : Fin 6 → Nat)
    (proved_depth_sum : total = d1 + d2 + d3 + d4)
    (proved_DEPTH_core_is_whole_sphere : d4 ≤ 1)
    (proved_ANCHOR_depth3 : d3 ≤ 24)
    (proved_DEPTH_depth1 : d1 = sT 0 + sT 1 + sT 2 + sT 3)
    (proved_DEPTH_depth2 : d2 = sP 0 + sP 1 + sP 2 + sP 3 + sP 4 + sP 5)
    (proved_MV_Alexander : (∀ i, sT i + 2 ≤ aT i + bT i + mT i) ∧ (∀ p, sP p + 2 ≤ aP p + bP p + mP p))
    (proved_P110_triple_depth1 : ∀ i, aT i ≤ 16)
    (proved_PIECES_one_cube_beaten : (∀ i, bT i ≤ 6) ∧ (∀ p, aP p ≤ 6 ∧ bP p ≤ 6))
    (proved_PIECES_complements : (∀ i, mT i ≤ 12) ∧ (∀ p, mP p ≤ 12)) :
    total ≤ 285 := by
  obtain ⟨hT, hP⟩ := proved_MV_Alexander
  obtain ⟨hb, hab⟩ := proved_PIECES_one_cube_beaten
  obtain ⟨hmT, hmP⟩ := proved_PIECES_complements
  have t0 := hT 0; have t1 := hT 1; have t2 := hT 2; have t3 := hT 3
  have a0 := proved_P110_triple_depth1 0; have a1 := proved_P110_triple_depth1 1
  have a2 := proved_P110_triple_depth1 2; have a3 := proved_P110_triple_depth1 3
  have b0 := hb 0; have b1 := hb 1; have b2 := hb 2; have b3 := hb 3
  have m0 := hmT 0; have m1 := hmT 1; have m2 := hmT 2; have m3 := hmT 3
  have p0 := hP 0; have p1 := hP 1; have p2 := hP 2; have p3 := hP 3; have p4 := hP 4; have p5 := hP 5
  have q0 := hab 0; have q1 := hab 1; have q2 := hab 2; have q3 := hab 3; have q4 := hab 4; have q5 := hab 5
  have n0 := hmP 0; have n1 := hmP 1; have n2 := hmP 2; have n3 := hmP 3; have n4 := hmP 4; have n5 := hmP 5
  omega

/-! ## [P400] the general-n bound: the per-set recurrence and its closed form

Splitting one cube `b` off `B`, Mayer–Vietoris gives
`c(A, B) + 2 <= c(A, B \ {b}) + c(A, {b}) + m` with `c(A, {b}) <= 6` and `m <= 6 |A| (|B| - 1)`.
Lean proves the closed form by induction on `|B|`, from the recurrence as a hypothesis. -/
theorem per_set_closed_form (a : Nat) (c : Nat → Nat)
    (proved_PIECES_base : c 1 ≤ 6)
    (proved_MV_step : ∀ k, 1 ≤ k → c (k + 1) + 2 ≤ c k + 6 + 6 * a * k) :
    ∀ k, 1 ≤ k → c k ≤ 4 * k + 2 + 3 * a * k * (k - 1) := by
  intro k hk
  induction k with
  | zero => omega
  | succ n ih =>
    rcases Nat.lt_or_ge n 1 with h | h
    · have : n = 0 := by omega
      subst this; simpa using proved_PIECES_base
    · have h1 := ih h
      have h2 := proved_MV_step n h
      have e : 3 * a * (n + 1) * (n + 1 - 1) = 3 * a * n * (n - 1) + 6 * a * n := by
        cases n with
        | zero => omega
        | succ m => simp only [Nat.add_sub_cancel]; grind
      omega

/-- the bound's values: exact at n = 2, 3, and 285, 1081 at n = 4, 5 -/
def fcap (a k : Nat) : Nat := 4 * k + 2 + 3 * a * k * (k - 1)
def gbound (n : Nat) : Nat := 1 + ((List.range n).drop 1).foldl (fun s l => s + C n l * fcap l (n - l)) 0
example : gbound 2 = 13 ∧ gbound 3 = 67 ∧ gbound 4 = 285 ∧ gbound 5 = 1081 := by decide

/-! ## [P401] the tightened recurrence: the complement's pieces share face centres

All pieces `{M_a >= M_c, M_a >= M_b}` on one face sector `s` of `a` contain the face centre `n_s`,
where `M_a = 1 >= M_x` for every cube (Cauchy–Schwarz; the facet-centre lemma [P311]), so they form
ONE component: `m <= 6 |A|`, not `6 |A| (|B| - 1)`. -/
theorem per_set_closed_form_tight (a : Nat) (c : Nat → Nat)
    (proved_PIECES_base : c 1 ≤ 6)
    (proved_MV_step_facet_centres : ∀ k, 1 ≤ k → c (k + 1) + 2 ≤ c k + 6 + 6 * a) :
    ∀ k, 1 ≤ k → c k ≤ 4 * k + 2 + 6 * a * (k - 1) := by
  intro k hk
  induction k with
  | zero => omega
  | succ n ih =>
    rcases Nat.lt_or_ge n 1 with h | h
    · have : n = 0 := by omega
      subst this; simpa using proved_PIECES_base
    · have h1 := ih h
      have h2 := proved_MV_step_facet_centres n h
      have e : 6 * a * (n + 1 - 1) = 6 * a * (n - 1) + 6 * a := by
        cases n with
        | zero => omega
        | succ m => simp only [Nat.add_sub_cancel]; grind
      omega

/-- depth 1 at every n: `d1 <= n (10 n - 14) = 10 n^2 - 14 n`, the ceiling law at l = n - 1 -/
theorem depth1_ceiling (n d1 per : Nat) (hn : 2 ≤ n)
    (proved_DEPTH_depth1_sum : d1 ≤ n * per)
    (proved_per_cube : per ≤ 4 * (n - 1) + 2 + 6 * 1 * ((n - 1) - 1)) :
    d1 ≤ n * (10 * n - 14) := by
  have : 4 * (n - 1) + 2 + 6 * 1 * ((n - 1) - 1) = 10 * n - 14 := by omega
  rw [this] at proved_per_cube
  exact Nat.le_trans proved_DEPTH_depth1_sum (Nat.mul_le_mul_left n proved_per_cube)

theorem max4_le_261 (total d1 d2 d3 d4 : Nat)
    (sT aT bT mT : Fin 4 → Nat) (sP aP bP mP : Fin 6 → Nat)
    (proved_depth_sum : total = d1 + d2 + d3 + d4)
    (proved_DEPTH_core_is_whole_sphere : d4 ≤ 1)
    (proved_ANCHOR_depth3 : d3 ≤ 24)
    (proved_DEPTH_depth1 : d1 = sT 0 + sT 1 + sT 2 + sT 3)
    (proved_DEPTH_depth2 : d2 = sP 0 + sP 1 + sP 2 + sP 3 + sP 4 + sP 5)
    (proved_MV_Alexander : (∀ i, sT i + 2 ≤ aT i + bT i + mT i) ∧ (∀ p, sP p + 2 ≤ aP p + bP p + mP p))
    (proved_P110_triple_depth1 : ∀ i, aT i ≤ 16)
    (proved_PIECES_one_cube_beaten : (∀ i, bT i ≤ 6) ∧ (∀ p, aP p ≤ 6 ∧ bP p ≤ 6))
    (proved_PIECES_facet_centre_complements : (∀ i, mT i ≤ 6) ∧ (∀ p, mP p ≤ 12)) :
    total ≤ 261 := by
  obtain ⟨hT, hP⟩ := proved_MV_Alexander
  obtain ⟨hb, hab⟩ := proved_PIECES_one_cube_beaten
  obtain ⟨hmT, hmP⟩ := proved_PIECES_facet_centre_complements
  have t0 := hT 0; have t1 := hT 1; have t2 := hT 2; have t3 := hT 3
  have a0 := proved_P110_triple_depth1 0; have a1 := proved_P110_triple_depth1 1
  have a2 := proved_P110_triple_depth1 2; have a3 := proved_P110_triple_depth1 3
  have b0 := hb 0; have b1 := hb 1; have b2 := hb 2; have b3 := hb 3
  have m0 := hmT 0; have m1 := hmT 1; have m2 := hmT 2; have m3 := hmT 3
  have p0 := hP 0; have p1 := hP 1; have p2 := hP 2; have p3 := hP 3; have p4 := hP 4; have p5 := hP 5
  have q0 := hab 0; have q1 := hab 1; have q2 := hab 2; have q3 := hab 3; have q4 := hab 4; have q5 := hab 5
  have n0 := hmP 0; have n1 := hmP 1; have n2 := hmP 2; have n3 := hmP 3; have n4 := hmP 4; have n5 := hmP 5
  omega

def fcap2 (a k : Nat) : Nat := 4 * k + 2 + 6 * a * (k - 1)
def gbound2 (n : Nat) : Nat := 1 + ((List.range n).drop 1).foldl (fun s l => s + C n l * fcap2 (n - l) l) 0
example : gbound2 2 = 13 ∧ gbound2 3 = 67 ∧ gbound2 4 = 261 ∧ gbound2 5 = 871 := by decide

/-! ## [P404] `max(4) <= 195`, conditionally: the level-2 charging argument

Every vertex of `Gamma` (the level-2 boundary) is charged to a vertex of some triple's bottom
diagram `B_S` with the same degree: two-body vertices, and triple points whose fourth cube does not
contain them.  The triple budgets `E_S - V_S = d2(S) - 1 - c_S <= 16` then bound `Gamma`'s excess.
`X` is the excess at triple points whose fourth cube contains them (Gamma follows the triple's TOP
diagram there); `W4u` the four-fold excess not covered by its four `B_S` occurrences. -/
theorem max4_le_195_charging (total d1 d2 d3 d4 : Nat) (EG VG c2 X W4u : Int) (bud : Fin 4 → Int)
    (proved_depth_sum : total = d1 + d2 + d3 + d4)
    (proved_depth1_ceiling : d1 ≤ 104)
    (proved_ANCHOR_depth3 : d3 ≤ 24)
    (proved_core : d4 ≤ 1)
    (proved_Euler_Gamma_with_components : (d2 : Int) = EG - VG + c2 + 1)
    (proved_charging_if_no_shared_face_plane : EG - VG ≤ bud 0 + bud 1 + bud 2 + bud 3 + X + W4u)
    (proved_ANCHOR_triple_budget : ∀ S, bud S ≤ 16)
    (hyp_OQ30_c2_eq_1 : c2 = 1)
    (proved_circle_lemma_X_eq_0 : X = 0)
    (proved_circle_lemma_fourfold_charged : W4u = 0) :
    total ≤ 195 := by
  have b0 := proved_ANCHOR_triple_budget 0; have b1 := proved_ANCHOR_triple_budget 1
  have b2 := proved_ANCHOR_triple_budget 2; have b3 := proved_ANCHOR_triple_budget 3
  omega

end Cube
