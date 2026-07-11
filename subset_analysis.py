#!/usr/bin/env python3
# Working principles: six_cube_search_results.md (Postscript 2, subset maximality). Project index: README.md
"""Subset-maximality analysis of the certified 6-cube winner.

Question (2026-07-09): in a maximal 6-cube configuration, are all pairs
maximal 2-configurations?  All triples maximal 3-configurations?  Can all
six 5-subsets be maximal 5-configurations?

Method: exact-count (certify_six.exact_count_config) every k-subset of the
certified winner (random seed 12, rationalized, EXACT 595) for k = 2..5,
and compare against random-search baselines for the empirical maximum at
each k.  Known reference values: generic pair = 13 (6+6+1, the universal
"one piece per face of the subtracted cube" law + convex core); rigorous
pair ceiling = 17 (every component of A-minus-B contains a corner of A,
8 corners; so <= 8+8+1).

Usage: python3 subset_analysis.py
"""
import statistics
import time
from itertools import combinations

from scipy.spatial.transform import Rotation

from certify_six import rationalize, exact_count_config
from six_cube_search import random_mats


def main():
    win = rationalize(random_mats(12), 512)
    print('== k-subsets of the certified winner (seed 12, EXACT 595) ==',
          flush=True)
    win_max = {}
    for k in (2, 3, 4, 5):
        vals = []
        for idx in combinations(range(6), k):
            total, _ = exact_count_config([win[i] for i in idx],
                                          verbose=False)
            vals.append(total)
        win_max[k] = max(vals)
        print(f'k={k}: {len(vals)} subsets, counts min={min(vals)} '
              f'median={statistics.median(vals)} max={max(vals)}  '
              f'full list {sorted(vals)}', flush=True)

    print('== random-search baselines for max_k ==', flush=True)
    for k, n in ((2, 200), (3, 100), (4, 40), (5, 30)):
        best, vals = 0, []
        t0 = time.time()
        for s in range(n):
            mats = [m for m in
                    Rotation.random(k, random_state=10007 + 97 * s + k)
                    .as_matrix()]
            total, _ = exact_count_config(rationalize(mats, 512),
                                          verbose=False)
            vals.append(total)
            best = max(best, total)
        print(f'k={k}: n={n} random configs: max={best} '
              f'median={statistics.median(vals)} min={min(vals)}  '
              f'({time.time() - t0:.0f}s)', flush=True)
        print(f'      winner-subset max at k={k}: {win_max[k]}  '
              f'{"= " if win_max[k] == best else "< " if win_max[k] < best else "> "}'
              f'random-search max', flush=True)


if __name__ == '__main__':
    import sys as _sys
    if len(_sys.argv) > 1 and _sys.argv[1] in ('-h', '--help'):
        print(__doc__ or __file__); raise SystemExit(0)
    main()
