#!/usr/bin/env python3
# Working principles: golden_wall_report.md + QFIELD_SPEC.md. Project index: README.md
"""Targeted follow-up sweep for golden_six.py (same log, same wrappers).

Motivation (from the first search phase, golden_search.jsonl): the best
total 681 occurs exactly at the four sqrt3-convergent quaternions
(2,1,1,1), (7,4,4,4), (12,7,7,7), (26,15,15,15) -- all rotations about
(1,1,1), angles 81.9..90.6 deg. (1,1,1) is a 3-fold axis of the golden
compound AND of golden cube 1, so the configuration is periodic in the
angle mod 120 deg, and the effective fundamental domain is (0, 60].
81.9 deg = -38.1 = 38.1 deg equivalent. This script sweeps the angle about
(1,1,1) systematically (family A), sweeps the rational 2-fold axis (1,0,0)
(90-deg periodic by cube symmetry), and repeats both sweeps in family B
(anchored on G2, where the same quaternions are genuinely different
configurations). Everything is appended to golden_search.jsonl.
"""
import json
import time
from multiprocessing import Pool

from golden_six import (LOG_PATH, load_done, log_line, _worker)

# (a,b,b,b) = rotation about (1,1,1) by theta = 2*atan(sqrt3*b/a);
# swept thetas cover ~8..120 deg (equivalently the fundamental (0,60])
DIAG = [(20, 1, 1, 1), (10, 1, 1, 1), (7, 1, 1, 1), (6, 1, 1, 1),
        (13, 2, 2, 2), (5, 1, 1, 1), (9, 2, 2, 2), (4, 1, 1, 1),
        (11, 3, 3, 3), (10, 3, 3, 3), (7, 2, 2, 2), (17, 5, 5, 5),
        (3, 1, 1, 1), (8, 3, 3, 3), (5, 2, 2, 2), (3, 2, 2, 2),
        (4, 3, 3, 3), (5, 4, 4, 4), (5, 3, 3, 3), (7, 5, 5, 5),
        (9, 7, 7, 7), (8, 5, 5, 5), (11, 7, 7, 7), (7, 6, 6, 6),
        (7, 3, 3, 3), (9, 4, 4, 4), (11, 4, 4, 4), (13, 7, 7, 7),
        (9, 5, 5, 5), (11, 6, 6, 6)]
# (a,b,0,0) = rotation about the x-axis (a RATIONAL 2-fold axis of the
# golden compound) by 2*atan(b/a)
XAXIS = [(3, 1, 0, 0), (2, 1, 0, 0), (5, 2, 0, 0), (4, 1, 0, 0),
         (5, 1, 0, 0), (7, 2, 0, 0), (5, 3, 0, 0), (7, 3, 0, 0),
         (8, 3, 0, 0), (9, 2, 0, 0)]


def main():
    done = load_done()
    print(f'{len(done)} cached evals')
    best = max(done.items(), key=lambda kv: kv[1][0])
    print(f'best so far: {best[0]} -> {best[1][0]}')
    jobs = []
    for q in DIAG + XAXIS:
        for fam in ('A', 'B'):
            if (fam, q) not in done:
                jobs.append((fam, q))
    print(f'{len(jobs)} fresh evals to run')
    t0 = time.time()
    with Pool(8) as pool:
        for family, quat, total, bd, dt in pool.imap_unordered(_worker, jobs):
            log_line(family, quat, total, bd)
            done[(family, quat)] = (total, bd)
            print(f'  [{family}] {quat}  total={total}  ({dt:.1f}s)',
                  flush=True)
    print(f'sweep done in {time.time() - t0:.0f}s')
    top = sorted(done.items(), key=lambda kv: -kv[1][0])[:8]
    for (fam, q), (total, bd) in top:
        print(f'TOP {fam} {q} {total} {dict(sorted(bd.items()))}')


if __name__ == '__main__':
    import sys as _sys
    if len(_sys.argv) > 1 and _sys.argv[1] in ('-h', '--help'):
        print(__doc__ or __file__); raise SystemExit(0)
    main()
