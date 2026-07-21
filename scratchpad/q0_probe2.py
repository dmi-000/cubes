#!/usr/bin/env python3
"""Q0 follow-up: given a candidate global axis s, check per-CUBE (not
per-pair) whether s is expressible in that cube's own relabeled frame as
lying in the local xy-plane (zero z-component) -- i.e. whether the cube
genuinely has a face-axis role consistent with a single shared axis s --
and whether the resulting tilt (tan psi = v0/v1) AGREES across all cubes
that admit such a relabeling. This is the real single-axis-family test:
common axis AND common psi, with one relabeling Q_i per CUBE (not per
pair)."""
import math
from fractions import Fraction as Fr

from nfamily_common import quat_to_matrix_exact, mat_mul, mat_transpose, CUBE_ROT_GROUP


def mat_vec(M, v):
    return tuple(sum(M[i][k] * v[k] for k in range(3)) for i in range(3))


def per_cube_options(Mi, s):
    """All Q in the 24-group such that Q^T (Mi^T s) has zero z-component.
    Returns list of (Q, (v0,v1)) with (v0,v1) the in-plane components
    (exact Fractions, un-normalized -- but |s| is common to all cubes so
    v0/v1 ratio is directly comparable)."""
    MiT_s = mat_vec(mat_transpose(Mi), s)
    out = []
    for Q in CUBE_ROT_GROUP:
        v = mat_vec(mat_transpose(Q), MiT_s)
        if v[2] == 0:
            out.append((Q, (v[0], v[1])))
    return out


def check_single_axis(name, quats, s, cube_idx=None):
    mats = [quat_to_matrix_exact(*q) for q in quats]
    if cube_idx is None:
        cube_idx = list(range(len(mats)))
    print(f'\n--- {name}: candidate axis s={s} ---')
    tan_psi_values = {}
    for i in cube_idx:
        opts = per_cube_options(mats[i], s)
        ratios = set()
        for Q, (v0, v1) in opts:
            if v1 != 0:
                ratios.add(Fr(v0, v1))
            elif v0 != 0:
                ratios.add('inf')
        print(f'  cube {i}: {len(opts)} relabelings give zero-z; tan(psi) candidates: {sorted(ratios, key=str)}')
        tan_psi_values[i] = ratios
    # does a common tan(psi) exist across ALL cubes simultaneously?
    common = None
    for i in cube_idx:
        common = tan_psi_values[i] if common is None else (common & tan_psi_values[i])
    print(f'  COMMON tan(psi) across all cubes: {common}')
    return common


if __name__ == '__main__':
    quats183 = [(1, 0, 0, 0), (0, 5, 3, 2), (1, -4, -1, 1), (1, 1, -1, -4)]
    quats393 = [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5), (2, 1, 1, 1), (1, 1, 1, 1)]

    # 393: candidate s=(0,3,2) from the unique (0,3) pair witness
    check_single_axis('393 full', quats393, (0, 3, 2))
    # 393 sub-clique {0,2,3,4} (drop cube 1)
    check_single_axis('393 sub-clique {0,2,3,4}', quats393, (0, 3, 2), cube_idx=[0, 2, 3, 4])

    # 183: try each pair's candidate that appears widely. (1,2) gave unique (0,5,2).
    check_single_axis('183 full, s=(0,5,2)', quats183, (0, 5, 2))
    check_single_axis('183 full, s=(3,0,2)', quats183, (3, 0, 2))
    check_single_axis('183 full, s=(3,5,0)', quats183, (3, 5, 0))
