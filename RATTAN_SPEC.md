# RATTAN_SPEC — the rational-tangent sweep (the slice the records actually live in)

Task for the implementing agent (Sonnet). Background: Postscript 27 in
six_cube_search_results.md (READ-ONLY), glue_report.md, nfamily_report.md,
nfamily_common.py (reuse). Validated files and the ledger: never edit.
≤4 cores; detached runs; interim results into the report as you go.

## Motivation

The records' family structure lives at RATIONAL-TANGENT tilts with
irrational sines: 393 contains an exact single-axis 4-clique (cubes
{1,2,3,4}, axis (3,2,0), tan ψ = 2/3, d = 13); 183's triple {0,2,3} is a
family clique three ways (tan 2/3 / 3/5 / 2/5; d = 13, 34, 29). Every
prior sweep used Pythagorean (rational-sine) tilts and was structurally
blind to this locus. The glue search's best configs sit EXACTLY 8 below
the record at n = 4, 5, and 6 — the rational-tangent slice is the
natural place to close (or explain) that floor.

## Arithmetic (verify as gate G0)

Tilt tan ψ = q/p (gcd = 1, d = p² + q² non-square): sinψ = q/√d,
cosψ = p/√d. A phase step Δ keeps Rel(Δ, ψ) RATIONAL iff cosΔ ∈ ℚ and
sinΔ = s′·√d with s′ ∈ ℚ, i.e. (cosΔ, s′) is a rational point on the
conic c² + d·s′² = 1, parametrized by rational t:
  cosΔ = (1 − d t²)/(1 + d t²),   s′ = 2t/(1 + d t²).
Check Rel's entries: cosΔ·cos²ψ + sin²ψ = (cosΔ·p² + q²)/d,
cosψ·sinψ·(1−cosΔ) = pq(1−cosΔ)/d, cosψ·sinΔ = p·s′ — all rational. ✓
Conic angles are closed under addition (norm-1 elements of ℚ(√d)), so
chains and arbitrary tuples of conic phases all stay rational →
integer quaternions → the fast C++ engine ./cube_regions_n applies.

## Gates

G0: implement the parametrization exactly (Fractions); verify a round
    trip and closure under angle addition.
G1 (the sharp gate): reproduce the 393 record's OWN 4-clique from the
    parametrization — find (t-values) such that the pairwise relative
    rotations of cubes {1,2,3,4} of `4,1,1,-1;3,3,7,3;5,-1,-5,-5;
    2,1,1,1;1,1,1,1` (after transforming into the axis-(3,2,0), tanψ=2/3
    frame) are exactly Rel(Δ(t), ψ). This proves the sweep space
    CONTAINS the record's clique.
G2: two-engine agreement (C++ vs certify_six.exact_count_config) on one
    n=4 and one n=5 rational-tangent config.
G3: reproduce 723 from the ledger quats.

## Sweep

1. **Single-axis, rational-tangent**: tilts q/p ∈ {2/3, 2/5, 3/5, 1/2,
   1/3, 1/4, 3/4, 1/5, 4/5, 5/12, ...} (prioritize the records' three).
   Phases: conic angles from rational t with small Farey denominators
   (|t| = a/b, b ≤ ~40), chains and random tuples, n = 4, 5, 6.
   Budget ~50k–200k configs (engine ~10ms each).
2. **Record-clique completion (the targeted shot)**: take the EXACT
   4-clique {1,2,3,4} of 393 as fixed base; sweep the 5th cube over (a)
   more conic angles on the same axis, (b) integer quaternions up to
   norm ~600 (this is how 393 itself is built — cube 0 is NOT on the
   axis); at n=6 take 393's five cubes fixed and sweep the 6th (this
   space contains 723 — verify you can re-find it) and take the best
   n=5 findings + a 6th. Similarly complete 183's triply-resonant
   triple {0,2,3} with a 4th cube.
3. **Hill-climb** the top candidates (t-perturbations, axis-menu, extra
   cube quats), multi-restart.
4. ANY total > record (183/393/723), or = record with a non-congruent
   structure (check pairwise invariants): verify with the Python oracle
   immediately and FLAG AT TOP. Main session records; never edit the
   ledger.

## Deliverables

rattan_report.md (gates, best per n with quats + depth profiles, whether
the −8 floor closes, coverage), rattan_sweep.py, rattan_results.jsonl.
