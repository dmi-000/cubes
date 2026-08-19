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

## Current

| file | status |
|---|---|
| `isolation67_eps.json` | **Authoritative face counts for both 67s.** Infinitesimal ε, no step size. 728 + 2 196 faces, 0 unresolved, 0 budget rejects, both ISOLATED, best neighbour 63. |
| `dimension67.json` | First-order data for both 67s (walls, wall classification, candidate dim). Its octahedral facet counts 59, 53, 59, 53, 57, 63 were independently reproduced by the ε engine (`eps_gate.py`), and `candidate_dim` comes from a null space, not from stepping. |
| `dimension_gate.json` | ℚ(√d) port gate: rational path vs field path, agreeing exactly. |
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
