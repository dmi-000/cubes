# Cube-compound region counting

Exact enumeration of the bounded 3D regions formed by compounds of *n*
congruent, concentric unit cubes (each the cube [−1,1]³ under a rotation
Rₖ ∈ SO(3)). "Exact" means no floating point in any decision: every
region count is computed with rational or algebraic (ℚ(√d), and towers
ℚ(√a,√b)) arithmetic and certified predicates, so a reported count is a
theorem about that configuration, not a numerical estimate.

The scientific record lives in **`six_cube_search_results.md`** (read its
postscripts in order — several early conclusions were overturned by exact
counting and the corrections matter). This README is the map of the code
and documents around it.

## Current records (all exact)

| n | best bounded regions | configuration | field |
|---|---|---|---|
| 3 | 67 | octahedral 3-compound = golden 3-subset | ℚ(√2) / ℚ(√5) |
| 6 | **717** | D₂-orbit-of-4 + free + axis-aligned cube | ℚ (rational) |
| 6 | 705 | two 3-fold triples on shared (1,1,1) axis | ℚ (rational) |
| 6 | 699 | two 3-fold triples (earlier record) | ℚ (rational) |
| 6 | 681 | golden five + sixth on the (1,1,1) wall | ℚ(√5) |
| 6 | 655 | two 60°-body-diagonal pair walls, constructed | ℚ (rational) |
| 6 | 635 | best from 360k random rational seeds + climbing | ℚ (rational) |
| 7 | 1085 | best n=7 campaign seed (search ongoing) | ℚ (rational) |

Deep-depth ceilings **d3 ≤ 164, d4 ≤ 102, d5 ≤ 36, d6 = 1** have never
been exceeded in any config or on any wall tested (conjectures C4/C5/C6,
with a proof program in `C45_notes.md`). The 717 record has depth
histogram {1:210, 2:210, 3:158, 4:102, 5:36, 6:1} — its gain over 699 is
entirely in depth-1, with a deep tail *below* the ceilings. See
Postscript 11 for its quaternions.

## Quick start

```sh
# Build the C++ engine (no dependencies):
clang++ -O2 -std=c++17 -o cube_regions   cube_regions.cpp     # n=6 (default)
clang++ -O2 -std=c++17 -o cube_regions_n cube_regions.cpp     # same source, --n K

# Self-test (axial fan of 6 cubes must count 121):
./cube_regions --selftest

# Count one seed's configuration exactly:
./cube_regions --seed 2228            # -> 623

# Count an explicit compound (semicolon-separated integer quaternions w,x,y,z):
./cube_regions --quats '3,1,0,0;3,0,1,0;3,0,0,1;41,28,22,14;41,14,28,22;41,22,14,28'   # -> 699

# Any n from 2..12:
./cube_regions_n --n 7 --seed 777     # -> 973

# Every program responds to --help:
./cube_regions --help
python3 exact_search.py --help
```

Python programs print their module docstring on `--help`. Nothing here
needs pip installs beyond numpy/scipy/mpmath (used only by the Python
oracle and the seed-chain validation).

## Continuing the searches

Every config is identified by `(n, seed)` or by explicit quats, and
seeds are independent and deterministic, so any range can be (re)run in
any order and merged. Campaigns append-and-dedupe by seed, so it is safe
to overlap ranges. Progress so far: **n=6 covered through seed 359,999**
(`campaign_results.jsonl`); **n=7 through seed 52,999** (`campaign_n7.jsonl`).
Prefix long runs with `nohup caffeinate -i … &` to survive logout/sleep.

### n = 6 (rational campaign — extend the 360k already done)

```sh
# Continue the random-seed campaign from where it stopped (8 workers):
nohup caffeinate -i python3 run_campaign.py 360000 500000 8 \
      >> campaign.out 2>&1 &
# Result appends to campaign_results.jsonl; the driver reports best total
# and flags any ceiling violation (d3>164, d4>102, d5>36, d6≠1).
```

### n = 6 (record hunt — climb toward >699, not just sample)

Random sampling plateaued at 635; the records past that came from
constraint-first construction and hill-climbing, so to beat 699 climb:

```sh
# Exact greedy hill-climb from the current best configs (logs every eval):
python3 phase_b_hillclimb.py --topk 20 --workers 8 --objectives total \
      --restarts 4 --out hillclimb_log.jsonl
# Seed a climb from the 699 record directly (fast C++ eval of one config):
./cube_regions --quats '3,1,0,0;3,0,1,0;3,0,0,1;41,28,22,14;41,14,28,22;41,22,14,28'
# The three wall/field programs that produced 655/681/699 are re-runnable:
python3 multiwall_m4_extend.py --help    # rational double-wall (655)
python3 golden_six.py search             # golden ℚ(√5) wall (681)
python3 slide3_p3.py --help              # two-triple overlay (699)
```

### n > 6 (generalized campaign — spec: `NPLUS_SPEC.md`)

```sh
# Continue n=7 from where it stopped (capped at 4 workers by convention
# while the field program has compute priority):
nohup caffeinate -i python3 run_campaign_n.py --n 7 53000 150000 4 \
      >> campaign_n7.out 2>&1 &          # appends to campaign_n7.jsonl

# Start n=8 (fresh; ~5k seeds is the trimmed target):
nohup caffeinate -i python3 run_campaign_n.py --n 8 3000 8000 4 \
      >> campaign_n8.out 2>&1 &          # -> campaign_n8.jsonl

# Hill-climb the best n=7 configs found so far:
python3 phase_b_hillclimb_n.py --help

# Re-run the n>6 validation gates before trusting a new n:
python3 scratch_gate_g1.py    # n=6 regression vs the oracle
python3 scratch_gate_g2.py    # n∈{2,3,4,5,7,8} cross-check vs Python oracle
```

### After any run: check for records and violations

```sh
# Best total + max-per-depth + any ceiling breach in a log:
python3 phase_c_analysis.py                          # n=6 aggregate
python3 check_live_boundaries.py 360000 500000       # scan a seed range
# Quick best-in-log:
python3 -c "import json;m=max(json.loads(l)['bounded'] for l in open('campaign_n7.jsonl'));print(m)"
```

Record the outcome in `six_cube_search_results.md` (Postscript 6 for
n>6 is a living section; add a postscript for a new n=6 record).
`exact_search_results.jsonl` is **read-only** ground truth — never write
to it.

## Documentation (`.md` files)

| file | kind | what it is |
|---|---|---|
| `six_cube_search_results.md` | **ledger** | The authoritative project record. Postscripts 1–11: exact-count corrections to the voxel era, subset maximality, the C++ campaign, the 635→681→699→717 record chain, the ℚ(√5)/tower field program, the sliding-3-cube result, and the symmetry-stratified sweep. Start here. |
| `C45_notes.md` | notes | Proof program for the deep ceilings (d3≤164, d4≤102, d5≤36) via the radial-escape lemma and bottom-diagram census (T1 Euler count + T2 semicontinuity). |
| `CPP_SPEC.md` | spec | Design of the C++ engine: integer-homogeneous coordinates, int128 predicate budget, seed chain, validation gates. Working-principles doc for `cube_regions.cpp`. |
| `NPLUS_SPEC.md` | spec | Generalization of the engine and campaigns to n>6 (`--n K`). Working-principles doc for the `*_n.py` and `scratch_*_n.py` drivers. |
| `QFIELD_SPEC.md` | spec | Extend the search from rational rotations to ℚ(√d) (and the ℚ(√3,√5) tower). Field/wall taxonomy. |
| `MULTIWALL_SPEC.md` | spec | Multi-constraint ("stacked wall") search + tower verification. Working-principles doc for `qtower.py` and `multiwall_*.py`. |
| `SLIDE3_SPEC.md` | spec (V1) | Original plan for overlaying two sliding 3-cube triples. Its section 0 family is **superseded** by V2 (kept for the record). |
| `SLIDE3_SPEC_V2.md` | spec | Corrected sliding-3-cube family (common 3-fold axis; congruence up to octahedral self-symmetry). Working-principles doc for `slide3_*.py`. |
| `golden_wall_report.md` | report | Results of the ℚ(√5) golden-wall pilot (found 681). |
| `multiwall_report.md` | report | Results of the multi-constraint / tower search (found rational 655; explained the (1,1,1) wall). |
| `slide3_report.md` | report | Sliding-3-cube results: section 0 = V1 (family disproven), `## V2` = corrected family and the 699 record. |

**Out of scope (separate Sean Carroll AMA project, not part of this
work):** `IMPROVEMENT_PLAN.md`, `patreon_scrape.md`, and `norton.py`.
They live in this directory for historical reasons; ignore them for the
cube work.

## Source code

Every source file begins with a module docstring (its purpose + usage)
and a `Working principles:` comment naming the doc that explains its
method. Group by role:

### Exact counting engines
| file | purpose | principles |
|---|---|---|
| `cube_regions.cpp` | Primary engine. C++17, no deps. Integer-homogeneous exact counter; `--n`, `--seed(s)`, `--quats`, `--selftest`. ~5–80 ms/config. | `CPP_SPEC.md` |
| `certify_six.py` | Python oracle: `exact_count_config()` over certified intervals + ℚ(√5); the cross-check the C++ engine is validated against. Any n. | ledger + `CPP_SPEC.md` |
| `cube_compound_exact.py` | ℚ(√5) golden-compound counter (`run(N)`); the `Q5` exact field class used everywhere. | ledger |
| `cube_compound_interval.py` | 3-tier certified-interval kernel (float→mpmath→exact) that filters predicate signs. | ledger |
| `cube_compound_regions.py` | Original general region counter (plane-arrangement construction). | ledger |
| `six_cube_search.py` | Shared config helpers (`count_mats`, `random_mats`, rational rotations). | ledger |
| `qtower.py` | Recursive quadratic-tower field ℚ(√a,√b) with exact recursive sign; verifier for wall points. | `MULTIWALL_SPEC.md` |
| `slide3_q2.py` | ℚ(√2) field + counter (octahedral 45° endpoint). | `SLIDE3_SPEC_V2.md` |
| `golden_rotations.py` | `rot_from_quat`: integer quaternion → exact rational rotation matrix (common-scale, no per-component denominators). | ledger |

### Search & campaign drivers
| file | purpose | principles |
|---|---|---|
| `exact_search.py` | Seed search; validate (axial=121, five=351) then count rationalized configs. `nohup`-friendly. | ledger |
| `run_campaign.py` | Parallel n=6 falsification campaign (shards → `campaign_results.jsonl`, ceiling watch). | `CPP_SPEC.md` |
| `run_campaign_n.py` | Same for any n (`--n K` → `campaign_n<K>.jsonl`). | `NPLUS_SPEC.md` |
| `phase_b_hillclimb.py` | Exact greedy hill-climb on integer quats (±1/±2 moves, \|c\|≤512), logs every eval. | ledger (P4) |
| `phase_b_hillclimb_n.py` | Hill-climb for general n. | `NPLUS_SPEC.md` |
| `golden_six.py` | Golden five + rational sixth cube search (found 681). | `golden_wall_report.md` |
| `golden_sweep.py`, `golden_sweep2.py` | Angle/parameter sweeps around the golden wall. | `golden_wall_report.md` |
| `multiwall_m1.py` | In-field (ℚ(√5)) stacked-wall search. | `MULTIWALL_SPEC.md` |
| `multiwall_m4.py`, `multiwall_m4_extend.py` | Rational double-wall construction (found 655). | `MULTIWALL_SPEC.md` |
| `slide3_p1.py`, `slide3_p2.py`, `slide3_p3.py` | Sliding-triple overlay search phases (grid → climb → alignment walls). | `SLIDE3_SPEC_V2.md` |
| `slide3_search.py` | Quaternion/overlay library for the slide3 drivers. | `SLIDE3_SPEC_V2.md` |
| `task_a_certify635.py` | Certifies 635 a local max (all ±1..±4 neighbor moves). | ledger (P5) |
| `task_c_deep_hillclimb.py` | Deep multi-restart climb (confirmed 635 plateau). | ledger (P5) |

### Analysis & checks
| file | purpose | principles |
|---|---|---|
| `breakdown.py` | Per-subset depth breakdown of a config (per-cube d1, per-pair d2, …). | ledger (P2–3) |
| `subset_analysis.py` | Subset-maximality analysis (are all k-subsets maximal?). | ledger (P2) |
| `mod4_check.py` | Tests the bounded ≡ 2n−1 (mod 4) parity law. | ledger |
| `pair_checks.py` | Pair-wall experiments (generic 4 vs wall 9/13). | ledger (P2) |
| `phase_c_analysis.py` | Campaign aggregate analysis (spectrum, ceilings, per-subset budgets). | ledger (P4) |
| `check_live_boundaries.py` | Standalone ceiling-violation scan over a seed range (read-only). | ledger (P4) |
| `scratch_census_n.py` | Bottom-diagram census measurement for general n. | `NPLUS_SPEC.md` |
| `scratch_gate_g1.py`, `scratch_gate_g2.py` | n>6 validation gates (G1 regression, G2 cross-check). Run with no args. | `NPLUS_SPEC.md` |
| `scratch_mod4_check_n.py` | mod-4 law at scale for general n. | `NPLUS_SPEC.md` |

### Infrastructure
| file | purpose | principles |
|---|---|---|
| `mt_sim.py` | Validated reimplementation of the seed→configuration RNG chain (numpy MT19937 + polar Gaussian + scipy quaternion order + common-scale rounding); the basis for the C++/JS ports. | `CPP_SPEC.md` |
| `make_seed_viewer.py` | Rebuilds the interactive seed-viewer artifact HTML from the logs. | ledger |

## Data logs (`.jsonl`)

One JSON object per line, each with the config's quats, `bounded` total,
and `by_depth` histogram (most also carry `per_label`).

- `exact_search_results.jsonl` — the original oracle ensemble (**read-only ground truth**).
- `campaign_results.jsonl` — n=6 campaign (≈278k configs).
- `campaign_n7.jsonl` (+ `*_shard_*`) — n=7 campaign.
- `hillclimb_log.jsonl` — Phase B climbs.
- `golden_search.jsonl`, `multiwall_search.jsonl`, `slide3_search.jsonl` — the three field/wall search programs.
- `campaign_shard_*.jsonl`, `campaign_n7_shard_*.jsonl` — transient per-worker shards (merged into the campaign files).

## Conventions

- **Exact only.** No floating point decides a region boundary. Rational
  rotations come from integer quaternions at a single common scale
  (cap 512); irrational configs use ℚ(√d) or a quadratic tower.
- **Validation gates before campaigns.** Axial fan of 6 cubes = 121;
  five-compound = 351; the C++ engine is checked against the Python
  oracle on 200 seeds with zero mismatches before any search is trusted.
- **Voxel counts cannot rank configurations** — a lesson learned twice;
  only exact counts settle anything.
- **Invariant comments.** Where the wrong alternative looks like an
  improvement, the source says why (e.g. common-scale rounding,
  coincident-plane ownership). Don't "simplify" those away.
