#!/usr/bin/env python3
"""Flexible parallel overlay sweep driver for the (1,1,1)-3-fold wall.
Reuses slide3_search infra. 4 workers max. Logs to slide3_search.jsonl.
Usage: import and call run(jobs, phase) where jobs is list of (meta, (q1,p1,q2,p2,R)).
"""
import sys, os, json, time, math
sys.path.insert(0, '/Users/dmi/carroll')
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp
from slide3_search import overlay_quats, fits_cap, gcd_reduce, farey, theta_deg, LOG_PATH, ENGINE
import subprocess

MPCTX = mp.get_context('fork')

NWORKERS = 4


def _run_chunk(args):
    jobs = args  # list of (meta, params) params=(q1,p1,q2,p2,R)
    ok = []
    for meta, params in jobs:
        q1, p1, q2, p2, R = params
        quats = overlay_quats(q1, p1, q2, p2, R)
        if fits_cap(quats):
            ok.append((meta, quats))
    if not ok:
        return [], 0
    inp = '\n'.join(';'.join(','.join(map(str, g)) for g in q) for _, q in ok) + '\n'
    proc = subprocess.run([ENGINE, '--quats-stdin'], input=inp, capture_output=True, text=True)
    out_lines = proc.stdout.strip().split('\n') if proc.stdout.strip() else []
    assert len(out_lines) == len(ok), f'{len(out_lines)} vs {len(ok)}'
    recs = []
    for (meta, quats), line in zip(ok, out_lines):
        rec = json.loads(line)
        if 'error' in rec:
            continue
        out = dict(meta)
        out['quats'] = rec['quats']
        out['total'] = rec['bounded']
        out['by_depth'] = {int(k): v for k, v in rec['by_depth'].items()}
        recs.append(out)
    return recs, len(ok)


def chunkify(lst, nchunks):
    k = (len(lst) + nchunks - 1) // nchunks
    return [lst[i:i+k] for i in range(0, len(lst), k)]


def run(jobs, phase, chunk_mult=6):
    # tag meta with phase
    for meta, _ in jobs:
        meta['phase'] = phase
    chunks = chunkify(jobs, NWORKERS * chunk_mult)
    t0 = time.time()
    all_recs = []
    n_eval = 0
    with ProcessPoolExecutor(max_workers=NWORKERS, mp_context=MPCTX) as ex:
        for recs, ne in ex.map(_run_chunk, chunks):
            all_recs.extend(recs)
            n_eval += ne
    dt = time.time() - t0
    with open(LOG_PATH, 'a') as f:
        for r in all_recs:
            f.write(json.dumps(r) + '\n')
    best = max((r['total'] for r in all_recs), default=0)
    over = [r for r in all_recs if r['total'] > 699]
    print(f'[{phase}] {n_eval} evals in {dt:.1f}s ({dt/max(n_eval,1)*1000:.1f}ms/eval); '
          f'max={best}; configs jobs={len(jobs)}; >699: {len(over)}')
    if over:
        for r in over:
            print('  !!! >699:', json.dumps(r))
    return all_recs, over
