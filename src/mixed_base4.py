#!/usr/bin/env python3
# Working principles: mixed_q2_full.py (the n=6 version, verified); this is the
# same method with the fixed base as a parameter.
"""Irrational strata over an arbitrary rational base: can they reach the record?

At n=6 the mixed strata (two edge-edge PLANES against two fixed cubes, one
corner QUADRIC against a third) turned out to contain 224 184 countable
irrational configurations, eight of whose congruence classes reach the record
727.  That undercut the claim that n=3 is the tower's unique irrational rung
(Postscript 51 addendum 5) -- but only at n=6, because no other base had been
enumerated.

This asks the same question between 3 and 6.  Fix the (n-1)-cube subset of a
record and let one cube range over the wall strata:

    n=4 base: three cubes of the 183 record   -> can a fourth reach 183?
    n=5 base: four cubes of the 393 record    -> can a fifth reach 393?

If irrational configurations match the records at these levels too, then
irrational strata are simply part of the landscape everywhere and n=3's
distinction narrows to REQUIREMENT (no rational configuration attains 67),
resting on one conditional theorem.  If they fall short, something really does
change between n=3 and n>=4 -- and the obvious suspect is the cap-sum
tightness boundary, which changes at exactly n=4.

INVARIANT: exact rational arithmetic in the enumeration (Fraction); counts come
from cube_regions_q2, whose overflow guard rejects rather than truncates.  A
discriminant is a perfect square only when its exact rational root is verified.
"""
import itertools
import json
import math
import os
import pickle
import subprocess
import sys
import tempfile
from fractions import Fraction as F

import sympy as sp

import record_hunt as R

a, b, c = sp.symbols('a b c', real=True)

# the four 3-subsets of the 183 record, i.e. every base from which a fourth
# cube can complete it; the earlier n=4 run used only the first.
BASES_N4 = [
    [(1, 0, 0, 0), (0, 5, 3, 2), (1, -4, -1, 1)],
    [(1, 0, 0, 0), (0, 5, 3, 2), (1, 1, -1, -4)],
    [(1, 0, 0, 0), (1, -4, -1, 1), (1, 1, -1, -4)],
    [(0, 5, 3, 2), (1, -4, -1, 1), (1, 1, -1, -4)],
]
BASES = {
    4: BASES_N4[0],
    5: [(1, 0, 0, 0), (0, 5, 3, 2), (1, -4, -1, 1), (1, 1, -1, -4)],  # 183 itself
    6: [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5), (2, 1, 1, 1), (1, 1, 1, 1)],
}
RECORD = {4: 183, 5: 393, 6: 727}
MAXCOMP = 4000


def rot(q):
    w, x, y, z = q
    n = w * w + x * x + y * y + z * z
    return sp.Matrix([[w*w+x*x-y*y-z*z, 2*(x*y-w*z), 2*(x*z+w*y)],
                      [2*(x*y+w*z), w*w-x*x+y*y-z*z, 2*(y*z-w*x)],
                      [2*(x*z-w*y), 2*(y*z+w*x), w*w-x*x-y*y+z*z]]) / n


def edges(M):
    out = []
    for ax in range(3):
        o1, o2 = [t for t in range(3) if t != ax]
        for s in (-1, 1):
            for t in (-1, 1):
                out.append((s * M[:, o1] + t * M[:, o2], M[:, ax]))
    return out


def build(base, tag):
    """Planes (from edge-edge walls) and quadrics (corner-on-face), per cube."""
    cache = 'mixed_base_%s.pkl' % tag
    if os.path.exists(cache):
        return pickle.load(open(cache, 'rb'))
    M6 = rot((1, a, b, c))
    e6 = edges(M6)
    corners6 = [M6 * sp.Matrix(s) for s in itertools.product((1, -1), repeat=3)]
    planes, quads = {}, {}
    for j, q in enumerate(base):
        Rj = rot(q)
        ef = edges(Rj)
        P = set()
        for x1, x2 in itertools.product(e6, ef):
            det = sp.Matrix.hstack(x1[1], x2[1], x2[0] - x1[0]).det()
            num = sp.expand(sp.together(sp.simplify(det)).as_numer_denom()[0])
            if num == 0:
                continue
            for f, _ in sp.factor_list(num)[1]:
                p = sp.Poly(f, a, b, c)
                if p.total_degree() != 1:
                    continue
                co = [sp.Rational(p.coeff_monomial(m)) for m in (a, b, c, 1)]
                g = sp.ilcm(*[x.q for x in co])
                co = [int(x * g) for x in co]
                nz = [abs(x) for x in co if x]
                d0 = nz[0]
                for v in nz[1:]:
                    d0 = math.gcd(d0, v)
                co = [x // (d0 or 1) for x in co]
                for x in co:
                    if x:
                        if x < 0:
                            co = [-y for y in co]
                        break
                P.add(tuple(co))
        planes[j] = sorted(P)
        Q = set()
        cj = [Rj * sp.Matrix(t) for t in itertools.product((1, -1), repeat=3)]
        for k in range(3):
            for sgn in (1, -1):
                for cor in corners6:
                    e = (Rj[:, k].T * cor)[0, 0] - sgn
                    num = sp.expand(sp.together(sp.simplify(e)).as_numer_denom()[0])
                    if num != 0:
                        Q.add(sp.factor(num))
                for v in cj:
                    e = (M6[:, k].T * v)[0, 0] - sgn
                    num = sp.expand(sp.together(sp.simplify(e)).as_numer_denom()[0])
                    if num != 0:
                        Q.add(sp.factor(num))
        quads[j] = [quad_coeffs(x) for x in sorted(Q, key=sp.default_sort_key)]
        print('  cube %d: %d planes, %d quadrics' % (j, len(planes[j]),
                                                     len(quads[j])), flush=True)
    pickle.dump((planes, quads), open(cache, 'wb'))
    return planes, quads


def quad_coeffs(P):
    p = sp.Poly(sp.expand(P), a, b, c)
    return {m: F(int(sp.Rational(co).p), int(sp.Rational(co).q))
            for m, co in zip(p.monoms(), p.coeffs())}


def qeval(co, pt):
    v = F(0)
    for (i, j, k), cf in co.items():
        v += cf * pt[0] ** i * pt[1] ** j * pt[2] ** k
    return v


def line_of(p, q):
    n1, n2 = p[:3], q[:3]
    d = (n1[1]*n2[2]-n1[2]*n2[1], n1[2]*n2[0]-n1[0]*n2[2], n1[0]*n2[1]-n1[1]*n2[0])
    if not any(d):
        return None
    k = max(range(3), key=lambda i: abs(d[i]))
    i, j = [t for t in range(3) if t != k]
    det = n1[i]*n2[j] - n1[j]*n2[i]
    if det == 0:
        return None
    r1, r2 = -p[3], -q[3]
    pt = [F(0), F(0), F(0)]
    pt[i] = F(r1*n2[j] - r2*n1[j], det)
    pt[j] = F(n1[i]*r2 - n2[i]*r1, det)
    return tuple(pt), tuple(F(x) for x in d)


def isqrt_exact(fr):
    if fr < 0:
        return None
    n, dd = fr.numerator, fr.denominator
    rn, rd = math.isqrt(n), math.isqrt(dd)
    return F(rn, rd) if rn*rn == n and rd*rd == dd else None


def squarefree(m):
    sf, d0 = 1, 2
    while d0 * d0 <= m:
        e = 0
        while m % d0 == 0:
            m //= d0
            e += 1
        if e % 2:
            sf *= d0
        d0 += 1
    return sf * m


def main():
    n = int(sys.argv[1])
    which = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    base = BASES_N4[which] if n == 4 else BASES[n]
    rec = RECORD[n]
    print('base variant %d' % which, flush=True)
    print('base: %d fixed cubes, target n=%d record %d' % (len(base), n, rec),
          flush=True)
    planes, quads = build(base, 'n%d_%d' % (n, which if n==4 else 0))

    bycls, nsys = {}, 0
    idx = range(len(base))
    for tri in itertools.combinations(idx, min(3, len(base))):
        for qi in tri:
            others = [t for t in tri if t != qi]
            if len(others) < 2:
                continue
            pi, pj = others
            for P1 in planes[pi]:
                for P2 in planes[pj]:
                    L = line_of(P1, P2)
                    if L is None:
                        continue
                    p0, dd = L
                    s1 = tuple(p0[t] + dd[t] for t in range(3))
                    s2 = tuple(p0[t] - dd[t] for t in range(3))
                    for co in quads[qi]:
                        nsys += 1
                        C0, Cp, Cm = qeval(co, p0), qeval(co, s1), qeval(co, s2)
                        A = (Cp + Cm - 2*C0) / 2
                        B = (Cp - Cm) / 2
                        if A == 0:
                            continue
                        disc = B*B - 4*A*C0
                        if disc <= 0 or isqrt_exact(disc) is not None:
                            continue            # rational or no real root
                        sf = squarefree(disc.numerator * disc.denominator)
                        r = isqrt_exact(disc / sf)
                        if r is None:
                            continue
                        for sgn in (1, -1):
                            comps = []
                            for u in range(3):
                                al = p0[u] + (-B)/(2*A)*dd[u]
                                be = sgn*r/(2*A)*dd[u]
                                comps.append((al, be))
                            L2 = 1
                            for al, be in comps:
                                for v in (al, be):
                                    L2 = L2*v.denominator // math.gcd(L2, v.denominator)
                            quad = ((L2, 0),) + tuple((int(al*L2), int(be*L2))
                                                      for al, be in comps)
                            if max(abs(x) for pr in quad for x in pr) <= MAXCOMP:
                                bycls.setdefault(sf, set()).add(quad)
    print('systems %d -> %d fields, %d candidate configs'
          % (nsys, len(bycls), sum(len(v) for v in bycls.values())), flush=True)

    fixed = ';'.join(','.join('%d:0' % x for x in q) for q in base)
    out = open('mixed_base_n%d_%d_hits.jsonl' % (n, which if n==4 else 0), 'a')
    best, counted, rejected = (0, None, None), 0, 0
    for sf in sorted(bycls, key=lambda k: -len(bycls[k])):
        cfgs = sorted(bycls[sf])
        lines = [fixed + ';' + ','.join('%d:%d' % t for t in q) for q in cfgs]
        with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as fh:
            fh.write('\n'.join(lines) + '\n')
            path = fh.name
        p = subprocess.run(['./cube_regions_q2', '--d', str(sf), '--quats-stdin'],
                           stdin=open(path), capture_output=True, text=True)
        got = 0
        for line, q in zip(p.stdout.splitlines(), cfgs):
            if not line.startswith('{'):
                continue
            d = json.loads(line)
            if 'bounded' not in d:
                continue
            got += 1
            t = d['bounded']
            if t > best[0]:
                best = (t, sf, q)
            if t >= rec - 4:
                out.write(json.dumps({'d': sf, 'total': t, 'quat': q,
                                      'by_depth': d['by_depth']}) + '\n')
                out.flush()
                if t >= rec:
                    print('  *** n=%d TOTAL %d (record %d) in Q(sqrt%d): %s'
                          % (n, t, rec, sf, q), flush=True)
        counted += got
        rejected += len(cfgs) - got
        os.unlink(path)
    print('\nn=%d: counted %d irrational configs, rejected %d; best %s'
          % (n, counted, rejected, best), flush=True)
    print('record is %d -> irrational strata %s it'
          % (rec, 'REACH' if best[0] >= rec else 'fall short of'), flush=True)


if __name__ == '__main__':
    main()
