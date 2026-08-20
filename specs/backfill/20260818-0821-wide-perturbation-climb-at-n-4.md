# Wide-perturbation climb at n=4

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-08-18T08:21:43 |
| Agent type | general-purpose |
| Model override | sonnet |
| Session | `833a739b-86d7-4754-94e1-446688dfcac3` |
| Tool-use id | `toolu_013s5FTHhzyByBZAPurcJ9Ji` |
| Files named | `wideclimb_n4.json`, `wideclimb_n4.py` |
| Present in repo | `wideclimb_n4.json`, `wideclimb_n4.py` |
| Cited in LEDGER/RESULTS | `wideclimb_n4.json`, `wideclimb_n4.py` |

## Prompt as sent

```text
Write and run `/Users/dmi/cube-compounds/wideclimb_n4.py`. Work in that directory. A search campaign — implement as specified, run it, report findings.

# THE LEAD

The n = 4 record **183** is the level this project has least confidence in. It was found (Postscript 15 in `LEDGER.md` — read it) by a chain of SIX basin escapes: 159 → 171 → 173 → 175 → 179 → 183. A 200 000-configuration random campaign reached only **137**, and plain ±1/±2 greedy climbing stalls below 177. The ledger states: *"wide (multi-component) perturbation + re-climb escapes each local max into a richer basin — the wide-perturbation escape is the operative technique"*.

Six escapes each found a richer basin. There is no principled reason the sixth was the last. **Re-run that technique far more aggressively.**

Target to beat: **183** (rational, quats `1,0,0,0;0,5,3,2;1,-4,-1,1;1,1,-1,-4`).

# THE ENGINE

`./cube_regions_n --quats 'w,x,y,z;...'` for integer quaternions with all |component| ≤ 512; beyond that use `./cube_regions_q2w --d 0 --quats '...'`. For throughput prefer `./cube_regions_q2w --d 0 --quats-stdin` with one configuration per line — batch thousands per call. Output is one JSON per line with a `bounded` field; an unparseable line means the engine REFUSED the input (overflow budget) — count those separately, never as a low score.

# KNOWN-ANSWER GATE (run FIRST, mandatory)

`1,0,0,0;0,5,3,2;1,-4,-1,1;1,1,-1,-4` must count **183**. If not, STOP and report.

# THE ALGORITHM

Always fix cube 0 = `1,0,0,0` (global rotation is a gauge freedom).

Repeat many independent restarts (aim for several hundred):
1. **Random start**: 3 free cubes, integer components drawn from a magnitude cap chosen per restart from {2, 3, 4, 6, 9, 12, 20} — vary it, since the ledger records that MENU SHAPE matters more than menu size.
2. **Narrow climb**: perturb ONE component of ONE cube by ±1 or ±2, accept improvements, iterate to a local maximum.
3. **WIDE escape** (the operative step): perturb SEVERAL cubes simultaneously — 2 or 3 of them, each by a random vector with components in ±1..±4 — then re-climb narrowly. Accept if the new local max beats the old.
4. Repeat step 3 until some number of consecutive wide escapes (say 15) fail to improve. Record the final value and configuration.

Track the **distribution of local maxima reached**, not only the best — how often each plateau value occurs is the informative statistic, and it tells us whether 183 is a common attractor or a rare one.

Budget roughly 40 minutes.

# REPORTING — be strict

Write `wideclimb_n4.json`, log to `wideclimb_n4.log`:
- histogram of final local-maximum values over all restarts
- how many restarts reached 183, and how many exceeded it
- the best configuration found, printed in full
- engine refusals, counted separately
- the escape-chain length distribution (how many wide escapes improved before stalling)

**If anything exceeds 183**: re-verify that single configuration independently through BOTH `./cube_regions_n` and `./cube_regions_q2w --d 0`, and report both counts. Do not claim a record on one engine.

Report back: the histogram, how often 183 was reached, whether anything beat it, and the best configuration.
```
