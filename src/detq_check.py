#!/usr/bin/env python3
"""WHY every wall splits over Q: det(Q) is a perfect square IDENTICALLY.

Postscript 103 measured 63432 rational rulings and 0 irrational and could only
report it as a census.  The reason is an identity.  The two ruling families of a
nondegenerate quadric surface are defined over Q(sqrt(det Q)), so a wall splits
over Q exactly when det(Q) is a square in Q -- a property of the WALL, not of the
point used to probe it.  Computed symbolically here, for both wall types:

    W4 (face plane of the free cube through base triple point p):
        det(Q) = (|p|^2 - 1)^2

    W3 (edge of the free cube meeting base crossing line through q, direction m):
        det(Q) = 16*(|m x q|^2 - 2|m|^2)^2 = (4*(|m x q|^2 - 2|m|^2))^2

Both are squares for every RATIONAL base datum, so every wall of a rational base
is split over Q at every n -- nothing in the derivation mentions the base or n.
That proves the census rather than extending it.

The vanishing loci are the degenerate (cone / plane-pair) walls, and each is a
distinguished radius of the unit cube:

    W4 degenerate  <=>  |p| = 1      = the FACE distance
    W3 degenerate  <=>  dist(line, origin)^2 = 2  = the EDGE distance squared

Run: python3 detq_check.py   (symbolic identity, then verification on the 393 base)
"""
import sys
from fractions import Fraction as F
import sympy as sp
sys.path.insert(0, HERE)
from solve_ends import catalogue, BASE
import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__))

x, y, z = sp.symbols('x y z')
M = sp.Matrix([[1+x**2-y**2-z**2, 2*(x*y-z),        2*(x*z+y)],
               [2*(x*y+z),        1-x**2+y**2-z**2, 2*(y*z-x)],
               [2*(x*z-y),        2*(y*z+x),        1-x**2-y**2+z**2]])
N = 1 + x**2 + y**2 + z**2


def form_of(expr):
    """4x4 symmetric matrix of a quadratic form in (x,y,z), homogenised by w."""
    poly = sp.Poly(sp.expand(expr), x, y, z)
    Q = sp.zeros(4, 4)
    for monom, coeff in poly.terms():
        idx = []
        for j, e in enumerate(monom):
            idx += [j]*e
        assert len(idx) <= 2, ('not a quadric', monom)
        idx += [3]*(2-len(idx))
        a, b = idx
        if a == b:
            Q[a, b] += coeff
        else:
            Q[a, b] += coeff/2
            Q[b, a] += coeff/2
    return Q


def symbolic_identities():
    p1, p2, p3 = sp.symbols('p1 p2 p3')
    q1, q2, q3, m1, m2, m3 = sp.symbols('q1 q2 q3 m1 m2 m3')
    p = [p1, p2, p3]
    print('W4, all six (axis, sign) branches:')
    target4 = (p1**2 + p2**2 + p3**2 - 1)**2
    for i in range(3):
        for sign in (1, -1):
            d = sp.factor(sp.simplify(form_of(sum(p[k]*M[k, i] for k in range(3)) - sign*N).det()))
            assert sp.simplify(d - target4) == 0, (i, sign, d)
    print('   det(Q) = (|p|^2 - 1)^2   for all 6, verified symbolically')

    qv = sp.Matrix([q1, q2, q3]); mv = sp.Matrix([m1, m2, m3])
    cross = mv.cross(qv)
    target3 = 16*((cross.dot(cross)) - 2*mv.dot(mv))**2
    print('W3, all twelve edges:')
    for a in range(3):
        b, c = [t for t in range(3) if t != a]
        for sb in (1, -1):
            for sc in (1, -1):
                D = 2*M[:, a]
                P = sb*M[:, b] + sc*M[:, c] - M[:, a]
                G = sp.expand(sp.Matrix.hstack(D, mv, N*qv - P).det())
                quo, rem = sp.div(sp.Poly(G, x, y, z), sp.Poly(N, x, y, z))
                assert rem.as_expr() == 0, ('N does not divide', a, sb, sc)
                d = sp.simplify(form_of(quo.as_expr()).det())
                assert sp.simplify(d - target3) == 0, (a, sb, sc, sp.factor(d))
    print('   det(Q) = 16*(|m x q|^2 - 2|m|^2)^2   for all 12, verified symbolically')


def verify_on_base():
    pts, lines = catalogue(BASE)
    deg4 = sum(1 for p, _, _ in pts if sum(F(c)**2 for c in p) == 1)
    def cross(a, b):
        return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
    deg3 = 0
    for p0, d, ca, cb in lines:
        q = [F(v) for v in p0]; m = [F(v) for v in d]
        cr = cross(m, q)
        if sum(v*v for v in cr) - 2*sum(v*v for v in m) == 0:
            deg3 += 1
    print('393 base: %d triple points, %d degenerate (|p| = 1)' % (len(pts), deg4))
    print('          %d crossing lines, %d degenerate (dist^2 = 2)' % (len(lines), deg3))
    print('  => %d W4 walls and %d W3 walls, ALL nondegenerate and ALL split over Q'
          % (6*(len(pts)-deg4), 12*(len(lines)-deg3)))


if __name__ == '__main__':
    symbolic_identities()
    verify_on_base()
