# Session state

Updated 2026-09-08, end of the wall-recording thread.

## Running (started 2026-09-08, mapping the CONTINUUM_MAP backlog)

| job | writes | status |
|---|---|---|
| `src/map_arcs.py` | `data/arc_node_map.json`, `runs/` | arc D done (control, reproduces the record); A, B, C building conditions — not cached, ~15 min each at n = 6 plus the variety solve |
| `src/map_n9.py` | `data/n9_region_map.json`, `runs/map_n9.log` | simplified representative measured (83 walls, lineality 4); its variety solve at ambient 24 is running, then the original representative |
| `src/map_dihedral.py` | `data/dihedral_family_map.json`, `runs/map_dihedral.log` | 1 278 ψ sampled; counting. Prints only at the end |

All three write incrementally except `map_dihedral`. None of them is needed by
anything else; they can be killed and relaunched at the price of the correction.

**Two things to check when they land**, both already written down so agreement is
a test rather than a description:
- [P289](LEDGER.md#p289) predicts the n = 9 variety has **3** directions
  (`variety = lineality − 1`, fitted on n = 4..8, and n = 9 is the level it was
  not fitted to).
- **83 vs 99 walls** at n = 9. RESULTS records 99 from `walls = 24n − 117` on the
  ORIGINAL representative; the simplified one measures 83. If that holds, the
  wall count is an observable separating two representatives that agree in count
  and in `by_depth` at every depth — the mechanism [P285](LEDGER.md#p285) could
  only name.

## Earlier jobs, all finished. `runs/solve_shapes.log`, `runs/map_continua.log`,
`runs/export_walls.log`, `runs/wall_keys.log` are complete and current.

Two logs are kept deliberately and must NOT be read as results:
- `runs/solve_shapes.VOID_prefix_bug.log` — computed with the wrong
  `branch_numerator` ([P288](LEDGER.md#p288)). Void.
- `runs/map_continua.uncached.log`, `runs/export_walls.uncached.log` — partial
  runs killed when the orphaned cache was restored. Superseded, not wrong.

## What today's last thread established

**The wall polynomials are recorded** — as their reconstruction KEY, which is the
same thing. `data/wall_keys.json`, code `src/wall_keys.py`. A wall is
`(frame, group, sig, c0)` plus the record quaternions, and that is the complete
argument list of `dimension.branch_numerator`. Gated three ways (G1 vanishing at
the record, G2 two-route gradient agreement, G3 a corrupted-key control that
fires). n = 4..8 and arcA; `n4_183` recorded as UNEVALUABLE, not skipped.

**Two defects found on the way**, both in [P288](LEDGER.md#p288):

1. The reorg orphaned `dimension_cache` (587 entries) and `catalogue_cache`
   (219) — `HERE`-relative paths following the code instead of the data, failing
   silently. Fixed with the `ROOT` shim. Effect: `solve_shapes` went from an hour
   of setup to `setup 0s`; `map_continua` + `export_walls` from hours to three
   minutes. Every entry recomputed while the cache was orphaned was a duplicate.
2. `branch_numerator` cancelled denominators that only cancel when a condition's
   two normals belong to the same cube, guarded by an assert disabled with
   `or True`. Wrong for 6% of conditions at n = 6, 16% at n = 7.

**Numbers as they now stand:**

    n =                     4    5    6    7    8
    distinct walls         12   18   27   51   75
    lineality               1    1    1    2    3
    coincidence variety     0    0    0    1    2     <- n=7, n=8 CORRECTED
    count-plateau tangents  0    0    2    1    1

The coincidence-variety correction does **not** overturn
[P117](LEDGER.md#p117): the n = 7 curve holds all 300 tight conditions at t = 1
(independently confirmed) but the count falls 1217 → 1213 at t = 1/64. Records
are pinned by the COUNT. Both senses are now named wherever the claim appears.

## The chain: bracket → wall → polynomial → root

Three links of four now exist.

- **bracket** — `src/solve_wall.py`, n = 9 wall at `t ∈ (13/3, 139/32)`.
- **wall** — `data/wall_keys.json`.
- **polynomial** — `wall_keys.on_quat_line(key, quats, moving, A, B, span)`
  returns exact univariate coefficients along `q(t) = (span−t)A + tB`, which is
  the form the brackets actually take. Demonstrated on n = 6: `P(0) = 0` on 27/27
  walls, degrees 2 and 4, 8 walls with a nonzero rational root.
- **root** — not built for n = 9, and the obstacle is cost, not method: the
  conditions at a 10-cube configuration have never been computed. That is the
  next expensive step, and it will now cache.

## Still open

- OQ 30 (bound `c_ℓ`), OQ 32 (what determines `W₀`), Hypotheses **T**, **W**, **C**
  (`RESULTS.md` §3b).
- Why the coincidence variety starts having dimension at n = 7.
- Unmapped: 727 arcs A–C, the n = 9 region's other dimensions, the 67↔67
  dihedral family (irrational; needs `cube_regions_q2` and in-field perturbation).
- The 727 arc ANOMALY: measured at `s = 10/3`, outside MAXIMISERS' `[9/4, 3]`.
  Recorded as not concluded.
- `sync_layout_to_github.sh` has not been run against the publish tree.
