# Propagate new n=7/n=8 records

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-07-30T05:33:39 |
| Agent type | general-purpose |
| Model override | sonnet |
| Session | `c4196554-d37e-44f9-8da5-5d7210e1f156` |
| Tool-use id | `toolu_01JNQtg7yDQYa1VgCw3ttn6F` |
| Files named | `n7_program_report.md`, `six_cube_search_results.md` |
| Present in repo | `n7_program_report.md` |
| Cited in LEDGER/RESULTS | `n7_program_report.md` |

## Prompt as sent

```text
Mechanical documentation-update task in /Users/dmi/carroll (math research project counting bounded regions of n concentric unit cubes). Two new records were found and two-engine certified today (2026-07-29) by the main session. Do NOT re-derive or re-verify them, do NOT run any search or counting program.

HARD CONSTRAINTS: do NOT edit `six_cube_search_results.md` (the ledger — already updated by the main session, in both the top level and the `cubes/` mirror). Do not edit date-prefixed transcript files, `.jsonl`/`.json` data, or anything under `cb/` (a frozen old snapshot). `/Users/dmi/carroll/cubes/` IS a live byte-identical mirror of the top level — apply every edit to both copies.

## The new facts

N1. n=7 record: **1211** (previous 1207, +4).
    quats = 4,1,1,-1; 3,3,7,3; 5,-1,-5,-5; 2,1,1,1; 1,1,1,1; 5,2,2,2; 39,-5,-34,-31
    by_depth = {1:272, 2:328, 3:260, 4:190, 5:118, 6:42, 7:1}, total 1211, ≡ 3 mod 4.

N2. n=8 record: **1889** (previous 1879, +10).
    quats = the 1211 seven cubes plus 3,-4,4,4
    by_depth = {1:344, 2:454, 3:382, 4:302, 5:222, 6:136, 7:48, 8:1}, total 1889, ≡ 1 mod 4 (a parity exception; generic is 2n−1 ≡ 3 mod 4).

N3. Both are ±2 local maxima; all depth ceilings C(l,n) respected, with d7 = 48 = 6·8 attaining the l=1 ceiling.

N4. How found (worth one sentence where a document explains the nesting/extension principle): extending the 1207 record gave n=8 = 1887; its 7-subsets contained 1211, i.e. the n=7 record improved as a byproduct of searching n=8; re-extending 1211 upward then gave 1889. 1211 is a plateau — also reached independently by extending each of the three other known 723 realizations.

N5. No movement at n ≤ 6: the best 6-subset of 1211 is exactly 723, and 183/393/723 all stand. The record tower is now 183 → 393 → 723 → 1211 → 1889, still adjacent-by-one-cube.

N6. Full details are in the ledger's new **Postscript 45** — cite it as the source in any place where documents cite postscripts.

## Edits

E1. `README.md` "Current records" table: update the n=7 row (1207+ → **1211+**, description should reflect that it is a greedy/extension record from 723's family, now a plateau reached four ways) and the n=8 row (1879+ → **1889+**, extension of the 1211 record). Keep the table's column structure. If a growth-table or tower line appears elsewhere in README (e.g. "13/67/183+/393+/723/1207+/1879+"), update it too.

E2. `PROJECT.md`: there is a table row around line 710 reading `| best bounded pieces | 13 | 67 | 183+ | 393+ | 723 | 1207+ | 1879+ |` — update the last two entries. Then grep PROJECT.md for every other mention of 1207 or 1879 and update those that state the current record (leave dated/historical narrative that describes what was true at the time, adding a brief "(now 1211 / 1889, Postscript 45)" parenthetical instead of rewriting).

E3. Grep the remaining project `.md` files (top level only, plus the `cubes/` mirror) for `1207` and `1879` and apply the same rule: update live "current record" statements; annotate rather than rewrite historical/dated sections. Files likely to hit: JOURNEY.md, n7_program_report.md, NPLUS_SPEC.md, C45_notes.md. Note `n7_program_report.md` is a dated report of a completed run — annotate, do not rewrite its results.

E4. Where a document explains the nesting/extension principle (JOURNEY.md and PROJECT.md both do), add one short sentence recording N4's round trip (n=7 record → n=8 → better n=7 → better n=8), since it is the cleanest instance of that principle the project has produced.

Keep every edit minimal and in the surrounding document's voice. Do not invent numbers beyond N1–N5.

## Report back
Every file changed with before/after for each edit, plus any 1207/1879 mention you deliberately left alone and why.
```
