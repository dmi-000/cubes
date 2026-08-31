#!/usr/bin/env python3
"""Is "exactly one null direction changes the count" a fact, or a height artifact?

`eps_null3.py` found, at n = 6..9, that the count-preserving null directions number
nullity - 1 — and that the single CHANGING direction is at every rung the one with a
long primitive representative (|v|max ~5 000-10 000) while every holding one has
|v|max 1.  A perfect split by input height is METHODS 15's tell for a badly chosen
representative, so it must be ruled out before the pattern is believed.

TWO CONTROLS, both able to fail:

  SCALE.  eps-counts are invariant under positive scaling of the direction (scaling
  by L multiplies the degree-k coefficient by L^k, which cannot flip the sign of the
  lowest nonzero one).  So 2*v and 3*v must return exactly what v returns.  Scaling a
  SHORT holding vector up to the long ones' height is the sharp version: if height
  drove the answer, a tall multiple of a holding direction would change the count.

  QUOTIENT.  If the holding set is a hyperplane H in the null space, then adding any
  holding vector to the changing one stays outside H and must still change.
"""
import sys
sys.path.insert(0, '.')
from fractions import Fraction as F
from math import gcd
from qfield import Q
import dimension as D
from wallcount import R
from epscount import count_eps
from eps_null import walls_and_null


def primitive(v):
    den = 1
    for x in v:
        den = den * F(x).denominator // gcd(den, F(x).denominator)
    iv = [int(F(x) * den) for x in v]
    g = 0
    for x in iv:
        g = gcd(g, abs(x))
    return [x // (g or 1) for x in iv]


def cnt(pt, q0, v):
    c = count_eps(pt, [Q(F(x), 0, 0) for x in v], 0, q0)
    return c if c is not None else count_eps(pt, [Q(F(x), 0, 0) for x in v], 0, q0, wide=True)


for n in (7, 8):
    quats = R[n]
    pt, walls, null, ncols = walls_and_null(quats)
    rec = D.count_at(pt, len(quats))
    B = [primitive(v) for v in null]
    hold = [v for v in B if cnt(pt, quats[0], v) == rec]
    chng = [v for v in B if cnt(pt, quats[0], v) != rec]
    print('\nn=%d record %d: %d holding, %d changing' % (n, rec, len(hold), len(chng)),
          flush=True)

    print('  SCALE control — a holding direction scaled UP to the changing one\'s height:',
          flush=True)
    h = hold[0]
    for k in (1, 2, 3, 4980, 9960):
        v = [k * x for x in h]
        c = cnt(pt, quats[0], v)
        print('     %5d * v_hold  |v|max %-8d -> %-6s  %s'
              % (k, max(abs(x) for x in v), c,
                 'holds' if c == rec else 'CHANGES — height DOES drive it'), flush=True)
    print('  SCALE control — the changing direction scaled:', flush=True)
    g = chng[0]
    for k in (1, 2, 3):
        v = [k * x for x in g]
        c = cnt(pt, quats[0], v)
        print('     %5d * v_chng  |v|max %-8d -> %-6s  %s'
              % (k, max(abs(x) for x in v), c,
                 'same as v — scale-invariant' if c == cnt(pt, quats[0], g)
                 else 'DIFFERS — not scale-invariant'), flush=True)

    print('  QUOTIENT control — changing direction plus each holding one:', flush=True)
    for i, hv in enumerate(hold):
        for a in (1, -1, 2):
            v = primitive([x + a * y for x, y in zip(g, hv)])
            c = cnt(pt, quats[0], v)
            print('     v_chng %+d*h%d  |v|max %-8d -> %-6s  %s'
                  % (a, i, max(abs(x) for x in v), c,
                     'still changes — consistent with a hyperplane'
                     if c != rec else 'HOLDS — holding set is NOT a hyperplane'),
                  flush=True)
