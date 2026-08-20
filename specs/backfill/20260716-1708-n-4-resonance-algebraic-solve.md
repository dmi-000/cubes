# n=4 resonance algebraic solve

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-07-16T17:08:16 |
| Agent type | default |
| Model override | sonnet |
| Session | `c4196554-d37e-44f9-8da5-5d7210e1f156` |
| Tool-use id | `toolu_01RjLtJzVDCsgZdRsAwiu3TN` |
| Files named | `nfamily_common.py`, `resonance4_report.md`, `resonance4_solve.py`, `six_cube_search_results.md` |
| Present in repo | `nfamily_common.py`, `resonance4_report.md`, `resonance4_solve.py` |
| Cited in LEDGER/RESULTS | `nfamily_common.py`, `resonance4_report.md`, `resonance4_solve.py` |

## Prompt as sent

```text
Execute the task specified in /Users/dmi/carroll/RESONANCE4_SPEC.md: derive the cross-class coincidence-alignment conditions of the dihedral family exactly, solve the non-uniform 4-cube resonance systems algebraically (Gröbner/resultants over the trig variables with c²+s²=1 relations; wolframscript is available and the algebraic_*.wl files show the established pattern), and exactly count every real candidate found, comparing against the family plateau 175, the record 183, and the cap 195. Read the spec fully first — it defines the Rel-gauge setup, the fundamental domain from the proved theorems, two hard gates (R1: the n=3 substitution Δ=120° must reproduce ψ=arcsin(1/√3) and ψ=arctan(φ²) as exact roots; R2: reproduce 67 through your field-engine ladder before counting new candidates), the field ladder for exact counting (C++ for rational, ℚ(√d) clone engines via the six-replacement recipe, qtower pattern for degree-4 towers, report-as-open for higher degree), and the record protocol (anything ≥183: second engine + flag at top; never edit six_cube_search_results.md or validated files). Reuse /Users/dmi/carroll/nfamily_common.py. Write resonance4_report.md, resonance4_solve.py (or .wl), resonance4_results.jsonl to /Users/dmi/carroll. ≤4 cores, detached long runs, interim findings into the report as you go. Report back: gate results, the resonance table (exact parameters, fields, counts, depth profiles), and the verdict on whether any n=4 family resonance reaches or beats 183.
```
