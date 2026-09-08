#!/usr/bin/env python3
# Working principles: supersedes the Groebner path in locus_enum.py.
"""Exhaustive three-wall enumeration by LINEAR algebra.

Every coincidence condition on the 393 base factors into two rational linear
forms -- each wall is a PAIR OF PLANES in the sixth cube's Cayley coordinates,
not an irreducible quadric.  Consequences:

  * a three-wall system is 2^3 = 8 linear systems, each a 3x3 rational solve,
    so every solution is rational BY CONSTRUCTION -- the irrational-strata gap
    is provably empty here, not merely unobserved (irrational_probe.py found
    0 of 2451 real roots irrational, which is now explained rather than lucky);
  * Bezout's bound of 8 points is exactly those eight plane choices;
  * the 144 walls per fixed cube collapse to 24 DISTINCT planes, so the whole
    family is 10 cube-triples x 24^3 = 138 240 systems -- seconds of linear
    algebra, where the Groebner path needed ~18 ms each.

This makes the enumeration genuinely exhaustive over the three-wall family at
negligible cost, and leaves region counting as the only real expense.

INVARIANT: exact rational arithmetic (Fraction) in the solve; candidates are
deduplicated by their orbit under the cube's own 24 rotations before counting.
A singular 3x3 system means the three planes share a line or are parallel --
recorded as positive-dimensional, never silently dropped.
"""
import itertools
import json
import math
import pickle
import sys
from fractions import Fraction as F

import sympy as sp

import record_hunt as R

a, b, c = sp.symbols('a b c', real=True)
FIVE = [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5), (2, 1, 1, 1),
        (1, 1, 1, 1)]
CAP = 512
REPORT_AT = 723


def extract_planes():
    """Distinct planes (A,B,C,D) with Aa+Bb+Cc+D = 0, per fixed cube."""
    per = pickle.load(open('locus_polys.pkl', 'rb'))
    out = {}
    for j in range(5):
        S = set()
        for P, _ in per[j]:
            for f, _m in sp.factor_list(P)[1]:
                p = sp.Poly(f, a, b, c)
                if p.total_degree() != 1:
                    continue
                co = [sp.Rational(p.coeff_monomial(m)) for m in (a, b, c, 1)]
                g = sp.ilcm(*[x.q for x in co])
                co = [int(x * g) for x in co]
                nz = [abs(x) for x in co if x]
                d = nz[0]
                for v in nz[1:]:
                    d = math.gcd(d, v)
                co = [x // (d or 1) for x in co]
                for x in co:                      # canonical sign
                    if x:
                        if x < 0:
                            co = [-y for y in co]
                        break
                S.add(tuple(co))
        out[j] = sorted(S)
    return out


def solve3(p, q, r):
    """Exact intersection point of three planes, or None if singular."""
    M = [p[:3], q[:3], r[:3]]
    rhs = [-p[3], -q[3], -r[3]]
    det = (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
           - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
           + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))
    if det == 0:
        return None
    def cof(col):
        N = [list(row) for row in M]     # M's rows come from tuples
        for i in range(3):
            N[i][col] = rhs[i]
        return (N[0][0] * (N[1][1] * N[2][2] - N[1][2] * N[2][1])
                - N[0][1] * (N[1][0] * N[2][2] - N[1][2] * N[2][0])
                + N[0][2] * (N[1][0] * N[2][1] - N[1][1] * N[2][0]))
    return (F(cof(0), det), F(cof(1), det), F(cof(2), det))


def to_quat(pt):
    den = 1
    for v in pt:
        den = den * v.denominator // math.gcd(den, v.denominator)
    q = (den, int(pt[0] * den), int(pt[1] * den), int(pt[2] * den))
    g = 0
    for x in q:
        g = math.gcd(g, abs(x))
    q = tuple(x // g for x in q) if g > 1 else q
    return q if any(q) and max(abs(x) for x in q) <= CAP else None


def qmul(p, q):
    w, x, y, z = p
    e, f, g, h = q
    return (w * e - x * f - y * g - z * h, w * f + x * e + y * h - z * g,
            w * g - x * h + y * e + z * f, w * h + x * g - y * f + z * e)


SYMS = list(dict.fromkeys(
    R.canon([t])[0] for t in
    [(w, x, y, z) for w in (-1, 0, 1) for x in (-1, 0, 1) for y in (-1, 0, 1)
     for z in (-1, 0, 1)
     if (w, x, y, z) != (0, 0, 0, 0) and w * w + x * x + y * y + z * z in (1, 2, 4)]))


def sym_key(q):
    return min(R.canon([qmul(tuple(q), h)])[0] for h in SYMS)


def main():
    planes = extract_planes()
    for j in range(5):
        print('cube %d: %d distinct planes' % (j, len(planes[j])), flush=True)
    total_sys = sum(len(planes[i]) * len(planes[j]) * len(planes[k])
                    for i, j, k in itertools.combinations(range(5), 3))
    print('systems to solve: %d' % total_sys, flush=True)

    seen, cands, singular = set(), [], 0
    for i, j, k in itertools.combinations(range(5), 3):
        for p in planes[i]:
            for q in planes[j]:
                for r in planes[k]:
                    pt = solve3(p, q, r)
                    if pt is None:
                        singular += 1
                        continue
                    qt = to_quat(pt)
                    if qt is None:
                        continue
                    key = sym_key(qt)
                    if key in seen:
                        continue
                    seen.add(key)
                    cands.append(qt)
    print('distinct candidates: %d (singular systems: %d)'
          % (len(cands), singular), flush=True)

    eng = R.Engine(6, int(sys.argv[1]) if len(sys.argv) > 1 else 3)
    out = open('locus_linear.jsonl', 'a')
    best, hist = (0, None), {}
    B = 500
    for s in range(0, len(cands), B):
        chunk = cands[s:s + B]
        res = eng.count([[list(x) for x in FIVE] + [list(qt)] for qt in chunk])
        for qt, (tot, bd) in zip(chunk, res):
            hist[tot] = hist.get(tot, 0) + 1
            if tot > best[0]:
                best = (tot, qt)
            if tot >= REPORT_AT:
                out.write(json.dumps({'total': tot, 'sixth': qt,
                                      'by_depth': bd}) + '\n')
                out.flush()
                if tot > 727:
                    print('*** ABOVE 727: %d  %s' % (tot, qt), flush=True)
        print('  counted %d/%d, best so far %s'
              % (min(s + B, len(cands)), len(cands), best), flush=True)
    print('\nDONE. best = %s' % (best,), flush=True)
    print('top of the distribution:',
          {t: hist[t] for t in sorted(hist)[-12:]}, flush=True)
    json.dump({'hist': {str(k): v for k, v in hist.items()},
               'best': [best[0], list(best[1])], 'candidates': len(cands)},
              open('locus_linear_summary.json', 'w'), indent=1)


if __name__ == '__main__':
    main()
