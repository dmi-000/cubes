#!/usr/bin/env python3
"""Phase B: identify and count EVERY endpoint of every 727 continuum.

Phase A (`continua.py`) finds the maximal 727 stretches on each 727-carrying
line.  This takes each end of each stretch and answers three questions
exactly:

  WHERE   bisect to a tight bracket, then take the exact root of whichever
          catalogue condition changes sign inside it;
  WHICH   which wall type closes the interval -- edge-edge (linear in t),
          corner-on-face or W4 (quadratic), or W3 (QUARTIC, so the root can
          be an algebraic number of degree 4 that lies in no Q(sqrt d));
  WHAT    the exact region count AT the endpoint, which Postscript 62 shows
          differs from the interior AND from just outside.

INVARIANT: the endpoint configuration evaluated is the exact root.  A rational
sample "very close" to the endpoint is a different configuration with a
different count -- that is the entire finding of Postscript 62, so
approximating here would destroy the thing being measured.

Degree > 2 roots are REPORTED AS SUCH and not counted: the C++ engines are
Q(sqrt d) only, and counting a quartic point needs the degree-agnostic
`opencount.py` field engine.  Reporting "unable, degree 4" is a result; a
silently skipped endpoint is not.
"""
import collections
import json
import math
import subprocess
import sys
from fractions import Fraction as F

import sympy

from continua import (FIVE, FIXED_W, build_catalogues, count_many, peval,
                      restrict, to_quat)

FIXED_N = ';'.join(','.join(map(str, q)) for q in FIVE)


def count_one(q):
    r = count_many([q])
    return r[0] if r else None


def bisect(p0, dd, lo, hi, want_hi_727, depth=40):
    """Narrow [lo,hi] so that exactly one end counts 727."""
    for _ in range(depth):
        mid = (lo + hi) / 2
        q = to_quat(tuple(p0[u] + mid*dd[u] for u in range(3)))
        if q is None:
            break
        c = count_one(q)
        if c is None:
            break
        if (c == 727) == want_hi_727:
            hi = mid
        else:
            lo = mid
    return lo, hi


def squarefree(D):
    d, s = D, 1
    f = 2
    while f*f <= d:
        while d % (f*f) == 0:
            d //= f*f
            s *= f
        f += 1
    return d, s


def count_at_root(root, p0, dd):
    """Exact count at the configuration p0 + root*dd. Returns (count, note)."""
    x = sympy.Symbol('x')
    mp = sympy.minimal_polynomial(root, x)
    deg = sympy.degree(mp)
    if deg == 1:
        r = sympy.Rational(root)
        pt = tuple(F(r.p, r.q)*F(dd[u]) + F(p0[u]) for u in range(3))
        q = to_quat(pt, cap=10**8)
        if q is None:
            return None, 'rational root, components too large'
        out = subprocess.run(['./cube_regions_q2w', '--d', '0', '--quats',
                              FIXED_W + ';' + ','.join('%d:0' % v for v in q)],
                             capture_output=True, text=True).stdout
        try:
            return json.loads(out).get('bounded'), 'rational'
        except Exception:
            return None, 'engine error'
    if deg != 2:
        return None, 'degree %d root -- needs the degree-agnostic engine' % deg
    a2, a1, a0 = [sympy.Rational(c) for c in sympy.Poly(mp, x).all_coeffs()]
    disc = a1*a1 - 4*a2*a0
    D = sympy.Rational(disc)
    Dint = int(D) if D.q == 1 else None
    if Dint is None or Dint < 0:
        return None, 'non-integer or negative discriminant'
    sf, scale = squarefree(Dint)
    sq = sympy.sqrt(sf)
    comps = []
    for v in [sympy.Integer(1)] + [sympy.expand(sympy.radsimp(
            sympy.nsimplify(sympy.Rational(p0[u]) + root*sympy.Rational(dd[u]))))
            for u in range(3)]:
        pol = sympy.Poly(sympy.expand(v), sq)
        cs = pol.all_coeffs()[::-1]
        if len(cs) > 2:
            return None, 'nested radical'
        c0 = sympy.Rational(cs[0])
        c1 = sympy.Rational(cs[1]) if len(cs) > 1 else sympy.Rational(0)
        comps.append((F(c0.p, c0.q), F(c1.p, c1.q)))
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
    line = FIXED_W + ';' + ','.join('%d:%d' % c for c in ints)
    out = subprocess.run(['./cube_regions_q2w', '--d', str(sf),
                          '--quats-stdin'], input=line + '\n',
                         capture_output=True, text=True).stdout
    for l in out.splitlines():
        if l.startswith('{'):
            j = json.loads(l)
            return j.get('bounded'), 'Q(sqrt %d)' % sf
    return None, 'no engine output'


def main():
    cat = build_catalogues()
    data = json.load(open('typology_data.json'))
    recs = [json.loads(l) for l in open('continua_shard_0.jsonl')]
    todo = [(r['line'], run) for r in recs for run in r['runs']]
    print('continua found: %d, endpoints to analyse: %d'
          % (len(todo), 2*len(todo)), flush=True)

    tally = collections.Counter()
    out = open('continua_endpoints.jsonl', 'a')
    for li, (a, b) in todo:
        L = data['lines'][li]
        p0 = tuple(F(x) for x in L['p0'])
        dd = tuple(F(x) for x in L['dir'])
        restricted = {k: [restrict(m, p0, dd) for m in v]
                      for k, v in cat.items()}
        for side, lo0, hi0, want in (('lower', F(a) - F(1, 2), F(a), True),
                                     ('upper', F(b), F(b) + F(1, 2), False)):
            lo, hi = bisect(p0, dd, lo0, hi0, want)
            hits = []
            for kind, polys in restricted.items():
                for co in polys:
                    vlo, vhi = peval(co, lo), peval(co, hi)
                    if vlo == 0 or vhi == 0 or (vlo > 0) != (vhi > 0):
                        hits.append((kind, co))
            info = {'line': li, 'side': side, 'bracket': [str(lo), str(hi)],
                    'walls': sorted({k for k, _ in hits})}
            got = None
            for kind, co in hits:
                x = sympy.Symbol('x')
                expr = sum(sympy.Rational(c.numerator, c.denominator)*x**i
                           for i, c in enumerate(co))
                for r in sympy.real_roots(expr, x):
                    if sympy.Rational(lo.numerator, lo.denominator) <= r <= \
                            sympy.Rational(hi.numerator, hi.denominator):
                        cnt, note = count_at_root(r, p0, dd)
                        info.update({'wall': kind, 'root': str(r),
                                     'count': cnt, 'field': note})
                        got = (kind, cnt, note)
                        break
                if got:
                    break
            tally[(info.get('wall', 'NONE'), info.get('count'))] += 1
            print('line %3d %-5s bracket width %.2e  walls=%-28s -> %s'
                  % (li, side, float(hi-lo), ','.join(info['walls']) or 'none',
                     ('%s, count %s (%s)' % got) if got else 'no root found'),
                  flush=True)
            out.write(json.dumps(info) + '\n')
            out.flush()
    print('\nsummary (wall type, count at endpoint):')
    for k in sorted(tally, key=str):
        print('   %-28s %d' % (str(k), tally[k]))


if __name__ == '__main__':
    main()
