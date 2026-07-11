#!/usr/bin/env python3
# Working principles: SLIDE3_SPEC_V2.md + slide3_report.md. Project index: README.md
"""SLIDE3_SPEC.md Section 1, Phase P1: coarse (theta1, theta2, R) map.

Runs the full grid in parallel (<=4 worker processes, each its own
`cube_regions --quats-stdin` subprocess on a disjoint chunk), logs every
eval to slide3_search.jsonl (phase='P1'), and prints the top 30 by total.
"""
import json
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor

from slide3_search import (farey, r_candidates, overlay_quats, fits_cap,
                            LOG_PATH, ENGINE)

NWORKERS = 4


def _run_chunk(lines):
    """lines: list of (meta, quats). Returns list of dict records (dropping
    configs that violate the component cap or the engine flags as a
    degenerate 'error' arrangement -- both are logged separately by the
    caller, not silently dropped)."""
    ok = [(m, q) for m, q in lines if fits_cap(q)]
    skipped_cap = [(m, q) for m, q in lines if not fits_cap(q)]
    if not ok:
        return [], skipped_cap, []
    inp = '\n'.join(';'.join(','.join(map(str, g)) for g in q)
                     for _, q in ok) + '\n'
    proc = subprocess.run([ENGINE, '--quats-stdin'], input=inp,
                           capture_output=True, text=True)
    out_lines = proc.stdout.strip().split('\n') if proc.stdout.strip() else []
    assert len(out_lines) == len(ok), \
        f'{len(out_lines)} outputs for {len(ok)} inputs'
    records, errors = [], []
    for (meta, quats), line in zip(ok, out_lines):
        rec = json.loads(line)
        if 'error' in rec:
            errors.append((meta, quats, rec['error']))
            continue
        out = dict(meta)
        out['quats'] = rec['quats']
        out['total'] = rec['bounded']
        out['by_depth'] = {int(k): v for k, v in rec['by_depth'].items()}
        records.append(out)
    return records, skipped_cap, errors


def chunk(lst, n):
    k = (len(lst) + n - 1) // n
    return [lst[i:i + k] for i in range(0, len(lst), k)]


def main():
    theta_grid = farey(8)          # (p, q) pairs, tan(theta/2) = p/q
    r_grid = r_candidates()
    print(f'theta grid: {len(theta_grid)}  R candidates: {len(r_grid)}  '
          f'-> {len(theta_grid) ** 2 * len(r_grid)} configs')

    jobs = []
    for p1, q1 in theta_grid:
        for p2, q2 in theta_grid:
            for tag, R in r_grid:
                meta = {'phase': 'P1', 'q1': q1, 'p1': p1, 'q2': q2,
                        'p2': p2, 'R': list(R), 'Rtag': tag}
                quats = overlay_quats(q1, p1, q2, p2, R)
                jobs.append((meta, quats))
    print(f'built {len(jobs)} job configs')

    chunks = chunk(jobs, NWORKERS)
    t0 = time.time()
    all_records = []
    n_errors = 0
    n_skipped = 0
    with ProcessPoolExecutor(max_workers=NWORKERS) as ex:
        for records, skipped, errors in ex.map(_run_chunk, chunks):
            all_records.extend(records)
            n_errors += len(errors)
            n_skipped += len(skipped)
            if errors:
                with open(LOG_PATH, 'a') as f:
                    for meta, quats, msg in errors:
                        rec = dict(meta)
                        rec['quats'] = quats
                        rec['error'] = msg
                        f.write(json.dumps(rec) + '\n')
    dt = time.time() - t0
    print(f'P1 done: {len(all_records)} evals, {n_errors} degenerate errors, '
          f'{n_skipped} skipped (cap) in {dt:.1f}s '
          f'({dt / max(1, len(jobs)) * 1000:.1f} ms/eval)')

    with open(LOG_PATH, 'a') as f:
        for rec in all_records:
            f.write(json.dumps(rec) + '\n')

    all_records.sort(key=lambda r: -r['total'])
    print('\ntop 30 by total:')
    for r in all_records[:30]:
        print(f"  total={r['total']:4d}  q1={r['q1']:3d} p1={r['p1']:3d}  "
              f"q2={r['q2']:3d} p2={r['p2']:3d}  R={r['R']} ({r['Rtag']})  "
              f"by_depth={r['by_depth']}")

    with open('/Users/dmi/carroll/slide3_p1_top.json', 'w') as f:
        json.dump(all_records[:200], f)
    print('\nsaved top 200 to slide3_p1_top.json')


if __name__ == '__main__':
    import sys as _sys
    if len(_sys.argv) > 1 and _sys.argv[1] in ('-h', '--help'):
        print(__doc__ or __file__); raise SystemExit(0)
    main()
