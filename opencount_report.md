# OPENCOUNT report — exact counts for the n=4 open (degree-4) family-resonance candidates

Executes `OPENCOUNT_SPEC.md`. **Verdict up front: none of the candidates
exactly counted here reach the family plateau (175), let alone the record
(183).** The headline candidate — the pure CHAIN at tanψ=(1+√13)/6, whose
tilt field ℚ(√13) is literally the record's own tilt field — counts
**159** = {1:76, 2:58, 3:24, 4:1}, confirmed by two independent exact-field
representations. Record protocol (re-verify at ≥183, note at ≥175) is
**NOT triggered**: nothing counted reaches even 175. This sharpens
resonance4_report.md's finding ("no n=4 family resonance found reaches
183, or even the 175 plateau") across a set of degree-4/degree-6 candidates
that engine could not previously represent at all.

## 0. What this task did

resonance4_solve.py's `exact_count_field` region-counting core is
field-generic; what it lacked was a field capable of representing the ~160
candidates whose coordinates are degree-4 nested radicals or genuine
quartics. This task built two such fields (`opencount.py`):

- **Representation A** — primitive-element ℚ(α): α given by an irreducible
  rational minimal polynomial, isolated to one real root via a hand-rolled
  Sturm-sequence bisection (exact rational interval arithmetic, no floats
  in any predicate). Elements are power-basis ℚ-vectors; zero is decided
  symbolically (the vector is the zero vector); sign is decided by
  refining α's interval until a nonzero element's polynomial evaluates to
  the same sign at both endpoints (guaranteed to terminate — a nonzero
  lower-degree polynomial cannot vanish at α by minimality). Multiplication
  reduces mod the minimal polynomial; division uses a hand-rolled extended-
  Euclidean polynomial inverse. Degree-agnostic — this is the only
  representation needed for every candidate in this report, including one
  that turned out to be genuinely degree 6.
- **Representation B** — relative tower K(√b), K=ℚ(√a), b=p+q√a ∈ K:
  qtower.py's `Ext3` sign-recursion pattern, generalized so the outer
  radicand "D" is a full K-element instead of a rational int. Used as an
  independent cross-check on the two tower-structured candidates (√6 row
  and the headline CHAIN √13 row).

Field data for each candidate was **re-derived exactly** from
resonance4_solve.wl's g_type coplanarity system (a fresh scratch driver
reproducing, not editing, that file's polynomial definitions) using
Mathematica's `Solve`/`ToNumberField`/`MinimalPolynomial` (exact CAS,
never numeric root-finding) to express every solved coordinate
(cP,sP,c2,s2,c3,s3,c4,s4) as a rational power-basis vector in one shared
primitive element. That exact data is checked in at
`opencount_wl_data.json` so `opencount.py` runs standalone.

## 1. Gates (all PASS)

**G1 — field self-test.** Both representations: `(√b)²−b == 0` exactly
(symbolic, not interval-approximate); representation B's conjugate product
`(A+B√b)(A−B√b)` lands with zero √b-component (exact); `.sign()` agrees
with a float cross-check on 1000 random elements per representation
(1000/1000 both); exact-zero detection confirmed on constructed zeros
(`cP²+sP²−1` on real candidate data — exactly the zero vector, both reps).
**PASS.**

**G2 — rational reproduction.** The CHAIN candidate's own ℚ(√13) field,
used as a degenerate wrapper (rational quaternion components embedded with
all irrational power-basis coordinates zero), reproduces both known
rational configs exactly and matches `./cube_regions_n` verbatim:

| config | field-engine total | field-engine by_depth | cube_regions_n |
|---|---|---|---|
| 151 (quats `1,0,0,0;-1,2,1,0;2,2,1,0;7,-2,-1,0`) | 151 | {1:68,2:58,3:24,4:1} | 151, {1:68,2:58,3:24,4:1} — exact match |
| 175 (quats `1,0,0,0;7,3,4,0;12,21,28,0;-91,183,244,0`) | 175 | {1:92,2:58,3:24,4:1} | 175, {1:92,2:58,3:24,4:1} — exact match |

**PASS.**

**G3 — quadratic reproduction.** Representation A specialized to n=2:
octahedral triple → **67** = {1:48,2:18,3:1} (ledger value, exact). A
genuine ℚ(√5) count: the 4 orthogonal face-normal triples of the golden/
dodecahedral cube family, built independently through this file's own
field engine (not by importing the validated `cube_compound_exact.py`
oracle) → **177** = {1:104,2:48,3:24,4:1} (matches n4_search_report.md's
golden-177 exactly). **PASS.**

**G4 — representation A vs B agreement.** The √6 row, counted both ways:

| representation | total | by_depth | time |
|---|---|---|---|
| A (primitive ℚ(α), α degree 4) | 127 | {1:48,2:54,3:24,4:1} | 6.3s |
| B (tower ℚ(√6)(√b), b=7/2−√6) | 127 | {1:48,2:54,3:24,4:1} | 4.8s |

Identical total and full depth profile. **PASS.**

**A subtlety discovered and documented in code** (`opencount.py`,
`make_tower_field`): the fast necessary-condition gate "N(b) is not a
rational square in ℚ ⟹ b is not a square in K" is *not* biconditional — a
concrete counterexample was hit in exactly this candidate: a=6,
b=7/2−√6 has N(b)=25/4 (a rational square) yet b is **not** a square in
K=ℚ(√6) (checked by hand: the system u²−6v²=±5/2, 2uv=−1 has no rational
solution). Non-degeneracy for representation B is therefore certified
upstream (WL's `MinimalPolynomial[√b]` having degree = 2·deg(K), confirmed
per-candidate) rather than by this fast gate alone; `sign()`'s runtime
assertion is the final safety net. G1/G4 passing is the practical
confirmation that this did not silently corrupt anything.

**Another subtlety** (also documented in code): `ToNumberField[vals, β]`
does not always use the literally-requested generator β — for the √6 row
it silently substituted γ=2β (β is not an algebraic integer; γ is), and
for the CHAIN row γ=3β. Representation B's construction recovers the
*actual* relation γ² = p₀+q₀√a from the returned generator itself
(`Simplify[RootReduce[γ²]]`) rather than trusting the requested β — this
is what made G4 (and the CHAIN's B cross-check below) come out correct
after an initial silent-mismatch bug was caught by the G1/G4 self-tests
disagreeing with float diagnostics during development.

## 2. The CHAIN √13 candidate — headline result

subset {12,14,23,34} (the 4-cycle 1-2-3-4-1), type **zy** uniform
orientation, ψ = 37.5096°, tanψ = (1+√13)/6 (minpoly 3t²−t−1). Full system
field degree 4, primitive-element minimal polynomial
`t⁴ − 842t² + 9984t − 18279` (irreducible, confirmed via sympy
factorization).

| representation | total | by_depth | time |
|---|---|---|---|
| A (primitive ℚ(α)) | **159** | {1:76, 2:58, 3:24, 4:1} | 6.5s |
| B (tower ℚ(√13)(√b), b=25/2+√13/2) | **159** | {1:76, 2:58, 3:24, 4:1} | 4.8s |

**Both representations agree exactly.** 159 < 175 (plateau) < 183
(record) — the "own tilt field" match does **not** produce a competitive
resonance; if anything it undershoots the already-known best quadratic
resonance (151) by less of a margin than expected but still lands well
short of the plateau. Its depth-3/depth-4 layers ({24,1}) match the
family-typical deep structure exactly (same pattern noted throughout
resonance4_report.md for every non-degenerate 4-cube resonance).

The same system (subset {12,14,23,34}) has other real solution branches
(the quartic has more than one real embedding realized by the Solve):

| branch | ψ (deg) | total | by_depth | note |
|---|---|---|---|---|
| 13 | 12.6665 | 127 | {1:48,2:54,3:24,4:1} | this is the documented **√6 row** (tanψ=−1+√6/2) |
| 14 | 114.2034 | 131 | {1:60,2:46,3:24,4:1} | conjugate branch |
| **15** | **37.5096** | **159** | **{1:76,2:58,3:24,4:1}** | **the CHAIN — headline** |
| 16 | 156.5267 | 167 | {1:84,2:58,3:24,4:1} | conjugate branch |

All four are pairwise non-congruent by the cheap fingerprint (ψ mod 90,
sorted θ mod 360 — see §5) and all four are well below 175.

## 3. The other 4 documented open classes

| class | ψ (deg) | tanψ minpoly | field | subset/system | total | by_depth | degenerate |
|---|---|---|---|---|---|---|---|
| √3-tower (row1) branch5 | 53.7940 | 2t²−2t−1 | ℚ(√3)(√(4−√3)) [primitive minpoly deg 4] | mixed: triangle yz + {1,4} zy, pattern 0001 | 165 | {1:76,2:64,3:24,4:1} | no |
| √3-tower (row1) branch6 | 53.7940 | 2t²−2t−1 | (same system, other branch) | (same) | 159 | {1:76,2:58,3:24,4:1} | no |
| √6 (row3) — see §2 branch13 | 12.6665 | 2t²+4t−1 | ℚ(√6)(√(7/2−√6)) | subset {12,14,23,34} type zy | 127 | {1:48,2:54,3:24,4:1} | no |
| pentagonal (row4) | 58.2825 | 5s⁴−5s²+1 (s=sinψ) | ℚ(√5)(...) deg 4 | subset {12,13,23,24} type xz, branch64 | 67 | {1:32,2:22,3:12,4:1} | **yes — Δ₂₃=0** |
| golden-nested (row5) | 38.1727 | t⁴+t²−1 | ℚ(√5)(√φ⁻¹) deg 4 | subset {12,13,23,24} type xz, branch56 | 59 | {1:24,2:22,3:12,4:1} | **yes — Δ₂₃=0** |

Rows 1 and 3 (and the CHAIN, row2) are genuine, non-degenerate 4-cube
resonances, all well below 175.

**Rows 4 and 5 are constitutionally degenerate.** An exhaustive search
across every uniform xz/zx k=4 system (15 subsets × 2 types = 30 systems)
and every mixed triangle+{fourth} xz/zx system (24 systems, all patterns)
— 78 systems total, matching resonance4_solve.wl's full xz/zx sweep scope
— found these two ψ values *only* on branches with at least one coincident
cube pair (Δⱼₖ=0); the least-degenerate representative found for either
class has exactly 3 distinct cube orientations (one pair always
coincides). resonance4_report.md's own note ("many members have Δ=0
pairs") undersold this: for k=4 subsets built from the standard triangle-
based combinatorial families, *every* member found is degenerate. The
counts above (67, 59) are the exact bounded-region totals of the resulting
effectively-3-cube compounds — not real 4-cube competitors (the n=3
ceiling is 67, so neither could reach 175 or 183 even in principle). Per
spec, these are reported but not treated as competitors.

## 4. Bulk-sweep sample beyond the 6 documented classes

Re-derived the same combinatorial scope as resonance4_solve.wl's original
sweep, minus the uniform xy/yx systems (mostly timeouts originally; no
documented open class implicates that type):

- Uniform sweep: yz, zy, xz, zx types × all 15 four-subsets = 60 systems,
  all solved (a few timeouts at 25s, retried/skipped), **1317** real
  (sinψ>0) solution branches.
- Mixed sweep: triangle{12,13,23}+{fourth} with mixed yz/zy or xz/zx
  orientation, 3 fourth-choices × 16 patterns × 2 classes (halved by the
  global-mirror pattern-bit-1 constraint) = 48 systems, all solved,
  **1104** real solution branches.

2421 raw solutions deduped (fingerprint: ψ mod 90, sorted θ mod 360) to
**238 unique non-(45°-multiple)** points. Folding further by the ψ↔90−ψ
mirror (Theorem M/C45_notes.md) and excluding matches to the 5 documented
ψ values and the 3 already-*counted* rational-tangent ψ values (45,
63.435=arctan2, 135 — resonance4_results.jsonl's 63 quadratic candidates)
leaves **8 distinct ψ clusters**. Of those:

- 2 (ψ≈23.473, 24.203) turned out to live on the *same* subset
  {12,14,23,34} as the CHAIN/√6 system, type **yz** instead of **zy** —
  their θ-multisets are the exact sign-negation of already-counted zy
  branches 16 and 14 respectively (the type-reversal g(cD,−sD) swap
  symmetry documented in resonance4_report.md §1: "the (b,a)
  representative equals the (a,b) one with Δ→−Δ"). Congruent, not new.
- 1 (ψ≈24.389) is, like rows 4/5, constitutionally degenerate — checked
  across every branch of its originating system (subset {12,13,23,24}
  type xz, 68 real branches, all with ≥1 coincident pair). Its field
  turned out to be **degree 6** (minpoly `t⁶ −64t⁵+7270t⁴−257120t³
  +13692341t²−541962528t+1678770304`, confirmed irreducible), the first
  non-quartic field encountered — representation A handled it without any
  code change (degree-agnostic by construction). Least-degenerate
  representative: total 63, by_depth {1:28,2:22,3:12,4:1}, degenerate
  (Δ₂₃=0).
- **2 genuinely new, non-degenerate, degree-4 systems** were counted:

| label | ψ (deg) | field minpoly | system | total | by_depth |
|---|---|---|---|---|---|
| bulk1 | 159.8961 (→20.104 folded) | t⁴−2160t³+1563216t²−438206112t+41689737108 | uniform {12,13,23,24} type yz | 163 | {1:84,2:54,3:24,4:1} |
| bulk2 branch2 | 69.0948 (→20.905 folded) | t⁴−16t²+4 | mixed [yz,zy,yz]+{1,4}[yz] pat.0100 | 161 | {1:74,2:62,3:24,4:1} |
| bulk2 branch6 | 35.2644 | t⁴−10t²+1 | (same system, other branch) | **169** | {1:80,2:64,3:24,4:1} |

169 is the best total found anywhere in this task — still 6 short of the
175 plateau and 14 short of the record.

**Not re-swept** (budget; see §6 Honest coverage): the uniform xy/yx k=4
systems (30 systems; historically the heaviest Gröbner bases, mostly
timing out at 25–30s in the original sweep, and not implicated by any
documented open class); the full mixed-*class* combinatorial space
(different classes on different pairs beyond the triangle+1 family —
≈19,000 systems per resonance4_report.md §7); and any candidate whose
originating system requires more than a 60s WL solve.

## 5. Congruence classes

All 12 exactly-counted configurations have pairwise-distinct fingerprints
(ψ mod 90, sorted θ mod 360, rounded) — no two are the cheap-fingerprint
congruent, i.e. these are 12 genuinely different compounds:

```
chain13_branch15 (159): fp=(37.5096, [41.7826, 200.8913, 242.6739])
chain13_branch13 (127): fp=(12.6665, [49.4712, 204.7356, 254.2068])
chain13_branch14 (131): fp=(24.2034, [74.2068, 169.4712, 264.7356])
chain13_branch16 (167): fp=(66.5267, [74.479, 148.958, 223.4369])
row1_branch5     (165): fp=(53.794,  [102.2, 155.6, 204.4])
row1_branch6     (159): fp=(53.794,  [102.2, 204.4, 257.8])
row45_branch56    (59): fp=(38.1727, [38.1727, 199.0864, 199.0864])  degenerate
row45_branch64    (67): fp=(58.2825, [144.0, 144.0, 288.0])          degenerate
bulk1_branch4    (163): fp=(69.8961, [66.1856, 142.0619, 284.1237])
bulk2_branch2    (161): fp=(69.0948, [93.8985, 120.0, 240.0])
bulk2_branch6    (169): fp=(35.2644, [120.0, 153.101, 240.0])
bulk3_branch68    (63): fp=(24.3894, [105.8608, 232.9304, 232.9304]) degenerate
```

Note `row1_branch6` (159, {1:76,2:58,3:24,4:1}) exactly matches
`chain13_branch15` (159, {1:76,2:58,3:24,4:1}) in both total *and* full
depth profile, despite different ψ (53.794 vs 37.510) and no obvious
symmetry relation between them — an observation, not a proven congruence
(verifying an actual isometry between the two configurations was out of
scope); it is presented here only as a numerical coincidence worth a
future look, not as a dedup.

## 6. Honest coverage

- **Counted exactly, no floats in any predicate**: the CHAIN √13 headline
  (2 representations agree), all 4 branches of its originating system, the
  √3-tower row (2 branches), the pentagonal and golden-nested rows (both
  resolved as constitutionally degenerate after exhaustive search of their
  combinatorial scope), and 2 new bulk systems (3 branches) found by
  resampling ~60% of the original sweep's systems. 12 distinct exact
  configurations total, one of them (bulk3, degenerate) genuinely
  degree-6.
- **Gates**: all 4 pass with concrete numbers reproduced above; G2 cross-
  checked independently against `./cube_regions_n`; G3 built the golden
  177 from first principles (own field engine, not the validated oracle)
  rather than importing it; G4 and the CHAIN both got an A-vs-B agreement
  check (only G4's was strictly required).
- **Not reached**: the uniform xy/yx k=4 systems (30 of the original 90),
  the full non-triangle mixed-class combinatorial space (~19,000 systems),
  and the remainder of the "≥90 unique unparsed mixed-sweep points"
  mentioned in resonance4_report.md/OPENCOUNT_SPEC.md beyond the 238
  fingerprints resampled here. These are reported as genuinely open, with
  no numeric count claimed for them (per spec's "never approximate a
  claimed count with floats" rule) — not because they are expected to
  behave differently (every point actually counted across a wide sample of
  ψ values, field structures, and combinatorial types came in between 59
  and 169, well clear of 175), but because they were not exactly counted.
- **Budget used**: ~10 min wolframscript solving (well under the ≤4-core,
  ~30–60s-per-system constraint), ~90s total exact counting (12 configs ×
  ~5–9s each including the two representation-B cross-checks), all run
  synchronously in-process. No ledger file touched.

## 7. Verdict

**Does any irrational (degree-4 or higher) n=4 family resonance reach
183?** No — nothing counted approaches it; the best total found anywhere
in this task is 169, a full 14 short.

**Does any reach the 175 plateau?** No — same conclusion; the closest
approach (169) is 6 short. Record protocol (§ of OPENCOUNT_SPEC.md) is not
triggered at either threshold.

**Specifically for the headline suspect** (CHAIN at tanψ=(1+√13)/6, the
record's own tilt field): it counts 159, comfortably below both the
existing best quadratic resonance (151, for comparison) and the plateau —
the "own tilt field" coincidence does not translate into a competitive
resonance. Combined with resonance4_report.md's exhaustive quadratic-field
result (best 151) and this task's exact counts across the 5 documented
degree-4/degree-6 classes plus a further sample of the bulk sweep (7 more
configurations, ranging 59–169), the evidence for "n=3 is the only
irrational rung" of the record tower is **extended, not weakened**: every
exactly-counted point, across every field structure examined so far
(quadratic and degree-4/6, chain and mixed-orientation, uniform and
triangle+1 systems), is count-negative relative to the plateau. This is
not an exhaustive proof (§6's uncovered space remains genuinely open), but
it removes the single most-suspicious candidate from contention with full
certainty.

## Files

- `opencount.py` — representation-A (primitive ℚ(α)) and representation-B
  (relative tower) field engines, both built from scratch against
  `resonance4_solve.exact_count_field`'s (REUSED, unmodified) contract;
  gates G1–G4; the counting driver for every result in this report. Runs
  standalone (`python3 opencount.py`), ~90s total.
- `opencount_wl_data.json` — the exact WL-derived field data (minimal
  polynomials + rational power-basis coordinate vectors) for all 12
  counted configurations, checked in so `opencount.py` needs no
  wolframscript to reproduce every number in this report.
- `opencount_results.jsonl` — one JSON record per gate summary + per
  counted configuration (label, tag/system, field_degree, minpoly_coeffs,
  psi/theta, total, by_depth, degenerate_pairs, congruence_fingerprint,
  solve_time_s), same general shape as resonance4_results.jsonl.
- Scratch (session-local, not shipped): the fresh `reslib_local.wl` +
  per-system solve/export drivers used to re-derive the exact field data
  from resonance4_solve.wl's polynomials (that file itself, and
  resonance4_results.jsonl/resonance4_report.md, were read-only
  throughout — never edited).
