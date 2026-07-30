#!/usr/bin/env python3
# Working principles: exact rational arithmetic only (Fraction); a coincidence
# is an EQUATION, so a floating-point "almost zero" is not a coincidence.
"""Exact incidence signature of a cube against a fixed set of cubes.

A contact in this project is an edge of one cube crossing an edge of another
(Postscript 40: those are exactly the degree-4 vertices of the pairwise
intersection polytope, and they carry the contact half of the Euler budget).
Each such crossing is TWO conditions in general position:

    coplanarity  det[d_i, d_j, c_j - c_i] = 0      <- the algebraic equation
    interiority  |u_i| <= 1 and |u_j| <= 1         <- an inequality, not a wall

Only the first is a wall in configuration space.  This module reports both,
because the elimination that follows needs the equation count m (how many
independent conditions a candidate already satisfies) while the region count
only changes when an interior crossing appears or leaves.

Used to set up the 729 feasibility question: with the five cubes of 393 held
fixed, the sixth has 3 degrees of freedom, so at most 3 INDEPENDENT
coplanarity conditions can be imposed generically -- any pattern needing more
is infeasible unless the conditions are dependent, which is what symmetry
buys.  Counting m for the known 727 tells us where in that budget it sits.
"""
import itertools
from fractions import Fraction as F


def rot(q):
    """Exact rotation matrix of an integer quaternion, entries in Q."""
    w, x, y, z = q
    n = F(w * w + x * x + y * y + z * z)
    return [[F(w * w + x * x - y * y - z * z) / n, F(2 * (x * y - w * z)) / n,
             F(2 * (x * z + w * y)) / n],
            [F(2 * (x * y + w * z)) / n, F(w * w - x * x + y * y - z * z) / n,
             F(2 * (y * z - w * x)) / n],
            [F(2 * (x * z - w * y)) / n, F(2 * (y * z + w * x)) / n,
             F(w * w - x * x - y * y + z * z) / n]]


def col(R, j):
    return [R[0][j], R[1][j], R[2][j]]


def edges(q):
    """The 12 edges as (point_on_edge, direction); both exact."""
    R = rot(q)
    out = []
    for a in range(3):
        b, c = [t for t in range(3) if t != a]
        for s in (-1, 1):
            for t in (-1, 1):
                p = [s * col(R, b)[k] + t * col(R, c)[k] for k in range(3)]
                out.append((p, col(R, a)))
    return out


def cross(u, v):
    return [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2],
            u[0] * v[1] - u[1] * v[0]]


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def crossing(e1, e2):
    """(coplanar, interior) for two edges, exactly."""
    p1, d1 = e1
    p2, d2 = e2
    n = cross(d1, d2)
    nn = dot(n, n)
    if nn == 0:
        return (False, False)                      # parallel: no isolated wall
    w = [p2[k] - p1[k] for k in range(3)]
    if dot(w, n) != 0:
        return (False, False)
    # coplanar and non-parallel => the lines meet; locate the point on each
    u1 = F(dot(cross(w, d2), n), 1) / nn
    u2 = F(dot(cross(w, d1), n), 1) / nn
    return (True, abs(u1) <= 1 and abs(u2) <= 1)


def signature(cfg, k):
    """Coincidences of cube k against every other cube of cfg."""
    ek = edges(cfg[k])
    tot_cop = tot_int = 0
    per = {}
    for j, q in enumerate(cfg):
        if j == k:
            continue
        cop = inte = 0
        for e1, e2 in itertools.product(ek, edges(q)):
            c, i = crossing(e1, e2)
            cop += c
            inte += i
        per[j] = (cop, inte)
        tot_cop += cop
        tot_int += inte
    return tot_cop, tot_int, per


FIVE = [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5), (2, 1, 1, 1),
        (1, 1, 1, 1)]                                        # the 393 config
SIXTH = {'727': (7, 14, 1, -5), '727-alt': (15, -12, -2, -13),
         '723': (5, 2, 2, 2), '725-ish generic': (9, 5, -3, 2)}

if __name__ == '__main__':
    for tag, q in SIXTH.items():
        cfg = FIVE + [q]
        cop, inte, per = signature(cfg, 5)
        print('%-16s sixth=%-16s coplanar %3d   interior %3d   per-cube %s'
              % (tag, str(q), cop, inte,
                 [per[j][1] for j in range(5)]), flush=True)
    # baseline: how many coincidences live inside the fixed five themselves
    tot = 0
    for i, j in itertools.combinations(range(5), 2):
        cfg = list(FIVE)
        c = sum(crossing(e1, e2)[1]
                for e1, e2 in itertools.product(edges(cfg[i]), edges(cfg[j])))
        tot += c
    print('within the fixed five: %d interior crossings' % tot)
