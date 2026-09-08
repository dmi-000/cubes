#!/usr/bin/env python3
"""Null directions vs the count, in the eps -> 0 limit, with refusals escalated.

Final form of the [P175] recheck.  Every null basis vector at n = 6..9, both signs
(eps is a POSITIVE infinitesimal, so v and -v are separate questions), narrow engine
first and the 256-bit engine on any refusal.  Nothing is reported as a negative that
was not evaluated.

Controls, both able to fail: the zero direction must reproduce the record; a wall
gradient must change it.
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


def ev(pt, q0, v, rec):
    """narrow engine, escalating to the wide one on refusal; reports which"""
    out = []
    for sgn in (1, -1):
        dv = [Q(F(sgn * x), 0, 0) for x in v]
        c = count_eps(pt, dv, 0, q0)
        eng = 'narrow'
        if c is None:
            c = count_eps(pt, dv, 0, q0, wide=True); eng = 'WIDE'
        out.append((c, eng))
    return out


tot_hold = tot_change = tot_unev = 0
for n in (6, 7, 8, 9):
    quats = R[n]
    pt, walls, null, ncols = walls_and_null(quats)
    rec = D.count_at(pt, len(quats))
    z = count_eps(pt, [Q(0, 0, 0)] * ncols, 0, quats[0])
    wg = count_eps(pt, [Q(F(x), 0, 0) for x in walls[0]], 0, quats[0])
    if wg is None:
        wg = count_eps(pt, [Q(F(x), 0, 0) for x in walls[0]], 0, quats[0], wide=True)
    print('\nn=%d  record %d  nullity %d   CONTROLS zero->%s %s, wall-grad->%s %s'
          % (n, rec, len(null), z, 'OK' if z == rec else 'FAIL',
             wg, 'OK' if (wg is not None and wg != rec) else 'FAIL'), flush=True)
    if z != rec or wg is None or wg == rec:
        sys.exit('controls failed at n=%d' % n)
    h = c_ = u = 0
    for i, v0 in enumerate(null):
        v = primitive(v0)
        r = ev(pt, quats[0], v, rec)
        vals = [x[0] for x in r]
        if None in vals:
            u += 1; tag = 'UNEVALUATED even on the wide engine'
        elif vals[0] == rec and vals[1] == rec:
            h += 1; tag = 'HOLDS both sides'
        elif rec in vals:
            h += 1; tag = 'holds ONE side — BOUNDARY'
        else:
            c_ += 1; tag = 'changes'
        print('   b%d |v|max %-6d  +eps %-6s(%s)  -eps %-6s(%s)  %s'
              % (i, max(abs(x) for x in v), vals[0], r[0][1], vals[1], r[1][1], tag),
              flush=True)
    print('   n=%d: %d hold, %d change, %d unevaluated  (nullity %d, deficit %d)'
          % (n, h, c_, u, len(null), ncols - (ncols - len(null))), flush=True)
    tot_hold += h; tot_change += c_; tot_unev += u

print('\nTOTAL over n=6..9: %d hold, %d change, %d UNEVALUATED'
      % (tot_hold, tot_change, tot_unev), flush=True)
