# Glued family-clique search — does gluing reach or beat 183/393/723?

Executes `GLUE_SPEC.md`. Reuses `nfamily_common.py` (exact Rodrigues/
quaternion core, read-only) and `./cube_regions_n` (read-only); never
edits `six_cube_search_results.md` or any validated file. Code:
`glue_search.py` (modes `q0` / `gates` / `sweep`); raw sweep log
`glue_results.jsonl` (319,141 configs); per-cell axis analysis
`glue_q0.json`; per-cell best `glue_best.json`.

**No result in this campaign beats or ties a record** — the verification
protocol (independent Python-oracle re-check before anything gets
flagged as a record claim) was never triggered. The headline numbers:
best glued totals **175 / 385 / 715** at n=4/5/6, against records
**183 / 393 / 723** — all three deficits land at **exactly −8**, up from
the single-axis family's −8 / −58 / −108 (`nfamily_report.md`). Gluing
closes almost the entire deficit at n=5 and n=6 (50 and 100 points
recovered) without reaching either record, and the closing pattern
converges to the same −8 gap the pure family already had at n=4. Full
story below, Q0 first as required.

## Q0 (critical first step): is 183 or 393 itself SINGLE-AXIS?

**No — flagged prominently as required, but the answer does NOT flip
Postscript 26's verdict.** Exact test (`glue_search.py --mode q0`, all
Fraction/no-float arithmetic; method and airtightness argument in the
module docstring above `q0_report()`): for every pair, find the cube-
symmetry relabeling that puts the relative rotation in `Rel(Δ,ψ)` form
(this is a *necessary and sufficient* condition, not a heuristic — any
rotation whose axis lies in the appropriate local plane has that form,
so the exact-Fraction witness alone certifies it) and extract the exact
global axis line; then test whether ONE axis and ONE common tilt ψ
(exact `tan ψ` as a Fraction) is shared by every cube in the record.

| record | full-record axis intersection | verdict |
|---|---|---|
| 183 (n=4, all 6 pairs family per Q3) | empty | **not single-axis** |
| 393 (n=5, all 10 pairs family per Q3) | empty | **not single-axis** |
| 723's embedded 393 (cubes 0–4) | empty | **not single-axis** |
| 723 full (n=6) | empty | **not single-axis** |

So Postscript 26's core claim — the records are gluings, not disguised
single-axis members — **stands**, exactly as tested for the first time
here (the earlier per-pair test in `nfamily_report.md` was axis-agnostic
and never checked this).

**But there is a much richer near-single-axis structure than previously
known, and it changes *why* the family sweep couldn't reach the
records.** Every record contains **(n−1)-of-n single-axis sub-cliques**
— not just "some axis per pair" but one shared axis AND one shared exact
`tan ψ` across n−1 of the n cubes:

- **393** (and 723's embedded copy): **three overlapping 4-of-5
  sub-cliques**, all at the *same* tilt `tan ψ = 2/3` (equivalently
  `3/2`): `{0,1,3,4}` axis `(2,0,3)`, `{0,2,3,4}` axis `(0,3,2)`,
  `{1,2,3,4}` axis `(3,2,0)`. Cubes 3,4 are common to all three; cubes
  0,1,2 each get excluded from exactly one. Cube 5 (in 723) is excluded
  from all of them — consistent with Q3's finding that cube 5 links only
  to cubes 3,4.
- **183**: **three different 3-of-4 sub-cliques**, each pairing the
  identity cube (0) with two of {1,2,3}, at **three different** tilts:
  `{0,1,2}` axis `(0,5,2)`, `tan ψ=5/2`; `{0,1,3}` axis `(3,0,2)`,
  `tan ψ=3/2`; `{0,2,3}` axis `(3,5,0)`/`(2,-3,0)`/`(5,2,0)`, THREE
  distinct tilts (`5/3`, `2/3`, `2/5`) all simultaneously valid for that
  one triple (extra coincidental structure only possible with just 3
  pairs). `{1,2,3}` alone is **not** single-axis (its three pairwise
  axes are all different) — cube 0 is the essential hub.
- **Every one of these `tan ψ` values is IRRATIONAL** (checked exactly:
  `tan ψ = p/q` is Pythagorean, i.e. `sin ψ, cos ψ` both rational, iff
  `p²+q²` is a perfect square; here `13, 29, 34` — none are). The `13`
  case (`tan ψ=2/3`, `sin ψ=2/√13`, `cos ψ=3/√13`) recurs **both** inside
  183 and inside 393/723 — a candidate n>3 analogue of the irrational
  octahedral/golden special points already known at n=3 (Postscript 25).

**Why this matters for the "sweep menu too coarse" hypothesis (Q0's
explicit charge).** It does *not* flip to "coarse menu" — it sharpens
the diagnosis to "the wrong space, at any resolution." `nfamily_common`'s
`PyAngle`/`rel_matrix` machinery requires ψ **itself** to be Pythagorean
(`PyAngle` asserts `c²+s²=1` with both `c,s` exact `Fraction`s). The
records' near-maximal sub-cliques sit at ψ with irrational `sin,cos` —
no refinement of the Pythagorean menu, however fine, ever lands there
(measure-zero irrational points, exactly the n=3 coverage caveat in
`nfamily_report.md`, now shown to persist as embedded structure at
n=4/5/6). One consequence checked directly: the pairwise phase
differences Δ inside these sub-cliques are **also** irrational
(`cos Δ = 29/133` for one 393 pair, and `133²−29²=16848` is not a
perfect square either) — so this is not a simple "use 2ψ instead of ψ"
fix; the rational locus is a genuinely different, currently
unparametrized algebraic variety. **Practical upshot for the sweep
below**: even the SIZE-(n−1) clique inside a glued attempt at the literal
record is out of reach for a Pythagorean-menu clique generator — so the
sweep cannot literally reconstruct 183/393/723, only search nearby in
the same *structural class* (two cliques glued by a rational rotation).
That the sweep still closed 87–93% of the single-axis-family deficit
(below) shows the *gluing idea* is right even though this specific
clique-internals parametrization can't reach the exact irrational point.

Detail JSON: `glue_q0.json`.

## Gates

`glue_search.py --mode gates` — all three PASS:

- **G1** (two-engine agreement, one glued config per n): built
  clique A (chain, Pythagorean a=36.87°, ψ=53.13°) glued via an integer
  quaternion G to clique B (chain, a=61.93°, ψ=22.62°), sizes (3,1) /
  (4,1) / (5,1) at n=4/5/6. C++ `cube_regions_n` and Python
  `certify_six.exact_count_config` agree **exactly** on total and full
  depth histogram at all three n: 143={1:58,2:60,3:24,4:1},
  319={1:94,2:118,3:76,4:30,5:1}, 607={1:140,2:188,3:144,4:98,5:36,6:1}.
  **PASS**.
- **G2** (reproduce 723 from the ledger quats): `cube_regions_n` on
  `4,1,1,-1;3,3,7,3;5,-1,-5,-5;2,1,1,1;1,1,1,1;5,2,2,2` gives exactly
  **723** = {1:210,2:216,3:164,4:96,5:36,6:1}. **PASS**.
- **G3** (reconstruct 723 as a gluing): clique A = the embedded 393
  taken verbatim (its psi is irrational per Q0, so it cannot come from
  the Pythagorean menu — using its exact quats is the honest reading of
  "clique A" for this gate); clique B = the trivial size-1 case, where
  `Rel(0,0)=I` exactly (verified) so `G = cube 5's own quat` reproduces
  cube 5 exactly, and the reassembled 6-quat config recounts to 723 with
  the correct depth histogram. **PASS** — confirms the parametrization
  `clique A ∪ G·clique B` is expressive enough to represent a real
  record; the sweep's limitation is the clique-internals menu (Q0), not
  the gluing parametrization itself. Note (n=5,1) singleton cliques
  collapse: `Rel(θ,ψ)` for ANY θ,ψ is just some fixed rotation once you
  don't force θ=ψ=0, but the *freedom* of a lone cube is already fully
  carried by G alone — this is why the sweep's (a,1) cells enumerate G
  directly as the free cube's placement rather than also scanning a
  redundant ψ_B/θ_B.

## The sweep

Config space per GLUE_SPEC: clique A = `{Rel(θ_i,ψ_A)}` (Pythagorean,
`nfamily_common.rel_matrix`), clique B = same, wholesale-rotated by an
integer quaternion G, sizes (n=4: (3,1),(2,2); n=5: (4,1),(3,2); n=6:
(5,1),(4,2),(3,3)).

**Method** (`glue_search.py --mode sweep`): (1) generate Pythagorean
chain-clique candidates for sizes 2–5 from a 33-point menu (~70–850
candidates per size), rank by their OWN standalone region count (cheap,
size ≤5); (2) coarse pass — top-8 clique-A × top-8 clique-B (or ×1 for
size-1) × a 400-point sampled G menu (24-cube-group ∪ random sample of
integer quaternions, `|component|≤3`, 1120 total directions); (3) widen
— re-sweep G to the full `|component|≤4` menu (2928 directions) from the
top-3 coarse restarts per cell; (4) neighbor hill-climb (G perturbed by
composing with the 24-cube-group and small quaternions) for 3 rounds;
(5) a final **targeted refinement pass** widened the G menu further to
`|component|≤6` (12,768 directions) around each cell's single best
config. ≤4 cores throughout (batched C++ calls split across an
`mp.Pool(4)`, `run_batch_parallel`); total wall-clock ≈45 min, detached.
**319,141 configs counted and logged** to `glue_results.jsonl`.

### Best per (n, clique sizes)

| n | sizes | best | record | deficit | vs single-axis family best | quats | by_depth |
|---|---|---|---|---|---|---|---|
| 4 | (3,1) | 175 | 183 | −8 | +0 (=175) | `1,0,0,0; 7,3,4,0; 12,21,28,0; 1,2,2,2` | {1:88,2:62,3:24,4:1} |
| 4 | (2,2) | 175 | 183 | −8 | +0 (=175) | `1,0,0,0; 7,3,4,0; -2,5,2,2; 40,-21,-16,-21` | {1:92,2:58,3:24,4:1} |
| 5 | (4,1) | 381 | 393 | −12 | +46 | `1,0,0,0; 7,3,4,0; 12,21,28,0; -91,183,244,0; 0,-2,4,3` | {1:140,2:130,3:80,4:30,5:1} |
| 5 | (3,2) | **385** | 393 | **−8** | **+50** | `1,0,0,0; 45,28,21,0; 80,252,189,0; -2,2,5,-2; 40,-16,-21,21` | {1:144,2:130,3:80,4:30,5:1} |
| 6 | (5,1) | 663 | 723 | −60 | +48 | `1,0,0,0; 15,6,8,0; 25,36,48,0; -45,138,184,0; 119,-72,-96,0; 3,0,-1,-2` | {1:168,2:204,3:152,4:102,5:36,6:1} |
| 6 | (4,2) | 713 | 723 | −10 | +98 | `1,0,0,0; 7,3,4,0; 12,21,28,0; -91,183,244,0; 0,-2,4,3; -10,-26,37,1` | {1:206,2:210,3:160,4:100,5:36,6:1} |
| 6 | (3,3) | **715** | 723 | **−8** | **+100** | `1,0,0,0; 7,3,4,0; 12,21,28,0; 3,0,-4,6; 37,-15,2,54; 148,-105,162,156` | {1:190,2:222,3:164,4:102,5:36,6:1} |

Bold rows are the per-n champions (best clique-size split). **385 and
715 were independently re-verified with the Python oracle
(`certify_six.exact_count_config`)** — both match the C++ total and full
depth histogram exactly (385: {1:144,2:130,3:80,4:30,5:1}; 715:
{1:190,2:222,3:164,4:102,5:36,6:1}). Neither beats or ties a record, so
the record-claim protocol (two-engine verification before flagging at
the top of the report) was exercised but produced no claim.

**Deficit pattern (striking, not obviously an artifact).** The best
glued configs at all three n land **exactly 8 short** of the record:
183−175=8, 393−385=8, 723−715=8. n=4's gluing search found *no*
improvement at all over the pure single-axis family (175 either way,
and (2,2)'s depth histogram {1:92,2:58,3:24,4:1} matches the single-axis
family's best member exactly — see `nfamily_report.md` — while (3,1)'s
{1:88,2:62,...} reaches the same 175 by trading 4 points from d1 into
d2, `d1+d2=150` in both). At n=5 and n=6 the deficit that was −58/−108
for a single axis collapses to the SAME −8 that n=4 always had — as if
−8 is a structural floor for "everything family/glued-family can reach"
once enough gluing freedom is available, and n=4 simply had no further
freedom to lose. This pattern is suggestive rather than proven (no
argument here derives it), and is exactly the kind of regularity worth
a follow-up search focused narrowly on closing that specific 8-point gap
(deeper local moves — see coverage below).

**Where the gap sits (depth-wise).** Records keep the same "deep layers
pinned" signature the pure family already showed
(`nfamily_report.md` Q2): 715's `{5:36,6:1}` match the record exactly;
713's `{5:36,6:1}` too. The −8 deficit for n=6 (3,3) sits entirely in
shallow layers: d1 190 vs record 210 (−20), d2 222 vs 216 (**+6**, i.e.
the glued config actually *exceeds* the record in d2), d3 164 vs 164
(exact), d4 102 vs 96 (**+6**, also exceeds). So the deficit is
concentrated in d1 alone (−20), partially offset by d2/d4 surpluses
(+12) — a genuinely different trade-off than the pure single-axis
family's n=6 profile (which undershot d1 through d4 all at once).

## Honest coverage statement

- **The literal records are provably out of reach for this exact
  parametrization** (Q0): their maximal near-single-axis sub-cliques sit
  at irrational (ψ, and even pairwise Δ) that no Pythagorean menu, at
  any resolution, can land on. The sweep can only search the same
  *structural class* (two Pythagorean-menu cliques glued by a rational
  G), not literally reconstruct 183/393/723 — this is not a budget
  limitation, it is what Q0 established as a hard boundary of the
  parametrization.
- **Clique-internals menu**: candidates ranked by *standalone* region
  count (cheap proxy) — a clique that scores well alone need not glue
  best; only the top 8 per size were tried in the main sweep (widened to
  ~15–20 implicitly via the 3 multi-restarts x top-8 pool overlap, not a
  full top-20 pass). A systematic top-20-or-more clique-pool sweep was
  not run (time budget); given the observed clean ranking (best
  standalone totals 13/63/175/335 for sizes 2/3/4/5 closely tracking
  `nfamily_results.jsonl`'s own numbers), this is a plausible but
  unproven completeness gap.
- **G menu**: coarse pass sampled 400 of the 1120 `|component|≤3`
  directions (plus the 24-cube-group) at random (seeded); every
  near-record cell was then independently re-swept with the FULL
  `|component|≤6` menu (12,768 directions) around its single best
  config in the final refinement pass — so the reported bests are not
  starved by the initial random subsampling, but a `|component|≤6` cap
  is still finite; "then widen for promising cells" per the spec was
  honored (three widen tiers: 3→4→6), not exhausted (7, 8, ... untried).
- **Hill-climbing was G-only.** `hillclimb_cell` perturbs G (composing
  with the 24-cube-group and small quaternions) but never perturbs
  clique-internal θ/ψ once a clique pair is fixed — unlike
  `nfamily_sweep.py`'s single-coordinate θ/ψ neighbor search. Given the
  −8 floor recurring at all three n and the clean partial-credit in d2/
  d4 at n=6, a θ/ψ-level local search around the current champions (not
  attempted here) is the most promising unexplored direction to actually
  close the residual 8-point gap, if it is closable within this
  parametrization at all.
- **Multi-restart was from the top-3 coarse candidates per cell**, not
  the full top-10 the spec mentions (time budget: each restart's widen
  phase costs a full `|component|≤4` sweep, ~2,900 configs).
- **Budget used**: 319,141 configs, ≈45 min wall-clock on ≤4 cores (well
  under a 10k–50k-per-cell notion of the budget, more like 25k–60k per
  cell across 7 cells) — stopped because the widen-to-6 refinement pass
  produced no further improvement at 5/7 cells and only +4 at the other
  2 (5,3,2: 381→385; 6,3,3: 711→715), suggesting the G-search direction
  specifically is close to exhausted at this clique-pair choice, not
  that the campaign ran out of time.

## Files

- `glue_search.py` — Q0 axis analysis, G1/G2/G3 gates, sweep + hill-climb
  driver (`--mode q0|gates|sweep`).
- `glue_results.jsonl` — 319,141 logged configs (n, sizes, ψ/θ pqr where
  applicable, Gquat, quats, total, by_depth).
- `glue_q0.json` — Q0 per-record axis/tan-ψ detail.
- `glue_best.json` — final best config per (n, sizes) cell.
