#!/usr/bin/env python3
"""What happens AT the endpoint of a 727 continuum?

A 727 stretch of a wall line is an interval.  Its endpoints are wall crossings
(Postscript 58).  The question is whether the interval is OPEN or CLOSED: does
the count still read 727 exactly at the endpoint, or has it already dropped?

The geometric expectation is that it drops.  A coincidence MERGES regions —
a sliver between two faces closes up — so the count at a degenerate
configuration should be no larger than at nearby generic ones, and strictly
smaller when the coincidence involves faces that really bound regions.  If
that is right, the maximum is attained on an OPEN set and never at its own
boundary, which is a statement about where records can live.

But it cannot be assumed, because this project has already found walls that
are combinatorially inert: 105 of the 183 irrational 727s sit ON a wall with
the same per-label type as both neighbours (Postscript 61 addendum).  A wall
whose coincidence is phantom changes nothing at all.

METHOD.  Walk a 727-carrying line, locate the sampled ends of the 727 stretch,
compute the exact condition roots there, and evaluate the count AT the root —
with `cube_regions_n` if the root is rational, with `cube_regions_q2` in
Z[sqrt d] if it is a quadratic irrational.  No sampling near the endpoint can
answer this; the endpoint has to be hit exactly.

INVARIANT: the configuration evaluated must be the root itself, verified by
substituting back into both defining conditions exactly.  "Very close to the
endpoint" is precisely the thing that does not answer the question.
"""
import json
import math
import pickle
import subprocess
import sys
from fractions import Fraction as F

import sympy

from base_points import FIVE
from chamber_walls import quad_coeffs, restrict, roots_in, to_quat, w4_polys
from incidence2 import base_catalogue

FIXED_N = ';'.join(','.join(map(str, q)) for q in FIVE)
FIXED_Q2 = ';'.join(','.join('%d:0' % x for x in q) for q in FIVE)


def count_rational(pt):
    q = to_quat(pt, cap=10**7)
    if q is None:
        return None, None, 'components too large'
    out = subprocess.run(['./cube_regions_n', '--quats',
                          FIXED_N + ';' + ','.join(map(str, q))],
                         capture_output=True, text=True).stdout
    if not out.startswith('{'):
        return None, q, 'engine error'
    d = json.loads(out)
    return d.get('bounded'), q, d.get('error')


def squarefree(D):
    """D = s^2 * d with d squarefree; returns (d, s).  sqrt(D) = s*sqrt(d), so
    p + q*sqrt(D) = p + (q*s)*sqrt(d).  The engine requires a squarefree d --
    a square factor collapses distinct (p,q) onto the same value and silently
    breaks the vertex dedup identity relies on."""
    d, s = D, 1
    f = 2
    while f*f <= d:
        while d % (f*f) == 0:
            d //= f*f
            s *= f
        f += 1
    return d, s


def count_algebraic(sf, comps, engine='./cube_regions_q2w'):
    """comps: four (p, q) pairs of Fractions, cleared to integers here."""
    sf, scale = squarefree(sf)
    comps = [(p, q*scale) for p, q in comps]
    den = 1
    for p, q in comps:
        for v in (p, q):
            den = den * v.denominator // math.gcd(den, v.denominator)
    ints = [(int(p*den), int(q*den)) for p, q in comps]
    g = 0
    for p, q in ints:
        g = math.gcd(g, math.gcd(abs(p), abs(q)))
    if g > 1:
        ints = [(p//g, q//g) for p, q in ints]
    if max(max(abs(p), abs(q)) for p, q in ints) > 10**7:
        return None, ints, 'components too large'
    line = FIXED_Q2 + ';' + ','.join('%d:%d' % c for c in ints)
    # the WIDE engine: endpoint roots routinely need more than the narrow
    # 2^112 chain budget (this line's upper endpoint needs 214 bits)
    out = subprocess.run([engine, '--d', str(sf),
                          '--quats-stdin'], input=line + '\n',
                         capture_output=True, text=True).stdout
    for l in out.splitlines():
        if l.startswith('{'):
            d = json.loads(l)
            return d.get('bounded'), ints, d.get('error')
    return None, ints, 'no output'


def main():
    li = int(sys.argv[1]) if len(sys.argv) > 1 else 9
    LO = F(sys.argv[2]) if len(sys.argv) > 2 else F(-24)
    HI = F(sys.argv[3]) if len(sys.argv) > 3 else F(24)
    data = json.load(open('typology_data.json'))
    L = data['lines'][li]
    p0 = tuple(sympy.Rational(x) for x in L['p0'])
    dd = tuple(sympy.Rational(x) for x in L['dir'])
    p0f = tuple(F(str(x)) for x in p0)
    ddf = tuple(F(str(x)) for x in dd)

    # --- 1. where does 727 hold? ------------------------------------------
    step = F(1, 8)
    ts, quats = [], []
    t = LO
    while t <= HI:
        q = to_quat(tuple(p0f[u] + t*ddf[u] for u in range(3)), cap=10**7)
        if q:
            ts.append(t)
            quats.append(q)
        t += step
    inp = '\n'.join(FIXED_N + ';' + ','.join(map(str, q)) for q in quats) + '\n'
    out = subprocess.run(['./cube_regions_n', '--quats-stdin'], input=inp,
                         capture_output=True, text=True).stdout
    rows = [json.loads(l) for l in out.splitlines() if l.startswith('{')]
    seq = [(t, d.get('bounded')) for t, d in zip(ts, rows)]
    idx = [i for i, (_, c) in enumerate(seq) if c == 727]
    if not idx:
        print('line %d: no 727 in [%s, %s]' % (li, LO, HI))
        return
    i0, i1 = idx[0], idx[-1]
    print('line %d: 727 over sampled t in [%s, %s] (%d of %d samples)'
          % (li, seq[i0][0], seq[i1][0], len(idx), len(seq)))
    print('   just outside: t=%s -> %s   t=%s -> %s'
          % (seq[i0-1][0] if i0 else None, seq[i0-1][1] if i0 else None,
             seq[i1+1][0] if i1+1 < len(seq) else None,
             seq[i1+1][1] if i1+1 < len(seq) else None))

    # --- 2. exact condition roots bracketing each end ----------------------
    planeset = pickle.load(open('locus_planes.pkl', 'rb'))
    planes = [p for c in sorted(planeset) for p in planeset[c]]
    quads = quad_coeffs()
    cand = []
    for A, B, C, D in planes:
        for r in roots_in(restrict({(1, 0, 0): A, (0, 1, 0): B, (0, 0, 1): C,
                                    (0, 0, 0): D}, p0, dd), LO, HI):
            cand.append(('edge-edge', r))
    for m in quads:
        for r in roots_in(restrict(m, p0, dd), LO, HI):
            cand.append(('corner-face', r))
    # Postscript 58: the classical catalogue explains only 6 of 46 chamber
    # boundaries; the W4 walls (a free-cube face plane through a real triple
    # point of the base) explain 43.  Leaving them out is what produced an
    # earlier run of this script finding ZERO roots at either endpoint.
    pts, _ = base_catalogue()
    for m in w4_polys(pts):
        for r in roots_in(restrict(m, p0, dd), LO, HI):
            cand.append(('W4', r))

    for side, lo, hi in (('LOWER', seq[i0-1][0] if i0 else LO, seq[i0][0]),
                         ('UPPER', seq[i1][0], seq[i1+1][0]
                          if i1+1 < len(seq) else HI)):
        here = [(k, r) for k, r in cand
                if sympy.Rational(lo) <= r <= sympy.Rational(hi)]
        print('\n%s end, between t=%s and t=%s: %d exact roots'
              % (side, lo, hi, len(here)))
        for kind, r in here[:6]:
            rv = sympy.nsimplify(r)
            pt = [sympy.nsimplify(p0[u] + rv*dd[u]) for u in range(3)]
            if rv.is_rational:
                ptf = tuple(F(str(sympy.Rational(x))) for x in pt)
                tot, q, err = count_rational(ptf)
                print('   %-12s t = %-22s RATIONAL   count AT the root: %s %s'
                      % (kind, str(rv)[:22], tot, err or ''))
            else:
                sq = [a for a in rv.atoms(sympy.Pow)
                      if a.exp == sympy.Rational(1, 2)]
                if len(sq) != 1:
                    print('   %-12s t = %-22s (unhandled algebraic form)'
                          % (kind, str(rv)[:22]))
                    continue
                sf = int(sq[0].base)
                comps = []
                ok = True
                for x in [sympy.Integer(1)] + pt:
                    poly = sympy.Poly(sympy.expand(x), sq[0])
                    cs = poly.all_coeffs()[::-1]
                    if len(cs) > 2:
                        ok = False
                        break
                    a0 = sympy.Rational(cs[0])
                    a1 = sympy.Rational(cs[1]) if len(cs) > 1 else 0
                    comps.append((F(a0.p, a0.q),
                                  F(sympy.Rational(a1).p, sympy.Rational(a1).q)))
                if not ok:
                    print('   %-12s t = %-22s (nested radical, skipped)'
                          % (kind, str(rv)[:22]))
                    continue
                tot, ints, err = count_algebraic(sf, comps)
                print('   %-12s t = %-22s IRRATIONAL Q(sqrt%d)  count AT the'
                      ' root: %s %s' % (kind, str(rv)[:22], sf, tot, err or ''))


if __name__ == '__main__':
    main()
