# Build (1,1,1,1) wall gradients

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-08-18T02:48:46 |
| Agent type | general-purpose |
| Model override | sonnet |
| Session | `833a739b-86d7-4754-94e1-446688dfcac3` |
| Tool-use id | `toolu_01NBQ2JfWEF5AYeZaHbGJLRT` |
| Files named | `check_4cube_walls.json`, `dimension.py`, `quad_walls.json`, `quad_walls.py` |
| Present in repo | `check_4cube_walls.json`, `dimension.py`, `quad_walls.json`, `quad_walls.py` |
| Cited in LEDGER/RESULTS | `check_4cube_walls.json`, `dimension.py`, `quad_walls.json`, `quad_walls.py` |

## Prompt as sent

```text
Write `/Users/dmi/cube-compounds/quad_walls.py`. This is a fully specified task — do not redesign it, and do not explore alternatives. Work in that directory.

# GOAL

Compute one integer per n: **δ = rank added to the wall Jacobian by the (1,1,1,1) wall type**, for the records n=6,7,8,9.

# BACKGROUND (do not re-derive)

`dimension.py` builds wall conditions from pairs and triples of cubes, so it structurally cannot express the "(1,1,1,1)" codimension-1 wall type = four face planes from four DIFFERENT cubes concurrent. Those walls exist at the records. So the measured rank is a lower bound. δ is how much rank they add.

# INPUTS ALREADY COMPUTED — USE THEM, DO NOT RECOMPUTE

`/Users/dmi/cube-compounds/check_4cube_walls.json` already lists the real (1,1,1,1) points: keys are n ("5".."9"), each has `quad`: a list of `{"point": [3 rational strings], "cubes": [4 cube indices]}`. There are 12 per n, identical across n. Load these; do NOT re-enumerate concurrency points.

The record configurations (quaternion tuples, cube 0 first):
'''python
BASE=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
R={5:BASE,6:BASE+[(7,14,1,-5)]}
R[7]=R[6]+[(4,-3,-4,-4)]; R[8]=R[7]+[(24,-24,24,-61)]; R[9]=R[8]+[(56,56,55,56)]
'''

# THE CONDITION

A face plane of cube c has equation `m · x = 1` where m is a signed column of cube c's rotation matrix (6 planes per cube: 3 columns × 2 signs). Four planes with normals m1..m4 are concurrent iff

    det [[m1x,m1y,m1z,-1],[m2x,m2y,m2z,-1],[m3x,m3y,m3z,-1],[m4x,m4y,m4z,-1]] == 0

That determinant, as a symbolic expression in the Cayley coordinates, IS the wall condition. Its gradient is the row to add to the Jacobian.

# HOW TO MATCH EXISTING CONVENTIONS (critical — copy these exactly)

'''python
import dimension as D, sympy as sp
D.set_field(0); D.QZERO[:]=[quats[0]]
pt = D.point_of(quats)                    # Cayley coords, cube 0 FROZEN as gauge
ncols = 3*(len(quats)-1)
vars_ = sp.symbols('c0:%d'%ncols)
Rs = D.frames(vars_, quats[0])            # Rs[c] is cube c's rotation matrix, symbolic
subs = {v: sp.Rational(p.numerator,p.denominator) for v,p in zip(vars_,pt)}
'''
Cube c's signed face normals in the WORLD frame are the columns of `Rs[c]`, both signs: `[Rs[c][r,k] for r in range(3)]` and its negation, for k in 0,1,2.

Existing ≤3-cube walls, for the rank comparison:
'''python
tight,_ = D.cached_conditions(Rs, len(quats), vars_, pt, D.quats_of(pt,quats[0]), quats[0])
good = [t for t in tight if not t['degenerate']]
# dedupe by gradient up to positive scale:
def _norm(g):
    piv = next((x for x in g if x!=0), None)
    return tuple(str(x/piv) for x in g) if piv is not None else None
'''
Rank via `len(D.nullspace(rows, ncols))`: rank = ncols - len(nullspace). Gradients must be `fractions.Fraction`, matching `t['grad']`.

# ALGORITHM

For each n in 6,7,8,9:
1. Load the 12 points for that n from check_4cube_walls.json.
2. For each point P and its 4 cubes: find WHICH signed normal of each of the 4 cubes gives a plane through P — i.e. the m with `m·P == 1` exactly (use exact sympy Rationals, never floats). If a cube has more than one such normal, take each combination.
3. Build the 4×4 determinant expression symbolically from those four normals.
4. **GATE (mandatory): evaluate the determinant at `subs`. It MUST be exactly 0.** If it is not, you have the wrong planes — report it and stop; do not proceed to gradients. This is the check that the condition is actually satisfied at the record.
5. Gradient = `[F(sp.Rational(sp.expand(sp.diff(expr,v).subs(subs)))) for v in vars_]`. Discard identically-zero gradients, counting how many were zero.
6. rank_old = rank of the deduped ≤3-cube walls. rank_new = rank of those plus the new gradients. **δ = rank_new − rank_old.**

# CORRECTNESS ORACLE — THIS IS THE POINT OF THE TASK

It is PROVED that **δ ≤ 1**. (Lineality at n=6 is 1 and cannot go negative.) So:
- δ ∈ {0,1} → plausible, report it.
- **δ ≥ 2 → YOUR CODE IS WRONG.** Do not report δ≥2 as a result. Investigate and say what you found.
Also expect δ(6) ≥ δ(7) ≥ δ(8) ≥ δ(9), since the n=6 walls all lift into higher n.

# OUTPUT

Print per n: number of conditions built, number with zero gradient, rank_old, rank_new, ambient, lineality_old, lineality_new, δ. Write the same to `quad_walls.json`. Log to `quad_walls.log`.

# CONSTRAINTS

- Exact arithmetic only. No floats anywhere, no `limit_denominator`, no `evalf`.
- Do not modify `dimension.py` or any existing file. Create only `quad_walls.py` and its outputs.
- If sympy is slow, that is acceptable; correctness first. n=9 has ambient 24 and may take a while.
- Put a module docstring explaining WHY this exists (the Jacobian's blindness to this wall type) and what δ means.

Report back: the δ per n, whether the mandatory gate passed at every point, and any place where the code disagreed with the oracle.
```
