#!/usr/bin/env python3
# Working principles: six_cube_search_results.md (Postscript 2, pair walls). Project index: README.md
"""Pair-count checks prompted by a surprise: all 215 generic pairs counted
exactly 4 bounded regions, while the five-compound pair is certified 13 and
the axial pair 9.  Hypothesis: 13 and 9 live on DEGENERATE walls (shared
corners / coincident faces), and 4 is the generic-chamber value; the walls
carry MORE regions than the chambers around them (pinches split the
wrap-around shells into separated spikes).

Checks:
  1. five-compound pair through exact_count_config      -> must be 13
  2. Pythagorean axial pair (0 deg, 36.87 deg about z)  -> must be 9
  3. the same two pairs perturbed off their walls       -> new information:
     does the wall value persist in a neighbouring chamber, or collapse
     toward the generic 4?
"""
import math

import numpy as np

from certify_six import rationalize, exact_count_config
from cube_compound_exact import build_axes, find_cubes
from exact_search import pyth_rot_z
from golden_rotations import Rot
from cube_compound_regions import rodrigues


def golden_cube_matrices():
    axes = build_axes()
    triples = find_cubes(axes)
    rots = []
    for t in triples:
        cols = [axes[i] for i in t]
        rots.append(Rot([[cols[j][i] for j in range(3)] for i in range(3)]))
    return rots


def as_float(rot):
    return np.array([[float(e) for e in row] for row in rot.m])


def main():
    golden = golden_cube_matrices()

    total, bd = exact_count_config(golden[:2], verbose=False)
    print(f'five-compound pair: EXACT {total} (expect 13)  depth {dict(sorted(bd.items()))}')

    pair_ax = [pyth_rot_z(1, 0, 1), pyth_rot_z(4, 3, 5)]
    total, bd = exact_count_config(pair_ax, verbose=False)
    print(f'pythagorean axial pair: EXACT {total} (expect 9)  depth {dict(sorted(bd.items()))}')

    # perturb one cube of each pair by ~1 degree about a generic axis,
    # rationalized; does the wall value survive into the open chamber?
    d = rodrigues([1.0, 0.6, 0.2], math.radians(1.0))
    for name, pair in (('five-pair', golden[:2]), ('axial pair', pair_ax)):
        mats = [as_float(pair[0]), d @ as_float(pair[1])]
        rats = rationalize(mats, 4096)     # fine scale: stay near the wall
        total, bd = exact_count_config(rats, verbose=False)
        print(f'{name} perturbed 1 deg: EXACT {total}  depth {dict(sorted(bd.items()))}')
    for name, pair in (('five-pair', golden[:2]), ('axial pair', pair_ax)):
        d2 = rodrigues([1.0, 0.6, 0.2], math.radians(8.0))
        mats = [as_float(pair[0]), d2 @ as_float(pair[1])]
        rats = rationalize(mats, 4096)
        total, bd = exact_count_config(rats, verbose=False)
        print(f'{name} perturbed 8 deg: EXACT {total}  depth {dict(sorted(bd.items()))}')


if __name__ == '__main__':
    import sys as _sys
    if len(_sys.argv) > 1 and _sys.argv[1] in ('-h', '--help'):
        print(__doc__ or __file__); raise SystemExit(0)
    main()
