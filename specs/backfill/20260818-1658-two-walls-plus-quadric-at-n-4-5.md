# Two walls plus quadric at n=4/5

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-08-18T16:58:45 |
| Agent type | general-purpose |
| Model override | sonnet |
| Session | `833a739b-86d7-4754-94e1-446688dfcac3` |
| Tool-use id | `toolu_01G28rKWD8EzueN3NiHsBQSp` |
| Files named | `base_points.py`, `irrational_probe.py`, `locus_linear.py`, `qfield.py`, `two_plus_quadric.json`, `two_plus_quadric.py` |
| Present in repo | `base_points.py`, `irrational_probe.py`, `locus_linear.py`, `qfield.py`, `two_plus_quadric.json`, `two_plus_quadric.py` |
| Cited in LEDGER/RESULTS | `base_points.py`, `irrational_probe.py`, `locus_linear.py`, `qfield.py`, `two_plus_quadric.json`, `two_plus_quadric.py` |

## Prompt as sent

```text
Write and run `/Users/dmi/cube-compounds/two_plus_quadric.py`. Work in that directory. **Run it to completion in the foreground and report the numbers — do not background the work and wait for a monitor.**

# THE LEAD, AND WHY IT IS THE ONLY ONE LEFT

The n=3 record 67 is IRRATIONAL. Searching for irrational records has failed three ways, each for a now-understood reason:

1. **Random sampling fails structurally.** Walls are codimension 1 and records sit at wall intersections, so drawing from an open set hits a measure-zero target with probability 0. Measured: 15 663 configurations across 7 fields reached only 137–177 at n=4 (record 183).
2. **Three-wall solving cannot produce irrational points against a rational base.** Every wall then has rational coefficients, so every three-plane intersection is rational. Measured: **0 irrational roots out of 2 451** over 400 systems (`irrational_probe.py`). Corollary, nearly a theorem: *a cube on ≥3 independent walls against a rational base is necessarily rational, so irrational candidates carry AT MOST TWO coincidences.*
3. **Maximal subset spectrum is not maximal count.** A 4-cube compound with all four triples = 67 and all six pairs = 13 exists and counts **177**, six BELOW the 183 record.

**What remains — and this is what you are building.** Two rational planes leave a rational LINE; a QUADRIC along that line gives a quadratic in one parameter whose roots are rational or in ℚ(√d). This is how every irrational 727 arose and how the 67s arise. **Irrationality is an OUTPUT of wall solving, not an input to sample over.**

# REUSE, DO NOT REWRITE

- `locus_linear.py` — read it first. It does exhaustive three-wall enumeration on the 393 base by linear algebra, exploiting that edge-edge conditions factor into **pairs of rational planes**. Its plane-extraction is what you want for the two-plane half.
- `base_points.py` — `planes(cfg)`, `mat(q)`, `solve3`, `in_cube`; also builds the real triple points and crossing lines of a base.
- `qfield.py` — exact ℚ(√d) arithmetic: `Q(a,b,d)`, exact `sign()`, `rot()`, `clear_denoms()`.
- Engine: `./cube_regions_q2w --d D --quats-stdin`, component syntax `p:q`, batch one config per line. An unparseable output line means the engine REFUSED that input — count refusals separately, NEVER as a low count.

# THE CONSTRUCTION

For a fixed rational base (do BOTH of these):
- **n=4 target 183**: base = a 3-cube rational configuration. Use the three cubes of the 183 record `1,0,0,0;0,5,3,2;1,-4,-1,1` (drop its fourth), and also a 13-pair extended by one cube.
- **n=5 target 393**: base = the four cubes `4,1,1,-1;3,3,7,3;5,-1,-5,-5;2,1,1,1`.

Then, for the FREE cube with Cayley coordinates (a,b,c) ∈ ℚ³:
1. Enumerate the **linear** (plane) conditions — the factored edge-edge walls, as `locus_linear.py` does.
2. Choose PAIRS of independent planes → each pair determines a rational LINE, parameterised exactly as `P0 + t·D` with rational `P0, D`.
3. Enumerate the **quadric** conditions (corner-on-face type — irreducible, not factoring into planes).
4. Substitute the line into each quadric → a quadratic `αt² + βt + γ = 0` with rational coefficients. Its discriminant `Δ = β² − 4αγ`:
   - Δ a perfect square → rational roots (already reachable; count them anyway for comparison)
   - **Δ NOT a perfect square → t ∈ ℚ(√d) with d = squarefree part of Δ. THESE ARE THE TARGETS.**
5. For each irrational root, build the free cube's quaternion over ℤ[√d] (clear denominators exactly with `qfield.clear_denoms`) and count the full configuration with the field engine at that d.

# MANDATORY GATES (run FIRST; if any fails, STOP and report)

- `./cube_regions_n --quats '1,0,0,0;0,5,3,2;1,-4,-1,1;1,1,-1,-4'` → **183**
- `./cube_regions_q2w --d 2 --quats '1:0,0:0,0:0,0:0;1:0,1:0,0:1,0:0;-1:0,1:0,0:1,0:0'` → **67**
- At least one line-meets-quadric solve must reproduce a KNOWN configuration count, or you must report that no such control was found.

# REPORT — be strict

Write `two_plus_quadric.json`, log to `two_plus_quadric.log`:
- how many plane conditions, quadric conditions, and (line, quadric) systems were formed
- how many gave rational roots vs **irrational** roots, and the distribution of squarefree parts d
- the count distribution over all configurations built, rational and irrational separately
- **best count found, and whether anything reaches or exceeds 183 (n=4) / 393 (n=5)**
- engine refusals, counted separately with their reasons if available

If anything reaches or exceeds a record, re-verify that single configuration independently and print its full quaternion list. Do not claim a record on one engine call.

Report back: number of irrational roots found, the d values, best count per target, and whether any record was reached.
```
