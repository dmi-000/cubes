# n = 4 record hunt: the golden wall is beaten — new record 183

*2026-07-12. Scope: establish the n=4 record and search above the golden
four-cube compound's 177. Deliverables: `n4_search.py`, `n4_search.jsonl`,
this report. ~300,000 exact configurations evaluated in total (see
Coverage below). Every count in this document is exact (rational or
ℚ(√5) arithmetic, no floating point in any predicate) and independently
cross-checked by two separate counters.*

## Headline result

**The golden four-cube compound (177) is NOT the n=4 maximum.** A purely
RATIONAL configuration reaches **183**, found by hill-climbing far beyond
the first local maximum a greedy search finds — the climb needed several
escapes from radius-4-certified local maxima via wide (multi-component)
perturbation before reaching this value:

```
quats = [[1,0,0,0], [0,5,3,2], [1,-4,-1,1], [1,1,-1,-4]]
by_depth = {1: 92, 2: 66, 3: 24, 4: 1}     total 183
```

Cube 0 is the identity (axis-aligned) rotation; the other three are
generic-looking rational quaternions with no obvious extra symmetry.
Verified two independent ways with an EXACT match on both the total and
the full depth histogram:

- `./cube_regions_n --n 4 --quats '1,0,0,0;0,5,3,2;1,-4,-1,1;1,1,-1,-4'`
  → `"bounded":183, "by_depth":{"1":92,"2":66,"3":24,"4":1}`
- `certify_six.exact_count_config` (independent Python oracle, rational
  rotations built via `golden_rotations.rot_from_quat`) → `183`,
  `{1: 92, 2: 66, 3: 24, 4: 1}` — identical.

183 is certified a **radius-4 local maximum** (no single-component move
of ±1..±4 on any of the 16 quaternion components improves it, checked
twice from two different discovery routes) and is a **robust plateau**,
not a lucky one-off: across 40 independent wide-perturbation restarts
from a neighboring point, 9 reconverged to exactly 183 and none exceeded
it. It is not a proof of maximality — only an exhaustive proof over all
rational configurations could establish that — but it is strong evidence
of a genuine local optimum, most likely global among rational
configurations at this search depth.

## 1. Golden four-cube compound: confirmed 177

`cube_compound_exact.run(4)` (the first 4 of the 5 golden/dodecahedral
cubes, ℚ(√5) exact arithmetic):

```
N=4: bounded regions = 177   by depth: {1: 104, 2: 48, 3: 24, 4: 1}
```

Re-derived independently: built the same 4 cubes' rotation matrices
directly from the icosahedral axes (axis-index triples `(0,1,2)`,
`(3,9,14)`, `(4,10,13)`, `(5,7,12)` out of the 15 two-fold axes,
handedness fixed by swapping two columns where the raw triple came out
left-handed) and fed them to `certify_six.exact_count_config` — same
engine class that validates the C++ counter. Result: **177**, by_depth
`{1: 104, 2: 48, 3: 24, 4: 1}` — exact match. Two of the four cube
matrices (rows, entries `a + b√5`):

```
cube 0 (axis-aligned):  [[1,0,0],[0,1,0],[0,0,1]]
cube 1:  [[1/4+r5/4, -1/2, 1/4-r5/4],
          [-1/4+r5/4, 1/4+r5/4, -1/2],
          [1/2, -1/4+r5/4, 1/4+r5/4]]
```
(cubes 2 and 3 are the analogous cyclic images; full matrices logged in
`n4_search.jsonl`, phase `"0"`.)

**Engine validation gate.** `cube_regions_n --n 4` cross-checked against
the `certify_six` oracle on 5 random seeds (1, 2, 3, 17, 999): exact
match on total AND full depth histogram in every case (111, 131, 127,
87, 127). The n=4 rational counter is validated before any search began.

## 2. Rational campaign: 200,000 seeds

`run_campaign_n.py --n 4 0 200000 4` (4 workers, ~12–20 ms/config).
Result: `campaign_n4.jsonl`, 200,000 exact configs.

- **Best random total: 137** (seed 148785, `by_depth {1:48,2:64,3:24,4:1}`).
  Far below 177 — confirms the established pattern (n=6: random plateaus
  around 635, well under the 723 record) that unstructured rational
  sampling cannot reach the good walls.
- Top of the observed spectrum: 137, 136(×8), 135(×1240), 133(×4),
  132(×46), 131(×7770), ... — dominated by totals ≡ 3 (mod 4) as
  predicted, with sparse off-residue neighbors.
- **mod-4 law**: predicted `bounded ≡ 2·4−1 = 7 ≡ 3 (mod 4)`. Exception
  rate in the random campaign: **3.33%** (6,655 / 200,000) — noticeably
  higher than n=6's <0.1% exception rate on its random campaign. This is
  an open observation, not resolved here: it may mean the n=4 parity law
  has more small-measure exceptional strata, or that 4-plane arrangements
  hit degenerate coincidences more easily than 6-plane ones; a proof-side
  investigation is future work.

## 3. Hill-climb from the campaign (phase_b_hillclimb_n.py)

Exact ±1/±2-component greedy climbs from the campaign's top-20 seeds,
3 objectives (total, d1, d2), 2 random restarts each, 4 workers:
7,023 exact evaluations (`hillclimb_n4_log.jsonl`).

| objective | champion | by_depth |
|---|---|---|
| total | **142** | {1:51, 2:66, 3:24, 4:1} |
| d1 | 137 (d1=48) | {1:48, 2:64, 3:24, 4:1} |
| d2 | 135 (d2=66) | {1:44, 2:66, 3:24, 4:1} |

142 > 137 (the campaign max), confirming climbing helps, but this greedy
single-pass climb from *generic* seeds still falls far short of both 177
and 183 — the good walls are not reachable by climbing from noise alone,
matching the n=6 lesson exactly.

## 4. Structured/symmetry families (n4_search.py phases G, S1, S2, S3)

Four structured families were built and searched, each generalizing an
n=6-record pattern down to n=4:

**Phase G — golden 3-subset + 1 free rational cube.** Mirrors
`golden_six.py`'s approach (which found 681 at n=6). Family A: free
cube's matrix `Q(quat)` (world-relative). Family B: `Q(quat)` composed
with the irrational golden cube 1. 204 evaluations (symmetric candidates
+ random + hill-climb). **Max found: 177**, and *only* when family B's
free cube coincides with one of the golden five's other two cubes
(quats `(0,1,0,0)`, `(0,0,0,1)`, `(1,1,1,1)`, `(1,-1,-1,-1)`,
`(1,-1,-1,1)`, `(1,-1,1,1)`, `(-1,1,1,1)` all land on exactly 177) — i.e.
this just rediscovers golden 4-subsets, consistent with the known fact
that every 4-subset of the golden five equals 177 (subset-maximality,
Postscript 2 of `six_cube_search_results.md`). **No rational (non-golden)
free 4th cube attached to a golden 3-subset beat or matched 177.**

**Phase S1 — exact-rational octahedral-type 2-axis-pair family.**
Generalizes `six6_mats` (n=6, 3 axis-pairs) to n=4 (2 axis-pairs), using
an INTEGER parameter t so every point of the sweep is exactly rational
(`quat=(t,±1,0,0)` and `(t,0,±1,0)`) — no floating-point angle
approximation anywhere. Sweep t=1..60, then hill-climb (all 4 cubes
free). Seed value: 93 at t=2. Greedy climb reached **159**
(`{1:68,2:66,3:24,4:1}`) — this is the starting point for the deep climb
in Section 5 below.

**Phase S2 — shared-C4-axis orbit of a tilted base cube.** cube_k =
Rz(k·90°)·Q0 for k=0..3 (Rz(90°) exactly rational). Symmetric + 24 random
Q0 candidates + hill-climb. **Max found: 141** (`q0=(-67,-166,-73,-186)`).

**Phase S3 — shared-(1,1,1)-C3 orbit of 3 + 1 free cube.** Mirrors the
n=6 record's shape (C3-orbit-of-3 + 3 free) scaled to n=4 (orbit-of-3 +
1 free); R111(120°) = quat (1,1,1,1), exactly rational. 14 orbit seeds ×
56 free-cube candidates + hill-climb. **Max found: 135**
(`q0=(-498,355,129,-476)`, `qfree=(3,1,1,1)`). Notably, the mod-4
exception rate WITHIN this family alone is **60%** (178/297 of its
records) — far above the 3.3% generic rate — a clean confirmation that
highly symmetric shared-axis walls "jump to the other allowed residue"
more often, as noted qualitatively for n=6 in `PROJECT.md` §5.

None of the four structured families alone beat golden's 177.

## 5. The deep climb that broke 177 (the key result)

The S1 champion (159) turned out to sit at the base of a much richer
basin that a single greedy ±1/±2 pass cannot see. The methodology (now
`phaseD_deepclimb` in `n4_search.py`, run as phase `D`):

1. Climb ±1/±2 to a local max.
2. **Certify** it at radius 4 (±1..±4 on every single component) — a
   strictly stronger test than the local-max stopping condition.
3. If certified, fire many **wide perturbations** (1–6 SIMULTANEOUS
   components, each shifted by ±1..±4) at the *original* starting
   config, then greedily re-climb each from scratch. A single-component
   search can never make a multi-component jump, so this is the only way
   to escape a genuine radius-4 local max into a better one.

Applied iteratively (each new plateau re-fed as the next radius-4-check
and restart base), the chain of certified local maxima was:

```
159 → 171 → 173 → 175 → 179 → 183
```

Every arrow is a case where the previous value passed its radius-4
certification (no single-component move improves it) but a WIDE
perturbation + reclimb found something strictly better — each of these
plateaus is real, not a search artifact, and escaping it needs a
genuinely different mechanism (multi-component jump) than the one that
found it (single-component climb). The final value, 183, itself passed
radius-4 certification twice (from two different configs reaching it)
and recurred in 9/40 further wide-perturbation restarts without ever
being exceeded.

**Reproducibility inside the deliverable script**: `n4_search.py`'s
phase `D`, run standalone with a fresh RNG seed (42, different from the
seeds used in the exploratory run above), independently reproduced
significant progress along the same chain — `159 → 169 → 171 → 179` —
within a single scripted invocation (`python3 n4_search.py D`, seeded
from `S1_CHAMPION`), confirming the *method* finds these values, not
just one lucky manual run. The exact 183 record's quats are logged
explicitly in `n4_search.jsonl` and are independently re-verifiable by
direct invocation of either counter (Section headline above); finding it
again is a matter of RNG luck in the restart loop, not of the record
being unreproducible — the config itself is a fixed, checkable fact.

## 6. Structural analysis: the depth trade-off, confirmed at n=4

Across all ~300,000 exact n=4 configurations evaluated in this task
(campaign + hill-climb + structured families + deep climb), the maximum
per-depth counts ever observed are:

| depth | max observed | notes |
|---|---|---|
| d1 | 104 | golden compound only; no rational config ever reached above 92 |
| d2 | 66 | reached by both the rational hill-climb champion (142) and the 183 record |
| d3 | **24** | **never once exceeded, in any of ~300,000 configs, rational or golden** |
| d4 | 1 | always exactly 1 (theorem: the depth-n core is a single convex body) |

**d3 ≤ 24 is a strong empirical ceiling** — the n=4 analog of the n=6
conjectures C4/C5/C6 (`d3≤164` etc. there). It is tight (achieved
generically by both the golden wall AND the 183 record AND the rational
hill-climb champion) and unbroken across every family tried.

**The golden compound (177) and the new record (183) sit at DIFFERENT
points of the same depth trade-off surface** described in `PROJECT.md`
§5 — this is the cleanest confirmation of that law found in this task:

| config | d1 | d2 | d3 | d4 | total |
|---|---|---|---|---|---|
| golden (177) | 104 | 48 | 24 | 1 | 177 |
| record (183) | 92 | 66 | 24 | 1 | 183 |
| Δ | −12 | +18 | 0 | 0 | **+6** |

d3 and d4 are IDENTICAL between the two — both sit exactly at the
deep-layer cap. The entire gain of the new record over golden is a
shallow-layer REDISTRIBUTION: it trades away 12 units of d1 richness for
18 units of d2 richness, netting +6. This is exactly the "deep layers
quantize, shallow layers trade" structure documented for n=6 (Postscript
14), now demonstrated as the mechanism by which n=4's record beats its
best "obvious" (golden/symmetric) candidate.

**mod-4 parity of the two records**: golden's 177 ≡ 1 (mod 4) — the
"other" allowed residue, a wall exception, exactly as `PROJECT.md` §5
predicts for highly symmetric walls. The new record 183 ≡ 3 (mod 4) —
the GENERIC residue, despite being a highly non-generic, hard-won point
of configuration space. This is a useful discriminator: the 183 record
is not obviously sitting on a coincidence-generating symmetric wall (no
extra plane concurrences are forced by symmetry the way the golden
compound's corner concurrences are); its richness looks like it comes
from a more subtle, lower-symmetry alignment. Characterizing that
alignment (which planes concur, at what multiplicity) is natural future
work, mirroring the incidence-geometry analysis `PROJECT.md` §6 did for
the n=6 chain.

## 7. Coverage and honest limits

- **~300,593 exact n=4 configurations** evaluated in total: 200,000
  random campaign + 7,023 hill-climb + 93,570 in `n4_search.jsonl`
  (structured families G/S1/S2/S3, the deep-climb chain, and validation
  gates — includes many repeated/logged intermediate hillclimb steps).
- The deep-climb methodology (Section 5) was only run from ONE structured
  starting point (the S1 champion) with extensive random-restart
  exploration around it; it was NOT systematically applied to every
  campaign/hillclimb/S2/S3 champion. Applying it more broadly (especially
  from the S2/S3 structured families, or from fresh random seeds at
  radius-4-certified local maxima in the 130s-140s range) has not been
  ruled out as a route to something above 183 — this is the most obvious
  next step, not a closed question.
- No proof of maximality is claimed for 183. Radius-4 single-component
  certification plus dozens of wide multi-component restarts is strong
  empirical evidence, not a proof; n=6's 635 record needed a similar
  radius-4 certification plus 50 independent deep climbs before being
  called "certified locally maximal," and even that record was later
  superseded by 723 via entirely different (constructive, non-climbing)
  methods. The same could happen here.
- ℚ(√2) or ℚ(√3) walls (echoing the n=6 program's Postscript 7-8) were
  NOT explored for n=4 in this task — only the golden ℚ(√5) wall (via
  the golden 3-subset) and plain rational configurations. This is an
  open direction (mirrors open problem 5 in `PROJECT.md`).

## 8. Answers to the task's questions

- **Confirmed golden n=4 = 177?** YES, exactly, two independent ways
  (`cube_compound_exact.run(4)` and `certify_six.exact_count_config` fed
  the golden axes directly), by_depth `{1:104, 2:48, 3:24, 4:1}`.
- **Best rational n=4 total found:** **183** (quats
  `[[1,0,0,0],[0,5,3,2],[1,-4,-1,1],[1,1,-1,-4]]`, by_depth
  `{1:92,2:66,3:24,4:1}`), reached via deep multi-restart hill-climbing
  from a structured (octahedral-type) seed, radius-4 certified, robust
  under 40+ restarts.
- **Did anything beat 177?** **YES.** 183 > 177, confirmed by two
  independent exact counters. This overturns the working assumption that
  the golden four-cube compound is the n=4 maximum, and updates the
  growth table: n=4 best known is now **183**, not "177" — the "+"
  status other n's in `README.md`'s table already carry.
- **Best estimate of the n=4 maximum, with honest coverage:** likely
  close to but not certainly at 183. The depth structure (d3 capped at
  24, d4=1, d1+d2 the only lever) bounds how much more room there is:
  the richest d1 ever seen is 104 (golden) and the richest d2 is 66
  (both the 142-champion and the 183-record); if some rational
  configuration achieved BOTH simultaneously (d1=104, d2=66) the total
  would be 104+66+24+1 = 195 — an a-priori ceiling from this task's own
  observed maxima per depth (NOT a proof that such a configuration
  exists; d1 and d2 richness may not be jointly achievable, especially
  since the campaign's own richest d1 configs plateau their d2 lower and
  vice versa). 183 should be read as a strong new lower bound with real
  headroom above it that a wider deep-climb campaign (Section 7) would
  most likely close further.

## Files

- `n4_search.py` — the search driver (phases `0` validation gates, `G`
  golden3+free, `S1` octahedral-type family, `S2` C4-orbit family, `S3`
  C3-orbit+free family, `D` deep multi-restart climb — the phase that
  found 183, `M` mod-4 check). `python3 n4_search.py --help` or
  `python3 n4_search.py <phases...>`.
- `n4_search.jsonl` — every exact evaluation from phases 0/G/S1/S2/S3/D
  plus the deep-climb exploration that reached 183 (93,570 records).
- `campaign_n4.jsonl` — 200,000-seed random campaign (pre-existing
  infrastructure, `run_campaign_n.py --n 4`).
- `hillclimb_n4_log.jsonl` — 7,023-eval hill-climb from campaign seeds
  (`phase_b_hillclimb_n.py --n 4`).
- This report.
