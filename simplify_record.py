#!/usr/bin/env python3
"""Steer ONE cube of a record to a simple rational, using the region's own freedom.

The n=9 record's ninth cube is `(88787,-9061,74275,113786)`, height 113 786 -- 60x
taller than any other cube in any record, and the only one that also lacks the
two-distinct-magnitudes pattern the other nine share ([P217]). [P211] called that height
"forced by codimension" on the strength of dyadic rounding and conjugation by each cube;
[P216] showed why both are bad searches.

The freedom is countable. The record's region has dimension 4 (eps-verified preserving
rank), while ONE cube's Cayley coordinates are only 3 numbers. So if the 3x4 submatrix of
the tangent basis restricted to that cube has rank 3, the map (tangent) -> (that cube's
position) is ONTO, and the cube can be steered to any nearby triple with a dimension of
slack to spare. Solve for the t that lands it on a simple rational, then let the count
decide whether the step stayed in the region -- the region is curved, so the anchor is
the count and not the linear algebra.

Every accepted candidate goes through climb.gate: both engines and three global
rotations, exactly as a record does.
"""
import sys
from fractions import Fraction as F
from math import gcd
sys.path.insert(0, '.')
import sympy as sp
import climb as C
from record_height import preserving_basis

def steer(cubes, j, label, dens=range(1, 400)):
    """make cube j simple by moving inside the region; j is an index into cubes"""
    pt, rec, good, ncols = preserving_basis(cubes)
    h0 = max(abs(x) for q in cubes for x in q)
    print('%s: count %d, preserving rank %d, ambient %d, height %d'
          % (label, rec, len(good), ncols, h0), flush=True)
    if not good:
        print('   no preserving directions'); return None
    idx = [3 * (j - 1), 3 * (j - 1) + 1, 3 * (j - 1) + 2]   # cube 0 is the gauge
    A = sp.Matrix([[F(b[i]) for b in good] for i in idx])
    r = A.rank()
    print('   cube %d occupies coordinates %s; the tangent basis has rank %d there'
          ' (3 needed to steer it freely)' % (j, idx, r), flush=True)
    v = [F(pt[i]) for i in idx]
    print('   its Cayley coords now: %s' % [str(x) for x in v], flush=True)
    best = (h0, None, None)
    for d in dens:
        w = [F(round(x * d), d) for x in v]
        if w == v:
            continue
        rhs = sp.Matrix([w[k] - v[k] for k in range(3)])
        try:
            sol = sp.linsolve((A, rhs))
        except Exception:
            continue
        if not sol:
            continue
        t = list(sol)[0]
        t = [F(sp.nsimplify(x).subs({s: 0 for s in x.free_symbols})) if getattr(x, 'free_symbols', set())
             else F(sp.Rational(x)) for x in t]
        p2 = [F(pt[i]) + sum(t[k] * good[k][i] for k in range(len(good))) for i in range(ncols)]
        cf = C.cfg_at(p2, cubes[0])
        h = max(abs(x) for q in cf for x in q)
        hj = max(abs(x) for x in cf[j])
        if C.cnt(cf) != rec:
            continue
        if h < best[0]:
            best = (h, cf, d)
            print('   d=%-4d cube %d -> %s (height %d), configuration height %d  [%.1fx smaller]'
                  % (d, j, str(cf[j]), hj, h, h0 / h), flush=True)
    if best[1] is None:
        print('   nothing simpler found'); return None
    ok, why = C.gate(best[1], rec)
    print('   BEST height %d (was %d): gate %s' % (best[0], h0, why), flush=True)
    print('   %s' % ';'.join(','.join(map(str, q)) for q in best[1]), flush=True)
    return best

if __name__ == '__main__':
    steer(C.N9, 8, 'n=9 record 2787')
