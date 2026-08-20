# Chase corner-handoff network

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-07-16T09:14:55 |
| Agent type | default |
| Model override | sonnet |
| Session | `c4196554-d37e-44f9-8da5-5d7210e1f156` |
| Tool-use id | `toolu_017iGJGGpaEydvhzRtKX4W8R` |
| Files named | `bigfamily.py`, `handoff_report.md`, `loopholes.py`, `pairmap.py`, `six_cube_search_results.md`, `trace10.py`, `window26.py` |
| Present in repo | `handoff_report.md` |
| Cited in LEDGER/RESULTS | `handoff_report.md` |

## Prompt as sent

```text
Execute the task specified in /Users/dmi/carroll/HANDOFF_SPEC.md: determine whether more than 18 physical edge-concurrence points can be carried continuously from the octahedral 3-cube compound to the golden one through the "big family" configuration space, allowing corner handoffs where a contact point switches edges at a cube vertex. Read the spec fully first — it defines the family, the contact/trajectory/handoff semantics, three hard gates (G1 consistency repair of a known pair-vs-triple count discrepancy, G2 baseline reproduction of the 18-carry and 26-window results, G3 handoff calibration through the golden point) that must pass before exploration counts, and the exploration plan (greedy wall rescue in the full 3-parameter space, backwards-from-golden, subset flood-fill). Background scripts are in /Users/dmi/carroll/dihedral_scratch/ (bigfamily.py, pairmap.py, loopholes.py, trace10.py, window26.py) and the ledger context is six_cube_search_results.md Postscript 25 + addenda (read-only — never edit it or any validated file). Write your report to /Users/dmi/carroll/handoff_report.md, scripts to dihedral_scratch/handoff_*.py. ≤4 cores, run detached, don't park on monitors. Report: gate results, the maximum end-to-end carried count found with witness path (or the obstruction picture if 18 stands), stated honestly as a lower bound plus local obstruction evidence.
```
