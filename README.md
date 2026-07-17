# Cube-compound region counting

Exact enumeration of the bounded 3D regions formed by compounds of *n*
congruent, concentric unit cubes (each the cube [−1,1]³ under a rotation
Rₖ ∈ SO(3)). "Exact" means no floating point in any decision: every
region count is computed with rational or algebraic (ℚ(√d), and towers
ℚ(√a,√b)) arithmetic and certified predicates, so a reported count is a
theorem about that configuration, not a numerical estimate.

The scientific record lives in **`six_cube_search_results.md`** (read its
postscripts in order — several early conclusions were overturned by exact
counting and the corrections matter). For the narrative synthesis — the
problem, the methods, the record chain, and the structural laws — read
**`PROJECT.md`**. This README is the map of the code and documents around
it.

## Current records (all exact)

| n | best bounded regions | configuration | field |
|---|---|---|---|
| 2 | 13 | 60° about a shared body diagonal (confirmed max) | ℚ (rational) |
| 3 | 67 | octahedral 3-compound = golden 3-subset (confirmed max) | ℚ(√2) / ℚ(√5) |
| 4 | **183** | wide-perturbation climb; golden 177 beaten | ℚ (rational) |
| 5 | **393** | 5-subset of the 723 record; golden 351 beaten | ℚ (rational) |
| 6 | **723** | C₃-orbit-of-3 + 3 free cubes, shared (1,1,1) axis | ℚ (rational) |
| 6 | 717 | D₂-orbit-of-4 + free + axis-aligned cube | ℚ (rational) |
| 6 | 705 | two 3-fold triples on shared (1,1,1) axis | ℚ (rational) |
| 6 | 699 | two 3-fold triples (earlier record) | ℚ (rational) |
| 6 | 681 | golden five + sixth on the (1,1,1) wall | ℚ(√5) |
| 6 | 655 | two 60°-body-diagonal pair walls, constructed | ℚ (rational) |
| 6 | 635 | best from 360k random rational seeds + climbing | ℚ (rational) |
| 7 | **1207+** | greedy extension of 723; certified vs climb+blueprints | ℚ (rational) |
| 8 | **1879+** | greedy extension of 1207 (first n=8 config) | ℚ (rational) |

Deep-depth ceilings **d3 ≤ 164, d4 ≤ 102, d5 ≤ 36, d6 = 1** have never
been exceeded in any config or on any wall tested (conjectures C4/C5/C6,
with a proof program in `C45_notes.md`). The 723 record has depth
histogram {1:210, 2:216, 3:164, 4:96, 5:36, 6:1} — it buys total by
lowering depth-4 below its ceiling. See Postscript 12 for its quaternions.

**The dihedral family (Postscripts 25–26)**: a closed-form one-parameter
family of 3-cube compounds (cube ± its 120° rotations about an
in-face-plane axis) has *both* n=3 records as special points — octahedral
at ψ=arcsin(1/√3), golden at tanψ=φ² — plus a new exactly-certified
ℚ(√6) point at ψ=45° counting **49** = {30,18,1} (not a record; a
plateau *minimum*, not a maximum). Generalized to n cubes, the family by
itself tops out below the records (175/335/615 at n=4/5/6, vs. 183/393/
723), but every record turns out to be built almost entirely from family
*pairs* glued across different axes (183: 6/6 pairs; 393: 10/10; 723:
12/15). Four theorems about the family (mirror symmetry, 90° periodicity,
the coincidence identity, and a rational/irrational obstruction) are
proved in `C45_notes.md` §12. Full story in `PROJECT.md` §7 and the
ledger's Postscripts 25 (+4 addenda) and 26 (+1 addendum).

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

**Interactive viewer.** `depth_explorer.html` is a single self-contained
file (no dependencies, no build, no network) — open it in any browser to
explore a compound: a depth-coloured draggable cross-section, a rotatable
depth point-cloud, depth/cube filters, octahedral (√2) and golden (√5)
presets, and rings marking where 4+ face-planes meet (gold = corner
coincidence, blue = edge crossing). Accepts 2–8 cubes as integer
quaternions or as decimal rotation matrices (so √n configs load directly).
An **opaque surface mode** renders the compound's faces as solid, shaded,
depth- or containment-coloured polygons instead of a point cloud, with
live highlighting of exactly the faces currently splitting or merging,
mouse-wheel zoom, and one-sided clipping against the cross-section plane.
The old "67 ↔ 67 slide" has been **replaced** by a **dihedral-family
slider** (ψ from 0° to 90°, named tick marks including mirror-golden, a
live ghost/near-miss counter, and a "maintain concurrences" lock) that
traces the exact-coincidence family of Postscripts 25–26 instead of the
old slide's near-miss ghost gaps. Also hosted:
https://claude.ai/code/artifact/044d34a6-3f36-43b2-9ec8-17fb5691c87c

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
| `six_cube_search_results.md` | **ledger** | The authoritative project record. Postscripts 1–21: exact-count corrections to the voxel era, subset maximality, the C++ campaign, the 635→…→717→723 record chain, the ℚ(√5)/tower field program, the sliding-3-cube result, and the symmetry-stratified sweep. Postscripts 22–24: n=7/n=8 records (1207, 1879), the cap-sum-tight proof route for n=2/3, and the first proved theorem (the anchor lemma). Postscripts 25 (+4 addenda) and 26 (+1 addendum): the dihedral family — its closed-form discovery, the persistent 18-core and corner docking, the exact region-count staircase (including the new ℚ(√6) point, 49), the handoff-chase verdict, and the n>3 finding that records are gluings of family cliques. Start here. |
| `C45_notes.md` | notes | Proof program for the deep ceilings (d3≤164, d4≤102, d5≤36) via the radial-escape lemma and bottom-diagram census (T1 Euler count + T2 semicontinuity). §10: the proven anchor lemma. §12: four proved theorems about the dihedral family (mirror symmetry, 90° periodicity, the coincidence identity, and the rational-invariant obstruction with its n=3-is-the-unique-irrational-level corollary). |
| `nfamily_report.md` | report | Executes `NFAMILY_SPEC.md`: does the dihedral family help at n>3? Answer: not as a search space on its own (175/335/615 vs. records 183/393/723, growing deficit) — but every record is a gluing of family-position pairs (183: 6/6, 393: 10/10, 723: 12/15), which reframes the record search as a search over clique gluings. |
| `handoff_report.md` | report | Executes `HANDOFF_SPEC.md`: chases whether more than the dihedral family's persistent 18 edge concurrences can be carried continuously from the octahedral 67 to the golden 67. Verdict: no path found beyond 18; a specific local obstruction (two extra-coincidence curves grazing the same ψ=45° wall ~70° apart in phase) is identified and described, not a proof of a ceiling. Also corrects an earlier "60 total contacts" figure for golden (correct: 18 interior + 54 corner label-pairs, 24 distinct physical points). |
| `dihedral_slider_report.md` | report | Executes `DIHEDRAL_SLIDER_SPEC.md`: replaces the viewer's old "67↔67 slide" with a slider along the dihedral family, plus four rounds of follow-up from live feedback — a core-aware "maintain concurrences" lock, track tick marks (field points + exact region-count transitions), split/merge surface highlighting, zoom, and one-sided opaque clipping. |
| `opaque_report.md` | report | Executes `OPAQUE_SPEC.md`: adds the opaque surface rendering mode to the viewer (each cube face split into its true convex pieces by every other selected cube's planes, depth- or containment-coloured, painter's-algorithm sorted), with a full gate suite (membership audits, ray audits, regression checks). |
| `DIHEDRAL_FAMILY_NEXT.md` | handoff | Task list for continuing the dihedral-family work (region-count sweep, second-engine verification, formalizing the coincidence theorem, extending to n>3, the viewer preset) — the source of the task numbering referenced by the reports above. |
| `NFAMILY_SPEC.md`, `HANDOFF_SPEC.md`, `DIHEDRAL_SLIDER_SPEC.md`, `OPAQUE_SPEC.md` | specs | Working-principles docs for `nfamily_report.md`, `handoff_report.md`, `dihedral_slider_report.md`, `opaque_report.md` respectively. |
| `GLUE_SPEC.md`, `RESONANCE4_SPEC.md` | specs | **In progress, no report yet.** `GLUE_SPEC.md`: does gluing dihedral-family cliques on different axes beat 723 (the reframing Postscript 26 motivates)? `RESONANCE4_SPEC.md`: an algebraic solve for whether the n=4 record has an irrational family "resonance" point analogous to the n=3 67s. Neither is claimed to have produced a result yet. |
| `CPP_SPEC.md` | spec | Design of the C++ engine: integer-homogeneous coordinates, int128 predicate budget, seed chain, validation gates. Working-principles doc for `cube_regions.cpp`. |
| `NPLUS_SPEC.md` | spec | Generalization of the engine and campaigns to n>6 (`--n K`). Working-principles doc for the `*_n.py` and `scratch_*_n.py` drivers. |
| `QFIELD_SPEC.md` | spec | Extend the search from rational rotations to ℚ(√d) (and the ℚ(√3,√5) tower). Field/wall taxonomy. |
| `MULTIWALL_SPEC.md` | spec | Multi-constraint ("stacked wall") search + tower verification. Working-principles doc for `qtower.py` and `multiwall_*.py`. |
| `SLIDE3_SPEC.md` | spec (V1) | Original plan for overlaying two sliding 3-cube triples. Its section 0 family is **superseded** by V2 (kept for the record). |
| `SLIDE3_SPEC_V2.md` | spec | Corrected sliding-3-cube family (common 3-fold axis; congruence up to octahedral self-symmetry). Working-principles doc for `slide3_*.py`. |
| `golden_wall_report.md` | report | Results of the ℚ(√5) golden-wall pilot (found 681). |
| `multiwall_report.md` | report | Results of the multi-constraint / tower search (found rational 655; explained the (1,1,1) wall). |
| `slide3_report.md` | report | Sliding-3-cube results: section 0 = V1 (family disproven), `## V2` = corrected family and the 699 record. |
| `ALGEBRAIC_SEARCH.md` | spec+report | The algebraic (not numeric) search: solves incidence equations symbolically (Wolfram) — 1-parameter exact wall-mapping and multi-constraint GroebnerBasis solving — then counts each config exactly. Records live at high-multiplicity *point* concurrences (coincident corners = shared axes), with a 9-fold sweet spot. Working-principles doc for `algebraic_search.wl`, `algebraic_demo.wl`, `algebraic_groebner.wl`, `algebraic_groebner2.wl`, `algebraic_bridge.py`, `cad_probe_n2.wl` (CAD feasibility probe; verdict in C45_notes §11). |
| `PROJECT.md` | write-up | Narrative synthesis of the whole project — problem, methods, the record chain, the structural laws, and open problems. Read this for the story; read the ledger for the primary record. |
| `JOURNEY.md` | informal account | The story of the project — discoveries, surprises, corrections, the frustration principle and ceiling law, and an honest description of the human/frontier-model/agent/tool collaboration. Self-contained, with a reproduce-it-yourself section. Start here for the most readable entry point. |

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
| `q3_count.py` | ℚ(√3) field + counter, a field-constant clone of `slide3_q2.py`; counts Pythagorean-angle dihedral-family members exactly. | `DIHEDRAL_FAMILY_NEXT.md` |
| `q6_count.py` | ℚ(√6) field + counter, same clone pattern; counts the ψ=45° face-diagonal family point (49 = {30,18,1}). | `DIHEDRAL_FAMILY_NEXT.md` |
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

### Dihedral family (n>3 generalization)
| file | purpose | principles |
|---|---|---|
| `nfamily_common.py` | Exact core: closed-form `Rel(Δ,ψ)` Rodrigues rotation (relative rotation between any two family members, depends only on their phase difference and ψ), square-root-free integer-quaternion extraction, exact edge-crossing counter, the family-membership axis test used to analyze records. | `nfamily_report.md` |
| `nfamily_gates.py` | The three validation gates (exact round-trip, two-engine agreement, record reproduction) for the n-cube family machinery. | `nfamily_report.md` |
| `nfamily_sweep.py` | Sweep driver (chains, random phase tuples, neighbor-hillclimb rounds) that produced the n=4/5/6 family maxima (175/335/615). | `nfamily_report.md` |
| `nfamily_q3_records.py` | Checks every pair of every record (183/393/723) and the n=3 octahedral witness for family membership (183: 6/6 pairs, 393: 10/10, 723: 12/15). | `nfamily_report.md` |
| `dihedral_scratch/` | Exploration and verification scripts from the dihedral-family work: the original numerical discovery path, persistence/docking checks, the pair-curve identity, the corner-handoff linker and gates (`handoff_*.py`), and more. Read-only exploration history, not a maintained library. | `DIHEDRAL_FAMILY_NEXT.md`, `HANDOFF_SPEC.md` |
| `glue_search.py` | **In progress.** Two-clique gluing search (does gluing dihedral-family cliques on different axes beat 723?). No report yet — see `GLUE_SPEC.md`. | `GLUE_SPEC.md` |

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
- `nfamily_results.jsonl` — the n=4/5/6 dihedral-family sweep (9,218 exact configs: chains, random phase tuples, hill-climb rounds).
- `nfamily_q3_records.json` — the pairwise family-membership analysis of the 183/393/723 records and the n=3 octahedral witness.

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
