#!/usr/bin/env python3
"""Direction scan in the WORLD frame -- the chart the earlier scan got wrong.

dirscan.py perturbs q -> q*(1, eps*u): a RIGHT multiplication, i.e. u in the
cube's own body frame.  Its n=2 controls passed, but both n=2 tangents point
along the rotation AXIS, which is fixed by the rotation, so body and world
directions coincide there and the control could not detect a chart error.  A
tangent in general position is a different integer triple in each frame, so an
integer scan in the body frame misses it.

This scans the world frame, q -> (1, eps*u)*q, exactly.  Both scans together
cover both charts.
"""
import itertools, json, subprocess, sys
from fractions import Fraction as F
from math import gcd
sys.path.insert(0, "/private/tmp/claude-502/-Users-dmi-cube-compounds/88682f8c-0607-4f2d-8384-b3993c9c5ded/scratchpad")
from dirscan import qmul, redq, batch, DIRS, BASE, I

def scan(qs, label, cubes=None, epss=(F(1,32), F(1,128), F(1,512))):
    base = batch([list(qs)])[tuple(tuple(q) for q in qs)]
    n = len(qs)
    cubes = cubes or list(range(1, n))
    survivors = []
    for ci in cubes:
        cfgs, meta = [], []
        for u in DIRS:
            for e in epss:
                q = qmul((F(1), e*u[0], e*u[1], e*u[2]), tuple(F(v) for v in qs[ci]))
                cfgs.append([tuple(qs[k]) if k != ci else redq(q) for k in range(n)])
                meta.append(u)
        res = batch(cfgs)
        got = {}
        for cfg, u in zip(cfgs, meta):
            got.setdefault(u, []).append(res.get(tuple(tuple(q) for q in cfg)))
        for u, vals in got.items():
            if all(v == base for v in vals):
                survivors.append((ci, u))
    print('%-16s count=%-5s WORLD frame: %d directions x %d cubes x %d scales -> %d hold'
          % (label, base, len(DIRS), len(cubes), len(epss), len(survivors)), flush=True)
    for ci, u in survivors:
        print('      cube %d  direction %s' % (ci, u), flush=True)
    return survivors

if __name__ == '__main__':
    print('=== controls (tangents along the rotation axis; both charts agree) ===')
    scan([I, (1,-12,-11,0)], 'n=2 mirror 13')
    scan([I, (10,3,3,3)], 'n=2 diagonal 13')
    print('=== control in GENERAL position: 727 arc A, tangent (1,-3,-6) ===')
    scan(BASE+[(6,53,-87,-156)], 'n=6 727 arcA', cubes=[5])
    print('=== the open cells ===')
    scan([(1,0,0,0),(0,5,3,2),(1,-4,-1,1),(1,1,-1,-4)], 'n=4 183')
    scan(BASE, 'n=5 393')
