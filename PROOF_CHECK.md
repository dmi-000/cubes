# Proof check: what a machine has verified, and what still needs a reader

*Current as of 2026-09-28 ([P398](LEDGER.md#p398)). Regenerate the checks with
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
| tower bound (198 at n = 4) | `tower` | PROVED IF holes ≤ 1 and the accounting step | [P326], [P396] |
| **`max(4) ≤ 261`**, and `d₁ ≤ 10n² − 14n` | `max4_le_261`, `depth1_ceiling` | PROVED | tightening of 285 (`max4_le_285`), [P401](LEDGER.md#p401) |
| `max(4) ≤ 285` | `max4_le_285` | PROVED | no hypothesis; anchored by an independent exact counter equal to the engine on 17 configurations ([P399](LEDGER.md#p399)) |
| `max(4) ≤ 194 + c₂`, so 195 | `max4_le_195_charging` | PROVED IF `c₂ = 1` | scope: no shared face plane; `X = 0`, `W4u = 0` by the circle lemma ([P404](LEDGER.md#p404), [P405](LEDGER.md#p405)) |
| general-n bound, exact at n = 2, 3 | `per_set_closed_form` | PROVED | the induction on `|B|`; anchored at n = 5 ([P400](LEDGER.md#p400)) |
| `max(4) ≤ 953` | `total_le_953` | PROOF GAP | depth-2 premise refuted ([P274]) |
| every wall splits over ℚ | `Detq.lean`, 18 branches | identities kernel-checked | the wall polynomial is built in Lean from the rotation matrix; the matrix form, the exact division and the determinant are Lean's; three must-fail controls fail |
| 727's pattern isolated and unaugmentable | — | exact CAS re-run | `eliminate729.py`, sympy Gröbner, 2026-09-28: same result. Not kernel-checked (needs Gröbner cofactors) |

Every triple cap in the table carries its scope, pairwise transversality ([P397](LEDGER.md#p397)).

## The review list: project lemmas Lean takes on trust

Standard facts are not listed (Euler's formula with `c` components, the handshake lemma, Euler for a
convex polytope, "a convex set is connected", "a union of k convex sets has at most k components").

| lemma | source | used by | what to check |
|---|---|---|---|
| **ANCHOR** (Theorem 1): every component of `S_C(R)` contains a face-centre direction of C | max2_report.md §1, [P33] | max(2), max(3) both routes, Theorem S, `d_{n−1} ≤ 6n` | the "q_t lands in the same component U" step, flagged soft in PROOF_67's open item 2 |
| **FIB**: depth-(k−1) regions biject with components of a spherical set | PROOF_67 §2, PROOF_FORMAL B1 | max(2), max(3), Theorem S | "routine" in the source; convexity and O interior |
| **six-slab cover** `a, b ≤ 6` | PROOF_FORMAL A2, [P110] | max(3) MV route | |
| **six convex sectors** `m ≤ 6` | [P110] Addendum 2 | max(3) MV route | that each sector piece of the complement is convex |
| **Mayer–Vietoris + Alexander duality** `s ≤ a + b + m − 2` | [P110] | max(3) MV route | the standing hypotheses `a, b ≥ 1`, `U, C ≠ ∅` and the degenerate cases |
| **Step T's local inequality (◆)** and its summation | PROOF_STEP_T.md | `W ≤ 92`, the triple cap at n ≥ 4 | assumes pairwise transversality |
| **Part D1–D3**: contact degree = polytope vertex degree | PROOF_FORMAL Part D | `W ≤ 92` | assumes pairwise transversality |
| **triple points are bottom vertices** | PROOF_67 §5.3 | Lemma 1a | PROOF_67's own caveat: tangential triple points |
| **[P237] steps 2–4**: three-body gain, two-body gain, "adding cubes only deletes outer vertices" | [P237] | `d₁` bound, the pair cap `E_i ≤ 10` everywhere | whether the weight form `EE + 2·SC2` assumes transversality ([P397]) |
| **[P56] (I)–(V)** | [P56] | increment | |
| **Theorem S, Lemmas 2 and 3** | PROOF_SUBSET.md | Theorem S | pure set and partition combinatorics: formalisable in full with Mathlib |
| **the level identity** `d_ℓ = E_ℓ − V_ℓ + c_ℓ + 1` | [P243] | tower, `d₁` bound | |
| **the excess accounting** `sum(E − V) ≤ T + two-body` | [P326], [P388] addendum | tower | ARGUED, recorded as not verified |
| **the wall polynomials** W4, W3 | [P104] | wall splitting | that they are the right geometric conditions |
| **DEPTH**: depth-A regions biject with components of `{max_A M < min_B M}` | [P399] | `max(4) ≤ 285` | the radial fibre argument, ties included; tested against the engine on 17 configurations |
| **LOCAL COINCIDENCE**: near a two-body vertex, or a triple point whose fourth cube does not contain it, the level-2 boundary equals a triple's bottom diagram | [P404] | `max(4) ≤ 194 + c₂ + …` | same degree; checked on every vertex of 210 configurations |
| **CIRCLE LEMMA**: at a point p, all active facet normals of all cubes project onto one circle; top-diagram switches inject into colour changes | [P405] | `X = 0`, `W4u = 0` | the exactness of the local model; the no-tie argument; tested with a must-fail control |
| **PIECES**: those sets and their complements are unions of convex pieces, one per active face | [P399] | `max(4) ≤ 285` | convexity of `{M_a < t.u}` on a sector; pointedness |
<!-- reviewed 2026-09-28: cites the parts of P237, P243 and P326 that stand, with their conditions in the table -->

## What this pass found

1. **The Euler route to max(3) assumes a connected top diagram.** PROOF_67 §5: "for a cellular
   graph on S²". Not proved. max(3) = 67 is unaffected: the Mayer–Vietoris route needs no such
   assumption, and no transversality either.
2. **[P237]'s `+ 2` assumes `c₁ = 1`.** Its own step 1 carries `c`; the published bound dropped it.
3. **The triple cap lost its transversality scope when lifted to every n** ([P397](LEDGER.md#p397)).
4. **Stale labels**: PROOF_67's "CANDIDATE PROOF" for the contact bound (completed in
   PROOF_FORMAL); RESULTS filed the merge law, a verified identity, among the proofs.
5. **`detq_check.py` did not run** (a variable used before its definition); fixed, and it reproduces.
