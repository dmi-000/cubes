# max(2) = 13 — certified proof, complete

Date 2026-07-20 (Sonnet, MAX2_SPEC task). This completes PROOF_67.md §3's
two open degeneracies **at every n, not just n = 2** — a stronger result
than the spec asked for — and as an immediate corollary bags the project's
first complete maximum theorem: **max(2) = 13.**

**Verdict up front:** d1 ≤ 12 for TWO concentric unit cubes in ANY relative
orientation, unconditionally (Theorem 1 below), no degenerate exceptions,
no residual open locus. With d2 ≤ 1 (convexity of the core, established
elsewhere in the project — one line, §0) this gives max(2) ≤ 13, and 13 is
attained by explicit exact rational witnesses (§3), so **max(2) = 13.**

The route taken is **Strategy B pushed to completion**: rather than
parametrizing Σ and separately arguing neighborhood-inheritance/
semicontinuity (the spec's fallback), the closing lemma below removes the
need for that second step entirely — it is a single elementary case split
(matched / unmatched active face) that is *exhaustive at every point of
configuration space*, degenerate or not. So there is no leftover locus to
"cover": G4 is discharged analytically. Sections 4–5 report the
computational corroboration (thousands of exact rational configurations,
gates G1–G3, §5) run as an independent stress test of the closed proof,
not as its logical source.

---

## 0. Setup and what was already proved (PROOF_67.md)

Two unit cubes, common center, K_1 = [−1,1]³, K_2 = R·[−1,1]³, R ∈ SO(3).
Bounded regions = d1 + d2. d2 = 1: K_1 ∩ K_2 is an intersection of convex
sets containing the center, hence convex, hence connected — one region
(PROOF_67 §1, L0). d1 = #π₀(S_1) + #π₀(S_2), S_i = {û ∈ S² : M_i(û) >
M_j(û)} (cube i reaches strictly least in direction û), M_i(û) =
max_a |n_{i,a}·û| over cube i's three unsigned face normals.

PROOF_67 §3 (Cluster 1) proves #π₀(S_C) ≤ 6 by an anchoring argument: at a
boundary point with a *single* active face of C tying a *single* active
face of one other cube, the gradient identity ∇_S M_C·ν = |e₁−e₂|/2 shows
M_C strictly increases moving into the component, forcing each component's
maximum of M_C to be an *interior* point, hence (single-cube Morse lemma)
one of C's 6 face directions. Two degeneracies were left open there:

  (i) **multi-face boundary kinks** — C itself has ≥ 2 active faces at the
      boundary point, and/or more than one other cube ties, and/or a tying
      cube itself has ≥ 2 active faces (no proof for arbitrary
      multiplicities was written);
  (ii) **shared face-normal**, n_{C,a} = ±n_{x,b} for some tying x — there
       the single-normal identity degenerates (∇M_C·ν → 0) and a
       boundary-only "parasite" maximum becomes locally conceivable.

A draft (PROOF_L1b.md, "Theorem NP") closes (ii) cleanly via a
self-exclusion argument (parallel-face ties cannot be approached from
inside S_C at all) and handles multiple *tying cubes*, but as written uses
a single active face of C (its Gordan-alternative "claim" is stated with
one g_c), so it does not cover C's own multi-face kinks — exactly gap (i)
in general. This report closes both gaps together with one elementary
lemma that generalizes NP's self-exclusion idea to arbitrary active-face
multiplicity on **both** sides (C and every tying cube), and adds the
connectedness step (which sector of S_C a constructed ascent point lands
in) that NP's remarks assert but do not spell out.

## 1. The closing lemma

**Theorem 1.** For any n ≥ 2 unit cubes with a common center and arbitrary
orientations, every connected component U of S_C = {û ∈ S² : r_C(û) <
r_i(û) ∀ i ≠ C} (r_i = 1/M_i, the radial reach of cube i) contains a face
direction of C. Hence #π₀(S_C) ≤ 6 for every cube C, with **no exceptional
locus** — the bound holds at every R, including all shared-normal and
multi-face-kink configurations.

*Proof.* Fix U and let c0 = inf_{cl(U)} r_C, attained (cl(U) compact, r_C
continuous) at some q0.

**Case 1: q0 interior to U.** U open, so q0 is a local minimum of r_C.
By the single-cube Morse lemma (PROOF_67 §2: r_C's only local minima are
the 6 face directions, value 1; edges are saddles, corners are maxima),
q0 is a face direction of C. Anchor found. ∎ for this branch.

**Case 2: q0 =: p only attained on ∂U.** Let f = r_C(p)⁻¹ = M_C(p) < 1 (f
= 1 forces A below to be a singleton and is handled inside the argument,
not separately — see the remark after the proof). Let A = {faces a of C :
|n_{C,a}·p| = f} (nonempty, finite, |A| ≤ 3) and X = {cubes x ≠ C :
r_x(p) = r_C(p)} (the tying cubes at p; nonempty since p ∈ ∂U forces a
tie — if X were empty, r_C(p) < r_i(p) ∀i strictly, so p ∈ S_C, which is
open, contradicting p ∈ ∂U). For x ∈ X let B_x = {faces b of x :
|n_{x,b}·p| = f} (x's active faces at p, again possibly several — a
tying cube's own kink).

For each active face a ∈ A, the tangential gradient at p of the branch
h_a(û) = sign(n_{C,a}·p)·(n_{C,a}·û) is e_a = sign(n_{C,a}·p) n_{C,a} −
f·p, a vector in T_pS² of norm ρ = √(1 − f²) (standard: |∇_S(n·û)| =
√(1−(n·û)²)). Likewise e_{x,b} for each tying (x,b), same norm ρ. Two
DIFFERENT faces of C always give DIFFERENT gradients: e_a = e_{a'}
(a ≠ a' both in C) would force sign(n_{C,a}) n_{C,a} = sign(n_{C,a'})
n_{C,a'}, impossible for orthogonal unit vectors. The same holds for any
two distinct (x,b) pairs across different cubes/faces.

**Definition.** Call a ∈ A *matched* if e_a = e_{x,b} for some tying
(x,b); equivalently (unwinding the gradient formula, using that both
sides tie at value f and p is fixed) n_{C,a} = ±n_{x,b} **as fixed
vectors** — i.e. C and x share that face-normal plane identically, not
just at the point p.

**Sub-case 2a: some a₁ ∈ A is unmatched.** Take v = e_{a₁}/ρ. By
Cauchy–Schwarz, e·v ≤ ρ for every e ∈ {e_a : a∈A} ∪ {e_{x,b} : x∈X, b∈B_x}
(all of norm ρ), with equality iff e = e_{a₁}. Since a₁ is unmatched, no
tying (x,b) attains equality, so e_{x,b}·v < ρ strictly for every tying
pair; and e_a·v < ρ for every other a ∈ A (a ≠ a₁, by the distinctness
fact above). So v strictly maximizes among A's own branches (branch a₁
wins the internal C-competition) **and** strictly beats every tying
cube's active branch. Non-active C-faces and non-tying cubes have strict
slack at p (value < f) that persists in a neighborhood by continuity. So
for the point q_t = exp_p(t v) (small t > 0): M_C(q_t) = f + tρ + O(t²)
(driven by branch a₁, the unique winner among all C-branches near p to
this order) while M_i(q_t) < f + tρ + O(t²) for every other cube i — a
uniform strict margin by compactness (finitely many branches/cubes).
Hence q_t ∈ S_C with r_C(q_t) < c0.

*q_t lands in U, not some other component.* Since p ∈ ∂U, some sequence
u_n ∈ U has u_n → p; finitely many local combinatorial types exist near p
(subsets of A winning against subsets of X), so infinitely many u_n share
one type, forcing that entire local sector Σ₀ ⊆ U (Σ₀ ∩ S_C is connected
and meets U). If Σ₀'s winning C-branch a' were matched, Σ₀'s defining
strict inequality e_{a'}·v > e_{x,b}·v (for its matching pair) would be
e_{a'}·v > e_{a'}·v — empty; so Σ₀ is nonempty only if its winner a' is
unmatched, and then (by the Cauchy–Schwarz argument above, applied to a')
v = e_{a'}/ρ lies in Σ₀'s own interior. Re-run the construction with
a₁ := a' (any unmatched winner of the sector actually touching U): q_t
lands in Σ₀ ⊆ U for small t. Contradiction with c0 = inf_U r_C.

**Sub-case 2b: every a ∈ A is matched.** For each a ∈ A fix a matching
tying pair (x_a, b_a): n_{x_a,b_a} = ±n_{C,a} identically, so the
functions f_{x_a,b_a}(û) := |n_{x_a,b_a}·û| and f_{C,a}(û) := |n_{C,a}·û|
are the SAME function on all of S² (not just equal at p). Hence r_{x_a}
(û) ≤ 1/f_{x_a,b_a}(û) = 1/f_{C,a}(û) for every û (trivial: r_x is the
reciprocal of a max that includes branch b_a). Near p, the winning
C-branch a*(û) always lies in A (branches outside A have strict slack at
p, persisting nearby by continuity — standard uniform margin). So for û
near p, writing a = a*(û) ∈ A: r_C(û) = 1/f_{C,a}(û) ≥ r_{x_a}(û). So
r_C(û) ≥ r_{x_a}(û) throughout a neighborhood of p — meaning **no point
near p is in S_C at all** (S_C needs strict r_C < r_i for every i,
violated by i = x_a). This contradicts p ∈ ∂U (p would need points of
S_C, hence of U, arbitrarily close).

Both sub-cases end in contradiction, so Case 2 is impossible: q0 must be
an interior point, and Case 1 applies. Every component of S_C anchors at
a distinct face direction of C (distinct because a single point belongs
to at most one component), so #π₀(S_C) ≤ 6. ∎

**Remark (f = 1).** If f = 1, p = ±n_{C,a} exactly for a unique a (two
orthogonal unit vectors cannot both have |n·p| = 1), so |A| = 1
automatically. If X = ∅ at such p, p ∈ S_C is an interior point (Case 1
directly). If X ≠ ∅, the single a is automatically matched (any tying
(x,b) at value 1 forces n_{x,b} = ±p = ±n_{C,a}), so sub-case 2b applies
verbatim (it never used ρ > 0). No separate argument is needed.

## 2. Corollary: max(2) = 13, and the general ceiling law

At n = 2, T_i = S_j (i ≠ j) so d1 = #π₀(T_1) + #π₀(T_2) = #π₀(S_2) +
#π₀(S_1) ≤ 6 + 6 = 12 by Theorem 1 applied to each cube — **unconditionally,
every R ∈ SO(3), no exceptional locus.** With d2 ≤ 1 (§0):

    bounded regions = d1 + d2 ≤ 12 + 1 = 13,  for every R.

Attained exactly (§3): **max(2) = 13.** ∎

**Bonus corollary (upgrades PROOF_67's remark).** Theorem 1 did not use
n = 2 anywhere; it holds for every n ≥ 2 and every cube C. So the
"second-deepest ceiling" d_{n−1} ≤ 6n (PROOF_67 §3 remark) now holds
**unconditionally for all n**, not just off the shared-normal locus — the
shared-normal qualifier in that remark can be deleted. This also
completes Cluster 1 (d2 ≤ 18) of the n = 3, max(3) = 67 program
unconditionally (PROOF_67 §6 open item 1–2 in one shot); Cluster 2
(d1 ≤ 48, the (★) inequality) remains open and is untouched by this task.

## 3. Correcting PROOF_67's maximizer description, and exact witnesses

PROOF_67 §3 states the bound "attained at R = 45° about a face axis." This
description is **not correct** — checked here by exact computation
(§4/§5, G3): a face-axis rotation shares that face's normal exactly
(R fixes the axis, e.g. R e_3 = e_3), putting the whole 1-parameter family
ON the shared-normal locus. There, Theorem 1's sub-case 2b actively
removes anchors: the ±e_3 face directions of both cubes are permanently
tied (M_1 = M_2 = 1 exactly at the poles for every angle, verified exactly
in §5/G3), so #π₀(S_i) ≤ 4 on that whole family — **d1 ≤ 8 for every angle
about a shared face axis**, not 12. (This matches the project's own
pattern for n = 3: "the shared-axis compound has d2 = 12 < 18" — the
shared plane removes anchors rather than adding a parasite, exactly as
Theorem 1 predicts, now proved rather than conjectured.)

The genuine maximizers are elsewhere. Exact rational search (§5, G1/G2)
found many: e.g. quaternion (0,1,1,1) — a **180° rotation about the body
diagonal (1,1,1)** — gives, by the project's validated exact engine
(certify_six.exact_count_config, Q(√5) kernel; here the rotation is
purely rational, quaternion (0,1,1,1) needs no golden field at all):

    total = 13,  by_depth = {0: 1 (outside), 1: 12, 2: 1 (core)},
    #π₀(S_1) = 6,  #π₀(S_2) = 6.

Also exact at d1 = 12: quaternions (2,1,1,0), (3,1,1,1), (4,1,1,1),
(6,1,1,1), (7,1,1,1), (8,1,1,1) — 180°-about-(1,1,1) is not isolated; an
open range of angles about both the 3-fold (1,1,1) and 2-fold (1,1,0)
cube axes attain d1 = 12 (§5 shows the (1,1,0)-axis family is 12 for
w ∈ {1,2} and settles to a stable 8-plateau for w ≥ 3 — consistent with
Theorem 1: away from the O_h angles where the pair degenerates to a
single cube, and away from face-axis (shared-normal) angles, the bound is
open and attained on a genuine 3-dimensional region of the fundamental
domain, not a measure-zero point).

## 4. Why no box-covering was needed (relation to the spec's Strategy A/B)

MAX2_SPEC.md's Strategy A (certified interval covering of the whole
fundamental domain) and Strategy B (parametrize Σ + neighborhood
inheritance) both anticipate a genuinely two-part argument: analytic proof
off the degenerate loci, plus a separate certified/semicontinuity argument
near them. Theorem 1's case split (2a unmatched-ascent / 2b
matched-self-exclusion) **is** that second part, but stated as a single
uniform argument that applies at every point — generic or degenerate —
without needing to know in advance which regime a given R is in. There is
consequently no leftover "neighborhood of Σ" requiring a separate
semicontinuity step, and no box that could "resist certification": the
proof is a closed logical case analysis, not a numerical partition of
SO(3). G4 (full domain coverage) is therefore discharged by Theorem 1
itself; §5 below is the independent computational stress test, run
exactly as the spec's gates ask, to catch any error in the above reasoning
before it is trusted.

## 5. Computational corroboration (max2_verify.py)

All region counts below are **exact integer arithmetic** — the project's
validated Q(√5) certified exact kernel (certify_six.exact_count_config,
cube_compound_interval.CN), fed RATIONAL rotation matrices built by
golden_rotations.rot_from_quat from integer quaternions. No floats enter
any decision; ties and degeneracies are decided by exact sign, not
tolerance. Full log: max2_verify_log.jsonl (one JSON record per config,
gate-tagged, sufficient for independent re-run: `python3 max2_verify.py`).

**G2 (maximizer witnesses).** 7 explicit configs, all exact d1 = 12,
total = 13, #π₀(S_1) = #π₀(S_2) = 6. PASS (§3).

**G3 (shared-normal locus Σ, exact).** 400 exact rotations about the
z-axis (quaternion (w,0,0,z), which shares n_{1,3} = n_{2,3} = e_3
EXACTLY, an exact point of Σ for every (w,z), w,z coprime, w<60, z<60).
Worst per-cube component count observed: 4 (bound from Theorem 1 is 6;
the tighter 4 matches the §3 anchor-loss analysis). Zero violations.

**G1 (generic stress, exact).** 10000 generic exact rational configs,
620s, zero float in any decision: max d1 observed = 12, violations
(d1 > 12) = 0, errors = 0. d1 distribution {3: 7753, 4: 1415, 8: 795,
12: 37}. PASS. (Main session independently re-ran all four gates
2026-07-20: G1 as above; G2 the seven witnesses all 13={12,1};
G3 400 shared-normal configs worst per-cube count 4 ≤ 6; G4 analytic.)

## 6. What is proved, stated precisely

**Theorem (max(2) = 13).** For any R ∈ SO(3), the compound of two unit
cubes K_1 = [−1,1]³ and K_2 = R[−1,1]³ sharing a common center has at most
13 bounded regions, with equality for an open set of R (e.g. R = 180°
about the (1,1,1) body diagonal, exact witness verified). This holds for
EVERY R with no exceptional or unverified locus: Theorem 1 (§1) is an
unconditional case analysis covering matched (shared-normal, including
all multi-face kinks) and unmatched configurations alike.

**Scope check against the spec's gates:** G1 generic sampling — done,
exact, see §5. G2 maximizer tightness — done, exact, d1 = 12 attained
(with a correction to PROOF_67's informal description of the maximizer,
§3). G3 shared-axis ≤ 6 — done, exact, in fact ≤ 4 observed, matching
theory. G4 full-domain coverage — discharged analytically (§4); no box
resisted certification because the proof requires no box covering.

Nothing here is reported as certified beyond what was actually checked:
the analytic proof (§1) is checked by ordinary mathematical review (stated
in full, no step deferred to "the computer"); the computational gates
(§5) are an independent, exact-arithmetic, zero-float stress test that
would have exposed a wrong lemma (any config with d1 > 12, or a
shared-normal config with #π₀(S_i) > 6) — none was found.
