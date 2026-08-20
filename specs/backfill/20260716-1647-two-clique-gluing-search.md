# Two-clique gluing search

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-07-16T16:47:50 |
| Agent type | default |
| Model override | sonnet |
| Session | `c4196554-d37e-44f9-8da5-5d7210e1f156` |
| Tool-use id | `toolu_01TZcv6wK7jjVw5XAzxgqm6b` |
| Files named | `glue_report.md`, `glue_search.py`, `nfamily_common.py`, `six_cube_search_results.md` |
| Present in repo | `glue_report.md`, `glue_search.py`, `nfamily_common.py` |
| Cited in LEDGER/RESULTS | `glue_report.md`, `nfamily_common.py` |

## Prompt as sent

```text
Execute the task specified in /Users/dmi/carroll/GLUE_SPEC.md: search the space of glued family cliques (two cliques of cubes on different axes, each clique internally in the dihedral family, glued by a rational rotation G) at n=4/5/6 to see whether it reaches or beats the records 183/393/723. Read the spec fully first. Critical first step Q0: determine whether the 393 and 183 records are themselves SINGLE-AXIS family members (the earlier test was per-pair axis-agnostic; if all pairs share one global axis, Postscript 26's "family can't reach records" conclusion flips to "the sweep menu was too coarse" — flag prominently). Then gates G1 (two-engine agreement), G2 (reproduce 723), G3 (reconstruct 723 as a gluing), then the sweep with hill-climbing. Reuse the exact machinery in /Users/dmi/carroll/nfamily_common.py and the C++ engine ./cube_regions_n. Anything beating a record: verify with certify_six.exact_count_config immediately and flag at the top of the report — never edit six_cube_search_results.md or validated files. Write glue_report.md, glue_search.py, glue_results.jsonl to /Users/dmi/carroll. ≤4 cores, detached long runs, interim results into the report as you go. Report back: Q0 answer, gate results, best per (n, clique-sizes) with quats and depth profiles, honest coverage.
```
