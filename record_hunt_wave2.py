#!/usr/bin/env python3
# Working principles: record_hunt.py (engine + climb machinery it imports).
"""Wave 2 of the n=7/n=8 hunt: exploit wave 1's two candidates.

Wave 1 (record_hunt_n8.jsonl) extended the 1207 seven-cube record and found
n=8 = 1887, whose 7-subsets contain n=7 = 1211.  Neither has been climbed:
1211 arrived as a SUBSET (never optimized in its own right) and 1887's climb
used only 2 wide restarts.  This script closes both loops in dependency
order, so each stage starts from the best config the previous one produced:

  1. climb 1211  (n=7)                    -> best7
  2. extend best7 with a fresh menu (n=8)  -> best8   [bottom-up]
  3. climb best8 harder                    -> best8'
  4. subsets of best8'                     -> n=7 candidates [top-down]

Counts are exact (cube_regions_n); nothing here is a claimed record until
certify_six agrees -- see the project rule in LEDGER.md.
"""
import json
import random
import sys

import record_hunt as R

WORKERS = 2
OUT = open('record_hunt_wave2.jsonl', 'a')
rng = random.Random(20260729)

start7 = [[4, 1, 1, -1], [3, 3, 7, 3], [5, -1, -5, -5], [2, 1, 1, 1],
          [1, 1, 1, 1], [5, 2, 2, 2], [39, -5, -34, -31]]        # 1211
start8 = [[4, 1, 1, -1], [3, 3, 7, 3], [5, -1, -5, -5], [2, 1, 1, 1],
          [1, 1, 1, 1], [5, 2, 2, 2], [5, 4, -4, -4],
          [39, -5, -34, -31]]                                     # 1887

e7 = R.Engine(7, WORKERS)
best7, tot7 = R.climb(e7, start7, OUT, 'n7_climb', rng, restarts=4)
print('n7 climbed:', tot7, R.fmt(best7), flush=True)
R.log(OUT, stage='wave2_best7', total=tot7, quats=best7)

e8 = R.Engine(8, WORKERS)
cands = [best7 + [q] for q in R.menu(6000, rng)]
res = e8.count(cands)
order = sorted(range(len(cands)), key=lambda k: -res[k][0])
print('extend best7 ->', [res[k][0] for k in order[:8]], flush=True)
best8, tot8 = (start8, e8.count([start8])[0][0])
for k in order[:4]:
    cfg, tot = R.climb(e8, cands[k], OUT, 'n8_seed%d' % k, rng, restarts=2)
    R.log(OUT, stage='wave2_n8_climbed', total=tot, quats=cfg)
    print('n8 climbed:', tot, flush=True)
    if tot > tot8:
        best8, tot8 = cfg, tot

cfg, tot = R.climb(e8, best8, OUT, 'n8_deep', rng, restarts=6)
if tot > tot8:
    best8, tot8 = cfg, tot
print('WAVE2 BEST n8:', tot8, R.fmt(best8), flush=True)
R.log(OUT, stage='wave2_best8', total=tot8, quats=best8)

for t, sub, bd in R.subsets(e8, best8):
    R.log(OUT, stage='wave2_n7_subset', total=t, quats=sub, by_depth=bd)
    print('n7 subset:', t, R.fmt(sub), flush=True)
R.log(OUT, stage='done', evals7=e7.evals, evals8=e8.evals)
