# The widened ℚ(√d) engine — gate report

`cube_regions_q2w.cpp` / `./cube_regions_q2w`, built to
[`specs/WIDE_ENGINE_SPEC.md`](specs/WIDE_ENGINE_SPEC.md). The validated narrow engine
`cube_regions_q2.cpp` was not modified.

**Why.** Of 508 818 candidate configurations on the mixed 2-plane + 1-quadric
strata at n=6, the narrow engine counted 224 184 and **rejected 284 634** for
exceeding its 2^112 chain budget (`mixed_q2_full.out`). Rejected is not
"checked"; those configurations are uncounted, and the record could be among
them.

**Not the sign predicate.** `sign(p + q√d)` squares its operands and so needs
more width than the value chain, but the narrow engine's own budget derivation
establishes that across the whole admissible region the i128 CHAIN bound
always binds first. A cheaper sign test — deciding p + q√d by continued
fraction convergents of √d rather than by comparing p² with d q² — therefore
buys no extra range. Widening the scalar is the only thing that helps.

## Gates

**G1 — EQUIVALENCE. PASS.** 1365 configurations across 33 distinct fields
(d = 3, 5, 6, 10, 13, 62, 82, 113, 115, 226, 281, 310, 313, 337, 370, 394,
403, 577, 593, 609, 705, 721, 817, 1093, 1177, 1614, 1785, 1930, 2190, 2741,
2857, 3689, …), taken from `mixed_q2_hits.jsonl` so every case is known to sit
inside the narrow budget. Both engines received byte-identical input.
**Identical `bounded` AND identical `by_depth` on all 1365, 0 mismatches.**
Driver: `wide_gate.py`.

A methodological note, because the first version of this gate PASSED
VACUOUSLY: the driver joined a quaternion's four components with `;` instead
of `,`, so every line failed to parse, both engines emitted the same error
JSON, and the comparison of two identical error lists reported "IDENTICAL"
across all 1365 rows in 0.11 seconds. The impossible timing is what gave it
away. The driver now asserts that every row produced an actual count before
any comparison is believed — a gate that can pass on empty output is worse
than no gate.

**G2 — RATIONAL SPECIALISATION. PASS.** With `--d 0`, agreement with
`cube_regions_n`:

| configuration | wide | `cube_regions_n` |
|---|---|---|
| `4,1,1,-1;3,3,7,3;5,-1,-5,-5;2,1,1,1;1,1,1,1;7,14,1,-5` | 727 | 727 |
| the same five (393 base) | 393 | 393 |
| `1,0,0,0;0,5,3,2;1,-4,-1,1;1,1,-1,-4` | 183 | 183 |
| `1,0,0,0;0,1,1,1` | 13 | 13 |

The 727 depth profile also matches: {214, 220, 156, 100, 36, 1}.

**G3 — BUDGET BOUNDARY. PASS.** At d = 5 with a sixth-cube component
magnitude 3001 (the narrow limit at d = 5 is 1855), the narrow engine rejects
with its traced diagnostic — "needs ~117.5 bits at the i128 chain stage
(limit 112)" — and the wide engine counts the configuration: 683 regions. At
d = 5 with magnitude 10^14 and 10^18 the wide engine rejects cleanly with the
same style of traced message.

*Known rough edge, pre-existing and not introduced by the widening:* a
component too large for `int64` aborts during input parsing with an uncaught
`std::out_of_range` from `stoll` rather than a clean `ConfigError`. Both
engines do this. It is a parsing defect, not an arithmetic one — nothing is
silently truncated — but it should be tidied.

**G4 — SELFTEST. PASS.** `./cube_regions_q2w --selftest` reports ALL PASS,
including the axial families (n = 2..12, totals (2n−1)² = 9 … 529).

**G5 — PERFORMANCE.** On the identical 1365-configuration G1 input:
narrow 64.5 s, wide 149.6 s, **ratio 2.32x**. Well inside the ~10x the spec
allowed.

## New admissible region

The chain threshold moves from 2^112 to 2^240 and the sign threshold from
2^231 to 2^496, keeping the same headroom style (16 bits below the type's
capacity). Empirically at d = 5 the admissible component magnitude moves from
1855 to somewhere between 10^13 and 10^14 — the pipeline is roughly degree 4
in the component magnitude, so 128 extra bits of headroom buys about 2^32.

## Status

The engine is gated and in use. Counting the previously-rejected strata is a
separate, longer job — `wide_campaign.py`, a detached sharded campaign that
re-counts ALL 508 818 configurations with the wide engine, so it doubles as an
equivalence check at scale. Its results are reported in the ledger, not here.
