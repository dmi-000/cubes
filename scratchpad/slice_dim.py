#!/usr/bin/env python3
"""Is the single-cube slice dimension EXACTLY the aligned reading, or only >= it?

The aligned probe finds 1 direction at n=7 and 2 at n=8, which bounds the
dimension from below.  Scanning every primitive integer direction |u_i| <= 3 in
the exact chart q -> q*(1, eps*u), on the cubes that carry those directions,
bounds it from above within that cube's 3-dimensional slice: if nothing but the
known direction survives at three scales, the slice dimension is 1, not >= 1.
Multi-cube directions stay untested, so this resolves the slice and not the
moduli space.
"""
import sys
from fractions import Fraction as F
sys.path.insert(0, "/private/tmp/claude-502/-Users-dmi-cube-compounds/88682f8c-0607-4f2d-8384-b3993c9c5ded/scratchpad")
import dirscan as D

BASE = [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
N7 = BASE+[(7,14,1,-5),(4,-3,-4,-4)]
N8 = BASE+[(7,14,1,-5),(4,-3,-4,-4),(24,-24,24,-61)]

def one_cube(qs, ci, label, epss=(F(1,32), F(1,128), F(1,512))):
    base = D.batch([list(qs)])[tuple(tuple(q) for q in qs)]
    cfgs, meta = [], []
    for u in D.DIRS:
        for e in epss:
            q = D.qmul(tuple(F(v) for v in qs[ci]), (F(1), e*u[0], e*u[1], e*u[2]))
            cfgs.append([tuple(qs[k]) if k != ci else D.redq(q) for k in range(len(qs))])
            meta.append(u)
    res = D.batch(cfgs)
    got = {}
    for cfg, u in zip(cfgs, meta):
        got.setdefault(u, []).append(res.get(tuple(tuple(q) for q in cfg)))
    hold = [u for u, v in got.items() if all(x == base for x in v)]
    print('%s cube %d: %d directions x %d scales -> %d hold  %s'
          % (label, ci, len(D.DIRS), len(epss), len(hold), sorted(hold)), flush=True)

one_cube(N7, 6, 'n=7 1217')
one_cube(N8, 6, 'n=8 1895')
one_cube(N8, 7, 'n=8 1895')
