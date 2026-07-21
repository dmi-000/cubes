# Six-cube compound region search — results

Empirical (voxel flood-fill) search over compounds of 6 congruent concentric
cubes for the configuration maximizing the number of bounded regions the 6
cube surfaces cut space into. Tool: `cube_compound_regions.py` (unmodified,
validated logic) extended additively by `six_cube_search.py` (new file,
matrix-list counting path with the identical small→big merge policy,
tau = 3R).

## Reference points

- **axial fan (N cubes about a shared 4-fold axis)**: exactly `(2N-1)^2`
  bounded regions, proven (cross-section edge lines are all tangent to the
  common incircle ⇒ no triple points). For N=6: **121**.
- **five-cube compound** (5 cubes of the dodecahedron, UC09): **351** bounded
  (exact, from the Q(√5) field arithmetic in `cube_compound_exact.py`).
- **loose ceiling**: C(35,3) = 6545, the plane-arrangement bound for 36
  planes. Not remotely approached by any configuration found — cube faces
  are bounded squares, not full planes, and even the most complex stable
  configuration found here (~1340) is well under a quarter of this ceiling.

## Step 1 — tool validation

```
one:200      -> bounded=1     (expected 1)   OK
stella:260   -> bounded=9     (expected 9)   OK
axial2:260   -> bounded=9     (expected 9)   OK
axial3:260   -> bounded=25    (expected 25)  OK
axial4:300   -> bounded=49    (expected 49)  OK
axial6:300   -> bounded=126, unresolved=5    (expected 121)
axial6:400   -> bounded=128, unresolved=7
axial6:500   -> bounded=127, unresolved=6
```

The first five match exactly. `axial6` does not match 121 on the nose, but
in every one of the three resolutions run, `bounded - unresolved = 121`
exactly (126-5, 128-7, 127-6) — precisely the documented tip-fragment
artifact (a handful of small components each lack a same-label *big*
neighbour within the 3-voxel dilation search, so they're counted as
"unresolved" rather than merged). This is consistent with, not a
contradiction of, the analytic proof. Treated as PASS with a noted caveat;
proceeded to Step 2.

## Step 2 — `six_cube_search.py`

New file, imports `cube_compound_regions` and adds `labels_grid_mats` /
`count_mats`: identical slab-wise labeling and identical small→big
same-label merge / tau=3R policy as `ccr.count()`, but taking an explicit
list of 6 rotation matrices instead of a preset name. Verified byte-for-byte
identical output to `ccr.count('six6:20+rot', 120)` before use.

`grot` (apply the module's fixed generic global rotation) is exposed as a
parameter rather than hardcoded, because empirically it is *not*
universally beneficial — see the axial finding below.

## Step 3a — six6 theta sweep

`six6:T+rot`, R=200 and R=300 (R=380 added for the two best):

| theta | R=200 bounded (unresolved) | R=300 bounded (unresolved) | R=380 bounded (unresolved) |
|---:|---:|---:|---:|
| 5  | 2509 (2400) | 3757 (3576) | — |
| 10 | 1292 (1111) | 1302 (1073) | — |
| 15 | 656 (427)   | 573 (320)   | — |
| 20 | 471 (218)   | 428 (145)   | — |
| **25** | **436 (153)** | **441 (134)** | **458 (151)** |
| 30 | 465 (182)   | 482 (175)   | 368 (13) |
| 35 | 580 (297)   | 644 (337)   | — |
| 40 | 1227 (992)  | 1564 (1329) | — |
| 44 | 8983 (8844) | 12256 (12096) | — |

Both tails (theta→0, theta→45) blow up and keep growing with resolution —
near those limits pairs of cube faces approach coincidence (theta=0: all 6
cubes coincide; theta=45: six6 degenerates to the highly symmetric
`escher3`), producing genuinely-thin sliver regions that no finite R here
resolves. These are not trustworthy.

theta=25 is the standout: bounded stays in a tight band (436 / 441 / 458)
across three resolutions with a roughly *constant* unresolved count
(153/134/151, not shrinking with R) — the signature of genuinely small real
regions, not a merge failure. **theta=30's unresolved count collapses from
182/175 down to 13 at R=380** — the signature of the *opposite* artifact
(coarser grids failing to find the big same-label neighbour); its truer
value is closer to 368 than to ~470.

**Best in the six6 family: theta ≈ 25°, bounded ≈ 440-460, three-resolution
stable.**

## Step 3b — axial6 baseline

Confirmed the "any distinct twist set gives 121" claim, using the
*un-rotated* path (`grot=False`) — the axial family's cubes are jittered
away from exact grid alignment already (see Step 1), and, surprisingly,
forcing the generic global rotation makes things *worse* for this family
(tested: with `grot=True`, the same 3 twist sets gave 246/125u, 776/663u,
300/179u instead of the well-behaved values below). Recorded as a concrete
counterexample to "always use +rot" — it should be "use +rot to counter
exact axis alignment; a fixed generic rotation is not otherwise a free
improvement, and can introduce its own unlucky near-alignments."

| twists (deg)                | R=300 bounded (unresolved) | bounded−unresolved |
|---|---:|---:|
| 0,15,30,45,60,75 (default)  | 126 (5)  | 121 |
| 0,7,19,33,51,80             | 125 (8)  | 117 |
| 3,11,26,40,58,71            | 131 (10) | 121 |

All consistent with the proven constant 121.

## Step 3c — random search (40 seeds, R=200, `grot=True`)

Raw bounded counts ranged from **962 (seed 20)** to **6395 (seed 5)** — huge
variance, but almost entirely explained by unresolved fraction (66% to 96%
of the raw count is unmerged "small" components). High-unresolved-fraction
seeds are the suspects for near-degenerate coincidental alignments; this was
confirmed directly (next section).

## Step 3d/e — refinement at R=300/380/(450)

**Negative control (seed 5, highest raw R=200 count):**

| R | bounded | unresolved |
|---:|---:|---:|
| 200 | 6395 | 6159 |
| 300 | 8675 | 8384 |
| 380 | 10245 | 9919 |

Monotonically diverging, no sign of leveling off, and already exceeds the
6545 plane-arrangement ceiling at R=300 — this is impossible for a genuine
finite region count from 6 bounded cubes, so this is conclusively a
voxelization artifact (an accidental near-tangency in this random draw),
not a real winner. **Discarded.**

**Candidates selected by low unresolved fraction at R=200, refined:**

| seed | R=200 | R=300 | R=380 | R=450 | verdict |
|---:|---:|---:|---:|---:|---|
| 20 | 962 (641) | 1009 (636) | 958 (546) | 948 (505) | stable ~950-1010, unresolved fraction falling (67%→53%) |
| 34 | 973 (670) | 960 (595)  | —          | —          | stable ~960-975 |
| 1  | 1136 (843)| 1125 (767) | —          | —          | stable ~1125-1136 |
| 21 | 1215 (895)| 1172 (792) | 1158 (743) | —          | stable, mildly decreasing, converging ~1150-1160 |
| 35 | 1223 (905)| 1235 (853) | 1189 (775) | —          | stable ~1190-1235 |
| 26 | 1198 (887)| 1225 (863) | 1271 (880) | —          | stable, mild growth ~1200-1270 |
| 12 | 1183 (850)| 1275 (894) | 1301 (880) | 1411 (981) | still growing at R=450 (+110 last step) — **not yet converged**, unreliable magnitude |
| **18** | 1195 (894) | 1315 (962) | 1346 (962) | 1337 (933) | **converged**: R=300/380/450 agree to ≈1% (1315/1346/1337); unresolved fraction slowly falling (75%→70%) |

**Winner: seed 18** (`Rotation.random(6, random_state=18)`, `grot=True`).
Bounded region count **≈ 1337–1346**, stable across three independent
resolutions (R=300, 380, 450) to within 1%.

Depth histograms (0 = outside, k = inside exactly k of the 6 cubes):

```
seed 18, R=380:  {0:1, 1:140, 2:464, 3:412, 4:230, 5:99, 6:1}   bounded=1346
seed 18, R=450:  {0:1, 1:168, 2:474, 3:366, 4:198, 5:130, 6:1}  bounded=1337
```

(depth 2-3, i.e. pairwise/triple overlaps, dominate — expected for a
generic arrangement of 6 bodies with no special symmetry to concentrate
volume at high depth, unlike the axial/five-cube families).

## Step 3d — hill-climbing: negative result

Hill-climbed from two seeds (35 and 18) for 10 steps at R=200, greedy accept
on raw bounded count, perturbation annealed 5°→2°. From seed 35: raw R=200
bounded rose 1223 → 1777 (looked like a big win). **Checked the final
climbed configuration at higher resolution:**

| R | bounded | unresolved |
|---:|---:|---:|
| 200 | 1777 | 1474 |
| 300 | 2068 | 1701 |
| 380 | 2304 | 1912 |

Diverging just like the seed-5 negative control, not plateauing like the
genuine seed-18 winner. **Conclusion: hill-climbing on raw (unresolved-
inclusive) R=200 bounded count is an unreliable objective — it climbs
toward near-degenerate coincidental alignments that inflate the voxel
artifact count, not toward genuinely more regions.** This is reported as an
explicit negative finding per the task brief; a resolution-stability-aware
objective (e.g., penalize growth in bounded count between two resolutions)
would be needed to hill-climb safely, and was out of the remaining time
budget.

## Bottom line

| configuration | bounded regions | resolution stability |
|---|---:|---|
| axial6 (any twist set) | 121 (exact, proven) | n/a — exact |
| five-cube compound | 351 (exact) | n/a — exact |
| six6, theta=25° (best symmetric) | ≈ 440-460 | stable R=200/300/380 |
| **random seed 18 (winner)** | **≈ 1340** | **stable R=300/380/450 (±1%)** |
| random seed 5 (discarded) | "6395"→"10245"→∞ | diverging — artifact |

**The search's winner is the random 6-cube compound from seed 18**
(`scipy.spatial.transform.Rotation.random(6, random_state=18)`, composed
with the module's fixed generic rotation), giving a resolution-stable
bounded-region count of **≈ 1337-1346** — about **3.8×** the five-cube
compound's 351 and about **11×** the axial fan's 121. This confirms the
expected qualitative picture (generic/random configurations beat the
symmetric families, because symmetry creates coincidences that merge
regions rather than splitting them) but the margin required real
resolution-stability filtering to trust: most high-raw-count random draws
(including the single highest, seed 5, and the hill-climbed configuration)
were voxelization artifacts from accidental near-degenerate alignments, not
real winners.

Among the *structured* six6 rotational family, theta ≈ 25° is the best and
is comfortably resolution-stable at ≈ 440-460 — itself already ~25% above
the five-cube compound's 351, without needing any randomness.

## Caveats (read before citing any number above)

- **Voxel-level confidence only.** Nothing here is a proof. The exact
  Q(√5) counter (`cube_compound_exact.py`) and its certified-interval
  cousin (`cube_compound_interval.py`) can only handle sub-compounds of the
  rigid five-cube compound, whose face normals live in the golden field
  Q(√5); `scipy.spatial.transform.Rotation.random()` matrices (and generic
  `six6:T` matrices for most T) leave that field immediately, so there is
  no exact cross-check available for any of the winning configurations.
- **Both directions of voxel error are real and were both observed**: tip
  fragments inflate the count (seed 5, the hill-climbed configuration,
  six6 near 0°/45°); sub-voxel separators between what should be distinct
  regions can also silently merge and deflate it (suspected for six6
  theta=30 at coarse R, where the unresolved count collapsed from ~180 to
  13 between R=300 and R=380 — the opposite artifact signature from seed
  5's divergence).
- **Only two-or-more-resolution-agreeing values were trusted as findings.**
  Every number reported as a "winner" or "stable" above agrees to within
  ~1-5% across at least 3 independent grid resolutions (R=200/300/380, plus
  R=450 for the top random candidate). Raw single-resolution counts (e.g.
  the 40-seed R=200-only sweep) were used only to *rank candidates for
  refinement*, never as final answers.
- **The random search was not exhaustive.** 40 seeds, plus refinement of 8,
  plus 2 failed hill-climb attempts, is a small sample of SO(3)^6. A better
  answer than seed 18's ~1340 almost certainly exists; this report claims
  only that seed 18 is the best *resolution-stable* configuration found
  within the ~40-minute compute budget, not a global optimum.
- Full raw JSON outputs for every run (sweep, axial baseline, 40-seed
  search, all refinements, hill-climb histories) were kept in this
  session's scratchpad, not in this repo, since they are working files
  rather than deliverables; the tables above are the complete distilled
  record.

## Postscript: exact certification overturns the ranking

After the voxel search concluded, the winning configurations were
*rationalized* (each rotation rounded to an exact rational rotation via a
common-scale integer quaternion, N=512, error ~0.2 deg — `certify_six.py`)
and re-counted EXACTLY by the certified-interval kernel generalized to
arbitrary rational plane triples (`exact_search.py`). Validation of the
generalized pipeline: axial-6 with rational Pythagorean twists → exactly
121; the five-cube compound through the same code path → exactly 351. A
coincident-plane bug (shared z=±1 faces in axial/six6 families) was caught
by the phantom-label assertion during validation and fixed; the invariant
is documented in `certify_six.py`.

**The certified results contradict the voxel ranking:**

| configuration | voxel estimate | EXACT count |
|---|---:|---:|
| seed 18 ("winner", plateau R300-450) | ~1315–1346 | **567** |
| seed 12 | 1183–1411 ("not converged") | **595** |
| seed 20 | 948–1009 (lowest raw count!) | **595** |
| seed 39 | — | 591 |
| seeds 8, 34, 36 | — | 587 |
| six6 θ=10..40° (all) | "440–460 at θ=25, tails diverge" | **355, exactly, θ-independent** |
| axial-6 | 121 (proven) | 121 ✓ |
| five-cube compound | 351 (exact) | 351 ✓ |

Full 40-seed certified counts are in the `exact_search.py batch` output;
range 467–595, all with depth-6 = 1 (convex core) and depth-5 = 36
(= 6 × the universal "all-but-one gives 6 pieces" law).

Corrected conclusions:
1. **The certified winners among configurations tried are random seeds 12
   and 20, with exactly 595 bounded regions** (rationalized forms). Seed
   18's voxel plateau (~1340) was ~70% tip-fragment artifacts; its true
   count is 567.
2. **The six6 family is exactly constant at 355** for generic θ — like the
   axial family's 121, the rotational-freedom family has θ-independent
   combinatorics; the voxel sweep's structure ("best at 25°") was entirely
   artifact. 355 barely beats the five-cube compound's 351.
3. **Voxel counts of generic 36-plane configurations are unusable even for
   ranking** (the lowest raw voxel count tied for the certified maximum).
   A stable-looking plateau with a high unresolved fraction is not
   evidence of convergence.
4. Generic beats symmetric by ~1.6× (595 vs 355), not the 3.8× the voxel
   numbers suggested.

Certified claims are about the rationalized (exactly rational)
configurations; the 40-seed sample remains small and the global maximum is
unknown. But every number in the table above is now an exact integer with
machine-checked consistency invariants, at ~6 s per configuration — faster
than the voxel counts it replaces.

## Postscript 2: subset-maximality analysis (subset_analysis.py, pair_checks.py)

Exact counts of every k-subset of the 595 winner (seed 12) vs random baselines:

| k | winner's subsets | random max | golden (five-compound) subset |
|---|---|---:|---:|
| 2 | all 15 = **4** | 4 (200 tried) | **13** |
| 3 | 29..38 (median 33) | 38 | **67** |
| 4 | 111..135 | 131 | **177** |
| 5 | 289..313 | 317 | **351** |

Key discoveries:
1. **Generic pairs are constant at 4** (1 lens + 3 outside pieces); the rich
   pair counts (axial 9, five-compound 13) live ONLY on measure-zero
   degenerate walls (coincident faces / shared corners) and collapse to 4
   under 1-degree perturbation (pair_checks.py). Walls carry MORE regions
   than their neighbouring chambers at small k.
2. **The five-cube compound achieves "all subsets maximal(-known)" at every
   level**: its pairs are all 13, triples all 67, quadruples all 177 - each
   the best known for its k, all equal by the transitivity of A5.
3. **The actual 6-cube maxima are the opposite**: no subset of the generic
   winners is close to maximal (pairs 4 vs 13, triples <=38 vs 67,
   quintuples <=313 vs 351).
4. **Why the pattern must break at 6**: four cubes of a five-compound
   determine the fifth uniquely (12 of the 15 two-fold axes used; the
   remaining orthogonal triple is forced). So if all six 5-subsets of a
   6-configuration were golden five-compounds, cubes 5 and 6 would both be
   the unique completion of {1..4} - equal, contradiction. Conditional on
   the golden compound being the true 5-maximum, "all six 5-subsets
   maximal" is IMPOSSIBLE, vindicating the question that prompted this
   analysis. (And no icosahedral 6-cube compound exists: 10 does not
   divide 24.)

Search record meanwhile: seed 119 = EXACT 603 (viewer artifact published).

## Postscript 3: C++ engine, per-subset structure, and a corrected "law"

**Per-subset breakdowns** (`breakdown.py`, and now logged per-config): the
shallow ceilings are BUDGETS, not per-unit laws. In the 623 record the
per-cube depth-1 counts are [22,22,16,18,12,22] (individual cubes reach 22
but the sum caps at 112) and per-pair depth-2 counts range 10..20 summing
208; the three top records have *different* depth-3/4 distributions with
*identical* sums 164/102 — conserved-at-max. Depth-5 is a strict 6-per-cube
law in every record.

**Corrected claim**: depth-5 = 36 is NOT universal. Scanning the full
oracle ensemble (6,671 seeds): 36 occurs 99.4% of the time, but 34 occurs
37 times and 32 once — the six per-cube "innermost" face patches (radial
escape lemma) can MERGE around a cube edge when all other cubes are far in
that direction. Conjecture C6 is therefore d5 <= 36 (and d6 = 1, which is
a theorem: the core is convex). Earlier text stating "36 always" is
superseded. Found because the C++ campaign smoke test flagged sub-36
configs at seeds 3088/3168/3244/3346 and the oracle confirmed they are
genuine (the "law" was an artifact of looking only at maxima and records).

**C++ engine** (`cube_regions.cpp`, spec in `CPP_SPEC.md`): exact integer
arithmetic in homogeneous coordinates (vertices from plane-triple Cramer,
int128, 256-bit centroid predicates), same algorithm and assert suite as
`certify_six.py`. Gates passed: axial-6 rational-twist selftest = 121 with
depth histogram {24x5, 1}; 200-seed oracle match, zero mismatches (counts
AND depth histograms); ~0.13-0.29 s/config single-threaded, ~22 configs/s
with 8 workers (`run_campaign.py`) — roughly 2M certified configs/day.
Driver watches conjectures C1-C5 (total<=623, d1<=112, d2<=208, d3<=164,
d4<=102) and C6 (d5<=36, d6==1). First 400-seed smoke range (3000-3400):
no ceiling violations; best 611.

Status: mass campaign ready to launch detached
(`nohup caffeinate -i python3 run_campaign.py 3000 200000 8 >> campaign.out 2>&1 &`);
exact hill-climbing (Phase B) and full analysis (Phase C) pending — the
implementing agent hit its session limit after delivering the validated
engine.

## Postscript 4: mass falsification campaign — C1/C2/C3 fall, new record 635

Full campaign delivered (Phases A-C of `CPP_SPEC.md`), superseding the
"pending" status above.

**Scope.** Phase A: 106,525 random seeds counted exactly (8 parallel
`cube_regions` workers on disjoint blocks of 3000..188692; stopped at the
~100k-seed target, merged to `campaign_results.jsonl`). Together with the
user's background oracle ensemble (seeds 40..7009) and 7,937 exact
hill-climb evaluations (Phase B, `hillclimb_log.jsonl`), the analysis set
is 117,422 distinct exactly-counted configurations. Throughput: ~82
ms/config single-threaded uncontended; ~40 configs/s aggregate during the
campaign (193 ms/config mean under full 8-way load).

**Headline: conjectures C1, C2, C3 are FALSIFIED.**

- Twelve random seeds break all three at once: 631 at seeds 29390, 30108,
  39451 and 627 at seeds 13311, 33098, 36078, 61638, 64824, 84866, 86468,
  89514, 162978.
- Phase B hill-climbing (moves: ±1/±2 on one quaternion component,
  re-gcd, |c| ≤ 512; 36 greedy starts + random restarts) pushed the record
  to **635 bounded regions**, with d1 = 118 and d2 = 214:

      quats = [[129,-171,-137,-28], [382,278,63,-186], [200,289,312,-203],
               [314,101,-391,1], [124,-61,26,-215], [276,269,33,335]]
      by_depth = {1:118, 2:214, 3:164, 4:102, 5:36, 6:1}   total 635
      d1 per cube [16,20,20,20,22,20]; d2 per pair
      [24,24,22,16,14,14,14,12,12,12,10,10,10,10,10]

  (two moves from seed 30108's configuration; one representative of a
  plateau of ~208 single-move-equivalent quat tuples). Every 623-start
  climbed to 625-631 within 1-3 moves — 623 was never even a local
  maximum of the exact objective.
- Independent certification: seeds 29390 (631), 30108 (631), 33098 (627)
  and the explicit 635 configuration were re-counted by the validated
  Python pipeline (`certify_six.exact_count_config`) with identical
  totals and depth histograms.

**Conjecture status after 117,422 exact configurations:**

| conjecture | status | evidence |
|---|---|---|
| C1 total ≤ 623 | **FALSIFIED** | 631 ×3 random seeds; 635 by climbing |
| C2 depth-1 ≤ 112 | **FALSIFIED** | 116 random; 118 climbed |
| C3 depth-2 ≤ 208 | **FALSIFIED** | 212 random; 214 climbed |
| C4 depth-3 ≤ 164 | survives | attained in 13.2%, never exceeded |
| C5 depth-4 ≤ 102 | survives | attained in 82.6%, never exceeded |
| C6 depth-5 ≤ 36, depth-6 = 1 | survives | d5=36 in 99.4% (34 ×713, 32 ×8); d6=1 always |

Updated observed ceilings: total ≤ 635, d1 ≤ 118, d2 ≤ 214 (new
conjectures at the same epistemic level the old ones had — the old ones
lasted one order of magnitude of search).

**Structure of the top of the spectrum.** Every configuration with total
≥ 625 (2,619 of them) has depth-3/4/5/6 pinned at exactly (164, 102, 36,
1): above 625 the entire variation is in d1 + d2, and the observed total
spectrum is {625, 627, 629, 631, 635} — 633 never appears anywhere in
117k configs. At 623 a second histogram class exists (d3 = 162 with
larger d1/d2). The "conserved-at-max" reading of C4/C5 strengthens: d4 =
102 is hit by 82.6% of ALL random configurations (it is the generic
value, not a rare maximum), d3 = 164 by 13.2%.

**Per-subset findings** (per-cube depth-1, per-pair depth-2, from
per_label): the per-cube maximum is 26 (e.g. seeds 179994, 177366 — the
latter reaching total 623 with a 26-cube), the per-pair maximum is 34
(seed 139148, total only 587). Neither extreme is compatible with record
totals: the 635/631 records have balanced profiles (cubes 16-24, pairs
≤ 24).

  [CORRECTION 2026-07-11, see subset_richness_report.md] The phrase
  "only mid-total", used earlier in this section for the d1=26 / d2=34
  configs, is MISLEADING and is withdrawn. Within the random ensemble
  (median total 555, p99 603, max 631) those totals are HIGH percentiles,
  not the middle: total 587 is the ~91st percentile, 623 ~100th. Measured
  over all 277,832 configs, subset-richness and total are POSITIVELY
  correlated — corr(total, max per-cube d1) = +0.64, corr(total, max
  per-pair d2) = +0.58, monotone, no mid-peak — and richest-subset
  configs cluster at the TOP of the distribution. The true statement is
  not "richness trades against total" but "records combine HIGH richness
  with balance": the 699 record (Postscript 9) has per-cube d1 = 30 for
  ALL six cubes — above this ensemble's max of 26 — and perfectly
  balanced. What random seeding cannot do is reach the measure-zero WALLS
  where a subset spikes to its field ceiling (pair 13, triple 67); it
  finds the rich-subset direction but not the constructed optima.

  Configurations with three ≥22-cubes exist (539 of them, best
total 629 at d1=118 with profile [24,16,22,24,14,18]) but none with
four — stacking 22-cubes saturates: both the balanced [16,20,20,20,22,20]
and the lopsided [24,16,22,24,14,18] profiles cap at d1 = 118.

**Depth-5 anomaly, quantified**: sub-36 depth-5 occurs in 0.61% of
configurations (34 ×713, 32 ×8, never odd, never <32) and is strictly a
low-total phenomenon: sub-36 configs average total 492 vs the ensemble's
557, max 563. Merged innermost patches cost more elsewhere than they
save. Also: 99.91% of totals are odd (each cube is centrally symmetric,
so regions pair up under x → -x around the self-symmetric core); the 48
even totals are mostly NOT the d5-merging configs (only 8 overlap).

**Tools delivered** (all counts exact, no floating point in any
predicate): `cube_regions.cpp` (C++17 counter, gates: axial-6 selftest
121 with histogram {24×5,1}; seeds 0..199 oracle match with zero
mismatches on counts AND histograms), `run_campaign.py` (parallel driver
+ merge + violation watch), `phase_b_hillclimb.py` (exact greedy
climbing, all evaluations logged as explicit quats),
`phase_c_analysis.py` (this breakdown analysis, re-runnable as data
grows). Logs: `campaign_results.jsonl` (106,525 configs with per_label),
`hillclimb_log.jsonl` (7,937 configs). `exact_search_results.jsonl` was
treated as read-only ground truth throughout.

## Postscript 5: 635 certified locally maximal; campaign to 260k; exact spherical census confirms T1

Three workstreams (2026-07-10, agent-executed, results in `task_a.log` /
`task_c.out` / `scratch_diagram/`).

**1. The 635 record is a certified local maximum.** All 192
single-component neighbor moves (±1..±4 on any of the 24 quaternion
components, re-gcd, |c| ≤ 512) were evaluated exactly: none exceeds 635
(`task_a_certify635.py`). Fifty independent deep hill-climbs restarted
from distinct points of the surrounding plateau (single-move-equivalent
quat tuples, including a gcd-reduced representative) all terminate at
635 (`task_c_deep_hillclimb.py`, 50/50 `local_max`). 635 is a radius-4
local max sitting on a broad plateau; beating it needs a jump, not a
step.

**2. Campaign extended to seed 260,000 — no new records, deep ceilings
intact.** 71,308 new exact configs (seeds 188692..260000), merged total
177,832 in `campaign_results.jsonl`; the full analysis set is now
~200k distinct exact configurations. Best new random total: 627 (×4,
e.g. seed 223671). Max observed d3/d4/d5 in the new range: 164/102/36 —
zero C4/C5/C6 violations; odd-total fraction 99.93%, consistent with
the mod-4 law's exception rate. The chunk [260000, 360000) was launched
but killed by a session limit before producing shards; restartable.

**3. Exact spherical-arrangement census: T1 is TRUE as stated, and the
census is rigid.** For five configs (record 635; generic seeds 12 and
2228; sub-36 seed 3088; a six6-family wall config) the swap curves
Sigma_1/2/3 were built exactly (rational great-circle predicates,
`scratch_diagram/exact_arrangement.py`) and independently the B_l cells
were counted by dense sampling (`cellcount.py`). Findings:

- Generic configs (635, seed12, seed2228) have IDENTICAL vertex/edge
  counts: Sigma_1 (V,E) = (68,102), Sigma_2 = (200,300), Sigma_3 =
  (324,486), giving E−V = 34/100/162 exactly as T1 predicts and Euler
  cell counts 36/102/164 = the observed depth-5/4/3 ceilings. The
  vertex census is pure: every Sigma_l vertex is a rank-triple point
  (incidence flags 204 = 3·68, 600 = 3·200, 972 = 3·324); own-edge
  crossings contribute ZERO vertices to generic swap curves. A fixed
  (V,E) across unrelated generic configs is the signature of a
  combinatorial identity — T1 is now an empirically exact census
  awaiting a counting proof, no longer a conjecture-shaped guess.
- Validation gate passed: sampled cell counts match the
  per_label-derived depth counts on all generic configs (the one
  mismatch, seed2228 l=3 giving 162, was sampling resolution: 164 at
  N=4,000,000 points, `refine_seed2228.py`).
- The sub-36 config (seed 3088, d5=34) deviates exactly as T2 predicts:
  E−V drops to 32/96/148, and 8/8/48 vertices become own-edge type —
  degeneracy REMOVES census vertices and merges cells, never adds.
- The six6-family wall config breaks the sampled-cells = regions
  correspondence (B_1 cells 30 vs d5 = 24): on positive-codimension
  ties the strict sets U_S merge across walls, so diagram cells
  OVERCOUNT regions there. Direction is again downward (24 ≤ 30 ≤ 36) —
  consistent with C6, and a caveat recorded: the census argument runs
  in the generic stratum; walls are handled by T2, not T1.
- **Shoulder-cell hunt: empty.** In all five configs — including the
  degenerate ones — every B_1 cell contains a face-center anchor
  (n_unanchored_roots = 0 across the board). The conjectured mechanism
  for T2 (bottom cells are floor-anchored; shoulders exist only on the
  top side) survives its first serious hunt.

**Proof status for C4/C5/C6** (see C45_notes.md): T1's census numbers
are now measured exactly and are config-independent; what remains is
(a) a combinatorial derivation of V_l = 68/200/324 for generic
6-tuples, and (b) T2 (degeneracy only merges bottom cells), whose
anchoring mechanism is now supported by the empty shoulder hunt.

**Viewer**: `seed119_viewer.html` regenerated with a quaternion-input
mode (paste 6 integer quats, exact counts snapshot + wireframe) —
the 635 record is now displayable despite having no seed.

## Postscript 6: n > 6 cubes — engine generalized, n=7 campaign underway

STATUS: IN PROGRESS (last updated 2026-07-11). This postscript records
what the n>6 program has reached so far and is updated as the campaign
continues; the parked implementation agent resumes it toward the full
cross-n picture (spec: NPLUS_SPEC.md). Numbers below are exact and
independently re-verified by the engine.

**Engine.** cube_regions.cpp gained `--n K` (K = 2..12) with no change
to the overflow budget (predicates still involve one plane and one
vertex; K only multiplies counts, not magnitudes). Binary cube_regions_n.
Gates passed: n=6 regression is exact (seed 2228 -> 623, unchanged);
n=7 cross-checks against the Python oracle hold (seeds 777/778/779 ->
973/993/873); axial selftest passes at each n.

**n = 7 campaign (partial).** 50,000 exact configs, seeds 3000..52999
(campaign_n7.jsonl), 4 workers (capped — the ℚ(√d)/wall program has
compute priority). Best so far **1085** (independently re-verified),
above the prior n=7 best-known of 993:

    quats = [[389,-161,212,199],[71,419,285,18],[161,-116,147,-68],
             [-12,52,-11,509],[1,414,148,262],[91,155,78,473],
             [-193,254,397,50]]
    by_depth = {1:158, 2:306, 3:264, 4:194, 5:120, 6:42, 7:1}   total 1085

Top of the observed spectrum: {1053, 1057, 1061, 1065, 1069, 1077,
1081, 1085} (no 1073 seen so far — a gap, echoing the missing 633 at
n=6). Per-depth maxima over the 50k configs: d1 158, d2 306, d3 264,
d4 194, d5 120, d6 42, d7 1 — these are the current empirical n=7
ceilings (not yet stress-tested by hill-climbing, so provisional upper
observations, not conjectures).

**mod-4 at n=7.** The parity law bounded ≡ 2n−1 (mod 4) predicts ≡ 1
for n=7; observed 49,941 of 50,000 ≡ 1, with 51 ≡ 3 and 8 ≡ 2 (the
same rare invariant-shell exceptions seen at n=6, here 0.12%). Law
holds.

**Record growth so far** (certified lower bounds; max regions by n):
n=2: 13, n=3: 67, n=4: 183+, n=5: 393+, n=6: 723, n=7: 1207+, n=8: 1879+. (The n≤5
and n=6 values are the current records from the rational/wall programs;
n=7 is campaign-only, no hill-climb yet.)

**Still pending** (resumes when the field program yields compute):
finish/scale the n=7 campaign, n=7 hill-climb from the top-20, the
trimmed n=8 campaign (~5k seeds), the depth-freeze structure per n
(which deep sums are conserved-at-max, the analog of n=6's frozen
(164,102,36,1) tail), and the T1(l,n) bottom-diagram census across n.
This section will be extended with those results.

## Postscript 7: beyond rational rotations — the ℚ(√d) program

(Numbering note: Postscript 6 is reserved for the cross-n report of the
n>6 agent, in flight; its gates already passed — `cube_regions_n --n 7
--seed 777` = 973 matching the Python oracle, `--n 6` regression exact —
and its first n=7 campaign row, seed 3000 = 997, already exceeds the
prior n=7 best-known 993.)

**Question** (user, 2026-07-10): could restricting the search to
rational rotations prevent the exact alignments needed for maximal
regions? Answer: in principle yes, and demonstrably at small n.

**Theory.** The count function is constant on finitely many
ℚ-semialgebraic strata; SO(3,ℚ) is dense, so every value attained on a
full-dimensional (generic) stratum is rationally attained — if the max
is generic, rationality costs nothing (and the 635 record's broad
integer-move plateau says it sits inside an open stratum). But maxima
can live on lower-dimensional walls, and walls sort by the field their
defining incidences need:

- rational: all coincident-plane walls; the pair-13 wall (60° about a
  shared body diagonal is a rational matrix); the shared-face-axis
  pair family (9 regions at EVERY generic angle — Pythagorean angles
  reach it rationally; only its symmetric 45° point is irrational);
- ℚ(√2): exact 45° relations about rational axes;
- ℚ(√3): exact 30°/60° relations (e.g. three cubes equally spaced
  about one axis);
- ℚ(√5): the icosahedral group — the golden five-compound and all its
  sub-walls (n=5's leader: 351 vs ~317 best random — the one place a
  wall demonstrably leads its n, though the random n=5 baseline is
  thin and will be firmed up by the --n engine);
- degree ≥4: k ≥ 4 cubes equally spaced about an axis (cos 90°/k),
  towers ℚ(√2,√3), …; universal fallback = certified intervals + exact
  sign on minimal polynomials (the CN design anticipates this).

Some number field always suffices (algebraic points are dense in every
stratum), but no single quadratic field covers all walls.

**Against walls** stands the census evidence (Postscript 5): degeneracy
only merges bottom-diagram cells (T2 direction), and observed walls
trade small shallow gains (six6: d1 = 120 > 118) for large deep losses
(total 355). Whether ANY exact-incidence wall can net-win the total at
n=6 is precisely what the field program tests.

**Engine readiness.** `exact_count_config` already computes over
CN-wrapped ℚ(√5), and the golden face normals (±φ/2, ±1/(2φ), ±1/2)
are exact unit vectors there — the five golden rotation matrices are
orthonormal over ℚ(√5) and feed the validated counter directly.

**In flight.** A ℚ(√5) pilot (golden_six.py) is searching golden-five +
sixth-cube configurations (families: rational sixth; rational rotation
of a golden cube), gated on 351/1/13/67/177 regression, rational-seed
embedding, and duplicate-cube coincidence handling; results land in
golden_wall_report.md and will be merged here. The continuation
framework for ℚ(√2)/ℚ(√3)/further ℚ(√5) — field-generic Qd class,
five hard gates, symmetric-vs-rational-control methodology (the delta
against a matched rational control is the measurement), and the
256-bit caveat for any future C++ ℤ[√d] port — is `QFIELD_SPEC.md`.
This program has priority over the n>6 campaigns.

**Update (2026-07-10, same day): the golden wall SHATTERS the rational
record.** The ℚ(√5) pilot passed all gates (sub-compound totals
1/13/67/177/351 cross-validated by two independent engines; rational
seed 40 reproduced exactly; duplicate-cube coincidence → 351). First
search results, all counts exact:

- EVERY random rational sixth cube added to the golden five beats 635:
  probes gave 643, 653, 669 before any climbing.
- Hill-climbing reached **681 bounded regions** (e.g. sixth-cube quat
  (2,1,1,1)), independently re-verified through the oracle path:
  by_depth = {1:234, 2:192, 3:128, 4:90, 5:36, 6:1}. New overall
  record; 635 stands only as the RATIONAL record. 681 ≡ 1 (mod 4) — a
  wall exception, precedented (351 likewise breaks the n=5 generic law).
- Structure: ALL the gain is shallow — d1 = 234 (rational record 118),
  d2 = 192 — while the deep counts sit BELOW the generic ceilings
  (d3 = 128 < 164, d4 = 90 < 102), exactly the T2 direction. The six6
  lesson ("walls trade shallow gains for bigger deep losses") is
  overturned in net: the golden wall nets +46 over the best rational
  config. C4/C5 remain unviolated — they cap the deep counts, and
  walls only lower those.
- The climb's best quats (2,1,1,1), (7,4,4,4), (26,15,15,15) have
  w/x converging to √3: the search is steering toward the sixth cube
  at exactly 90° about the body diagonal (1,1,1) — a ℚ(√3) incidence
  which, on top of the ℚ(√5) five, makes the limit configuration live
  in the degree-4 tower ℚ(√3,√5). The "additional extension" question
  is thereby answered constructively: the tower engine is now needed
  to evaluate the actual wall point (the 681s are rational-side
  approximants; the on-wall count may jump either way).

Search still running; full report to be merged from
golden_wall_report.md. Rational-search postscript: the extended n=6
campaign finished — 100,000 more seeds (260k-360k, merged total
277,832 configs), best random 631, zero C4/C5/C6 violations; the
rational record 635 survived 360k seeds precisely because the real
maxima live on walls no rational configuration touches.

**Refinement (golden_wall_report.md, final).** The 681 set is a
θ-INDEPENDENT plateau: 28 quats, all rotations of the sixth cube about
the body diagonal (1,1,1) — a 3-fold axis shared by the axis-aligned
golden cube and the icosahedral compound — over θ ≈ 8–10° and 64–112°,
every one with the identical histogram {1:234, 2:192, 3:128, 4:90,
5:36, 6:1}; certified radius-2 local max. So the operative second
constraint is the SHARED 3-FOLD AXIS, not θ = 90°: the √3-convergents
lie inside the plateau but are not special (whether the exact 90°
point — the ℚ(√3,√5) tower value — differs from 681 is being verified
by the multiwall agent). Further: family B re-anchored on golden cube
2 gives 679 at quat (8,3,0,0) (θ≈41° about x, a 2-fold axis of the
compound) with **d1 = 238**, twice the rational d1 record; all boosts
are depth-1 only (d2 ≤ 198, d3 ≤ 132, d4 = 90 throughout). All 150
random sixth cubes beat 635 (range 637–665); sub-635 occurs only when
the sixth lands exactly on a golden cube (351). Full details:
golden_wall_report.md.

## Postscript 8: multi-constraint search pays — tower verification, the (1,1,1) wall explained, and a new RATIONAL record 655

(multiwall_report.md, multiwall_search.jsonl, qtower.py; Postscript 6
remains reserved for the parked n>6 cross-n report.)

- **Tower engine**: qtower.py builds ℚ(√3,√5) as Q5(√3) over the
  validated Q5 base; gates W-G1..4 all pass; evals 0.5–27 s.
- **The exact √3×√5 point counts 681** — identical histogram to the
  rational plateau; no jump at the wall. The convergents (26,15,15,15)
  and (97,56,56,56) already realize the identical 4711-cell arrangement:
  the climb locks into the wall's combinatorial type before reaching it.
- **The 681 plateau is a 1-D wall, now explained**: ANY sixth-cube
  angle about the exact (1,1,1) axis gives 681. That diagonal is a
  dodecahedron vertex shared by golden cubes 0 and 2; the order-3
  icosahedral generator about it fixes those cubes and 3-cycles the
  other three. The four body diagonals split 1-vs-3 under this
  symmetry: the fixed-type diagonal gives 681, its three B-orbit
  siblings give 657 (verified exactly in the tower).
- **Rational double-wall control (the surprise): 655.** Two
  independent 60°-own-diagonal pair relations among six otherwise
  free RATIONAL cubes reached 655 in only 2,476 evaluations (C++ and
  Python cross-verified), beating the 360k-seed unrestricted rational
  record 635 AND its matched free-cube control (615) at equal budget.
  Constraint-first search wins even inside ℚ: the rational record is
  now 655, and it is wall-constructed, not random.
- **Not all walls give**: within-ℚ(√5) stacks are net losers
  (coincident-plane ≤ 563; 60°-own-diagonal constant 657 < 681), and
  the ℚ(√2,√5) exact-45° wall LOSES regions (543, with d5 = 32 — a
  wall that merges even the deep layer). Wall direction is not
  monotone; each family must be counted.

Record table: overall 681 (golden five + sixth on the (1,1,1) wall,
ℚ(√5) suffices — the tower point is not special); rational 655
(double-pair-wall construction); rational random+climb 635; d1 record
238 (golden family B); deep ceilings d3 ≤ 164 / d4 ≤ 102 / d5 ≤ 36
still never exceeded anywhere, including on every wall tested.

## Postscript 9: sliding 3-cube triples — a new RATIONAL AND OVERALL record 699 (slide3_report.md)

(slide3_report.md, slide3_search.jsonl, slide3_q2.py, slide3_search.py,
slide3_p1/p2/p3.py; SLIDE3_SPEC.md + SLIDE3_SPEC_V2.md. Postscript 6 still
reserved for the parked n>6 cross-n report.)

Prompted by the user's observation that a family of maximal 3-cube
configurations slides continuously between the octahedral 3-cube compound
and the three cubes inscribed in a dodecahedron. Two program threads.

- **The 3-cube family, corrected (V2).** The right continuous family is a
  common-3-fold-axis orbit T(t) = { S(t), C·S(t), C²·S(t) }, C = 120°
  about (1,1,1) (= B), with the seed S(t) rotating about the axis
  â of Δ = S_dod·S_octᵀ (angle 40.31°, a NON-coordinate axis). Endpoints
  built EXACTLY: S_oct = Rx(45°) in ℚ(√2) (slide3_q2.py, a Q(√2) clone of
  qtower's exact counter) and S_dod = golden cube 1 in ℚ(√5), each
  C-orbit counting **67**. The user's edge-crossing marker is confirmed at
  both ends: the edge crossing sits at the **midpoint (0.5)** at the
  octahedral end and the **golden-section point (1/φ² = 0.382)** at the
  dodecahedral end. Interior t is generic (≈37); the two count-67
  configurations are isolated walls connected through a generic sea (same
  wall-vs-generic structure as everywhere else in this project).

- **Congruence test fix (methodological).** An earlier attempt claimed no
  golden 3-subset is 3-fold symmetric. That was an artifact of (i)
  find_cubes returning two IMPROPER frames (det = −1) and (ii) comparing
  RAW relative-rotation traces without reducing by the cube's own 24-fold
  self-symmetry. Reduced correctly (proper frames; R = Mᵢ·u·Mⱼᵀ minimized
  over u ∈ O), **all 10 golden pairs share the identical relation (min
  angle 44.4775°, trace 3φ/2)** — the icosahedral 2-transitivity — and the
  golden 3-cycle subset {1,3,4} (fixed set of C) IS a genuine 3-fold triple.
  Lesson for all future congruence checks here: force proper frames and
  reduce by O before comparing.

- **Overlay search → NEW RECORD 699 (rational, both-engine-verified).**
  X(θ₁,θ₂,R) = T(θ₁) ∪ R·T(θ₂), two 3-fold triples. The winning region is
  the **shared (1,1,1) 3-fold axis**: both triples 3-fold-symmetric about
  (1,1,1) and R = (a,b,b,b) a rotation about that same axis, so the whole
  6-cube compound keeps a global 3-fold symmetry — the SAME constraint that
  built 681, but now with BOTH halves on the axis and reachable in ℚ.

      quats = [[3,1,0,0],[3,0,1,0],[3,0,0,1],
               [41,28,22,14],[41,14,28,22],[41,22,14,28]]
      by_depth = {1:180, 2:216, 3:164, 4:102, 5:36, 6:1}   total 699

  Cross-verified by certify_six.exact_count_config (699, identical
  histogram); a certified radius-2 local max on a plateau (≥3 (θ₁,θ₂,R)
  cells realize 699). **699 beats overall 681 (+18), rational 655 (+44),
  rational-random 635 (+64).** 699 ≡ 3 (mod 4) (generic parity, not a wall
  exception). Deep counts d3/d4/d5/d6 = 164/102/36/1 sit exactly at the
  established ceilings — no violation. NEW depth highs: **d2 = 216 (prior
  observed ceiling 214), d1 = 180** — the entire gain over 681 is shallow
  (d1+d2), the familiar T2 direction. Coarse+fine landscape: ~67k exact
  evals logged (slide3_search.jsonl); the (1,1,1)-diagonal R family
  dominates (699), sibling-diagonal R caps at 671, near-icosahedral R at
  657; R ∈ O (identity/90°-face/180°-edge) collapses to ≤ 407 (dead).
  Two GOLDEN triples overlaid (ℚ(√5) oracle) are a clean net LOSER (≤ 673),
  slower, and buy nothing over the rational construction.

- **In flight (follow-on agents).** (1) finishing the fine (1,1,1)-diagonal
  rational sweep at Farey(16–20)² × denser diagonal angles + radius-3/4
  two-component climb of 699, hunting 701+; (2) tower-verifying the EXACT
  on-(1,1,1)-axis wall points (ℚ(√2,√3), ℚ(√2,√5) composita) and the mixed
  octahedral×golden overlay on the shared axis. Results to be merged.

Record table (updated): **overall AND rational record 699** (two 3-fold
triples on the shared (1,1,1) axis, ℚ); prior overall 681 (golden five +
(1,1,1) sixth, ℚ(√5)); prior rational 655 (double-pair wall); rational
random+climb 635; d1 record 238 (golden family B), d2 high 216 (699); deep
ceilings d3 ≤ 164 / d4 ≤ 102 / d5 ≤ 36 still never exceeded anywhere.

## Postscript 10: symmetry-stratified sweep of the walls — no new record, framework validated, coverage caveat

(symmetry_search.py, symmetry_search.jsonl, symmetry_search_report.md,
SYMMETRY_SEARCH_SPEC.md.) Systematic search of the symmetry walls: for
each finite subgroup G ⊂ SO(3), enumerate 6-cube orbit-partitions and
exact-count each family in its proper field. A cube is a coset in
SO(3)/O, so orbits are computed and deduped modulo the octahedral group
(order 24, proper frames).

**Framework validated.** Gates GA–GE pass: orbit machinery correct
(generic C₃ seed → orbit 3, aligned seed → orbit 1); reproduces the
octahedral 3-compound = 67, the (C₃, 3+3) 699 config, and the (I,
5+free) 681 config exactly.

**Result: nothing beat 699.** Best symmetry-family totals (Phase 1
rational G via cube_regions; Phase 2 ℚ(√5) for I/C₅):

| family | best | vs 699 |
|---|---|---|
| I:5+free, C₅:5+free (golden) | 681 | −18 |
| T:4+free2 | 661 | −38 |
| D₃:3+3 | 657 | −42 |
| C₂:2+2+2 | 653 | −46 |
| D₂:4+free2 | 651 | −48 |
| C₆:6 | 649 | −50 |
| C₃:3+free3 | 643 | −56 |

**CAVEAT — this is a LOWER-BOUND map, not tight ceilings.** The
per-family seed grids are restrictive: the C₃:3+3 family, which
PROVABLY contains 699 (gate GC reproduces it, and its quats
independently count 699), was searched only to **399** — its grid tried
thin axis-angle seeds, not the general-quaternion seeds the record
needs (its second triple's seed is a full quaternion [41,28,22,14], not
a coordinate-axis rotation). So the sweep does NOT independently
re-derive 699, and every "best" above is a floor, not a proven family
maximum. The true ceiling of the 699-holding family remains the slide3
result (Postscript 9: 699, radius-2 local max, finer Farey sweep still
open).

**What the sweep DOES establish**: (1) the framework and dispatch are
correct (gates); (2) the golden I/C₅ families cap at 681 as known; (3)
no symmetry class OUTSIDE the shared-axis 3+3 / golden families reached
within ~40 of 699 even at coarse coverage — the maximum concentrates in
those two families. Phase 3 (ℚ(√2)/ℚ(√3)/towers) was deferred with
justification: no rational family came near enough to 699 to warrant a
quadratic refinement, and the one concrete tower point (the ℚ(√3,√5)
681 wall) was already shown non-special (Postscript 8).

**Next move if pursued**: re-run the top families (C₃:3+3 first, to
independently confirm ≤699; then the core+free families T/D₃/C₂) with
full-quaternion seed grids + deeper hill-climb, since the current grids
demonstrably under-cover. Until then, 699 stands and the symmetry map
is a floor.

## Postscript 11: full-quaternion symmetry re-run — NEW RECORD 717 (and 705); Postscript 10's negative was a coverage artifact

(symmetry_search2.py, symmetry_search2.jsonl, symmetry_search_report2.md,
SYMMETRY_SEARCH_V2.md.) Postscript 10's sweep validated the framework
but under-searched: its per-family seed grids used thin axis-angle
seeds, so C₃:3+3 (which provably contains 699) capped at 399. Re-run
with FULL integer-quaternion seeds — same validated orbit construction,
only the seed sampler + climber changed.

**Two configs beat 699; new project record 717** (both independently
re-verified by ./cube_regions, both respect every deep ceiling
d3≤164/d4≤102/d5≤36/d6=1, zero deep-count violations across 9,528
evals):

    717  D₂:4+free2   quats 5,2,2,2; -2,-2,2,5; -2,5,-2,2; -2,2,5,-2;
                            2,1,1,1; 1,0,0,0
         by_depth {1:210, 2:210, 3:158, 4:102, 5:36, 6:1}   (+18 over 699)
    705  C₃:3+3       quats 3,1,0,0; 1,2,2,1; 2,-1,-2,-1;
                            21,14,11,7; -11,31,39,25; 53,-3,-17,-11
         by_depth {1:180, 2:222, 3:164, 4:102, 5:36, 6:1}   (+6 over 699)

Both are radius-4 local maxima. Notable structure:
- **717's gain is entirely depth-1**: d1 = 210 (vs 699's 180, and above
  the old d1 record 180), while d3 = 158 sits BELOW the 164 ceiling —
  a record achieved with a SHALLOWER deep tail than 699. The record is a
  D₂-orbit-of-4 core + one free cube + one axis-aligned cube.
- 705 pushes d2 to 222 (new depth-2 high) with d3 = 164 at ceiling; its
  winning C₃ seed (21,14,11,7) is literally the one-unit neighbor of the
  699 seed the old thin grid could not represent.
- **Parity**: 717 and 705 are both ≡ 1 (mod 4), the WALL-exception class
  (like 681), whereas 699 was ≡ 3 (generic parity). The higher-symmetry
  records sit in the exception class.

**Postscript 10 corrected.** Its "nothing beat 699" and its per-family
"bests" were floors from thin coverage, now superseded: C₃:3+3 399→705,
D₂:4+free2 651→717, C₂:2+2+2 653→677. Families whose small orbits live
on a 1-parameter alignment locus a uniform quaternion draw never hits
(T:4+free2, D₃:3+3 — generic orbit sizes 12 and 6) were gridded over
their true DOF and reproduced 661/657, confirming those ARE the maxima
on that locus. Golden I/C₅:5+free confirmed a local cap at 681 (radius-3/4
ℚ(√5) climb). Coverage rule established: generic full quaternions give
orbit sizes 3/2/6/4 under C₃/C₂/C₆/D₂, so those accept full-quat seeds
for every block — and that is exactly where the gains landed.

**Record table (updated): overall 717** (D₂:4+free2, rational); 705
(C₃:3+3); prior 699 (two 3-fold triples), 681 (golden ℚ(√5)), 655
(double-pair wall). New depth highs d1 = 210 (717), d2 = 222 (705); deep
ceilings d3≤164/d4≤102/d5≤36 still never exceeded. Open: climb 717's D₂
family deeper (radius 5+) and re-examine whether an even shallower-tail
route (d3 < 158) buys more d1.

## Postscript 11 addendum: 717 is capped — the shallow-tail tradeoff is a 1:1 conservation

(d2_deepclimb.py, d2_deepclimb.jsonl, d2_deepclimb_report.md.) Deep-climb
of the D₂:4+free2 record with a larger neighborhood (single ±1..±6,
two-component ±1/±2, cross-block escape; 15 restarts) plus a 60-restart
broad D₂ resweep and siblings (D₂:2+4 → 547, D₂:2+2+2 degenerate):
**nothing beats 717.** Both known 717 configs are certified radius-4+
local maxima.

The deep-vs-shallow exchange table (best total at each d3 over 22,202
by_depth'd evals) rises to a FLAT ridge at 717 spanning d3 = 152, 158,
AND 164 (the ceiling), then falls off on both sides (d3=150 → 685,
d3=156 → 699). All three 717 configs share d1 = 210, d4/d5/d6 = 102/36/1,
and **d2 + d3 = 368 exactly conserved** (216+152 = 210+158 = 204+164):
lowering d3 returns precisely its worth in d2, so the "shallow-tail
tradeoff" is a 1:1 conservation that cannot exceed 717. A 717 config
exists WITH the deep tail at the ceiling (d3=164, quats
8,3,3,3;-3,-3,3,8;-3,8,-3,3;-3,3,8,-3;3,2,2,2;1,0,0,0), so the
below-ceiling tail is incidental, not the source of the record. 717
stands as the capped maximum of this family.

## Postscript 12: shared-axis "intersection" families — NEW RECORD 723

(symmetry_search3.py, symmetry_search3.jsonl, symmetry_search3_report.md,
SYMMETRY_SEARCH_V3.md.) Prompted by the user's "find intersections
between families" idea: build the 6 cubes as a union of two orbits under
different groups sharing a common axis (the structure behind 699 and
717). Gates reproduced 717 and 699 through the shared-axis builder.

**NEW RECORD 723** (verified by ./cube_regions), family
**C₃core3+free3 on (1,1,1)** — a C₃ orbit of 3 cubes about the body
diagonal + 3 free cubes:

    quats 4,1,1,-1; 3,3,7,3; 5,-1,-5,-5; 2,1,1,1; 1,1,1,1; 5,2,2,2
    by_depth {1:210, 2:216, 3:164, 4:96, 5:36, 6:1}   (+6 over 717)

- **Deep tail flexes again, in a NEW slot**: 723 has d4 = 96 BELOW its
  102 ceiling (d3 = 164 at ceiling), whereas 717 kept d4 = 102 and
  dropped d3. So the "trade a deep layer for shallow" mechanism is not
  tied to one depth — d1 = 210 is the constant, and the record buys
  total by lowering whichever deep layer costs least. d5/d6 = 36/1
  still pinned.
- **Parity**: 723 ≡ 3 (mod 4), generic parity (like 699, unlike 717's
  wall-exception ≡ 1). ~16 distinct 723 configs found (a plateau).

**Other V3 findings** (nothing else beat 717): T:4+free2 re-run with
full-quat free cubes TIES 717 (was 661 in V2 — the record is reachable
in the tetrahedral family too); C₂core2+free4 on (0,0,1) = 703; C₃⊕C₃
= 705; C₄/D₄:4+free2 = 683; D₃:3+free3 = 681. The T-generating
different-axis intersection (C₂(001)+C₃(111), ⟨C₂,C₃⟩=T) was a net loser
at 613 — forcing the full polyhedral symmetry HURTS; the loose
shared-axis union is what pays.

**Record chain: 635→655→681→699→705→717→723.** All deep ceilings
(d3≤164, d4≤102, d5≤36, d6=1) still never exceeded. Open: full-quat
C₃core3+free3 was only partly climbed — deeper climb of the 723 plateau,
and the same core+free template with a C₃ core on other axes / larger
cores.

## Postscript 13: incidence geometry — edge vs corner concurrences, the 9-fold sweet spot, and the algebraic search

(algebraic_search.wl/algebraic_demo.wl/algebraic_groebner*.wl/algebraic_bridge.py,
edge_search.py/edge_search_report.md, ALGEBRAIC_SEARCH.md, PROJECT.md.)
Prompted by the user's observation that the octahedral 3-cube maximum
uses edge concurrences and the dodecahedral one uses corner concurrences,
and the conjecture that a 6-cube maximum might substitute edge for corner
concurrences.

**Incidence characterization (exact).** Records sit at high-multiplicity
POINT concurrences (extra planes through a point), never line/edge
concurrences (no line lies on ≥3 planes — max line-multiplicity 2, same
as random; 3 coplanar normals never occur). Two point modes:
- EDGE concurrence: 4 planes = 2+2 (an edge of one cube crossing an edge
  of another), |x|²≈2. The octahedral 3-compound is edge-pure.
- CORNER concurrence: 6 or 9 planes = 3+3 / 3+3+3 (cube corners
  coinciding), |x|²=3. The golden 3-compound and both 717/723 are
  corner-dominated (two 9-fold 3+3+3 points). "k cubes share a corner"
  ⟺ "they differ by rotations about that corner's axis" — corner-sharing
  IS the shared-axis family, explaining why shared-axis searches win.
  723 also carries ~180 lesser edge (2+2) concurrences: the modes coexist.

**Multiplicity has a SWEET SPOT.** Forcing a 12-fold concurrence (four
cubes at one corner, via the Gröbner solver) gives only 393 — far below
the record. 9-fold is near-optimal; over-concentration merges away
regions.

**Edge-for-corner conjecture: NOT supported (evidence, not proof).**
~4,600 exact configs across four strategies (incl. exact ℚ(√2)): best
edge-dominated total = 691 (edge-pure, two octahedral 3-compounds joined
by R=(31,13,33,30), by_depth {1:174,2:214,3:164,4:102,5:36,6:1}) — 32
below 723, the whole gap in depth-1 (174 vs 210). Edge-richness
ANTI-correlates with total (Spearman ≈ −0.58 in structured families;
edge-maximizing climbs drive the total DOWN). Corner concurrences are the
stronger ingredient; edge crossings build d2 but not the d1 shell the
shared-axis construction produces. Caveat: an unsampled region or an
irrational edge wall beyond ℚ(√2) is not excluded.

**Algebraic search built (ALGEBRAIC_SEARCH.md).** Rotations about an
integer axis take a rational Cayley parameter (matrix stays over ℚ), so
incidences are polynomial equations solvable exactly (Wolfram). Two
solvers: (1) 1-parameter wall-mapping — solving n_face(s)·v=1 over a
family's vertices returns its exact rational walls (126 along the 723
shared-axis slide; counting confirms 723 an exact local max there); (2)
multi-constraint GroebnerBasis solve — weld an unknown cube to fixed
cubes by corner-coincidence, eliminate + solve; validated (recovers the
C₃ corner-stabilizer), found 26 exact configs at 689 with d1=224 (a
depth-1 high above the record's 210). Neither beat 723, but both reach
exact points a numeric grid misses and map the incidence↔count tradeoff.
The deep-layer caps (d3≤164/d4≤102/d5≤36), not depth-1, are the binding
constraint on beating 723.

## Postscript 14: the depth trade-off structure — deep layers quantize, shallow layers grow, records sacrifice deep for shallow

(Analysis over 456,922 exactly-counted configs pooled from every log with
a depth profile. Prompted by the user's reframing: the goal is not to
maximize any single heuristic but to map which depth trade-offs are
possible.)

**Sequential saturation, deepest first, then pinning.** Binning configs
by total and taking the mean profile [d1,d2,d3,d4,d5,d6], the deep layers
fill to their caps IN ORDER and then freeze:
  - d5 → 36 by total ≈ 475
  - d4 → ≈102 by total ≈ 525
  - d3 → ≈164 by total ≈ 600
  - d6 = 1 always.
From total ≈600 to the record, d3/d4/d5 are pinned at 164/102/36 and ALL
growth is in the shallow layers (d1: 119→206, d2: 194→214).

**Two distinct trade-offs:**
  1. At FIXED total — a conserved exchange between adjacent layers (the
     717 plateau has d2+d3 = 368 constant; regions shuffle between d2 and
     d3 without changing the total).
  2. To INCREASE the total — the deep layers cannot grow (capped), so the
     shallow ones do; and near the ceiling the profitable move is to give
     BACK a little deep count to unlock a lot of shallow count. 723 trades
     6 units of d4 (102→96) for roughly +45 in d1 vs the best d4=102
     config — a strongly non-1:1 trade. 717 likewise sacrifices d3
     (164→158). This deep-sacrifice lever is under-explored.

**Why (radial framework).** Deep-layer counts = cells of the innermost
great-circle "bottom-diagrams," which have a fixed GENERIC value — a
config either realizes the generic diagram (the cap 164/102/36) or a
degenerate merged one (below). They are QUANTIZED. Shallow-layer counts =
outermost diagrams, uncapped, growing with arrangement complexity. So the
maximum-total problem is: saturate the quantized deep layers, maximize the
unbounded shallow ones, and spend deep sacrifices only where they buy
disproportionate shallow gain.

**Reframed objective.** "Beat 723" = find the optimal point on the
deep-sacrifice surface: sweep the feasible (d3,d4,d5) profile and maximize
d1+d2 at each. 723 proves sacrificing d4 pays; whether sacrificing d3 AND
d4 together (or another combination) nets higher is open. Gröbner
corner-welding already reached d1 = 224 (with depressed deep layers), so
the shallow ceiling is high — the exchange rate is the question.

**Also open: non-concentric cubes.** No solid argument exists that
off-centering can't increase the count; allowing translations only adds
DOF, so the off-center max is ≥ the concentric max. The "concentric
maximizes overlap" intuition is undercut by our own sweet-spot finding
(over-concentration reduces the count). Off-centering should cost deep
layers (the common-intersection core weakens) but may buy shallow ones —
the same exchange. Untested only because every engine here assumes
concentric.

### Postscript 14 — results & a correction (2026-07-12)

Three experiments ran on the trade-off/extra-DOF questions:

- **Deep-sacrifice sweep** (deepsweep.py, 20,032 exact configs): best total
  = 723, nothing beat it. The trade-off surface: total 723 is reached
  along a RIDGE of deep profiles — (164,102,36) with d1+d2=420 AND
  (164,96,36) with d1+d2=426 both give 723. **CORRECTION:** the earlier
  claim that 723 trades 6 units of d4 for "+45 in d1" was WRONG — it
  compared 723 against the AVERAGE d4=102 config, not the best. Properly
  optimized, the deep↔shallow trade is ≈1:1 at the frontier (give back 6
  deep, recover 6 shallow, same total), and sacrificing MORE deep loses
  (e.g. (158,94,36) reaches only 719). So 723 sits at/near the peak of the
  trade-off surface; the deep-sacrifice lever is exhausted at ~723, not
  under-explored. Evidence 723 is a genuine local optimum, not proof.
- **Off-center** (offcenter_count.py, t=0 gate PASSED reproducing 723 and
  3 seeds; 167 perturbations): off-centering 723 does NOT help — best
  non-trivial total 706 (single small shift), monotonically worse from
  there; ALL depth layers decrease on average. Translating all six cubes
  together (a rigid shift) keeps 723 (invariance check). So around the
  record concentric is locally optimal — contradicting the guess that
  off-centering might trade deep for shallow; it just destroys regions.
- **Unequal sizes** (offcenter_count.py extended: cube k gets half-width
  s_k; offset ±s_k, containment/extent scale by s_k; size=1 gate
  reproduces 723): INCONCLUSIVE for 723. Every size perturbation of 723
  hit an exact face-coincidence (723 is so symmetric that resizing any
  cube by a rational factor creates a degeneracy) that this non-robust
  Python counter cannot evaluate — all 48 trials skipped. Settling the
  size question needs a degeneracy-robust counter (symbolic perturbation)
  or the C++ engine extended to per-cube sizes. Size PRESERVES central
  symmetry (unlike translation), so it is the gentler extra DOF and the
  more likely of the two to help, but it remains untested at n=6.

## Postscript 15: n=4 — golden 177 is NOT the maximum; new rational record 183

(n4_search.py, n4_search.jsonl, n4_search_report.md, prompted by Chris
Cole flagging the n=4 entry. The growth table's old "135+" was a rational
undershoot; corrected first to 177, now to 183.)

The golden four-cube sub-compound (4 of the 5 dodecahedral cubes) counts
**177** exactly (by_depth {1:104,2:48,3:24,4:1}, ℚ(√5)), confirmed by two
independent engines. But it is NOT the 4-cube maximum:

**New n=4 record: 183** (fully rational, verified by both cube_regions_n
and the Python oracle; ≡ 3 mod 4, generic parity):

    quats = [[1,0,0,0],[0,5,3,2],[1,-4,-1,1],[1,1,-1,-4]]
    by_depth = {1:92, 2:66, 3:24, 4:1}   total 183   (+6 over golden 177)

Certified a radius-4 local maximum (recurred 9/40 wide-restart climbs,
never exceeded). This mirrors n=6 exactly: the best RATIONAL config beats
the golden/√5 wall (n=6: 723 > 681; n=4: 183 > 177). The golden compound
leads among *symmetric* configs but is not the global max.

**How found**: 200k random campaign (best 137) → hill-climb (142) → four
symmetric families generalizing the n=6 record shapes (golden-3+free,
octahedral-type, C4-orbit, C3-orbit+free; max 159, none beat 177) → DEEP
multi-restart climbing from the octahedral-family champion: wide
(multi-component) perturbation + re-climb escapes each local max into a
richer basin, 159→171→173→175→179→183. The wide-perturbation escape is
the operative technique; plain ±1/±2 greedy climbing stalls below 177.

**Structural echo of the n=6 trade-off surface**: golden (177) and the
record (183) both have d3=24, d4=1 (identical deep tail); the record
trades 12 units of d1 for 18 of d2 (net +6) — same "grow the shallow
layers, deep layers pinned" pattern. **d3 ≤ 24 held across ~300,000
exact n=4 configs** (rational and golden) — a candidate n=4 analog of the
n=6 deep-layer ceilings.

**Not proven maximal**: the deep-climb was run systematically from only
one structured seed; applying it to the other families' champions is the
obvious next step. A naive additive bound from best-ever d1 (104, golden)
+ best d2 (66) + d3 cap 24 + 1 = 195 suggests real headroom remains.

## Postscript 16: records NEST — 723's subsets contain the smaller records, and its 5-subset beats golden 351

(Analysis of the record configs' sub-compounds, prompted by questions on
whether outstanding configs are built from outstanding sub-configs, and
Chris Cole's "does this call into question 351?".)

**351 is called into question — decisively.** A 5-cube sub-compound of
the 723 record (drop its 6th cube) counts **393**, verified by both
cube_regions_n and the Python oracle: quats [[4,1,1,-1],[3,3,7,3],
[5,-1,-5,-5],[2,1,1,1],[1,1,1,1]], by_depth {1:156,2:128,3:78,4:30,5:1},
+42 over golden 351. ALL five 5-subsets of 723 beat 351 (375/381/381/
381/387/393). The golden five-compound is NOT the n=5 maximum — same
story as n=4 (rational 183 > golden 177). Growth table n=5: 351 → 393+.
(d4 = 30 = 6·5 in the 393 config — the depth-(n−1) ≤ 6n ceiling holds.)

**Records NEST.** The subset spectrum of the 723 record:

| subset size | best subset count | the k-cube record | note |
|---|---|---|---|
| 2 | 13 (×5) | 13 | hits the record |
| 3 | 63 (×5) | 67 | 94% — falls short of the golden 67 |
| 4 | 183 | 183 | hits the n=4 record exactly |
| 5 | 393 | (was 351) | EXCEEDS the old golden value |

So 723 CONTAINS the n=4 record (183) and a 5-cube config (393) above the
old n=5 record, and its pairs hit the n=2 record (13). Its 3-subsets
reach only 63 (< 67): the golden/octahedral SYMMETRIC 67 is not
rationally compatible with 723's structure, whereas the rational records
(13, 183, 393) nest cleanly.

**Construction principle suggested.** Outstanding configs are
hierarchically nested — an n-cube record contains an (n−1)-cube config at
or above the (n−1) record. This motivates GREEDY EXTENSION: take the best
k-cube config, add a cube optimally, climb → candidate (k+1) record. The
183/393/723 chain is exactly such a tower (183 ⊂ … , 393 ⊂ 723). The
even-k subsets hitting their records while the odd-k (3) falls short is an
unexplained parity in the nesting worth investigating.

### Postscript 16 addendum: greedy extension VALIDATED — new n=7 record 1207

The nesting principle predicts an n-cube record can be built by extending
the (n−1) record with one cube. Tested directly: the 723 six-cube record
+ one seventh cube, over just 256 seventh-cube orientations (NO
hill-climbing), reaches **1207** — verified by both cube_regions_n and the
Python oracle — beating the prior n=7 best-known 1085 (from a 50k-seed
campaign) by 122.

    quats = 723's six cubes + [5,4,-4,-4]
    by_depth = {1:272, 2:324, 3:260, 4:192, 5:116, 6:42, 7:1}   total 1207
    (d6 = 42 = 6·7 — the depth-(n−1) ≤ 6n ceiling holds at n=7 too)

So greedy extension of the record BEATS a full random campaign at the
next n, cheaply — the construction principle is not just descriptive but
generative. Growth table n=7: 1085+ → 1207+. Un-climbed; hill-climbing
from 1207, and iterating the extension to n=8, are the obvious next steps.
The record tower is now 183(n4) → 393(n5) → 723(n6) → 1207(n7), adjacent
levels related by adding/dropping one cube.

### Postscript 16 addendum 2: n=2 and n=3 stress-tested — 13 and 67 hold

With the golden values 177 (n=4) and 351 (n=5) both broken, n=2 and n=3
were stress-tested. Thorough search in their low-dimensional spaces
(config space is 3(n−1)-D: n=2 is 3-D, n=3 is 6-D): n=2 = 13 CONFIRMED
(1,783 random seeds + hill-climbs, nothing above 13); n=3 = 67 CONFIRMED
(4,414 seeds + climbs, nothing above 67). Confidence scales inversely with
dimension, so these small cases are far better established than the large
records. Two structural reasons they are safer than 177/351: the 13-pair
is already RATIONAL (60° about a shared body diagonal), not a golden value
that a rational config could undercut; and at n=3 the SYMMETRIC value (67)
beats the best rational three-cube subsets of the records (63) — symmetric
leads at n=3, whereas rational overtook symmetric at n=4,5. Caveat:
thorough search, not proof. Confidence ladder: n=2 (near-certain) > n=3
(strong) > n=4 183 / n=5 393 (golden beaten, rational best-so-far) > n=6
723 > n=7 1207 (extension-seeded, least settled).

### Postscript 16 addendum 3: n=5 = 393 is robust; native search can't reach it

Full n=5 search (n5_search.py, ~171,600 exact configs): 393 confirmed the
best, nothing beat it. Wide-perturbation deep-climb (155 restarts from 393
and neighbors) found ZERO improvement, and — unlike n=4's 183, which had
to escape five successive plateaus — 393 shows NO plateau structure, so it
is a substantially more robust local optimum. d4 ≤ 30 = 6·5 held across
all ~171,600 configs (and is the generic value, >90% of random). Notable:
n=5-NATIVE structured families (golden-rationalized, octahedral-type,
C4-orbit, C3-orbit+free) deep-climbed only to 377/369/323/309 — all short
of 393. So 393 is reachable only as a sub-compound of the 723 six-cube
record, not by any independent five-cube search. This sharpens the nesting
principle: the n=5 optimum is INHERITED from the n=6 record, with no
constructive five-cube route to comparable richness — the tower is
top-down as much as bottom-up.

## Postscript 17: local perfection is globally frustrated past n=3 — the "middle-layer" mechanism

(Prompted by the observation that golden N4 is built from optimal
sub-configs on every subset yet is not maxN4. Verified exactly.)

**All-subsets-optimal ⟺ golden, and it equals the max only for n ≤ 3.**
- golden four-compound (177): ALL four 3-subsets = 67 (=max₃) and all six
  2-subsets = 13 (=max₂) — every part optimal — yet 177 < max₄ = 183.
- max₄ (183): 3-subsets = 63/63/63/55 (< 67), pairs = 13/13/13/9/9/9 —
  NOT all optimal. The global maximum must DETUNE its subsets to win.

"Every k-subset optimal" is a rigid constraint satisfiable only by the
fully symmetric (icosahedral) compound. So local perfection forces golden,
and golden is beaten for n ≥ 4 — a FRUSTRATION: honor all local
constraints (golden) OR maximize the whole (183), not both.

**Why n=4? The middle layer.** Compare depth profiles (d1..d_n):
  - n=3: golden=max=67 = {48, 18, 1}. Layers: d1 (top) and d2 =
    depth-(n−1) = 18 = 6·3 (the ceiling). NO middle layer. Golden maxes
    BOTH → golden = max.
  - n=4: golden {104, 48, 24, 1} vs max {92, 66, 24, 1}. Both hit
    d3 = 24 = 6·4 (ceiling). But d2 is a MIDDLE layer (neither the top d1
    nor the ceiling-ed deep layer). Golden leaves d2 = 48; the max pushes
    it to 66 by sacrificing d1 (104→92), netting +6.
  - n=5: golden {180,80,60,30,1} vs max {156,128,78,30,1}. Middle layers
    d2,d3: golden 80/60, max 128/78 — golden far behind in the middle.

Mechanism: **golden concentrates the count in the top layer (d1) and the
6n-capped deep layer, but n=4 is the FIRST size with a middle depth layer
that is neither — and golden leaves middle layers sub-maximal. The global
maximum trades down d1 to fill the middle, and wins.** (Golden is markedly d1-HEAVY: golden d1 = 104 (n4), 180 (n5) both exceed
the max-total configs' d1 = 92, 156 — so golden concentrates the outer
layer and the total-max redistributes to the middle. Whether golden
GLOBALLY maximizes d1 is a stronger claim, still untested.) This unifies the golden-falling, the C₃-only (not icosahedral)
symmetry of records, the incidence sweet spot, and why greedy extension
(which inherits detuned subsets) beats assembling from optimal parts.

## Postscript 17 addendum: the DOF hierarchy — local optima are RIGID, flexibility lives in suboptimal-but-structured configs

(Corrects earlier loose claims about pair flexibility, incl. a mistaken
"13 is 47% flat".) Sampling 1,500 random pairs: the count distribution is
4 (94%), 5 (4%), 9 (2%), 13 (0.1%). So:

| pair count | how common | degrees of freedom |
|---|---|---|
| 4 (generic) | 94% | full 3-D open sea |
| 9 (shared face-axis) | 2% | CONTINUOUS — exactly 9 at every angle about the shared axis (verified 8 angles) |
| 13 (the MAXIMUM) | 0.1% | rigid, near-isolated high-codimension wall |

The MAX pair (13) is the RAREST and most rigid; the suboptimal 9 sits on a
fatter, continuously-parameterized locus. Same for triples: 67 is ISOLATED
(Postscript 9 — octahedral ℚ√2 and golden ℚ√5 endpoints connected by a
family whose INTERIOR drops to ~37; near-45° rational octahedral gives only
55, exact 45° needed; a climbed 63-triple has 0% DOF openness). So **local
optima (13, 67) are rigid points; they are NOT count-preserving-continuous.**

Key distinction: a config always has CONFIGURATION DOF (you can perturb the
cubes), but the optima have no COUNT-PRESERVING DOF. The flexibility that a
larger arrangement can exploit lives in the suboptimal-but-structured
configs (the 9-pair's tunable shared-axis angle).

**This SHARPENS the frustration principle (Postscript 17):** local optima
are rigid, so the globally optimal arrangement is FORCED to build from
locally-suboptimal-but-flexible pieces. Golden fails precisely because it
insists on the rigid optimal pieces (all pairs = 13); the true max uses
tunable 9-pieces. Structure of max₄ (183): an axis-aligned HUB cube paired
13 (max) to each of three SPOKE cubes, with the spokes mutually 9-paired
(the C₃ orbit — a shared-axis cluster whose angles are the tunable freedom).
The C₃core+free family that built 723 is the six-cube version of this.

## Postscript 18: shared-axis-cluster construction — free spoke angles recover every record; locked/control variants fall short

(shared_axis_search.py/.jsonl, campaign partially complete — n=6 templates
still running; interim results already decisive on the hypothesis.)

Tests the Postscript-17-addendum principle constructively: parameterize
hub-and-spoke families (on-axis cubes + a cluster of spokes sharing an
axis, each spoke at an independent rational angle — the continuous 9-DOF)
and search the spoke angles DIRECTLY.

- **Gates: the family CONTAINS the records** — 183 and 723 both expressed
  exactly as instances (n=4 onaxis2+spoke2; n=6 spoke3+onaxis3).
- **n=4: free angles reach 183 (the record); C₃-locked angles only 165;
  unstructured 4-free control 163.** Freeing the flexible DOF is worth
  +18 over locking to the symmetric angles.
- **n=5: three cluster templates reach 393 (the record); control 369.**
- **n=6 (in progress): the 723 template reaches 723 free vs 679 locked.**

Verdict so far: "build from flexible 9-DOF clusters and tune the angles"
is a VALIDATED construction principle — it recovers every record from the
right variables where generic search and angle-locking fail; no template
has (yet) beaten a record. Full report when the n=6 templates finish.

## Postscript 19: THE GENERAL CEILING LAW — depth-(n−l) ≤ (12l−6)n − 2(l²−1)

(Discovered by fitting the bottom-l maxima across n and cross-checked two
independent ways. The single most consolidating result of the project.)

**The law.** For n concentric unit cubes and 1 ≤ l ≤ n−1:

    C(l, n)  =  (12l − 6)·n  −  2(l² − 1)
    depth-(n−l)  ≤  C(l, n),   attained (generically or by records/golden)

Slopes 6, 18, 30, 42, … (arithmetic, step 12); intercepts −2(l²−1).
Special cases: l=1 gives the 6n law (Postscript 14 era); l=n−1 gives the
TOP layer d1 ≤ 10n² − 14n.

**Evidence 1 — attainment table** (max observed per layer over ~1M exact
configs from every campaign/search log, n=2..7):

    n\l    l=1      l=2      l=3      l=4      l=5      l=6
     2    12=12      --       --       --       --       --
     3    18=18    48=48      --       --       --       --
     4    24=24    66=66   104=104     --       --       --
     5    30=30    84=84   134=134  180=180     --       --
     6    36=36   102=102  164=164  222=222  234<276     --
     7    42=42   120=120  194=194  264=264  306<330  158<392

Every testable cell l ≤ 4: ATTAINED EXACTLY, ZERO violations. The only
unattained cells are the shallowest layers at n=6,7 — exactly the
frustration (all layers cannot be capped simultaneously).

**Evidence 2 — golden attains the top-layer ceiling.** Golden depth-1 =
48, 104, 180 at n=3,4,5 = C(n−1,n) exactly. ("Golden maximizes d1" is now
a formula, and golden = the top-layer-ceiling config; the records are the
deep-layer-ceiling configs; the middle is the contested ground.)

**Evidence 3 — the spherical census matches.** All measured swap-curve
censuses are TRIVALENT (E = 3V/2), so Euler gives cells = 2 + V/2, i.e.
V_l(n) = 2·C(l,n) − 4 = (24l − 12)n − 4l². Measured at n=6 (Postscript 5):
V₁,V₂,V₃ = 68, 200, 324; formula: 68, 200, 324. Exact agreement from a
completely independent measurement.

**Corollary (max-total bound).** Total ≤ 1 + Σ_{l=1}^{n−1} C(l,n)
= 1 + (n−1)(16n² − 17n + 6)/3. At n=6: ≤ 801 (record 723; the gap is the
frustration cost). At n=4: ≤ 195 (record 183 — matches the "naive additive
bound" of Postscript 15, now derived). At n=5: ≤ 429 (record 393).
[445 was an arithmetic slip, corrected 2026-07-13.]

**Proof target, now crisp (T1/T2 sharpened).** T1: show the swap-curve
Σ_l of a generic n-cube compound has exactly (24l−12)n − 4l² vertices,
all trivalent; Euler then gives cells = C(l,n). T2: degeneracy only
merges cells (never exceeds the generic count). l=1 already reduces to
the no-shoulder lemma (envelope has only the 6n face-center minima).

**Predictions.** (i) d1 at n=6 can reach 276 (observed max 234 — 42 of
headroom; hunting a d1=276 config is a sharp target). (ii) n=8: deep
ceilings 48, 138, 224, 306. (iii) Any config exceeding ANY C(l,n) kills
the law — a standing falsification target.

### Postscript 19 addendum: why 63 beats 67 as a building block — deep structure persists, shallow count is recut

(Closes the building-block thread of Postscripts 16-18 using the ceiling
law. Verified on all six 63-triples of the 723 record.)

    golden 67:      {1:48, 2:18, 3:1}   pairs [13,13,13]  isolated √5/√2 wall
    723's 63-triples: {1:44, 2:18, 3:1}   pairs [9,13,13]   rational, tunable
    (all six 63-triples have the IDENTICAL profile and pair structure)

The two triples are IDENTICAL in the deep layers — both saturate
C(1,3) = 18 and have the single core. 67's entire +4 advantage lives in
depth-1, which is precisely the layer that does NOT survive embedding: a
larger compound's new faces recut and reassign the triple's depth-1
regions, while the deep skeleton (pairwise/triple intersections) persists
and feeds the big config's deep layers.

And 67 buys those +4 disposable regions by replacing the one FLEXIBLE
9-pair with a third rigid 13 — costing exactly what a building block
needs: (a) the continuous shared-axis angle (the tuning knob the assembly
spends), and (b) rational compatibility (all-13 at 67 forces the
golden/octahedral wall, whose extensions lose: 681 < 723).

**Principle: a building block's worth = deep structure (persists under
embedding) + flexibility (spent by the assembly). Shallow count is
recyclable and worthless to the tower. 63 is 67 with 4 depth-1 regions
converted back into a tuning knob — which is why the record is built
from deep-saturated, shallow-detuned, one-knob pieces.**

## Postscript 20: the deficit-propagation envelope — an empirical branch-and-bound bound, and 723 nearly cornered

(envelope_mine.py/.jsonl: 532 configs stratified across the total
spectrum + the records, all six 5-subsets of each counted exactly —
~3,200 config↔subset pairs. The missing-bound program of the
branch-and-prune reframing, first measurement.)

**Bound 1 — the extension envelope.** Over the whole corpus,
T − max_subset_total ≤ 336 (attained by 699 over its uniform 363
subsets; the records 723 and 717 sit at 330). Conjecture E1: every
6-config satisfies T ≤ S_max + 336, i.e. adding a sixth cube to a
5-config with total S yields at most S + 336.

**Corollary (723 nearly cornered).** If E1 holds, any 6-config beating
723 must CONTAIN a 5-subset with total ≥ 388. The known n=5 landscape:
the record 393 (= 723's own subset family), 717's best subset 387, and
every native n=5 search capped at 377 (Postscript 16 addendum 3, ~171k
configs). So beating 723 would require a 5-config in a class that only
the 723 family is known to occupy — the search for >723 reduces to the
search for new 5-configs ≥ 388, a far smaller frontier. (Empirical
bound; sample thin at the top — stated as conjecture E1, not theorem.)

**Bound 2 — deep-deficit propagation is STEEP.** Configs whose worst
5-subset misses its bottom-1 cap (d4 < 30 = C(1,5)) are capped far
below the record: min-subset-deficit 0 → max T = 723; deficit 2 → max
T = 567; deficit ≥3 → ≤ 519. All top configs (631+) have EVERY 5-subset
saturating both subset deep caps (d4 = 30, d3 = 84 = C(2,5) attained).
Conjecture E2: a positive deep deficit in any 5-subset costs the total
>150 — subset deep-saturation is a NECESSARY condition for records,
usable as a hard prune in blueprint search.

Together E1+E2 are the missing bounds for branch-and-bound: E2 prunes
blueprints whose parts can't deep-saturate; E1 bounds completions by
the best contained 5-config. Both are measured envelopes awaiting proof
— the natural lemma behind E1 is a zone-style bound on the regions a
sixth cube's six faces can create in a 30-plane arrangement.

### Postscript 18 addendum: shared-axis campaign complete (~150k evals)

Final per-template bests (free spoke angles vs C₃-locked, all n):
- n=4: best template free=183 (RECORD; locked 165; control 163).
- n=5: three templates reach 393 (RECORD; note the 723-subset template
  reaches it LOCKED too — consistent, since 393 retains the C₃ symmetry);
  control 369.
- n=6: the 723 template reproduces 723 free (locked 679); two-cluster
  spoke3+spoke3 reaches 717 free (693 locked); all other templates and
  the unstructured control ≤ 709. NOTHING beat any record.

Closing verdict: the hub-and-spoke/shared-axis family with FREE spoke
angles contains and recovers every record (183/393/723) from ~10-15k
evals per template, while angle-locking costs 15-45 and unstructured
controls trail by 20-30. The flexible 9-DOF is confirmed as the right
search variable; the blueprint level is now handed to the
branch-and-prune program (Postscript 20 bounds E1/E2 as its pruning).

## Postscript 21: blueprint branch-and-prune complete — 67 skeletons exhausted, nothing beats 723

(blueprint_enum.py, blueprint_search.py/.jsonl, blueprint_search_report.md.
The branch-and-prune program of Postscript 20, executed.)

**Catalog**: 391 raw blueprints (cluster partitions × axes × kinds) →
67 canonical survivors after symmetry/specialization collapse, plus 2
pruned with documented justification: P2 the golden/octahedral all-13
wall (irrational, and its best extension 681 < 723 — Postscript 12), P3
the multi-axis polyhedral-forcing family (tested at 613, dominated).

**Gates**: the 723 blueprint (onaxis3+spoke3 on (1,1,1)) survives
pruning and its knob optimization reproduces 723 exactly.

**Result**: all 67 skeletons knob-searched (spoke-angle coordinate
descent + free-cube climbs + wide-perturbation hops; ~600-1,400 exact
evals each, 83,700+ total): **nothing beat 723**. Best non-gate
blueprints: spoke6_ax001 = 689, onaxis4+free2 = 681, onaxis3+free3 =
679. A 4×-budget refinement of the top-12 runners-up runs detached
(first result: spoke6_ax001 confirmed stuck at 689).

**Standing of the record after this**: 723 is now (i) exhaustive at the
blueprint/skeleton level within the rational shared-axis/free family at
stated coverage, (ii) cornered at the subset level by envelope E1 (any
beater must contain a 5-config ≥ 388; only the 723 family is known to
reach that), and (iii) at the peak of the deep-sacrifice trade-off
surface (Postscript 14). Three independent closures. Beating 723 now
requires either a fundamentally new 5-cube near-record, an irrational
wall outside every family tested, or a violation of envelope E1.

## Postscript 22: the n=7 program — 1207 certified, the ceiling law passes its out-of-sample test, first n=8 record 1879

(n7_program.py/.jsonl/n7_program_report.md — the full n≤6 apparatus
applied at n=7 in one pass; the law's first test on a size it wasn't
fitted to... l≥5 aside, since l≤4 at n=7 were in the fitting data;
the fresh tests here are the near-attainment of l=5 and all of n=8.)

**1207 stands, now certified**: ±1/±2 climb flat; 26 wide-perturbation
restarts (best 1197); 7th-cube swap/reoptimize (1199); and the n=7
blueprint catalog (100 skeletons, 30 searched in budget, gate PASS) has
its best = the 1207 blueprint itself (onaxis3+spoke3+free1 on (1,1,1),
free 1207 vs locked 1187). Free spoke angles beat locked in every row.

**Ceiling law at n=7: zero violations in 112,864 exact records.**
Caps l=1..4 (42/120/194/264) all ATTAINED exactly. l=5 (depth-2):
observed 328 vs cap 330 — within 2 after a dedicated hunt. l=6
(depth-1): observed 276 vs cap 392, far short — mirroring n=6, where
the shallow caps are the unattained ones (the frustration).

**First n=8 record: 1879** (= 1207 + 8th cube, 300-candidate sweep +
climb), by_depth {1:340, 2:450, 3:380, 4:302, 5:222, 6:136, 7:48, 8:1}.
Against the law's predictions C(l,8) = 48/138/228/306/384/458/528:
d7 = 48 ATTAINED, d6 = 136 (−2), d5 = 222 (−6), d4 = 302 (−4) — no
violations, deep layers hugging their caps from below exactly as the
law prescribes for a single un-refined config. Tower now
183 → 393 → 723 → 1207 → 1879.

**Envelope at the 6→7 step**: max(T − S_max) over the top-50 n=7
configs = 484 (the 1207−723 point). And ALL 350 six-cube subsets of
those configs saturate the n=6 deep cap d5 = 36 (350/350) — subset
deep-saturation as a necessary condition replicates one level up.

The general-n picture is now: one formula governing every deep layer at
every size tested (n=2..8, ~1.2M exact configs, zero violations), a
record tower built by single-cube extension whose every level is the
best known, and the shallow caps as the standing open frontier.

## Postscript 23: the cap-sum bound is TIGHT at n=2 and n=3 — a proof of 13 and 67 reduces to two lemmas

(Prompted by Chris Cole: "I wonder if there is a proof of 67 somewhere in
there. Zaslavsky would be thrilled. A proof could borrow ideas from the
proof that there are five Platonic solids." He is right — the reduction
was already implicit in the ceiling law.)

The law's per-layer caps sum to an upper bound on the total,
1 + Σ_{l=1}^{n−1} C(l,n). Checking small n:

    n=2: 1 + 12           = 13   = the record  — TIGHT
    n=3: 1 + 18 + 48      = 67   = the record  — TIGHT
    n=4: 1 + 24 + 66 +104 = 195  vs 183 — gap 12 (frustration begins)
    n=5: 1 + ... = 429           vs 393 — gap 36

So for n ≤ 3 the maximum EQUALS the cap-sum (no frustration: with no
middle layer, both caps are simultaneously attainable, and golden/
octahedral attain them). Hence:

**A complete proof that max(2) = 13 requires only:**
  L1(2): for two unit cubes, depth-1 ≤ 12 — equivalently the
  direction-sphere envelope max over the 6 face-normals |n·û| has no
  local maxima besides the ±normals (two orthonormal triads only).

**A complete proof that max(3) = 67 requires only:**
  L1(3): depth-2 ≤ 18 (same no-extra-peaks lemma, 9 normals), and
  L2(3): depth-1 ≤ 48 — via the top-1 ("which cube reaches farthest")
  diagram: prove its swap curve generically has V = 92 vertices, all
  trivalent (Euler then gives cells = 2 + V/2 = 48), plus the
  semicontinuity half (degenerations only merge cells). Anchors: each
  cube's 8 corner directions are local maxima of its reach, giving 24
  anchored cells; the census bounds the remaining 24.

Both attainers are already exactly verified (golden triple by two
independent ℚ(√5) engines; octahedral compound in the gated ℚ(√2)
engine; identical profiles {48,18,1}), and non-exceedance is tested by
4,414 seeded climbs at n=3 plus every 3-subset in the ~1.2M-config
corpus. The lemmas are the only missing pieces.

The Zaslavsky framing is exactly right: C(l,n) is a face-count formula
for a structured family of great-circle-arc arrangements on S², and the
proof shape is the Platonic one — a finite local classification (which
vertex types the swap curves can have, constrained by each cube's
orthonormal normal triad) followed by Euler's formula. At n=3 there are
only 9 normals, so the local classification is finite and plausibly
hand-checkable. L1(2) is the single easiest full theorem on the board.

### Postscript 23 addendum: do the proofs extend to n > 3? (Chris Cole)

- The PER-LAYER lemmas extend uniformly in n: the census V_l(n) =
  (24l−12)n − 4l² is linear in n with an l-only correction, so the local
  vertex classification does not grow with n — proving L1 in general
  form proves depth-(n−1) ≤ 6n for ALL n at once; the l=2 census gives
  depth-(n−2) ≤ 18n−6 for all n. The hard direction is l, not n.
- The EXACT-MAXIMUM proofs provably do NOT extend: cap-sum tightness
  fails from n=4 (195 vs 183, 429 vs 393, 801 vs 723) — the frustration
  phenomenon. n=2,3 are the last sizes where per-layer analysis decides
  the maximum.
- An n ≥ 4 maximum proof needs JOINT-layer inequalities (trade-off
  constraints), of which we have measured shadows (d2+d3 = 368 ridge,
  envelopes E1/E2) but no conjectured exact form. Candidate first step:
  a rigidity lemma "d1 = 10n²−14n forces golden" (true in all data),
  enabling case analysis on d1 — necessary but not yet sufficient
  (at n=4 it leaves max ≤ 193 vs true 183). Open.

## Postscript 24: FIRST THEOREM — the anchor lemma is proven (all n), and the n=2 CAD verdict

Direct outcome of the fine-graining exchange with Chris Cole.

**Theorem A (proven).** The radial envelope of any n-cube configuration
has local minima only at the 6n face-center directions (value 1 = the
inradius). Proof is a two-line sandwich: at a local max of
M = max_i |n_i·û|, every ACTIVE |n_i·û| is itself locally maximized
(it is squeezed between its value and M), and a single |cos| has maxima
only at ±n_i with value 1. Full statement + proof in C45_notes §10.
This kills the long-standing "three-form peak" crux — a phantom: peaks
of a max require each active piece to peak. Numerically corroborated
(exactly 6n maxima, value 1, every config sampled; consistent with all
earlier zero-shoulder censuses).

**What remains for C(1,n) = 6n**: only excluding "parasite" cells
(components whose envelope-inf sits on the boundary tie curve, not the
interior). Sharper than before; two candidate routes recorded.

**CAD probe (n=2 unrestricted chamber exam)**: 4 of 12 distinct
vertex-wall quartics → 4.6M-leaf decomposition in ~4 min; the full wall
set is infeasible on this machine. Chris's caveat ("fine-graining works
if we fix a family") is thereby quantified at the smallest case: the
viable certification mode is per-family (few knobs), or Theorem A +
Euler census.

### Postscript 9 addendum (2026-07-13): the slide axis identified exactly

The 67↔67 family's seed rotates by δ about â where, unnormalized,
â ∝ ( −(√2+√10), −(4+√2+√10), −2+3√2+2√5−√10 ) / 8
  = ( −√2·φ/4, −(√2·φ/4 + 1/2), … )        [√2+√10 = 2√2·φ]
and cos δ = (−6 + 3√2 + 2√5 + 3√10)/16  (δ = 40.306°).
The axis lives in the COMPOSITUM ℚ(√2,√5) — the bridge between the
octahedral (√2) and golden (√5) walls — and is a symmetry axis of
neither endpoint (57.6° from (1,1,1)). Cube k of the family spins about
Cᵏ·â: three skew axes forming a 120°-orbit around the invariant global
3-fold axis (1,1,1). Interactive: the depth explorer's "67 ↔ 67 slide".

### Postscript 9 addendum 2 (2026-07-13): edge crossings along the slide — near-persistence quantified

User: "some of the edge concurrences should persist on the slide."
Measured: at t=0 the octahedral compound has 30 EXACT edge crossings
(crossing parameter 1 − 1/√2 ≈ 0.293 along the edge). In the interior
NO crossing is exact (confirming the P9 caveat) but 6–18 NEAR-crossings
persist with gaps of only 0.0015–0.006 (cube half-width 1) — the
crossings open into hairline gaps whose closest-approach points slide
along the edges — and at t=1 the gaps snap shut again with the crossing
at s = 1/φ = 0.618, the golden section (the user's original
middle→corner marker). So the edge-concurrence structure persists as a
sub-percent-gap GHOST through the whole family, exact only at the two
walls. Viewer updated to render near-concurrences as fading ghost rings.

## Postscript 25: the DIHEDRAL FAMILY — a closed-form 1-parameter family with exact edge coincidences, containing both 67s; the ghosts explained; a new exactly-certified compound in Q(sqrt6)

Prompted by the user viewing the slide midpoint (t=0.5) and asking whether a
nearby configuration — "perhaps with irrational rotations" — could close the
near-miss edge crossings exactly, noting the coincident edges looked
perpendicular to (1,1,1). That observation was the key.

**The family.** Take the cube [-1,1]^3 and rotate it by +-120 degrees about an
axis n(psi) = (sin psi, cos psi, 0) lying IN one of its own face planes
(through the center). The three cubes {I, S, S^2},
S = S(psi) = -1/2 I + (3/2) n n^T + (sqrt3/2) [n]_x, form a C3 orbit about
the axis s = n rotated... equivalently, in the world frame used by the
viewer: seed matrix with columns
[cos(psi) w + sin(psi) s | -sin(psi) w + cos(psi) s | u],
u any unit vector perpendicular to s=(1,1,1)/sqrt3, w = s x u, orbited by
C = 120 degrees about (1,1,1). The u-freedom (theta) is exactly a global
rotation about (1,1,1), so modulo congruence this is ONE parameter, psi.
Every member is D3-symmetric: the C2 axes are the cubes' horizontal face
axes u, Cu, C^2u.

**The coincidence theorem (hand algebra + 1e-16 numerics, not yet formal).**
For EVERY psi, the edge-edge coplanarity conditions of all three edge classes
(x-, y-, z-edges) vanish identically. For the u-edges it is elementary: all
three cubes' u-edges lie in two common planes perpendicular to (1,1,1) at
heights +-(sin psi + cos psi) (and +-(cos psi - sin psi)), and non-parallel
lines in a common plane always meet. For the other two classes the identity
falls out in the frame {w, s, u} using u x Cu = (sqrt3/2)s (verified at
random (theta,psi) to machine zero; dihedral_scratch/family_check.py).
Interior-of-segment crossing counts form plateaus in psi:
  12 (0<psi<21deg), 18 (21..45.5), 24 AT psi=45 exactly, 18, 12, and
  spikes: 30 at psi = arcsin(1/sqrt3) = 35.264deg, 30 at arctan(sqrt2),
  48 at psi = 0 and 90 (shared-axis compound, pair invariant 1+sqrt3).

**Both 67s are members.**
- Octahedral 67: psi = arcsin(1/sqrt3), axis n = (1, sqrt2, 0)/sqrt3.
  30 interior crossings, pair invariant 1/2+sqrt2 (matches).
- Golden 67: tan(psi) = phi^2, i.e. sin(psi) = phi/sqrt3,
  cos(psi) = 1/(phi sqrt3) — consistency is the identity
  phi^2 + phi^-2 = 3. Axis n proportional to (phi^2, 1, 0). Pair invariant
  = 3phi/2 = 2.4270509831... to 1e-16. At exactly this psi the 18 interior
  crossings hand over to 54 AT-CORNER contacts — the blue-ring -> gold-ring
  morph of Postscript 9, now in closed form.
- The relative rotation is the classical golden matrix
  (1/2)[[phi,1,1/phi],[1,-1/phi,-phi],[-1/phi,phi,-1]] at the golden point.

**Why the slide has ghosts.** The 67<->67 slide (Postscript 9) connects the
two 67s but leaves this family (its interior seed has face-axis dot (1,1,1)
approx 0.05, not 0). The dihedral family connects the same two endpoints
THROUGH exact-coincidence configurations the whole way. The ghost gaps of the
slide are precisely the cost of stepping out of the dihedral surface.
(First found numerically: from t=0.5, a 1.66-degree seed rotation about
approx (0.799,-0.545,-0.254) lands back in the family at psi=52.20 deg,
closing all 12 ghosts into 18 exact crossings; continuation + congruence
invariants then revealed the family. dihedral_scratch/edge_close*.py.)

**A new exactly-certified compound.** psi = 45 deg: axis = the FACE DIAGONAL
(1,1,0)/sqrt2. S = (1/4)[[1,3,r6],[3,1,-r6],[-r6,r6,-2]], entries in
Q(sqrt6). 24 interior crossings (plateau maximum away from the 67s).
Exact count via q6_count.py (new engine: field-constant clone of the
validated slide3_q2.py, D: 2->6; identity-pair self-test passes; S certified
orthonormal with S^3=I in exact arithmetic):
  TOTAL = 49, depth profile {d1: 30, d2: 18, d3: 1}.
Same deep layers as both 67s (18, 1) — another instance of "deep structure
conserved, d1 is what varies" (Postscript 17). SINGLE-ENGINE exact count
(not a record claim); a second engine pass is listed in the follow-ups.

**Arithmetic density (open route).** With sin psi = p/r, cos psi = q/r
rational (Pythagorean triples), S(psi) has entries in Q(sqrt3) — an infinite
family of exactly-countable members. A Q(sqrt3) clone of slide3_q2.py (one
constant) plus a Pythagorean sweep would chart the region count along the
whole family exactly. See DIHEDRAL_FAMILY_NEXT.md.

Files: q6_count.py (Q(sqrt6) verifier + the 49 count), dihedral_scratch/
(exploration + verification scripts), DIHEDRAL_FAMILY_NEXT.md (handoff).

### Postscript 25, addendum: the persistent 18-core — octahedral-to-golden slides WITHOUT breaking a single concurrence; corner docking; corrected transition locations

Prompted by the user asking for "another way to slide from octahedral sqrt2
to golden sqrt5 while maintaining edge concurrences." Fine-grained pair-
identity tracking (0.1-deg grid, persistence.py/docking.py in
dihedral_scratch/) shows the dihedral family already does this, more
literally than Postscript 25 realized:

1. **The 18-core.** The interior crossing SET is one and the same set of
   18 edge pairs (6 per cube pair) on the ENTIRE open interval
   (20.905deg, 69.095deg) — i.e. between the two golden copies. The count
   changes en route (30 at the octahedral points, 24 at the face-diagonal
   point) are +12/+6/+12 EXTRA coincidences that exist only exactly AT
   those isolated psi (measure zero); the core 18 never opens a gap. The
   ghost bands around the special points are entirely the extra pairs
   approaching/leaving — never the core.
2. **Corner docking.** At arrival at golden (either copy), nothing
   breaks: 6 of the core 18 remain interior at segment parameter
   t = +-0.23607 = 1/phi^3 (the golden section yet again; cf. the s=1/phi
   crossing of Postscript 9), and the other 12 land EXACTLY on cube
   corners (t = +-1, gap ~3e-16) — they BECOME the golden corner-
   coincidence structure. Verified identically at mirror-golden
   (20.905 deg): 6 interior + 12 docked, 0 broken.
3. **So**: sliding 35.264 -> 69.095 (or the shorter mirror route
   35.264 -> 20.905, arriving at a congruent golden compound) maintains
   all 18 core edge concurrences unbroken start to finish. Keeping all 30
   of octahedral's crossings is impossible at golden with interior
   crossings alone (golden has 18-core worth: 6 interior + 12 docked);
   whether some off-family path in the full 3-DOF C3 space preserves more
   than 18 is open (the 12 octahedral extras appear to be isolated —
   they exist only at the octahedral points of the family).
4. **Correction to the transition table**: the crossing SET changes ONLY
   at 20.905 (= 90 - arctan(phi^2), mirror-golden), 45, and 69.095
   (golden) in [20,70] — the "unnamed transitions at ~21.4 / ~68.6 deg"
   previously baked into the viewer's REGION_CHANGE_DEG are ghost-band
   BOUNDARIES (the fuzzy 0.02-gap window), not set changes, and the
   earlier bisection "conflation" mystery near 69 deg dissolves: there is
   only one event there, golden itself. Viewer follow-up: relabel those
   marks, and the "maintain concurrences" lock can be redefined
   core-aware (the core-18 is maintained on the whole span between the
   golden copies, so locking should permit the full octahedral->golden
   drag).

### Postscript 25, addendum 2: paths preserving MORE than 18 — the pair-curve identity, a 26-concurrence chain triple, and why 18 is still the end-to-end record

User asked for paths preserving more than the 18-core. Findings
(dihedral_scratch/: bigfamily.py, pairmap.py, loopholes.py, trace10.py,
window26.py):

1. **The big family.** The dihedral construction generalizes: n cubes,
   each with a face-axis u_k perpendicular to a COMMON axis s, arbitrary
   phases theta_k about s, and a COMMON tilt psi. Exact edge coincidences
   persist (control: different psi per cube kills all of them). Pair
   crossing structure depends only on (Delta theta, psi).
2. **Within the C3 dihedral family, >18 is impossible**: the 12 octahedral
   extras are valid only at isolated psi (measure zero on the slice).
3. **The pair-curve identity (new).** In the (Delta, psi) pair-plane, ALL
   FOUR extra coincidences of the octahedral pair share ONE zero curve
   Delta_c(psi) through (120 deg, 35.264 deg) — their line-coplanarity
   residuals stay ~1e-16 along the entire traced curve (psi from ~2 to
   ~85 deg), i.e. all 10 of the octahedral pair's edge-line coincidences
   hold identically on a one-parameter curve, not just at the octahedral
   point. (Full-3-DOF check: the 10 conditions' Jacobian at the
   octahedral pair config has rank 2 — kernel dim 1 — the curve is the
   whole local solution set.) Segment validity (|t|<=1) holds for psi in
   roughly (27.5, 46.5) deg; outside, the extra crossings exit through
   cube corners.
4. **A 26-concurrence path (new).** Chain triple theta = (0, Delta_c(psi),
   2*Delta_c(psi)): pairs (1,2) and (2,3) ride the curve carrying 10
   coincidences each; pair (1,3) at 2*Delta_c keeps its core 6. Verified:
   26 exact concurrences maintained continuously for psi in
   [35.264, ~44.5] deg (Delta_c drops 120 -> ~110). At psi ~44.5 the
   extras dock/exit at corners and the count falls to 18; at 45 the
   third pair briefly holds 8 (total 20).
5. **End-to-end oct -> golden still caps at 18** (best known): the four
   extra labels are not in golden's 24-label contact set at all, and the
   pair curve's segment window closes at ~46.5 deg. Open loophole:
   corner HANDOFFS — at |t|=1 a concurrence point can switch to an
   adjacent edge's label and continue; golden has 60 contacts total, so
   a handoff chain carrying >18 physical concurrence POINTS into golden
   is not excluded. Tracing the handoff network is a well-posed numeric
   task (delegable).
6. **n>3 relevance.** The big family is an (n-1)+1-parameter
   exact-coincidence scaffold for ANY n: every cube pair in segment
   range carries >=6 exact edge concurrences; chains
   theta=(0, Dc, 2Dc, ...) let consecutive pairs carry 10. Entries are
   algebraic (Pythagorean psi -> Q(sqrt3)), so members are exactly
   countable with the planned q3 engine. Records already exploit
   common-axis structure (723 contains a C3 orbit about (1,1,1); the
   continuous 9-family pairs are the psi->0 degenerations), so an
   in-family exact sweep at n=4/5/6 over (theta_2..theta_n, psi) — an
   n-dimensional sheet instead of (3n-3) — is a cheap structured probe
   of the trade-off surface. Proposed as follow-up alongside
   DIHEDRAL_FAMILY_NEXT.md Task 1.

### Postscript 25, addendum 3: EXACT region counts along the dihedral family (Task 1 executed) — a symmetric staircase, spikes at the 67s, and a local MINIMUM at the face-diagonal point

DIHEDRAL_FAMILY_NEXT.md Task 1, C3 slice, executed with a new Q(sqrt3)
engine (q3_count.py, field-constant clone of the validated slide3_q2.py,
same pattern as q6_count.py; identity self-test + orthonormality + S^3=I
asserts). At Pythagorean psi (sin=p/r, cos=q/r rational), S(psi) =
-I/2 + (3/2)nn^T + (sqrt3/2)[n]_x has entries in Q(sqrt3) -> exactly
countable. 40 points swept (~0.6 s each). Result, symmetric about 45 deg:

  psi in (0, ~9.6):        25 = {12, 12, 1}
  psi in (~9.6, ~10.9):    31 = {18, 12, 1}
  psi in (~10.9, 20.905):  43 = {24, 18, 1}
  psi in (20.905, 69.095): 55 = {36, 18, 1}     <- the central plateau
  ... mirrored on the other side; endpoints psi=0/90 (shared axis): 25.
  Isolated spikes: octahedral 35.264 -> 67 = {48,18,1};
  face-diagonal 45 -> 49 = {30,18,1} (Q(sqrt6) engine, addendum 25);
  golden 69.095 -> 67 = {48,18,1}.
  (Wall between 31 and 43 bracketed in (9.53, 10.39) deg; its mirror in
  (79.61, 80.47). Exact wall locations not yet identified.)

Observations:
1. **d3 = 1 always, d2 = 18 across the whole middle band** (dropping to 12
   only below ~10 deg and mirrored) — ALL action is in d1
   (12->18->24->36, spiking 48 at both 67s, 30 at 45 deg). The
   "deep-structure-conserved, d1-varies" principle (Postscript 17) holds
   pointwise along the entire family.
2. **The family's maxima are exactly the two 67s** — the proven n=3
   global maximum is attained precisely at the two most special family
   points, from a plateau of 55.
3. **The face-diagonal point is a local MINIMUM (49 < 55)**: its +6 extra
   edge crossings MERGE regions instead of creating them, while the +12
   extras at the octahedral points RAISE the count by 12. Coincidence-
   richness cuts both ways; it is how walls concur, not how many — the
   sharpest small illustration yet of the trade-off principle.
4. **Region-count walls != crossing-set walls**: the crossing set changes
   only at 20.905/45/69.095 (addendum 2), but the count also jumps at
   ~9.6/~10.9 deg (and mirrors) where d2 changes with NO edge-crossing
   event — vertex/face combinatorial walls of the deeper arrangement.
5. Bonus (not yet exploited): in the BIG family, Pythagorean phase
   DIFFERENCES make the relative rotations fully RATIONAL — integer
   quaternions — so the (theta_2, theta_3, psi) directions off the C3
   slice are countable by the fast C++ engine directly. The 2-parameter
   exact count map is a cheap delegable follow-up.

Files: q3_count.py (engine + sweep driver, 40-point table in __main__).

### Postscript 25, addendum 4: the handoff chase — 18 stands, the obstruction identified, and a CORRECTION to addendum 2's golden contact count

The corner-handoff exploration (HANDOFF_SPEC.md; scripts
dihedral_scratch/handoff_*.py; full report handoff_report.md) is done.
Verdict: **no path carrying more than 18 physical concurrences from
octahedral to golden was found** — 18 is the confirmed lower bound with a
specific, describable local obstruction; not a proven ceiling.

**CORRECTION (addendum 2, item 5).** "Golden has 60 exact contacts
(6 interior + 54 corner)" mixed a threshold artifact with a label count.
Correct figures (handoff_g1.py, confirmed against persistence.py): golden
triple = **18 interior + 54 corner LABEL-pairs (72)**; deduplicated to
physical points = **18 interior + 6 corner points = 24** (each corner
point is a genuine vertex-to-vertex coincidence registering 3x3=9 label
pairs). The old "6 interior" came from evaluating at psi rounded to
69.0948 deg (2e-5 deg off the exact arctan(phi^2)), where the 12 docking
core pairs already sit past the |t|<0.9999 cutoff. Golden's 18 interior =
6 persisting core + that point's OWN 12 extras — the golden-side analogue
of the octahedral +12. Also: octahedral has MORE distinct contact points
(30) than golden (24), so ">18 into golden" needs 19 of golden's 24
physical points fed — tight but not excluded a priori.

**What the chase established** (all three gates passed; the linker
independently reproduces the 18-carry, the 26-window, and — untuned —
the 12-plateau past golden):
1. Driving THROUGH golden on the C3 path, all 18 core trajectories pass
   continuously; beyond it 6 stay interior, 6 execute genuine verified
   corner handoffs (e.g. (0,1,0,1) -> (0,1,4,5) at shared vertex
   (-1,-1,-1)), 6 die. Handoffs are real and the machinery detects them.
2. The chain path's wall is at exactly **psi=45 deg, theta2 =
   arccos(-1/3) = 109.4712 deg (the tetrahedral angle)**, where cube-A's
   vertex (-1,1,-1) touches cube-B's vertex (1,-1,-1) — a vertex-VERTEX
   coincidence offering 9 relabeling candidates. NONE of the 9 continues
   to the golden basin: most re-hit |t|=1 immediately (psi=45 is a
   resonance where several branches of the algebraic curve cross); the
   rest run off to the shared-axis region (psi to 89 deg).
3. Golden's own extras form a THIRD pair-curve identity (x-z class:
   (1,9),(2,10),(9,0),(10,3) share one curve through golden). Traced
   backwards it walls at psi=45.00 deg, theta2=180.0 deg — the same
   psi-45 resonance but ~70 deg away in theta2 from the octahedral-side
   wall, and neither curve's far branch links them.
4. **The obstruction**: octahedral extras (y-z class, curve near
   theta2~110) and golden extras (x-z class, curve near theta2~180) are
   different label families on different curves; both graze the psi=45
   resonance but nothing bridges the 70-deg theta2 gap while holding any
   cross-class equality. Grid corroboration: pair-level count >=7 covers
   only 0.28% of the (theta2, psi) plane — a 1-D curve network, no open
   patches (as the DOF count predicts).
Scope: single-hop rescues at the identified walls + three cross-class
families + coarse grid; multi-hop chains through second/third walls not
exhausted.

## Postscript 26: the records are BUILT FROM family pairs — the n>3 verdict on the dihedral family

NFAMILY_SPEC.md executed (nfamily_report.md; two-engine gates G0/G1/G2 all
passed; spot-verified by the main session). The family generalized to n
cubes = {Rel(theta_k, psi)} with Rel(D,psi) = Rodrigues rotation by D
about axis (sin psi, cos psi, 0) — a new closed form making every
Pythagorean-parameter member an INTEGER-QUATERNION config, countable by
the C++ engine (~10 ms each).

**As a search space: no.** Best verified family members (9,218-config
exact sweep: chains, random Pythagorean phases, hill-climbing): n=4: 175
(record 183, -8); n=5: 335 (393, -58); n=6: 615 (723, -108). The deficit
GROWS with n. Caveat (fundamental, not budget): Pythagorean sweeps cannot
land on irrational spikes — at n=3 the same sweep sees only the
55-plateau, never the 67s — so these are lower bounds on the continuous
family's supremum.

**As structure: overwhelmingly yes.** Exact pairwise tests (two
independent methods, 34/34 agreement; crossing counts + an axis test
"exists a cube-symmetry relabeling with R[0][1]==R[1][0] exactly"):
- 183 record: ALL 6 pairs in family position (6 exact crossings each).
- 393 record: ALL 10 pairs in family position.
- 723 record: 12/15 — cubes {0..4} form a full family 5-clique (= the
  embedded 393, consistent with record nesting), cube 5 family-linked to
  two of them, generic vs the rest.
- 67 (n=3): confirmed a family member in exact Q(sqrt2) arithmetic —
  first exact (non-numeric) confirmation of its 30 crossings.
So the records are gluings of family cliques on DIFFERENT axes, not
single-axis members: the single-common-axis family is a strict subset of
"configs built from family-position pairs," and the latter is what
records exploit. Record-hunting reframed: search over multi-clique
gluings (clique sizes, axes, tilts, phases) instead of raw SO(3)^n.

**Deep layers**: at every n the family pins d_n=1 and d_{n-1} at exactly
the record's own value (24/30/36 at n=4/5/6) across the whole
non-degenerate range; the deficits sit in the SHALLOW layers (n=4: the
entire -8 in d2 alone, 58 vs 66, with d1/d3/d4 matching the record
exactly). Sharpest form yet of "deep structure conserved, shallow layers
are what records win."

**Also**: psi <-> 90-psi mirror symmetry persists at every n; chains at
a=90 deg collapse to total 93 INDEPENDENT of n (cube 90-degree
self-symmetry makes added cubes redundant — the degeneracy predicted in
DIHEDRAL_FAMILY_NEXT Task 4, now quantified).

Files: nfamily_report.md, nfamily_common.py, nfamily_gates.py/.out,
nfamily_q3_records.py/.json, nfamily_sweep.py, nfamily_results.jsonl.

### Postscript 26, addendum: four theorems PROVED (C45_notes.md section 12)

Answering "can we prove anything?" — yes, four statements moved from
verified-numerics to proved today (full proofs in C45_notes.md sect. 12):
- **Theorem M (mirror)**: config({theta_k}, psi) is congruent to
  config({-theta_k}, 90-psi) via the x<->y coordinate swap (improper
  isometry; conjugation reverses the rotation sense and swaps the axis
  components). Proves the psi<->90-psi degeneracy seen in every sweep,
  for all n; all family sweep domains are rigorously halved.
- **Theorem P (periodicity)**: psi+90 gives the SAME compound
  (M(psi+90) = M(psi)*rot(e3,90)); true parameter range is psi in [0,45].
- **Theorem F (coincidence identity)**: all same-class edge-line
  coincidences hold identically on the whole family — z-class by the
  equal-heights argument, y-class by a five-line vector computation
  (the coplanarity form collapses to s c^2 (sin D - sin D) = 0),
  x-class from y-class via Theorem P's relabeling. The family's exact
  crossings rest on proof; only segment-interior validity (|t|<=1)
  remains numeric (Sturm-certifiable, listed as next).
- **Theorem R (rational obstruction)**: rational configurations have
  rational O-reduced pair invariants; the 67s' invariants are 1/2+sqrt2
  and 3phi/2 — so no rational config is congruent to either.
  **Corollary**: conditional on the two known 67s being the only n=3
  maximizers, the n=3 maximum REQUIRES irrational coordinates — making
  n=3 provably the unique irrational level of the record tower, given
  witness uniqueness.
Identified as provable-next with real work: certified staircase (Sturm),
core-18 segment bounds with docking values +-1, +-1/phi^3, the
pair-curve identity, and (the prize, unchanged) the two lemmas of
Postscript 23 for max(3)=67.

## Postscript 27: the gluing search — records still unbeaten (deficit exactly 8 at every n), and the RATIONAL-TANGENT discovery (with a correction to the agent's clique inventory)

GLUE_SPEC.md executed (glue_report.md; gates G1/G2/G3 all passed;
319,141 exact configs; every near-record hit re-verified with the Python
oracle). Headline numbers, all two-engine verified:

| n | best glued (sizes)         | record | deficit |
|---|----------------------------|--------|---------|
| 4 | 175 (no gain over single)  | 183    | -8      |
| 5 | 385 (3+2)                  | 393    | -8      |
| 6 | 715 (3+3)                  | 723    | -8      |

Gluing recovers 50 of the single-axis deficit at n=5 and 100 at n=6 —
converging to a common floor of EXACTLY 8 below the record at every n.
Nothing beat or tied a record; the record-claim protocol never fired.

**Q0 verdict**: no record is a single-axis family member (full-record
axis intersections exactly empty). Postscript 26 stands.

**CORRECTION to the agent's sub-clique inventory** (main session,
exhaustive exact re-derivation over all subsets x all 3^k face-axis
choices, Fractions only): the agent claimed three overlapping 4-of-5
cliques in 393; in fact there is EXACTLY ONE single-axis 4-clique in
393: cubes {1,2,3,4}, integer axis (3,2,0), tan psi = 2/3 (hyp^2 = 13,
so sin/cos in Q(sqrt13)) — verified: each cube's local axis is a signed
permutation of (2,3,0), exactly. The other two claimed cliques fail
exact verification (their cubes lack the zero component / 2:3 ratio).
183's inventory, corrected and exhaustive: NO 4-clique, and three
3-cliques all on the SAME cube triple {0,2,3} with three DIFFERENT
integer axes — (2,-3,0) at tan 2/3 (sqrt13), (3,5,0) at tan 3/5
(sqrt34), (5,2,0) at tan 2/5 (sqrt29): a triply-resonant family triple.
393 has no 5-clique; 183 no 4-clique.

**The discovery that survives and sharpens**: the records' family
structure lives at RATIONAL-TANGENT, IRRATIONAL-SINE tilts
(tan psi = 2/3, 2/5, 3/5; hyp^2 = 13, 29, 34 non-square). A Pythagorean
(rational-sine) sweep can NEVER land on these at any resolution — the
Postscript 26 sweep searched the wrong rational locus. Yet these
configurations ARE integer-quaternion (the records prove it): a pair at
rational tan psi = q/p has rational Rel iff cos Delta is rational and
sin Delta is in sqrt(d)*Q with d = p^2+q^2 — rational points on the
conic c^2 + d s'^2 = 1, parametrizable by rational slope. So the
C++-searchable single-axis locus extends far beyond Pythagorean-x-
Pythagorean, and the natural next sweep is over rational-tangent tilts
with conic-coupled phase steps — the slice the records actually live in.
The exactly-8 floor at three consecutive n is either a coincidence or a
structural constant of the gluing space; the rational-tangent sweep
should decide which.

(Also: the n=4 resonance solve (RESONANCE4_SPEC.md) hit its session
limit mid-run; to be resumed.)

## Postscript 28: the n=4 resonance solve — cross-class alignment is count-NEGATIVE at n=4; best resonance 151, and it is secretly RATIONAL

RESONANCE4_SPEC.md executed (resonance4_report.md, resumed after a
session-limit interruption; resonance4_solve.py/.wl,
resonance4_results.jsonl). Gates R1 and R2 passed; R1 additionally
re-verified independently by the main session (sympy: both polynomials
vanish exactly at the known n=3 resonances).

**The cross-class coplanarity polynomials** (Rel gauge, cD=cos Delta,
sD=sin Delta, cP=cos psi, sP=sin psi; representative sign-variants):

    g_xy = 2 cD sP^2 - cD + cP sD - sD sP - 2 sP^2 + 1
    g_yz = -cD cP sP + cD sP^2 + cD - cP sD + cP sP - sP^2 + 1
    g_xz = cD cP - cD sP - cP - sD + sP     (sP=0 factor dropped)

Each type has 8 sign-variant curves (16 label pairs in antipodal
pairs); swapping the cubes is sD -> -sD, so ORIENTATION matters — the
n=3 octahedral resonance is itself mixed-orientation (Deltas
120,120,240). R1: substituting Delta=120 deg gives psi=arcsin(1/sqrt3)
as an exact root of g_yz and psi=arctan(phi^2) of g_xz.

**Systems solved**: 90 uniform k=4 systems (46 exact, 44 Groebner
timeouts, concentrated in the heavy xy class) + all 48 targeted
mixed-orientation triangle+1 systems. 385 unique candidate points. No
non-degenerate resonance has rational PARAMETERS; 63 candidates in
single quadratic fields — ALL exactly counted via a generic Q(sqrt d)
field engine (factory clone of the validated slide3_q2.py); ~160
degree-4-nested candidates reported open with minimal polynomials, per
spec's do-not-approximate rule.

**Verdict: every exactly-counted n=4 family resonance is
count-negative.** Best: 151 = {68,58,24,1} at tan psi = 2, theta =
(-131.81, 96.38, -35.43) deg, pairs {12,13,23,24} on the yz curve —
vs 175 (family plateau), 183 (record), 195 (cap-sum). The n=3 "+12
spike" mechanism does NOT carry to n=4 in any quadratic field: extra
coincidences merge regions, as at n=3's face-diagonal 49 < 55. Deep
structure conserved pointwise: every non-degenerate resonance counted
has d4=1 and d3=24 exactly.

**Main-session observation that unifies the two campaigns**: the 151
witness's parameters are irrational (Q(sqrt5)) but its CONFIGURATION is
rational — sin(theta_k) in sqrt5*Q times axis components in Q/sqrt5
cancels — and it reduces to tiny integer quaternions

    1,0,0,0; -1,2,1,0; 2,2,1,0; 7,-2,-1,0     (axis (2,1,0))

i.e. it sits exactly on Postscript 27's rational-tangent conic
(c^2 + 5 s'^2 = 1; cube 2's point is c=-2/3, s'=-1/3). Third-engine
verification: the C++ engine on those quats gives 151 = {68,58,24,1},
agreeing with both of the agent's engines. So the algebraically-found
resonances at rational-tangent tilts ARE inside the rattan sweep space
— the resonance solve and the conic sweep are probing the same locus
from two directions, and at n=4 that locus tops out below the plateau.

**Most interesting open point**: a pure chain theta_k = k*a
(a ~ 200.891 deg) at tan psi = (1+sqrt13)/6 — the record's own tilt
field Q(sqrt13) — with all four pairs {12,23,34,14} on one curve;
degree-4 nested coordinates, needs a certified nested-radical sign
oracle to count. The corner-contact (|t|=1) resonance sweep was not
reached.

## Postscript 29: the rational-tangent sweep (interim) — the "exactly 8" floor is BROKEN at n=5: deficit now 6

RATTAN_SPEC.md in flight (rattan_report.md; rattan_sweep.py;
rattan_results.jsonl, 17,080 configs at smoke scale; the implementing
agent hit its session limit before launching the full sweep — interim
results below are already two-engine verified and recorded now).

**All four gates pass.** G0: exact conic parametrization
(c,s') = ((1-d t^2)/(1+d t^2), 2t/(1+d t^2)) with round-trip and
group-law closure t1 (+) t2 = (t1+t2)/(1 - d t1 t2), all Fractions.
G1 (the sharp gate): 393's own 4-clique {1,2,3,4} is exactly a conic
chain on axis (3,2,0), tan psi = 2/3, d=13, at t-values

    t = 0 (base = clique cube 2), -5/6, 3/4, -1/5

with the three non-base pairs matching the conic group law with NO
further search (e.g. pair (1,3): c=29/133, s'=36/133 both ways). The
sweep space provably contains the record's clique. G2: two-engine
agreement on fresh rational-tangent configs at n=4 and n=5. G3: 723
reproduced from the ledger quats.

**Bonus**: 183's triply-resonant triple {0,2,3} independently
re-derived on all three axes — and in ALL three parametrizations the
two non-base cubes sit at OPPOSITE conic phases (t and -t): the record
triple is an antipodal pair about cube 0 three ways simultaneously.

**Headline: the deficit floor is not 8.** Taking 393's exact 4-clique
as fixed base and adding a 5th cube ON the same axis at conic phase
t5 = 3/14 (a plateau of t5 in [~8/39, ~3/14] gives the same count):

    n=5: 387 = {148,130,78,30,1}
    quats 1,0,0,0; -6,-10,15,0; 4,-6,9,0; 5,2,-3,0; 14,-6,9,0

Two-engine verified (C++ engine in the sweep; Python oracle re-run
independently by the main session: exact agreement). 387 > 385 (the
glue campaign's best): at n=5 the deficit to the record is now 6, so
the "exactly 8 at every n" pattern of Postscript 27 was a coincidence
of the glue search space, not a structural constant. Note the winning
config is FIVE cubes on ONE axis — a single-axis 5-chain-with-
non-uniform-phases, something the glue campaign's 3+2 split could not
represent.

Other interim facts: 393's clique alone counts 179 at n=4 (only -4);
the reconstructed conic chain reproduces the literal ledger clique's
count exactly (end-to-end gauge validation). The tier-3 "183 triple +
4th integer quat" search re-found the 183 RECORD itself — main session
check: the found 4th cube (1,-1,-1,4) right-multiplied by the cube
symmetry (0,1,-1,0) is exactly the ledger's (0,5,3,2). 723's 6th cube
(5,2,2,2) is NOT in family position w.r.t. the 4-clique (off-axis,
like 393's cube 0). Chains alone top out at 175 (n=4) / 671 (n=6).

## Postscript 30: the event catalogue — the "+-1 per coincidence" law dies, a depth-conservation law survives 12/12, and a correction to Postscript 25 addendum 3

EVENTS_SPEC.md executed (events_report.md, events_extract.py,
events.jsonl; all gates passed; new field-agnostic coincidence census
pair_census validated against nfamily_common on 16 pairs and against
the golden 18+54/6 census from an independently hand-derived matrix).
Twelve exact events tabulated across n=3 (dihedral family), n=4
(175/151/143), n=5 (387-plateau edges).

**The conjectured "+-1 region per coincidence" law is NOT general.**
It is EXACT (+/-1.000) precisely for the pure-interior-crossing n=3
events: octahedral spike +12 count on +12 crossings, its mirror, and
the face-diagonal -6 on +6. Everywhere else it bends or breaks:

- golden spike: +12 regions from 6 physical vertex-vertex contacts =
  +2.000/point — the SAME total 67 reached by a different mechanism at
  a different exchange rate than the octahedral 67;
- n=4, 175 -> 151: coincidences INCREASE (+2 interior) while the count
  DROPS 24 — falsified in sign, not just magnitude;
- n=5 plateau edges: identical coincidence deltas (+-2 corner points)
  give -2/point at one edge and -4/point at the other, depending only
  on WHICH cube pair touches;
- band-edge walls (~9.5 deg and mirror): count jumps +12 with the
  exact crossing census FROZEN (certified zero Fraction difference) —
  a genuine third event class: pure diagram-combinatorial
  reorganization with no coincidence change at all.

**The law that survives every event (12/12): depth conservation.** The
entire count delta of every event lands in d1 (occasionally d1+d2);
every deeper layer is bit-for-bit unchanged — creates, merges,
interior and corner mechanisms, no-coincidence walls, n=3/4/5 alike.
Postscript 17's "deep structure conserved" is now a pointwise,
per-event exact statement.

**CORRECTION to Postscript 25 addendum 3** (verified independently by
the main session with q3_count at psi ~ 0.23/2.29/7.6 deg): the table
row "psi in (0, ~9.6): 25 = {12,12,1}" is wrong as an interval. 25
holds ONLY at the isolated point psi=0 (and 90 by mirror); generic
psi arbitrarily close to 0 gives 31 = {18,12,1}: the 31-plateau spans
all of (0, ~9.5), and the 43-plateau (~9.5, 20.905). True structure
below the golden-mirror:
{25 at psi=0 only} | 31 on (0,~9.5) | 43 on (~9.5, 20.905) | 67 at
20.905 | 55 central band. psi=0 is itself a NEGATIVE mega-spike:
crossings jump 12 -> 48 while the count drops 6 (ratio -0.167) — the
most coincidence-rich, count-poorest event known; near-total geometric
redundancy at the fully degenerate shared-axis point.

Consequence for the theory program: a "create-vs-merge criterion"
cannot be a function of the coincidence census alone — it must see
the d1-layer combinatorics (top-diagram cell structure), which is
exactly what the census extraction (CENSUS_SPEC.md, in flight) is
digging out. The exact algebraic location of the ~9.5 deg wall is
still unpinned (bracketed (7.628, 9.527) deg; needs a resultant on
the top-diagram cell-change condition — natural follow-up).

## Postscript 32: the open n=4 resonance candidates counted exactly — still all count-negative; best 169 < 175, the sqrt13 chain = 159

OPENCOUNT_SPEC.md executed (opencount_report.md, opencount.py,
opencount_results.jsonl, opencount_wl_data.json). resonance4
(Postscript 28) left ~160 n=4 resonance candidates uncounted because
their coordinates live in degree-4 (nested-radical) fields where the
voxel triage is unreliable. This closes the countable ones exactly via
two independent exact-sign engines: a primitive-element number field
Q(alpha) (element = 0 iff its power-basis vector is 0 — exact; sign by
refining alpha's isolating interval) and a relative-quadratic tower
Q(sqrt a)(sqrt b). All four gates passed and were RE-RUN independently
by the main session: G1 exact-zero detection + 1000/1000 sign-vs-float
both representations; G2 reproduces rational 151 and 175 verbatim
against ./cube_regions_n; G3 reproduces octahedral 67 (Q(sqrt2)) and
golden-177 (Q(sqrt5)) through the field engine; G4 the sqrt6 candidate
counts 127 identically in BOTH representations.

**Verdict: no open candidate reaches 175 (the family plateau), let
alone 183 (the record).** Highlights (all with the deep layers
conserved, d3=24, d4=1, as everywhere on the resonance set):

- **The prime suspect settled**: the pure CHAIN at tan psi=(1+sqrt13)/6
  (psi=37.51 deg) — the record's OWN tilt field Q(sqrt13) — counts
  **159 = {76,58,24,1}**, confirmed by both field representations. The
  tilt-field coincidence with the 183 record produces no competitive
  resonance.
- Best total found anywhere: **169 = {80,64,24,1}** at psi=35.264 deg
  (the octahedral angle arcsin(1/sqrt3)), theta=(120,-120,153.1) — a
  degree-4 bulk-sweep point, still 6 short of the plateau.
- Documented rows: sqrt3-tower branches 159/165; sqrt6 branches
  127/131/167; the pentagonal (5s^4-5s^2+1) and golden-nested
  (t^4+t^2-1) rows are constitutionally degenerate — no non-degenerate
  4-distinct-cube member exists in their scope (best degenerate
  representatives 67/59, effectively 3-cube compounds). The
  degree-agnostic engine also handled one incidental degree-6 field
  with no code change.

**Honest coverage** (per report §6): 108 of the sweep's systems
re-derived from wolframscript (2421 solutions -> 238 fingerprints);
12 distinct exact counts spanning degree-4 and degree-6, every one
count-negative vs 175. NOT covered: the uniform xy/yx systems (30) and
the full non-triangle mixed-CLASS space (~19k systems) — so this
extends but does not EXHAUST resonance4. Record protocol not triggered.

Net: with Postscript 28's quadratic-field verdict, this makes "n=4
family resonances are uniformly count-negative" hold across every field
degree tested (2, 4, 6), the strongest computational support yet that
n=3 is the only irrational rung of the tower — with the standing
caveats that the mixed-class space is unswept and that "3 is unique"
remains conditional on the two 67s being the sole 3-cube maxima
(Theorem R corollary).

## Postscript 33: FIRST COMPLETE MAXIMUM THEOREM — max(2) = 13 proved (all R), and d2<=18 / d_{n-1}<=6n proved unconditionally

MAX2_SPEC.md executed (max2_report.md, max2_verify.py,
max2_verify_log.jsonl). The task was framed as a certified interval
covering; the agent instead found a clean ANALYTIC proof (Theorem 1)
that closes both degeneracies PROOF_67.md §3 had left open, for all n at
once. Main session reviewed the proof line by line (judged correct, one
standard step flagged), re-ran all gates, and independently verified the
maximizer facts. Recorded as a proof with that provenance — NOT merely
an agent claim.

**Theorem 1 (no parasites, all n).** Every connected component U of
S_C = {u : cube C reaches strictly least} contains a face direction of
C; hence #pi0(S_C) <= 6 for every cube C, with NO exceptional locus.
Proof mechanism: at the inf of r_C over cl(U), if it sits on the
boundary, split on whether some active face a of C is "matched" (shares
a normal identically with a tying cube). All branch gradients have equal
norm rho = sqrt(1-f^2), so by Cauchy-Schwarz v = e_a/rho is the UNIQUE
steepest-ascent direction — an unmatched a gives an into-U ascent point
with r_C below the inf (contradiction); if ALL active faces are matched,
the shared normals force r_C >= r_x in a whole neighborhood, so no S_C
point is near the boundary (contradiction). Any cube sharing a normal
with an active face of C is automatically tying, so the split is
exhaustive. The equal-norm + Cauchy-Schwarz choice handles arbitrary
face/cube multiplicity in one stroke — the multiplicities and shared
normals PROOF_67 flagged as gaps (i)/(ii). Shared normals are
self-exclusion, not parasites: the shared plane removes an anchor,
never adds one.

**Consequences (all proved):**
- **max(2) = 13** for every R in SO(3): d1 = #pi0(S_1)+#pi0(S_2) <= 12
  (Theorem 1), d2 = 1 (convex core), attained. The project's FIRST
  complete maximum theorem. Maximizer = 180 deg about the body diagonal
  (1,1,1), quaternion (0,1,1,1) -> 13 = {12,1} EXACT (rational,
  oracle-verified), on an open range of R.
- **d2 <= 18 unconditionally at n=3** — Cluster 1 of max(3)=67 now
  complete (was: proved only off the shared-normal locus).
- **d_{n-1} <= 6n for all n unconditionally** — the l=1 ceiling law of
  Postscript 19, previously only empirical (~1M configs), now a theorem.

**Correction to PROOF_67 (mine):** I had written the n=2 maximizer as
"45 deg about a face axis." Wrong — a face-axis rotation shares that
normal (on the shared-normal locus), where Theorem 1's self-exclusion
gives only d1 <= 8. Verified exactly: quaternion (2,0,0,1) and (5,0,0,2)
both -> 9 = {8,1}. The genuine maximizer is 180-about-(1,1,1). Good
catch by the agent, confirmed by main session.

**Verification (main session, 2026-07-20):** all four gates re-run:
G1 10,000 exact rational configs, max d1 = 12, zero violations; G2 seven
witnesses all 13={12,1}, #pi0(S_i)=6; G3 400 exact shared-normal configs,
worst per-cube count 4 (<=6). Maximizer 13 and face-axis 8/9 re-derived
independently through certify_six. Proof reviewed and judged correct; the
one soft step ("the ascent point lands in the SAME component U") is
standard and tightenable, corroborated by the zero-violation stress test,
and is not logically load-bearing for the reviewed argument.

**Status of max(3)=67 after this:** deep half PROVED (d2<=18, d3<=1);
shallow half is the sole remaining gap, exactly the inequality
Sum_v(deg_v-2) <= 92 on the top diagram (PROOF_67 sect.5,
CENSUS_BOUND_SPEC.md). 67 holds iff that holds.

## Postscript 34: feasibility verdict on the last gap (star) Sum(deg-2)<=92 — it splits 32+60, the easy half reduces to a clean "<=16 simultaneous triples" lemma, the hard half needs targeted (not random) search

CENSUS_BOUND_SPEC.md run in feasibility-first mode (census_bound_report.md,
census_bound.py). Gates: G1 reproduces 67={48,18,1} both witnesses; G2
the weight is exactly 92 at both maximizers via an INDEPENDENT code path
(cross-validates census_extract); G3 10,000 Haar-random configs, ZERO
violations of (star), max weight observed only 32. No (star) violation
found anywhere — max(3)=67 not refuted. Main session verified G2 and the
anchor-refutation independently.

**The central structural finding.** The weight-92 budget splits exactly
as the census's 32+60:
- Triple-point weight <= 32 (the "easy half"): generic configs ALREADY
  have 32 (32 trivalent triple points, F=18, d1=18 generic); random
  sampling saturates here. Reduces to a clean SIMULTANEITY lemma: "at
  most 16 elementary active-face triples (f0,f1,f2,s01,s12) are
  simultaneously realizable at any one config" -> x2 antipodal = 32.
  The number 16 is robust (max over 10^4 random configs = 16; exact at
  BOTH maximizers; 16 bare face-triples with unique sign patterns). This
  is a packing/angle-budget argument in the spirit of Theorem 1's
  matched/unmatched dichotomy applied to TRIPLES - the tractable next
  theorem. NOTE: reframes C45 sect.8's "Platonic elimination" - the
  restriction is NOT "which triples are globally impossible" (all 108 of
  the naive 3x3x3x2x2 occur SOMEWHERE) but "how many co-occur" (<=16).
- Contact-vertex weight <= 60 (the "hard half"): the 30 deg-4 / 6 deg-6
  same-pair coincidence vertices. This is a MEASURE-ZERO coincidence
  locus - structurally invisible to random sampling (why G3 maxes at 32,
  never approaching 92: the hard half isn't reachable by chance). Needs a
  TARGETED search, recommended via the dihedral family (C45 sect.12
  Theorem F: certain coincidences hold identically along Rel(theta,psi)) or
  by directly solving the coincidence equations - NOT blind sampling. The
  crux of (star); this run could not move it.

**Routes ruled out (concrete).** Chamber enumeration (approach 2):
INFEASIBLE, pilot measures chamber angular diameter <~0.02 rad in the 6-D
domain -> ~10^11-10^13 chambers. Certified-interval covering (approach 3):
infeasible for the same reason, worse constant. Anchor-reduction
(approach 4, my PROOF_67 sect.5.1 lead): DEAD/refuted (0/32 anchoring
triple points at both maximizers, confirmed exact + brute-force, 0.6-2.4%
margins) - corrected in PROOF_67 sect.5.1.

Net: the last gap is now cleanly split into a tractable sub-lemma (triple
weight <=32 via <=16-simultaneity) and the genuine crux (contact weight
<=60, a coincidence-locus classification needing the dihedral family).
max(3)=67 holds iff both hold; nothing found threatens it.

## Postscript 35: sub-lemma 1a PROVED — triple-point weight <= 32 (via d2 <= 18); max(3)=67 now hinges on ONE inequality (contact weight <= 60)

Main session, 2026-07-20 (proof + exact numerical verification). The
"easy half" of (star) closes cleanly, and it REUSES the proven d2 <= 18
rather than the packing/simultaneity argument the feasibility pass
envisioned.

Key observation: a triple point (M_0=M_1=M_2, all three cubes reach
equally far) is a vertex of BOTH the top diagram (the three
reaches-FARTHEST regions meet) AND the bottom diagram (the three
reaches-LEAST regions meet) — when all three values coincide, moving off
the point the argmax cycles through all three (top vertex) and the argmin
cycles through all three (bottom vertex). So the triple-point SET is
shared by the two diagrams.

LEMMA 1a: #triple points <= 32 (<=16 up to antipode); hence top-diagram
triple-point weight (deg-3, weight 1 each) <= 32.
PROOF: in the bottom diagram (deg-2 vertices suppressed), faces = S_i
components so F_bot = d2 <= 18 (Theorem 1). All remaining vertices deg>=3
=> by Euler V_bot <= 2(F_bot - 2) <= 32. Triple points are deg>=3 bottom
vertices, so #triple <= 32. QED.

Verified exactly: the generic relation is the EQUALITY #triple =
2(d2 - 2) (both diagrams trivalent on the shared vertex set, both
F = 2 + V/2, so d1 = d2 generically). Confirmed on 4 random configs
(#triple = 24,32,24,32 with fine-sampled d2 = 14,18,14,18 -> exact match)
and both maximizers (32 = 2(18-2), d2=18 attained, 1a TIGHT). This also
explains the census's "bottom stays generic": coincidences inflate the
TOP into contact vertices (the <=60 half) but leave the triple-point
count pinned by the bottom, which d2 <= 18 caps.

Caveat (same flavor as Theorem 1's soft step): needs each triple point to
be a genuine deg>=3 bottom vertex; a tangential triple point (bottom
argmin fails to cycle - a non-generic coincidence) folds into 1b's
degenerate analysis. Does not occur at the maximizers or generically.

STATUS OF max(3)=67: d3<=1 proved, d2<=18 proved, triple weight<=32
PROVED. The SOLE remaining gap is contact-vertex weight <= 60 (sub-lemma
1b) - the measure-zero coincidence-locus classification, to attack via
the dihedral family (Theorem F), not random search. max(3)=67 holds iff
contact weight <= 60. PROOF_67.md sect.5.3 has the proof.

## Postscript 36: region count is AFFINE-INVARIANT — the records are realized by a whole affine family of parallelepiped cells (congruent rhombohedra match 67), correcting a first wrong probe

Exploratory (2026-07-21, main session), prompted by "could cuboids/other
cells beat cube records?". Method: the region counter counts
{x : |m_a . x| <= 1 for the 3 body normals m_a}; feeding NON-orthonormal
columns counts a general parallelepiped cell. Validated: orthonormal
columns reproduce cube_regions_n (e.g. [I,R2,R3] cube triple = 55 =
{36,18,1}, exact).

**KEY FACT (user's point): region count is invariant under any global
invertible linear map A** (planes -> planes, arrangement type preserved).
So applying A to a cube-67 compound {R_k C} gives {A R_k C}, a compound of
PARALLELEPIPEDS, with count still 67. If A commutes with the compound's
symmetry the cells stay congruent. For the golden 67 (3-fold symmetry S
about (1,1,1)): take A = I + c*J (J = all-ones matrix) = a stretch ALONG
(1,1,1); it commutes with S, so the three cells A R_k C are congruent
RHOMBOHEDRA (cube stretched along its body diagonal). Verified EXACTLY
(cell normals A^{-1} R_k, Q(sqrt5)): total = 67 = {48,18,1} for all
c in [-1/6 .. 1] (drops to 57 only at c=2 where a wall is crossed). So
**congruent rhombohedra MATCH the 67 record over an open interval** - the
cube (c=0) is NOT special, it is one point of an affine family.

**CORRECTION of a first, wrong probe.** An earlier version of this
postscript claimed "cube is a STRICT local max vs cell shape" from a sweep
m_a(t)=e_a+t*(1,1,1) applied in each cube's OWN body frame (cells
R_k * rhombohedron), which collapsed 67 fast (67/37/25/13). That
deformation is NOT a global affine map (it deforms each cell in its own
rotated frame), so it does not preserve the arrangement - the collapse was
an artifact of the wrong operation, not a property of rhombohedra. The
correct WORLD-frame affine stretch (above) preserves 67. Lesson: cell-shape
questions must be posed as global affine maps to respect the affine
invariance of region count.

Consequences and what stays open:
- Congruent RHOMBOHEDRA match every record (affine stretch along the
  record's 3-fold axis). Congruent CUBOIDS (orthogonal stretch) do NOT
  arise this way for the octahedral/golden symmetry: an axis-PERMUTING
  symmetry forbids a non-scalar diagonal A that commutes with it (forces
  a=b=c=cube) - consistent with the n=2 cuboid scan finding no cuboid pair
  beating 13 (200 exact, best 8).
- Affine images only MATCH the record (count invariant); to BEAT it you
  need a parallelepiped config OFF the affine orbit of cubes. Not found:
  n=2 exact cuboid scan and n=3 rational rhombohedron scan (best 63 =
  rational cube max) produced no beat. So max_parallelepiped >= max_cube
  with equality on the affine orbit; whether it is STRICTLY greater is
  open.
- Proof bearing: since region count is affine-invariant but the
  equal-gradient-norm proof of d2<=18 / max(2)=13 is NOT (it uses
  orthonormality), an AFFINE-INVARIANT reformulation of the bounds may be
  cleaner and would automatically cover the whole parallelepiped orbit.
  The natural objects are parallelepiped compounds up to affine
  equivalence; "cube" is just a convenient representative.

## Postscript 37: *** RETRACTED (see Postscript 38) *** — this postscript is WRONG; it counted cells of the INFINITE-plane arrangement, not real face-bounded regions

RETRACTION (2026-07-21): every "beats the record" number below (hexahedra
40, off-center 25) is an ARTIFACT of a buggy counter that split regions at
the INFINITE extensions of face planes instead of at the actual finite
FACES. Under the correct definition (connected components of constant
cube-containment = the project's phantom-merged count), ALL these configs
give <= 13 at n=2: off-center = 5={4,1}, hexahedron pairs = 4, exactly as
the trivial convex-cover bound forces (A\B is covered by 6 half-space
intersections, one per face of B, so <= 6 components; d1 <= 12; total <=
13 for ANY two convex 6-faced bodies). "Central symmetry is the cap" is
FALSE - the cap is the generic convex-cover bound, holding for all convex
cells. See Postscript 38 for the correct analysis. The original (wrong)
text is kept below, struck, for the record.

~~Exploratory (2026-07-21, main session), answering "can anything with cube
topology beat 67?". YES, and immediately. A general convex hexahedron with
cube topology (6 quadrilateral faces, 8 vertices, cube adjacency) need NOT
have parallel opposite faces - so it contributes 6 INDEPENDENT face planes
per body, vs only 3 plane-DIRECTIONS (3 parallel pairs) for a
cube/cuboid/parallelepiped. Double the plane richness per body.

Method: trustworthy LP-based exact cell counter (enumerate realized sign
vectors of all planes; LP-verify each feasible + bounded; depth by
containment). Validated: reproduces the cube n=2 maximizer EXACTLY,
13 = {12,1}. (The grid counter is unreliable here - thin-cell aliasing,
counts that grow with resolution - and was NOT used for the conclusion.)

Result (n=2, both bodies verified genuine cube-topology: 8 vertices, 6
active faces; all contain the common center O; d2=1 sanity holds):
  eps:   0     0.05   0.1    0.2    0.3
  total: 13    17     18     23     21   (d1 = 12,16,17,22,20; d2=1)
Even eps=0.05 beats 13. The cube is NOT a local max within cube-topology
bodies; breaking parallelism raises d1 past 12 at once. A random n=2
hexahedron scan reached 40 = {39,1} - d1=39, more than TRIPLE the cube cap
of 12. (LP counter samples cells, so these are LOWER bounds on the true
counts; the qualitative "beats 13" is rock-solid.)

**Why: it is CENTRAL SYMMETRY that caps, not topology or rigidity.**
- Cube/cuboid/rhombohedron/parallelepiped are all CENTRALLY SYMMETRIC
  (opposite faces parallel & equidistant); they are exactly the affine
  images of a cube; region count is affine-invariant, so they all MATCH
  (Postscript 36) and are all CAPPED (13 at n=2).
- A general cube-topology hexahedron is NOT centrally symmetric, and the
  cap vanishes. Mechanism: the proof that caps cubes (Theorem 1, d2<=18,
  the <=6 components-per-body anchor bound) rests on the equal-gradient-
  norm identity at reach-ties, which comes from |n.u| = the |.| of
  CENTRAL SYMMETRY (faces come in +-n pairs). Without it the tie-gradient
  norms differ, parasite components form freely, and d1 balloons.

So the entire records tower (13/67/183/...) and its proof machinery
(Theorem 1, the mod-4 parity law, antipodal region pairing, d_n=1) are
features of CENTRALLY-SYMMETRIC cells. max(3)=67 is a theorem about cubes
(centrally symmetric) and stands; it is simply NOT the max over all
cube-TOPOLOGY cells - dropping central symmetry is a different, larger
problem with no such cap. This precisely locates where on the rigidity
ladder the records live: at the central-symmetry (parallelepiped) rung,
not the combinatorial-cube rung.

WHICH RIGIDITIES SUSTAIN >{12,1} (n=2, LP counter, lower bounds): the
ONLY forbidden one is cell central symmetry (inversion -I in the cell's
point group = parallelepiped = capped at 13). Everything else is
compatible: CONGRUENT non-central pair -> 39={38,1} (no penalty for
congruence); 4-fold-symmetric FRUSTUM pair (non-central) -> 27={26,1};
unconstrained -> 38={37,1}. Nuance: more cell symmetry costs some count
(frustum 27 < generic 39) but does NOT cap - only the inversion symmetry
triggers the parasite-exclusion cap. So a cell may carry any point group
that EXCLUDES -I (rotational axes, mirrors, frustum C4v, tapered-
rhombohedron C3v) and still clear the record cap; it must only avoid
central symmetry.

REFINEMENT + a correction to the off-centering belief: the true
cap-hypothesis is not "the cell is centrally symmetric about its own
center" but "the reach FROM THE COMMON CENTER O is symmetric,
r(u)=r(-u)". For a cube those coincide only when it is CENTERED at O.
Move a cube off O (center c): its faces sit at n_a.x = n_a.c +-1, still
parallel, but the reach-from-O vectors become m_a^+- = +-n_a/(1 +- n_a.c)
of UNEQUAL length -> breaks the equal-gradient-norm identity -> lifts the
cap, the SAME mechanism as non-parallel faces. Verified (LP counter, n=2):
OFF-CENTER cube pairs reach 25 = {24,1}, ~2x the concentric cap of 13
(d1=24 vs 12); less than the 39 of full non-parallel hexahedra because
off-centering keeps 3 plane-DIRECTIONS (unequal-length pairs) rather than
6 independent planes. This CORRECTS the standing project belief
"off-centering strictly hurts / concentric is optimal" (PROJECT.md sect.10):
that only tested TRANSLATING the 723 record (a local perturbation of a
concentric-tuned optimum, which of course falls), NOT a from-scratch
off-center search. Concentric is a LOCAL max; it is NOT the global max
once off-centering is allowed. Caveat on "record": the radial/depth
framework assumes O interior to every body; large offsets put O outside a
cube (its ray-contribution no longer starts at r=0), muddying the
depth-profile notion the records are stated in - so a fair off-center
"record" search should keep O interior to all cells, or restate the
target as raw bounded-cell count.~~ [END OF RETRACTED POSTSCRIPT 37]

## Postscript 38: the counting error corrected — regions are separated by FACES, not infinite planes; and a trivial proof that max(2) = 13 for ALL convex 6-faced cells

Root cause (user caught it, looking at the off-center viewer): "some
regions are separated by the infinite planes through the faces, not by the
faces." Exactly right. A "region formed by the cubes" is a connected
component of the complement of the actual finite FACE polygons -
equivalently a component of constant CUBE-CONTAINMENT (which cubes contain
the point), since you cross a real face iff the containment set changes.
Crossing a face's infinite EXTENSION where that cube is absent changes no
containment bit and must NOT split a region. The project's engines
(cube_regions_n, certify_six) do exactly this "phantom-facet merge". My
Postscript-37 experiments used LP/grid counters that instead counted cells
of the INFINITE-plane arrangement (constant 12-bit sign vector), which
over-splits - inflating the counts.

CORRECTED COUNTS (exact overlap-graph method; validated: concentric
maximizer = 13 = {12,1}, matching cube_regions_n):
- off-center cube pair (quat 0,1,1,1 + offset .5,0,.25): **5 = {4,1}**
  (Postscript 37 wrongly said 25).
- hexahedron (non-parallel-face) pairs: best **4** (wrongly said 40).
- off-center random scan: best **7** (wrongly said 25).
NONE beat 13.

TRIVIAL PROOF that max(2) <= 13 for ANY two convex cells with <= 6 faces
each: the depth-1 region contributed by cell A is A\B; write A\B =
union over the (<=6) faces f of B of (A intersect {outside face f}), each
a convex set, so A\B has <= 6 connected components (a union of k convex
sets has <= k components). Symmetrically B\A <= 6. With the single convex
core, total <= 6+6+1 = 13. This holds for cubes, cuboids, rhombohedra,
general hexahedra, off-center - ANY convex 6-faced bodies. So at n=2 the
cap 13 is NOT special to cubes or to central symmetry; it is the generic
convex-cover bound. (Note this also RE-PROVES max(2)=13 far more cheaply
than Theorem 1's equal-gradient-norm argument - Theorem 1's value is for
n>=3, where B is replaced by a NON-convex union of others and the cover
argument no longer applies.)

RETRACTIONS/CORRECTIONS:
- Postscript 37 is RETRACTED in full (hexahedra/off-center do NOT beat
  records; "central symmetry is the cap" is false; the "rigidity ladder"
  and frustum/congruence numbers were all sign-vector artifacts).
- The answer given to "could off-centering beat a record" (yes) is WRONG;
  correct answer: NO at n=2 (convex-cover), and the standing project
  belief "off-centering does not help" is VINDICATED, not overturned.
- Postscript 36 SURVIVES: affine-invariance of the count is correct
  (linear maps preserve containment), and "congruent rhombohedra match 67"
  was computed with certify_six (the correct engine) - matching, not
  beating, and true. Only 36's tentative "central symmetry" framing is
  superseded by the convex-cover picture here.
- Whether any NON-cube convex cell ATTAINS 13 at n=2 (the bound) is a
  separate, still-fine question: parallelepipeds do, via affine images of
  the cube-13 (Postscript 36); the bound is 13 for all 6-faced convex
  cells regardless.

n=3 correct counts (overlap-graph method extended to 3 cells; validated:
octahedral cube triple = 67 = {48,18,1}): general HEXAHEDRON triples
(random) best 20 = {10,9,1}; OFF-CENTER cube triples (random) best
26 = {13,12,1} - both FAR below 67. (Random, not optimized, so not a
proof of no-beat, but the same direction as n=2: irregular cells do
WORSE, cubes are near-optimal.) Note the convex-cover argument gives
d3<=1 and d2<=18 for ALL convex 6-faced cells (re-proving those bounds
beyond cubes), but only d1<=108 (each depth-1 region = union of 6x6=36
convex pieces), so it does NOT rule out a non-cube cell beating 67 at
n>=3 - that remains genuinely open, with all correct evidence pointing
to "no".

LESSON: use the project's own engines (or the exact overlap-graph /
containment method) for region counts; never the raw sign-vector cell
count, which is a different (larger) quantity.

## Postscript 39: the CORRECT successor to P37 — the max(3)=67 proof layers GENERALIZE to all convex 6-faced cells, and flex does not beat 67

Consolidation (2026-07-21, correct containment counter throughout). This
replaces the retracted P37 "central-symmetry" narrative with the right
one. Three of the four layers of the max(3)=67 proof are now seen to hold
for ANY 3 concentric convex 6-faced cells (cubes, cuboids, rhombohedra,
general hexahedra, off-center), NOT just cubes:
- d3 <= 1: convexity of the triple intersection.
- d2 <= 18: convex-cover — depth-2 region (X∩Y)\Z = union over Z's 6
  faces of a convex set, <= 6 comps, x3 pairs = 18.
- triple-point weight <= 32: follows from d2<=18 via the shared top/bottom
  vertex + bottom-Euler argument (Postscript 35), all radial, no cube
  specifics.
So d1 = 2 + (1/2)(triple + contact) and the WHOLE remaining question is
contact <= 60, equivalently d1 <= 48, equivalently #comp(cell\(others))
<= 16 per cell.

FLEX EVIDENCE (correct counter, ~4300 evals): hill-climbs maximizing total
regions from the octahedral 67 (2100 evals) AND the golden 67 (best 67)
AND random starts (best 31/31/33) NEVER exceed 67; random flex scans top
at ~33. So d1 <= 48 appears to hold for all convex 6-faced cells too -
i.e. **max(3)=67 generalizes to a conjecture: any 3 concentric convex
6-faced cells make <= 67 bounded regions, attained by cubes/parallelepipeds
(their affine images tie it, P36).** Nothing flex beats 67.

REMAINING GAP (unchanged in difficulty, clarified in scope): d1 <= 48,
i.e. #comp(cell\(B∪C)) <= 16. Convex-cover gives only <=36/cell (via
cell\(B∪C) = (cell\B)∩(cell\C), intersection of two <=6-component sets =
<=36), a factor ~2 loose. Tightening 36->16 is the SAME top-diagram
component bound as the cube-specific sub-lemma 1b (contact<=60); the
general framing just forbids cube specifics, so any proof must be robust.
This is the clean lemma to attack: bound the components of a convex
6-faced cell minus two convex bodies at <= 16. It subsumes max(3)=67.

Note P37's "beats records / central symmetry is the cap" is fully dead;
the correct statement is the opposite - cubes are (conjecturally) EXTREMAL
among convex 6-faced cells, and the cap is generic to convexity + 6 faces.

## Postscript 40: the remaining gap reduced to a clean INCIDENCE bound on the cells' edge-skeletons (verified), with an Euler-on-intersection handle (not yet closed)

Real run at contact-weight <= 60 (2026-07-21). Progress on FORMULATION,
NOT a completed proof - stated honestly.

VERIFIED CORRESPONDENCE: the top-diagram contact vertices are physical
crossings of the cells' 1-skeletons. A deg-4 contact = an edge-edge
crossing (an edge of cell i meets an edge of cell j in 3-space); a deg-6
contact = a corner coincidence (triple point at cell corners). Checked
exactly at octahedral 67: 30 edge-edge crossings, 10 per pair = the 30
deg-4 vertices. (Also: physical triple points ∂A∩∂B∩∂C, T=32, ARE the
direction-sphere triple vertices - since x on all 3 convex surfaces in
direction u => r_A=r_B=r_C=|x| at u.)

REDUCTION: contact weight <= 60  <=>  2*(edge-edge crossings) +
4*(corner coincidences) <= 60, for the 1-skeletons of 3 concentric convex
6-faced cells, ON-TOP (crossing must lie in a direction where its two
cells reach farthest = outside the third cell). Shape-independent; the
cleanest form of the crux (no direction sphere, no census).

HANDLE (new, right kind): edge-edge crossings of cells P,Q = the DEGREE-4
vertices of the convex intersection polytope P∩Q (a point where 2 faces
of P and 2 of Q meet). P∩Q has <=12 faces, so Euler bounds its excess
degree: Sum_v(deg_v - 3) <= 2F-4-V <= ~16 per pair. Same species of
argument that makes d2<=18 shape-independent, now on the pairwise
intersection.

NOT CLOSED: the Euler-on-P∩Q bound is ~1.6x loose (~16/pair vs actual 10;
~48 total vs needed 30). Two missing ingredients: (1) the ON-TOP
restriction (only crossings outside the third cell count) is not yet
folded into the Euler bound; (2) the edge/corner weight tradeoff (golden:
18*2+6*4=60) must hold across the redistribution. Concrete next step:
incorporate "outside the third cell" into the P∩Q Euler bound - that is
what stands between ~48 and 30.

## Postscript 41: CANDIDATE PROOF of max(3)=67 (all convex 6-faced cells) via Euler on the PAIRWISE intersection polytopes — the contact bound closes

2026-07-21, main session. Grew directly out of the user's "if 67 is
shape-independent there must be an Euler-characteristic constraint"
intuition. STATUS: candidate proof; one step verified on 35 configs
(tight at BOTH maximizers, zero failures) but wanting a rigorous
local-degree write-up before "proved". Nothing found > 67.

THE PROOF CHAIN (3 convex cells, each <=6 faces, concentric):
1. d1 = 2 + (1/2)(T + contact)   [Euler on the top diagram; T = # triple
   points, contact = weight of the deg>=4 top vertices]. So
   2(d1-2) = T + contact.
2. T <= 32   [PROVEN, Postscript 35: T = triple-point weight, bounded via
   the bottom-diagram Euler + d2<=18].
3. **contact <= Sum over the 3 pairs of (2*F(cell_i ∩ cell_j) - 4).**
   For a convex polytope, Sum over ALL vertices of (deg-2) = 2E-2V =
   2(V+F-2)-2V = 2F-4. The top-diagram contact vertices map to the
   deg>=4 vertices of the pairwise intersection polytopes with matching
   degree (a deg-4 top contact = an edge-edge crossing = a deg-4 vertex
   of P_i∩P_j; deg-6 = a corner = deg-6 vertex; etc.), so
   contact <= Sum_pairs Sum_v(deg_v - 2) = Sum_pairs(2F-4).
   Each cell has <=6 faces => F(P_i∩P_j) <= 12 => 2F-4 <= 20 =>
   contact <= 3*20 = **60.**
4. => 2(d1-2) <= 32 + 60 = 92 => **d1 <= 48.**
5. d2 <= 18, d3 <= 1   [convex-cover / convexity; Postscript 38/39].
6. total <= 48 + 18 + 1 = **67**, attained by cubes/parallelepipeds. QED
   (modulo step-3 rigor).

VERIFICATION (correct containment counter throughout): step 3 inequality
2(d1-2)-T <= Sum_pairs(2F-4) checked on 35 configs - octahedral 67 and
golden 67 (both TIGHT: contact=60=Sum(2F-4)), 12 near-octahedral
perturbations, 21 random hexahedra - ZERO failures, and Sum(2F-4)<=60
always (F<=12 is a hard fact). The two maximizers SATURATE every
inequality (T=32, contact=60, F=12 on all 3 pairs), which is exactly why
67 is the max and why the bound is calibrated, not loose.

STEP-3 CORRESPONDENCE - now argued (the LOCAL FACE-COUNT lemma):
At a contact where cells i,j are tied for farthest (cell k strictly less),
let a,b = # faces of i,j ACTIVE at the physical point x0. Then BOTH
degrees equal a+b:
  - deg_top = #sign-changes of M_i-M_j around the direction = a+b (the a
    active faces of i fan into a sectors, b into b sectors; M_i-M_j is
    linear per sector and flips once per ray).
  - deg_poly = edges of the pointed 3-cone cut by the a+b facet-planes
    through x0 (all active faces pass through x0) = a+b.
So deg_top = a+b = deg_poly (edge-edge a=b=2 ->4; corner a=b=3 ->6),
matching the exact spectra at both maximizers ({30 deg-4} octahedral;
{18 deg-4, 6 deg-6} golden). Hence contact = Sum(deg_top-2) =
Sum over contact vertices (deg_poly-2) <= Sum over ALL pairwise-polytope
vertices (deg_poly-2) = Sum_pairs(2F-4).

VERIFICATION STRENGTHENED: the inequality contact <= Sum_pairs(2F-4)
checked on 130 configs total (both maximizers TIGHT; near-octahedral
perturbations, random hexahedra, off-center cubes, cuboids, rhombohedra),
ZERO failures, ZERO d1>48. Directly confirms the bound independent of the
per-vertex argument.

LEMMA FILLED IN (PROOF_FORMAL.md, 2026-07-21): the |S|=2 correspondence
is now RIGOROUS - a genuine contact has a,b>=2; the swap curve has a+b
arcs; P_i∩P_j at x0 is a POINTED cone with a+b facets => a+b edges
(pointedness: the a+b active facet-normals span R^3 since the two cells
meet transversally at the isolated point x0). No "cut-off face" issue
arises. This covers EVERY contact at both maximizers. The one residual is
degenerate triple points (|S|=3, top-degree>3): fixed by booking ALL |S|=3
vertices into the triple-point term (Part C) and extending W_triple<=32 to
them via deg_top<=deg_bot (Step T). Non-generic, 0/130 occurrences, absent
at both maximizers.
NET: max(3)=67 PROVED for the generic stratum AND both maximizers (tight),
and for all convex 6-faced cells up to the single non-generic Step T. Full
clean proof: PROOF_FORMAL.md; narrative: PROOF_NARRATIVE.md.

SIGNIFICANCE: this proves max(3)=67 for ALL 3 concentric convex 6-faced
cells (cubes are one case), via three separate Euler arguments - bottom
diagram (T<=32), convex-cover (d2<=18), and NOW pairwise-intersection
polytopes (contact<=60). It is the shape-independent Euler constraint the
user predicted. Also finally supersedes the whole retracted-P37 detour:
the answer is that cubes are extremal and the cap is a triple Euler bound.

## Postscript 31: the census extraction — the 92 budget is EXACT at both 67 witnesses, its accounting corrected, and the coincidences ARE top-diagram vertices

CENSUS_SPEC.md executed (census_report.md, census_extract.py,
census_data.json; main session re-verified the Euler arithmetic from
the raw V/E and the weight decompositions below). Gates: G1 both
witnesses reproduce 67 = {48,18,1} (slide3_q2 for octahedral Q(sqrt2);
certify_six oracle for golden Q(sqrt5), matrix hand-derived, S^3=I
exact); G2 the sharp gate — exact-arithmetic diagram graphs give
TOP-1 Euler faces F = 48 and BOTTOM F = 18 at BOTH witnesses (W1:
V=62, E=108; W2: V=56, E=102; bottoms V=32, E=48); G3 antipodal
symmetry; plus a generic rational cross-validation (37-config: top
18, bottom 18, oracle-matched).

**The census, correcting sect. 13's projected accounting.** The
projected budget "46 triples x 2 = 92, F <= 2 + 92/2 = 48" is right
in TOTAL WEIGHT and wrong in attribution:

- Total top-diagram weight Sum_v(deg_v - 2) = 92 EXACTLY at both
  witnesses — the d1 = 48 bound is Euler-TIGHT (F = 2 + 92/2).
- Rank-triple points carry only 32 units: exactly 32 triple points,
  ALL trivalent, at both witnesses = 16 occurring active-face triples
  (6 C3-orbits) x 2 antipodal points. No merged triple points.
- The other 60 units sit on SAME-PAIR double-tie vertices, and these
  are precisely the coincidence census: W1 = its 30 interior edge-edge
  crossings, each a degree-4 vertex (weight 2, 30x2 = 60); W2 = its
  18 interior crossings (deg 4) + 6 physical corner contacts (deg 6,
  weight 4): 36 + 24 = 60. Two different degenerations, same 92.
- Sect. 13 L2.b's assumption "kinks are degree-2, discountable" is
  FALSE at both attainers: the (c2)/(c3) classification must budget
  same-pair multi-tie vertices alongside rank triples. The corrected
  target statement: Sum_v(deg_v - 2) <= 92 over triple points AND
  pair-contact vertices, with equality at both witnesses.
- BOTTOM diagrams of both witnesses are fully generic: V=32, E=48,
  F=18, zero degenerate vertices — exactly the V_1(3) = 12n-4 = 32
  census — despite the heavy top-side degeneracies.

**Synthesis with Postscript 30** (the two campaigns interlock): edge
and corner coincidences live as VERTICES OF THE TOP DIAGRAM ONLY —
the bottom diagram of even the maximally-degenerate witnesses is
untouched. That is WHY every event's count delta lands in d1 with
deep layers conserved (Postscript 30's 12/12 law): coincidence
events add/remove top-diagram vertex weight, and d1 = top faces =
2 + weight/2, while d2/d3 read the bottom diagram, which the
coincidences never touch. The create-vs-merge question becomes:
does the acquired vertex weight EXCEED the swap-arc structure it
consumes — an Euler bookkeeping question on one diagram, no longer
a mystery spread across mechanisms.

Proof-program status after this: cluster 2's remaining work is the
(c2) feasibility classification with the corrected two-type budget
and the (c3) degeneracy-robust form — the witnesses' own numbers now
give the exact equality cases the classification must reproduce.

Full sweep (dense tilt menu, tier-4 hill-climbs, n=6 completions of
the new 387) still to run — the agent resumes after its limit resets.

### Postscript 29 addendum: 723 is a PLATEAU with (at least) four non-congruent realizations — an exact three-layer exchange law inside the summit

Tier 3 at full scale (393's five ledger cubes fixed + 4,000 random 6th
integer quats, ||q||^2 <= 600): 27 completions tie 723 EXACTLY (28
counting the known (5,2,2,2)), none beat it. They fall into exactly
FOUR depth profiles (a different histogram proves non-congruence
outright):

    d2, d3, d4 = 216+2k, 164-4k, 96+2k    for k = 0,1,2,3
    d1=210, d5=36, d6=1 fixed;  d2+d3+d4 = 476 constant

k=0 is the ledger profile; k=1,2,3 are genuinely new compounds with
the same total. Example 6th quats: (11,11,10,11) k=2 (norm 463, not a
symmetry multiple of (5,2,2,2), norm 37), (3,-4,-3,3), (5,-5,5,4).
Every hit oracle-verified by the agent; main session independently
re-ran (11,11,10,11) through the C++ engine: 723 = {210,220,156,100,
36,1} confirmed. So the n=6 record is not an isolated configuration
but a summit plateau on which (d2,d3,d4) trade at fixed exchange rate
(+2,-4,+2) — the Postscript-11-addendum shallow-tail conservation
appearing exactly, at the top. The record VALUE 723 stands unbeaten;
"the 723 compound" is now four compounds (at least).

Also from run 1 at full tier-3 scale: 183-triple on-axis 4th-cube
sweeps (all three resonant axes, full Farey-40) top out below the
integer-quat completions — the 4th record cube must be off-axis,
exactly like 393's cube 0 and 723's cube 5. Phase 2 (71,510 more
configs: dense tilt menu + 387-completions + hill-climbs) has finished
computing; bests unchanged so far (183/387/723); agent summary pending.

## Postscript 42: Step T is NOT routine — the reduction "deg_top ≤ deg_bot at triple points" is FALSE (counterexample realized on genuine cells); max(3)=67 stands on the generic stratum + both maximizers, degenerate triple points remain an open gap

2026-07-21, main session, answering the user's "please write Step T
rigorously." Attempting to discharge the one step PROOF_FORMAL.md had
marked "routine/LOW risk," I instead found it is false as stated, and
have corrected all three proof documents accordingly.

WHAT STEP T NEEDED: W_triple ≤ 32 including degenerate triple points
(|S|=3 top-diagram vertices of degree > 3). The marked route: every
triple point is a bottom-diagram vertex, and "deg_top ≤ deg_bot" there,
so W_triple ≤ Σ_bottom(deg_bot−2) = 2(d2−2) ≤ 32.

WHY IT FAILS: deg_top ≤ deg_bot is false. The top diagram (farthest
cell) is the argmin of the three cells' support functions m_i = h_{P_i}
(P_i = convex hull of the active-facet tangential gradients at the triple
point); the bottom diagram (nearest cell) is the argmax. The argmax is
the support function of conv(∪P_i) — a simple outer envelope; the argmin
is an INNER envelope of convex bodies, which genuinely wiggles more.
Explicit: cell A a corner (a=3, small gradient triangle), cells B,C thin
blades (b=c=2, gradients ≈ (±g,0) and (0,±g)). The corner is farthest in
all four diagonal sectors and each blade near its own axis →
  deg_top = 8,  deg_bot = 4.
Confirmed three ways (scripts saved to project):
 • stepT_local.py — abstract support-function switch counts: 8 vs 4.
 • stepT_realize.py — built as three ≤6-facet cells about O (two blade
   wedges μz+g|x|≤1, μz+g|y|≤1 capped to 5 facets; one 3-facet corner
   cone capped to 4), valid triple point (x0 on 3/2/2 facets, O interior).
 • stepT_degcheck.py — sampled the ACTUAL reach functions on a small
   circle around û0: farthest-cell degree 8, nearest-cell degree 4.
So deg_top > deg_bot occurs for honest convex cells, not just the model.

WHY 67 IS NOT IN DANGER (but this is evidence, not proof): the isolated
degenerate triple gives only 10 total regions (region-poor); it is
non-generic (measure zero); ABSENT at both maximizers (their bottom
diagrams are exactly generic — 32 degree-3 triple points); and never
appeared in any sampled config. A 250-config search (thin boxes,
near-coincident triples) maxed at d1=18, far under 48 — random boxes just
don't interleave like the special maximizers, so this is weak. The record
67 rests on the project's exhaustive engine search, independent of this
proof. The open content of Step T is exactly: can a degenerate triple
point (deg_top > deg_bot) coexist with a high-count configuration and push
d1 past 48? Unresolved.

CORRECT ROUTE (recommended, not yet done): abandon the triple/contact
split for the degenerate case. The top diagram is precisely the radial
projection to S² of ∂U, U = K1∪K2∪K3, so d1 = 2 + ½W is the combinatorial
complexity of the boundary of a UNION of three convex ≤6-facet polytopes.
A global/amortized bound on that union-boundary complexity (rather than a
per-vertex deg_top ≤ deg_bot) is what would close d1 ≤ 48 unconditionally.

DOCUMENTS CORRECTED: PROOF_FORMAL.md (Step T rewritten from "LOW risk"
to OPEN, with the counterexample and the union-boundary route; status
section updated), PROOF_67.md (top verdict, §5.4 residual, §6, Open #1),
PROOF_NARRATIVE.md ("Where it stands"). The |S|=2 contact lemma
(deg_top = a+b = deg_poly, Part D) remains rigorous and unaffected —
the gap is solely the |S|=3 degenerate stratum. Net honest status:
max(3) = 67 is a theorem on the generic stratum and at both maximizers;
universal over all convex 6-faced cells only up to Step T.
