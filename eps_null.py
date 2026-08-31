#!/usr/bin/env python3
"""Do the wall matrix's NULL DIRECTIONS preserve the count?  Asked with eps, not a step.

[P175] concluded "a direction crossing no wall still changes the count" and on that
basis retracted [P162], [P173] and [P174].  Its entire evidence is finite steps:

    727, null direction (all cubes):  t=0: 727   1/1000: 685   1/100: 685   1: 593

Two of those agree.  By this project's own rule ("two samples agreeing means they
share a cell", FAILURE_MODES 14) that is not convergence — both can sit outside the
region being measured, in the same wrong one.  And the walls are the TANGENT
structure ([P166]), so the count is constant only INFINITESIMALLY: a step of 1/1000
answers a question about 1/1000, not about the limit.

`epscount.py` and `cube_regions_eps` were built on 2026-08-16 for exactly this, and
P175 did not use them.  Here eps is a positive infinitesimal in Q(sqrt d)(eps), the
sign of every predicate being the sign of the lowest-degree nonzero coefficient, so
the count returned IS the eps -> 0 limit with no step size anywhere.

CONTROLS, both able to fail (FAILURE_MODES 2):
  ZERO      direction 0 must reproduce the record exactly.
  CROSSING  a wall-gradient direction crosses a wall by construction, so it must
            CHANGE the count.  If it does not, the adapter is not moving the
            configuration and every other row here is meaningless.
"""
import sys
sys.path.insert(0, '.')
import sympy as sp, dimension as D
from fractions import Fraction as F
from qfield import Q
from wallcount import R
from math import gcd
from epscount import count_eps


def walls_and_null(quats):
    """wall gradients at the record, and a basis of their null space"""
    D.set_field(0); D.QZERO[:] = [quats[0]]
    pt = D.point_of(quats)
    ncols = 3 * (len(quats) - 1)
    vars_ = sp.symbols('c0:%d' % ncols)
    Rs = D.frames(vars_, quats[0])
    tight, loose = D.cached_conditions(Rs, len(quats), vars_, pt,
                                       D.quats_of(pt, quats[0]), quats[0])
    good = [t for t in tight if not t['degenerate']]
    seen, walls = set(), []
    for t in good:
        g = t['grad']
        piv = next((x for x in g if x != 0), None)
        if piv is None:
            continue
        k = tuple(str(x / piv) for x in g)
        if k not in seen:
            seen.add(k); walls.append(g)
    return pt, walls, D.nullspace(walls, ncols), ncols


if __name__ == '__main__':
    for n in (6, 7, 8):
        quats = R[n]
        pt, walls, null, ncols = walls_and_null(quats)
        rec = D.count_at(pt, len(quats))
        print('\nn=%d  record %d   walls %d  ambient %d  nullity %d'
              % (n, rec, len(walls), ncols, len(null)), flush=True)

        zero = count_eps(pt, [Q(0, 0, 0)] * ncols, 0, quats[0])
        print('   CONTROL zero direction        -> %-6s %s'
              % (zero, 'OK' if zero == rec else 'GATE FAILED'), flush=True)
        if zero != rec:
            sys.exit('adapter does not reproduce the record; nothing below is meaningful')

        w = walls[0]
        cross = [Q(F(x), 0, 0) for x in w]
        cv = count_eps(pt, cross, 0, quats[0])
        print('   CONTROL wall-gradient dir     -> %-6s %s'
              % (cv, 'OK, count changes' if (cv is not None and cv != rec)
                 else 'GATE FAILED — a wall-crossing direction did not change the count'),
              flush=True)
        if cv is None or cv == rec:
            sys.exit('crossing control failed; the adapter is not displacing the point')

        # eps is a POSITIVE infinitesimal, so v and -v are different questions.  A
        # direction holding on one side only means the record sits on the BOUNDARY of
        # the count-preserving set along that line — which is what [P182]'s endpoint
        # pattern predicts, measured here without a step size.
        print('   --- null directions, eps -> 0 limit, BOTH SIGNS ---', flush=True)
        same = diff = unev = 0
        for i, v in enumerate(null):
            # A refusal is usually about the REPRESENTATIVE, not the object
            # (METHODS 15): a direction is defined up to positive scale, so clear
            # denominators and divide out the content before blaming the engine.
            den = 1
            for x in v:
                den = den * F(x).denominator // gcd(den, F(x).denominator)
            iv = [int(F(x) * den) for x in v]
            g = 0
            for x in iv:
                g = gcd(g, abs(x))
            iv = [x // (g or 1) for x in iv]
            row = []
            for sgn in (1, -1):
                c = count_eps(pt, [Q(F(sgn * x), 0, 0) for x in iv], 0, quats[0])
                if c is None:            # retry on the original representative
                    c = count_eps(pt, [Q(F(sgn) * F(x), 0, 0) for x in v], 0, quats[0])
                row.append(c)
                if c is None: unev += 1
                elif c == rec: same += 1
                else: diff += 1
            # UNEVALUATED is never folded into "changes" (FAILURE_MODES 16c)
            tag = ('UNEVALUATED — engine refused, NOT a negative result'
                   if None in row else
                   'HOLDS both sides — interior' if row[0] == rec and row[1] == rec else
                   'holds one side only — BOUNDARY' if rec in row else
                   'changes both sides')
            print('   null %d  +eps -> %-6s   -eps -> %-6s   %s   |v|max %d'
                  % (i, row[0], row[1], tag, max(abs(x) for x in iv)), flush=True)
        print('   summary over %d signed directions: %d hold, %d change, %d UNEVALUATED'
              % (2 * len(null), same, diff, unev), flush=True)
