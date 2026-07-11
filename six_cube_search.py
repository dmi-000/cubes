#!/usr/bin/env python3
# Working principles: six_cube_search_results.md. Project index: README.md
"""Search over compounds of 6 congruent concentric cubes for the configuration
that maximizes the number of BOUNDED regions the 6 cube surfaces cut space into.

Extends cube_compound_regions.py additively: does not modify any validated
logic there, only imports it and adds a matrix-list-based labels/count path
(the existing compound()/labels_grid()/count() only accept named presets).

Usage
-----
  python3 six_cube_search.py sweep      # theta-sweep of six6 family
  python3 six_cube_search.py axial      # axial6 baseline sanity (a few twist sets)
  python3 six_cube_search.py random     # ~40 random 6-cube compounds, seeds 0..39
  python3 six_cube_search.py climb      # hill-climb from the best-so-far configs
  python3 six_cube_search.py refine     # re-run best configs at R=300, R=380
"""
import json
import math
import sys
import time

import numpy as np
from scipy import ndimage as ndi
from scipy.spatial.transform import Rotation

import cube_compound_regions as ccr

GENERIC_ROT = ccr.GENERIC_ROT
JITTER = ccr.JITTER


def labels_grid_mats(mats, R, L=1.8, jit=JITTER, grot=True):
    """Same slab-wise labeling as ccr.labels_grid, but takes an explicit list
    of rotation matrices instead of a preset name. grot=True applies the
    module's fixed generic global rotation to de-align from the voxel grid
    (mandatory here since random/six6 cubes are otherwise axis-ish aligned)."""
    if grot:
        mats = [GENERIC_ROT @ Rk for Rk in mats]
    n = len(mats)
    dt = np.uint8 if n <= 8 else np.uint16
    xs = [np.linspace(-L, L, R) + j for j in jit]
    X2, X3 = np.meshgrid(xs[1], xs[2], indexing='ij')
    label = np.zeros((R, R, R), dt)
    for iz in range(R):
        pts = np.stack([np.full_like(X2, xs[0][iz]), X2, X3], -1)
        for k, Rk in enumerate(mats):
            u = pts @ Rk
            inside = np.max(np.abs(u), -1) <= 1.0
            label[iz] |= (inside.astype(dt) << k)
    return label, n


def count_mats(mats, R, tau=None, verbose=True, name='cfg', grot=True):
    """Bounded-region count for an explicit rotation-matrix list. Identical
    small->big merge policy and tau=3R default as ccr.count().

    grot: apply the fixed generic global rotation (as the '+rot' suffix
    does in ccr.labels_grid). Recommended for axis-aligned/structured
    families (six6, axial) per the module docstring -- BUT empirically for
    the axial family the un-rotated (jitter-only) path already avoids grid
    artifacts and is *more* stable (see six_cube_search_results.md); grot
    is exposed as a flag rather than hardcoded so callers can pick per
    family instead of assuming '+rot' always helps."""
    label, _ = labels_grid_mats(mats, R, grot=grot)
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
                continue
            cnt += 1
            unresolved += 1
        tot += cnt
        d = bin(int(l)).count('1')
        by_depth[d] = by_depth.get(d, 0) + cnt
        per_label[int(l)] = cnt
    bounded = tot - 1
    if verbose:
        print(f'{name:20s} R={R:4d}  bounded={bounded:5d}  '
              f'(tau={tau} vox, unresolved smalls counted: {unresolved})')
        print(f'{"":20s} by depth (0=outside): {dict(sorted(by_depth.items()))}')
    return bounded, unresolved, by_depth, per_label


def random_mats(seed):
    rot = Rotation.random(6, random_state=seed)
    return [m for m in rot.as_matrix()]


def perturb_mats(mats, deg, seed):
    rng = np.random.default_rng(seed)
    out = []
    for M in mats:
        axis = rng.normal(size=3)
        axis /= np.linalg.norm(axis)
        theta = math.radians(deg) * rng.uniform(-1, 1)
        dM = ccr.rodrigues(axis, theta)
        out.append(dM @ M)
    return out


def six6_mats(theta_deg):
    th = math.radians(theta_deg)
    out = []
    for ax in ([1, 0, 0], [0, 1, 0], [0, 0, 1]):
        out += [ccr.rodrigues(ax, th), ccr.rodrigues(ax, -th)]
    return out


def sweep(R=200):
    results = []
    for T in [5, 10, 15, 20, 25, 30, 35, 40, 44]:
        t0 = time.time()
        mats = six6_mats(T)
        b, u, bd, pl = count_mats(mats, R, name=f'six6:{T}')
        results.append(dict(kind='six6', theta=T, R=R, bounded=b, unresolved=u,
                             by_depth=bd, dt=time.time() - t0))
    return results


def axial_baseline(R=300, grot=False):
    results = []
    twist_sets = [
        [0, 15, 30, 45, 60, 75],
        [0, 7, 19, 33, 51, 80],
        [3, 11, 26, 40, 58, 71],
    ]
    for i, tw in enumerate(twist_sets):
        mats = [ccr.rodrigues([0, 0, 1], math.radians(t)) for t in tw]
        b, u, bd, pl = count_mats(mats, R, name=f'axial6:set{i}', grot=grot)
        results.append(dict(kind='axial6', twists=tw, R=R, bounded=b, unresolved=u,
                             by_depth=bd))
    return results


def random_search(R=200, nseeds=40):
    results = []
    for seed in range(nseeds):
        t0 = time.time()
        mats = random_mats(seed)
        b, u, bd, pl = count_mats(mats, R, name=f'rand:{seed}')
        results.append(dict(kind='random', seed=seed, R=R, bounded=b, unresolved=u,
                             by_depth=bd, dt=time.time() - t0))
    return results


def hill_climb(mats0, R, steps=10, deg0=5.0, name='climb', seed0=1000):
    cur = mats0
    cur_b, cur_u, cur_bd, _ = count_mats(cur, R, name=f'{name}:start')
    history = [dict(step=-1, bounded=cur_b, unresolved=cur_u)]
    for s in range(steps):
        deg = deg0 * (1 - 0.6 * s / max(1, steps - 1))  # anneal 5deg -> 2deg
        cand = perturb_mats(cur, deg, seed0 + s)
        b, u, bd, _ = count_mats(cand, R, name=f'{name}:step{s}')
        history.append(dict(step=s, bounded=b, unresolved=u, deg=deg))
        if b > cur_b:
            cur, cur_b, cur_u, cur_bd = cand, b, u, bd
    return cur, cur_b, cur_u, history


if __name__ == '__main__':
    import sys as _sys
    if len(_sys.argv) > 1 and _sys.argv[1] in ('-h', '--help'):
        print(__doc__ or __file__); raise SystemExit(0)
    mode = sys.argv[1] if len(sys.argv) > 1 else 'sweep'
    if mode == 'sweep':
        out = sweep()
    elif mode == 'axial':
        out = axial_baseline()
    elif mode == 'random':
        out = random_search()
    else:
        print('unknown mode; use sweep|axial|random')
        sys.exit(1)
    print(json.dumps(out, default=str))
