#!/usr/bin/env python3
"""Solve for W3/W4 wall crossings along a line in Cayley space.

An arc of constant count ends where its line crosses a count-changing wall, so
the bound is a ROOT of the wall's equation restricted to the line -- not
something to bisect for (Postscript 90).  The catalogue planes give that root by
one linear solve, but most arc ends sit on the never-enumerated W3/W4 walls
(Postscripts 57, 58).  This supplies those.

Along a line the Cayley vector is v(s) = a0 + s*d, so the UNNORMALISED rotation
matrix has entries quadratic in s, and N = 1 + |v|^2 is quadratic too:

  W4  the free cube's face plane passes through a base TRIPLE POINT p:
      (R^T p)_i = +-1  <=>  (M^T p)_i -+ N = 0,  a QUADRIC in s.
      424 points x 3 components x 2 signs.

  W3  an EDGE of the free cube meets a base CROSSING LINE:
      det[d_edge, d_line, p_line - p_edge] = 0, whose entries are quadratic in
      s, giving degree <= 6 before the common N factors cancel.
      360 lines x 12 edges.

Roots are exact: rational ones exactly, quadratic irrationals as (p +- sqrt D)/q.
"""
import math
from fractions import Fraction as F

import incidence2 as I


def pmul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                out[i+j] += x * y
    return out


def padd(*ps):
    n = max(len(p) for p in ps)
    out = [F(0)] * n
    for p in ps:
        for i, x in enumerate(p):
            out[i] += x
    return out


def pscale(p, k):
    return [x*k for x in p]


def line_polys(a0, d):
    """M (unnormalised rotation, entries as polys in s) and N, for v = a0+s*d."""
    x = [F(a0[0]), F(d[0])]
    y = [F(a0[1]), F(d[1])]
    z = [F(a0[2]), F(d[2])]
    one = [F(1)]
    xx, yy, zz = pmul(x, x), pmul(y, y), pmul(z, z)
    N = padd(one, xx, yy, zz)
    M = [[padd(one, xx, pscale(yy, -1), pscale(zz, -1)),
          pscale(padd(pmul(x, y), pscale(z, -1)), 2),
          pscale(padd(pmul(x, z), y), 2)],
         [pscale(padd(pmul(x, y), z), 2),
          padd(one, pscale(xx, -1), yy, pscale(zz, -1)),
          pscale(padd(pmul(y, z), pscale(x, -1)), 2)],
         [pscale(padd(pmul(x, z), pscale(y, -1)), 2),
          pscale(padd(pmul(y, z), x), 2),
          padd(one, pscale(xx, -1), pscale(yy, -1), zz)]]
    return M, N


def real_roots(p):
    """Exact real roots of a rational polynomial of degree <= 2, else numeric."""
    while p and p[-1] == 0:
        p = p[:-1]
    if len(p) <= 1:
        return []
    if len(p) == 2:
        return [-p[0]/p[1]]
    if len(p) == 3:
        c, b, a = p
        disc = b*b - 4*a*c
        if disc < 0:
            return []
        r = math.isqrt(disc.numerator * disc.denominator)
        if F(r, disc.denominator) ** 2 == disc:      # exact rational root
            sq = F(r, disc.denominator)
            return [(-b - sq)/(2*a), (-b + sq)/(2*a)]
        s = math.sqrt(float(disc))
        return [F(x).limit_denominator(10**12)
                for x in ((-float(b)-s)/(2*float(a)), (-float(b)+s)/(2*float(a)))]
    import numpy as np
    rr = np.roots([float(x) for x in reversed(p)])
    return [F(float(x.real)).limit_denominator(10**12)
            for x in rr if abs(x.imag) < 1e-9]


def w4_params(a0, d, pts):
    """s values where a free-cube face plane passes through a base triple point."""
    M, N = line_polys(a0, d)
    out = set()
    for s_pt, npl, ncub in pts:
        for i in range(3):
            col = padd(*[pscale(M[k][i], F(s_pt[k])) for k in range(3)])
            for sign in (1, -1):
                for r in real_roots(padd(col, pscale(N, -sign))):
                    out.add(r)
    return sorted(out)


def psub(a, b):
    return padd(a, pscale(b, F(-1)))


def det3_poly(a, b, c):
    """det[a b c] with columns whose entries are polynomials in s."""
    return padd(pmul(a[0], psub(pmul(b[1], c[2]), pmul(b[2], c[1]))),
                pscale(pmul(a[1], psub(pmul(b[0], c[2]), pmul(b[2], c[0]))), F(-1)),
                pmul(a[2], psub(pmul(b[0], c[1]), pmul(b[1], c[0]))))


def w3_params(a0, d, lines):
    """s values where a free-cube EDGE meets a base CROSSING LINE.

    With M the unnormalised rotation and N = 1+|v|^2, an edge has direction
    D = 2*M[:,a] and base point P = M[:,b]*sb + M[:,c]*sc - M[:,a], both over N.
    The coplanarity determinant then carries 1/N^2, and its numerator

        det[ D , d_line , N*p_line - P ]

    is degree 4 in s -- the project's quartic.  360 lines x 12 edges."""
    M, N = line_polys(a0, d)
    edges = []
    for a in range(3):
        b, c = [t for t in range(3) if t != a]
        for sb in (1, -1):
            for sc in (1, -1):
                P = [padd(pscale(M[i][b], F(sb)), pscale(M[i][c], F(sc)),
                          pscale(M[i][a], F(-1))) for i in range(3)]
                D = [pscale(M[i][a], F(2)) for i in range(3)]
                edges.append((D, P))
    out = set()
    for p0, d2, ca, cb in lines:
        d2p = [[F(x)] for x in d2]
        for D, P in edges:
            w = [psub(pscale(N, F(p0[i])), P[i]) for i in range(3)]
            for r in real_roots(det3_poly(D, d2p, w)):
                out.add(r)
    return sorted(out)


if __name__ == '__main__':
    pts, lines = I.base_catalogue()
    print('base catalogue: %d triple points, %d crossing lines' % (len(pts), len(lines)))
    a0 = [F(19, 3), F(-7), F(-11)]
    d = [F(1), F(-3), F(-6)]
    W = w4_params(a0, d, pts)
    print('arc A: %d W4 crossings on the line' % len(W))
    near = [s for s in W if F(3, 2) < s < F(7, 2)]
    print('  W4 crossings in s in (1.5, 3.5): %s'
          % ', '.join('%.9f' % float(s) for s in sorted(near)))
    print('  (arc A is 721 at s=2, 723 at 33/16, 727 from 17/8 to about 3.05)')
