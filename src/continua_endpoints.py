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


def sign_surd(P, Q, D):
    """sign of P + Q*sqrt(D), P,Q rational, D a positive non-square integer."""
    if Q == 0:
        return (P > 0) - (P < 0)
    if P == 0:
        return (Q > 0) - (Q < 0)
    if (P > 0) == (Q > 0):
        return 1 if P > 0 else -1
    # opposite signs: compare P^2 against Q^2*D
    c = P*P - Q*Q*D
    if c == 0:
        return 0
    return (1 if P > 0 else -1) * (1 if c > 0 else -1)


def roots_of(co, lo, hi):
    """Exact roots of the polynomial `co` (ascending Fraction coefficients)
    lying in [lo, hi], each as (P, Q, D) meaning P + Q*sqrt(D).

    Degree 1 and 2 only -- higher degrees are reported by the caller, never
    approximated.  sympy is deliberately NOT used here: real_roots() returns
    CRootOf objects for quartics, and any attempt to turn one into radicals
    invites nsimplify, which is a NUMERIC guessing heuristic and produced
    expressions like 2**(103/253) when it was let into this pipeline.
    """
    deg = len(co) - 1
    if deg == 1:
        r = -co[0]/co[1]
        return [(r, F(0), 0)] if lo <= r <= hi else []
    if deg > 2:
        # FACTOR over Q first. A W3 condition is a quartic in t, but it may
        # factor -- line 9's lower endpoint is a quartic whose quadratic
        # factor 4455t^2 - 11790t + 6151 carries the root. Reporting "degree
        # 4, cannot count" without factoring under-reports what is reachable.
        # sympy is used here ONLY for exact symbolic factorisation over Q,
        # never to approximate a root.
        x = sympy.Symbol('x')
        expr = sum(sympy.Rational(c.numerator, c.denominator)*x**i
                   for i, c in enumerate(co))
        try:
            _, factors = sympy.factor_list(sympy.Poly(expr, x))
        except Exception:
            return None
        out, hard = [], False
        for f, _mult in factors:
            fc = [sympy.Rational(c) for c in f.all_coeffs()[::-1]]
            if len(fc) - 1 > 2:
                hard = True
                continue
            sub = roots_of([F(c.p, c.q) for c in fc], lo, hi)
            if sub:
                out.extend(sub)
        if out:
            return out
        return None if hard else []
    a0, a1, a2 = co[0], co[1], co[2]
    disc = a1*a1 - 4*a2*a0
    if disc < 0:
        return []
    num, den = disc.numerator, disc.denominator
    Dint = num*den                        # sqrt(disc) = sqrt(num*den)/den
    sf, scale = squarefree(Dint)
    out = []
    for sgn in (1, -1):
        P = -a1/(2*a2)
        Q = F(sgn*scale, den) / (2*a2)
        if sign_surd(P - lo, Q, sf) >= 0 and sign_surd(P - hi, Q, sf) <= 0:
            out.append((P, Q, sf))
        if disc == 0:
            break
    return out


def count_at_root(root, p0, dd):
    """Exact count at p0 + root*dd, root given as (P, Q, D)."""
    P, Q, D = root
    comps = [(F(1), F(0))] + [(F(p0[u]) + P*F(dd[u]), Q*F(dd[u]))
                              for u in range(3)]
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
    if max(max(abs(a), abs(b)) for a, b in ints) > 10**8:
        return None, 'components too large'
    line = FIXED_W + ';' + ','.join('%d:%d' % c for c in ints)
    out = subprocess.run(['./cube_regions_q2w', '--d', str(D),
                          '--quats-stdin'], input=line + '\n',
                         capture_output=True, text=True).stdout
    for l in out.splitlines():
        if l.startswith('{'):
            j = json.loads(l)
            return j.get('bounded'), ('rational' if D == 0
                                      else 'Q(sqrt %d)' % D), j
    return None, 'no engine output', None


def main():
    cat = build_catalogues()
    data = json.load(open('typology_data.json'))
    recs = [json.loads(l) for l in open('continua_shard_0.jsonl')]
    todo = [(r['line'], run) for r in recs for run in r['runs']]
    print('continua found: %d, endpoints to analyse: %d'
          % (len(todo), 2*len(todo)), flush=True)

    tally = collections.Counter()
    # TRUNCATE, not append. This file has now caused the same error twice:
    # records from superseded runs sit alongside the live ones, and any later
    # analysis silently mixes them. A results file that accumulates across
    # incompatible runs is not a log, it is a trap.
    out = open('continua_endpoints.jsonl', 'w')
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
                    # A condition that vanishes IDENTICALLY on the line is one
                    # of the two walls DEFINING it -- it is zero at every
                    # parameter, so it brackets nothing and has no root to
                    # find. Skipping these is not a convenience: including
                    # them made the sign test fire on every endpoint and then
                    # crash real_roots() on the zero polynomial.
                    if all(c == 0 for c in co) or len(co) < 2:
                        continue
                    vlo, vhi = peval(co, lo), peval(co, hi)
                    if vlo == 0 or vhi == 0 or (vlo > 0) != (vhi > 0):
                        hits.append((kind, co))
            info = {'line': li, 'side': side, 'bracket': [str(lo), str(hi)],
                    'walls': sorted({k for k, _ in hits})}
            got = None
            degs = set()
            for kind, co in hits:
                rs = roots_of(co, lo, hi)
                if rs is None:
                    degs.add(len(co) - 1)
                    continue
                for r in rs:
                    cnt, note, full = count_at_root(r, p0, dd)
                    if full:
                        info['by_depth'] = full.get('by_depth')
                        info['per_label'] = full.get('per_label')
                    info.update({'wall': kind,
                                 'root': '%s%+s*sqrt(%d)' % (r[0], r[1], r[2]),
                                 'count': cnt, 'field': note})
                    got = (kind, cnt, note)
                    break
                if got:
                    break
            # Do NOT stop at the first bracketing condition when it failed to
            # resolve: several walls can cross the same endpoint, and only some
            # of their polynomials factor. Breaking early made C3 orbit-mates
            # disagree (line 9's endpoint resolved, line 88's did not), which
            # is impossible for congruent configurations and is what exposed
            # this.
            if got is None and degs:
                info['unresolved_degree'] = sorted(degs)
                got = ('degree %s' % sorted(degs), None,
                       'needs the degree-agnostic engine')
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
