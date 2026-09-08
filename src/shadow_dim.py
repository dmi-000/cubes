#!/usr/bin/env python3
"""Is an irrational 727 a chamber INTERIOR point (a continuum) or a BOUNDARY?

Postscript 58: a type-chamber of a wall line is bounded by wall crossings, and
two conditions define the line, so a point with k == 2 active conditions is
interior to a chamber -- a continuum of its own combinatorial type -- while
k >= 3 makes it a crossing, a zero-dimensional stratum.

This counts k exactly, in Q(sqrt d), for every distinct irrational 727 the
mixed strata produced.  It decides the question "are the irrational
configurations with rational shadows part of a continuum?" at the level of the
CONFIGURATION rather than of the count.

INVARIANT: exact Z[sqrt d] arithmetic; a wall is active iff the condition
polynomial vanishes identically in the field, never within a tolerance.
"""
import collections, json, pickle, sympy
from fractions import Fraction as F


def make_field(D):
    class Q:
        __slots__ = ('p', 'q')
        def __init__(s, p, q=0): s.p = F(p); s.q = F(q)
        def __add__(s, o): o = cv(o); return Q(s.p+o.p, s.q+o.q)
        __radd__ = __add__
        def __sub__(s, o): o = cv(o); return Q(s.p-o.p, s.q-o.q)
        def __rsub__(s, o): return cv(o).__sub__(s)
        def __mul__(s, o):
            o = cv(o); return Q(s.p*o.p + D*s.q*o.q, s.p*o.q + s.q*o.p)
        __rmul__ = __mul__
        def __truediv__(s, o):
            o = cv(o); n = o.p*o.p - D*o.q*o.q
            return Q((s.p*o.p - D*s.q*o.q)/n, (s.q*o.p - s.p*o.q)/n)
        def __pow__(s, n):
            r = Q(1)
            for _ in range(n): r = r*s
            return r
        def zero(s): return s.p == 0 and s.q == 0
    def cv(o): return o if isinstance(o, Q) else Q(o)
    return Q


def catalogue():
    planes = pickle.load(open('locus_planes.pkl', 'rb'))
    plist = [p for k in sorted(planes) for p in planes[k]]
    raw = pickle.load(open('corner_conds.pkl', 'rb'))
    syms = set()
    for k in raw:
        for e in raw[k]: syms |= e.free_symbols
    sa, sb, sc = sorted(syms, key=str)
    quads = []
    for k in sorted(raw):
        for e in raw[k]:
            p = sympy.Poly(e, sa, sb, sc)
            quads.append({tuple(m): int(v) for m, v in
                          zip(p.monoms(), p.coeffs())})
    return plist, quads


def main():
    plist, quads = catalogue()
    hits = [r for r in (json.loads(l) for l in open('mixed_q2_hits.jsonl'))
            if r['total'] == 727]
    byd = collections.defaultdict(set)
    for r in hits:
        byd[r['d']].add(tuple(tuple(c) for c in r['quat']))

    kdist = collections.Counter()
    interior = []
    for D in sorted(byd):
        Q = make_field(D)
        for quat in sorted(byd[D]):
            w, x, y, z = [Q(p, q) for p, q in quat]
            if w.zero():
                kdist['w=0 (chart edge, skipped)'] += 1
                continue
            a, b, c = x/w, y/w, z/w
            k = 0
            for A, B, C, Dd in plist:
                if (A*a + B*b + C*c + Dd).zero():
                    k += 1
            for m in quads:
                s = Q(0)
                for (i, j, l), v in m.items():
                    s = s + v*(a**i)*(b**j)*(c**l)
                if s.zero():
                    k += 1
            kdist[k] += 1
            if k <= 2:
                interior.append((D, quat, k))
    print('active-wall count k over every distinct irrational 727:')
    for k in sorted(kdist, key=str):
        print('   k = %-4s : %d configurations' % (k, kdist[k]))
    print('\nk <= 2 (chamber interior -> a continuum of its own type): %d'
          % len(interior))
    for D, quat, k in interior[:5]:
        print('   d=%d %s k=%d' % (D, quat, k))


if __name__ == '__main__':
    main()
