#!/usr/bin/env python3
"""What actually bounds a type-chamber of the 727 plateau?

Postscript 54 established that a per-label TYPE is a chamber of a wall line,
and TYPOLOGY.md guessed that the zero-width ones sit where extra coincidences
meet.  Sharpened: a chamber boundary should be a parameter value where a THIRD
condition activates (two define the line).  So along one line,

    #type changes  ==  #wall crossings,   and each change brackets a crossing.

WHAT THE FIRST VERSION OF THIS SCRIPT GOT WRONG, kept here because the mistake
is easy to repeat: it evaluated the condition catalogue AT the sampled points
and asked whether the type changed there.  Wall crossings are measure zero, so
sampled rationals essentially never land on one; the test reported "25 of 27
type changes have no active condition" when what it had actually measured is
that a sample rarely sits exactly on a wall.  The right test restricts every
condition TO the line, solves for its roots in the sampled range, and compares
the root count with the observed change count.

CATALOGUES.  Restricted to the line, an edge-edge plane is linear in t and a
corner-on-face quadric is quadratic in t.  Postscript 57's newly catalogued W4
walls -- a free-cube face plane through one of the base's 424 real triple
points -- are also quadratic in t, and are included here, since the whole
question is whether the enumerated conditions suffice to explain the chamber
structure or whether the unenumerated types are doing the work.

INVARIANT: exact arithmetic for root existence AND for locating a root inside
a sample bracket.  A root at a bracket endpoint, or two roots inside one
bracket, is exactly the situation a float comparison would misreport, and it
is the situation this test is trying to resolve.
"""
import collections
import json
import math
import pickle
import subprocess
import sys
from fractions import Fraction as F

import sympy

from base_points import FIVE, mat
from incidence2 import base_catalogue

FIVES = ';'.join(','.join(map(str, q)) for q in FIVE)


def quad_coeffs():
    """corner-on-face quadrics as {(i,j,k): int} monomial dicts."""
    raw = pickle.load(open('corner_conds.pkl', 'rb'))
    syms = set()
    for cube in raw:
        for e in raw[cube]:
            syms |= e.free_symbols
    a, b, c = sorted(syms, key=str)      # pickled symbols carry real=True;
    out = []                             # fresh symbols() would be different
    for cube in sorted(raw):             # objects and Poly would treat them
        for e in raw[cube]:              # as coefficients
            p = sympy.Poly(e, a, b, c)
            out.append({tuple(m): int(v) for m, v in
                        zip(p.monoms(), p.coeffs())})
    return out


def w4_polys(pts):
    """W4 walls as monomial dicts in (a,b,c).

    With q = (1,a,b,c) the unnormalised rotation matrix is M / N,
    N = 1+a^2+b^2+c^2, so "face plane of axis j through base point p" is
    M[:,j] . p -+ N = 0 -- a quadric with integer coefficients."""
    a, b, c = sympy.symbols('a b c')
    N = 1 + a*a + b*b + c*c
    M = [[1+a*a-b*b-c*c, 2*(a*b-c), 2*(a*c+b)],
         [2*(a*b+c), 1-a*a+b*b-c*c, 2*(b*c-a)],
         [2*(a*c-b), 2*(b*c+a), 1-a*a-b*b+c*c]]
    out = []
    for p, npl, ncub in pts:
        den = 1
        for v in p:
            den = den * v.denominator // math.gcd(den, v.denominator)
        pi = [int(v*den) for v in p]
        for j in range(3):
            colp = sum(M[i][j]*pi[i] for i in range(3))
            for s in (1, -1):
                e = sympy.expand(colp - s*den*N)
                pl = sympy.Poly(e, a, b, c)
                out.append({tuple(m): int(v) for m, v in
                            zip(pl.monoms(), pl.coeffs())})
    return out


def restrict(mono, p0, dd):
    """Substitute the line p0 + t*dd into a monomial dict; return [c0,c1,c2]."""
    t = sympy.Symbol('t')
    expr = 0
    for (i, j, k), v in mono.items():
        expr += v * ((p0[0] + t*dd[0])**i * (p0[1] + t*dd[1])**j
                     * (p0[2] + t*dd[2])**k)
    p = sympy.Poly(sympy.expand(expr), t)
    co = [sympy.Rational(0)]*3
    for m, v in zip(p.monoms(), p.coeffs()):
        if m[0] <= 2:
            co[m[0]] = sympy.Rational(v)
        elif v != 0:
            raise ValueError('degree %d on the line' % m[0])
    return co


def roots_in(co, lo, hi):
    """Exact real roots of c0 + c1 t + c2 t^2 inside [lo, hi]."""
    c0, c1, c2 = co
    out = []
    if c2 == 0:
        if c1 == 0:
            return []
        r = sympy.Rational(-c0, c1)
        if lo <= r <= hi:
            out.append(r)
        return out
    D = c1*c1 - 4*c2*c0
    if D < 0:
        return []
    sq = sympy.sqrt(D)
    for s in (1, -1):
        r = sympy.nsimplify((-c1 + s*sq) / (2*c2))
        if lo <= r <= hi:
            out.append(r)      # simplify() here dominated the runtime and the
        # comparisons below are exact on the unsimplified form anyway
        if D == 0:
            break
    return out


def to_quat(pt, cap=100000):
    den = 1
    for v in pt:
        den = den * v.denominator // math.gcd(den, v.denominator)
    q = (den, int(pt[0]*den), int(pt[1]*den), int(pt[2]*den))
    g = 0
    for x in q:
        g = math.gcd(g, abs(x))
    q = tuple(x//g for x in q) if g > 1 else q
    return q if any(q) and max(abs(x) for x in q) <= cap else None


def main():
    nlines = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    den = int(sys.argv[2]) if len(sys.argv) > 2 else 16
    LO = F(sys.argv[3]) if len(sys.argv) > 3 else F(-4)
    HI = F(sys.argv[4]) if len(sys.argv) > 4 else F(4)
    first = int(sys.argv[5]) if len(sys.argv) > 5 else 0
    data = json.load(open('typology_data.json'))
    planeset = pickle.load(open('locus_planes.pkl', 'rb'))
    planes = [p for cube in sorted(planeset) for p in planeset[cube]]
    quads = quad_coeffs()
    pts, _ = base_catalogue()
    w4 = w4_polys(pts)
    print('catalogue: %d edge-edge planes, %d corner-on-face quadrics,'
          ' %d W4 quadrics' % (len(planes), len(quads), len(w4)), flush=True)

    for li, L in enumerate(data['lines'][first:first+nlines], start=first):
        p0 = tuple(sympy.Rational(x) for x in L['p0'])
        dd = tuple(sympy.Rational(x) for x in L['dir'])
        # --- exact wall crossings on the line, by catalogue -----------------
        groups = {'edge-edge': [], 'corner-face': [], 'W4': []}
        for A, B, C, D in planes:
            co = restrict({(1, 0, 0): A, (0, 1, 0): B, (0, 0, 1): C,
                           (0, 0, 0): D}, p0, dd)
            groups['edge-edge'] += roots_in(co, LO, HI)
        for m in quads:
            groups['corner-face'] += roots_in(restrict(m, p0, dd), LO, HI)
        for m in w4:
            groups['W4'] += roots_in(restrict(m, p0, dd), LO, HI)
        allroots = sorted(set().union(*[set(v) for v in groups.values()]),
                          key=lambda r: float(r))

        # --- observed type changes ------------------------------------------
        samples = []
        n = int((HI - LO) * den)
        for i in range(n + 1):
            t = LO + F(i, den)
            pt = tuple(F(str(p0[u])) + t*F(str(dd[u])) for u in range(3))
            q = to_quat(pt)
            if q is not None:
                samples.append((sympy.Rational(t.numerator, t.denominator), q))
        inp = '\n'.join(FIVES + ';' + ','.join(map(str, q))
                        for _, q in samples) + '\n'
        out = subprocess.run(['./cube_regions_n', '--quats-stdin'], input=inp,
                             capture_output=True, text=True).stdout
        rows = [json.loads(l) for l in out.splitlines() if l.startswith('{')]
        seq = [(t, d.get('bounded'),
                tuple(sorted(d['per_label'].items())) if d.get('bounded') else None)
               for (t, _), d in zip(samples, rows)]

        changes = [(seq[i-1][0], seq[i][0]) for i in range(1, len(seq))
                   if (seq[i-1][1], seq[i-1][2]) != (seq[i][1], seq[i][2])]
        explained = 0
        for lo, hi in changes:
            if any(lo <= r <= hi for r in allroots):
                explained += 1
        # how many changes would be explained WITHOUT the new W4 walls
        old = sorted(set(groups['edge-edge']) | set(groups['corner-face']),
                     key=lambda r: float(r))
        explained_old = sum(1 for lo, hi in changes
                            if any(lo <= r <= hi for r in old))
        n727 = sum(1 for _, tot, _ in seq if tot == 727)

        print('\nline %d over t in [%s, %s], step 1/%d' % (li, LO, HI, den))
        print('   %d samples, %d count 727, %d type changes' %
              (len(seq), n727, len(changes)))
        print('   wall crossings on the line: edge-edge %d, corner-face %d,'
              ' W4 %d, distinct %d'
              % (len(groups['edge-edge']), len(groups['corner-face']),
                 len(groups['W4']), len(allroots)))
        print('   type changes bracketing a known crossing:'
              ' %d/%d with W4, %d/%d without'
              % (explained, len(changes), explained_old, len(changes)),
              flush=True)


if __name__ == '__main__':
    main()
