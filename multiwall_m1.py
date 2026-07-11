#!/usr/bin/env python3
# Working principles: MULTIWALL_SPEC.md + multiwall_report.md. Project index: README.md
"""M1 (mechanism A): within-Q(sqrt5) stacked walls, existing Q5 engine only.
Logs to multiwall_search.jsonl. Does NOT modify certify_six.py / golden_six.py.
"""
import json
import time
from itertools import product

from golden_six import golden_five
from golden_rotations import rot_from_quat, Rot
from certify_six import exact_count_config

LOG = '/Users/dmi/carroll/multiwall_search.jsonl'


def log(rec):
    with open(LOG, 'a') as f:
        f.write(json.dumps(rec) + '\n')
        f.flush()


def m1b():
    """sixth = g5[k] * D(+-60deg about local body diagonal), for each of the
    5 golden cubes k and each of its 4 body-diagonal directions (8 signed
    quats). D60 built via rot_from_quat(3,s0,s1,s2) / (3,-s0,-s1,-s2) (exact
    rational 60/-60deg about (1,s0,s1,s2)... using standard body-diagonal
    quats matching golden_six.symmetric_candidates' convention)."""
    g5 = golden_five()
    diag_quats = []
    for s1, s2 in product((1, -1), repeat=2):
        diag_quats.append((f'60_(1,{s1},{s2})', (3, 1, s1, s2)))
        diag_quats.append((f'-60_(1,{s1},{s2})', (3, -1, -s1, -s2)))
    results = []
    for k in range(5):
        for tag, q in diag_quats:
            D = rot_from_quat(*q)
            sixth = g5[k] * D
            t0 = time.time()
            total, bd = exact_count_config(g5 + [sixth], verbose=False)
            dt = time.time() - t0
            rec = dict(family='M1b', anchor_cube=k, tag=tag, quat=list(q),
                       total=total, by_depth={int(a): b for a, b in bd.items()},
                       secs=round(dt, 1))
            log(rec)
            results.append(rec)
            print(f'  M1b cube{k} {tag:16s} total={total:4d} ({dt:.1f}s)',
                  flush=True)
    best = max(results, key=lambda r: r['total'])
    print(f'M1b best: cube{best["anchor_cube"]} {best["tag"]} '
          f'total={best["total"]}')
    return results


def m1a():
    """sixth = g5[k] * R_z(phi): shares one face-plane exactly with golden
    cube k (whichever axis maps to R_z's fixed z-column); phi ranges over
    rational quaternion angles about z (quaternion (a,0,0,b)). Coincident
    plane, in-plane free rotation."""
    g5 = golden_five()
    # rational angle candidates about z: (a,b) -> angle 2*atan2(b,a)
    angle_quats = [(1, 0), (4, 3), (3, 4), (5, 12), (12, 5), (1, 1), (1, 2),
                   (2, 1), (7, 1), (1, 7), (5, 3), (3, 5), (8, 15), (15, 8)]
    results = []
    for k in range(5):
        for a, b in angle_quats:
            Rz = rot_from_quat(a, 0, 0, b)
            sixth = g5[k] * Rz
            t0 = time.time()
            total, bd = exact_count_config(g5 + [sixth], verbose=False)
            dt = time.time() - t0
            rec = dict(family='M1a', anchor_cube=k, quat=[a, 0, 0, b],
                       total=total, by_depth={int(x): y for x, y in bd.items()},
                       secs=round(dt, 1))
            log(rec)
            results.append(rec)
            print(f'  M1a cube{k} angle_quat=({a},0,0,{b}) total={total:4d} '
                  f'({dt:.1f}s)', flush=True)
    best = max(results, key=lambda r: r['total'])
    print(f'M1a best: cube{best["anchor_cube"]} quat={best["quat"]} '
          f'total={best["total"]}')
    return results


if __name__ == '__main__':
    import sys as _sys
    if len(_sys.argv) > 1 and _sys.argv[1] in ('-h', '--help'):
        print(__doc__ or __file__); raise SystemExit(0)
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else 'both'
    if mode in ('m1b', 'both'):
        print('=== M1(b): 60deg about each golden cube\'s own body diagonal ===')
        m1b()
    if mode in ('m1a', 'both'):
        print('\n=== M1(a): coincident face-plane, free in-plane rotation ===')
        m1a()
