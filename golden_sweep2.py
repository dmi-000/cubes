#!/usr/bin/env python3
# Working principles: golden_wall_report.md + QFIELD_SPEC.md. Project index: README.md
"""Final exploration phase (same log/wrappers as golden_six.py).

1. Off-axis neighbor scans around three MORE representatives of the
   681 on-axis plateau ((20,1,1,1), (5,2,2,2), (4,3,3,3)) -- the earlier
   hillclimb only scanned around (2,1,1,1); different plateau points expose
   different off-axis perturbation directions after gcd reduction.
2. Greedy hillclimb (same move set) from family B's x-axis peak (8,3,0,0)
   = 679, plus a finer B x-axis sweep around theta ~ 41 deg.
"""
import time
from multiprocessing import Pool

from golden_six import (load_done, log_line, _worker, neighbors, hillclimb)

FINE_X_B = [(11, 4, 0, 0), (13, 5, 0, 0), (19, 7, 0, 0), (21, 8, 0, 0),
            (23, 8, 0, 0), (17, 6, 0, 0), (15, 6, 0, 0), (25, 9, 0, 0)]


def main():
    done = load_done()
    best = {'total': 0, 'family': None, 'quat': None, 'bd': None}
    for (fam, q), (t, bd) in done.items():
        if t > best['total']:
            best.update(total=t, family=fam, quat=q, bd=bd)
    print(f'{len(done)} cached; best {best["family"]} {best["quat"]} '
          f'{best["total"]}')

    with Pool(8) as pool:
        # off-axis neighbors of three more 681 plateau points
        jobs = []
        for rep in [(20, 1, 1, 1), (5, 2, 2, 2), (4, 3, 3, 3)]:
            for q in neighbors(rep):
                if ('A', q) not in done:
                    jobs.append(('A', q))
        jobs = sorted(set(jobs))
        print(f'neighbor scan: {len(jobs)} fresh evals')
        t0 = time.time()
        for family, quat, total, bd, dt in pool.imap_unordered(_worker, jobs):
            log_line(family, quat, total, bd)
            done[(family, quat)] = (total, bd)
            mark = '  <-- ABOVE 681' if total > 681 else ''
            if total > best['total']:
                best.update(total=total, family=family, quat=quat, bd=bd)
            print(f'  [A] {quat} total={total} ({dt:.1f}s){mark}', flush=True)
        print(f'neighbor scan done in {time.time() - t0:.0f}s')

        # fine B x-axis sweep near 41 deg
        jobs = [('B', q) for q in FINE_X_B if ('B', q) not in done]
        print(f'fine B x-sweep: {len(jobs)} fresh evals')
        for family, quat, total, bd, dt in pool.imap_unordered(_worker, jobs):
            log_line(family, quat, total, bd)
            done[(family, quat)] = (total, bd)
            if total > best['total']:
                best.update(total=total, family=family, quat=quat, bd=bd)
            print(f'  [B] {quat} total={total} ({dt:.1f}s)', flush=True)

        # hillclimb from B (8,3,0,0)
        hillclimb('B', (8, 3, 0, 0), pool, best, done, max_steps=5)

    print(f'FINAL best: {best["family"]} {best["quat"]} {best["total"]} '
          f'{best["bd"]}')


if __name__ == '__main__':
    import sys as _sys
    if len(_sys.argv) > 1 and _sys.argv[1] in ('-h', '--help'):
        print(__doc__ or __file__); raise SystemExit(0)
    main()
