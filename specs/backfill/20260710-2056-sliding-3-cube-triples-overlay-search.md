# Sliding 3-cube triples overlay search

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-07-10T20:56:56 |
| Agent type | general-purpose |
| Model override | sonnet |
| Session | `c4196554-d37e-44f9-8da5-5d7210e1f156` |
| Tool-use id | `toolu_01BuqtgX7fz3nkPYyMw12NZo` |
| Files named | `six_cube_search_results.md`, `slide3_report.md` |
| Present in repo | `slide3_report.md` |
| Cited in LEDGER/RESULTS | `slide3_report.md` |

## Prompt as sent

```text
Working directory: /Users/dmi/carroll. Exact cube-compound region-counting project. Your complete brief is SLIDE3_SPEC.md — read it and the files it lists, then execute in order: section 0 (verify/pin down the sliding 3-cube family connecting the octahedral 3-compound and the golden dodecahedral triple — verify the user's premise, don't assume it), section 1 (overlay search: two triples, slide θ₁/θ₂, relative rotation R; gates S1/S2 first; phases P1 coarse map → P2 climb → P3 constraint-first alignment walls → P4 snap-and-verify), section 2 (chart the landscape for handover — this mapping deliverable matters as much as the record hunt). Write slide3_report.md + slide3_search.jsonl; never edit six_cube_search_results.md or validated files; ≤4 cores. Final message: verdict on the family premise (with θ* identified exactly if it exists), best overlay total vs records 681/655/635 with quats, the two or three most promising mapped regions with their active constraints, and what a follow-on agent should do first.
```
