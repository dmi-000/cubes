#!/usr/bin/env python3
# Working principles: six_cube_search_results.md + CPP_SPEC.md. Project index: README.md
"""Exact certification of the six-cube search winner (random seed 18).

Pipeline (see six_cube_search_results.md for the search itself):
  1. rationalize: each of the 6 winner rotations is rounded to an exact
     RATIONAL rotation via a common-scale integer quaternion (N=512 by
     default: error ~2/N rad ~ 0.22 deg, matrix denominators ~N^2).
     Region counts are locally constant in configuration space (they change
     only on measure-zero degeneracy walls), so if the voxel count of the
     rounded configuration lands in the winner's plateau, the rounding did
     not cross a wall.
  2. voxel check: count_mats on the rationalized configuration at R=300 and
     R=380 must land near the seed-18 plateau (~1315-1346).  If not, retry
     with a finer scale (N=2048).
  3. exact count: the certified-interval kernel (cube_compound_interval)
     generalized from the golden 15-axes setup to arbitrary rational
     orthonormal triples: 36 planes n.x = +-1 with n the COLUMNS of each
     rotation matrix.  Same cell-clipping, facet-identity, phantom-merge
     algorithm; the result is the exact bounded-region count of the
     rationalized configuration, an integer, certified.

The final claim certified is about the RATIONALIZED configuration: 'there
exists a compound of 6 congruent concentric cubes with exactly M bounded
regions', with M expected in the seed-18 plateau.  The float seed-18
configuration itself stays voxel-level (its matrices are not in any Q(sqrt n)).
"""
import math
import sys
import time
from fractions import Fraction as Fr

import numpy as np
from scipy.spatial.transform import Rotation

from cube_compound_exact import Q5, ZERO, ONE
from cube_compound_interval import CN, clip, dot, vadd, vscale, STATS
from golden_rotations import rot_from_quat
from six_cube_search import count_mats, random_mats


def rationalize(mats, N=512):
    """Round float rotation matrices to exact rational rotations.

    INVARIANT: after building each exact rotation, its float image is
    compared against the input matrix.  A quaternion component-order
    mistake (scipy is scalar-LAST; rot_from_quat is scalar-first) would
    produce a perfectly valid but WRONG rotation that is_rotation() cannot
    catch; only this round-trip comparison does."""
    out = []
    for M in mats:
        q = Rotation.from_matrix(M).as_quat()          # x, y, z, w
        comps = (q[3], q[0], q[1], q[2])               # -> w, x, y, z
        ints = [round(c * N) for c in comps]
        if not any(ints):
            ints = [1, 0, 0, 0]
        g = math.gcd(*ints)
        if g > 1:
            ints = [i // g for i in ints]
        Q = rot_from_quat(*ints)
        F = np.array([[float(e) for e in row] for row in Q.m])
        err = float(np.abs(F - np.asarray(M)).max())
        assert err < 3.0 / N + 1e-9, f'rounding error {err} too large'
        out.append(Q)
    return out


def exact_count_config(rots, verbose=True, with_labels=False):
    """Exact bounded-region count for cubes R_k([-1,1]^3), R_k rational.

    Generalization of cube_compound_interval.run(): planes are n.x = +-1
    for n the columns of each rotation matrix (exact unit vectors).
    with_labels=True additionally returns the per-label region counts
    (label = bitmask of containing cubes) for per-subset breakdowns."""
    for k in STATS:
        STATS[k] = 0
    one = CN.leaf(ONE)
    cubes = []
    for R in rots:
        cols = [tuple(CN.leaf(R.m[i][j]) for i in range(3)) for j in range(3)]
        cubes.append(cols)
    nq = len(cubes)

    planes = [(k, j, c) for k in range(nq) for j in range(3) for c in (1, -1)]

    # INVARIANT: coincident planes carry the facets of ALL their owning
    # cubes.  With shared axes (axial / six6 families) several cubes
    # contribute the SAME geometric plane (e.g. z = +-1 for every cube
    # rotated about z); only the first coincident plane ever cuts (later
    # clips find no strict crossing), so every facet on that plane carries
    # the first pid.  A facet is REAL for each owning cube whose face
    # square strictly contains it, and crossing it flips exactly those
    # cubes' bits.  Testing only the first pid's cube wrongly merges cells
    # across another cube's real face -- the phantom-label assert below
    # caught precisely this on the axial-6 validation (121) before
    # coincidence classes were added.  Do not "simplify" back to
    # single-owner testing.
    def plane_key(k, j, c):
        comps = [x.exact() for x in cubes[k][j]]
        s = 0
        for x in comps:
            s = x.sign()
            if s != 0:
                break
        if s < 0:
            comps = [-x for x in comps]
            c = -c
        return (tuple((x.a, x.b) for x in comps), c)

    classes = {}
    for k, j, c in planes:
        classes.setdefault(plane_key(k, j, c), []).append((k, j))
    owners_of = [classes[plane_key(k, j, c)] for (k, j, c) in planes]

    from itertools import product
    B, nB = CN.leaf(Q5(4)), CN.leaf(Q5(-4))
    corners = list(product((B, nB), repeat=3))

    def box_face(fix_axis, val):
        pts = [c for c in corners if c[fix_axis] is val]
        a, b = [i for i in range(3) if i != fix_axis]
        pts.sort(key=lambda p: (p[a].iv[0], p[b].iv[0]))
        p00, p01, p10, p11 = pts
        return [p00, p01, p11, p10]

    cells = [[(('box', i, s), box_face(i, v))
              for i in range(3) for s, v in ((1, B), (-1, nB))]]

    for pid, (k, j, c) in enumerate(planes):
        n = cubes[k][j]
        cq = one if c == 1 else -one
        f = lambda p, n=n, cq=cq: dot(n, p) - cq
        cache = {}
        nxt = []
        for cell in cells:
            neg, pos = clip(cell, f, cache)
            for half in (neg, pos):
                if half is not None:
                    nxt.append([(pid if q == 'cap' else q, loop)
                                for q, loop in half])
        cells = nxt
    if verbose:
        print(f'exact: arrangement cells = {len(cells)}')

    def centroid_pts(pts):
        kk = CN.leaf(Q5(Fr(1, len(pts))))
        s = (CN.leaf(ZERO),) * 3
        for p in pts:
            s = vadd(s, p)
        return vscale(s, kk)

    def label(w):
        lab = 0
        for k in range(nq):
            if all((dot(cubes[k][j], w) - one).sign() < 0 and
                   (dot(cubes[k][j], w) + one).sign() > 0 for j in range(3)):
                lab |= 1 << k
        return lab

    labs = [label(centroid_pts(list({p for _, loop in c for p in loop})))
            for c in cells]

    groups = {}
    for ci, cell in enumerate(cells):
        for pid, loop in cell:
            if isinstance(pid, tuple):
                continue
            groups.setdefault((pid, frozenset(loop)), []).append(ci)

    parent = list(range(len(cells)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for (pid, verts), cs in groups.items():
        assert len(cs) == 2, f'facet shared by {len(cs)} cells'
        a, b = cs
        w = centroid_pts(list(verts))
        flip = 0
        for kk, jj in owners_of[pid]:
            others = [cubes[kk][t] for t in range(3) if t != jj]
            if all((dot(n, w) - one).sign() < 0 and
                   (dot(n, w) + one).sign() > 0 for n in others):
                flip |= 1 << kk
        if flip:
            assert labs[a] ^ labs[b] == flip, 'real facet flip mismatch'
        else:
            assert labs[a] == labs[b], 'phantom facet with differing labels'
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb

    comps = set()
    for ci in range(len(cells)):
        comps.add((labs[ci], find(ci)))
    per_label = {}
    for lab, _r in comps:
        per_label[lab] = per_label.get(lab, 0) + 1
    assert per_label.get(0, 0) == 1, 'outside must be a single region'
    by_depth = {}
    for lab, cnt in per_label.items():
        d = bin(lab).count('1')
        by_depth[d] = by_depth.get(d, 0) + cnt
    total = sum(per_label.values()) - 1
    if with_labels:
        return total, by_depth, per_label
    return total, by_depth


if __name__ == '__main__':
    import sys as _sys
    if len(_sys.argv) > 1 and _sys.argv[1] in ('-h', '--help'):
        print(__doc__ or __file__); raise SystemExit(0)
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 18
    mats = random_mats(seed)

    accepted = None
    for N in (512, 2048):
        rats = rationalize(mats, N)
        fl = [np.array([[float(e) for e in row] for row in Q.m])
              for Q in rats]
        print(f'--- N={N}: voxel check of rationalized configuration')
        b300, u300, _, _ = count_mats(fl, 300, name=f'rat{N}', grot=False)
        b380, u380, _, _ = count_mats(fl, 380, name=f'rat{N}', grot=False)
        if 1250 <= b380 <= 1420:
            accepted = (N, rats, (b300, b380))
            break
        print(f'    outside plateau; refining scale')
    assert accepted, 'no rationalization landed in the plateau'
    N, rats, (b300, b380) = accepted

    print(f'--- exact count (N={N}, matrix heights <= ~{N * N})')
    t0 = time.time()
    total, by_depth = exact_count_config(rats)
    dt = time.time() - t0
    print(f'EXACT bounded regions = {total}   by depth: '
          f'{dict(sorted(by_depth.items()))}')
    print(f'({dt:.0f}s; voxel plateau was ~1315-1346, rationalized voxel '
          f'checks: R300={b300}, R380={b380})')
    nsign = STATS["tier1"] + STATS["tier2"] + STATS["tier3"]
    print(f'sign tiers: {nsign} total | float {STATS["tier1"]} | '
          f'200-bit {STATS["tier2"]} | exact {STATS["tier3"]} '
          f'(zeros {STATS["zero"]})')
