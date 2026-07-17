# RESONANCE4 report — cross-class coincidence resonances of the n=4 dihedral family, solved algebraically

Executes `RESONANCE4_SPEC.md`. **Verdict up front: no n=4 family resonance
found reaches 183, or even the 175 family plateau.** The best exactly-counted
resonance is **151** = {d1:68, d2:58, d3:24, d4:1} in ℚ(√5) at the
rational-tangent tilt tanψ=2 (≡ tanψ=1/2 in the fundamental domain). At n=4,
cross-class coincidence alignment is count-NEGATIVE across the board — like
the face-diagonal point at n=3 (49 < 55), not like the octahedral spike
(67 > 55). Record protocol not triggered (nothing ≥ 183; nothing > 175).
Coverage caveats below (a set of degree-4 candidates remains open, exactly
per spec's "do not approximate" rule).

## 1. The cross-class conditions, exactly (and GATE R1)

Setup: Rel gauge (Theorems M/P/F, C45_notes.md §12). Cube 1 = I, cube k =
Rel(θ_k, ψ). Pair structure depends only on (Δ = θ_k−θ_j, ψ). Variables
cD=cosΔ, sD=sinΔ, cP=cosψ, sP=sinψ with the circle relations c²+s²=1.

For each ordered cross-class type (edge of class a on cube A vs class b on
cube B, a≠b) there are 16 label pairs. Sympy derivation (Groebner normal
form modulo the two circle relations; `derive2.py` logic reproduced in
`resonance4_solve.wl`) gives, per type, **8 distinct coplanarity polynomials
up to overall sign** (the 16 label pairs fall in antipodal pairs — the
central symmetry of either cube). Representative polynomials (label signs
A=(−1,−1), B=(−1,−1)):

```
g_xy(Δ,ψ) = 2·cD·sP² − cD + cP·sD − sD·sP − 2·sP² + 1
g_yz(Δ,ψ) = −cD·cP·sP + cD·sP² + cD − cP·sD + cP·sP − sP² + 1
g_xz(Δ,ψ) = sP · (cD·cP − cD·sP − cP − sD + sP)      [sP=0 factor dropped:
             the nontrivial branch is the degree-1-in-(cD,sD) factor]
```

Structural facts established symbolically:

- **Swap symmetry**: the (b,a) representative equals the (a,b) one with
  Δ → −Δ (sD → −sD), exactly. So each unordered pair contributes one curve
  per class *per orientation*; orientation matters (the polynomials are not
  even in sD).
- **Within a type, the 8 sign-variants are NOT one curve** — they are 8
  branches exchanged by the label symmetries; each is linear in (cD,sD),
  so for fixed ψ each variant has ≤ 2 roots in Δ. (The n=3 evidence "all
  four y-z extras share one curve" refers to the four *specific* labels
  active at the octahedral point — those four residuals are related by the
  sign flips (sA,sB) → (−sA,−sB) and lie pairwise on two curves meeting at
  the octahedral point; verified: all four vanish there.)
- **GATE R1 (PASS, exact)**: substituting Δ=120° (cD=−1/2, sD=√3/2):
  - g_yz vanishes at ψ = arcsin(1/√3): sympy `simplify` → 0 exactly, and
    independently wolframscript `FullSimplify` → 0.
  - g_xz vanishes at ψ = arctan(φ²): both engines → 0 exactly.
  Additionally the *other* member of the yz antipodal family also vanishes
  at the octahedral point (the two curves crossing there), matching
  Postscript 25-addendum-2's rank-2 Jacobian observation. Reduction of the
  second yz-variant modulo the ideal ⟨g_yz, circles⟩ leaves
  2(cD·sP² + cD − sP² + 1) ≠ 0 — the two variants are genuinely different
  curves that happen to intersect at (120°, 35.264°).

Tracing g_yz's Δ(ψ) branch through the octahedral point reproduces the
known pair-curve: Δ(35.264°)=120°, Δ(45°)=109.471° (the tetrahedral angle —
the psi=45 wall of Postscript 25 addendum 4), Δ→90° as ψ→90°.

## 2. GATE R2 (PASS)

Fresh field-engine ladder, bottom rung: a *generic* ℚ(√d) engine
(`resonance4_solve.py: make_qd(d)` + `exact_count_field`) built by the
six-replacement recipe from the validated read-only `slide3_q2.py`
(automated as a class factory: the two D's in mul, two in div, two in the
sign discriminant, plus float/repr cosmetics). With d=2 on the octahedral
triple (Rx45/Ry45/Rz45): **total=67, depth {1:48, 2:18, 3:1}** — exactly
the ledger's octahedral 67 and exactly slide3_q2.py's output. PASS.

C++ rung sanity: `cube_regions_n --quats` reproduces 63 = {44,18,1} on a
rational n=3 chain (cross-checked earlier in nfamily_gates G1).

## 3. Resonance systems at n=4

DOF = 4 (θ₂,θ₃,θ₄,ψ). k=4 conditions ⇒ 0-dimensional (isolated) systems;
k≤3 gives positive-dimensional families (recorded as such, not enumerated —
they are curves/surfaces of configurations, not isolated resonances).
Variables (c2,s2,c3,s3,c4,s4,cP,sP) with 4 circle relations; each condition
is one g_type on one pair's (cosΔ,sinΔ) (exact polynomial after the angle
subtraction formulas). Solved with wolframscript `Solve[..., Reals]`
(Groebner-based) per system, 25–30s time limit each.

**Sweep A (uniform)**: all 15 four-subsets of the 6 pairs × 6 oriented
types (xy,yz,xz,yx,zy,zx) = 90 systems. 46 solved exactly, 44 hit the time
limit (all timeouts in the xy/yx class and a few xz/zx — the quadratic-in-cD
xy class produces the heaviest Groebner bases). 1152 real solutions with
sinψ>0.

**Sweep B (mixed orientation, targeted)**: the n=3 octahedral resonance is
itself mixed-orientation (Δ pairs 120,120,240: the 240 pair rides the
reversed curve g(cD,−sD)), so uniform sweeps structurally miss n=3-embedded
resonances. Systems: triangle {12,13,23} + fourth pair {k4}, orientations
mixed within class yz and within class xz, 3 fourth-pairs × 8 patterns
(halved by Theorem M's global mirror) × 2 classes = **48 systems, all 48
solved, zero timeouts**. 1104 real solutions.

After fingerprint dedupe (ψ mod 90, sorted θ mod 360): 187 + 198 unique
candidate points. Field census (unique points):

| field kind | uniform | mixed | countable now |
|---|---|---|---|
| rational | all at ψ≡0 (mod 90) — shared-axis degenerate | same | (degenerate) |
| single quadratic ℚ(√d) | 36 | 27 | yes — counted below |
| degree-4 nested / Root objects | ~151 | ~171 | **open** (see §5) |

Notably there are **no non-degenerate rational resonances** — every
resonance point is irrational, consistent with Theorem R's spirit.

## 4. Exact counts (every ℚ(√d) candidate, single-quadratic engine)

All 63 unique quadratic candidates were exactly counted (no floats in any
predicate). They collapse to a handful of congruence classes:

| ψ (exact) | tanψ | field | θ-structure (deg) | total | depth profile | vs plateau 175 |
|---|---|---|---|---|---|---|
| arctan 2 (63.435 ≡ 26.565) | **2 (rational!)** | ℚ(√5) | (−131.81, 96.38, −167.24) and variants | **151** | {68, 58, 24, 1} | **−24** |
| arctan 2 | 2 | ℚ(√5) | (−131.81, 96.38, 35.43) variants | 143 | {62, 56, 24, 1} | −32 |
| arctan 2 | 2 | ℚ(√5) | two cubes coincident (Δ=0 pair) | 57 | {24/26, 20/18, 12, 1} | (degenerate: 3 distinct cubes) |
| 45° | 1 | ℚ(√2) | θ's at multiples of 90 | 13, 1 | {6,·,6,1} / {·} | (degenerate: 90°-self-symmetry collapse, cf. Postscript 26's 93) |
| 135°≡45° | 1 | ℚ(√2) | mixed | 57 | {24–26, 18–20, 12, 1} | (one Δ=0 pair, 3 distinct cubes) |

Notes:

- **The best resonance, 151**, sits at the *rational-tangent* tilt tanψ=2
  (mirror-equivalent tanψ=1/2) — squarely in the Postscript-27
  rational-tangent family (tanψ=p/q ⇒ field ℚ(√(p²+q²)); here 2²+1²=5 ⇒
  ℚ(√5)). Exact witness (Rel gauge):
  cosψ=1/√5, sinψ=2/√5; (cosθ,sinθ) for cubes 2..4 =
  (−2/3, −√5/3), (−1/9, 4√5/9), (22/27, −7√5/27)
  [θ ≈ (−131.810°, 96.379°, −35.431°)]; system = pairs
  {12,13,23,24} all on the yz curve (uniform orientation). Its d3=24 and
  d4=1 match the record's deep layers exactly; the deficit is d1 (68 vs 92)
  and d2 (58 vs 66). **Two-engine agreement**: the generic-ℚ(√d) clone and
  the validated `certify_six.exact_count_config` oracle (independent code
  path, CN-interval + Q5 exact) both give 151 = {68,58,24,1} — beyond
  protocol requirements (< 183 would need none).
- 57-class entries have a coincident cube pair (the resonance systems don't
  forbid Δ_jk=0); they are exact counts of effectively-3-cube compounds and
  not competitive by construction.
- All ψ=45 solutions of the xz class are the known degenerate corner of the
  family (Postscript 25 addendum 4's ψ=45 resonance wall) — the counts (1,
  13) reflect θ's collapsing to multiples of 90°.
- Depth-profile constancy: every non-degenerate 4-cube resonance counted
  has d4=1 and d3=24 — the family-typical deep layers — reconfirming
  "deep structure conserved" pointwise on the resonance set.

## 5. Open candidates (higher-degree fields — reported, not approximated)

Per spec, these are NOT counted; minimal polynomials and structure only
(recorded in `resonance4_results.jsonl` with `status:"open"`):

| ψ (deg) | tanψ minimal poly | field notes | structure |
|---|---|---|---|
| 53.794 / 69.896 | 2t²−2t−1 (t=(1±√3)/2) | cosψ needs √(4±√3): degree-4 *nested*, not a ℚ(√a,√b) tower — outside the qtower D_LIST pattern | yz-class, θ ≈ (102.2, −155.6, 48.8) |
| 37.510 / 66.527 | 3t²−t−1 (t=(1±√13)/6) | ℚ(√13)-tangent (the record-tilt field of Postscript 27!), coordinates degree-4 nested | **chain** θ_k = k·a, a ≡ 200.891° — pairs {12,23,34,14} all on one zy curve |
| 12.666 / 24.203 | 2t²+4t−1 | √6-nested | yz-class |
| 38.173 / 51.827 | t⁴+t²−1 | golden-nested (t²=1/φ) | xz-class |
| 31.72 / 58.28 | 5s⁴−5s²+1 (s=sinψ) | pentagonal; many members have Δ=0 pairs | xz, θ at multiples of 72° |
| (assorted) | WL Root[quartics] | ~90 more unique points in the mixed sweep unparsed | — |

The ℚ(√13)-tangent chain candidate is the most interesting open point: it
is a pure chain (the n=4 analogue of the n=3 C₃ resonances), its tangent
field matches the n=4 record's own tilt field, and float triage ranks it
highest. But the triage voxel counter is demonstrably unreliable at these
resolutions (the known-175 config reads 246 at R=120, 215–262 at R≤400),
so no numeric count is quotable — an exact count needs a general
real-algebraic sign oracle (certified intervals over the degree-4 nested
field), listed as the natural next step.

Why these can't ride the existing ladder: qtower.py's pattern covers
ℚ(√a,√b) with *rational* a,b; here the second extension is √(4±√3) (a
non-rational radicand), i.e. a relative quadratic over ℚ(√3). The engine
generalization (sign via norm-form recursion over the base field) is
mechanical but new code with new correctness risk — out of scope under the
spec's "certified-interval only if straightforward."

## 6. Corner-contact (|t|=1) sweep — NOT DONE

Spec step 3 (secondary priority) was not reached within budget. The ψ=45,
θ=tetrahedral-angle vertex-vertex resonance is known count-negative at n=3;
its n=4 analogues remain unmapped.

## 7. Honest coverage

- Solved exactly: 46/90 uniform-type k=4 systems + 48/48 targeted
  mixed-orientation triangle systems. 44 uniform systems timed out at 25s
  (mostly xy/yx class — quadratic in cD, heaviest elimination); their
  *quadratic-field* solutions are plausibly congruent to counted ones (the
  xy class shares the yz class's algebra under Theorem P relabeling), but
  this is inferred, not verified.
- Mixed-*class* systems (different classes on different pairs, beyond the
  triangle+1 family) were not enumerated: the full space is 15 subsets ×
  6⁴ assignments ≈ 19k systems. The two n=3 resonance mechanisms (yz
  octahedral, xz golden) and their mixed-orientation embeddings are
  covered; xy-class and cross-class combinations are not.
- k=1,2,3 systems are positive-dimensional families (1-, 2-, 3-parameter);
  the isolated-resonance question is exactly the k=4 case solved here.
  The k=3 "n=3-resonance ⊕ free cube 4" families exist trivially (add any
  4th cube to the octahedral/golden 67) but are not isolated points.
- Everything ≥ deg-4 field is open (§5) — none counted, none approximated.
- Budget: ~35 min wolframscript solving (4 cores max, sequential kernels),
  ~2 min exact counting (63 candidates × ~1.2s each), well within limits.

## 8. Verdict

Within everything exactly counted, **the n=4 family's cross-class
resonances are all count-negative**: best 151 vs plateau 175 vs record 183
vs cap 195. The n=3 "+12 spike" mechanism does **not** carry to n=4 in any
quadratic-field resonance — the extra coincidences merge regions rather
than create them, as at the n=3 face-diagonal point. The surviving hope for
a family-resonance route to ≥183 narrows to the open degree-4 points of §5,
most plausibly the ℚ(√13)-tangent chain (whose tilt field matches the
record's own), and to the un-swept mixed-class systems.

## Files

- `resonance4_solve.wl` — the g-polynomials + system builder + both sweep
  drivers (wolframscript; reslib/sweep_uniform/sweep_mixed concatenated).
- `resonance4_solve.py` — generic ℚ(√d) engine factory (`make_qd`), exact
  Rel-matrix builder over any field, `exact_count_field` core (clone
  lineage: slide3_q2.py ← qtower.exact_count_tower ← certify_six), GATE R2.
- `resonance4_results.jsonl` — 69 records: 63 exact counts (36 uniform +
  27 mixed) + 6 open-candidate classes with minimal polynomials.
- Scratch (session-local, not shipped): sympy derivations (`derive2.py`,
  `gate_r1*.py`), sweep outputs (`uniform_k4_results.jsonl`,
  `mixed_k4_results.jsonl`), triage.
