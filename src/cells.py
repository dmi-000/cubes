#!/usr/bin/env python3
"""a, b, m, s for ANY centrally symmetric convex cells -- the shape-general engine.

Everything the Step B machinery does is cube-specific: `step_a3.components` uses
the l1 support function of the box, `step_b.min_l1_hull` likewise, and
`innermost.py` sectorises by the six directions of ||u||_inf.  Postscript 106's
derivation claims the constant in

    s <= a + b + m - 2,   a = comp(Ci\\Cj), b = comp(Ci\\Ck), m = comp(i innermost)

is the FACE COUNT of the cell (m <= F_i, six sectors for a cube), not a universal
4.  That prediction cannot be tested without leaving cubes, which is what this is.

A cell is given by F/2 facet normals N: the body is {x : |n.x| <= 1 for n in N},
centrally symmetric by construction, and its radial extent is
r(u) = 1 / max_{n in N} |n.u|.  All four quantities are then counts of connected
components of cones in R^3:

    K = {r_i > r_j} = union over (n in Nj, sigma = +-1) of the CONVEX cone
        { u : sigma n.u > |m.u| for all m in Ni }
    L  likewise with Nk;  K n L = pairwise intersections of those cones;
    C = complement of K u L, cut by which facet of cell i attains the max --
        one convex cone per (facet, sign), hence m <= F_i immediately.

Each piece is an intersection of homogeneous half-spaces, so nonemptiness is
exact Fourier-Motzkin elimination over the rationals -- no LP solver, no floats.
Components are a union-find over pieces, gluing when two pieces meet: on an open
overlap for the open sets K, L, K n L, and on any shared ray for the closed C
(the convention `innermost.py` already uses).

GATE: on cubes this must reproduce `step_a3.components`, `step_b.singleton_comp`
and `innermost.comp_innermost` exactly, which `--gate` checks on the eight
witnesses of Postscript 106.
"""
import itertools
import sys
from fractions import Fraction as F
import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__))

sys.path.insert(0, HERE)


# ---------------------------------------------------------------- exact solver
def feasible_strict(rows):
    """Is there u in R^3 with row.u > 0 for every row?  Exact Fourier-Motzkin."""
    ineqs = [[F(c) for c in r] for r in rows]          # each means r.u > 0
    for var in range(3):
        pos, neg, zero = [], [], []
        for r in ineqs:
            if r[var] > 0:
                pos.append(r)
            elif r[var] < 0:
                neg.append(r)
            else:
                zero.append(r)
        nxt = list(zero)
        for p in pos:
            for n in neg:
                # eliminate `var`: combine with positive coefficients
                comb = [p[k] * (-n[var]) + n[k] * p[var] for k in range(3)]
                comb[var] = F(0)
                if all(c == 0 for c in comb):
                    return False                        # 0 > 0
                nxt.append(comb)
        ineqs = nxt
        if not ineqs:
            return True
    return not any(all(c == 0 for c in r) for r in ineqs)


def cone_pieces_K(Ni, Nj):
    """The convex cones whose union is K = {r_i > r_j}, as strict-inequality rows."""
    out = []
    for n in Nj:
        for sig in (1, -1):
            sn = [sig * c for c in n]
            rows = []
            for mm in Ni:
                rows.append([sn[t] - mm[t] for t in range(3)])
                rows.append([sn[t] + mm[t] for t in range(3)])
            if feasible_strict(rows):
                out.append(rows)
    return out


def components_of(pieces, glue_strict=True):
    """Union-find over convex pieces; glue when two pieces meet."""
    parent = list(range(len(pieces)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i, j in itertools.combinations(range(len(pieces)), 2):
        if find(i) == find(j):
            continue
        rows = pieces[i] + pieces[j]
        if feasible_strict(rows):
            parent[find(i)] = find(j)
    return len({find(i) for i in range(len(pieces))})


def counts(Ni, Nj, Nk):
    """(a, b, s, m) for cells i, j, k given by their facet normals."""
    Kp = cone_pieces_K(Ni, Nj)
    Lp = cone_pieces_K(Ni, Nk)
    a = components_of(Kp)
    b = components_of(Lp)
    KL = []
    for p in Kp:
        for q in Lp:
            rows = p + q
            if feasible_strict(rows):
                KL.append(rows)
    s = components_of(KL)

    # C = {r_i <= r_j and r_i <= r_k}, cut by which facet of i attains the max
    Cp = []
    for f in Ni:
        for tau in (1, -1):
            tf = [tau * c for c in f]
            rows = []
            for mm in Ni:                      # this facet attains the max
                if mm is f:
                    continue                   # not against itself: 0 > 0
                rows.append([tf[t] - mm[t] for t in range(3)])
                rows.append([tf[t] + mm[t] for t in range(3)])
            rows.append(list(tf))              # ... and on the correct side
            for other in (Nj, Nk):             # and cell i is inside the others
                for n in other:
                    # these conditions are |n.u| <= tf.u -- NON-strict.  A row that
                    # is identically zero (cell i's facet parallel to one of the
                    # other cell's) means 0 <= 0, which is VACUOUS; feeding it to a
                    # strict solver reads it as 0 > 0 and silently deletes a real
                    # component of C.  That bug made m read 4 instead of 6 on cubes
                    # and 2 instead of 4 on prisms, and produced two spurious
                    # violations of the Postscript 106 bound before the
                    # Mayer-Vietoris argument flagged m as impossible (2026-08-12).
                    for row in ([tf[t] - n[t] for t in range(3)],
                                [tf[t] + n[t] for t in range(3)]):
                        if any(row):
                            rows.append(row)
            if feasible_strict(rows):
                Cp.append(rows)
    m = components_of(Cp)
    return a, b, s, m


# ------------------------------------------------------------------- the cells
def cube_normals(q=None):
    from step_a2 import normals
    if q is None:
        return [[F(1), F(0), F(0)], [F(0), F(1), F(0)], [F(0), F(0), F(1)]]
    ns = normals(q)
    return [list(ns[i]) for i in range(0, 6, 2)]       # one per +- pair


def prism_normals(k):
    """A 2k-gonal prism: k side normals (rational, from Pythagorean-ish steps)
    plus the axis -- F = 2k + 2 facets."""
    sides = []
    steps = [(F(1), F(0)), (F(3, 5), F(4, 5)), (F(-3, 5), F(4, 5)),
             (F(5, 13), F(12, 13)), (F(-5, 13), F(12, 13)), (F(8, 17), F(15, 17))]
    for i in range(k):
        cx, cy = steps[i % len(steps)]
        sides.append([cx, cy, F(0)])
    return sides + [[F(0), F(0), F(1)]]


def rotate(N, q):
    from step_a2 import mat
    M = mat(q)
    return [[sum(M[r][c] * n[c] for c in range(3)) for r in range(3)] for n in N]


# ------------------------------------------------------------------- the gates
WITNESSES = {
    '(13,13)': ((1, 2, 1, 1), (-2, 1, 0, -1)),
    '(13,9)': ((2, 1, 1, 1), (2, -1, -2, 0)),
    '(9,9)': ((-1, 0, 2, 2), (-2, 1, -2, 0)),
    '(5,5)': ((-1, -3, -2, -1), (-2, -3, 3, 1)),
    '(4,4)': ((-2, -1, 3, -5), (5, -1, 3, -2)),
}


def gate():
    from step_a2 import normals
    from step_a3 import components
    from step_b import singleton_comp
    from innermost import comp_innermost
    print('GATE — cubes: this engine vs the cube-specific machinery')
    print('%-9s %-16s %-16s %-16s %-16s' % ('combo', 'a (step_a3)', 'b (step_a3)',
                                            's (step_b)', 'm (innermost)'))
    ok = True
    for k, (qa, qb) in WITNESSES.items():
        nj, nk = normals(qa), normals(qb)
        want = (components(nj), components(nk), singleton_comp(nj, nk)[0],
                comp_innermost(nj, nk))
        got = counts(cube_normals(), cube_normals(qa), cube_normals(qb))
        ok &= got == want
        print('%-9s %-16s %-16s %-16s %-16s  %s'
              % (k, '%d / %d' % (got[0], want[0]), '%d / %d' % (got[1], want[1]),
                 '%d / %d' % (got[2], want[2]), '%d / %d' % (got[3], want[3]),
                 'ok' if got == want else 'MISMATCH'))
    print('GATE %s' % ('PASS' if ok else 'FAIL'))
    return ok


if __name__ == '__main__':
    gate()
