# Enumerate extension chambers at 727

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-08-18T03:30:11 |
| Agent type | general-purpose |
| Model override | sonnet |
| Session | `833a739b-86d7-4754-94e1-446688dfcac3` |
| Tool-use id | `toolu_01MfQJGbz5smQh3dsiwtjiVU` |
| Files named | `extension_chambers.json`, `extension_chambers.py`, `isolation67.py`, `record_neighbours.py`, `size_local.py` |
| Present in repo | `extension_chambers.json`, `extension_chambers.py`, `isolation67.py`, `record_neighbours.py`, `size_local.py` |
| Cited in LEDGER/RESULTS | `isolation67.py`, `record_neighbours.py`, `size_local.py` |

## Prompt as sent

```text
Write `/Users/dmi/cube-compounds/extension_chambers.py`. Fully specified — implement it, do not redesign. Work in that directory.

# GOAL

The 727 record is the 393 five-cube base plus a sixth cube `(7,14,1,-5)`. Enumerate the **local chambers around that sixth cube's position** in its own 3-dimensional Cayley space, and report the exact region count in each. This is the first exact answer to "what can the sixth cube do".

# WHY THIS IS TRACTABLE (context, already measured — do not re-derive)

Extending a base by one cube is a 3-DIMENSIONAL problem: the base's own walls do not constrain the new cube. Against the fixed 393 base the new cube's walls form a finite catalogue (2544 W4 + 4320 W3 = 6864), but **only 12 are incident at the 727 point** — 4 W4 and 8 W3, measured by `size_local.py` (read it; reuse its functions rather than rewriting them). Twelve surfaces through a point in R^3 bound the local chambers at roughly a few hundred.

# INPUTS

- `size_local.py` — has `base_arrangement()` returning `(real_triple_points, crossing_lines, planes)` and `free_faces_edges(q)`. **Import and reuse.** It also identifies which walls are incident; extend it to RETURN the incident ones, not just count them.
- Free cube Cayley point: `dimension.cayley_of((7,14,1,-5))`. Base: `FIVE` from `base_points`.
- Counting engine: use `epscount.count_eps(pt, direction, 0, q0)` where `pt` is the FULL configuration's Cayley coordinates and `q0` the frozen cube 0 — see `record_neighbours.py` for the exact calling convention. This uses an infinitesimal step, so there is no step size to choose.

# ALGORITHM

1. Get the 12 incident walls. For each, compute its **gradient at the free cube's Cayley point** — a vector in R^3 (the free cube's 3 coordinates only). Do this exactly:
   - W4 wall (free face plane through fixed base point p): the condition is `m(c)·p − 1 = 0` where `m(c)` is the free cube's face normal as a function of its 3 Cayley coordinates c. Build symbolically with sympy from `dimension.cayley_matrix(c)`, substitute the point, differentiate.
   - W3 wall (free edge meets fixed base line): the condition is the 3x3 determinant `det[D(c), d, W(c)] = 0` where `D(c)` is the edge direction, `d` the fixed line direction, `W(c)` the vector between a point on each. Same treatment.
   - **GATE (mandatory): each condition must evaluate to EXACTLY 0 at the free cube's point** — that is what "incident" means. If any does not, you have the wrong wall; report and stop.
2. Enumerate the sign vectors (faces) of these ~12 gradients in R^3, exactly, using the Fourier–Motzkin routine `faces()` in `isolation67.py` (import it; it takes `(walls, ncols, zero, log)` and returns `(sigma, witness_direction)` pairs). ncols = 3 here.
3. For each face, take its witness direction, embed it into the FULL configuration's coordinate space as a direction moving ONLY the sixth cube (zeros in the other 12 coordinates), normalise with `dimension.normalize_dir`, and count with `count_eps`.
4. Report a histogram of counts over faces, the best count found, and the sign vector + direction achieving it.

# WHAT TO REPORT

Print and write to `extension_chambers.json`:
- number of incident walls, number of realizable faces
- histogram {count: number of faces}
- best count, and whether anything **exceeds 727**
- number of faces where the engine returned None (**report as UNEVALUABLE, never as "no improvement"**)

# CRITICAL CONSTRAINTS

- **Exact arithmetic only.** `fractions.Fraction` / sympy Rational. No floats, no `evalf`, no tolerances.
- **Never treat an engine `None` as a count.** It means the overflow budget refused the input. Count and report them separately.
- Do NOT rank chambers by how many walls they touch — this project has REFUTED "more coincidences implies a higher count". The engine decides, always.
- Do not modify any existing file. Create only `extension_chambers.py` and its outputs.
- If the face enumeration returns more than ~5000 faces something is wrong with the gradients; stop and report rather than grinding.

# SANITY CHECK

The base configuration itself (zero direction) must count **727**. Verify this before enumerating anything; if it does not, stop and report.

Report back: incident wall count, face count, the histogram, the best count, whether anything beat 727, and the unevaluable count.
```
