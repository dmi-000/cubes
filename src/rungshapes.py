#!/usr/bin/env python3
"""Shape of each tower rung's maximising locus, by SOLVING rather than sampling.

A 13-pair (METHODS 12) is a pair of cubes whose relative rotation is about a body
diagonal: the 2-cube compound then has 13 regions instead of 15.  The locus of such
partners for a fixed base cube b is the CURVE

    q(t) = b * (1, t*a),      a a body diagonal,  t in Q

in Cayley coordinates.  For each rung of the tower we ask, exactly, whether the
rung's last cube lies on such a curve for some earlier cube b and some diagonal a:
solve  b^-1 * c  =  scalar * (1, t*a)  by requiring the vector part be parallel to
a, which determines t or refutes the pair.  No sampling is involved in this step.

Then, for each curve found, sweep it to measure how far the record count extends.
That second step IS sampled and so gives a LOWER BOUND on the locus's extent
(METHODS 1's corollary).  It must be run on the WIDE engine: offsets with large
denominators canonicalise to quaternions far above the narrow engine's 512 cap, so
on cube_regions_n almost every offset comes back unevaluable and a plateau reads as
an isolated point (FAILURE_MODES 16c).

Gate: the solve must recover METHODS 12's known 13-pair curves at 2785 (base cube 1
at |t| = 227/889) before any new answer is believed.
"""
import json, subprocess, sys
from fractions import Fraction as F
from math import gcd

from growth727 import BASE                      # cubes 0..4 of the tower

TOWER = {                                       # rung -> full cube list
    727:  BASE + [(7, 14, 1, -5)],
    1217: BASE + [(7, 14, 1, -5), (4, -3, -4, -4)],
    1895: BASE + [(7, 14, 1, -5), (4, -3, -4, -4), (24, -24, 24, -61)],
    2785: BASE + [(7, 14, 1, -5), (4, -3, -4, -4), (24, -24, 24, -61),
                  (56, 56, 55, 56)],   # k=56, the RECORDED member (P178);
                                       # P181's n=10 campaign extended k=57 instead
}
DIAGONALS = [(1, 1, 1), (1, 1, -1), (1, -1, 1), (-1, 1, 1)]
WIDE = './cube_regions_q2w'


def qmul(p, q):
    w, x, y, z = p; e, f, g, h = q
    return (w*e - x*f - y*g - z*h, w*f + x*e + y*h - z*g,
            w*g - x*h + y*e + z*f, w*h + x*g - y*f + z*e)


def qconj(p):
    return (p[0], -p[1], -p[2], -p[3])


def canon(q):
    """Projective representative: clear denominators, divide by gcd, fix sign."""
    den = 1
    for x in q:
        den = den * F(x).denominator // gcd(den, F(x).denominator)
    w = [int(F(x) * den) for x in q]
    g = 0
    for v in w:
        g = gcd(g, abs(v))
    w = [v // (g or 1) for v in w]
    for v in w:
        if v > 0:
            break
        if v < 0:
            w = [-x for x in w]
            break
    return tuple(w)


def solve_curve(b, c, a):
    """Exact: is c on the curve b*(1,t*a)?  Return t, or None.

    b^-1*c is proportional to (1, t*a) iff its vector part is parallel to a with
    the right sign pattern.  Everything here is a rational identity test.
    """
    r = qmul(qconj(b), c)
    r0, rv = r[0], r[1:]
    if r0 == 0:                       # t = infinity: a half-turn, not on the chart
        return None
    ts = {F(v, r0 * ai) for v, ai in zip(rv, a) if ai}
    if len(ts) != 1:
        return None
    t, = ts
    return t if tuple(F(t) * ai * r0 for ai in a) == tuple(map(F, rv)) else None


def batch(cfgs, exe=WIDE):
    inp = '\n'.join(';'.join(','.join(map(str, q)) for q in c) for c in cfgs) + '\n'
    p = subprocess.run([exe, '--d', '0', '--quats-stdin'],
                       input=inp, capture_output=True, text=True)
    out = []
    for line in p.stdout.splitlines():
        try:
            out.append(json.loads(line).get('bounded'))
        except Exception:
            out.append(None)
    return out + [None] * (len(cfgs) - len(out))


def curves_through_last(cubes):
    c = cubes[-1]
    return [(i, a, t) for i, b in enumerate(cubes[:-1]) for a in DIAGONALS
            for t in [solve_curve(b, c, a)] if t is not None]


def sweep(cubes, i, a, t0, expected, den, half):
    """Sampled extent of `expected` along the solved curve.  LOWER bound."""
    base, b = cubes[:-1], cubes[i]
    ts = [t0 + F(k, den) for k in range(-half, half + 1)]
    cfgs = [base + [canon(qmul(b, (1, t * a[0], t * a[1], t * a[2])))] for t in ts]
    vals = batch(cfgs)
    runs, cur = [], None
    for t, v in zip(ts, vals):
        if v == expected:
            cur = [t, t] if cur is None else [cur[0], t]
        elif cur:
            runs.append(tuple(cur)); cur = None
    if cur:
        runs.append(tuple(cur))
    return ts, vals, runs


def main():
    # --- gate: METHODS 12's known curve at 2785 must come back --------------
    got = curves_through_last(TOWER[2785])
    # sign of t flips with the sign of the diagonal; the curve is the same
    if not any(abs(t) == F(227, 889) for _, _, t in got):
        sys.exit('GATE FAILED: 2785 curve t = -227/889 not recovered; got %s' % got)
    print('gate: 2785 reproduces METHODS 12 (t = -227/889)  OK\n')

    for rung in (727, 1217, 1895, 2785):
        cubes = TOWER[rung]
        found = curves_through_last(cubes)
        print('%-5d last cube %-16s  %d 13-pair curve(s)'
              % (rung, str(cubes[-1]), len(found)))
        for i, a, t in found:
            print('        base cube %d, axis %s, t = %s' % (i, a, t))
            _, vals, runs = sweep(cubes, i, a, t, rung, 630, 60)
            n_un = sum(1 for v in vals if v is None)
            for lo, hi in runs:
                print('          holds on [%s, %s]  width %s%s'
                      % (lo, hi, hi - lo,
                         '   <- contains recorded t' if lo <= t <= hi else ''))
            best = max((v for v in vals if v is not None), default=None)
            print('          %d offsets, %d unevaluable, max on line %s'
                  % (len(vals), n_un, best))
        if not found:
            print('        locus of this type: NONE.  Other types unevaluated.')
        print()


if __name__ == '__main__':
    main()
