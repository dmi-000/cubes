#!/usr/bin/env python3
"""The full neighbourhood structure of n = 2.

Two cubes have 3 degrees of freedom and, by the taxonomy of Postscript 57,
only TWO wall types can exist (W3 needs 3 cubes, W4 needs 4). So n = 2 is the
one level where the whole configuration space can be mapped.

Random sampling already shows the coarse picture: only five counts occur —
1, 4, 5, 9, 13 — with depth profiles {d1, 1} for d1 in {0, 3, 4, 8, 12}, and
**13 is attained on 9.5% of random rotations**, an open set. So unlike n = 6,
where 727 needs to sit on two walls at once, the n = 2 maximum needs no
coincidence at all.

This maps what happens ON the walls. The corner-on-face conditions are
quadrics in Cayley coordinates and are written down directly here: with
q = (1,a,b,c), M the unnormalised rotation matrix and N = 1+a^2+b^2+c^2,

    corner s of B lands on face i of A :   (M s)_i -+ N = 0
    corner c of A lands on a face of B :   (M^T c)_a -+ N = 0

96 quadrics in all. Walking a segment between two chambers, the exact roots of
these give the wall crossings, and the count AT the root is the wall's own
value -- which Postscript 68 shows can be above or below its neighbours.

INVARIANT: the count at a wall is evaluated at the EXACT root, never at a
nearby rational. That distinction is the whole content of Postscripts 62 and
68.
"""
import collections
import json
import math
import subprocess
import sys
from fractions import Fraction as F

import sympy

from continua_endpoints import roots_of, squarefree


def quadrics():
    a, b, c = sympy.symbols('a b c')
    N = 1 + a*a + b*b + c*c
    M = [[1+a*a-b*b-c*c, 2*(a*b-c), 2*(a*c+b)],
         [2*(a*b+c), 1-a*a+b*b-c*c, 2*(b*c-a)],
         [2*(a*c-b), 2*(b*c+a), 1-a*a-b*b+c*c]]
    out = []
    signs = [(i, j, k) for i in (1, -1) for j in (1, -1) for k in (1, -1)]
    for s in signs:
        for i in range(3):
            e = sum(M[i][t]*s[t] for t in range(3))
            for sg in (1, -1):
                out.append(('B-corner-on-A-face', sympy.expand(e - sg*N)))
        for aidx in range(3):
            e = sum(M[t][aidx]*s[t] for t in range(3))
            for sg in (1, -1):
                out.append(('A-corner-on-B-face', sympy.expand(e - sg*N)))
    mono = []
    for tag, e in out:
        p = sympy.Poly(e, a, b, c)
        mono.append((tag, {tuple(m): F(int(v)) for m, v in
                           zip(p.monoms(), p.coeffs())}))
    return mono


def restrict(m, p0, dd):
    lin = [[p0[u], dd[u]] for u in range(3)]

    def pmul(x, y):
        o = [F(0)]*(len(x)+len(y)-1)
        for i, u in enumerate(x):
            if u:
                for j, v in enumerate(y):
                    if v:
                        o[i+j] += u*v
        return o
    tot = [F(0)]
    for (i, j, k), co in m.items():
        term = [co]
        for e, base in ((i, lin[0]), (j, lin[1]), (k, lin[2])):
            for _ in range(e):
                term = pmul(term, base)
        if len(term) > len(tot):
            tot = tot + [F(0)]*(len(term)-len(tot))
        for idx, v in enumerate(term):
            tot[idx] += v
    while len(tot) > 1 and tot[-1] == 0:
        tot.pop()
    return tot


def peval(co, t):
    s = F(0)
    for x in reversed(co):
        s = s*t + x
    return s


def to_quat(pt, cap=10**7):
    den = 1
    for v in pt:
        den = den * v.denominator // math.gcd(den, v.denominator)
    q = (den, int(pt[0]*den), int(pt[1]*den), int(pt[2]*den))
    g = 0
    for x in q:
        g = math.gcd(g, abs(x))
    q = tuple(x//g for x in q) if g > 1 else q
    return q if any(q) and max(abs(x) for x in q) <= cap else None


def count_rat(q):
    out = subprocess.run(['./cube_regions_n', '--quats',
                          '1,0,0,0;' + ','.join(map(str, q))],
                         capture_output=True, text=True).stdout
    try:
        return json.loads(out).get('bounded')
    except Exception:
        return None


def count_surd(root, p0, dd):
    P, Q, D = root
    comps = [(F(1), F(0))] + [(p0[u] + P*dd[u], Q*dd[u]) for u in range(3)]
    den = 1
    for pp, qq in comps:
        for v in (pp, qq):
            den = den * v.denominator // math.gcd(den, v.denominator)
    ints = [(int(pp*den), int(qq*den)) for pp, qq in comps]
    g = 0
    for pp, qq in ints:
        g = math.gcd(g, math.gcd(abs(pp), abs(qq)))
    if g > 1:
        ints = [(pp//g, qq//g) for pp, qq in ints]
    if max(max(abs(x), abs(y)) for x, y in ints) > 10**7:
        return None, 'too large'
    ident = ','.join('%d:0' % v for v in (1, 0, 0, 0))
    line = ident + ';' + ','.join('%d:%d' % c for c in ints)
    out = subprocess.run(['./cube_regions_q2w', '--d', str(D),
                          '--quats-stdin'], input=line + '\n',
                         capture_output=True, text=True).stdout
    for l in out.splitlines():
        if l.startswith('{'):
            return json.loads(l).get('bounded'), ('rational' if D == 0
                                                  else 'Q(sqrt %d)' % D)
    return None, 'no output'


def main():
    quads = quadrics()
    print('corner-on-face quadrics for n=2: %d' % len(quads))
    # a segment through configuration space, chosen to cross several chambers
    p0 = (F(1, 5), F(1, 3), F(1, 7))
    dd = (F(1), F(2, 3), F(-1, 2))
    lo, hi = F(-2), F(2)
    step = F(1, 64)
    ts, qs = [], []
    t = lo
    while t <= hi:
        q = to_quat(tuple(p0[u] + t*dd[u] for u in range(3)))
        if q:
            ts.append(t)
            qs.append(q)
        t += step
    inp = '\n'.join('1,0,0,0;' + ','.join(map(str, q)) for q in qs) + '\n'
    out = subprocess.run(['./cube_regions_n', '--quats-stdin'], input=inp,
                         capture_output=True, text=True).stdout
    rows = [json.loads(l).get('bounded') for l in out.splitlines()
            if l.startswith('{')]
    assert len(rows) == len(qs)
    seq = list(zip(ts, rows))
    runs = []
    cur = None
    for t, c in seq:
        if cur is None or cur[0] != c:
            cur = [c, t, t]
            runs.append(cur)
        else:
            cur[2] = t
    print('chambers along the segment: %s'
          % ' '.join('%s[%s..%s]' % (c, a, b) for c, a, b in runs))

    print('\ncount AT each wall between consecutive chambers:')
    for i in range(len(runs) - 1):
        left, right = runs[i], runs[i+1]
        a, b = left[2], right[1]
        best = None
        for tag, m in quads:
            co = restrict(m, p0, dd)
            if all(x == 0 for x in co) or len(co) < 2:
                continue
            va, vb = peval(co, a), peval(co, b)
            if va == 0 or vb == 0 or (va > 0) != (vb > 0):
                rs = roots_of(co, a, b)
                if rs:
                    cnt, fld = count_surd(rs[0], p0, dd)
                    best = (tag, rs[0], cnt, fld)
                    break
        if best:
            tag, r, cnt, fld = best
            print('   %2d -> %2d : wall %-20s count AT wall = %-5s (%s)'
                  % (left[0], right[0], tag, cnt, fld))
        else:
            print('   %2d -> %2d : no corner-on-face wall found (edge-edge?)'
                  % (left[0], right[0]))


if __name__ == '__main__':
    main()
