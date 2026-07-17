#!/usr/bin/env python3
# Working principles: RATTAN_SPEC.md. Project index: README.md
"""RATTAN phase 2 -- the targeted completion runs, per main-session
priorities after run 1:

P1. Complete the NEW n=5 387 config (393's exact 4-clique + 5th on-axis
    cube at the t5 plateau) with a 6th cube: (a) on-axis conic phases
    (full Farey-40), (b) off-axis random integer quats ||q||^2 <= 600
    (the architecture of 393's cube 0 and 723's cube 5). Also complete
    OTHER t5-plateau members -- same 5-cube count, possibly different
    completion optima. Target: beat glue's 715; chase 723's -8.
P2. n=4 gap (clique alone = 179 = record-4): hill-climb all four clique
    phases jointly (Farey-40 neighborhood), and 3-subsets of the clique
    on-axis + 4th off-axis int quat (183's own architecture); extend the
    183-triple + 4th int-quat sweep with fresh seeds.
P3. n=5: joint perturbation of (clique t's, t5) around the 387.

Oracle throttling: ties at a record are oracle-verified for the first
ORACLE_CAP_PER_PROFILE hits of each (n, total, depth-profile) class;
later identical-profile ties are logged flagged-but-unverified (the
profile class is already established by then). Anything ABOVE a record
is always oracle-verified immediately.

Appends to rattan_results.jsonl (tag phase2-*), flags to
rattan_flagged.jsonl, interim text to rattan_report.md.
"""
import argparse
import itertools
import json
import math
import multiprocessing as mp
import random
import subprocess
import sys
import time
from fractions import Fraction as Fr

from rattan_sweep import (
    ConicAngle, build_family_quats_conic, rel_matrix_conic,
    gen_int_quat_extension, run_batch, worker, shard_batches,
    farey_t_values, T_MENU_FULL, RECORDS, RECORD_QUATS, RECORD_DEPTH,
    RESULTS_PATH, REPORT_PATH, CAP, append_report, run_cpp,
)
from nfamily_common import is_rotation_exact, matrix_to_int_quat, mat_mul
from nfamily_common import quat_to_matrix_exact
from golden_rotations import rot_from_quat
from certify_six import exact_count_config

FLAG_PATH = '/Users/dmi/carroll/rattan_flagged.jsonl'
ORACLE_CAP_PER_PROFILE = 2

CLIQUE_T = [Fr(0), Fr(-5, 6), Fr(3, 4), Fr(-1, 5)]  # G1's exact t-values
PQD = (3, -2, 13)


def clique_thetas(ts):
    p, q, d = PQD
    return [ConicAngle.from_t(t, d) for t in ts]


def build_from_ts(ts, cap=CAP):
    p, q, d = PQD
    quats, _ = build_family_quats_conic(p, q, d, clique_thetas(ts), cap=cap)
    return quats


# ---- record protocol with per-profile oracle throttling ------------------

_oracle_seen = {}


def check_record_v2(n, total, quats, depth):
    record = RECORDS.get(n)
    if record is None or total < record:
        return
    prof = tuple(depth.get(k, depth.get(str(k), 0)) for k in range(1, n + 1))
    key = (n, total, prof)
    cnt = _oracle_seen.get(key, 0)
    _oracle_seen[key] = cnt + 1
    verify = (total > record) or (cnt < ORACLE_CAP_PER_PROFILE)
    entry = {'n': n, 'total': total, 'record': record, 'quats': [list(q) for q in quats],
             'depth_profile': list(prof), 'oracle_run': verify}
    if verify:
        rots = [rot_from_quat(*q) for q in quats]
        py_total, py_depth = exact_count_config(rots, verbose=False)
        entry['oracle_total'] = py_total
        entry['oracle_confirmed'] = (py_total == total)
        msg = (f'*** RECORD-CLASS n={n} total={total} (record={record}) profile={prof} '
               f'oracle={py_total} confirmed={entry["oracle_confirmed"]} quats={quats} ***')
    else:
        msg = (f'*** RECORD-CLASS n={n} total={total} profile={prof} '
               f'(profile seen {cnt+1}x, oracle throttled) quats={quats} ***')
    print(msg, flush=True)
    with open(FLAG_PATH, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    if total > record:
        append_report(f'\n**>>> RECORD BEATEN: {msg} <<<**\n')


# ---- config generators ---------------------------------------------------

def p1_configs(rng, big_budget=20000, plateau_budget=2000):
    """Priority 1: n=6 completions of the 387."""
    p, q, d = PQD
    out = []

    # find the t5 plateau exactly: all Farey-40 t5 with 5-cube count 387
    plateau_lo, plateau_hi = Fr(8, 39), Fr(3, 14)
    plateau_cands = [t for t in T_MENU_FULL if plateau_lo <= t <= plateau_hi]
    five_cfgs = []
    for t5 in plateau_cands:
        try:
            quats = build_from_ts(CLIQUE_T + [t5])
        except ValueError:
            continue
        five_cfgs.append({'n': 5, 'kind': 'p1-387-plateau-check', 't5': str(t5),
                           'quats': quats})
    results = run_batch(5, five_cfgs)
    plateau = []
    for cfg, total, depth in results:
        if total == 387:
            plateau.append(Fr(cfg['t5']))
    print(f'[p1] t5 plateau members at 387 (of {len(plateau_cands)} candidates): '
          f'{[str(t) for t in plateau]}', flush=True)
    append_report(f'### P1: exact t5 plateau at 387: {[str(t) for t in plateau]} '
                   f'(checked all Farey-40 in [8/39, 3/14])\n\n')
    if not plateau:
        plateau = [Fr(3, 14)]
    primary = Fr(3, 14) if Fr(3, 14) in plateau else plateau[0]

    for t5 in plateau:
        base = build_from_ts(CLIQUE_T + [t5])
        budget = big_budget if t5 == primary else plateau_budget
        # (a) 6th on-axis
        t6_menu = T_MENU_FULL if t5 == primary else farey_t_values(12)
        for t6 in t6_menu:
            if t6 in (list(CLIQUE_T) + [t5]):
                continue
            try:
                quats = build_from_ts(CLIQUE_T + [t5, t6])
            except ValueError:
                continue
            out.append({'n': 6, 'kind': 'p1-387+6th-onaxis', 't5': str(t5),
                         't6': str(t6), 'quats': quats})
        # (b) 6th off-axis int quat
        for ql in gen_int_quat_extension(base, budget, rng):
            out.append({'n': 6, 'kind': 'p1-387+6th-intquat', 't5': str(t5),
                         'quats': ql})
    return out


def p2_configs(rng, hillclimb_budget=4000, subset_budget=5000, triple_budget=10000):
    """Priority 2: the n=4 -4 gap."""
    p, q, d = PQD
    out = []
    menu = T_MENU_FULL

    # (a) joint random perturbation of the four clique t's (Farey-40),
    #     biased small moves: replace 1-3 of the free phases with a menu
    #     value near the original (by value).
    sorted_menu = sorted(menu)

    def near(t, radius):
        # indices near t in sorted order
        import bisect
        i = bisect.bisect_left(sorted_menu, t)
        lo, hi = max(0, i - radius), min(len(sorted_menu), i + radius)
        return sorted_menu[lo:hi]

    base_ts = CLIQUE_T
    for _ in range(hillclimb_budget):
        ts = list(base_ts)
        k = rng.randint(1, 3)
        for coord in rng.sample([1, 2, 3], k):
            ts[coord] = rng.choice(near(ts[coord], 25))
        try:
            quats = build_from_ts(ts)
        except ValueError:
            continue
        out.append({'n': 4, 'kind': 'p2-clique-perturb',
                     't_list': [str(t) for t in ts], 'quats': quats})

    # (b) 3-subsets of the clique on-axis + 4th off-axis int quat
    for drop in range(4):
        ts3 = [t for i, t in enumerate(CLIQUE_T) if i != drop]
        try:
            base3 = build_from_ts(ts3)
        except ValueError:
            continue
        for ql in gen_int_quat_extension(base3, subset_budget, rng):
            out.append({'n': 4, 'kind': f'p2-3subset-drop{drop}+intquat', 'quats': ql})

    # (c) 183's triple + 4th int quat, fresh seeds (extends run 1's 4000)
    clique183 = [RECORD_QUATS[4][0], RECORD_QUATS[4][2], RECORD_QUATS[4][3]]
    for ql in gen_int_quat_extension(clique183, triple_budget, rng):
        out.append({'n': 4, 'kind': 'p2-183triple+intquat', 'quats': ql})
    return out


def p3_configs(rng, budget=4000):
    """Priority 3: joint perturbation around the 387 at n=5."""
    out = []
    sorted_menu = sorted(T_MENU_FULL)
    import bisect

    def near(t, radius):
        i = bisect.bisect_left(sorted_menu, t)
        lo, hi = max(0, i - radius), min(len(sorted_menu), i + radius)
        return sorted_menu[lo:hi]

    base_ts = CLIQUE_T + [Fr(3, 14)]
    for _ in range(budget):
        ts = list(base_ts)
        k = rng.randint(1, 2)
        for coord in rng.sample([1, 2, 3, 4], k):
            ts[coord] = rng.choice(near(ts[coord], 25))
        try:
            quats = build_from_ts(ts)
        except ValueError:
            continue
        out.append({'n': 5, 'kind': 'p3-387-perturb',
                     't_list': [str(t) for t in ts], 'quats': quats})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--workers', type=int, default=4)
    ap.add_argument('--seed', type=int, default=777001)
    ap.add_argument('--out', default=RESULTS_PATH)
    args = ap.parse_args()
    rng = random.Random(args.seed)
    t0 = time.time()

    def log(m):
        print(f'[{time.time()-t0:.0f}s] {m}', flush=True)

    append_report(f'\n## Phase 2 (targeted completions, seed {args.seed}) -- '
                   f'started {time.strftime("%Y-%m-%d %H:%M")}\n\n')

    log('generating configs...')
    cfgs = []
    cfgs += p1_configs(rng)
    log(f'P1: {sum(1 for c in cfgs)} configs so far')
    n_p1 = len(cfgs)
    cfgs += p2_configs(rng)
    log(f'P2: +{len(cfgs)-n_p1}')
    n_p2 = len(cfgs)
    cfgs += p3_configs(rng)
    log(f'P3: +{len(cfgs)-n_p2}; total {len(cfgs)}')

    by_n = {}
    for c in cfgs:
        by_n.setdefault(c['n'], []).append(c)
    shards = shard_batches([(n, cc) for n, cc in by_n.items()], chunk=300)
    log(f'{len(shards)} shards')

    best = {n: (0, None) for n in (4, 5, 6)}
    fh = open(args.out, 'a')
    done = 0
    with mp.Pool(args.workers) as pool:
        for n, results in pool.imap_unordered(worker, shards):
            for cfg, total, depth in results:
                rec = dict(cfg)
                rec['total'] = total
                rec['by_depth'] = depth
                rec['tag'] = 'phase2'
                fh.write(json.dumps(rec) + '\n')
                if total > best[n][0]:
                    best[n] = (total, cfg)
                check_record_v2(n, total, cfg['quats'], depth)
            fh.flush()
            done += 1
            if done % 10 == 0 or done == len(shards):
                log(f'shard {done}/{len(shards)}, best: ' +
                    ', '.join(f'n={m}:{best[m][0]}' for m in (4, 5, 6)))
            if done % 50 == 0:
                append_report(f'phase2 progress {done}/{len(shards)} shards, best: ' +
                               ', '.join(f'n={m}:{best[m][0]}' for m in (4, 5, 6)) + '\n')
    fh.close()

    summary = ['\n### Phase 2 final\n\n', '| n | best (phase 2) | record |\n',
               '|---|-----------------|--------|\n']
    for n in (4, 5, 6):
        total, cfg = best[n]
        summary.append(f'| {n} | {total} | {RECORDS[n]} |\n')
        log(f'n={n}: best={total} cfg={cfg}')
    append_report(''.join(summary))
    log('DONE')


if __name__ == '__main__':
    main()
