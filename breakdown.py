#!/usr/bin/env python3
# Working principles: six_cube_search_results.md (Postscripts 2-3, per-subset structure). Project index: README.md
"""Per-subset breakdown of a configuration's exact region counts.

Prints, for a given seed (or the current record), the depth-1 count per
cube, the depth-2 count per pair, depth-3 per triple (summary), etc. —
the structure behind the depth histogram, to see whether the observed
ceilings (112 total at depth 1, 208 at depth 2, ...) are balanced per-cube
laws (like depth-5's 6-per-cube) or lopsided global budgets.

Usage: python3 breakdown.py [seed ...]
"""
import sys
from itertools import combinations

from certify_six import rationalize, exact_count_config
from six_cube_search import random_mats


def breakdown(seed):
    rats = rationalize(random_mats(seed), 512)
    total, bd, pl = exact_count_config(rats, verbose=False, with_labels=True)
    print(f'seed {seed}: EXACT {total}  by depth '
          f'{dict(sorted(bd.items()))}')
    per_cube = [pl.get(1 << k, 0) for k in range(6)]
    print(f'  depth-1 per cube : {per_cube}  (sum {sum(per_cube)})')
    pairs = {}
    for i, j in combinations(range(6), 2):
        pairs[(i, j)] = pl.get((1 << i) | (1 << j), 0)
    print(f'  depth-2 per pair : {sorted(pairs.values(), reverse=True)}  '
          f'(sum {sum(pairs.values())})')
    hi = max(pairs.values())
    lo = min(pairs.values())
    print(f'    richest pairs: {[p for p, v in pairs.items() if v == hi]} = {hi}'
          f'   poorest: {[p for p, v in pairs.items() if v == lo]} = {lo}')
    for d in (3, 4):
        subs = [pl.get(sum(1 << i for i in c), 0)
                for c in combinations(range(6), d)]
        print(f'  depth-{d} per {d}-set: min {min(subs)} max {max(subs)} '
              f'sum {sum(subs)}  values {sorted(set(subs), reverse=True)}')
    quints = [pl.get(63 ^ (1 << k), 0) for k in range(6)]
    print(f'  depth-5 per missing-cube: {quints}')


if __name__ == '__main__':
    import sys as _sys
    if len(_sys.argv) > 1 and _sys.argv[1] in ('-h', '--help'):
        print(__doc__ or __file__); raise SystemExit(0)
    seeds = [int(a) for a in sys.argv[1:]] or [2228]
    for s in seeds:
        breakdown(s)
