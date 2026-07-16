#!/usr/bin/env python3
# Working principles: NFAMILY_SPEC.md. Project index: README.md
"""Sweep driver for the n-cube BIG/DIHEDRAL FAMILY (NFAMILY_SPEC.md).

Generates exact-integer-quaternion family configs at n in {4,5,6} in three
tiers -- (a) chain phases theta_k = k*a, (b) independent random Pythagorean
phase tuples, (c) neighborhood refinement around top scorers -- and counts
each with the fast C++ engine (./cube_regions_n --quats-stdin, batched per
n to avoid per-config subprocess overhead). Every result is appended to
nfamily_results.jsonl as {n, kind, psi_pqr, thetas (pqr list or 'chain:a'),
quats, total, by_depth}.

<=4 worker processes (multiprocessing.Pool), matching NFAMILY_SPEC.md's
core budget. Designed to run detached:
    nohup python3 nfamily_sweep.py --n 4 5 6 --random 2500 --workers 4 \\
        > nfamily_sweep.out 2>&1 &
"""
import argparse
import itertools
import json
import multiprocessing as mp
import random
import subprocess
import sys
import time

from nfamily_common import (PyAngle, IDENTITY_ANGLE, build_family_quats,
                             PQR_MENU, SMALL_PQR)

RESULTS_PATH = '/Users/dmi/carroll/nfamily_results.jsonl'
ENGINE = './cube_regions_n'

CAP_SUM = {4: 195, 5: 429, 6: 801}
RECORDS = {4: 183, 5: 393, 6: 723}


def menu_angles(pqr_list):
    seen = {}
    for p, q, r in pqr_list:
        a = PyAngle.from_pqr(p, q, r)
        seen[(a.c, a.s)] = a
    out = list(seen.values())
    out.sort(key=lambda a: a.deg())
    return out


FULL_MENU = menu_angles(PQR_MENU)      # 33 points spanning (0,90), coarser
SMALL_MENU = menu_angles(SMALL_PQR)    # 33 points, chosen for small chain denominators


def gen_chain_configs(n, cap=512):
    """All (a, psi) in SMALL_MENU x SMALL_MENU whose chain theta_k=k*a
    (k=0..n-1) fits the quaternion cap. Returns list of dicts."""
    out = []
    for a in SMALL_MENU:
        if a.s == 0:
            continue  # a=0 gives a degenerate (repeated) compound
        thetas_pow = [a.pow(k) for k in range(n)]
        for psi in SMALL_MENU:
            try:
                quats, _ = build_family_quats(psi, thetas_pow, cap=cap)
            except ValueError:
                continue
            out.append({'n': n, 'kind': 'chain', 'a_deg': round(a.deg(), 4),
                         'psi_deg': round(psi.deg(), 4), 'quats': quats})
    return out


def gen_random_configs(n, count, rng, cap=512):
    out = []
    tries = 0
    while len(out) < count and tries < count * 6:
        tries += 1
        psi = rng.choice(FULL_MENU)
        thetas = [IDENTITY_ANGLE] + [rng.choice(FULL_MENU) for _ in range(n - 1)]
        try:
            quats, _ = build_family_quats(psi, thetas, cap=cap)
        except ValueError:
            continue
        out.append({'n': n, 'kind': 'random', 'psi_deg': round(psi.deg(), 4),
                     'theta_deg': [round(t.deg(), 4) for t in thetas],
                     'quats': quats})
    return out


def gen_neighbor_configs(n, base_cfg, rng, cap=512, radius=1):
    """Perturb ONE coordinate (one theta_k, or psi) of base_cfg to an
    adjacent menu angle (by index in FULL_MENU), for local hill-climbing
    around a high scorer."""
    out = []
    psi0 = PyAngle.from_pqr(*_pqr_of_deg(base_cfg['psi_deg']))
    idx_psi = _menu_index(psi0)
    thetas0 = [PyAngle.from_pqr(*_pqr_of_deg(d)) if d != 0.0 else IDENTITY_ANGLE
               for d in base_cfg.get('theta_deg', [0.0] * n)]
    if 'theta_deg' not in base_cfg:
        return out
    for coord in range(len(thetas0)):
        for d in (-radius, radius):
            if coord == 0:
                continue  # theta_1 pinned at 0 by gauge
            idx_t = _menu_index(thetas0[coord])
            j = idx_t + d
            if not (0 <= j < len(FULL_MENU)):
                continue
            new_thetas = list(thetas0)
            new_thetas[coord] = FULL_MENU[j]
            try:
                quats, _ = build_family_quats(psi0, new_thetas, cap=cap)
            except ValueError:
                continue
            out.append({'n': n, 'kind': 'neighbor', 'psi_deg': round(psi0.deg(), 4),
                         'theta_deg': [round(t.deg(), 4) for t in new_thetas],
                         'quats': quats})
    for d in (-radius, radius):
        j = idx_psi + d
        if not (0 <= j < len(FULL_MENU)):
            continue
        new_psi = FULL_MENU[j]
        try:
            quats, _ = build_family_quats(new_psi, thetas0, cap=cap)
        except ValueError:
            continue
        out.append({'n': n, 'kind': 'neighbor', 'psi_deg': round(new_psi.deg(), 4),
                     'theta_deg': [round(t.deg(), 4) for t in thetas0],
                     'quats': quats})
    return out


_MENU_DEG = [a.deg() for a in FULL_MENU]


def _menu_index(angle):
    d = angle.deg()
    best_i, best_diff = 0, 1e9
    for i, md in enumerate(_MENU_DEG):
        diff = abs(md - d)
        if diff < best_diff:
            best_diff, best_i = diff, i
    return best_i


_DEG_TO_PQR = {}
for p, q, r in PQR_MENU:
    a = PyAngle.from_pqr(p, q, r)
    _DEG_TO_PQR[round(a.deg(), 4)] = (p, q, r)


def _pqr_of_deg(d):
    if d in _DEG_TO_PQR:
        return _DEG_TO_PQR[d]
    best = min(_DEG_TO_PQR, key=lambda k: abs(k - d))
    return _DEG_TO_PQR[best]


def run_batch(n, configs):
    """Run a batch of same-n configs through the C++ engine via
    --quats-stdin (one process call, avoids per-config subprocess
    overhead). Returns list of (config, engine_result_dict)."""
    if not configs:
        return []
    lines = [';'.join(','.join(str(c) for c in q) for q in cfg['quats'])
             for cfg in configs]
    proc = subprocess.run([ENGINE, '--n', str(n), '--quats-stdin'],
                           input='\n'.join(lines) + '\n',
                           capture_output=True, text=True, check=True)
    out = []
    for cfg, line in zip(configs, proc.stdout.strip().splitlines()):
        r = json.loads(line)
        if 'error' in r:
            continue
        depth = {int(k): v for k, v in r['by_depth'].items() if int(k) != 0}
        out.append((cfg, r['bounded'], depth))
    return out


def worker(args):
    n, configs = args
    return n, run_batch(n, configs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, nargs='+', default=[4, 5, 6])
    ap.add_argument('--random', type=int, default=2000, help='random configs per n')
    ap.add_argument('--workers', type=int, default=4)
    ap.add_argument('--seed', type=int, default=12345)
    ap.add_argument('--out', default=RESULTS_PATH)
    ap.add_argument('--neighbor-rounds', type=int, default=2)
    args = ap.parse_args()

    rng = random.Random(args.seed)
    t_start = time.time()

    fh = open(args.out, 'a')
    best = {n: (0, None) for n in args.n}

    def log_and_track(n, cfg, total, depth):
        rec = dict(cfg)
        rec['total'] = total
        rec['by_depth'] = depth
        fh.write(json.dumps(rec) + '\n')
        fh.flush()
        if total > best[n][0]:
            best[n] = (total, cfg)

    # ---- tier 1: chains ----
    print(f'[{time.time()-t_start:.0f}s] generating chain configs...', flush=True)
    all_batches = []
    for n in args.n:
        chains = gen_chain_configs(n)
        print(f'  n={n}: {len(chains)} chain configs', flush=True)
        all_batches.append((n, chains))

    with mp.Pool(args.workers) as pool:
        for n, results in pool.imap_unordered(worker, all_batches):
            for cfg, total, depth in results:
                log_and_track(n, cfg, total, depth)
            print(f'[{time.time()-t_start:.0f}s] n={n} chains done, '
                  f'best so far={best[n][0]} (record {RECORDS.get(n)})', flush=True)

    # ---- tier 2: random Pythagorean phase tuples ----
    print(f'[{time.time()-t_start:.0f}s] generating random configs...', flush=True)
    all_batches = []
    for n in args.n:
        rc = gen_random_configs(n, args.random, rng)
        print(f'  n={n}: {len(rc)} random configs', flush=True)
        all_batches.append((n, rc))

    with mp.Pool(args.workers) as pool:
        for n, results in pool.imap_unordered(worker, all_batches):
            for cfg, total, depth in results:
                log_and_track(n, cfg, total, depth)
            print(f'[{time.time()-t_start:.0f}s] n={n} random done, '
                  f'best so far={best[n][0]} (record {RECORDS.get(n)})', flush=True)

    # ---- tier 3: neighborhood refinement around current bests ----
    for round_i in range(args.neighbor_rounds):
        print(f'[{time.time()-t_start:.0f}s] neighbor round {round_i+1}...', flush=True)
        all_batches = []
        for n in args.n:
            _, cfg = best[n]
            if cfg is None or 'theta_deg' not in cfg:
                all_batches.append((n, []))
                continue
            nb = gen_neighbor_configs(n, cfg, rng)
            all_batches.append((n, nb))
        with mp.Pool(args.workers) as pool:
            for n, results in pool.imap_unordered(worker, all_batches):
                for cfg, total, depth in results:
                    log_and_track(n, cfg, total, depth)
                print(f'[{time.time()-t_start:.0f}s] n={n} neighbor round {round_i+1} done, '
                      f'best so far={best[n][0]}', flush=True)

    fh.close()
    print(f'[{time.time()-t_start:.0f}s] DONE. Best per n:', flush=True)
    for n in args.n:
        total, cfg = best[n]
        print(f'  n={n}: best={total}  record={RECORDS.get(n)}  cap_sum={CAP_SUM.get(n)}  cfg={cfg}', flush=True)


if __name__ == '__main__':
    main()
