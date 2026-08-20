# Count open n=4 resonance candidates

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-07-20T23:39:11 |
| Agent type | default |
| Model override | sonnet |
| Session | `c4196554-d37e-44f9-8da5-5d7210e1f156` |
| Tool-use id | `toolu_01MwAZTDrad8ABtK8EWz9QRU` |
| Files named | `opencount.py`, `opencount_report.md`, `six_cube_search_results.md` |
| Present in repo | `opencount.py`, `opencount_report.md` |
| Cited in LEDGER/RESULTS | `opencount.py`, `opencount_report.md` |

## Prompt as sent

```text
Execute /Users/dmi/carroll/OPENCOUNT_SPEC.md — exactly count the ~160 open n=4 resonance candidates that resonance4 left uncounted (degree-4 nested-radical fields), settling whether any irrational n=4 family resonance reaches the record 183. Working directory /Users/dmi/carroll. Read the spec first; it is self-contained and names the six documented candidate classes plus the bulk unparsed set, with exact tan ψ minimal polynomials.

Critical discipline:
- The counter needs only exact SIGNS of field elements. The robust, degree-agnostic representation is a primitive-element number field ℚ(α) (element = zero iff its power-basis vector is zero — exact; sign otherwise by refining α's isolating interval — terminates for nonzero algebraic numbers). Use this to avoid the "interval arithmetic cannot certify =0" trap. The relative-quadratic tower ℚ(√a)(√b) is a faster optimization for the tower cases; where both apply, cross-check they agree (gate G4).
- Reuse resonance4_solve.exact_count_field(rots, Field) — it is field-generic. Re-derive exact ψ/θ parameters from resonance4_solve.wl (RootReduce to minimal polynomials + isolating intervals), not from the report's identifying floats.
- Gates G1–G4 (field self-test incl. exact-zero detection; reproduce rational 175/151 through a degenerate field wrapper vs ./cube_regions_n; reproduce octahedral 67 via ℚ(√2) and one genuine ℚ(√5) count; cross-check two representations on one candidate) must ALL pass before any count is trusted.
- The tan ψ=(1+√13)/6 CHAIN candidate (ψ≈37.5°, subset {12,14,23,34}, the record's own tilt field) is the prime suspect — count it first.
- Dedupe by congruence (pairwise O-reduced invariants). Mark Δ=0 (coincident-cube) degenerate members. 
- RECORD PROTOCOL: anything ≥175 note it; anything ≥183 FLAG AT TOP and re-verify by the other representation (A vs B) or certified interval arithmetic with symbolic zero-guard, then a congruence check against the 183 record. Never edit six_cube_search_results.md or any validated file.

Use ≤4 cores, detached for long solves, don't idle on monitors (use background tasks and end your turn while compute runs; you'll be re-invoked on completion). Deliverables: opencount_report.md, opencount.py, opencount_results.jsonl.
```
