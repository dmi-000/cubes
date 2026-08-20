# Rational-tangent family sweep

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-07-17T06:48:48 |
| Agent type | default |
| Model override | sonnet |
| Session | `c4196554-d37e-44f9-8da5-5d7210e1f156` |
| Tool-use id | `toolu_01NYAZQ36Gjxf1EsRo3mE2hC` |
| Files named | `nfamily_common.py`, `rattan_report.md`, `rattan_sweep.py`, `six_cube_search_results.md` |
| Present in repo | `nfamily_common.py`, `rattan_report.md`, `rattan_sweep.py` |
| Cited in LEDGER/RESULTS | `nfamily_common.py`, `rattan_report.md`, `rattan_sweep.py` |

## Prompt as sent

```text
Execute the task specified in /Users/dmi/carroll/RATTAN_SPEC.md: sweep the rational-tangent slice of the single-axis cube family (tilts tanψ = q/p with conic-parametrized phase steps keeping everything integer-quaternion) at n=4/5/6 — the slice the records actually live in per Postscript 27 — including the targeted record-clique completion runs (fixed exact 4-clique {1,2,3,4} of the 393 record + swept extra cubes; 183's triply-resonant triple {0,2,3} + a 4th cube). Read the spec fully first: it defines the conic parametrization (gate G0), the sharp reproduction gate G1 (the sweep space must provably contain 393's own clique), two-engine gate G2, record-reproduction gate G3, the sweep tiers, and the record protocol (anything > record or = record non-congruent: oracle-verify immediately, flag at top, never edit six_cube_search_results.md or validated files). Reuse /Users/dmi/carroll/nfamily_common.py and ./cube_regions_n. Write rattan_report.md, rattan_sweep.py, rattan_results.jsonl to /Users/dmi/carroll. ≤4 cores, detached, interim findings into the report as you go. Report back: gate results, best per n, and whether the exactly-8 deficit floor closes.
```
