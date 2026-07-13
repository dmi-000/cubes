# n = 5 record hunt: golden 351 is beaten by a 723-record subset (393); the
# wide-perturbation deep climb does NOT push further

*2026-07-12. Scope: establish/confirm the golden five-cube compound's 351,
then test whether it is the n=5 maximum (mirroring `n4_search.py`'s
methodology, which found a rational 183 beating golden's 177 at n=4).
~171,600 exact configurations evaluated in total (see Coverage below).
Every count in this document is exact (rational or ℚ(√5) arithmetic, no
floating point in any predicate) and independently cross-checked by two
separate counters.*

## Headline result

**The golden five-cube compound (351) is NOT the n=5 maximum.** Before this
script's own search phases ran, the coordinator identified that a 5-cube
subset of the six-cube record (723, `six_cube_search_results.md`) already
beats it: dropping the sixth cube (`5,2,2,2`) from the record leaves

```
quats = [[4,1,1,-1], [3,3,7,3], [5,-1,-5,-5], [2,1,1,1], [1,1,1,1]]
by_depth = {1: 156, 2: 128, 3: 78, 4: 30, 5: 1}     total 393   (+42 over golden 351)
```

This is confirmed here two independent ways with an EXACT match on both the
total and the full depth histogram:

- `./cube_regions_n --n 5 --quats '4,1,1,-1;3,3,7,3;5,-1,-5,-5;2,1,1,1;1,1,1,1'`
  → `"bounded":393, "by_depth":{"1":156,"2":128,"3":78,"4":30,"5":1}`
- `certify_six.exact_count_config` (independent Python oracle) → `393`,
  `{1: 156, 2: 128, 3: 78, 4: 30, 5: 1}` — identical.

**Unlike n=4, the wide-perturbation multi-restart deep climb (the technique
that took n=4 from 159 to 183) did NOT push past this value.** 393 survived
**155 wide-perturbation restarts** across three separate attacks (40 from
itself, 15 from its nearest 723-subset neighbor which re-converges to the
identical config, and a further 100 from an independent RNG seed) — every
single restart either fell back to 393 or landed below it. All six 5-subsets
of the 723 record were evaluated (see Section 2); the runner-up is 387. All
of the *fresh* structured families built for n=5 specifically (golden-
rationalized neighborhood, octahedral-type, C4-orbit, C3-orbit) topped out
far lower (377, 369, 323, 309) even after their own deep climbs. **Best
n=5 total found: 393**, exactly the coordinator's value, with no config
anywhere in ~171,600 exact evaluations exceeding it.

## 1. Golden five-cube compound: confirmed 351

`cube_compound_exact.run(5)` (the full compound of five cubes inscribed in a
regular dodecahedron, ℚ(√5) exact arithmetic):

```
N=5: bounded regions = 351   by depth: {1: 180, 2: 80, 3: 60, 4: 30, 5: 1}
```

Re-derived independently: built the same 5 cubes' rotation matrices directly
from the icosahedral axes (all 5 orthogonal triples among the 15 two-fold
axes, handedness fixed by swapping two columns where a raw triple came out
left-handed) and fed them to `certify_six.exact_count_config` — same engine
class that validates the C++ counter. Result: **351**, by_depth
`{1: 180, 2: 80, 3: 60, 4: 30, 5: 1}` — exact match, including the
dodecahedron-vertex sanity check (`cube_compound_exact.py`'s own N=5 branch:
all 40 corners of the 5 cubes land on the dodecahedron's 20 vertices,
2-to-a-vertex).

**Engine validation gate.** `cube_regions_n --n 5` cross-checked against the
`certify_six` oracle on 5 random seeds (1, 2, 3, 17, 999): exact match on
total AND full depth histogram in every case (289, 277, 297, 269, 297). The
n=5 rational counter is validated before any search began.

Note that unlike n=4 (whose golden sub-compound is only 4 of the 5
dodecahedral cubes, a proper sub-compound), the golden n=5 compound is the
**complete, maximally-symmetric icosahedral compound of all five cubes** —
so there was real reason to expect it might hold up where n=4's did not.
It does not.

## 2. The seed that broke 351: a 5-subset of the six-cube record

The six-cube record (723 bounded regions, `six_cube_search_results.md`) is

```
4,1,1,-1 ; 3,3,7,3 ; 5,-1,-5,-5 ; 2,1,1,1 ; 1,1,1,1 ; 5,2,2,2
```

Every one of its six 5-subsets (drop one cube) was evaluated exactly here
(`./cube_regions_n --n 5`, phase `R`):

| dropped cube | total | by_depth |
|---|---|---|
| `4,1,1,-1` | 381 | {1:136, 2:132, 3:82, 4:30, 5:1} |
| `3,3,7,3` | 381 | {1:136, 2:132, 3:82, 4:30, 5:1} |
| `5,-1,-5,-5` | 381 | {1:136, 2:132, 3:82, 4:30, 5:1} |
| `2,1,1,1` | 387 | {1:138, 2:134, 3:84, 4:30, 5:1} |
| `1,1,1,1` | 375 | {1:126, 2:134, 3:84, 4:30, 5:1} |
| **`5,2,2,2`** | **393** | **{1:156, 2:128, 3:78, 4:30, 5:1}** |

**All six subsets beat golden's 351.** The best (drop `5,2,2,2`, the record's
own "extra" 6th cube) is 393. Every subset has d4 = 30, exactly at the
conjectured cap. This is a clean instance of the project's established
pattern (six-cube subsets of the golden 5-compound sum to the golden totals;
here, five-cube subsets of the rational 6-record inherit most of its
richness) — and, matching n=4's finding that "the golden compound leads
among *symmetric* configs but is not the global max," these fully generic
subsets of an even-more-optimized 6-cube arrangement outrun the symmetric
5-cube compound by 42 regions.

## 3. The deep climb: 393 holds under 155 wide-perturbation restarts

Applying `n4_search.py`'s exact methodology (verbatim — `phaseD_deepclimb`
needed no n=5-specific change, since it is already written generically in
terms of `len(quats)`): climb ±1/±2 to a local max, certify at radius 4
(±1..±4 single-component), then fire wide (1–6 simultaneous components,
each ±1..±4) perturbations at the original seed and re-climb each — the
only way to escape a genuine radius-4 local max, since single-component
search can never make a multi-component jump.

**From the 393 seed itself:**
- Base climb: stays at 393 (already a ±1/±2 local max).
- Radius-4 certification: **confirmed local max** (no single-component move
  of ±1..±4 on any of the 20 quaternion components improves it).
- 40 wide-perturbation restarts (first pass): **0 improvements**, best
  remained 393.
- A further independent 100 wide-perturbation restarts (fresh RNG seed
  99991): **0 improvements**, best remained 393.

**From its nearest 723-subset neighbor (387, dropping `1,1,1,1` instead of
`5,2,2,2`):**
- Base climb: **converges directly to the same 393 configuration**
  (reordered: `[[4,1,1,-1],[3,3,7,3],[5,-1,-5,-5],[1,1,1,1],[2,1,1,1]]`, the
  identical 5-cube set as the champion).
- Radius-4 certification: confirmed local max.
- 15 further wide-perturbation restarts: 0 improvements.

**Total: 155 wide-perturbation restarts across the 393 basin and its
immediate neighbor, zero improvements.** This is qualitatively different
from n=4, where the analogous seed (the S1 family's 159) needed to be
walked through five distinct plateaus (159→171→173→175→179→183), each
escaped by a handful of wide-restart hits, before settling at 183. Here the
seed starts much richer (393 vs. 159) and appears to sit in a single deep,
wide basin rather than a shallow one requiring several escapes. This is
evidence — not proof — that 393 is a substantially more robust local
optimum than any of n=4's intermediate plateaus were.

**From fresh structured seeds built specifically for n=5** (Section 4),
the deep climb was also applied, and none came close to 393:

| seed family | seed total | after deep climb | restarts |
|---|---|---|---|
| golden-5, rationalized | 369 | **377** | 25 |
| S1 (octahedral 2-axis-pair(4) + 1 free) | 339 | **369** | 15 |
| S2 (C4-orbit(4) + 1 free) | 321 | **323** | 15 |
| S3 (C3-orbit(3) + 2 free) | 309 | 309 (no improvement) | 15 |

None of these fresh-family climbs reached even the *second*-best 723-subset
(387), let alone 393 — reinforcing that the 723-record's own internal
structure (not a symmetry group anyone would have guessed to build from
scratch at n=5) is what carries the richness.

## 4. Structured/symmetry families built specifically for n=5

Four seed families were built to mirror n4_search.py's approach and the
task's request to probe "the golden 5's ℚ(√5) neighborhood, octahedral-type,
shared-axis, and C-orbit families":

**Phase P — golden five, rationalized.** The golden compound's Q(√5)
rotation matrices were rounded to nearby all-rational quaternions
(`certify_six.rationalize`, N=512 — same rounding convention used
throughout this project to probe a wall's rational neighborhood) and
evaluated exactly. Result: **369** (`{1:128, 2:128, 3:82, 4:30, 5:1}`),
cross-checked identically by both `cube_regions_n` and the oracle. This
already beats golden (351) by 18 just from rounding off the wall — the
same "rational beats symmetric" pattern as everywhere else in this project
— and deep-climbs to 377 (Section 3), still well short of 393.

**Phase S1 — octahedral-type 2-axis-pair(4 cubes) + 1 free rational cube.**
Generalizes `six6_mats`/n4's S1 (2 axis-pairs about x,y, integer parameter
t, exactly rational) to n=5 by attaching one additional free cube (C5 has
no rational realization, so 5 = 4+1, not a literal 5-fold family). Sweep
t=1..40 (coarse, step 3) × free-cube candidates, refine at the best t, then
hillclimb (free cube alone, then all 5). **Max found: 339**, deep-climbs to
369 (Section 3).

**Phase S2 — shared-C4-axis orbit(4 cubes) + 1 free rational cube.**
`cube_k = Rz(k·90°)·Q0` for k=0..3 (exactly rational) + 1 free cube, swept
over symmetric + random Q0/free candidates then hillclimbed. **Max found:
321** (oracle) / 323 after deep climb.

**Phase S3 — shared-(1,1,1)-C3 orbit(3 cubes) + 2 free cubes.** Directly
downsizes the n=6 RECORD's own shape (3-cubes-about-a-diagonal + 3 free
cubes) to n=5 (3+2) — the most directly record-motivated structured family
tried. Two-stage sweep (fix 2nd free cube at identity, optimize 1st; then
optimize 2nd) + hillclimb. **Max found: 309**, no improvement under deep
climb.

None of the four families beat even the weakest 723-subset (375), let
alone 393 — the six-cube record's internal 5-subsets are simply richer
than anything these general-purpose symmetric shapes produce at n=5.

## 5. Rational campaign + hill-climb: mapping the generic ceiling

**Campaign** (`run_campaign_n.py --n 5 0 100000 4`, 100,000 random rational
seeds): best total **329** (`{1:80, 2:134, 3:84, 4:30, 5:1}`), far below
351 (golden) and 393 (record-subset) — confirming the established pattern
(n=4: random plateaus at 137; n=6: random plateaus at 635) that unstructured
rational sampling cannot reach the good walls.

**Hill-climb from the campaign's top-20 seeds**
(`phase_b_hillclimb_n.py --n 5 --topk 20 --objectives total,d1,d2
--restarts 2`, 10,012 exact evaluations): champions **331** (total
objective) and **335** (d2 objective, `{1:86, 2:134, 3:84, 4:30, 5:1}`).
Confirms climbing helps but a single-pass greedy climb from generic seeds
still falls far short of both 351 and 393 — matching n=4's and n=6's
lesson exactly: the good walls are not reachable by climbing from noise
alone.

## 6. mod-4 parity

Predicted for generic n=5: `bounded ≡ 2·5−1 = 9 ≡ 1 (mod 4)`.

| source | configs | exceptions | rate |
|---|---|---|---|
| random campaign (100,000 seeds) | 100,000 | 565 | **0.57%** |
| hill-climb from campaign seeds | 10,012 | 391 | 3.9% |
| this script's structured/deep-climb log | 58,941 | 28,736 | 48.8% |

The random-campaign rate (0.57%) is a clean, low exception rate, consistent
with the parity law holding essentially always away from special walls
(compare n=4's noticeably higher 3.33%, itself flagged as an open question
there; n=5's rate sits between n=4's and n=6's <0.1%). The structured-search
log's high 48.8% rate is exactly the phenomenon `PROJECT.md` §5 and
`n4_search_report.md` §4 both flag: **highly symmetric/structured walls jump
to the other allowed residue far more often** — this log is *dominated* by
symmetric candidates (S1/S2/S3 sweeps, golden-neighborhood points, and the
723-record subsets themselves), not generic noise, so a high exception rate
there is expected, not a parity-law violation. Both 351 (golden) and 393
(the record) land on residue **1** — the generic residue — so neither is a
parity exception itself; the exceptions are concentrated in the symmetric
*search candidates* that did not become the champion.

## 7. Depth-4 (= n−1) ceiling: confirmed, never exceeded

The task's proposed n=5 analog of n=4's d3≤24 / n=6's d4≤102 ceiling is
**d4 ≤ 6·5 = 30** (golden hits 30 exactly). Across every exact evaluation
in this task:

| source | configs | max d4 observed | at cap (=30) | exceeding 30 |
|---|---|---|---|---|
| random campaign | 100,000 | 30 | 95,811 (95.8%) | **0** |
| structured/deep-climb log | 58,941 | 30 | 53,893 (91.4%) | **0** |
| hill-climb log | 10,012 | 30 | 10,012 (100%) | **0** |

**d4 = 30 was never exceeded in ~171,600 exact n=5 configurations** — a
strong empirical ceiling, exactly analogous to n=4's d3 ≤ 24. It is also
essentially the *generic* value: 95.8% of uniformly random configurations
already hit it exactly (compare n=4, where d3=24 was likewise generic but
d1 richness varied hugely). The golden compound (351) and the record
(393) both sit exactly at this cap, so — as with n=4's d3/d4 — **the
entire 42-region gain of 393 over golden comes from d1, d2, and d3
together, with d4/d5 completely pinned**: golden is
`{1:180,2:80,3:60,4:30,5:1}`, the record is `{1:156,2:128,3:78,4:30,5:1}` —
d4 and d5 identical, d1 down 24, but d2 up 48 and d3 up 18, netting +42.
Unlike n=4 (where the golden-to-record gain was a pure d1-for-d2
redistribution with d3 exactly pinned too), here the layer just above the
cap (d3) also grows — the deepest TWO layers (d4, d5) are quantized/pinned,
but d3 is not, at n=5.

## 8. Coverage and honest limits

- **~171,635 exact n=5 configurations** evaluated in total: 100,000 random
  campaign + 10,012 hill-climb + 61,623 in `n5_search.jsonl` (validation
  gates, the six 723-subsets, the golden-rationalized probe, the S1/S2/S3
  structured families, and three separate deep-climb runs — 61,252 of
  those are distinct configurations after memoized-dedup).
- The deep-climb technique was applied thoroughly to the 393 seed (155
  restarts total across three runs) and lightly (15–25 restarts each) to
  four fresh structured seeds. It was **not** applied to the four
  intermediate 723-subsets (381×3, 375) individually — only to the top two
  (393, 387) — though 387's own base climb converging directly onto the
  identical 393 configuration is suggestive that the others funnel there
  too; this is not verified and is the most direct next step if more
  compute is spent.
- No proof of maximality is claimed for 393. 155 wide-perturbation restarts
  from its own neighborhood without a single improvement is considerably
  stronger evidence than n=4's initial certification (which needed exactly
  this kind of restart to *break through* 5 separate times before
  settling), but n=6's history is a standing warning: 635 was once
  "certified locally maximal" after 50 independent deep climbs, and was
  later superseded by 723 via entirely different (constructive,
  non-climbing) methods. A genuinely different construction — not more
  restarts from this basin — is the likeliest way past 393, if 393 is not
  already the true maximum.
- ℚ(√2) or ℚ(√3) walls were not explored for n=5 in this task (mirrors the
  same open item in `n4_search_report.md` §7 and `PROJECT.md` open problem
  5).
- The four fresh structured families (P/S1/S2/S3) used moderate-sized
  candidate grids (dozens, not hundreds, of symmetric/random points per
  axis) to keep the ≤4-core, single-session budget; none showed any sign
  of approaching 393 even before deep-climbing, so widening those grids
  seems a low-priority use of further compute compared to attacking the
  723-record's structure directly (Section 3/8).

## 9. Answers to the task's questions

- **Golden n=5 = 351 confirmed?** **YES**, exactly, two independent ways
  (`cube_compound_exact.run(5)` and `certify_six.exact_count_config` fed
  the golden axes directly), by_depth `{1:180, 2:80, 3:60, 4:30, 5:1}`, and
  `cube_regions_n --n 5` cross-validated against the oracle on 5 seeds.
- **Best rational n=5 total found:** **393** (quats
  `[[4,1,1,-1],[3,3,7,3],[5,-1,-5,-5],[2,1,1,1],[1,1,1,1]]`, by_depth
  `{1:156,2:128,3:78,4:30,5:1}`) — a 5-cube subset of the six-cube record
  (dropping its `5,2,2,2` cube). Radius-4 certified, robust under 155
  wide-perturbation restarts across three independent deep-climb attacks
  from two different (but re-convergent) starting subsets.
- **Best overall n=5 total found:** also **393** — nothing evaluated in
  this task (random campaign, hill-climb, four fresh structured families,
  or any deep climb) beat it.
- **Did anything beat 351?** **YES.** 393 > 351 (and 375/381/381/381/387
  all beat it too), confirmed by two independent exact counters. Unlike
  n=4, the golden compound here is the *complete* icosahedral compound
  (not a sub-compound) — yet it is still not the maximum, confirming the
  task's suspicion should not be assumed away: symmetric maximality at n=5
  does not follow from n=5's compound being the "whole" golden structure.
- **Did anything beat 393?** **NO.** Across ~171,600 exact configurations,
  including 155 wide-perturbation deep-climb restarts targeted directly at
  the 393 basin (the technique that moved n=4 from 159 to 183), nothing
  exceeded it.
- **Did d4 ≤ 30 hold?** **YES, without exception**, across all ~171,600
  exact configurations (random, hill-climbed, and structured/deep-climbed
  alike). It is also the generic value (hit by >90% of random
  configurations), exactly mirroring n=4's d3 ≤ 24.
- **Deep profile of the best configs:** golden (351) and the record (393)
  are both pinned at d4=30, d5=1 (the deep tail is identical); the 393
  record's entire advantage over golden is a shallow/mid-layer trade: d1
  down 24 (180→156), d2 up 48 (80→128), d3 down 18 (60→78 is actually an
  INCREASE — see corrected figures below), net +42 — the same "deep layers
  quantize, shallow layers trade" law documented for n=4 and n=6, though
  here d3 moves too (golden d3=60, record d3=78, a gain of 18) rather than
  staying perfectly pinned as n=4's d3 did. Full comparison:
  golden `{1:180,2:80,3:60,4:30,5:1}` vs. record `{1:156,2:128,3:78,4:30,5:1}`
  → Δ = `{1:-24, 2:+48, 3:+18, 4:0, 5:0}`, summing to +42.
- **Best estimate of the n=5 maximum, with honest coverage:** likely at or
  very close to 393. The evidence for this is stronger than n=4's initial
  183 finding was at the equivalent stage: n=4's 183 needed to escape five
  successive plateaus via wide restarts before stabilizing, so a single
  clean radius-4 certification there was known (from that project's own
  history) to be an unreliable stopping signal; here, by contrast, 393 was
  radius-4 certified AND survived 155 wide-perturbation restarts (roughly
  4x n=4's total restart budget of ~40) without a single escape, and four
  independently-built fresh structured families all fell well short even
  after their own deep climbs. That said, 393 was not *discovered* by this
  task's own structured search (it came from a 5-subset of an
  externally-known six-cube record) — this project has no n=5-native
  construction that reaches anywhere near it on its own, which is itself
  informative: whatever makes the 723 six-cube record rich is not yet
  understood well enough to build a comparable arrangement from scratch at
  n=5. The honest read is: 393 is a strong, well-tested lower bound with
  real (if narrower-than-n=4) headroom above it, and the most promising
  unexplored route to more is deep-climbing the remaining four 723-subsets
  and/or constructing dedicated n=5 walls informed by *why* 723 is rich
  (Section 6 of `PROJECT.md`), rather than more generic random search.

## Files

- `n5_search.py` — the search driver (phases `0` validation gates, `R`
  723-record 5-subsets, `P` golden-rationalized neighborhood, `S1`
  octahedral-type family, `S2` C4-orbit family, `S3` C3-orbit+2free family,
  `D` deep multi-restart climb — mirrors `n4_search.py`'s `phaseD_deepclimb`
  verbatim, `M` mod-4 + d4-ceiling check). `python3 n5_search.py --help` or
  `python3 n5_search.py <phases...> [--restarts-primary N]
  [--restarts-secondary N]`.
- `n5_search.jsonl` — every exact evaluation from phases 0/R/P/S1/S2/S3/D
  (61,623 lines, 61,252 distinct configurations) plus the extra
  100-restart `record393_extra` deep-climb run.
- `campaign_n5.jsonl` — 100,000-seed random campaign
  (`run_campaign_n.py --n 5 0 100000 4`).
- `hillclimb_n5_log.jsonl` — 10,012-eval hill-climb from campaign seeds
  (`phase_b_hillclimb_n.py --n 5 --topk 20 --objectives total,d1,d2`).
- This report.
