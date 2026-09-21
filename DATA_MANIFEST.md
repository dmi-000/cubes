# Which .json files are current, superseded, or wrong

Run data is IMMUTABLE — none of these files is edited to correct it, because the
original numbers staying derivable is what makes correcting safe. This manifest
is therefore the only place a reader learns that a file is superseded. Started
2026-08-17 after the ε-engine correction; **files not listed are UNAUDITED, which
is not the same as correct.**

## Incorrect — do not read

| file | status |
|---|---|
| `isolation67.json` | **WRONG for `golden`: 36 of 2 196 face counts misassigned**, reporting values 33, 34 and 35 that do not occur. Produced by the "halve until two consecutive steps agree" rule, which is unsound ([FAILURE_MODES 14](FAILURE_MODES.md), [P119](LEDGER.md#p119)). Its `octahedral` half is correct and identical to the current file. Superseded by `isolation67_eps.json`. |

**Note the shape of this one, because it is the general lesson.** The superseded
run advertises its own gaps — `isolation67_run1_fixed_eps.json` says
`unresolved: 333` — while the WRONG file reports `unresolved: 0` and looks
finished. The most trustworthy-looking artifact was the defective one.

## Superseded — kept as the record of what was measured when

| file | status |
|---|---|
| `isolation67_run1_fixed_eps.json` | Fixed ε ∈ {1/64, 1/256, 1/1024}; **333 of 2 196 golden faces unresolved**, honestly recorded as such. Superseded by `isolation67_eps.json`. |
| `ee_per_pair.json` | Correct as a count of edge-PAIR INCIDENCES, which is not what it is labelled. Its `max: 24` at `q = (0,1,1,1)` includes 18 incidences at two SHARED CORNERS — one `(3,3)` vertex contributes nine. The edge-edge VERTEX count there is 6. Superseded by `ee_bound_refute.json` ([P330](LEDGER.md#p330)). |
| `ee_total.json` | Correct as measured, but the search was SEEDED from `ee_per_pair.json`'s argmaxima, so `max_EE: 36` is evidence about the wrong quantity's maximisers. The bound it supports is false. Superseded by `ee_bound_refute.json` ([P330](LEDGER.md#p330)). |

## Current

| file | status |
|---|---|
| `isolation67_eps.json` | **Authoritative face counts for both 67s.** Infinitesimal ε, no step size. 728 + 2 196 faces, 0 unresolved, 0 budget rejects, both ISOLATED, best neighbour 63. |
| `dimension67.json` | First-order data for both 67s (walls, wall classification, candidate dim). Its octahedral facet counts 59, 53, 59, 53, 57, 63 were independently reproduced by the ε engine (`eps_gate.py`), and `candidate_dim` comes from a null space, not from stepping. |
| `dimension_gate.json` | ℚ(√d) port gate: rational path vs field path, agreeing exactly. |
| `ee_bound_refute.json` | **Authoritative on edge-edge counts.** Counts `(2,2)` ARRANGEMENT VERTICES — the quantity [P328]'s identity uses — and MEASURES each vertex's excess instead of tabulating it, so the identity closes by construction and the deviations from [P328]'s constants are reported. Gated against the n = 4, 5, 6 records (183, 393, 727). |
| `ee_audit.json` | The gates BEHIND `ee_bound_refute.json`, and behind [P330]'s own claims: [P329]'s 24 incidences resolved by LOCATION (6 singles + 2 corners x 9), the `(2,2)` counter agreeing with an independent edge-intersection enumerator on **all 1856 pairs, 0 disagreements**, and [P329]'s search pool shown to CONTAIN a violation (40 against a bound of 36), which refutes [P330]'s first explanation of the miss. |
| `members_*.json`, `census_run1/members_*.json`, `members_t*.json` | The all-members census, **split across two runs and disjoint** — run 1 (790 classes) is snapshotted in `census_run1/`, run 2 (`t` tag, 36 n=9 classes) is the 4-way re-shard of 2026-08-17. Glob both; there are no duplicate keys. |

**Standing caveat on the census files.** `status` (empty / nonempty) and
`lineality` come from `nullspace` + `variety_incremental` — algebra, no stepping,
so they do not share the ε defect. The `confirmed` / `unevaluable` / `changed`
counters DO: they step at fixed ε ∈ {1/64, 1/256, 1/1024}. A step that leaves the
intended cell usually reports a count ≠ base and lands in `changed`, so `changed`
is inflated; but if the wrong cell happens to match the base count the direction
is wrongly `confirmed`, so `confirmed` is **not** a strict lower bound either.
Re-measurable with the ε engine; not yet done.

## Unaudited

Mechanical inventory in [DATA_INVENTORY.md](DATA_INVENTORY.md) (generated).

`census_variety_[0-3].json` (299 records), `census_variety_redo.json` (26),
`census_variety2_*` (90), `census_variety3_*` (16), `census_variety4_*` (322) are
five successive generations. **Lineage established 2026-08-18** (delegated scan,
`census_variety_lineage.md`): order by mtime is gen0 -> redo -> gen2 -> gen3 ->
gen4, and **gen4 is canonical** — it contains all 299 gen0 records plus 23 more.
gen2 and gen3 are subsumed test runs. `census_variety_redo.json` is the
`GeneratorsNeeded` rerun ([P117](LEDGER.md#p117)) and uses an incompatible key
model (no `idxs`), so it cannot be merged mechanically.

**Four cross-generation disagreements, all gen0 vs gen4, all in `confirmed`:**
(9,4,147) 27->23, (9,5,341) 45->38, (9,5,347) 12->10, (9,6,677) 15->14. `status`,
`lineality` and `dirs` agree everywhere. That the divergence sits ENTIRELY in
`confirmed` is consistent with the standing caveat above — `confirmed` comes from
fixed-eps stepping, `status` and `lineality` from algebra. Which count is right is
NOT established; both may be valid under different validation criteria.

**RESOLVED 2026-08-18:** `census_variety_redo.json` holds 26 records where
[P117](LEDGER.md#p117) describes 23 reruns, and both are right. There are exactly
**23 distinct `(n,k,count)` keys**; three of them — `(7,5,385)`, `(8,5,385)`,
`(9,5,385)` — name TWO classes each, one of lineality 1 and one of lineality 2.
P117 counted CRASHES (keyed by `(n,k,count)`); the rerun evaluated every class
matching those keys. 23 of the 26 records have lineality 1, matching P117's "every
one of them lineality 1" exactly.

The cause is this project's recurring one: `(n,k,count)` is an equivalence by
INVARIANT, not by congruence, and this file carries no `idxs` field to
disambiguate — the same reason the members census had to run all 826 members
rather than 221 representatives. Nothing is missing or spurious, and no conclusion
depended on telling the colliding pairs apart: all 26 returned `empty` with
`dirs = 0`, so both members of each pair agree. Earlier text, retained: supersession had
NOT been established — and now cannot be established from source, which
`data_inventory.py` found on 2026-08-17 and is the more useful fact.
`census_variety.py` writes `census_variety4_%d.json` and nothing in the
repository writes generations 1, 2 or 3: **the script was edited in place for
each generation**. The output NAME was bumped every time, so the data survives
intact — but the code that produced it does not, so those numbers can no longer
be reproduced or even attributed to a known method. Data was preserved;
provenance was not. New campaigns should version the producer, not just its
output path. [P117](LEDGER.md#p117) records that 23 lineality-1 classes
crashed with `GeneratorsNeeded` and were rerun, so at least one generation
corrects an earlier one — but which file supersedes which is unverified, and is
stated as unverified rather than guessed. All other `.json` files in the
repository are likewise unaudited.

## `data/continuum_boundaries.json` — CURRENT (2026-09-08)

Measured boundaries of record count-plateaus and their extension regions
([P285](LEDGER.md#p285)–[P287](LEDGER.md#p287), [CONTINUUM_MAP.md](CONTINUUM_MAP.md)).
Three regions: the n=9 line, the n=6 727 arc, the n=4 183 (isolated).

**Every boundary is a BRACKET between two sampled parameter values, not an exact locus.**
The file says so in its own `IMPORTANT` field. It also carries one unresolved ANOMALY —
727 measured at `s = 10/3`, outside the extent MAXIMISERS documents — recorded as not
concluded rather than as a correction.

### `data/wall_keys.json` (2026-09-08)

Per named record, every distinct wall's **reconstruction key** —
`(frame, group, sig, c0)` — plus its gradient, the record quaternions, and the
record point. The key is the complete argument list of
`dimension.branch_numerator`, so the key *is* the polynomial; expanding it in
3(n−1) variables is a choice the reader makes, not something that had to be
stored. Written by `src/wall_keys.py`, which also provides `on_line` (Cayley
line) and `on_quat_line` (quaternion line — the form the project's brackets take).

n = 4..8 give 12 / 18 / 27 / 51 / 75 distinct walls, and arcA 20. `n4_183` is
recorded as **UNEVALUABLE, not skipped**: cube 1 is a half-turn, so the record is
at Cayley infinity and this chart has no point for it.

Gated by `P(record) == 0`, by two-route agreement between the gradient and the
polynomial's directional derivative, and by a corrupted-key negative control that
fires on every wall. That first gate found the `branch_numerator` defect of
[P288](LEDGER.md#p288); before the fix it failed on 6/27 at n = 6, 24/51 at
n = 7, 42/75 at n = 8, with every failure having two distinct cubes in its group.

Supersedes `data/record_walls.json` for reconstruction purposes. That file is
still the right one for tangent tests, and still carries the `nullspace_dim`
per record (1, 1, 1, 2, 3 at n = 4..8) which this one does not.

### Session of 2026-09-09 to 09-12 — the wall-solving campaign

| file | what it holds |
|---|---|
| `data/wall_polynomials.json` | **every wall on each 727 arc as an exact polynomial, with ALL real roots** — rational as fractions, irrational as minimal polynomial + isolating interval. Supersedes `arc_special.json`'s rational-only search, which reported 10/6/0/4 roots as "irrational, not testable"; one of arc D's ten was its own plateau boundary ([P296](LEDGER.md#p296)) |
| `data/plateau_1217.json` | the 1217 count plateau: two directions with brackets, the third wall (degree-4 curve) with its positions, both provenances, the walls crossed with NO count change, and the selective-inheritance measurements at n = 8 and n = 9 |
| `data/n10_measured.json` | n = 10's first measurement — 480 tight, 100 walls, rank 21, lineality 6, 2 045 s. Differs from P185 because that describes 3913, a superseded configuration |
| `data/arc_node_map.json` | the four 727 arcs: walls, lineality, variety per arc |
| `data/arc_special.json` | special points of the four arcs, by solving. Carries its own `n_unevaluated` and `n_irrational_roots_in_extent`, and its sampled sweep is labelled **POWER_IS_NEAR_ZERO** with the measurement that earned it |
| `data/arcD_control.json` | arc D at non-record parameters — the control that showed the node has one structural class |
| `data/fibre_boundary.json` | the 1217 plateau's extents in the fibre, by geometric-then-simplest-rational bracketing |
| `data/tangents_full.json` | full-ambient tangent search. **Its premise is refuted** ([P298](LEDGER.md#p298)); kept because the refutation is the result |
| `data/n9_region_map.json` | both n = 9 representatives, which agree on count and `by_depth` and differ on everything structural |
| `data/dihedral_family_map.json`, `data/golden_edge.json` | the 67↔67 family's five runs and the approach that put the golden 67 ON the 55/43 wall |
| `data/vertex_scale.json` | exact closest vertex pairs per level — the arrangement's minimum feature size |
| `data/concurrency_walls_n6.json` | the SECOND wall family: four face planes through a point, per ray, as exact interpolated polynomials with their roots ([P304](LEDGER.md#p304)). `degree_bound_failures` is the check that the degree bound held — 0. Roots are determinant zeros; a root is a genuine common point only where rank(normals) = rank(augmented) = 3, not checked individually |
| `data/wall_census_n6.json` | the wall census: every crossing on a ray, the count in each cell between crossings, and one verdict per attributable wall. **`constancy_failures` on ray e0 is 0 across 685 cells counted at three rationals each — the completeness check.** `spurious` marks roots of a branch active nowhere near them |
| `data/plateau_solve.json` | which tight walls the plateau can be shown to leave, per level, and the premise's own candidate space evaluated at solved points ([P305](LEDGER.md#p305)). n = 6 is the outlier: its lineality holds no record count at all |
| `data/plateau_arcs_n6.json` | the four 727 arcs as candidate plateau directions. **Only arc D passes through the record**; the A, B, C rows are void and the file's `parameters` block says so |
| `data/plateau_container_n6.json`, `data/plateau_face_n6.json`, `data/plateau_face_extent_n6.json` | the first-order container of the n = 6 plateau: the flat of the 20 walls arc D keeps, rank 13, dimension 2; unchanged by adding the concurrency family; face left at λ = 763/3124 exactly |
| `data/plateau_leading_n6.json`, `data/plateau_decider_n6.json` | **the decider** ([P306](LEDGER.md#p306)): 486 quadruples change leading behaviour off arc D, of which **222 are genuine** (rank 3 = rank augmented) and 264 are parallel-pair degeneracies with no common point. Those 222 contain the arc and pin the plateau to dimension exactly 1 |
| `data/plateau_sector_n6.json` | **SUPERSEDED.** Its first cell was built from coincidence roots only — ungated and ~200× too wide, so it reported a distant cell's count as local. Kept because P306's reasoning quotes it |
| `data/plateau_order.json` | plateau dimensions settled at n = 6, 7, 8 as **1, 2, 2** by order of vanishing ([P307](LEDGER.md#p307)). Every level carries a `SCOPE` field naming the seeds — a dimension here is the branch through those directions, and seeding n = 7 from the lineality alone returns 1 instead of 2 |
| `data/attribution_audit_n8.json`, `data/boundary_cause_n7.json` | the attribution audit ([P308](LEDGER.md#p308)): the recorded boundaries are caused by coincidence conditions, and n = 7's are re-derived from both families to 0.002550224044 and 0.049672585064, matching the recorded values digit for digit |
| `data/VOID_2026-09-12_concurrency_walls_n6_transposed_planes.json`, `data/VOID_2026-09-12_wall_census_n6_transposed_concurrency.json` | **VOID, kept not deleted.** Produced with face normals taken as the ROWS of the rotation instead of the COLUMNS, i.e. the plane set of a different configuration ([FAILURE_MODES 39](FAILURE_MODES.md#39)). Every concurrency number in them describes that other object. Retained so the corrected entry's claims about what was wrong stay checkable |

**EVERY FILE MUST SAY HOW IT WAS MADE (convention, 2026-09-13).** Each `.json` written from
now on carries a `reproduce` block: the exact command line, the script and its **SHA-256**,
the declared parameters, the engines with their hashes, library versions, and the input files
consumed. There is no git here, so the hash IS the version — it is what distinguishes a file
written by today's `concurrency_walls.py` from one written before the plane-convention fix
([P304]), which no timestamp could. Paths are relative, never absolute and never a hostname,
because these files are quoted in published documents. `src/provenance.py` emits the block;
`PROV.stamp(parameters=vars(args))` is the whole call.

The eleven files from 2026-09-12/13 were stamped RETROSPECTIVELY from the session record and
say so in the block; everything later is emitted by the script itself. Files older than that
have no block, and reconstructing their parameters means reading the ledger.

**Probe scripts live in `src/probes/`, not in scratch.** Nine of this session's data files
were written by throwaway scripts in a temp directory — the exact failure the deliverables
rule names, since the file survives and the thing that made it does not. They are now in the
repository under the names their `reproduce` blocks cite.

**Read the caveat fields.** Several of these carry `IMPORTANT`, `CAVEATS` or
`POWER_IS_NEAR_ZERO` keys recording what the measurement does not cover; those were
written at the time and are load-bearing.

**One unprovenanced file, 2026-09-19.** `data/ee10_family_triples.json` was written by an
ad-hoc `python3 -c` before the probe existed, so it carries no `reproduce` block. It is
**superseded by `data/ee10_triples.json`**, which is the same enumeration run from
`src/probes/ee10_triples.py` with provenance: 336 family members, 54 432 triples, max
`sum EE = 26` at `E_S = 32` — identical numbers, a different tie-broken witness. It is kept
rather than deleted because it is a run's output ([METHODS]: data is immutable), and flagged
here because an unstamped file in `data/` is otherwise indistinguishable from a stamped one.
