#!/usr/bin/env python3
"""Census of the 727 continua and EVERY one of their endpoints.

Postscript 62 and its addendum analysed both ends of ONE line: the interval is
open, both endpoints irrational, one a W3 wall and one a W4, both counting 725
with the same depth profile.  Two endpoints of one line is an anecdote.  This
takes all the 727-carrying lines of `typology_data.json` and, for each maximal
727 stretch, locates both ends exactly, identifies which wall closes them, and
counts the configuration sitting there.

PHASE A  coarse scan per line -> maximal runs of 727 -> how many continua, how
         long, how many endpoints in total.
PHASE B  per endpoint: bisect to a tight bracket; find every catalogue
         condition changing sign inside it (edge-edge linear, corner-on-face
         and W4 quadratic, W3 QUARTIC); take the exact root; build the exact
         configuration and count it.

All four wall catalogues are carried as monomial dicts in (a,b,c) and
restricted to each line with pure-Fraction polynomial arithmetic -- sympy is
used only to build W3 once (cached) and to extract exact roots, never in the
per-line loop, which would otherwise dominate the runtime.

INVARIANT: an endpoint is identified by an EXACT sign change of an exact
rational polynomial across the bisection bracket, and the configuration
evaluated is the exact root, not a nearby rational.  A "very close" rational
is a different configuration and answers a different question -- the whole
point of Postscript 62 is that the endpoint's count differs from its
neighbours'.
"""
import collections
import json
import math
import os
import pickle
import subprocess
import sys
from fractions import Fraction as F

FIVE = [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5), (2, 1, 1, 1), (1, 1, 1, 1)]
FIXED_N = ';'.join(','.join(map(str, q)) for q in FIVE)
FIXED_W = ';'.join(','.join('%d:0' % x for x in q) for q in FIVE)
ENGINE = './cube_regions_q2w'


# --------------------------------------------------------------------------
# catalogues, as monomial dicts {(i,j,k): Fraction}
# --------------------------------------------------------------------------

def build_catalogues():
    cache = 'continua_catalogue.pkl'
    if os.path.exists(cache):
        return pickle.load(open(cache, 'rb'))
    import sympy
    from chamber_walls import quad_coeffs, w4_polys
    from incidence2 import base_catalogue
    from w3_poly import w3_polys_on_line       # noqa: F401  (import gate)

    planeset = pickle.load(open('locus_planes.pkl', 'rb'))
    planes = [{(1, 0, 0): F(A), (0, 1, 0): F(B), (0, 0, 1): F(C),
               (0, 0, 0): F(D)}
              for c in sorted(planeset) for (A, B, C, D) in planeset[c]]
    corner = [{k: F(v) for k, v in m.items()} for m in quad_coeffs()]
    pts, lines = base_catalogue()
    w4 = [{k: F(v) for k, v in m.items()} for m in w4_polys(pts)]

    # W3 built once, symbolically, in (a,b,c)
    a, b, c = sympy.symbols('a b c')
    N = 1 + a*a + b*b + c*c
    M = [[1+a*a-b*b-c*c, 2*(a*b-c), 2*(a*c+b)],
         [2*(a*b+c), 1-a*a+b*b-c*c, 2*(b*c-a)],
         [2*(a*c-b), 2*(b*c+a), 1-a*a-b*b+c*c]]
    col = lambda j: [M[i][j] for i in range(3)]
    w3 = []
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
                    P = sympy.Poly(sympy.expand(det), a, b, c)
                    w3.append({tuple(m): F(sympy.Rational(v).p,
                                           sympy.Rational(v).q)
                               for m, v in zip(P.monoms(), P.coeffs())})
    cat = {'edge-edge': planes, 'corner-face': corner, 'W4': w4, 'W3': w3}
    pickle.dump(cat, open(cache, 'wb'))
    return cat


def restrict(mono, p0, dd):
    """Substitute a + t*da etc into a monomial dict -> [c0, c1, ...] in t."""
    lin = [[p0[u], dd[u]] for u in range(3)]

    def pmul(x, y):
        out = [F(0)]*(len(x)+len(y)-1)
        for i, u in enumerate(x):
            if u:
                for j, v in enumerate(y):
                    if v:
                        out[i+j] += u*v
        return out

    total = [F(0)]
    for (i, j, k), coeff in mono.items():
        term = [coeff]
        for e, base in ((i, lin[0]), (j, lin[1]), (k, lin[2])):
            for _ in range(e):
                term = pmul(term, base)
        if len(term) > len(total):
            total = total + [F(0)]*(len(term)-len(total))
        for idx, v in enumerate(term):
            total[idx] += v
    while len(total) > 1 and total[-1] == 0:
        total.pop()
    return total


def peval(co, t):
    s = F(0)
    for c in reversed(co):
        s = s*t + c
    return s


def to_quat(pt, cap=10**9):
    den = 1
    for v in pt:
        den = den * v.denominator // math.gcd(den, v.denominator)
    q = (den, int(pt[0]*den), int(pt[1]*den), int(pt[2]*den))
    g = 0
    for x in q:
        g = math.gcd(g, abs(x))
    q = tuple(x//g for x in q) if g > 1 else q
    return q if any(q) and max(abs(x) for x in q) <= cap else None


def count_many(quats):
    lines = [FIXED_W + ';' + ','.join('%d:0' % x for x in q) for q in quats]
    out = subprocess.run([ENGINE, '--d', '0', '--quats-stdin'],
                         input='\n'.join(lines) + '\n',
                         capture_output=True, text=True).stdout
    res = []
    for l in out.splitlines():
        if l.startswith('{'):
            res.append(json.loads(l).get('bounded'))
    return res


def main():
    shard = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    nshard = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    LO, HI, STEP = F(-20), F(20), F(1, 2)

    data = json.load(open('typology_data.json'))
    lines = data['lines']
    print('lines carrying 727: %d  (shard %d of %d)'
          % (len(lines), shard, nshard), flush=True)
    cat = build_catalogues()
    print('catalogue: %s' % {k: len(v) for k, v in cat.items()}, flush=True)

    out = open('continua_shard_%d.jsonl' % shard, 'a')
    for li, L in enumerate(lines):
        if li % nshard != shard:
            continue
        p0 = tuple(F(x) for x in L['p0'])
        dd = tuple(F(x) for x in L['dir'])
        ts, qs = [], []
        t = LO
        while t <= HI:
            q = to_quat(tuple(p0[u] + t*dd[u] for u in range(3)))
            if q:
                ts.append(t)
                qs.append(q)
            t += STEP
        got = count_many(qs)
        # A short result list makes zip() silently truncate and every line
        # reads "0 continua" -- which is exactly what the first run of this
        # census produced, when the engine children were dying under memory
        # pressure from a concurrent 8-shard campaign. An empty answer must
        # be an error, never a finding.
        if len(got) != len(qs):
            raise SystemExit('engine returned %d results for %d configs on '
                             'line %d -- refusing to report a count built on '
                             'truncated output' % (len(got), len(qs), li))
        runs = []
        cur = None
        for t, c in zip(ts, got):
            if c == 727:
                if cur is None:
                    cur = [t, t]
                else:
                    cur[1] = t
            else:
                if cur:
                    runs.append(cur)
                cur = None
        if cur:
            runs.append(cur)
        rec = {'line': li, 'runs': [[str(a), str(b)] for a, b in runs],
               'n_samples': len(ts)}
        print('line %3d: %d continua %s' %
              (li, len(runs), [('%.3f..%.3f' % (float(a), float(b)))
                               for a, b in runs]), flush=True)
        out.write(json.dumps(rec) + '\n')
        out.flush()


if __name__ == '__main__':
    main()
