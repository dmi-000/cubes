#!/usr/bin/env python3
# Working principles: record_hunt.py / record_hunt_wave2.py (this replays wave 2).
"""Recover the n=8 = 1889 candidate wave 2 counted but was killed before logging.

wave 2 printed its extension totals (1889 leading) without the quaternions.
The menu is recoverable exactly: record_hunt_wave2.py seeds Random(20260729)
and, before menu(), the only rng consumer is climb(restarts=4), whose draw
COUNT does not depend on the configs it sees (neighbors(wide=6) always does
40 x 6 x 3 draws on a 7-cube config).  So replaying four neighbors() calls
puts the generator in the same state and menu(6000, rng) reproduces the very
candidates wave 2 evaluated.

INVARIANT: if the replay is right, 1889 appears among the totals below.  If it
does not, the reconstruction is wrong and the number must NOT be reported --
re-run a fresh extension instead.
"""
import random
import record_hunt as R

rng = random.Random(20260729)
best7 = [[4, 1, 1, -1], [3, 3, 7, 3], [5, -1, -5, -5], [2, 1, 1, 1],
         [1, 1, 1, 1], [5, 2, 2, 2], [39, -5, -34, -31]]      # 1211, the climb's start and end
for _ in range(4):
    R.neighbors(best7, rng, wide=6)          # replay the restart draws only

e8 = R.Engine(8, 2)
cands = [best7 + [q] for q in R.menu(6000, rng)]
res = e8.count(cands)
order = sorted(range(len(cands)), key=lambda k: -res[k][0])
print('top totals:', [res[k][0] for k in order[:8]], flush=True)
for k in order[:5]:
    print(res[k][0], R.fmt(cands[k]), res[k][1], flush=True)
