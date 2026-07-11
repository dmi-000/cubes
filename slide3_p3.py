#!/usr/bin/env python3
# Working principles: SLIDE3_SPEC_V2.md + slide3_report.md. Project index: README.md
"""SLIDE3_SPEC.md Section 1, Phase P3: constraint-first fine map of the
(1,1,1)-diagonal alignment wall.

Constraint imposed exactly: R = rotation about (1,1,1) by angle alpha,
quat (a, b, b, b) (rational alpha-halves: tan(alpha/2) = b*sqrt(3)/a stays
irrational but the QUAT is rational -- the axis is exact, the angle sweeps).
By the B-invariance of C(theta) (X(theta1,theta2,R) = X(theta1,theta2,R.B),
verified exactly in the R-sweep probe: the whole profile is 120-degree
periodic), the fundamental domain is alpha in (0, 120deg), i.e. b/a in
(0, 1]; b/a = 1 is alpha = 120deg = identity-equivalent (coincident-triple
value). R and R^-1 are covered by swapping theta1/theta2, and the full
(theta1, theta2) square is scanned, so signs are not needed.

Grid: theta over Farey(12) interior (tan(theta/2) = p/q), alpha over
Farey(7) fractions b/a in (0,1).
"""
import json
import subprocess
import time
from concurrent.futures import ProcessPoolExecutor

from slide3_search import farey, overlay_quats, fits_cap, LOG_PATH, ENGINE

NWORKERS = 4


def _run_chunk(lines):
    ok = [(m, q) for m, q in lines if fits_cap(q)]
    skipped = len(lines) - len(ok)
    if not ok:
        return [], skipped, 0
    inp = '\n'.join(';'.join(','.join(map(str, g)) for g in q)
                     for _, q in ok) + '\n'
    proc = subprocess.run([ENGINE, '--quats-stdin'], input=inp,
                           capture_output=True, text=True)
    out_lines = proc.stdout.strip().split('\n') if proc.stdout.strip() else []
    assert len(out_lines) == len(ok)
    records = []
    n_err = 0
    for (meta, quats), line in zip(ok, out_lines):
        rec = json.loads(line)
        if 'error' in rec:
            out = dict(meta)
            out['error'] = rec['error']
            records.append(out)
            n_err += 1
            continue
        out = dict(meta)
        out['quats'] = rec['quats']
        out['total'] = rec['bounded']
        out['by_depth'] = {int(k): v for k, v in rec['by_depth'].items()}
        records.append(out)
    return records, skipped, n_err


def chunk(lst, n):
    k = (len(lst) + n - 1) // n
    return [lst[i:i + k] for i in range(0, len(lst), k)]


def main():
    theta_grid = farey(12)
    alpha_grid = farey(7)      # (b, a) with 0 < b/a < 1
    print(f'theta: {len(theta_grid)}  alpha: {len(alpha_grid)}  '
          f'-> {len(theta_grid) ** 2 * len(alpha_grid)} configs')

    jobs = []
    for p1, q1 in theta_grid:
        for p2, q2 in theta_grid:
            for b, a in alpha_grid:
                R = (a, b, b, b)
                meta = {'phase': 'P3', 'q1': q1, 'p1': p1, 'q2': q2,
                        'p2': p2, 'R': list(R)}
                jobs.append((meta, overlay_quats(q1, p1, q2, p2, R)))

    chunks = chunk(jobs, NWORKERS * 4)
    t0 = time.time()
    all_records = []
    n_skip = n_err = 0
    with ProcessPoolExecutor(max_workers=NWORKERS) as ex:
        for records, skipped, errs in ex.map(_run_chunk, chunks):
            all_records.extend(records)
            n_skip += skipped
            n_err += errs
    dt = time.time() - t0
    n_ok = sum(1 for r in all_records if 'error' not in r)
    print(f'P3 done: {n_ok} evals, {n_err} degenerate, {n_skip} cap-skips '
          f'in {dt:.1f}s')

    with open(LOG_PATH, 'a') as f:
        for rec in all_records:
            f.write(json.dumps(rec) + '\n')

    good = [r for r in all_records if 'error' not in r]
    good.sort(key=lambda r: -r['total'])
    print('\ntop 40:')
    for r in good[:40]:
        print(f"  total={r['total']:4d}  th1=({r['p1']}/{r['q1']}) "
              f"th2=({r['p2']}/{r['q2']})  R={r['R']}  bd={r['by_depth']}")
    with open('/Users/dmi/carroll/slide3_p3_top.json', 'w') as f:
        json.dump(good[:400], f)


if __name__ == '__main__':
    import sys as _sys
    if len(_sys.argv) > 1 and _sys.argv[1] in ('-h', '--help'):
        print(__doc__ or __file__); raise SystemExit(0)
    main()
