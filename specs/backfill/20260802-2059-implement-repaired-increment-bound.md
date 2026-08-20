# Implement repaired increment bound

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-08-02T20:59:19 |
| Agent type | general-purpose |
| Model override | sonnet |
| Session | `c4196554-d37e-44f9-8da5-5d7210e1f156` |
| Tool-use id | `toolu_01MYo9pakjLEayNLEA57yM5K` |
| Files named | `increment_bound.py`, `increment_bound2.py`, `increment_bound2_report.md`, `six_cube_search_results.md` |
| Present in repo | `increment_bound.py`, `increment_bound2.py`, `increment_bound2_report.md` |
| Cited in LEDGER/RESULTS | `increment_bound.py`, `increment_bound2.py`, `increment_bound2_report.md` |

## Prompt as sent

```text
Working directory: /Users/dmi/carroll

Read /Users/dmi/carroll/INCREMENT_BOUND_SPEC.md in full and implement exactly what it specifies: a new file `increment_bound2.py` computing the bound B_j by formula (*), plus the four gates G1-G4, plus the report `increment_bound2_report.md`.

Context you need:
- `increment_bound.py` in the same directory is the FAILED earlier attempt. Reuse its `mat()` (exact rational rotation matrix from an integer quaternion) and its CONFIGS dict and its `count()` helper (which shells out to `./cube_regions_n --quats "w,x,y,z;w,x,y,z;..."` and reads the `bounded` field of the JSON on stdout). Do NOT modify that file.
- Exact arithmetic only: `fractions.Fraction`. No float may ever decide a comparison. This is the whole point — the earlier attempt failed precisely at tangency, where a float would be worthless.
- The spec's section 1 gives the algorithm step by step, including which degeneracies to DROP (tangent planes, with a tally) and which to FLAG and refuse to bound (arc overlap).

Gate discipline: G1 is a hand-computed case with a known answer (B = 12, c = 1, two degree-6 vertices, six degree-4 vertices, at eight named points). If your code does not reproduce it, do not adjust the gate or the expected value to match your code — report the mismatch, with the vertex list your code produced, and stop. The same for G2: if any row has B_j < Delta_j the bound is refuted and that is a legitimate, valuable result to report; do not paper over it.

Runtime: the n=6 cases have 30 planes and ~435 plane pairs per j, all exact rational — this should be seconds, not minutes. If something takes more than a couple of minutes, say so rather than waiting indefinitely.

When done, reply with: the G2 table verbatim, the G1 and G3 verdicts, the slack distribution, and any degeneracy flags. Do not edit six_cube_search_results.md or any other .md file except the report you are asked to write.
```
