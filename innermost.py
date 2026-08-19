#!/usr/bin/env python3
"""Measure m = comp(cube i is INNERMOST), the last unmeasured term of the law.

Postscript 106's addendum derives the singleton term from inclusion-exclusion for
the compactly-supported Euler characteristic on S^2:

    s = comp(K n L) = a + b + m - 2,
        K = {r_i > r_j}  (a components),  L = {r_i > r_k}  (b components),
        m = comp(C),  C = {r_i <= r_j and r_i <= r_k} = where cube i is INNERMOST.

The fitted constant +4 says m = 6, one component per face of cube i -- but m had
never been computed; it was inferred backwards from the fit.  This computes it
exactly, so the identity can be tested PER CONFIGURATION rather than only where
m happens to be 6.

THE GEOMETRY.  Every cube here is [-1,1]^3 under a rotation, so its radial extent
in direction u is r(u) = 1 / max_f |n_f . u| over its three face normals, and the
box's own is 1 / ||u||_inf.  Hence

    C = { u : |n_f . u| <= ||u||_inf for all f of cube j and all of cube k }.

C is a CONE, so cut it by which coordinate attains ||u||_inf: in the sector
sigma*u_t = ||u||_inf, normalise u_t = sigma and the remaining two coordinates run
over the square [-1,1]^2, where every condition |n . u| <= 1 is a pair of linear
inequalities.  So C meets each of the six sectors in a CONVEX POLYGON, computed
here by exact rational half-plane clipping, and m is a union-find over the six,
two sectors being joined when their traces on the shared wall meet.

Same shape as Step A's six convex slabs for A \\ B -- six convex pieces, glue by
an exact feasibility test -- which is why m <= 6 is immediate and only the
merging is at issue.

Run: python3 innermost.py
"""
import itertools
import random
import sys
from fractions import Fraction as F

sys.path.insert(0, HERE)
from step_a2 import normals
from step_a3 import components
from step_b import singleton_comp, UF
import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__))

SQUARE = [(F(-1), F(-1)), (F(1), F(-1)), (F(1), F(1)), (F(-1), F(1))]


def clip(poly, a, b, c):
    """Clip convex polygon to the half-plane a*x + b*y <= c (exact)."""
    if not poly:
        return []
    out = []
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        d1 = a * x1 + b * y1 - c
        d2 = a * x2 + b * y2 - c
        if d1 <= 0:
            out.append((x1, y1))
        if (d1 < 0 < d2) or (d2 < 0 < d1):
            t = d1 / (d1 - d2)
            out.append((x1 + t * (x2 - x1), y1 + t * (y2 - y1)))
    return out


def sector_polygon(t, sigma, normal_sets):
    """C restricted to the sector sigma*u_t = ||u||_inf, in the two free coords."""
    p, q = [r for r in range(3) if r != t]
    poly = list(SQUARE)
    for ns in normal_sets:
        for n in ns:
            # |n . u| <= 1 with u_t = sigma, u_p = x, u_q = y
            poly = clip(poly, n[p], n[q], 1 - n[t] * sigma)
            poly = clip(poly, -n[p], -n[q], 1 + n[t] * sigma)
            if not poly:
                return []
    return poly


def trace_on_wall(poly, axis_index, value):
    """Interval (lo, hi) of the other coordinate where poly meets the square's
    edge {coord axis_index == value}; None if it does not reach it."""
    other = 1 - axis_index
    pts = [v[other] for v in poly if v[axis_index] == value]
    if not pts:
        return None
    return (min(pts), max(pts))


def comp_innermost(nj, nk, detail=False):
    """m = number of connected components of {cube i innermost}."""
    sectors = [(t, s) for t in range(3) for s in (F(1), F(-1))]
    polys = {}
    for t, s in sectors:
        poly = sector_polygon(t, s, (nj, nk))
        if poly:
            polys[(t, s)] = poly
    keys = list(polys)
    uf = UF(len(keys))
    touching = 0
    for i, j in itertools.combinations(range(len(keys)), 2):
        (t1, s1), (t2, s2) = keys[i], keys[j]
        if t1 == t2:
            continue                       # opposite sectors share no wall
        free1 = [r for r in range(3) if r != t1]
        free2 = [r for r in range(3) if r != t2]
        # in sector 1 the wall toward sector 2 is {coord of axis t2 == s2}
        a1 = free1.index(t2)
        a2 = free2.index(t1)
        i1 = trace_on_wall(polys[keys[i]], a1, s2)
        i2 = trace_on_wall(polys[keys[j]], a2, s1)
        if i1 is None or i2 is None:
            continue
        lo, hi = max(i1[0], i2[0]), min(i1[1], i2[1])
        if lo < hi:
            uf.union(i, j)
        elif lo == hi:
            touching += 1
            uf.union(i, j)                 # C is closed: a shared point connects
    m = uf.count()
    return (m, len(keys), touching) if detail else m


def check(qa, qb, label=''):
    nj, nk = normals(qa), normals(qb)
    a = components(nj)
    b = components(nk)
    s = singleton_comp(nj, nk)[0]
    m, sec, touch = comp_innermost(nj, nk, detail=True)
    pred = a + b + m - 2
    return dict(label=label, a=a, b=b, s=s, m=m, sectors=sec, touching=touch,
                predicted=pred, ok=(s == pred))


WITNESSES = {
    '(13,13)': ((1, 2, 1, 1), (-2, 1, 0, -1)),
    '(13,9)': ((2, 1, 1, 1), (2, -1, -2, 0)),
    '(13,5)': ((2, 3, 0, 2), (1, 2, -3, -1)),
    '(13,4)': ((0, 4, 3, 1), (2, -3, 1, -5)),
    '(9,9)': ((-1, 0, 2, 2), (-2, 1, -2, 0)),
    '(9,5)': ((0, -2, 1, 2), (2, 3, 1, -1)),
    '(5,5)': ((-1, -3, -2, -1), (-2, -3, 3, 1)),
    '(4,4)': ((-2, -1, 3, -5), (5, -1, 3, -2)),
}


def main():
    print('THE EIGHT SHARD WITNESSES')
    print('%-9s %-3s %-3s %-4s %-3s %-9s %-5s' %
          ('combo', 'a', 'b', 's', 'm', 'a+b+m-2', 'ok'))
    for k, (qa, qb) in WITNESSES.items():
        r = check(qa, qb, k)
        print('%-9s %-3d %-3d %-4d %-3d %-9d %-5s' %
              (k, r['a'], r['b'], r['s'], r['m'], r['predicted'], r['ok']))

    print('\nRANDOM PAIRS -- does the identity survive where m may not be 6?')
    rng = random.Random(11)
    tally = {}
    bad = []
    n = 0
    for _ in range(400):
        h = rng.choice([2, 3, 5, 9])
        qa = tuple(rng.randint(-h, h) for _ in range(4))
        qb = tuple(rng.randint(-h, h) for _ in range(4))
        if not any(qa) or not any(qb):
            continue
        r = check(qa, qb)
        n += 1
        tally[r['m']] = tally.get(r['m'], 0) + 1
        if not r['ok']:
            bad.append((qa, qb, r))
    print('  %d pairs; m distribution: %s' % (n, dict(sorted(tally.items()))))
    print('  identity s = a + b + m - 2 holds: %d, fails: %d' % (n - len(bad), len(bad)))
    for qa, qb, r in bad[:5]:
        print('    FAIL %s %s  a=%d b=%d m=%d s=%d predicted=%d'
              % (qa, qb, r['a'], r['b'], r['m'], r['s'], r['predicted']))


if __name__ == '__main__':
    main()
