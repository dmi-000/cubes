# WIDE_ENGINE_SPEC — a 256-bit ℤ[√d] engine for the out-of-budget strata

Deliverable: `cube_regions_q2w.cpp`, built as `./cube_regions_q2w`, plus a
report. `cube_regions_q2.cpp` is VALIDATED and must not be modified.

## 0. Why

`cube_regions_q2` rejects any config whose traced pipeline bound exceeds
2^112. On the mixed strata that rejected **284 634 of 508 818** candidate
configurations at n=6 (`mixed_q2_full.out`) and ~108 984 at n=5. Those are not
known to be free of a record; they are simply uncounted. Raising the scalar
width raises the admissible (m, d) region and lets them be counted.

Note on the sign predicate: `sign(p + q√d)` squares its operands, but the
file header of `cube_regions_q2.cpp` records that across the whole admissible
region the i128 CHAIN bound is always the binding constraint, with the sign
bound strictly slacker. So a cheaper sign test (e.g. deciding p + q√d by
continued-fraction convergents of √d instead of comparing p² with d q²) would
NOT widen the admissible region — the value chain overflows first. Widening
the scalar is the only thing that helps, which is what this spec does.

## 1. The scalar type

Add `i256`: a signed 256-bit integer as 4 little-endian `uint64_t` limbs in
two's complement, supporting +, -, unary -, * (mod 2^256 — see the budget),
comparison, equality, `isZero`, `sign`, and construction from `int64_t` and
`__int128`. Multiplication is schoolbook over 32-bit half-limbs so every
partial-product accumulation is carry-safe in a `uint64_t`, exactly as
`mulU128` in the existing file already does for the 256-bit path.

`FieldElem` becomes a pair of `i256` instead of a pair of `i128`. Everything
else in the pipeline (planes, det3 minors, vertices, side-of-plane predicate)
keeps its structure; only the scalar type changes. Prefer templating
`FieldElem` on the scalar (or a typedef switch) over duplicating the algebra.

## 2. The budget, retraced

Reuse the existing `pipelineBound()` tracing (same 4-stage chain, same
worst-case propagation) and change only the two thresholds, keeping the same
style of headroom:

  - CHAIN: every intermediate (p, q) must stay under **2^240** (16 bits of
    headroom below 2^256).
  - SIGN: p² and d·q² must stay under **2^496** (16 bits below 2^512).

`validateBudget()` must still reject — hard, with `ConfigError`, before any
arithmetic runs — anything exceeding either threshold, and must still require
d squarefree (or 0). Silent truncation is the failure mode this whole project
guards against; a clamp is not acceptable.

Print, in the report, the new admissible ceiling: the largest d admissible at
m = 1, and the largest m admissible at d = 5, 13, 62, 1177, 8761.

## 3. The sign predicate

`FieldElem::sign()` keeps its same-sign/zero fast paths verbatim. The
mixed-sign branch must now compare p² against d·q² with operands up to 2^240,
so it needs an exact **512-bit** unsigned compare: implement `mulU256`
(4 limbs x 4 limbs -> 8 limbs) and `cmpU512`, in the same carry-safe style as
the existing `mulU128`/`cmpU256`, and use them ONLY there.

## 4. Gates — all required, all reported

G1 — EQUIVALENCE (the important one). Build a list of at least 3000
  configurations that are inside the NARROW budget, spanning at least six
  distinct d (take them from `mixed_q2_hits.jsonl`, and/or regenerate a slice
  with `mixed_q2_full.py`'s emitter; small-d classes like 5, 13, 62 are dense
  and easy). Run both engines on the identical input. REQUIRE identical
  `bounded` AND identical `by_depth` on every single one. Report the count
  compared and any mismatch with the offending config. One mismatch means the
  widened engine is wrong — report it, do not tune around it.

G2 — RATIONAL SPECIALISATION. With `--d 0`, the wide engine must agree with
  `./cube_regions_n` on: the 727 record
  `4,1,1,-1;3,3,7,3;5,-1,-5,-5;2,1,1,1;1,1,1,1;7,14,1,-5` -> 727; the 393 base
  (first five of those) -> 393; `1,0,0,0;0,5,3,2;1,-4,-1,1;1,1,-1,-4` -> 183;
  `1,0,0,0;0,1,1,1` -> 13.

G3 — BUDGET BOUNDARY. Exhibit one config REJECTED by `cube_regions_q2` and
  ACCEPTED (counted) by the wide engine, and one exceeding even the wide
  budget that is rejected by both with a clear `ConfigError`. Print both.

G4 — ARITHMETIC SELFTEST (`--selftest` flag). Randomised comparison of i256
  +, -, * and compare against `__int128` for operands below 2^60 (where both
  are exact), at least 100 000 trials; and of the 512-bit square-compare
  against a `__int128`-based computation for operands below 2^60. Any
  disagreement aborts.

G5 — PERFORMANCE. Time both engines on the same 3000-config G1 input and
  report the ratio. A slowdown up to ~10x is expected and fine; report the
  actual number.

## 5. Report

`wide_engine_report.md`: the gate results with real numbers, the new
admissible ceilings from section 2, the timing ratio, and an explicit
statement of what is still out of budget after widening (i.e. which of the
284 634 rejected n=6 configs remain rejected — count them by running
`validateBudget` logic over the rejected set, or state that all of them now
fit).

Do NOT edit `LEDGER.md` (ledger: main session only), and do
not modify `cube_regions_q2.cpp` or `cube_regions_n`.
