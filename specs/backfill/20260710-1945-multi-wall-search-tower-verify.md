# Multi-wall search + tower verify

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-07-10T19:45:49 |
| Agent type | general-purpose |
| Model override | sonnet |
| Session | `c4196554-d37e-44f9-8da5-5d7210e1f156` |
| Tool-use id | `toolu_014Wc9GLvHvoajetFTGWtybY` |
| Files named | `golden_six.py`, `multiwall_report.md`, `six_cube_search_results.md` |
| Present in repo | `golden_six.py`, `multiwall_report.md` |
| Cited in LEDGER/RESULTS | `golden_six.py`, `multiwall_report.md` |

## Prompt as sent

```text
Working directory: /Users/dmi/carroll. Exact cube-compound region-counting project. Your complete brief is the file MULTIWALL_SPEC.md — read it first and follow it exactly (it lists the other required reading: six_cube_search_results.md Postscripts 4-5 and 7 with update, QFIELD_SPEC.md, golden_six.py, golden_search.jsonl). Execute in the spec's priority order: tower gates W-G1..W-G4 → section 3 (exact count + incidence diagnosis of golden-five + 90°-about-(1,1,1), the ℚ(√3,√5) point) → M1 → M2 → M4 → M3. Hard rules from the spec: validated files and exact_search_results.jsonl untouched; write your findings to multiwall_report.md, never to six_cube_search_results.md; ≤4 cores; honest negatives welcome. Final message: gate pass/fail, the section-3 exact count vs the 681 plateau with the incidence diagnosis in plain geometry, and the best totals per search family with quats/params.
```
