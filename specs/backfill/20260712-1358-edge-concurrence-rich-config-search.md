# Edge-concurrence-rich config search

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-07-12T13:58:18 |
| Agent type | general-purpose |
| Model override | sonnet |
| Session | `c4196554-d37e-44f9-8da5-5d7210e1f156` |
| Tool-use id | `toolu_011GXMjrxgqUL7nACU8GPNFM` |
| Files named | `certify_six.py`, `cube_compound_exact.py`, `edge_search.py`, `edge_search_report.md`, `exact_search.py`, `six_cube_search_results.md`, `slide3_q2.py` |
| Present in repo | `certify_six.py`, `cube_compound_exact.py`, `edge_search.py`, `edge_search_report.md`, `exact_search.py`, `slide3_q2.py` |
| Cited in LEDGER/RESULTS | `certify_six.py`, `cube_compound_exact.py`, `edge_search.py`, `edge_search_report.md`, `exact_search.py`, `slide3_q2.py` |

## Prompt as sent

```text
Working directory: /Users/dmi/carroll. Exact cube-compound region-counting project. Read first: ALGEBRAIC_SEARCH.md, six_cube_search_results.md Postscripts 11-12, README.md, and slide3_q2.py (the exact ℚ(√2) counter). Current record: 723.

CONTEXT: We proved the two 3-cube maxima use different incidence modes — the OCTAHEDRAL 3-compound {Rx(45°),Ry(45°),Rz(45°)} uses EDGE concurrences (points where 4 planes meet = 2 from one cube + 2 from another = an edge crossing an edge, at |x|²≈2), while the DODECAHEDRAL/golden 3-compound uses CORNER concurrences (6 planes = 3+3 = corners coinciding, |x|²=3). Every 6-cube record we have (717, 723) is CORNER-dominated (top concurrence is 9-fold = three cubes sharing a corner). The open question: can an EDGE-dominated 6-cube config match or beat 723?

YOUR TASK: search for edge-concurrence-rich 6-cube configurations and test whether they are competitive with 723.

Build an incidence analyzer (reuse the exact rational one — quaternion→rational face normals, group triples of the 36 planes by common point, tally per-cube plane signatures at each point: a "2+2" 4-fold point = edge crossing, a "3+3" or "3+3+3" point = corner coincidence). For any candidate config report: total regions (via ./cube_regions), the max concurrence multiplicity and its signature, and counts of edge-type (2+2) vs corner-type (≥3+3) points — an "edge-dominance" measure.

Two search fronts:
1. OCTAHEDRAL-BASED family (ℚ(√2)): two octahedral 3-compounds combined — {Rx(45),Ry(45),Rz(45)} and a relatively-rotated copy R·{...}. Count exactly with slide3_q2.py's ℚ(√2) engine (extend it if needed; do NOT modify validated files — copy the counter into a new edge_search.py). Also try rational Pythagorean-angle approximations to 45° so ./cube_regions applies (edges can cross rationally, not only at exactly 45°). Search the relative rotation R and the approximation.
2. RATIONAL edge-maximizing hunt: random + hill-climb rational 6-cube configs, but rank/select by EDGE-concurrence richness (number and multiplicity of 2+2 points), and among edge-rich configs report the region totals. Does edge-richness correlate with high totals? Do any edge-dominated configs reach 723?

HARD RULES: exact arithmetic only in predicates; do NOT modify validated files (slide3_q2.py, cube_compound_exact.py, certify_six.py, exact_search.py, symmetry_search*.py) or six_cube_search_results.md; exact_search_results.jsonl read-only; ≤4 cores; run searches detached and write your report at the end rather than parking on monitors. Flag any total>723 immediately. Deliverables: edge_search.py, edge_search.jsonl, edge_search_report.md. Final message: best edge-dominated total vs 723, whether edge-richness correlates with region count, the octahedral-family best, and a verdict on whether an edge-dominated 6-cube config is competitive (which bears on the conjecture that a maximum could substitute edge for corner concurrences).
```
