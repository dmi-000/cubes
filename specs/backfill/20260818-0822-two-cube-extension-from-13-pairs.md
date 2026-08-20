# Two-cube extension from 13-pairs

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-08-18T08:22:01 |
| Agent type | general-purpose |
| Model override | haiku |
| Session | `833a739b-86d7-4754-94e1-446688dfcac3` |
| Tool-use id | `toolu_01CMv8W7ReqrdTEtwjT2pVYP` |
| Files named | `twocube_n4.json`, `twocube_n4.py` |
| Present in repo | `twocube_n4.json`, `twocube_n4.py` |
| Cited in LEDGER/RESULTS | `twocube_n4.py` |

## Prompt as sent

```text
Write and run `/Users/dmi/cube-compounds/twocube_n4.py`. Work in `/Users/dmi/cube-compounds`. A search campaign — implement as specified, run it, report findings.

# THE LEAD

The record tower breaks exactly once, at n = 3, for an arithmetic reason: the n=3 record 67 needs irrational coordinates, so the rational n=4 record 183 cannot contain it (every subset of a rational compound is rational). One-cube extension from n = 3 therefore cannot reach 183.

**But two-cube extension from n = 2 can.** 183 contains THREE 13-pairs, and 13 is the proven n = 2 maximum. So the route that bridges the break is: start from a 13-pair, add two cubes.

This searches that route systematically. Target to beat: **183**.

# THE n=2 MAXIMISERS

13 is achieved on a CONTINUUM: any rotation about a shared body diagonal. So a 13-pair is `1,0,0,0` together with a quaternion of the form `(w, t, t, t)` — a rotation about the (1,1,1) axis. Verify this: `./cube_regions_n --quats '1,0,0,0;3,1,1,1'` should count **13**. There is also a second family, a closed arc about an EDGE axis — `(w, t, t, 0)` type, e.g. `4,3,3,0`. Check that too and use both.

# THE ENGINE

For throughput: `./cube_regions_q2w --d 0 --quats-stdin`, one configuration per line, `w,x,y,z` groups separated by `;`. Batch thousands per call. Output is one JSON per line with a `bounded` field. **An unparseable line means the engine REFUSED that input (overflow budget) — count those separately and never treat a refusal as a low count.**

# KNOWN-ANSWER GATE (run FIRST, mandatory)

- `1,0,0,0;3,1,1,1` → **13**
- `1,0,0,0;4,3,3,0` → **13**
- `1,0,0,0;0,5,3,2;1,-4,-1,1;1,1,-1,-4` → **183**

If any fails, STOP and report.

# THE SEARCH

For each of several 13-pair bases (vary the second cube over the diagonal family `(w,t,t,t)` and the edge family, with small integer parameters — at least 10 distinct bases):

Add TWO further cubes with integer quaternion components drawn from a magnitude cap varied per batch over {2, 3, 4, 6, 9}. Cube 0 stays `1,0,0,0` (global rotation is a gauge freedom). Count in large batches.

Then hill-climb the best few: perturb one component by ±1, keep improvements, iterate.

Budget roughly 35 minutes.

# REPORTING — be strict

Write `twocube_n4.json`, log to `twocube_n4.log`:
- per base: how many counted, engine refusals, best count found
- the overall best configuration, printed in full
- **whether anything reached or exceeded 183**
- the distribution of counts (a histogram), not just the maximum

If anything reaches or exceeds 183, re-verify that single configuration through BOTH `./cube_regions_n` and `./cube_regions_q2w --d 0` and report both. Do not claim a record on one engine.

Report back: best per base, overall best, refusal count, and whether 183 was reached or beaten.
```
