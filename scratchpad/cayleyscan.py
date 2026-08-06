#!/usr/bin/env python3
"""Direction scan in the CAYLEY chart -- the chart the known tangents live in.

Both quaternion-chart scans are void by control: the world-frame one misses
727 arc A's verified tangent (1,-3,-6), and the body-frame one misses it too.
They pass only at n=2, where the tangent lies along the rotation axis and every
chart agrees.  The reason is simple once stated -- an integer-direction scan can
only find a tangent that is an integer triple IN THE CHART SCANNED, and a
tangent in general position is integral in at most one chart.

Every tangent this project has ever verified is a small integer triple in the
CAYLEY chart: (1,1,0), (1,1,1), (1,-3,-6), (1,1,-4), (-1,-1/7,3/14).  So that is
the chart to scan.  Its one defect is a cube with w = 0, whose Cayley point is
at infinity; such a cube is scanned in the quaternion w-chart instead and
flagged, because for it the scan proves nothing.
"""
import itertools, json, subprocess, sys
from fractions import Fraction as F
from math import gcd
sys.path.insert(0, "/private/tmp/claude-502/-Users-dmi-cube-compounds/88682f8c-0607-4f2d-8384-b3993c9c5ded/scratchpad")
from dirscan import batch, DIRS, BASE, I

def redq(q):
    L = 1
    for v in q: L = L*v.denominator//gcd(L, v.denominator)
    iq = [int(v*L) for v in q]
    g = 0
    for v in iq: g = gcd(g, abs(v))
    return tuple(v//g for v in iq)

def scan(qs, label, epss=(F(1,32), F(1,128), F(1,512))):
    base = batch([list(qs)])[tuple(tuple(q) for q in qs)]
    n = len(qs)
    survivors, skipped = [], []
    for ci in range(1, n):
        w = qs[ci][0]
        if w == 0:
            skipped.append(ci); continue
        c0 = [F(qs[ci][k+1], w) for k in range(3)]
        cfgs, meta = [], []
        for u in DIRS:
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
    print('%-16s count=%-5s CAYLEY chart: %d directions x %d cubes x %d scales -> %d hold%s'
          % (label, base, len(DIRS), n-1-len(skipped), len(epss), len(survivors),
             '  (cubes %s at Cayley infinity, NOT scanned)' % skipped if skipped else ''),
          flush=True)
    for ci, u in survivors:
        print('      cube %d  direction %s' % (ci, u), flush=True)
    return survivors

if __name__ == '__main__':
    print('=== CONTROL in general position: 727 arc A, tangent (1,-3,-6) ===')
    scan(BASE+[(6,53,-87,-156)], 'n=6 727 arcA')
    print('=== CONTROL: 723, tangent (1,1,1) ===')
    scan(BASE+[(10,9,9,9)], 'n=6 723')
    print('=== the open cells ===')
    scan([(1,0,0,0),(0,5,3,2),(1,-4,-1,1),(1,1,-1,-4)], 'n=4 183')
    scan(BASE, 'n=5 393')
