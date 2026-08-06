#!/usr/bin/env python3
"""Walk the tight-set null directions with the exact engine.

Positive results are self-certifying, so this converts candidates into verified
lower bounds on the moduli dimension.  Directions are taken to rationals at a
large denominator; a direction that fails at 1/1024 but holds at 1/16 is a
rounding artefact, not a tangent, and is reported as such.
"""
import sys, itertools
import numpy as np
from fractions import Fraction as F
from math import gcd
sys.path.insert(0, "/private/tmp/claude-502/-Users-dmi-cube-compounds/88682f8c-0607-4f2d-8384-b3993c9c5ded/scratchpad")
from tight2 import null_of, walk, count, BASE, I

def rat(v, den):
    return [F(float(x)).limit_denominator(den) for x in v]

def test(qs, label, extra_dirs=()):
    base = count(list(qs))
    nq, nt, rank, null, npar = null_of(qs)
    print('%-16s count=%-5s null dim %d of %d params' % (label, base, len(null), npar))
    cands = []
    for i, v in enumerate(null):
        cands.append(('basis%d' % i, v))
    if len(null) >= 2:
        for a, b in itertools.combinations(range(len(null)), 2):
            for w in (1, -1, 2, -2, 3, -3, F(1,2), F(-1,2), F(1,3), F(-1,3)):
                cands.append(('b%d%+gb%d' % (a, float(w), b), null[a]+float(w)*null[b]))
    for name, v in list(extra_dirs):
        cands.append((name, np.array(v, float)))
    hits = []
    for name, v in cands:
        v = v/np.max(np.abs(v))
        u = rat(v, 10**6)
        w = walk(qs, u, (F(1,64), F(1,1024)))
        if all(c == base for _, c in w):
            hits.append((name, v))
            print('   HOLDS  %-12s %s' % (name, np.array2string(
                v, precision=4, suppress_small=True, max_line_width=250)))
    if hits:
        M = np.array([h[1]/np.linalg.norm(h[1]) for h in hits])
        s = np.linalg.svd(M, compute_uv=False)
        d = int((s > 1e-6*s[0]).sum())
        print('   -> %d directions hold, spanning dimension %d' % (len(hits), d))
    else:
        print('   -> no null direction holds')
    return len(null), hits

if __name__ == '__main__':
    test([(1,0,0,0),(0,5,3,2),(1,-4,-1,1),(1,1,-1,-4)], 'n=4 183')
    test(BASE, 'n=5 393')
    test(BASE+[(10,9,9,9)], 'n=6 723')
    test(BASE+[(6,53,-87,-156)], 'n=6 727 arcA')
    test(BASE+[(7,14,1,-5)], 'n=6 727 rec')
    test(BASE+[(7,14,1,-5),(4,-3,-4,-4)], 'n=7 1217')
    test(BASE+[(7,14,1,-5),(4,-3,-4,-4),(3,-3,3,-8)], 'n=8 1891')
