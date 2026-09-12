# Session state

Updated 2026-09-12. **Nothing is running.** All results are on disk.

## What this session did

Started from "record enough to reconstruct the wall polynomials" and ended with a
gap register, most of it closed. Sixteen postscripts, P288–P303.

### Machinery built
| file | what it does |
|---|---|
| `src/wall_keys.py` | the reconstruction KEY per wall — `(frame, group, sig, c0)` IS the polynomial, via `branch_numerator`. `on_line` (Cayley line), `on_quat_line` (quaternion line). Works over ℚ(√d). Gated three ways. |
| `src/wall_solve.py` | every wall on a line as an exact polynomial with **all** real roots — rational as fractions, irrational as minimal polynomials |
| `src/arc_special.py` | special points of the 727 arcs, by solving not walking |
| `src/fibre_boundary.py` | plateau extents by geometric-then-simplest-rational bracketing |
| `src/tangents_full.py` | full-ambient tangents — **premise refuted, see P298** |
| `src/build_n10.py` | the n = 10 conditions, built at last (2 045 s, now cached) |
| `src/scrub_paths.py` | keeps resolved paths out of records; derives what it removes |

### Defects found and fixed
- **`branch_numerator` was wrong** whenever a condition's two normals came from different
  cubes — an assert disabled by `or True` (P288). n = 6, 7 verdicts re-run.
- **The reorg orphaned two caches** — 587 + 219 entries, silently (P288).
- **`_rational_roots` scanned to m, not √m** — 9.7 s → 0.004 s, and it is in
  `variety_incremental`'s inner loop, so it slowed every variety solve ever run.
- **Selective runs silently deleted records** in `wall_keys.py` and `map_arcs.py`
  (FAILURE_MODES 33).

## The big correction: tangent numbers

**Every count-plateau tangent number in this project is a lower bound from a method
whose premise is false** (P298). `tangents_eps` searches the last-cube slice AND
assumes tangents lie in every wall. Both are wrong: a direction crossing 7 of 51
walls holds the count. Measured since: **4 of 6 wall crossings leave the count
unchanged** (P303). The open problem everything rests on: *which* walls bound the
count plateau.

## The 1217 plateau, fully mapped

2-dimensional, a **pentagon** — two directions plus a third wall aligned with
neither, solved as a degree-4 curve (P299, P301). Boundaries inherit
**selectively** (P303): the fibre boundary and the third wall survive to n = 8 and
n = 9 at identical brackets, each costing exactly 4 regions; the base boundary
contracts ~5×, and n = 8's and n = 9's contracting walls are **different** — same
coarse bracket, different frames, groups and cubes. All in `data/plateau_1217.json`.

## Also established
- **arc D's extent SOLVED** (P296) — `(-2/19, 10695/1007 − 7√2248773/1007)`, closing
  `bracket → wall → polynomial → root` end to end for the first time. `arcs_extend.py`
  and MAXIMISER_TAXONOMY corrected in place.
- **n = 10 measured** (P300): 480 tight, 100 walls, rank 21, lineality 6. Differs from
  P185 because P185 measured 3913, a superseded configuration.
- **The 727 node**: nine special points, six compounds; the record lies on three of the
  four arcs (P294).
- **The two 67s** are in the wall-key index over ℚ(√2) and ℚ(√5).
- **The golden 67 sits ON the 55/43 wall**; the octahedral one is 14° inside (P291).

## Still open
1. **Which walls bound the count plateau** — the question P298 opened; everything
   dimensional depends on it.
2. Plateau dimension at n = 4, 5, 6 — *not* closed; "0" came from the false premise.
3. Arc D's second crossing tangent — still swept.
4. The n = 9 region's other dimensions; the dihedral family's exact edges.
5. `vertex_scale` covers level-graph vertices only; curvature never tested.

## Not done by me, waiting on you
- `python3 src/scrub_paths.py --tree github --apply` — 33 files in the publish tree.
- `cp TOWER_DIAGRAM.html github/` — the diagram is publish-clean (0 non-ASCII, only
  Google Fonts external).
- `data/2026-09-07-231403-compactions.txt` — a verbatim export; keep-or-exclude decision.
- `sync_layout_to_github.sh` — never run.
