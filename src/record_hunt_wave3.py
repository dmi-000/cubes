#!/usr/bin/env python3
# Working principles: record_hunt.py (engine + climb machinery it imports).
"""Wave 3: propagate the new n=6 record (727) up the tower.

727 = 393's five cubes + (7,14,1,-5), found in the large-height extension
stratum no n<=6 campaign had sampled.  Every level above it was built on
723, so each one is now re-derivable from a better base:

  1. extend 727 -> n=7   (current record 1211, itself built on 723)
  2. climb, then extend the winner -> n=8   (current record 1889)
  3. subsets of each winner, feeding back down

INVARIANT: nothing here is a record until certify_six agrees; totals below
are cube_regions_n only.
"""
import random
import record_hunt as R

W = 2
OUT = open('record_hunt_wave3.jsonl', 'a')
rng = random.Random(727727)

best6 = [[4, 1, 1, -1], [3, 3, 7, 3], [5, -1, -5, -5], [2, 1, 1, 1],
         [1, 1, 1, 1], [7, 14, 1, -5]]                      # 727

e7 = R.Engine(7, W)
cands = [best6 + [q] for q in R.menu(8000, rng)]
res = e7.count(cands)
order = sorted(range(len(cands)), key=lambda k: -res[k][0])
print('n7 extend:', [res[k][0] for k in order[:8]], flush=True)
best7, tot7 = cands[order[0]], res[order[0]][0]
for k in order[:4]:
    cfg, t = R.climb(e7, cands[k], OUT, 'n7_seed%d' % k, rng, restarts=2)
    R.log(OUT, stage='wave3_n7_climbed', total=t, quats=cfg)
    print('n7 climbed:', t, flush=True)
    if t > tot7:
        best7, tot7 = cfg, t
print('WAVE3 BEST n7:', tot7, R.fmt(best7), flush=True)
R.log(OUT, stage='wave3_best7', total=tot7, quats=best7)

e8 = R.Engine(8, W)
cands = [best7 + [q] for q in R.menu(6000, rng)]
res = e8.count(cands)
order = sorted(range(len(cands)), key=lambda k: -res[k][0])
print('n8 extend:', [res[k][0] for k in order[:8]], flush=True)
best8, tot8 = cands[order[0]], res[order[0]][0]
for k in order[:3]:
    cfg, t = R.climb(e8, cands[k], OUT, 'n8_seed%d' % k, rng, restarts=2)
    R.log(OUT, stage='wave3_n8_climbed', total=t, quats=cfg)
    print('n8 climbed:', t, flush=True)
    if t > tot8:
        best8, tot8 = cfg, t
print('WAVE3 BEST n8:', tot8, R.fmt(best8), flush=True)
R.log(OUT, stage='wave3_best8', total=tot8, quats=best8)

for t, sub, bd in R.subsets(e8, best8):
    R.log(OUT, stage='wave3_n7_subset', total=t, quats=sub, by_depth=bd)
    print('n7 subset:', t, R.fmt(sub), flush=True)
R.log(OUT, stage='done', evals7=e7.evals, evals8=e8.evals)
