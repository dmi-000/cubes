# Plan: two sliding 3-cube triples — overlay, slide, and relative-rotate

For a Sonnet agent. Read first: six_cube_search_results.md Postscripts
4–8, MULTIWALL_SPEC.md + multiwall_report.md (methods: constraint-first
search, snap-and-verify, tower verification via qtower.py), golden_six.py
(golden five matrices; wrapper into certify_six.exact_count_config).
Records to beat: overall 681, rational 655, rational-random 635. Rules
as always: validated files + exact_search_results.jsonl untouched; write
to slide3_report.md and slide3_search.jsonl only (ledger is merged by
the main session); ≤4 cores; honest negatives welcome.

## 0. Pin down the family (user's premise — VERIFY, do not assume)

User: "A family of maximal 3-cube configurations can continuously slide
between the octahedral compound of 3 cubes and 3 cubes inscribed in a
dodecahedron."

Candidate family: C(θ) = { R_x(θ)·cube, R_y(θ)·cube, R_z(θ)·cube }
(each cube rotated by the SAME angle about a different coordinate
axis; try sign/orientation variants — e.g. alternating senses — if the
plain version fails the checks below).

- Check O: at θ = 45°, C(θ) should be the classical octahedral compound
  of three cubes (each cube invariant under 90° about its own axis, so
  distinct orientations of R_a(θ) have period 90°; 45° is the symmetric
  midpoint).
- Check D: find θ* with C(θ*) congruent (up to ONE global rotation) to
  a 3-subset of the golden five (our golden triple counts 67 —
  Postscript-5-era certified value). Congruence test, exact: compare
  the multiset of pairwise relative-rotation traces tr(R_i R_jᵀ)
  against the golden triple's. Numerically locate θ*, then identify it
  (expect a golden value — try tan θ* ∈ {1/φ, φ−1, 2−φ, 1/φ², …} and
  verify symbolically; entries may need ℚ(√5) or a quadratic tower —
  use qtower.py to verify exactly).
- Check M (the "maximal family" claim): exact count of C(θ) along the
  slide. Rational θ via half-angle quats: (q,p,0,0)/(q,0,p,0)/(q,0,0,p)
  gives rotation about x/y/z by θ with tan(θ/2) = p/q — FULLY RATIONAL
  configs, so the fast C++ engine `./cube_regions --quats` (~80 ms)
  applies. Sample θ densely in (0°, 90°); record the count profile
  (is it constant? plateau structure? value vs golden-67 and vs the
  octahedral endpoint, which needs ℚ(√2) — count it exactly with a
  Qd/qtower instance over √2). If C(θ) is NOT maximal along the way or
  the family doesn't hit the golden triple, say so plainly, correct
  the family if a small variant works, and continue with whatever the
  true sliding family is.

## 1. The overlay search (the actual task)

Configuration space: two triples, X(θ₁, θ₂, R) = C(θ₁) ∪ R·C(θ₂),
R ∈ SO(3). 5 parameters (+ discrete variants: which axis-frame the
second triple slides in before R). Everything rational when θᵢ are
half-angle-rational and R is an integer quat: second-triple quats are
Hamilton products r∘(q,p,0,0) etc. — still integer quats. Keep
components modest and gcd-reduce so the engine's |c| ≤ 512 cap holds;
where products overflow the cap, fall back to the Python oracle path
(certify_six) for those evals and note it.

- Gate S1: θ₁ = θ₂, R = identity ⟹ coincident triples: count must
  equal the single triple's count (coincidence machinery).
- Gate S2: one eval cross-checked C++ vs Python oracle (same total +
  histogram).

Search protocol (log EVERYTHING to slide3_search.jsonl: θ-quats, R,
total, by_depth):

- P1 (coarse map): grid over (θ₁, θ₂) — say tan(θ/2) = p/q, q ≤ 8 —
  × a coarse R-grid (integer quats, small components, include
  symmetric candidates: identity-adjacent, 60°-about-(1,1,1),
  90°-about-face-axis, and the golden relative rotations tr-matched
  to the five-compound's pair relations). This is cheap at 80 ms/eval:
  ~10⁴–10⁵ evals is fine within the core cap.
- P2 (climb): exact hill-climbing from the top ~20 of P1, moving all
  free integers (p₁,q₁,p₂,q₂ and R components) by ±1/±2, gcd-reduce.
- P3 (alignment walls, constraint-first): impose the known-good pair
  relations BETWEEN the two triples — a 60°-shared-body-diagonal
  relation (built 655), a shared (1,1,1)-type 3-fold axis (built 681)
  — and slide (θ₁, θ₂) within each imposed wall.
- P4 (snap-and-verify): watch P2 trajectories for component-ratio
  convergence to surds (the multiwall M2 machinery); verify snapped
  points with qtower.py.

## 2. Map the landscape for handover (explicit user requirement)

The report must leave the search space CHARTED, not just scored:

- a (θ₁, θ₂) heat table (best-over-R count per cell) — text table is
  fine — marking the octahedral corner, θ* (golden) line, and diagonal;
- for each promising region: its location (parameter ranges), best
  config (quats), count + histogram, which alignment constraint (if
  any) is active, whether it touches a wall needing √2/√5/tower, and
  the natural NEXT move for a follow-on agent (finer grid? impose the
  wall exactly? climb?);
- a "dead regions" list with one-line reasons, so future searches skip
  them;
- open-questions section sized for a fresh Sonnet agent to resume from
  slide3_report.md + slide3_search.jsonl alone.

## 3. Context numbers (for calibration, all exact)

n=3 golden triple 67; n=6 records 681 (golden five + (1,1,1)-axis
sixth), 655 (two 60°-diagonal pair walls, rational), 635 (rational
random+climb, 360k seeds); deep ceilings d3 ≤ 164, d4 ≤ 102, d5 ≤ 36
never exceeded anywhere — flag immediately any config violating them;
d1 record 238. mod-4: generic totals ≡ 3 (mod 4) at n=6; wall configs
may deviate (681 ≡ 1). Two overlaid TRIPLES with internal symmetry are
wall-like — deviations expected, not bugs (but d6 must always be 1 and
totals odd unless something is genuinely degenerate).
