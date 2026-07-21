# OPENCOUNT_SPEC — exactly count the open n=4 resonance candidates

Task for the implementing agent (Sonnet). Background: RESONANCE4_SPEC.md,
resonance4_report.md §5 (the open candidates), resonance4_results.jsonl
(status:"open" rows), resonance4_solve.py (has `exact_count_field(rots,
Field)` — REUSE it; it is field-generic), resonance4_solve.wl (the
solver that produced the candidates — re-query it for exact parameters),
qtower.py and cube_compound_exact.py / certify_six.py (validated exact
engines, READ-ONLY reference), C45_notes.md §12 (Rel gauge). Ledger and
all validated files READ-ONLY. ≤4 cores; detached for any long solve;
interim results into the report as you go.

## Why this matters

resonance4 counted every n=4 family resonance in a single quadratic
field and found them ALL count-negative (best 151 < plateau 175 <
record 183), which is the main evidence that "n=3 is the only irrational
rung" of the record tower. But ~160 candidates were left UNCOUNTED
because their coordinates live in degree-4 fields, and the project's
voxel triage is demonstrably unreliable there (it reads the known-175
config as 246 at R=120). The single most interesting is a pure CHAIN at
tan ψ = (1+√13)/6 — the record's OWN tilt field ℚ(√13). **If any open
candidate counts ≥ 183, the "3 is the only irrational rung" conjecture
is FALSE and it is a headline.** This task settles them exactly.

## The candidates (resonance4_results.jsonl, status:"open")

Six documented classes plus a bulk of ~90 unparsed mixed-sweep points:

| ψ (deg) | tan ψ (min poly) | field character | structure |
|---|---|---|---|
| 53.794 | (1+√3)/2  (2t²−2t−1) | ℚ(√3)(√(4−√3)) | yz k=4 |
| 37.510 | (1+√13)/6 (3t²−t−1) | ℚ(√13)(√·) | **chain θ_k=k·200.891°, {12,14,23,34}** |
| 12.667 | −1+√6/2   (2t²+4t−1) | ℚ(√6)(√·) | yz, {12,14,23,34} |
| 58.283 | sinψ root of 5s⁴−5s²+1 | pentagonal ⊂ ℚ(√5) | xz, θ ∈ 72°·ℤ (many Δ=0) |
| 38.173 | t⁴+t²−1 (t²=1/φ) | ℚ(√5)(√φ⁻¹) | xz k=4 |
| — | WL Root[1−5#²+5#⁴] + ~90 unparsed | assorted quartic | mixed sweep |

Re-derive exact parameters from resonance4_solve.wl (re-run the relevant
Solve/Root calls and `RootReduce` to minimal polynomials with isolating
intervals) rather than trusting the float ψ; the report's floats are for
identification only.

## The engine (the core deliverable)

The region counter needs only the SIGN of field elements (dot products
of exact rotation-matrix columns). Two robust representations; use
whichever fits a candidate, prefer (A) for uniformity:

(A) **Primitive-element number field ℚ(α).** Put all of a candidate's
    coordinates in one field ℚ(α), α a real algebraic number given by an
    irreducible min poly + isolating interval. An element is a ℚ-vector
    in the power basis; it is EXACTLY ZERO iff that vector is zero
    (decidable, exact); its sign otherwise is found by refining α's
    isolating interval until the element's interval excludes 0
    (terminates for nonzero algebraic numbers). This sidesteps the
    "interval arithmetic cannot certify =0" trap entirely, because zero
    is caught symbolically in the power basis. sympy's `AlgebraicField` /
    `minimal_polynomial` / `Poly` over `QQ.algebraic_field(α)`, or a
    small hand-rolled class, both work. This handles ALL candidates,
    including the genuinely-quartic (non-tower) ones.
(B) **Relative quadratic tower ℚ(√a)(√b), b = p+q√a** (an optimization
    for the tower cases: rows 1–3, 5 above). Element A+B√b, A,B ∈ ℚ(√a).
    Sign via the standard quadratic-surd recursion: sign(A+B√b) with
    √b>0 — if A,B same sign that sign; if B=0 → sign(A); else compare
    A²  vs  B²b (both in ℚ(√a), signs known) to resolve. Generalizes
    qtower.py (which only does b ∈ ℚ). Faster than (A) where it applies.

Feed the resulting exact rotation matrices to
`resonance4_solve.exact_count_field(rots, Field)` (or certify_six's
counter wrapped on the field). Cube k = Rel(θ_k, ψ) in the Rel gauge:
axis n(ψ)=(sinψ,cosψ,0), rotation by θ_k; all of cosψ,sinψ,cosθ_k,sinθ_k
are elements of the field, derived exactly from the min polys.

## Gates (all must pass before any count is trusted; put in report)

G1 (field self-test): (√b)²=b exactly; conjugate products land in the
   base field; `.sign()` agrees with a 50-digit float evaluation on 1000
   random field elements, both representations. Exact-zero detection
   verified on constructed zeros (e.g. (√b)²−b).
G2 (rational reproduction): feed the KNOWN rational n=4 configs 175 and
   151 (151 quats 1,0,0,0;-1,2,1,0;2,2,1,0;7,-2,-1,0) through a
   DEGENERATE tower/field wrapper; the field counter must return exactly
   what ./cube_regions_n returns (151 = {68,58,24,1}, and the 175 profile
   from nfamily/glue data). This validates the counter plumbing on the
   new field code.
G3 (quadratic reproduction): reproduce the n=3 octahedral 67 via ℚ(√2)
   AND one genuine ℚ(√5) count (golden 351 at n=5, or 177 at n=4 — from
   the ledger) through the field engine, to validate a real quadratic
   extension end-to-end (compare to cube_compound_exact / the ledger).
G4 (nested reproduction): before counting the open candidates, count ONE
   candidate two independent ways — representation (A) and (B) where both
   apply (e.g. the √6 row) — and require identical total + depth profile.

## Counting run

For each open class: derive exact params, build matrices, count total +
depth profile + field, write to opencount_results.jsonl. Dedupe by
congruence (pairwise O-reduced invariants) — many mixed-sweep points are
congruent. Handle the Δ=0 (coincident-cube) degenerate members
explicitly: they are effectively 3-cube compounds, not competitors; mark
them. For the ~90 unparsed points, extract their fields from the .wl
sweep output; count all that are ≤ degree 4; anything higher-degree, use
representation (A) (it is degree-agnostic) or report the min poly and
mark genuinely-open if the field build is intractable.

**Record protocol**: any candidate ≥ 175 note; ≥ 183 FLAG AT TOP and
re-verify by the OTHER representation (A vs B) or by certified interval
arithmetic with symbolic zero-guard, then by a congruence check against
the record. Never edit six_cube_search_results.md or validated files.

## Deliverables

opencount_report.md (gates; a table of every open candidate with exact
ψ/θ min polys, field, total, depth profile, congruence class, and the
verdict "does any irrational n=4 resonance reach 183/175?"),
opencount.py (the field engines + driver), opencount_results.jsonl.
Honest coverage: which candidates counted, which fields were built,
which (if any) remain genuinely open and why.
