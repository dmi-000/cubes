#!/usr/bin/env python3
"""INDEPENDENT CONTROL for rulings.py -- rebuilds the arc-A wall from scratch.

This is route (b)/(c) of the three-way check `rulings_report.md` cites for the
G1 discrepancy: it constructs the W4 quadric with sympy directly from the
symbolic Cayley rotation, converts to an exact rational 4x4 form, and solves for
the two ruling directions by hand in Fraction arithmetic -- sharing NO code with
rulings.py.  It reproduces a,b,c = -14320/4617, 6184/1539, -664/513 and
disc = 64/729 for axis i=0, and finds BOTH rulings rational on all three active
branches of the triple point (-11/19, -31/19, -1/19).

That is what refutes the 2026-08-10 "one rational, one irrational" claim by a
route independent of the code that first reported it, so it is a deliverable,
not a probe.  Recovered from a session scratchpad on 2026-08-11 -- it had been
written to volatile temp, which is the third occurrence of that failure in this
project (see METHODS.md "Where work is allowed to live").

Run: python3 rulings_control.py
"""
from fractions import Fraction as F
import sympy as sp

x, y, z = sp.symbols('x y z')
Msym = [[1 + x**2 - y**2 - z**2, 2*(x*y - z), 2*(x*z + y)],
        [2*(x*y + z), 1 - x**2 + y**2 - z**2, 2*(y*z - x)],
        [2*(x*z - y), 2*(y*z + x), 1 - x**2 - y**2 + z**2]]
Nsym = 1 + x**2 + y**2 + z**2

def frac2sp(fr):
    return sp.Rational(fr.numerator, fr.denominator)

def homogenize(expr):
    poly = sp.Poly(sp.expand(expr), x, y, z)
    Q = [[sp.Integer(0)]*4 for _ in range(4)]
    for monom, coeff in poly.terms():
        total = sum(monom)
        wdeg = 2 - total
        assert wdeg >= 0, (monom, coeff)
        idxs = []
        for i, e in enumerate(monom):
            idxs += [i]*e
        idxs += [3]*wdeg
        assert len(idxs) == 2
        i, j = idxs
        if i == j:
            Q[i][j] += coeff
        else:
            Q[i][j] += coeff/2
            Q[j][i] += coeff/2
    return Q

def Q_to_fraction(Q):
    out = []
    for row in Q:
        r = []
        for v in row:
            v = sp.nsimplify(v)
            r.append(F(v.p, v.q))
        out.append(r)
    return out

p = (F(-11,19), F(-31,19), F(-1,19))
p0 = [F(19,2), F(-33,2), F(-30)]

for i, sign in [(0,1),(1,1),(2,-1)]:
    expr = sum(frac2sp(p[k])*Msym[k][i] for k in range(3)) - sign*Nsym
    Qsym = homogenize(expr)
    Q = Q_to_fraction(Qsym)
    # F(p0) check
    u0 = p0 + [F(1)]
    Fp0 = sum(u0[a]*Q[a][b]*u0[b] for a in range(4) for b in range(4))
    print('i',i,'sign',sign,'F(p0)=',Fp0)
    # row = u0^T Q
    row = [sum(u0[a]*Q[a][b] for a in range(4)) for b in range(4)]
    L = row[:3]
    print('  linear row (dx,dy,dz coeffs):', L)
    # find nullspace basis e1,e2 for L . d = 0
    # find pivot
    nz = [k for k in range(3) if L[k] != 0]
    if not nz:
        print('  degenerate: L all zero'); continue
    piv = nz[0]
    others = [k for k in range(3) if k != piv]
    e1 = [F(0)]*3; e2 = [F(0)]*3
    e1[others[0]] = F(1); e1[piv] = -L[others[0]]/L[piv]
    e2[others[1]] = F(1); e2[piv] = -L[others[1]]/L[piv]
    print('  e1=',e1,'e2=',e2)
    A = [row[:3] for row in Q[:3]]
    def qf(d):
        return sum(d[a]*A[a][b]*d[b] for a in range(3) for b in range(3))
    def bil(d1,d2):
        return sum(d1[a]*A[a][b]*d2[b] for a in range(3) for b in range(3))
    a_coef = qf(e1)
    c_coef = qf(e2)
    b_coef = bil(e1,e2)*2 - a_coef*0  # cross term coefficient for (alpha e1+beta e2): alpha^2 a + alpha beta * 2*bil + beta^2 c
    b_coef = 2*bil(e1,e2)
    print('  a,b,c =', a_coef, b_coef, c_coef)
    disc = b_coef*b_coef - 4*a_coef*c_coef
    print('  disc=', disc)
    import math
    if disc >= 0:
        r = math.isqrt(disc.numerator*disc.denominator)
        issq = F(r, disc.denominator)**2 == disc
        print('  perfect square disc?', issq)
        if issq and a_coef != 0:
            sq = F(r, disc.denominator)
            t1 = (-b_coef - sq)/(2*a_coef)
            t2 = (-b_coef + sq)/(2*a_coef)
            d1 = [t1*e1[k]+e2[k] for k in range(3)]
            d2 = [t2*e1[k]+e2[k] for k in range(3)]
            print('  rational ruling 1:', d1)
            print('  rational ruling 2:', d2)
