#!/usr/bin/env python3
"""W3 as a polynomial: a free-cube EDGE meeting a base CROSSING LINE.

The last unmodelled codimension-1 type (Postscript 57, the (2,1,1) case).  W4
was written as a quadric and immediately explained 43 of 46 chamber boundaries
plus one endpoint of a 727 continuum; the other endpoint of that same line has
NO catalogued root, which is what this module is for.

In Cayley coordinates q = (1,a,b,c) the unnormalised rotation matrix M has
quadratic entries and N = 1+a^2+b^2+c^2.  The free cube is (M/N)([-1,1]^3), so
its edge along axis A with signs sB, sC on the other two axes is the line

    point  P = (M[:,B]*sB + M[:,C]*sC - M[:,A]) / N,   direction M[:,A].

Meeting a fixed base crossing line (p, d) is the coplanarity condition
det[M[:,A], d, N*p - (M[:,B]*sB + M[:,C]*sC - M[:,A])] = 0, cleared of N.

DEGREE.  First column degree 2, third column degree 2, so the condition is
degree 4 in (a,b,c) -- NOT a quadric.  Restricted to a wall line it is a
QUARTIC in t, so a W3 crossing can be an algebraic number of degree 4, outside
every Q(sqrt d).  No engine in this project except the degree-agnostic
`opencount.py` can count such a configuration at all, and no enumeration in
this project could ever have produced one: the mixed strata solve a quadratic
and return Q(sqrt d) by construction.

INVARIANT: roots are located by exact sign change of the exact rational
polynomial at the bracket ends, never by evaluating a float near a root.
"""
import json
import sys
from fractions import Fraction as F

import sympy

from incidence2 import base_catalogue


def w3_polys_on_line(p0, dd):
    """Every W3 condition restricted to the line p0 + t*dd, as sympy Polys."""
    t = sympy.Symbol('t')
    a = sympy.Rational(p0[0]) + t*sympy.Rational(dd[0])
    b = sympy.Rational(p0[1]) + t*sympy.Rational(dd[1])
    c = sympy.Rational(p0[2]) + t*sympy.Rational(dd[2])
    N = 1 + a*a + b*b + c*c
    M = [[1+a*a-b*b-c*c, 2*(a*b-c),      2*(a*c+b)],
         [2*(a*b+c),     1-a*a+b*b-c*c,  2*(b*c-a)],
         [2*(a*c-b),     2*(b*c+a),      1-a*a-b*b+c*c]]
    col = lambda j: [M[i][j] for i in range(3)]

    _, lines = base_catalogue()
    out = []
    for (p, d, ca, cb) in lines:
        for A in range(3):
            B, C = [u for u in range(3) if u != A]
            for sB in (1, -1):
                for sC in (1, -1):
                    cA, cB_, cC = col(A), col(B), col(C)
                    third = [N*sympy.Rational(p[i]) -
                             (cB_[i]*sB + cC[i]*sC - cA[i]) for i in range(3)]
                    det = (cA[0]*(sympy.Rational(d[1])*third[2] -
                                  sympy.Rational(d[2])*third[1])
                           - cA[1]*(sympy.Rational(d[0])*third[2] -
                                    sympy.Rational(d[2])*third[0])
                           + cA[2]*(sympy.Rational(d[0])*third[1] -
                                    sympy.Rational(d[1])*third[0]))
                    P = sympy.Poly(sympy.expand(det), t)
                    if P.degree() >= 1:
                        out.append(((ca, cb, A, sB, sC), P))
    return out


def main():
    li = int(sys.argv[1]) if len(sys.argv) > 1 else 9
    lo = F(sys.argv[2]) if len(sys.argv) > 2 else F('1.93171215057373')
    hi = F(sys.argv[3]) if len(sys.argv) > 3 else F('1.93171310424805')
    data = json.load(open('typology_data.json'))
    L = data['lines'][li]
    p0 = tuple(F(x) for x in L['p0'])
    dd = tuple(F(x) for x in L['dir'])

    polys = w3_polys_on_line(p0, dd)
    degs = {}
    for _, P in polys:
        degs[P.degree()] = degs.get(P.degree(), 0) + 1
    print('W3 conditions restricted to line %d: %d, by degree in t: %s'
          % (li, len(polys), dict(sorted(degs.items()))), flush=True)

    rlo, rhi = sympy.Rational(lo.numerator, lo.denominator), \
        sympy.Rational(hi.numerator, hi.denominator)
    hits = []
    for tag, P in polys:
        vlo, vhi = P.eval(rlo), P.eval(rhi)
        if vlo == 0 or vhi == 0 or (vlo > 0) != (vhi > 0):
            hits.append((tag, P, vlo, vhi))
    print('\nW3 conditions changing sign inside the endpoint bracket'
          ' [%.14f, %.14f]: %d' % (float(lo), float(hi), len(hits)))
    for tag, P, vlo, vhi in hits:
        roots = [r for r in sympy.real_roots(P.as_expr(), sympy.Symbol('t'))
                 if rlo <= r <= rhi]
        for r in roots:
            mp = sympy.minimal_polynomial(r, sympy.Symbol('x'))
            print('   base cubes %s%s, free edge axis %d signs %+d%+d'
                  % (tag[0], tag[1], tag[2], tag[3], tag[4]))
            print('      root t* = %.15f' % float(r))
            print('      minimal polynomial: %s   (degree %d)'
                  % (sympy.factor(mp), sympy.degree(mp)))


if __name__ == '__main__':
    main()
