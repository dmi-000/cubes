#!/usr/bin/env python3
"""Q0 probe: is 183/393 (all-pairs-family) also SINGLE-AXIS (one global
axis + per-cube face relabeling makes every pair's family axis coincide)?

Method (exact, no floats): for pair (i,j), R = Mi^T Mj. Search cube i's
24-element own symmetry group for Q with (Q^T R)[1][0]==(Q^T R)[0][1]
(family_axis_test's witness). For each such witness Q, the LOCAL axis
vector (in cube i's Q-relabeled frame) is
  L = ((Q^T R)[2][1]-(Q^T R)[1][2], (Q^T R)[0][2]-(Q^T R)[2][0], 0)
(the antisymmetric part of Rel(Delta,psi) always has zero 3rd component,
and the first two components are 2 sinDelta * (sinpsi, cospsi)). The
GLOBAL axis is then G = Mj @ L (since R'w=w with R'=Q^T Mi^T Mj implies
Mi Q w = Mj w -- both sides equal the same global vector; verified
independently as Mi@Q@L too, both must agree -- a built-in sanity check).

For each record, collect per-pair candidate axis LINES (primitive integer
vectors, sign-canonicalized) over ALL witnesses found (there can be more
than one due to cube symmetry). Single-axis iff the per-pair candidate
sets have a common line across ALL pairs simultaneously.
"""
import math
from fractions import Fraction as Fr
from itertools import product

from nfamily_common import (quat_to_matrix_exact, mat_mul, mat_transpose,
                             CUBE_ROT_GROUP)


def mat_vec(M, v):
    return tuple(sum(M[i][k] * v[k] for k in range(3)) for i in range(3))


def canon_line(vec):
    """Reduce a rational 3-vector to a primitive integer direction, sign
    fixed so first nonzero component is positive. Returns None if zero."""
    fracs = [Fr(x) for x in vec]
    if all(f == 0 for f in fracs):
        return None
    lcd = 1
    for f in fracs:
        lcd = lcd * f.denominator // math.gcd(lcd, f.denominator)
    ints = [int(f * lcd) for f in fracs]
    g = math.gcd(*[abs(i) for i in ints])
    if g > 1:
        ints = [i // g for i in ints]
    # sign canonicalize
    for x in ints:
        if x != 0:
            if x < 0:
                ints = [-i for i in ints]
            break
    return tuple(ints)


def all_witnesses(Mi, Mj):
    R = mat_mul(mat_transpose(Mi), Mj)
    out = []
    for Q in CUBE_ROT_GROUP:
        Rp = mat_mul(mat_transpose(Q), R)
        if Rp[1][0] == Rp[0][1]:
            out.append((Q, Rp))
    return out


def pair_axis_candidates(Mi, Mj, Mj_full, Mi_full):
    """Return set of canonical global axis lines for pair using witnesses
    found from BOTH i's side and j's side (union), each cross-checked via
    the two equivalent global formulas."""
    cands = set()
    # i-side: relabel cube i
    for Q, Rp in all_witnesses(Mi, Mj):
        L = (Rp[2][1] - Rp[1][2], Rp[0][2] - Rp[2][0], Fr(0))
        G1 = mat_vec(Mj, L)
        G2 = mat_vec(mat_mul(Mi, Q), L)
        assert canon_line(G1) == canon_line(G2), 'i-side global axis formulas disagree'
        c = canon_line(G1)
        if c:
            cands.add(c)
    # j-side: relabel cube j, using R2 = Mj^T Mi
    for Q, Rp in all_witnesses(Mj, Mi):
        L = (Rp[2][1] - Rp[1][2], Rp[0][2] - Rp[2][0], Fr(0))
        G1 = mat_vec(Mi, L)
        G2 = mat_vec(mat_mul(Mj, Q), L)
        assert canon_line(G1) == canon_line(G2), 'j-side global axis formulas disagree'
        c = canon_line(G1)
        if c:
            cands.add(c)
    return cands


def analyze(name, total, quats):
    mats = [quat_to_matrix_exact(*q) for q in quats]
    n = len(mats)
    pair_cands = {}
    for i in range(n):
        for j in range(i + 1, n):
            cands = pair_axis_candidates(mats[i], mats[j], mats[j], mats[i])
            pair_cands[(i, j)] = cands
    print(f'\n=== {name} (total={total}, n={n}) ===')
    common = None
    for (i, j), cands in sorted(pair_cands.items()):
        print(f'  pair ({i},{j}): {len(cands)} candidate axis line(s): {sorted(cands)}')
        common = cands if common is None else (common & cands)
    print(f'  INTERSECTION across all pairs: {common}')
    return pair_cands, common


if __name__ == '__main__':
    records = {
        '183 (n=4)': (183, [(1, 0, 0, 0), (0, 5, 3, 2), (1, -4, -1, 1), (1, 1, -1, -4)]),
        '393 (n=5)': (393, [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5), (2, 1, 1, 1), (1, 1, 1, 1)]),
        '723 embedded 5-clique (n=6, cubes 0-4)': (None, [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5), (2, 1, 1, 1), (1, 1, 1, 1)]),
    }
    for name, (total, quats) in records.items():
        analyze(name, total, quats)
