# Irrational search at n=4 and n=5

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-08-18T08:21:27 |
| Agent type | general-purpose |
| Model override | sonnet |
| Session | `833a739b-86d7-4754-94e1-446688dfcac3` |
| Tool-use id | `toolu_014Fsi3UDS3A5o9pDoF3fgip` |
| Files named | `dimension67.py`, `extend67.py`, `irrational_n45.json`, `irrational_n45.py` |
| Present in repo | `dimension67.py`, `extend67.py`, `irrational_n45.json`, `irrational_n45.py` |
| Cited in LEDGER/RESULTS | `dimension67.py`, `extend67.py`, `irrational_n45.json`, `irrational_n45.py` |

## Prompt as sent

```text
Write and run `/Users/dmi/cube-compounds/irrational_n45.py`. Work in that directory. This is a search campaign — implement as specified, run it, report what it finds.

# THE LEAD

n = 3 is the only level whose record (67) is IRRATIONAL — it lives in ℚ(√2) and ℚ(√5). That single fact makes it invisible to every extension-based search above it: 183 contains no 67, because every subset of a rational compound is rational. **Nothing rules out an irrational record at n = 4 or n = 5.** Every current record at those levels was found by rational search or by extension, so an irrational one would never have been seen.

Current records to beat: **n=4: 183**, **n=5: 393**.

# THE ENGINE

`./cube_regions_q2w --d D --quats-stdin` — one configuration per line, batch mode, exact arithmetic in ℤ[√D]. Component syntax `p:q` meaning p + q√D; a bare integer means q=0. Groups separated by `;`, components by `,`.

Example line (3 cubes, d=2): `1:0,0:0,0:0,0:0;1:0,1:0,0:1,0:0;-1:0,1:0,0:1,0:0`

Read `extend67.py` for a working example of the batch call and output parsing. Output is one JSON object per line with a `bounded` field. **A line that fails to parse means the engine REFUSED that input (overflow budget) — count those separately and report them; never treat a refusal as a low count.**

# KNOWN-ANSWER GATE (mandatory, run FIRST)

These must reproduce exactly before any search result is believed:
- d=2, the octahedral 67: `1:0,0:0,0:0,0:0;1:0,1:0,0:1,0:0;-1:0,1:0,0:1,0:0` → **67**
- d=5, the golden 67: `2:0,1:1,-1:1,0:0` as cubes 2 and 3 with `1:0,0:0,0:0,0:0` first, and `-2:0,1:1,-1:1,0:0` → **67**
- the rational n=4 record with d=0: quats `1,0,0,0;0,5,3,2;1,-4,-1,1;1,1,-1,-4` → **183**

If any gate fails, STOP and report; do not search.

# THE SEARCH

For n = 4 and n = 5, over fields d ∈ {2, 3, 5, 6, 7, 10, 13} (all squarefree):

1. **Random**: quaternion components p + q√d with p, q drawn from small ranges (try several magnitude caps — the ledger records that MENU SHAPE matters more than menu size, and that small-magnitude menus caused a record to stand for weeks). Always fix cube 0 as the identity `1:0,0:0,0:0,0:0` (global rotation is a gauge freedom — searching over it is wasted work).
2. **Seeded**: start from the two 67s (their quaternions are in `dimension67.py`, `RECORDS`) and add 1 or 2 further cubes drawn as above. This is *not* the same as `extend67.py`, which only perturbs within a fixed base — vary the added cubes widely.
3. **Hill-climb** from the best few found: perturb one component at a time by ±1 in p or q, keep improvements, iterate to a local max. Then **WIDE perturbation**: perturb SEVERAL cubes at once and re-climb. The ledger (Postscript 15) records that plain greedy climbing stalls but wide perturbation escapes — that is the operative technique and the reason 183 was found.

Budget your time to roughly 40 minutes total, split across fields and n. Batch aggressively (thousands of configurations per engine call).

# REPORTING — be strict

Write `irrational_n45.json` and log to `irrational_n45.log`. Report:
- per (n, d): configurations counted, engine refusals, best count found, and the configuration achieving it
- **whether anything reached or exceeded 183 (n=4) or 393 (n=5)**
- if something does: re-verify it independently by re-running that single configuration through the engine, and print the full quaternion list so it can be checked by hand

Do NOT claim a record without that independent re-verification. Report the best found even when it falls short — a ceiling that many methods hit is itself informative. State counts of refusals separately from counts of low results.

Report back: best count per (n, d), total counted, refusals, and whether any record was beaten.
```
