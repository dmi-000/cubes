# Census extraction from 67 witnesses

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-07-18T00:41:49 |
| Agent type | default |
| Model override | sonnet |
| Session | `c4196554-d37e-44f9-8da5-5d7210e1f156` |
| Tool-use id | `toolu_01Fx89sZh76TVDp4piJRjpTv` |
| Files named | `census_data.json`, `census_extract.py`, `census_report.md`, `six_cube_search_results.md` |
| Present in repo | `census_data.json`, `census_extract.py`, `census_report.md` |
| Cited in LEDGER/RESULTS | `census_data.json`, `census_extract.py`, `census_report.md` |

## Prompt as sent

```text
Execute /Users/dmi/carroll/CENSUS_SPEC.md — the (c1) exact census data extraction from both n=3 record witnesses (octahedral ℚ(√2) and golden ℚ(√5)), feeding lemma L2.c of the max(3)=67 proof plan in C45_notes.md §13. Working directory /Users/dmi/carroll. Read the spec first; it is self-contained. Key discipline: every decision in exact field arithmetic (no floats in comparisons); gates G1 (reproduce both 67 counts) and G2 (Euler face counts 48 top / 18 bottom for BOTH witnesses) must pass before the census tables count as deliverable. If your exact numbers contradict §13's projected "46 triples × 2 = 92" arithmetic, report the discrepancy prominently — the data corrects the projection. Never edit six_cube_search_results.md or validated files. Deliverables: census_report.md, census_extract.py, census_data.json.
```
