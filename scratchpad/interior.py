#!/usr/bin/env python3
"""Is EVERY boundary a coincidence boundary?

The chamber decompositions evaluated one point between consecutive W3/W4 roots,
which assumes the count is constant there -- so they cannot test the assumption.
This samples densely INSIDE inter-root intervals instead.  A count change strictly
between two consecutive roots would be a boundary the coincidence catalogue does
not see; constancy everywhere is evidence that walls and coincidences coincide.
"""
import sys
from fractions import Fraction as F
sys.path.insert(0, "/Users/dmi/cube-compounds")
sys.path.insert(0, "/private/tmp/claude-502/-Users-dmi-cube-compounds/88682f8c-0607-4f2d-8384-b3993c9c5ded/scratchpad")
import incidence2 as I, wall_params as W
from maxline import q_of, evaluate, BASE

a0 = [F(0), F(0), F(0)]; d = [F(1), F(1), F(1)]
pts, lines = I.base_catalogue()
roots = sorted(set(W.w4_params(a0, d, pts)) | set(W.w3_params(a0, d, lines)))
gaps = sorted(((roots[i+1]-roots[i], roots[i], roots[i+1]) for i in range(len(roots)-1)),
              reverse=True)[:12]
print('723 line: %d roots; sampling the 12 WIDEST inter-root intervals, 40 points each'
      % len(roots), flush=True)
bad = 0
for w, lo, hi in gaps:
    N = 40
    ss = []
    for den in (1,2,3,4,6,8,12,16,24,32,48,64,96,128,256,512,1024):
        k0 = int(lo*den)+1
        for k in range(k0, k0+4000):
            v = F(k, den)
            if v >= hi: break
            if v > lo and v not in ss: ss.append(v)
            if len(ss) >= N: break
        if len(ss) >= N: break
    ss = ss[:N]
    vals = evaluate([BASE+[q_of([a0[i]+s*d[i] for i in range(3)])] for s in ss])
    got = [v for v in vals if v is not None]
    distinct = sorted(set(got))
    flag = '' if len(distinct) <= 1 else '   <== COUNT CHANGES INSIDE A CHAMBER'
    if len(distinct) > 1: bad += 1
    print('   (%.6f, %.6f) width %.6f : %d/%d evaluated, counts %s%s'
          % (float(lo), float(hi), float(w), len(got), N, distinct, flag), flush=True)
print('\n%d of %d widest chambers carry more than one count.' % (bad, len(gaps)), flush=True)
