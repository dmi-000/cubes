# Session state — 2026-09-12 (evening)

**Read this first, then [RESULTS.md](RESULTS.md) §4's scope correction.**

## The one thing that changed today

**No wall list in this project is known to be complete.** The wall census built for
[OQ 33](OPEN_QUESTIONS.md#33) found a second codimension-1 family of the COUNT — four
face planes through a common point — which no coincidence condition sees, and then found
a count-changing parameter belonging to neither family. [P304](LEDGER.md#p304),
[OQ 34](OPEN_QUESTIONS.md#34).

Anything that reads "the walls of this configuration" in an older document means the
COINCIDENCE walls. That is not the same set.

## What is established

- **OQ 33, on a full ray:** at the 727 record along e0, window ±1/4, 217 attributable
  crossings — of 21 crossings carrying a coincidence wall, **8 change the count and 13 do
  not**; of 663 carrying only concurrency walls, **0** change it. Every change is exactly
  ±4. P303's 4 of 6 was not a fluke of a hand-picked sample.
- **The census is G2-clean on that ray:** 685 cells, three rationals each, zero constancy
  failures — a completeness check on a wall list, which this project has never had before.
- **The two families do different jobs.** Coincidence walls are STEPS (count differs
  across). Concurrency walls are PUNCTURES (count equal on both sides, lower on the wall):
  at t = −2/9, 693 | 691 | 693.
- **The record is a point of extreme concurrency:** 6772 of e0's 7620 concurrency roots
  in the window sit at t = 0.
- **t = −2/9 solved:** the concurrency determinant on the ray cancels to `9t² + 20t + 4`.

## What is open, in order of weight

1. **The attribution audit P304 opens.** Every boundary located as "nearest wall root where
   the count changes" searched the coincidence family only — P296's arc D extent,
   P301/P302/P303's three walls of the 1217 plateau. The EXTENTS stand (they were counted).
   Whether the named condition is the actual cause is unchecked at n = 7, 8, 9. Run
   `concurrency_walls.py` on those rays and look for a root inside each straddle interval.
2. **One ray, one record.** The census has run on e0 at n = 6 only. `--family both` gives
   15 axis rays plus mixed ones; n = 7 is where P298's counterexample lives and is the
   real target.
3. Everything still listed under OQ 33: whether "coincidence walls only" survives at higher
   n and on non-axis rays, and whether the 7-of-18 that change the count are predictable
   from the group's cube indices.

## Instruments added today

| file | what it does | its gate |
|---|---|---|
| `src/wall_census.py` | every crossing on a ray, the count in each cell, one verdict per wall | G1 base is the record; G2 three-point constancy per cell, which STEERS the branch closure; G2N negative control (hide half the keys, G2 must fail — 13 of 103); G3 refusals counted |
| `src/concurrency_walls.py` | the four-plane family, by exact interpolation | degree bound verified at 3 unseen parameters (0 failures on 6 rays); G4 the known −2/9 wall must return with its quadruple |
| `src/wall_census_analyze.py` | criterion search over the census, and the count ON each rational wall | — |

Data: `data/wall_census_n6.json`, `data/concurrency_walls_n6.json`, both from the corrected
convention. The two files from the broken one are kept as `data/VOID_2026-09-12_*` —
renamed, not deleted, so the original numbers stay derivable.

**A trap this session walked into, worth knowing before extending the work**
([FAILURE_MODES 39](FAILURE_MODES.md#39)): the face normals are the COLUMNS of the rotation
matrix, not the rows. Every gate in the new code passed in the wrong convention, because
the fact each one checked against had been established by the same code.

## Standing constraints

- **Never write into `github/`.** The publish tree is the user's alone.
- No machine or network references in anything that reaches the public repo.
- Remediation commits stay bland.

## Waiting on the user

- `python3 src/scrub_paths.py --tree github --apply` (33 files)
- `cp TOWER_DIAGRAM.html github/`
- keep-or-exclude decision for `data/2026-09-07-231403-compactions.txt`
- `sync_layout_to_github.sh`
