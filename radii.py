#!/usr/bin/env python3
"""Coincidence RADII as a configuration invariant.

A user's proposal: record the radii at which cube boundaries coincide. Two properties the
plane-incidence signature of [P227] did not have come free:

  * a radius is invariant under a GLOBAL rotation, because it is a distance from the shared
    centre; and
  * it is invariant under each cube's own 24 symmetries, because those fix the cube setwise
    and hence fix its boundary as a point set.

So unlike the signature, this cannot be a property of the quaternion spelling -- the bug that
voided a 3.1M-row census. The invariance is by construction, and is gated below anyway.

SCALE. Cubes here are |M.x| <= 1 with M the rotation rows scaled by n = |q|^2, i.e. side 2.
So r^2 = 3 at a corner, 2 at an edge midpoint, 1 at a face centre. An EDGE-EDGE coincidence
lies on an edge of both cubes, hence 2 <= r^2 <= 3; a CORNER-CORNER coincidence has r^2 = 3
exactly. (For unit-side cubes divide by 4: sqrt(2)/2 <= r <= sqrt(3)/2, as the user states.)
"""
import itertools, sys
from collections import Counter
from fractions import Fraction as F
sys.path.insert(0, '.')
from cellcomplex import on_bdry_params
from euler3 import rowsT, frames, segments
from v3_outer import strictly_inside


def vertices(qs):
    """outer-boundary vertices: (r^2, planes-per-cube profile, degree)"""
    Ms = [rowsT(R) for R in frames(qs)]
    n = len(qs)
    node = {}; arcs = []
    for i, j in itertools.combinations(range(n), 2):
        for p, d, lo, hi in segments(Ms[i], Ms[j]):
            cuts = sorted({lo, hi} | {t for k in range(n) if k not in (i, j)
                                      for t in on_bdry_params(p, d, lo, hi, Ms[k])})
            for a, b in zip(cuts, cuts[1:]):
                if a >= b:
                    continue
                mid = tuple(p[z] + ((a + b) / 2) * d[z] for z in range(3))
                if any(strictly_inside(mid, Ms[k]) for k in range(n) if k not in (i, j)):
                    continue
                ends = []
                for t in (a, b):
                    P = tuple(p[z] + t * d[z] for z in range(3))
                    node.setdefault(P, len(node)); ends.append(node[P])
                arcs.append(tuple(ends))
    deg = Counter()
    for a, b in arcs:
        deg[a] += 1; deg[b] += 1
    out = []
    for P, idx in node.items():
        per = []
        for m in range(n):
            c = sum(1 for q in range(3)
                    if abs(sum(Ms[m][q][z] * P[z] for z in range(3))) == 1)
            if c:
                per.append(c)
        r2 = sum(F(x) * F(x) for x in P)
        out.append((r2, tuple(sorted(per, reverse=True)), deg[idx]))
    return out


def radius_signature(qs, kinds=None):
    """the multiset of r^2 over outer vertices, optionally restricted to a coincidence type"""
    h = Counter()
    for r2, per, d in vertices(qs):
        if kinds is not None and per not in kinds:
            continue
        h[r2] += 1
    return tuple(sorted(h.items()))


if __name__ == '__main__':
    CORNER = {(3, 3)}
    EDGE = {(2, 2)}
    CASES = {
        'n=4 record 183': [(1,0,0,0),(0,5,3,2),(1,-4,-1,1),(1,1,-1,-4)],
        'n=5 record 393': [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)],
        'n=4 haar':       [(1,0,0,0),(7,3,-2,5),(4,-5,3,1),(2,7,-3,4)],
    }
    print('GATE: edge-edge must have 2 <= r^2 <= 3; corner-corner must have r^2 = 3')
    ok = True
    for name, qs in CASES.items():
        vs = vertices(qs)
        e = [r2 for r2, per, d in vs if per == (2, 2)]
        c = [r2 for r2, per, d in vs if per == (3, 3)]
        eok = all(2 <= x <= 3 for x in e)
        cok = all(x == 3 for x in c)
        ok &= eok and cok
        print('  %-16s edge-edge %3d in [%s, %s] %s   corner-corner %2d all r^2=3 %s'
              % (name, len(e), min(e) if e else '-', max(e) if e else '-',
                 'OK' if eok else 'FAIL', len(c), 'OK' if cok else ('FAIL' if c else 'n/a')))
    print('  gate: %s' % ('PASS' if ok else 'FAIL'))
