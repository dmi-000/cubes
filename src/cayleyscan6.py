#!/usr/bin/env python3
"""Cayley-chart direction scan over |u| <= R, with a control that can pass.

Every earlier scan in this session searched primitive integer triples with
|u_i| <= 3 -- a set that does NOT contain 727 arc A's tangent (1,-3,-6) or arc
B's (1,1,-4).  So those runs could never have found them, and the controls that
did pass -- n=2's (1,1,1) and (1,1,0), 723's (1,1,1) -- are exactly the tangents
small enough to lie inside the set.  A control must be chosen because it is
HARD for the method, not because it is available.

R = 6 contains both missing tangents.  The chart is Cayley, where every verified
tangent in this project is integral.
"""
import os
import itertools, sys
from fractions import Fraction as F
from math import gcd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dirscan import batch, BASE, I
from cayleyscan import redq

def dirs(R):
    out = []
    for u in itertools.product(range(-R, R+1), repeat=3):
        if u == (0,0,0): continue
        if gcd(gcd(abs(u[0]), abs(u[1])), abs(u[2])) != 1: continue
        out.append(u)
    return out

def scan(qs, label, R=6, cubes=None, epss=(F(1,32), F(1,128), F(1,512))):
    D = dirs(R)
    base = batch([list(qs)])[tuple(tuple(q) for q in qs)]
    n = len(qs)
    cubes = cubes if cubes is not None else list(range(1, n))
    survivors, skipped = [], []
    for ci in cubes:
        w = qs[ci][0]
        if w == 0:
            skipped.append(ci); continue
        c0 = [F(qs[ci][k+1], w) for k in range(3)]
        cfgs, meta = [], []
        for u in D:
            for e in epss:
                c = [c0[k] + e*u[k] for k in range(3)]
                cfgs.append([tuple(qs[k]) if k != ci else redq([F(1)]+c)
                             for k in range(n)])
                meta.append(u)
        res = batch(cfgs)
        got = {}
        for cfg, u in zip(cfgs, meta):
            got.setdefault(u, []).append(res.get(tuple(tuple(q) for q in cfg)))
        for u, vals in got.items():
            if all(v == base for v in vals):
                survivors.append((ci, u))
    print('%-16s count=%-5s Cayley, |u|<=%d: %d dirs x %d cubes x %d scales -> %d hold%s'
          % (label, base, R, len(D), len(cubes)-len(skipped), len(epss),
             len(survivors),
             '  (cube %s at Cayley infinity, NOT scanned)' % skipped if skipped else ''),
          flush=True)
    for ci, u in survivors:
        print('      cube %d  direction %s' % (ci, u), flush=True)
    return survivors

if __name__ == '__main__':
    what = sys.argv[1]
    if what == 'ctl':
        scan(BASE+[(6,53,-87,-156)], 'n=6 727 arcA', cubes=[5], epss=(F(1,32),))
    elif what == '4':
        scan([(1,0,0,0),(0,5,3,2),(1,-4,-1,1),(1,1,-1,-4)], 'n=4 183')
    elif what == '5':
        scan(BASE, 'n=5 393')
