#!/usr/bin/env python3
"""Is the neighbourhood of a maximiser ONE count, or stratified by direction?

The figure's "drops to" row prints the HIGHEST count found immediately off the
locus.  That is only the whole story if the neighbourhood is uniform.  Scanning
every primitive Cayley direction |u| <= 3 at a fixed small eps and tabulating
what the count actually is answers it directly.
"""
import os
import collections, sys
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dirscan import batch, DIRS, BASE, I
from cayleyscan import redq

def around(qs, label, eps):
    base = batch([list(qs)])[tuple(tuple(q) for q in qs)]
    n = len(qs); cfgs = []
    for ci in range(1, n):
        w = qs[ci][0]
        if w == 0: continue
        c0 = [F(qs[ci][k+1], w) for k in range(3)]
        for u in DIRS:
            c = [c0[k] + eps*u[k] for k in range(3)]
            cfgs.append([tuple(qs[k]) if k != ci else redq([F(1)]+c) for k in range(n)])
    d = batch(cfgs)
    res = [d.get(tuple(tuple(q) for q in c)) for c in cfgs]
    res = [v for v in res if v is not None]
    h = collections.Counter(res)
    top = max(h)
    print('%-18s base %-5s eps %-8s %d directions -> %d distinct counts, max %s'
          % (label, base, str(eps), len(res), len(h), top), flush=True)
    for v, c in sorted(h.items(), reverse=True)[:9]:
        print('        %-5s %5d directions  (%.1f%%)%s'
              % (v, c, 100*c/len(res), '   <- the locus itself' if v == base else ''), flush=True)

around([I, (10,3,3,3)], 'n=2 13 diagonal', F(1,64))
around([(1,0,0,0),(0,5,3,2),(1,-4,-1,1),(1,1,-1,-4)], 'n=4 183', F(1,64))
around(BASE, 'n=5 393', F(1,64))
