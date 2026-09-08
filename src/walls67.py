#!/usr/bin/env python3
"""Wall extraction for the two n=3 maximisers — the only PROVED-ISOLATED records.

n = 3 is anomalous three separate ways: the only irrational rung, the only place
the tower fails to nest (183 does not embed in 393, P155), and the only rung whose
maximisers are proved isolated. P162 predicted the arrangement-level signature of
the third: deficit 0, where every record n >= 4 has deficit >= 1. Measured here.

ZERO GRADIENTS ARE DROPPED. The octahedral list carries one, which the
`degenerate` flag does not catch; left in, it joins the bottom flat and the
chamber recursion returns 0 for a real arrangement (FAILURE_MODES 18).
`zaslavsky.chambers` now refuses zero walls outright, and this filters them here.
"""
import sys
from fractions import Fraction as F
import sympy as sp
sys.path.insert(0, '.')
import dimension as D
from qfield import Q
from dimension67 import RECORDS


def walls_of_67(d):
    name, quats = RECORDS[d]
    D.set_field(d)
    qs = [tuple(Q(F(p), F(q), d) for p, q in quat) for quat in quats]
    pt = []
    for q in qs[1:]:
        pt += D.cayley_of(q)
    ncols = 3 * (len(qs) - 1)
    vars_ = sp.symbols('c0:%d' % ncols)
    Rs = D.frames(vars_, qs[0])
    tight, _ = D.cached_conditions(Rs, len(qs), vars_, pt, D.quats_of(pt, qs[0]), qs[0])
    seen, walls = set(), []
    for t in [x for x in tight if not x['degenerate']]:
        g = list(t['grad'])
        if not any(g):
            continue                      # zero gradient: not a hyperplane
        k = tuple(str(x) for x in g)
        if k not in seen:
            seen.add(k)
            walls.append(g)
    return name, walls, ncols, pt, qs


if __name__ == '__main__':
    from zaslavsky import chambers, Flats
    for d in sorted(RECORDS):
        name, W, nc, pt, qs = walls_of_67(d)
        L = Flats(W)
        b = []
        for i in range(len(W)):
            L._add(b, L.w[i])
        c, st, fl, secs = chambers(W, label='%-11s d=%d:' % (name, d))
        print('             walls %d  ambient %d  rank %d  DEFICIT %d  flats %d'
              % (len(W), nc, len(b), nc - len(b), fl))
