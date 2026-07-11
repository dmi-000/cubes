# Spec: deep-climb the 717 D₂ family + the shallow-tail tradeoff

For a Sonnet agent. Read: symmetry_search2.py (REUSE its D₂:4+free2
construction, orbit machinery, and climber — do not rewrite), README.md,
six_cube_search_results.md Postscripts 10–11. Current record: 717
(D₂:4+free2), quats 5,2,2,2; -2,-2,2,5; -2,5,-2,2; -2,2,5,-2; 2,1,1,1;
1,0,0,0 — by_depth {1:210, 2:210, 3:158, 4:102, 5:36, 6:1}.

## Why this run

717 is the first record whose deep tail is NOT pinned at the ceilings:
d3 = 158 < 164, yet the total beats 699 because d1 jumped to 210. That
breaks the "records always have (d3,d4,d5)=(164,102,36)" pattern and
opens a new question: **can you trade even more deep count for shallow
count and win?** This run pushes the D₂ family hard and tests that
tradeoff directly.

## Tasks

1. **Deep climb from 717** (the immediate lead). From the two known 717
   configs, hill-climb with a LARGER neighborhood than radius-4:
   - single-component moves ±1..±6, re-gcd, |c| ≤ 512;
   - TWO-component simultaneous moves ±1/±2 (the previous runs were
     mostly one-component — the 158-tail record may sit at a saddle a
     one-component climb can't leave);
   - ~30 restarts from perturbations of 717 (5–10 random moves off it).
   Report the new best and its radius of certified local-maximality.

2. **Sweep the D₂:4+free2 family broadly** with full-quat seeds (as in
   symmetry_search2.py) but MORE restarts (~60) and deeper climbs, since
   this family just produced the record and its first full-quat pass was
   only 25 random starts. Also try the sibling D₂ partitions
   (D₂:2+2+2, D₂:2+4, D₂:4+2 with the free/aligned roles swapped) at
   full-quat resolution — the record used "orbit-4 + free + aligned",
   so vary which cube is free vs aligned.

3. **The shallow-tail tradeoff (the scientific question).** For every
   eval, log the full by_depth. Then characterize the frontier: among
   high-total configs, plot/relate total against d3 (and d4, d5). Does
   lowering d3 below 158 ever raise the total further (via d1+d2), or is
   158 already the sweet spot? Specifically hunt configs with
   d3 ∈ {150..162} and see if any reach > 717. Report the best total at
   each observed d3 value — this maps the deep-vs-shallow exchange rate.

## Rules & gates

- Gate: rebuild the 717 config through your path and confirm it counts
  717 with the stated histogram before climbing (construction sanity).
- Fast C++ engine ./cube_regions, ≤4 cores. Log every eval (family,
  full seed quats, total, by_depth) to d2_deepclimb.jsonl.
- Flag any total > 717 immediately (new record) and any deep-count
  CEILING violation (d3 > 164, d4 > 102, d5 > 36, d6 ≠ 1 — that is a
  construction bug, not a find; stop and check). Note: d3 BELOW 164 is
  expected and interesting here, not a bug.
- Do NOT edit six_cube_search_results.md (main session merges a
  postscript), symmetry_search2.py, or validated files;
  exact_search_results.jsonl read-only. Exact predicates only.

## Deliverables

d2_deepclimb.jsonl and d2_deepclimb_report.md: the new best total (vs
717) with quats and local-max radius; the D₂ sibling-partition results;
and the deep-vs-shallow table (best total at each d3 value observed) with
one sentence on whether the shallow-tail tradeoff extends past 717 or
158 is the optimum. Honest negatives welcome — "717/158 is the local
optimum of the exchange" is a real result. Final message: new best vs
717, whether the shallow-tail tradeoff buys more, and the exchange-rate
table highlights.
