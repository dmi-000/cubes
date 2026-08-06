#!/usr/bin/env python3
"""Locally, do more coincidences mean more regions?

Globally they do not: 723 carries 180 edge-edge crossings and loses to 727's
150.  But that compares different strata.  Within ONE neighbourhood -- every
primitive Cayley direction at a fixed eps from a single maximiser -- the question
is whether the region count and the crossing count move together.
"""
import collections, statistics, sys
from fractions import Fraction as F
sys.path.insert(0, "/private/tmp/claude-502/-Users-dmi-cube-compounds/88682f8c-0607-4f2d-8384-b3993c9c5ded/scratchpad")
from dirscan import batch, DIRS
from cayleyscan import redq
from edgecross import crossing_set

def corr(qs, ci, label, eps=F(1,64)):
    base = batch([list(qs)])[tuple(tuple(q) for q in qs)]
    b_cr = len(crossing_set(qs))
    c0 = [F(qs[ci][k+1], qs[ci][0]) for k in range(3)]
    cfgs = [[tuple(qs[k]) if k != ci else redq([F(1)]+[c0[t]+eps*u[t] for t in range(3)])
             for k in range(len(qs))] for u in DIRS]
    d = batch(cfgs)
    rows = []
    for c in cfgs:
        r = d.get(tuple(tuple(q) for q in c))
        if r is None: continue
        rows.append((r, len(crossing_set(c))))
    print('%s  base: %d regions, %d crossings   (%d directions)' % (label, base, b_cr, len(rows)), flush=True)
    by = collections.defaultdict(list)
    for r, x in rows: by[r].append(x)
    for r in sorted(by, reverse=True):
        v = by[r]
        print('    %4d regions  ->  crossings %3d-%-3d  mean %6.1f   (%d dirs)'
              % (r, min(v), max(v), statistics.mean(v), len(v)), flush=True)
    xs = [r for r, _ in rows]; ys = [x for _, x in rows]
    mx, my = statistics.mean(xs), statistics.mean(ys)
    num = sum((a-mx)*(b-my) for a, b in rows)
    den = (sum((a-mx)**2 for a in xs)*sum((b-my)**2 for b in ys))**.5
    print('    Pearson r between region count and crossing count = %+.3f' % (num/den), flush=True)

REC183 = [(1,0,0,0),(0,5,3,2),(1,-4,-1,1),(1,1,-1,-4)]
corr(REC183, 2, 'n=4 183, cube 2')
corr(REC183, 3, 'n=4 183, cube 3')
