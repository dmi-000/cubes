#!/usr/bin/env python3
# Working principles: six_cube_search_results.md. Project index: README.md
"""Certified re-run of the six-cube search: exact counts for rationalized
configurations.

Why this exists: the voxel search's winner (random seed 18) showed a
"plateau" of ~1315-1346 bounded regions across three resolutions -- but
~70% of those components were "unresolved smalls", and the EXACT count of
the rationalized seed-18 configuration is 567.  The plateau was
artifact-dominated (hundreds of tip fragments in a generic 36-plane
arrangement mimic a stable count).  Voxel counts rank configurations
unreliably; the exact pipeline at ~6 s/configuration replaces the
objective outright.

Validation (run first, mandatory):
  - axial fan of 6 cubes with rational (Pythagorean-triple) twists about z
    must count exactly 121 = (2*6-1)^2 (proven analytically);
  - the five-cube compound fed through this generalized pipeline (its
    golden triples as matrix columns) must count exactly 351 (established
    by the dedicated exact counter).

Then every configuration family the voxel search tried is rationalized
(common-scale integer quaternions, N=512) and counted exactly.  Claims are
about the rationalized configurations - a dense set, which is all a search
needs.

Usage:  python3 exact_search.py validate | batch
"""
import sys
import time
from fractions import Fraction as Fr

from cube_compound_exact import Q5, ZERO, ONE, build_axes, find_cubes
from certify_six import rationalize, exact_count_config
from six_cube_search import random_mats, six6_mats
from golden_rotations import Rot


def pyth_rot_z(a, b, c):
    """Exact rotation about z with cos = a/c, sin = b/c (a^2+b^2=c^2)."""
    q = lambda x: Q5(Fr(x, c))
    return Rot([[q(a), q(-b), ZERO], [q(b), q(a), ZERO], [ZERO, ZERO, ONE]])


def validate():
    # six distinct rational twists about z: 0, 16.26, 28.07, 36.87, 43.60,
    # 67.38 degrees -- all distinct mod 90, so the (2N-1)^2 law applies
    zr = [(1, 0, 1), (24, 7, 25), (15, 8, 17), (4, 3, 5), (21, 20, 29),
          (5, 12, 13)]
    rots = [pyth_rot_z(a, b, c) for a, b, c in zr]
    t0 = time.time()
    total, bd = exact_count_config(rots)
    print(f'axial-6 rational twists: EXACT {total} (expect 121)  '
          f'{time.time() - t0:.0f}s  depth {dict(sorted(bd.items()))}')
    assert total == 121

    axes = build_axes()
    triples = find_cubes(axes)
    rots5 = []
    for t in triples:
        cols = [axes[i] for i in t]
        rots5.append(Rot([[cols[j][i] for j in range(3)] for i in range(3)]))
    t0 = time.time()
    total5, bd5 = exact_count_config(rots5)
    print(f'five-cube via general path: EXACT {total5} (expect 351)  '
          f'{time.time() - t0:.0f}s  depth {dict(sorted(bd5.items()))}')
    assert total5 == 351
    print('validation PASS')


def batch():
    results = []
    for seed in range(40):
        rats = rationalize(random_mats(seed), 512)
        t0 = time.time()
        total, bd = exact_count_config(rats)
        print(f'seed {seed:2d}: EXACT {total:5d}  ({time.time() - t0:4.0f}s)  '
              f'depth {dict(sorted(bd.items()))}', flush=True)
        results.append((f'seed{seed}', total))
    for T in (10, 15, 20, 25, 30, 35, 40):
        rats = rationalize(six6_mats(T), 512)
        t0 = time.time()
        total, bd = exact_count_config(rats)
        print(f'six6:{T:2d}: EXACT {total:5d}  ({time.time() - t0:4.0f}s)  '
              f'depth {dict(sorted(bd.items()))}', flush=True)
        results.append((f'six6:{T}', total))
    results.sort(key=lambda r: -r[1])
    print('\nTOP 10 (certified):')
    for name, total in results[:10]:
        print(f'  {name:10s} {total}')


def search(start, end, log='exact_search_results.jsonl'):
    """Open-ended verified search: exact counts for rationalized random
    seeds in [start, end), one JSON line per configuration appended to
    `log`.  Validation runs first (a search whose counter is broken is
    worse than no search).  Prints RECORD lines when the best improves."""
    import json
    validate()
    best = 0
    try:
        with open(log) as f:
            for line in f:
                best = max(best, json.loads(line)['bounded'])
        print(f'resuming: best so far in {log} is {best}', flush=True)
    except FileNotFoundError:
        pass
    with open(log, 'a') as f:
        for seed in range(start, end):
            rats = rationalize(random_mats(seed), 512)
            t0 = time.time()
            total, bd, pl = exact_count_config(rats, with_labels=True)
            rec = dict(seed=seed, bounded=total,
                       by_depth={int(k): v for k, v in bd.items()},
                       per_label={str(k): v for k, v in pl.items() if k},
                       secs=round(time.time() - t0, 1))
            f.write(json.dumps(rec) + '\n')
            f.flush()
            mark = ''
            if total > best:
                best = total
                mark = '   <-- RECORD'
            print(f'seed {seed:5d}: EXACT {total:5d}  '
                  f'({rec["secs"]:5.1f}s){mark}', flush=True)


if __name__ == '__main__':
    import sys as _sys
    if len(_sys.argv) > 1 and _sys.argv[1] in ('-h', '--help'):
        print(__doc__ or __file__); raise SystemExit(0)
    mode = sys.argv[1] if len(sys.argv) > 1 else 'validate'
    if mode == 'validate':
        validate()
    elif mode == 'search':
        start = int(sys.argv[2]) if len(sys.argv) > 2 else 40
        end = int(sys.argv[3]) if len(sys.argv) > 3 else 10 ** 9
        search(start, end)
    else:
        validate()
        batch()
