/-!
# The upper-bound reductions on max(n), with every geometric input as a NAMED HYPOTHESIS

Lean cannot see the cubes.  What it can check is the part that has actually gone wrong in this
project: the step from a list of facts about pairs, triples and levels to a bound on the count,
and in particular WHICH facts that step used.  Every geometric input below is a hypothesis of the
theorem that uses it, never an `axiom`, so nothing is assumed globally and `#print axioms` stays
clean.  The prefix of each hypothesis's name records its status in LEDGER.md, and
`../src/lean_status.py` reads the signatures back from Lean and derives each bound's label:

    proved_   a result proved in the ledger (the proof itself is outside Lean)
    argued_   argued in the ledger but recorded as not verified
    hyp_      an open hypothesis: a conjecture, or an identity that holds only under one
    refuted_  a premise the ledger has refuted

  any refuted_  ->  PROOF GAP        any hyp_ or argued_  ->  PROVED IF        else  ->  PROVED

Written 2026-09-28 after [P395]: `TOTAL <= 195 - Q4` was listed as proved under the wrong
condition.  Its hypotheses are now printed by Lean, not transcribed.

Half-integers (h(S) = 0.5 + ...) are handled by doubling, so everything is over Nat or Int.
-/

namespace Cube

/-- binomial coefficient (core Lean has none without Mathlib) -/
def C : Nat → Nat → Nat
  | _, 0 => 1
  | 0, _ + 1 => 0
  | n + 1, k + 1 => C n k + C n (k + 1)

example : C 4 3 = 4 ∧ C 4 2 = 6 ∧ C 10 3 = 120 := by decide

/-! ## [P348] `h(S) <= 47.5`, per 3-subset, as `2 h <= 95` -/

/-- `h2 = 2 h(S)`.  The identity `h = 0.5 + (1/2) sum E_i + E_S` is written with TRIVIAL holes
([P348] caveat 1), so it is a hypothesis, not a fact. -/
theorem h_le (h2 E1 E2 E3 ES : Nat)
    (hyp_P348_identity_trivial_holes : h2 = 1 + E1 + E2 + E3 + 2 * ES)
    (proved_P237_pair_cap : E1 ≤ 10 ∧ E2 ≤ 10 ∧ E3 ≤ 10)
    (proved_triple_cap_if_no_shared_face_plane : ES ≤ 32) :
    h2 ≤ 95 := by
  omega

/-! ## [P348]/[P341] `TOTAL <= 195 - Q4` at n = 4 -/

/-- The four 3-subsets' doubled `h`, and the identity `TOTAL = sum_S h(S) + 5 - Q4`, which [P341]
states with trivial holes. -/
theorem total_le_195_minus_Q4 (TOTAL Q4 : Int) (a b c d : Int)
    (hyp_P341_identity_trivial_holes : 2 * TOTAL = a + b + c + d + 10 - 2 * Q4)
    (hyp_P348_h_le_each : a ≤ 95 ∧ b ≤ 95 ∧ c ≤ 95 ∧ d ≤ 95) :
    TOTAL ≤ 195 - Q4 := by
  omega

/-- The same, assembled from the per-pair and per-triple caps: the whole chain in one statement.
Pair caps enter each triple separately; sharing a pair between triples only helps. -/
theorem total_le_195_minus_Q4_from_caps (TOTAL Q4 : Int)
    (e : Fin 4 → Fin 3 → Int) (es : Fin 4 → Int)
    (hyp_P341_identity_trivial_holes :
      2 * TOTAL = (1 + e 0 0 + e 0 1 + e 0 2 + 2 * es 0) + (1 + e 1 0 + e 1 1 + e 1 2 + 2 * es 1)
                + (1 + e 2 0 + e 2 1 + e 2 2 + 2 * es 2) + (1 + e 3 0 + e 3 1 + e 3 2 + 2 * es 3)
                + 10 - 2 * Q4)
    (proved_P237_pair_cap : ∀ s i, e s i ≤ 10)
    (proved_triple_cap_if_no_shared_face_plane : ∀ s, es s ≤ 32) :
    TOTAL ≤ 195 - Q4 := by
  have := proved_P237_pair_cap
  have h00 := this 0 0; have h01 := this 0 1; have h02 := this 0 2
  have h10 := this 1 0; have h11 := this 1 1; have h12 := this 1 2
  have h20 := this 2 0; have h21 := this 2 1; have h22 := this 2 2
  have h30 := this 3 0; have h31 := this 3 1; have h32 := this 3 2
  have t0 := proved_triple_cap_if_no_shared_face_plane 0; have t1 := proved_triple_cap_if_no_shared_face_plane 1
  have t2 := proved_triple_cap_if_no_shared_face_plane 2; have t3 := proved_triple_cap_if_no_shared_face_plane 3
  omega

/-! ## [P326] the tower bound `TOTAL <= 1 + 32 C(n,3) + 10 C(n,2) + 3(n-1)` -/

/-- [P326]'s chain.  Its label was "proved modulo one hypothesis" (holes).  Stated with its inputs
named, it had TWO non-proved ones: the holes, and the accounting step `sum(E - V) <= T + two-body`, PROVED since by [P407];
which [P388]'s addendum records as argued and not verified. -/
theorem tower (n L TOTAL SEV T3 TB holes : Nat)
    (proved_levels : L = n - 1)
    (proved_P243_level_identity : TOTAL = 1 + SEV + 2 * L + holes)
    (proved_P407_excess_accounting_if_no_shared_face_plane : SEV ≤ T3 + TB)
    (proved_triple_cap_if_no_shared_face_plane : T3 ≤ 32 * C n 3)
    (proved_P237_pair_cap : TB ≤ 10 * C n 2)
    (hyp_OQ30_holes_le_one_per_level : holes ≤ L) :
    TOTAL ≤ 1 + 32 * C n 3 + 10 * C n 2 + 3 * (n - 1) := by
  omega

example : 1 + 32 * C 4 3 + 10 * C 4 2 + 3 * (4 - 1) = 198 := by decide
example : 1 + 32 * C 10 3 + 10 * C 10 2 + 3 * (10 - 1) = 4318 := by decide

/-- `c_ell <= 2` on each of n = 4's three levels gives `holes <= L`: the step from the STRONG
CONJECTURE to the tower bound's hypothesis. -/
theorem holes_of_c_le_two (c1 c2 c3 holes : Nat)
    (proved_holes_def : holes = (c1 - 1) + (c2 - 1) + (c3 - 1))
    (hyp_OQ30_c_le_two : c1 ≤ 2 ∧ c2 ≤ 2 ∧ c3 ≤ 2) :
    holes ≤ 3 := by
  omega

/-! ## [P249] `max(4) <= 953`, the sum of per-depth bounds -/

/-- The depth-2 bound is [P243]'s, argued from "no two-body vertex below depth 1", which [P274]
refuted.  Lean checks the sum; the name records why the sum is not a proof. -/
theorem total_le_953 (TOTAL d1 d2 d3 d4 : Nat)
    (proved_depth_sum : TOTAL = d1 + d2 + d3 + d4)
    (proved_P237_depth1 : d1 ≤ 108 * C 4 3 + 10 * C 4 2 + 2)
    (refuted_P243_depth2_no_twobody_P274 : d2 ≤ 108 * C 4 3 + 2)
    (proved_P24_ceiling_l1 : d3 ≤ 6 * 4)
    (proved_core : d4 = 1) :
    TOTAL ≤ 953 := by
  have h : C 4 3 = 4 ∧ C 4 2 = 6 := by decide
  omega

end Cube
