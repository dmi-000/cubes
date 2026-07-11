#!/usr/bin/env python3
# Working principles: six_cube_search_results.md (original region counter). Project index: README.md
"""Count the 3D regions formed by a compound of n cubes (or other bodies).

Method
------
Voxel flood-fill on a grid over [-L, L]^3:
  1. Each voxel center gets an n-bit label: bit k set iff the point is inside
     body k (cube k = rotated copy of the axis-aligned cube [-1,1]^3).
  2. Regions = connected components (6-connectivity) of constant label,
     summed over all labels. The unbounded outside is label 0 (must be
     exactly 1 component: all compounds here are concentric convex bodies,
     so the union is star-shaped w.r.t. the origin -> no cavities, and every
     bounded region lies inside the union).

Known artifacts (both diagnosed empirically)
--------------------------------------------
1. TIP FRAGMENTS: a region with a thin tapering corner (acute wedge between
   two nearly-parallel faces) loses its tip across a sub-voxel neck; the tip
   shows up as a separate component ~O(R) voxels (e.g. 1-pixel column of
   full height), while genuine regions scale ~R^3.  Fix: merge any SMALL
   component (< tau ~ 3R voxels) into a same-label BIG component found
   within a few voxels of it.
2. POINT CONTACTS: two genuinely DISTINCT same-label regions can touch at a
   point (stella octangula spikes at the edge-edge crossings).  Therefore
   big components are NEVER merged with each other - only small->big.
Small components with no big same-label neighbour are counted but reported
as 'unresolved'; verify them by re-running at higher resolution (real
regions keep constant physical volume ~R^3, fragments grow only ~R).

Validation targets (hand-derived)
---------------------------------
  one      -> 1 bounded region (+ outside)
  stella   -> 9 bounded: 8 spikes + central octahedron   (Euler check:
              V=14, E=36, F=32 -> cells = V-E+F = 10 incl. outside)
  axialN   -> (2N-1)^2 bounded. N congruent cubes sharing a 4-fold axis,
              distinct twists: cross-section = N concentric squares whose
              edge lines are all tangent to the common incircle, so no
              triple points; 2D Euler: V=4N^2, E=8N^2-4N ->
              bounded 2D faces = (2N-1)^2; prism structure makes the 3D
              bounded count equal the 2D one.

Compounds
---------
  escher3 : 3 cubes, 45 deg about x, y, z          (rigid, octahedral, UC08)
  bakos4  : 4 cubes, 60 deg about the body diagonals (rigid, octahedral)
  five5   : the 5 cubes of the dodecahedron          (rigid, icosahedral, UC09)
            cube 0 axis-aligned, others rotated by k*72 deg about the
            5-fold axis (1, 0, phi)  [dodecahedron face axis for the
            vertex convention (+-1,+-1,+-1) u cyclic(0,+-1/phi,+-phi);
            NOTE: (0,1,phi) is the WRONG chirality class and fails the
            vertex check below]
  six6:THETA : 6 cubes, +-THETA deg about x, y, z   (rotational freedom, UC07;
            degenerates to escher3 at THETA=45)
  axialN[:TWIST0,TWIST1,...] : N cubes about the shared z (4-fold) axis,
            default twists k*90/N deg.

Usage
-----
  python3 cube_compound_regions.py count one:200 stella:260 axial3:260
  python3 cube_compound_regions.py count escher3:300 bakos4:300 five5:300
  python3 cube_compound_regions.py count five5:420 --min-size 8
  python3 cube_compound_regions.py diagnose axial3:260
  python3 cube_compound_regions.py check       # five5 vertex sanity check
"""
import argparse
import math
import sys

import numpy as np
from scipy import ndimage as ndi

PHI = (1 + 5 ** 0.5) / 2
FIVE_AXIS = (1.0, 0.0, PHI)  # 5-fold (face) axis of the standard dodecahedron
JITTER = (0.00123, 0.00234, 0.00345)  # avoid voxel centers on boundaries/symmetry planes

# regular tetrahedron pair (stella octangula) for validation
TET_V = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], float)


def rodrigues(axis, theta):
    a = np.asarray(axis, float)
    a = a / np.linalg.norm(a)
    K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + math.sin(theta) * K + (1 - math.cos(theta)) * (K @ K)


def compound(name):
    """Return list of rotation matrices R_k; cube k = R_k([-1,1]^3)."""
    if name == 'one':
        return [np.eye(3)]
    if name == 'escher3':
        return [rodrigues(ax, math.pi / 4)
                for ax in ([1, 0, 0], [0, 1, 0], [0, 0, 1])]
    if name == 'bakos4':
        return [rodrigues(d, math.pi / 3)
                for d in ([1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1])]
    if name.startswith('five'):
        # 'fiveN', N=1..5: first N cubes of the five-cube compound.
        # A5 is 3-transitive on the cubes, so any pair/triple/quadruple is
        # equivalent to any other; the first N are representative.
        N = int(name[4:])
        if not 1 <= N <= 5:
            raise ValueError('fiveN needs N in 1..5')
        return [rodrigues(FIVE_AXIS, 2 * math.pi * k / 5) for k in range(N)]
    if name.startswith('six6'):
        th = math.radians(float(name.split(':')[1])) if ':' in name else math.radians(20)
        out = []
        for ax in ([1, 0, 0], [0, 1, 0], [0, 0, 1]):
            out += [rodrigues(ax, th), rodrigues(ax, -th)]
        return out
    if name.startswith('axial'):
        spec = name[5:]
        if ':' in spec:
            nstr, twists = spec.split(':')
            angles = [math.radians(float(t)) for t in twists.split(',')]
        else:
            n = int(spec)
            angles = [k * (math.pi / 2) / n for k in range(n)]
        return [rodrigues([0, 0, 1], a) for a in angles]
    raise ValueError(f'unknown compound {name!r}')


GENERIC_ROT = rodrigues([1.0, 0.7, 0.3], 0.37)  # de-align compound from the grid


def labels_grid(name, R, L=1.8, jit=JITTER):
    """n-bit inside/outside label for each voxel center, built slab-wise.

    Suffix '+rot' applies one generic global rotation to the whole compound:
    region counts are rotation-invariant, but this removes grid/face
    alignments (an axis-aligned cube systematically false-merges regions
    separated by sub-voxel slabs parallel to the grid).
    """
    grot = None
    if name.endswith('+rot'):
        name = name[:-4]
        grot = GENERIC_ROT
    xs = [np.linspace(-L, L, R) + j for j in jit]
    X2, X3 = np.meshgrid(xs[1], xs[2], indexing='ij')
    if name == 'stella':
        label = np.zeros((R, R, R), np.uint8)
        for iz in range(R):
            pts = np.stack([np.full_like(X2, xs[0][iz]), X2, X3], -1)
            d = pts @ TET_V.T
            in1 = (d >= -1.0).all(-1)          # tetra with vertices  TET_V
            in2 = (d <= 1.0).all(-1)           # its central inversion
            label[iz] = in1.astype(np.uint8) | (in2.astype(np.uint8) << 1)
        return label, 2
    mats = compound(name)
    if grot is not None:
        mats = [grot @ Rk for Rk in mats]
    n = len(mats)
    dt = np.uint8 if n <= 8 else np.uint16
    label = np.zeros((R, R, R), dt)
    for iz in range(R):
        pts = np.stack([np.full_like(X2, xs[0][iz]), X2, X3], -1)
        for k, Rk in enumerate(mats):
            u = pts @ Rk                       # = R_k^T x ; inside iff max|u| <= 1
            inside = np.max(np.abs(u), -1) <= 1.0
            label[iz] |= (inside.astype(dt) << k)
    return label, n


def component_sizes(label):
    """Per-label list of connected-component sizes (6-connectivity)."""
    struct = ndi.generate_binary_structure(3, 1)
    out = {}
    for l in np.unique(label):
        lab, nc = ndi.label(label == l, structure=struct)
        sizes = np.bincount(lab.ravel())[1:]
        out[int(l)] = np.sort(sizes)[::-1]
    return out


def count(name, R, tau=None):
    """Region count with small->big same-label fragment merging (see docstring)."""
    label, _ = labels_grid(name, R)
    tau = tau or 3 * R
    struct = ndi.generate_binary_structure(3, 1)
    tot = 0
    unresolved = 0
    by_depth = {}
    per_label = {}
    for l in np.unique(label):
        lab, nc = ndi.label(label == l, structure=struct)
        sizes = np.bincount(lab.ravel())
        big = {i for i in range(1, nc + 1) if sizes[i] >= tau}
        cnt = len(big)
        slices = ndi.find_objects(lab)
        for i in range(1, nc + 1):
            if i in big:
                continue
            sl = tuple(slice(max(0, s.start - 4), min(dim, s.stop + 4))
                       for s, dim in zip(slices[i - 1], lab.shape))
            sub = lab[sl]
            grown = ndi.binary_dilation(sub == i, structure=struct, iterations=3)
            neigh = set(np.unique(sub[grown])) - {0, i}
            if neigh & big:
                continue            # tip fragment of a big region: merged
            cnt += 1                # no big neighbour: possibly a real tiny region
            unresolved += 1
        tot += cnt
        d = bin(int(l)).count('1')
        by_depth[d] = by_depth.get(d, 0) + cnt
        per_label[int(l)] = cnt
    print(f'{name:12s} R={R:4d}  bounded={tot - 1:5d}  '
          f'(tau={tau} vox, unresolved smalls counted: {unresolved})')
    print(f'{"":12s} by depth (0=outside): {dict(sorted(by_depth.items()))}')
    print(f'{"":12s} per label: {per_label}')
    return tot - 1


def diagnose(name, R):
    for l, sz in component_sizes(labels_grid(name, R)[0]).items():
        print(f'label {l:3d} (depth {bin(l).count("1")}): ncomp={len(sz):4d}  sizes={sz[:15]}')


def check_five():
    dod = {s for s in __import__('itertools').product((1, -1), repeat=3)}
    dod = {tuple(map(float, s)) for s in dod}
    a, b = 1 / PHI, PHI
    for base in [(0, a, b), (a, b, 0), (b, 0, a)]:
        nz = [i for i, c in enumerate(base) if c]
        for s1 in (1, -1):
            for s2 in (1, -1):
                q = list(base)
                q[nz[0]] *= s1
                q[nz[1]] *= s2
                dod.add(tuple(q))
    dod = np.array(sorted(dod))
    corners = np.array(list(__import__('itertools').product((1, -1), repeat=3)), float)
    worst = 0.0
    for Rk in compound('five5'):
        for v in corners:
            worst = max(worst, float(np.min(np.linalg.norm(dod - Rk @ v, axis=1))))
    print(f'five5 vertex check: max distance of rotated corners from '
          f'dodecahedron vertex set = {worst:.2e}  ({"OK" if worst < 1e-9 else "FAIL"})')


if __name__ == '__main__':
    import sys as _sys
    if len(_sys.argv) > 1 and _sys.argv[1] in ('-h', '--help'):
        print(__doc__ or __file__); raise SystemExit(0)
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('mode', choices=['count', 'diagnose', 'check'])
    p.add_argument('cases', nargs='*', help='name:resolution, e.g. five5:300')
    p.add_argument('--min-size', type=int, default=8,
                   help='voxel threshold separating regions from pinch artifacts')
    args = p.parse_args()
    if args.mode == 'check':
        check_five()
        sys.exit(0)
    for case in args.cases:
        nm, R = case.rsplit(':', 1)
        (count if args.mode == 'count' else diagnose)(nm, int(R))
