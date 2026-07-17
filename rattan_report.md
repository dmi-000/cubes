# RATTAN — the rational-tangent sweep (RATTAN_SPEC.md)

Sweep of the single-axis cube family at RATIONAL-TANGENT tilts
tan ψ = q/p with d = p² + q² **non-square** (sin ψ, cos ψ irrational, in
√d·ℚ), phases parametrized by rational points on the conic
c² + d·s′² = 1 — the slice Postscript 27 identified as where the
records' family structure actually lives, and which every prior
(Pythagorean-tilt) sweep was structurally blind to. Code:
`rattan_sweep.py`; raw log `rattan_results.jsonl`. Engine:
`./cube_regions_n` (read-only); Python oracle
`certify_six.exact_count_config` for all gate/record checks. Never
edits `six_cube_search_results.md` or any validated file.

**Record-claim status: FLAG — record-EQUAL, non-congruent structures
found (no record BEATEN anywhere in this campaign).** Tier 3 (393's
five ledger cubes fixed + swept 6th integer quat, ‖q‖² ≤ 600) produced
**28 distinct 6th-cube completions all counting exactly 723**, every
one immediately re-verified with the Python oracle
(`certify_six.exact_count_config` agrees exactly on total and depth in
all 28 cases). They fall into **4 distinct depth profiles, 7 hits
each**:

| d1 | d2 | d3 | d4 | d5 | d6 | note |
|----|----|----|----|----|----|------|
| 210 | 216 | 164 | 96 | 36 | 1 | = ledger 723 profile (incl. the known (5,2,2,2)) |
| 210 | 218 | 160 | 98 | 36 | 1 | **non-congruent tie** |
| 210 | 220 | 156 | 100 | 36 | 1 | **non-congruent tie** |
| 210 | 222 | 152 | 102 | 36 | 1 | **non-congruent tie** |

A different depth histogram proves non-congruence outright (congruent
compounds have identical histograms). Example non-ledger-profile 6th
quats: (11,11,10,11) (norm 463 — not any cube-symmetry multiple of
(5,2,2,2), norm 37), (3,−4,−3,3), (5,−5,5,4). Conservation across all
four profiles: d1, d5, d6 fixed at (210, 36, 1) and **d2+d3+d4 = 476
constant**, with (d2,d4) stepping in lockstep (+2,+2) and d3 paying −4
— the Postscript-11-addendum shallow-tail tradeoff appearing as an
exact three-layer exchange inside a record plateau. Raw hits:
`rattan_results.jsonl`, kind `393five+6th-intquat`, total 723. Main
session records any ledger postscript; this file never edits the
ledger.

## Gates — ALL PASS (run 2026-07-17, `rattan_sweep.py --gates-only`)

### G0 (conic parametrization: round trip + closure) — PASS

Implementation `ConicAngle` (all `fractions.Fraction`, no floats):
point (c, s′) on c² + d·s′² = 1 with c = cos Δ, s′ = sin Δ/√d formally;
`from_t` is the stereographic parametrization c = (1−dt²)/(1+dt²),
s′ = 2t/(1+dt²); `to_t` inverts via t = s′/(1+c). Verified exactly at
d=13 for t ∈ {1/7, −3/11, 5, 0, 2/3}: conic equation holds, round trip
t → (c,s′) → t is the identity. Closure under angle addition: the ring
product (c₁c₂ − d·s′₁s′₂, c₁s′₂ + c₂s′₁) of norm-1 elements of
ℚ(√−d) equals the direct parametrization of the conic group law
t₁ ⊕ t₂ = (t₁+t₂)/(1 − d·t₁t₂) — checked exactly (t₁=2/5, t₂=−3/7 →
t=−1/113, both paths identical). Rel(Δ(t), ψ) built via
`rel_matrix_conic` — the Rodrigues form with cos ψ = p/√d,
sin ψ = q/√d, sin Δ = s′√d substituted; every entry rational because
every odd power of √d in a sin ψ/cos ψ factor pairs with the odd power
in sin Δ and cancels:

    Rel[0][0]=(c·p²+q²)/d  Rel[0][1]=pq(1−c)/d  Rel[0][2]=p·s′
    Rel[1][1]=(c·q²+p²)/d  Rel[1][2]=−q·s′       Rel[2][2]=c

exactly the spec's checklist. `is_rotation_exact` + integer-quaternion
round-trip (`matrix_to_int_quat`, which asserts M → quat → M identity)
pass on every generated matrix.

### G1 (the sharp gate: 393's own 4-clique is IN the sweep space) — PASS

The 393 record `4,1,1,-1; 3,3,7,3; 5,-1,-5,-5; 2,1,1,1; 1,1,1,1`
(cubes indexed 0–4): its unique single-axis 4-clique is cubes
{1,2,3,4}, axis (3,2,0), tan ψ = 2/3, d = 13 (Postscript 27). Method:
fix cube **2** as the unlabeled base (Q_base = I; empirically the
clique's own internal gauge puts the base at index 2, not index 1 —
with any other base the axis witnesses land on permuted axes like
(2,−5,0)/(2,0,3) instead). For each other clique member k ∈ {1,3,4},
search the 24-element cube rotation group for the relabeling Q_k such
that Rel-form holds (Rp[1][0] = Rp[0][1]) AND the recovered world axis
(mapped through M_base) is exactly (3,2,0). The consistent sign gauge
is (p,q) = (3,−2) (still tan ψ = 2/3; q's sign flip is the
handedness of the local ψ-frame relative to the oriented axis).

Recovered exact conic angles (all on c² + 13s′² = 1, all round-trip
through the t-parametrization exactly):

| cube | c = cos Δ | s′ | t |
|------|-----------|-----|-----|
| 2 (base) | 1 | 0 | 0 |
| 1 | −289/361 | −60/361 | **−5/6** |
| 3 | −101/133 | 24/133 | **3/4** |
| 4 | 6/19 | −5/19 | **−1/5** |

Cross-check with NO further search (this is what makes it a proof of
mutual consistency, not three independent pair matches): the three
pairs not involving the base — (1,3), (1,4), (3,4) — computed directly
as N_j^T N_k, match the conic-group-law predictions Δ_jk = θ_j ⊖ θ_k
**exactly** (e.g. pair (1,3): c = 29/133, s′ = 36/133 both ways).
The t-denominators are 6, 4, 5 — comfortably inside the Farey-40 phase
menu. **The sweep space provably contains the record's clique.**

### G2 (two-engine agreement on rational-tangent configs) — PASS

- n=4, tan ψ = 2/3 (d=13), phases t = (0, 1/3, −2/5, 4/7):
  quats `(1,0,0,0),(3,2,3,0),(−5,4,6,0),(7,8,12,0)` → C++ and Python
  oracle agree exactly: total 161, depth {1:74, 2:62, 3:24, 4:1}.
- n=5, tan ψ = 2/5 (d=29), phases t = (0, 1/4, −3/8, 5/11, −1/6):
  quats `(1,0,0,0),(4,2,5,0),(−8,6,15,0),(11,10,25,0),(6,−2,−5,0)` →
  agree exactly: total 313, depth {1:92, 2:110, 3:80, 4:30, 5:1}.

### G3 (reproduce 723 from ledger quats) — PASS

`4,1,1,-1;3,3,7,3;5,-1,-5,-5;2,1,1,1;1,1,1,1;5,2,2,2` → 723,
depth {1:210, 2:216, 3:164, 4:96, 5:36, 6:1}, exactly the ledger.

## Bonus verification: 183's triply-resonant triple re-derived

Independent exact re-derivation (own witness search via
`find_clique_chain`, not copied from glue_q0.json): 183's cubes
{0,2,3} are simultaneously a conic-chain on all THREE axes:

| axis | d | tan ψ | t-values (cube0 base) |
|------|---|-------|------------------------|
| (2,−3,0) | 13 | 2/3 | t₂ = 1/5, t₃ = −1/5 |
| (3,5,0) | 34 | 3/5 | t₂ = 1/2, t₃ = −1/2 |
| (5,2,0) | 29 | 2/5 | t₂ = −1/3, t₃ = 1/3 |

Note the ± symmetry: in every one of the three resonances the two
non-base cubes sit at OPPOSITE conic phases. The record triple is not
just on three axes at once — it is a symmetric antipodal pair about
cube 0 in all three parametrizations simultaneously.

## Record protocol

Any total > record (183/393/723), or = record: re-verify immediately
with the Python oracle (`certify_six.exact_count_config`); if
confirmed, flag at the TOP of this report and in the run log. For
= record hits, pairwise invariants (exact edge-crossing counts +
family-axis tests, `nfamily_common`) decide congruence before any
claim of a "new" structure. `six_cube_search_results.md` and validated
files are never edited by this campaign.

## Sweep design

- **Tilt menu**: all coprime (p,q), p,q ≤ 15, d = p²+q² non-square,
  ordered records-first: (3,2) d13, (5,2) d29, (5,3) d34, then by d.
  Pythagorean q/p values from the spec's illustrative list (3/4, 5/12)
  are intentionally dropped — d square means rational sine, i.e. the
  already-swept nfamily locus.
- **Phase menus**: Farey t-values a/b; b ≤ 12 (93 values) for the
  dense chain pass, b ≤ 40 (981 values) for random tuples and the
  targeted completions.
- **Tier 1** chains θ_k = k·Δ(t): tilts × t (small menu) × n ∈ {4,5,6}.
- **Tier 2** random independent phase tuples over the full menus.
- **Tier 3** (the targeted shot): (a) 393's exact clique t-values
  (0, −5/6, 3/4, −1/5) + 5th conic phase over the full menu; (b) the
  literal ledger 4-clique quats + 5th cube as a random integer
  quaternion (‖q‖² ≤ 600 — how 393's own off-axis cube 0 is built);
  (c) 393's five ledger cubes + 6th (contains 723 — re-find check
  included); (c′) 393's five + 6th ON the (3,2,0)-axis via
  M₆ = M_base·Rel(Δ(t),ψ); (d) 183's triple + 4th cube, both as
  integer quats and as conic phases on each of the three axes.
- **Tier 4**: hill-climb (t-perturbations to Farey neighbors) around
  the per-n bests, multi-round.

Everything below this line is appended by the running sweep.

---
## Interim findings (smoke-scale run, 2026-07-17, appended while the full sweep is being launched)

- Tier-3(a) — 393's exact 4-clique (t = 0, −5/6, 3/4, −1/5 on axis
  (3,2,0), tan ψ = 2/3) + a 5th conic phase on the SAME axis — already
  yields **n=5 total 387** (depth {1:148, 2:130, 3:78, 4:30, 5:1}) at a
  plateau of 5th-cube phases t₅ ∈ [~8/39, ~3/14] (many Farey values in
  that interval give the identical count/profile — an open cell in
  t-space). **This beats the glue campaign's best 385 and BREAKS the
  "exactly −8" deficit floor at n=5: deficit is now −6.**
- The 393 clique alone counts **179 at n=4** (depth {1:92, 2:62, 3:24,
  4:1}) — only −4 below the 183 record; independently, the
  reconstructed conic chain (0, −5/6, 3/4, −1/5) reproduces exactly the
  same total and profile as the literal ledger clique quats, an
  end-to-end validation of the G1 gauge reconstruction.
- 723's 6th cube (5,2,2,2) is NOT in family position relative to the
  {1,2,3,4}-clique base (exact test: Rel-form fails) — the 6th record
  cube lives off this axis, like 393's cube 0.
- Chain tier interim bests: n=4: 175, n=6: 671 (both tan ψ = 2/3
  chains) — chains alone don't reach the records, as expected.

## Run 1 (tier-1/2 pilot + FULL tier-3 targeted completion) — complete

17,080 exact configs in `rattan_results.jsonl` (chains: 5 tilts x
Farey-12; random: 50/n pilot; tier 3 at full spec scale: 4,000 int-quat
completions per record base + full Farey-40 on-axis sweeps). Summary:

| n | best | record | deficit | how |
|---|------|--------|---------|-----|
| 4 | **183 = record (re-find)** | 183 | 0 | 183's triple {0,2,3} + 4th int quat |
| 5 | **387** | 393 | **−6** | 393's 4-clique + 5th on-axis conic phase |
| 6 | **723 = record (28 ways, 4 profiles)** | 723 | 0 | 393's five + 6th int quat |

- **n=4 re-find**: completing 183's own triple {0,2,3} with a swept 4th
  integer quat re-found the record: 4th cube (1,−1,−1,4), total 183,
  ledger depth profile {92,66,24,1}, oracle-confirmed. Main session
  verified congruence to the ledger 183: (1,−1,−1,4) right-multiplied
  by cube symmetry (0,1,−1,0) equals the ledger's (0,5,3,2) — a
  RE-FIND, not a new structure (recorded in ledger Postscript 29).
- **n=5 387** (deficit −6, breaking the glue campaign's "exactly −8"
  floor): oracle-verified by main session, recorded in Postscript 29.
  The 4-clique base is EXACT (G1's t-values); the 5th cube sits on the
  same axis at any t₅ in an open plateau [≈8/39, ≈3/14].
- **n=6 explicit re-find check**: 393's five + the known (5,2,2,2) 
  counts 723 with the exact ledger profile — CONFIRMED in-run.
- **The 723 tie plateau**: see flag at top. 28/4,000 random 6th-cube
  int quats tie the record exactly; none beat it. The completion
  space's summit is a plateau at exactly 723 with at least 4
  non-congruent realizations, and the three non-ledger profiles obey
  the exact exchange (d2,d3,d4) = (216+2k, 164−4k, 96+2k), k=0..3.
- 183-triple on-axis 4th-cube sweeps (all three resonant axes, full
  Farey-40) topped out below the int-quat completions — the 4th record
  cube needs to be off-axis, exactly like 393's cube 0 and 723's cube 5.

### P1: exact t5 plateau at 387: ['3/14', '4/19', '5/24', '6/29', '7/33', '7/34', '8/39'] (checked all Farey-40 in [8/39, 3/14])


## Phase 2 (targeted completions, seed 777001) -- started 2026-07-17 07:16

### P1: exact t5 plateau at 387: ['3/14', '4/19', '5/24', '6/29', '7/33', '7/34', '8/39'] (checked all Farey-40 in [8/39, 3/14])

### The 723 completion plateau, resolved into cube positions

Exact cube-symmetry classification (M6·S == M6′ over the 24-element
group) of the 28 tie hits: they represent **25 distinct 6th-cube
positions** (plus the ledger's own (5,2,2,2) = 26), none of them a
cube-symmetry copy of (5,2,2,2) — even the 6 random hits with the
LEDGER depth profile are genuinely different positions with the same
histogram. Breakdown: ledger profile {216,164,96}: 5 new positions;
{218,160,98}: 7; {220,156,100}: 7; {222,152,102}: 6. The 393-record's
completion summit is a broad plateau of at least 26 distinct positions
all landing on exactly 723, in at least 4 depth-histogram classes —
strong evidence the 723 value itself is a structural ceiling of this
completion space rather than an isolated optimum (cf. the exactly-−8
deficit story: whatever bounds the glued/family configs at record−8
appears here as a hard flat top at the record for off-axis completion
of the record's own 5-base).

phase2 progress 50/240 shards, best: n=4:183, n=5:387, n=6:719
phase2 progress 100/240 shards, best: n=4:183, n=5:387, n=6:719
phase2 progress 150/240 shards, best: n=4:183, n=5:387, n=6:719
phase2 progress 200/240 shards, best: n=4:183, n=5:387, n=6:719

### Phase 2 final

| n | best (phase 2) | record |
|---|-----------------|--------|
| 4 | 183 | 183 |
| 5 | 387 | 393 |
| 6 | 721 | 723 |
