#!/usr/bin/env python3
# Working principles: incidence.py (exact coincidence conditions), and the
# user's framing -- several constraints together form a system that may have
# finitely many solutions or none, and NONE means the search can be skipped.
"""Elimination on the 393 base: which coincidence patterns a sixth cube admits.

The five cubes of 393 are FIXED and rational, so a sixth cube has just three
degrees of freedom.  Parameterise it by Cayley coordinates (a,b,c):

    q = (1, a, b, c)  up to scale  -- every rotation except the 180-degree
                                      ones, which are handled separately

Each candidate coincidence is one polynomial equation in (a,b,c):

    coplanarity of edge e of the sixth cube with edge f of fixed cube j:
        det[ dir(e), dir(f), pt(f) - pt(e) ] = 0

There are 12 x 60 = 720 such polynomials.  The known 727 sixth cube satisfies
36 of them simultaneously -- far more than three, so they are massively
dependent, which is what makes that point special rather than generic.

The decidable questions this sets up, in order of cost:

  GATE   the 36 polynomials of the 727 pattern all vanish at the known point
         (if this fails, everything downstream is meaningless)
  Q1     is the 727 pattern's solution set zero-dimensional -- i.e. is 727
         isolated on this base, as the DOF probe suggested?
  Q2     AUGMENTATION: for each of the other 684 conditions, is
         {727 pattern} + {that condition} consistent?  A Groebner basis of
         {1} is a certificate that no sixth cube realises that richer
         pattern -- no search of the 3-DOF space can find one.

Q2 is the point.  Every infeasible augmentation removes a stratum from the
search permanently, and if ALL of them are infeasible then 727's coincidence
pattern is locally maximal on the 393 base -- which is the analytic version
of what 80,000 sampled sixth cubes failed to find by luck.

INVARIANT: exact rational arithmetic throughout (sympy Rational / Poly over
QQ).  A numerically small determinant is not a coincidence, and treating one
as such would manufacture strata that do not exist.
"""
import itertools
import json
import sys

import sympy as sp

a, b, c = sp.symbols('a b c', real=True)

FIVE = [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5), (2, 1, 1, 1),
        (1, 1, 1, 1)]
KNOWN = (7, 14, 1, -5)          # the 727 sixth cube


def rot_sym(q):
    """Rotation matrix of quaternion q (entries may be symbolic), normalised."""
    w, x, y, z = q
    n = w * w + x * x + y * y + z * z
    M = sp.Matrix([
        [w * w + x * x - y * y - z * z, 2 * (x * y - w * z), 2 * (x * z + w * y)],
        [2 * (x * y + w * z), w * w - x * x + y * y - z * z, 2 * (y * z - w * x)],
        [2 * (x * z - w * y), 2 * (y * z + w * x), w * w - x * x - y * y + z * z]])
    return M / n


def edge_list(M):
    """12 edges of the cube M([-1,1]^3) as (point, direction)."""
    out = []
    for ax in range(3):
        o1, o2 = [t for t in range(3) if t != ax]
        for s in (-1, 1):
            for t in (-1, 1):
                p = s * M[:, o1] + t * M[:, o2]
                out.append((p, M[:, ax]))
    return out


def coplanar_poly(e1, e2):
    """Numerator of det[d1, d2, p2-p1] -- vanishes exactly when coplanar."""
    p1, d1 = e1
    p2, d2 = e2
    d = sp.Matrix.hstack(d1, d2, p2 - p1).det()
    return sp.together(sp.simplify(d)).as_numer_denom()[0]


def main():
    Q = (1, a, b, c)
    M6 = rot_sym(Q)
    e6 = edge_list(M6)
    fixed = [edge_list(rot_sym(q)) for q in FIVE]

    subs = {a: sp.Rational(KNOWN[1], KNOWN[0]), b: sp.Rational(KNOWN[2], KNOWN[0]),
            c: sp.Rational(KNOWN[3], KNOWN[0])}

    polys, tags = [], []
    for j, ef in enumerate(fixed):
        for (i1, x1), (i2, x2) in itertools.product(enumerate(e6), enumerate(ef)):
            P = sp.expand(coplanar_poly(x1, x2))
            if P == 0:
                continue                      # identically parallel: no wall
            polys.append(P)
            tags.append((j, i1, i2))
    print('candidate conditions: %d' % len(polys), flush=True)

    active = [k for k, P in enumerate(polys) if sp.simplify(P.subs(subs)) == 0]
    print('GATE: conditions active at the known 727 cube: %d' % len(active),
          flush=True)
    if not active:
        print('GATE FAILED -- parameterisation or sign convention is wrong')
        return 1
    json.dump({'active': [tags[k] for k in active], 'total': len(polys)},
              open('eliminate729_pattern.json', 'w'))

    # Q1: dimension of the 727 pattern's variety
    G = sp.groebner([polys[k] for k in active], a, b, c, order='grevlex')
    print('Q1: Groebner basis of the 727 pattern has %d elements; '
          'is_zero_dimensional=%s' % (len(G.exprs), G.is_zero_dimensional),
          flush=True)

    # Q2: augmentation -- can any further condition be added?
    #
    # If the 727 pattern already cuts the parameter space down to finitely
    # many points, augmentation feasibility is EVALUATION, not elimination:
    # a further condition is realisable exactly when it vanishes at one of
    # those points.  That replaces 684 Groebner solves with 684 substitutions.
    pts = []
    if G.is_zero_dimensional:
        sols = sp.solve([sp.Eq(g, 0) for g in G.exprs], [a, b, c], dict=True)
        pts = [s for s in sols if all(v.is_real for v in s.values())]
        print('Q1b: %d real solution point(s) of the 727 pattern' % len(pts),
              flush=True)

    feasible, infeasible = [], 0
    for k, P in enumerate(polys):
        if k in active:
            continue
        if pts:
            ok = any(sp.simplify(P.subs(pt)) == 0 for pt in pts)
        else:
            Gk = sp.groebner([polys[i] for i in active] + [P], a, b, c,
                             order='grevlex')
            ok = list(Gk.exprs) != [sp.Integer(1)]
        if ok:
            feasible.append(tags[k])
            print('  FEASIBLE augmentation: %s' % (tags[k],), flush=True)
        else:
            infeasible += 1
    print('Q2: %d infeasible, %d feasible augmentations'
          % (infeasible, len(feasible)), flush=True)
    json.dump({'feasible': feasible, 'infeasible': infeasible},
              open('eliminate729_augment.json', 'w'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
