#!/usr/bin/env python3
"""The coincident-curve solve of METHODS section 12, run at EVERY level.

For a base of n cubes, a further cube forming a 13-pair with base cube b lies on
the curve q = b*(1, t*a), a a body diagonal.  Two such conditions are 2 linear
equations in one unknown; the interesting case is when they are CONSISTENT AS AN
IDENTITY, leaving a one-parameter family.  At n = 9 exactly 3 of 448 systems are
of that kind and the record lives on one of them.  Nothing restricted that
computation to n = 9, and it has never been run below it.
"""
import itertools, json, os, subprocess, sys
from fractions import Fraction as F
from math import gcd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solve13 import qmul, conj, cross, intq, count, DIAG

BASES = {
 "n=4 183 -> 5th":  [(1,0,0,0),(0,5,3,2),(1,-4,-1,1),(1,1,-1,-4)],
 "n=5 393 -> 6th":  [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)],
 "n=6 727 -> 7th":  [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1),(7,14,1,-5)],
 "n=7 1217 -> 8th": [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1),(7,14,1,-5),(4,-3,-4,-4)],
}

def coincident(bi, bj, a1, a2):
    m = qmul(conj(bj), bi); mw, mv = m[0], m[1:]
    A = cross(mv, a2)
    B = tuple(cross(tuple(mw*a1[k] for k in range(3)), a2)[k]
              + cross(cross(mv, a1), a2)[k] for k in range(3))
    return all(x == 0 for x in A) and all(x == 0 for x in B)

for label, B in BASES.items():
    n = len(B)
    fams = set()
    for (i, j) in itertools.combinations(range(n), 2):
        for a1 in DIAG:
            for a2 in DIAG:
                if coincident(B[i], B[j], a1, a2): fams.add((i, tuple(a1)))
    print("%s : %d of %d systems coincident -> %d distinct families"
          % (label, len(fams), n*(n-1)//2*16, len(fams)), flush=True)
    for i, a in sorted(fams):
        best = (0, None, None)
        for num in range(1, 700):
            t = F(num, 700)
            q = intq([F(x) for x in qmul(B[i], (1, t*a[0], t*a[1], t*a[2]))])
            if max(abs(v) for v in q) > 512: continue
            c = count(B+[q])
            if c and c > best[0]: best = (c, q, t)
        print("      family on cube %d, axis %-12s  best %s at t=%s  %s"
              % (i, str(a), best[0], best[2], best[1]), flush=True)
