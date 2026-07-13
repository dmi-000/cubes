# Spec: generalize the exact search to n > 6 intersecting cubes

Hand to an implementation agent ONLY after the current agent finishes
(both touch cube_regions.cpp). Read CPP_SPEC.md and Postscripts 3-5 of
six_cube_search_results.md first; this spec extends them.

## 1. Engine generalization (cube_regions.cpp)

- Add `--n K` (default 6, support 2..12). Everything scales: 6K planes,
  labels become uint64 bitmasks (K <= 12 keeps per_label maps sane; for
  K > 8 emit per_label sparsely, nonzero entries only).
- Seed chain: `Rotation.random(K, random_state=seed)` generalizes as-is
  (K*4 gaussians in row-major order, then per-cube sign-fix/round/gcd —
  mt_sim.py's sim_quats already takes n; port the K parameter).
- Overflow budget is UNCHANGED (predicates involve one plane and one
  vertex; K only multiplies counts, not magnitudes). Quaternion scale
  stays 512.
- Expected scale: cells grow ~ (6K choose 3)-ish truncated; K=7 was
  ~8k cells in Python (~11 s); C++ should be well under 1 s. K=10
  a few seconds. Memory trivial.

## 2. Validation gates (hard, before any campaign)

- G1regression: `--n 6` must still reproduce the 200-seed oracle
  (exact_search_results.jsonl) with zero mismatches — the
  generalization must not perturb n=6.
- G2cross: for n in {2,3,4,5,7,8}, three seeds each: C++ output must
  equal the Python oracle `certify_six.exact_count_config` (it already
  handles any n; k=7 seeds 777/778/779 are known: 973, 993, 873).
  Match counts AND depth histograms.
- G3: axial selftest still passes; timing report per n.

## 3. Campaign framework (run_campaign.py generalization)

- `--n` passthrough; per-n logs campaign_n<K>.jsonl (n=6 keeps
  campaign_results.jsonl for continuity).
- Reproducibility protocol unchanged: config identity = (n, seed) or
  explicit quats; every record logged with quats.

## 4. Science targets per n (what the searches are FOR)

- Record table max(n): known certified points: n=2: 4 generic (13 on
  the shared-diagonal wall), n=3: 67 (golden; 38+ random), n=4: 177
  (golden four-cube compound; 135+ random), n=5: 317+ (golden 351
  is a wall config), n=6: 635, n=7: 993+ (3 seeds only). Fit growth;
  hill-climb each n like n=6.
- Depth-structure freeze: for each n, which deep sums are conserved-at-
  max? Predictions from the radial framework (C45_notes.md): depth-n = 1
  (theorem, convex core); depth-(n-1) <= 6n conjecture (bottom-1 diagram,
  face anchors); bottom-2/bottom-3 diagrams have generic Euler census
  values T1(l,n) — MEASURE them (E - V per swap curve) for n=7,8 the way
  the census workstream does for n=6 (34/100/162). A formula for
  T1(l,n) across n is the empirical input a general-n proof needs.
- mod-4 law: bounded ≡ 2n-1 (mod 4) verified n=4..7; verify at scale for
  n=7,8 and quantify the exception rate (invariant-shell configs).
- Per-subset budgets: does the "per-cube depth-1 reaches X but the sum
  caps" budget structure recur at n=7? Does the top spectrum skip values
  (like 633 missing at n=6)?

## 5. Deliverables

- cube_regions.cpp with --n + gates output; updated run_campaign.py;
  campaign_n7.jsonl (target ~50k seeds) and campaign_n8.jsonl (~10k);
  hill-climbs at n=7 from its top-20; a per-n census table (records,
  frozen depths, mod-4 exceptions, T1 numbers); Postscript 6 in
  six_cube_search_results.md with the cross-n picture.
- Do not modify validated Python files; exact_search_results.jsonl
  read-only. Honest negatives welcome.
