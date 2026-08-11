# MAX2_SPEC — a certified proof that max(2) = 13

Task for the implementing agent (Sonnet, with care — this is a
proof-grade computation, not a heuristic search). Background:
PROOF_67.md (the analytic argument this completes — READ IT), C45_notes.md
§§10,13,15, certify_six.py / cube_compound_interval.py (the validated
certified-interval counter — REUSE its interval machinery). Ledger and
validated files READ-ONLY. ≤4 cores; detached; the goal is a rigorous
computer-assisted theorem, so correctness and honest error bars dominate
speed.

## The claim and what is already proved analytically

Two unit cubes, common center, K_1 = [−1,1]³, K_2 = R·[−1,1]³, R ∈ SO(3).
Bounded regions = d1 + d2, d2 = 1 (core, convex — PROVED), d1 =
#π₀(S_1) + #π₀(S_2) where S_i = {û ∈ S² : M_i(û) > M_j(û)} (cube i
reaches strictly least in direction û), M_i(û) = max_a|n_{i,a}·û|.
PROOF_67.md §3 proves **#π₀(S_i) ≤ 6, hence d1 ≤ 12 and max(2) ≤ 13**,
for every R OFF the shared-normal locus, by: at any boundary point of a
component with single active/tie faces, ∇M_i·ν = |e₁−e₂|/2 > 0 (the
into-component normal ν = (e₁−e₂)/|e₁−e₂|, equal gradient norms), so the
max of M_i over the component's closure is interior = a face direction
(single-cube Morse), one per component, ≤ 6. Attained at R = 45° about a
face axis (13 = 1 + 12).

**The ONLY gaps are two codimension-≥1 degeneracies** (PROOF_67.md §3):
(i) multi-face boundary kinks; (ii) shared face-normals n_{1,a}=±n_{2,b}
(there ∇M_i·ν can vanish and a boundary-only "parasite" max becomes
locally possible). This task discharges both by a certified computation,
completing the theorem.

## Reduction to a bounded certified check

Configuration space is R ∈ SO(3) modulo O_h × O_h (octahedral symmetry
on each cube) — a compact 3-manifold; take an explicit fundamental
domain (e.g. Rodrigues/quaternion chart with the standard O reductions).
The analytic proof already covers the OPEN dense complement of the
degenerate loci; the certified job is only NEIGHBORHOODS of:
  - the shared-normal locus Σ = {R : some n_{1,a} = ±R n_{2,b}} (finite
    union of 2-D subvarieties), and
  - the kink locus where a component boundary passes through a point with
    ≥3 simultaneously active faces.
Two acceptable strategies, in preference order:

**Strategy A (verify the conclusion directly, everywhere).** Cover the
fundamental domain with boxes; on each box, rigorously certify
#π₀(S_i) ≤ 6 for i=1,2. The clean certifiable proxy: by the analytic
lemma a component fails to anchor only if M_i has a boundary-only
supremum, which requires ∇M_i·ν = 0 somewhere on ∂S_i, i.e.
|e₁−e₂| = 0 with the active faces tying — a shared-normal event. So it
SUFFICES to certify, on each box of R-space, EITHER (a) the box is
disjoint from Σ AND every component of S_i (for the box's fixed
combinatorial type) anchors — via interval evaluation of M_i and its
gradient showing strict inward increase on all tie arcs — OR (b) the box
meets Σ and a direct exact/interval count on that box gives #π₀(S_i) ≤ 6.
Adaptive subdivision near Σ.

**Strategy B (the degenerate loci, parametrized).** Prove the generic
bound analytically (already done), then treat Σ as a lower-dimensional
family: parametrize shared-normal configs (fix the shared axis, one
remaining relative angle → a 1-parameter family per normal-pairing),
and on that family certify #π₀(S_i) ≤ 6 by interval arithmetic over the
1-D parameter × the sphere, plus a transversal argument that a
neighborhood of Σ inherits the bound (semicontinuity of the component
count away from Σ). Lower-dimensional, cheaper, but the neighborhood
inheritance step must be made rigorous, not assumed.

Use whichever you can make airtight; A is more uniform, B is cheaper.

## Interval machinery

Reuse cube_compound_interval.py's certified-numeric core (CN intervals
with exact rational endpoints and refinement). All box evaluations of
M_i, ∇_S M_i, tie conditions must be OUTWARD-rounded interval
computations; a certified "≤ 6" on a box means the interval logic
excludes any 7th component with certainty. Exact zeros (on Σ) handled
symbolically (rational R on Σ → exact arithmetic). NO bare floats in any
decision.

## Gates

G1: on a random SAMPLE of ~10⁴ generic R, the interval method's
    #π₀(S_i) equals a direct exact count (certify_six per-label logic
    restricted to the two cubes) — zero disagreements.
G2: at the maximizer R=45°-about-face-axis, certify d1 = 12 (the bound
    is attained, so the method must not under- or over-count there).
G3: the shared-axis (common face-normal) config certifies #π₀(S_i) ≤ 6
    (in fact the analytic evidence says fewer) — the degenerate case the
    proof must survive.
G4: the whole fundamental domain is covered (report box count, max
    subdivision depth near Σ, total wall-clock) with ZERO boxes failing
    the ≤6 certificate. Only then is the theorem proved.

## Deliverables

max2_report.md (the certificate: strategy, fundamental domain, box
statistics, the handling of Σ, and the explicit statement "d1 ≤ 12
certified over the entire fundamental domain, hence max(2) = 13"),
max2_verify.py, and a machine-checkable log of the covering (boxes +
verdicts) sufficient for an independent re-run. If any box resists
certification, report it precisely rather than declaring success — a
partial covering with a named uncertified region is a valid, honest
outcome. Never edit the ledger or validated files.
