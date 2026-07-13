#!/usr/bin/env python3
# Working principles: PROJECT.md; six_cube_search_results.md Postscripts
# 16-21 (record tower, ceiling law, envelope bounds, blueprint program).
# REUSES verbatim: shared_axis_search.py's cluster/genome/climb machinery
# (sas.build_config, cpp_batch_n, genome_config2, climb, multi_restart,
# locked_genome, random_genome, AXES) and blueprint_enum.py's
# integer_partitions + to_spec (both already n-independent). Only the
# catalog ENUMERATION (hardcoded to 6 in blueprint_enum.py) is
# regeneralized here to N=7, and the n=6-specific record-climb code of
# n4_search.py's phaseD_deepclimb is reimplemented directly on raw quat
# lists (not genomes) since the 1207 record's 7th cube is NOT a
# shared-axis cluster member.
"""n7_program.py -- self-contained n=7 record-hunting + verification
campaign (see this repo's task brief). Five tasks, run in order by
main(), each appending to n7_program.jsonl and (at the very end) writing
n7_program_report.md. Designed to run detached (nohup) with NO external
monitor loop: it writes its own report when done.

Tasks:
  1. CLIMB the known n=7 record 1207 (723's six cubes + 7th [5,4,-4,-4],
     never hill-climbed before this): wide-perturbation multi-restart
     deep-climb (n4_search.py's phaseD_deepclimb technique, ported to
     n=7) + a dedicated "swap/reoptimize the 7th cube only" pass.
  2. BLUEPRINT SEARCH at n=7: enumerate cluster-skeleton blueprints for 7
     cubes (blueprint_enum.py's canonicalization generalized from N=6 to
     N=7), gate on reproducing 1207 from the onaxis3+spoke3+free1
     skeleton (723's exact structure + 1 free cube), then knob-search
     every surviving blueprint (shared_axis_search.py's climb/
     multi_restart, reused unmodified) prioritized toward
     onaxis+spoke-about-(1,1,1) shapes.
  3. CEILING VERIFICATION: scan all available n=7 by_depth data (this
     script's own log + prior campaign logs) for violations of
     depth-(7-l) <= C(l,7) = (12l-6)*7 - 2(l^2-1), report attained caps,
     and run a targeted hunt (climb maximizing depth-1 / depth-2
     directly) to try to raise the unattained l=6/l=5 caps.
  4. EXTENSION to n=8: best n=7 config + an 8th-cube search (symmetric +
     random candidates, then a short climb) -> first n=8 record; check
     against the n=8 ceiling predictions.
  5. ENVELOPE at n=7: for the top ~50 n=7 configs seen anywhere in this
     run, exact-count all seven 6-subsets and report max(T - S_max), and
     6-subset saturation of the n=6 deep caps 164/102/36.

Usage:
  python3 n7_program.py              # all tasks, production budgets
  python3 n7_program.py task1        # just task 1 (debugging)
  python3 n7_program.py task1 task2  # tasks 1 and 2 only
"""
import argparse
import json
import math
import os
import random
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import blueprint_enum as be
import shared_axis_search as sas
from certify_six import exact_count_config
from golden_rotations import rot_from_quat

LOG_PATH = os.path.join(HERE, 'n7_program.jsonl')
REPORT_PATH = os.path.join(HERE, 'n7_program_report.md')
MAXC = 512
WORKERS = 4                       # hard cap per task rules

N7 = 7
RECORD_N7 = 1207

CFG_723 = [[4, 1, 1, -1], [3, 3, 7, 3], [5, -1, -5, -5],
           [2, 1, 1, 1], [1, 1, 1, 1], [5, 2, 2, 2]]
CUBE7 = [5, 4, -4, -4]
CFG_1207 = [list(q) for q in CFG_723] + [list(CUBE7)]

# ceiling law: C(l, n) = (12l-6)*n - 2(l^2 - 1)
def ceiling(l, n):
    return (12 * l - 6) * n - 2 * (l * l - 1)

CEIL7 = {l: ceiling(l, 7) for l in range(1, 7)}       # l=1..6
CEIL8 = {l: ceiling(l, 8) for l in range(1, 8)}       # l=1..7
CEIL6 = {l: ceiling(l, 6) for l in range(1, 6)}       # l=1..5 (for envelope)

_LOGF = open(LOG_PATH, 'a')
_T0 = time.time()


def log(rec):
    rec = dict(rec)
    rec.setdefault('t', round(time.time() - _T0, 1))
    _LOGF.write(json.dumps(rec) + '\n')
    _LOGF.flush()


def say(msg):
    print(f'[{time.time()-_T0:8.1f}s] {msg}', flush=True)


# ============================================================ core utils
def canon_quats(quats):
    out = []
    for q in quats:
        q = sas.gcd_reduce(list(q))
        for c in q:
            if c != 0:
                if c < 0:
                    q = [-x for x in q]
                break
        out.append(tuple(q))
    return tuple(out)


def neighbors_all(quats, free_idx=None, deltas=(-2, -1, 1, 2), max_c=MAXC):
    idxs = range(len(quats)) if free_idx is None else list(free_idx)
    out = []
    for i in idxs:
        for j in range(4):
            for d in deltas:
                q = [list(x) for x in quats]
                q[i][j] += d
                if all(c == 0 for c in q[i]):
                    continue
                cq = canon_quats(q)
                if any(abs(c) > max_c for qq in cq for c in qq):
                    continue
                out.append([list(x) for x in cq])
    return out


CACHE = {}
STATS = {'evals': 0, 'cache_hits': 0}


def batch_eval(configs):
    """Memoized exact evaluation via cube_regions_n (sas.cpp_batch_n).
    Returns list of (total, by_depth) or None, aligned with `configs`."""
    keys = [canon_quats(c) for c in configs]
    order, uniq = [], {}
    for k in keys:
        if k not in CACHE and k not in uniq:
            uniq[k] = len(order)
            order.append(k)
        elif k in CACHE:
            STATS['cache_hits'] += 1
    if order:
        cfgs = [list(map(list, k)) for k in order]
        res = sas.cpp_batch_n(cfgs, workers=WORKERS)
        STATS['evals'] += len(cfgs)
        for k, r in zip(order, res):
            CACHE[k] = r
    return [CACHE[k] for k in keys]


def score_total(total, bd):
    return total


def climb(start, tag, task, max_iters=200, deltas=(-2, -1, 1, 2),
          free_idx=None, score_fn=score_total, log_every=True):
    cur = [list(q) for q in canon_quats(start)]
    r = batch_eval([cur])[0]
    if r is None:
        return None, None
    cur_score = score_fn(*r)
    cur_r = r
    it = 0
    while it < max_iters:
        it += 1
        nbrs = neighbors_all(cur, free_idx=free_idx, deltas=deltas)
        if not nbrs:
            break
        results = batch_eval(nbrs)
        best_i, best_score = -1, cur_score
        for i, rr in enumerate(results):
            if rr is not None and score_fn(*rr) > best_score:
                best_i, best_score = i, score_fn(*rr)
        if best_i < 0:
            break
        cur, cur_r = nbrs[best_i], results[best_i]
        cur_score = best_score
    if log_every:
        log({'task': task, 'stage': 'climb_end', 'tag': tag,
             'n': len(cur), 'quats': cur, 'total': cur_r[0], 'by_depth': cur_r[1]})
    return cur, cur_r


def wide_perturb(quats, rng, n_changes, perturb_deltas=(-4, -3, -2, -1, 1, 2, 3, 4),
                  max_c=MAXC):
    q = [list(x) for x in quats]
    for _ in range(n_changes):
        i = rng.randrange(len(q))
        j = rng.randrange(4)
        q[i][j] += rng.choice(perturb_deltas)
        if all(c == 0 for c in q[i]):
            q[i][j] += 1
    cq = canon_quats(q)
    if any(abs(c) > max_c for qq in cq for c in qq):
        return None
    return [list(x) for x in cq]


def verify_oracle(quats):
    rots = [rot_from_quat(*q) for q in quats]
    total, bd = exact_count_config(rots, verbose=False)
    bd_pos = {k: v for k, v in bd.items() if k != 0}
    return total, bd_pos


def symmetric_candidates():
    """Small set of hand-picked exact-rational special-angle quats, reused
    verbatim in spirit from n4_search.symmetric_quats / shared_axis_search.
    FREEB."""
    cands = [(1, 0, 0, 0)]
    for i in range(3):
        q90 = [1, 0, 0, 0]; q90[i + 1] = 1; cands.append(tuple(q90))
        qm90 = [1, 0, 0, 0]; qm90[i + 1] = -1; cands.append(tuple(qm90))
        q180 = [0, 0, 0, 0]; q180[i + 1] = 1; cands.append(tuple(q180))
    for s1, s2 in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        cands.append((1, 1, s1, s2))
        cands.append((3, 1, s1, s2))
    cands.extend(sas.FREEB)
    out, seen = [], set()
    for q in cands:
        q = tuple(sas.gcd_reduce(list(q)))
        if q not in seen:
            seen.add(q)
            out.append(q)
    return out


def random_quat(rng, maxc=MAXC // 4):
    while True:
        q = tuple(sas.gcd_reduce([rng.randint(-maxc, maxc) for _ in range(4)]))
        if any(q):
            return q


# ============================================================== RESULTS
RESULTS = {'record_n7': {'total': RECORD_N7, 'quats': CFG_1207, 'bd': None},
           'task1': None, 'task2': None, 'task3': None, 'task4': None,
           'task5': None}


def note_candidate_beat(total, quats, bd, source):
    """If total beats the current best n=7 record, verify with the oracle
    before accepting it as a new RESULTS['record_n7']."""
    if total <= RESULTS['record_n7']['total']:
        return False
    say(f'!!!! candidate {total} > {RESULTS["record_n7"]["total"]} from {source} -- verifying with oracle...')
    oracle_total, oracle_bd = verify_oracle(quats)
    verified = (oracle_total == total)
    log({'task': 'FLAG', 'FLAG': 'CANDIDATE N7 RECORD', 'source': source,
         'cpp_total': total, 'oracle_total': oracle_total, 'verified': verified,
         'quats': quats, 'by_depth': bd})
    say(f'     oracle={oracle_total} verified={verified}')
    if verified:
        RESULTS['record_n7'] = {'total': total, 'quats': quats, 'bd': bd, 'source': source}
        say(f'     NEW N7 RECORD ACCEPTED: {total}')
    return verified


# =============================================================== TASK 1
def task1_climb(n_restarts=32, seed=20260713):
    say('=== TASK 1: deep climb of 1207 ===')
    rng = random.Random(seed)
    result = {'base': None, 'restarts': [], 'swap7': None, 'best': None}

    # (a) base greedy climb to a +-1/+-2 local max
    cur, r = climb(CFG_1207, 'base', 'task1')
    if r is None:
        say('  base climb: 1207 itself degenerate?! aborting task1')
        return result
    result['base'] = {'total': r[0], 'quats': cur, 'bd': r[1]}
    say(f'  base climb: {r[0]} (start 1207)')
    note_candidate_beat(r[0], cur, r[1], 'task1_base_climb')

    # (b) radius-4 single-component certification
    nbrs4 = neighbors_all(cur, deltas=(-4, -3, -2, -1, 1, 2, 3, 4))
    r4 = batch_eval(nbrs4)
    best_total, best_quats, best_bd = r[0], cur, r[1]
    for i, rr in enumerate(r4):
        if rr is not None and rr[0] > best_total:
            best_total, best_quats, best_bd = rr[0], nbrs4[i], rr[1]
    say(f'  radius-4 cert: {"IMPROVED to " + str(best_total) if best_total > r[0] else "confirmed local max"}')
    note_candidate_beat(best_total, best_quats, best_bd, 'task1_radius4')

    # (c) wide-perturbation multi-restart deep-climb (5-12 simultaneous
    # component moves off the ORIGINAL 1207, per n4_search.py's phaseD
    # methodology -- escaping a radius-4 local max needs a multi-component
    # jump a single-component search can never make)
    overall_best = {'total': best_total, 'quats': best_quats, 'bd': best_bd}
    for rs in range(n_restarts):
        nmoves = rng.randrange(5, 13)
        pq = wide_perturb(CFG_1207, rng, nmoves)
        if pq is None:
            continue
        cur2, r2 = climb(pq, f'restart{rs}', 'task1', max_iters=120)
        if r2 is None:
            continue
        result['restarts'].append({'rs': rs, 'nmoves': nmoves, 'total': r2[0]})
        if r2[0] > overall_best['total']:
            overall_best = {'total': r2[0], 'quats': cur2, 'bd': r2[1]}
            say(f'  restart {rs} (nmoves={nmoves}): {r2[0]}  <-- NEW BEST')
            note_candidate_beat(r2[0], cur2, r2[1], f'task1_restart{rs}')
        elif rs % 8 == 0:
            say(f'  restart {rs} (nmoves={nmoves}): {r2[0]}')

    # (c2) a further round of restarts perturbing the CURRENT BEST, not just
    # the original seed -- explores the neighborhood of whatever basin we've
    # found so far, deeper than a single perturbation radius from 1207.
    for rs in range(n_restarts // 2):
        nmoves = rng.randrange(5, 13)
        pq = wide_perturb(overall_best['quats'], rng, nmoves)
        if pq is None:
            continue
        cur2, r2 = climb(pq, f'restart2_{rs}', 'task1', max_iters=120)
        if r2 is None:
            continue
        if r2[0] > overall_best['total']:
            overall_best = {'total': r2[0], 'quats': cur2, 'bd': r2[1]}
            say(f'  restart2 {rs} (nmoves={nmoves}): {r2[0]}  <-- NEW BEST')
            note_candidate_beat(r2[0], cur2, r2[1], f'task1_restart2_{rs}')

    # (d) dedicated 7th-cube swap/reoptimize: fix 723's six cubes, search
    # the seventh cube's orientation widely, then climb only that cube.
    say('  (d) 7th-cube swap/reoptimize pass')
    cand7 = list(symmetric_candidates())
    while len(cand7) < 300:
        cand7.append(random_quat(rng, maxc=200))
    configs7 = [CFG_723 + [list(c)] for c in cand7]
    res7 = batch_eval(configs7)
    best7_total, best7_i = -1, -1
    for i, rr in enumerate(res7):
        if rr is not None and rr[0] > best7_total:
            best7_total, best7_i = rr[0], i
    say(f'  7th-cube sweep ({len(configs7)} candidates): best={best7_total}')
    if best7_i >= 0:
        cur7, r7 = climb(configs7[best7_i], 'swap7', 'task1', free_idx=[6], max_iters=80)
        result['swap7'] = {'total': r7[0] if r7 else None}
        say(f'  7th-cube climb (free_idx=6 only): {r7[0] if r7 else None}')
        if r7 is not None and r7[0] > overall_best['total']:
            overall_best = {'total': r7[0], 'quats': cur7, 'bd': r7[1]}
            note_candidate_beat(r7[0], cur7, r7[1], 'task1_swap7')
        # then a full-config climb starting from the best swap7 result
        if r7 is not None:
            cur7b, r7b = climb(cur7, 'swap7_full', 'task1', max_iters=100)
            if r7b is not None and r7b[0] > overall_best['total']:
                overall_best = {'total': r7b[0], 'quats': cur7b, 'bd': r7b[1]}
                note_candidate_beat(r7b[0], cur7b, r7b[1], 'task1_swap7_full')

    result['best'] = overall_best
    say(f'TASK 1 best: {overall_best["total"]}  (record before task1: {RECORD_N7})')
    RESULTS['task1'] = result
    return result


# =============================================================== TASK 2
def canonical_blueprints_n(N):
    """blueprint_enum.py's canonical_blueprints, generalized from the
    hardcoded 6 to arbitrary N (P1a/P1b logic unchanged; be.integer_partitions
    is already N-parametric, reused verbatim)."""
    seen = []
    for a in [0] + list(range(2, N + 1)):
        r = N - a
        for part in be.integer_partitions(r):
            spoke_sizes = tuple(sorted((x for x in part if x >= 2), reverse=True))
            n_free = sum(1 for x in part if x == 1)
            key = (a, spoke_sizes, n_free)
            if key not in seen:
                seen.append(key)
    return seen


def blueprint_tag_n(a, spoke_sizes, n_free, axis_name, N):
    parts = []
    if a:
        parts.append(f'onaxis{a}')
    for s in spoke_sizes:
        parts.append(f'spoke{s}')
    if n_free:
        parts.append(f'free{n_free}')
    if not parts:
        parts.append(f'allfree{N}')
    body = '+'.join(parts)
    axis_short = {'(1,1,1)': '111', '(0,0,1)': '001', '(1,1,0)': '110'}
    if axis_name is None:
        return f'n{N}_{body}'
    return f'n{N}_{body}_ax{axis_short[axis_name]}'


def build_catalog_n(N):
    rows = []
    bp_id = 0
    for (a, spoke_sizes, n_free) in canonical_blueprints_n(N):
        axis_list = sas.AXES.keys() if (a or spoke_sizes) else [None]
        for axis_name in axis_list:
            bp_id += 1
            is_gate = (a == 3 and spoke_sizes == (3,) and n_free == 1
                       and axis_name == '(1,1,1)')
            rows.append(dict(
                id=bp_id, axis=axis_name, a=a, spoke_sizes=spoke_sizes,
                n_free=n_free, tag=blueprint_tag_n(a, spoke_sizes, n_free, axis_name, N),
                spec=be.to_spec(a, spoke_sizes, n_free),
                n=a + sum(spoke_sizes) + n_free, is_gate=is_gate,
            ))
    return rows


def priority_key(row):
    """Prioritize onaxis+spoke shapes about (1,1,1) resembling the n=6
    winners (per task brief). Gate first, then (1,1,1)-axis structured
    blueprints with more clusters (more like the record), then other axes,
    then the all-free control last."""
    gate_rank = 0 if row['is_gate'] else 1
    axis_rank = 0 if row['axis'] == '(1,1,1)' else (1 if row['axis'] else 2)
    has_onaxis = 0 if row['a'] else 1
    n_clusters = len(row['spoke_sizes']) + (1 if row['a'] else 0)
    cluster_rank = -n_clusters
    free_rank = row['n_free']
    return (gate_rank, axis_rank, has_onaxis, cluster_rank, free_rank)


BUDGET_DEFAULT7 = dict(n_random_free=2, steps_free=8, restarts_wide_free=2,
                        n_random_locked=1, steps_locked=4, restarts_wide_locked=0)
BUDGET_GATE7 = dict(n_random_free=6, steps_free=20, restarts_wide_free=4,
                     n_random_locked=2, steps_locked=12, restarts_wide_locked=2)

BP_RESULTS = {}


def sas_log_redirect(rec):
    rec = dict(rec)
    rec['task'] = 'task2'
    log(rec)


sas.log = sas_log_redirect  # redirect shared_axis_search's internal log()
                             # calls (used by climb/multi_restart) into OUR
                             # jsonl -- do NOT write to shared_axis_search.jsonl,
                             # which is owned by a different (possibly still
                             # running / already-finished) process.


def run_blueprint(tag, axis_name, spec, budget, start_genomes=(), rng=None):
    t0 = time.time()
    locked_starts = ([sas.locked_genome(axis_name, spec, rng)]
                      if budget['n_random_locked'] > 0 else [])
    locked = sas.multi_restart(spec, axis_name, budget['n_random_locked'], rng,
                                steps=budget['steps_locked'],
                                restarts_wide=budget['restarts_wide_locked'],
                                tag=tag, part='locked', start_genomes=locked_starts)
    free = sas.multi_restart(spec, axis_name, budget['n_random_free'], rng,
                              steps=budget['steps_free'],
                              restarts_wide=budget['restarts_wide_free'],
                              tag=tag, part='free', start_genomes=start_genomes)
    dt = time.time() - t0
    rec = dict(tag=tag, axis=axis_name, spec=spec,
               locked_best=locked['best_total'], free_best=free['best_total'],
               locked_genome=locked['best_genome'], free_genome=free['best_genome'],
               free_bd=free['best_bd'], evals=locked['evals'] + free['evals'], dt=dt)
    BP_RESULTS[tag] = rec
    return rec


def task2_blueprint_search(time_budget_s=5400, seed=20260713):
    say('=== TASK 2: blueprint search at n=7 ===')
    rng = random.Random(seed)
    catalog = build_catalog_n(7)
    catalog.sort(key=priority_key)
    say(f'  catalog: {len(catalog)} blueprints (raw canonical x axis, no P2/P3 '
        f'collapse applied -- N=7 generalization of blueprint_enum.py)')

    gate_row = next(r for r in catalog if r['is_gate'])
    say(f'  GATE blueprint: id={gate_row["id"]} tag={gate_row["tag"]} '
        f'(onaxis3+spoke3+free1 on (1,1,1) -- 723\'s structure + the free 7th cube)')
    seed1207 = {'axis_name': '(1,1,1)',
                'clusters': [{'kind': 'spoke', 'base': (4, 1, 1, -1),
                               'angles': [(0, 1), (1, 1), (-1, 1)]},
                              {'kind': 'onaxis', 'base': None,
                               'angles': [(1, 2), (1, 1), (2, 5)]}],
                'free': [list(CUBE7)]}
    gate_rec = run_blueprint(gate_row['tag'], '(1,1,1)', gate_row['spec'],
                              BUDGET_GATE7, start_genomes=[seed1207], rng=rng)
    gate_ok = gate_rec['free_best'] is not None and gate_rec['free_best'] >= RECORD_N7
    say(f'  GATE result: free_best={gate_rec["free_best"]} (want >=1207) '
        f'{"PASS" if gate_ok else "FAIL"}')
    if gate_rec['free_best'] and gate_rec['free_best'] > RECORD_N7:
        cfg = sas.genome_config2(gate_rec['free_genome'])
        note_candidate_beat(gate_rec['free_best'], cfg, gate_rec['free_bd'], 'task2_gate')
    if not gate_ok:
        log({'task': 'task2', 'FLAG': 'GATE FAILED',
             'detail': 'blueprint family did not reproduce 1207 -- results below suspect'})
        say('  *** GATE FAILED -- continuing anyway but flagging in log ***')

    done, beats = [gate_row['tag']], []
    t0 = time.time()
    for row in catalog:
        if row['tag'] == gate_row['tag']:
            continue
        if time.time() - t0 > time_budget_s:
            say(f'  time budget ({time_budget_s}s) exhausted; '
                f'{len(done)}/{len(catalog)} blueprints run, stopping task2 sweep')
            break
        rec = run_blueprint(row['tag'], row['axis'] or '(1,1,1)', row['spec'],
                             BUDGET_DEFAULT7, rng=rng)
        done.append(row['tag'])
        beat = ''
        if rec['free_best'] and rec['free_best'] > RESULTS['record_n7']['total']:
            cfg = sas.genome_config2(rec['free_genome'])
            v = note_candidate_beat(rec['free_best'], cfg, rec['free_bd'], f'task2_{row["tag"]}')
            beat = ' <<< VERIFIED BEAT' if v else ' <<< unverified'
        if row['id'] % 10 == 0 or beat:
            say(f'  [{len(done)}/{len(catalog)}] {row["tag"]}: '
                f'locked={rec["locked_best"]} free={rec["free_best"]}{beat}')

    dt = time.time() - t0
    say(f'TASK 2 done: {len(done)}/{len(catalog)} blueprints run in {dt:.0f}s')
    best_bp = max(((t, r['free_best']) for t, r in BP_RESULTS.items()
                   if r['free_best'] is not None), key=lambda x: x[1], default=(None, None))
    say(f'  best blueprint overall: {best_bp}')
    RESULTS['task2'] = {'catalog_size': len(catalog), 'done': done,
                         'gate_ok': gate_ok, 'best': best_bp, 'dt': dt}
    return RESULTS['task2']


# =============================================================== TASK 3
def scan_file_for_n7(path, violations, maxvals):
    n = 0
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line or '"quats"' not in line or '"by_depth"' not in line:
                    continue
                try:
                    r = json.loads(line)
                except json.JSONDecodeError:
                    continue
                quats = r.get('quats')
                bd = r.get('by_depth')
                if not quats or not bd or len(quats) != 7:
                    continue
                bd = {int(k): v for k, v in bd.items()}
                n += 1
                for l in range(1, 7):
                    depth = 7 - l
                    val = bd.get(depth, 0)
                    if val > maxvals[l]['val']:
                        maxvals[l] = {'val': val, 'quats': quats, 'source': path}
                    if val > CEIL7[l]:
                        violations.append({'file': path, 'l': l, 'depth': depth,
                                            'val': val, 'cap': CEIL7[l], 'quats': quats})
    except FileNotFoundError:
        pass
    return n


def task3_ceiling(hunt_restarts=24, seed=20260714):
    say('=== TASK 3: ceiling verification at n=7 ===')
    say(f'  law: C(l,7) = {CEIL7}')
    violations = []
    maxvals = {l: {'val': -1, 'quats': None, 'source': None} for l in range(1, 7)}

    candidate_files = ['campaign_n7.jsonl', 'n7_program.jsonl',
                        'exact_search_results.jsonl']
    scanned = {}
    for fn in candidate_files:
        path = os.path.join(HERE, fn)
        cnt = scan_file_for_n7(path, violations, maxvals)
        scanned[fn] = cnt
        say(f'  scanned {fn}: {cnt} n=7 records with by_depth')

    # always include the known record(s) explicitly (in case they are not
    # captured verbatim in any jsonl, e.g. 1207 was originally reported
    # only in six_cube_search_results.md prose)
    known = [(RECORD_N7, CFG_1207)]
    if RESULTS['record_n7']['total'] != RECORD_N7:
        known.append((RESULTS['record_n7']['total'], RESULTS['record_n7']['quats']))
    for total, quats in known:
        r = batch_eval([quats])[0]
        if r is None:
            continue
        tot, bd = r
        for l in range(1, 7):
            depth = 7 - l
            val = bd.get(depth, 0)
            if val > maxvals[l]['val']:
                maxvals[l] = {'val': val, 'quats': quats, 'source': 'known_record'}
            if val > CEIL7[l]:
                violations.append({'file': 'known_record', 'l': l, 'depth': depth,
                                    'val': val, 'cap': CEIL7[l], 'quats': quats})

    say('  attained caps so far (post-scan, incl. known records):')
    for l in range(1, 7):
        mv = maxvals[l]
        status = 'ATTAINED' if mv['val'] == CEIL7[l] else f'short by {CEIL7[l]-mv["val"]}'
        say(f'    l={l} depth-{7-l}: max observed={mv["val"]}  cap={CEIL7[l]}  {status}')

    if violations:
        say(f'  !!!! {len(violations)} CEILING VIOLATIONS FOUND -- law may be false !!!!')
        for v in violations[:5]:
            log({'task': 'task3', 'FLAG': 'CEILING VIOLATION', **v})

    # targeted hunt: maximize depth-1 (l=6, cap 392) and depth-2 (l=5, cap
    # 330) directly, since generic/unclustered configs tend to be
    # shallow-heavy (Postscript 17's "golden is d1-heavy" finding suggests
    # UNCLUSTERED free configs -- not shared-axis records -- are the right
    # place to look for large d1/d2).
    hunts = {}
    rng = random.Random(seed)
    for depth_target, l in ((1, 6), (2, 5)):
        say(f'  hunting depth-{depth_target} (l={l}, cap={CEIL7[l]}, '
            f'observed max so far={maxvals[l]["val"]}) ...')
        score_fn = (lambda total, bd, dt=depth_target: bd.get(dt, 0))
        best = {'val': maxvals[l]['val'], 'quats': maxvals[l]['quats']}
        for rs in range(hunt_restarts):
            start = [list(random_quat(rng, maxc=120)) for _ in range(7)]
            cur, r = climb(start, f'hunt_d{depth_target}_{rs}', 'task3',
                            max_iters=60, score_fn=score_fn, log_every=False)
            if r is None:
                continue
            val = r[1].get(depth_target, 0)
            if val > best['val']:
                best = {'val': val, 'quats': cur, 'total': r[0], 'bd': r[1]}
                say(f'    restart {rs}: depth-{depth_target}={val}  <-- new best '
                    f'(total={r[0]})')
                log({'task': 'task3', 'stage': f'hunt_d{depth_target}', 'rs': rs,
                     'quats': cur, 'total': r[0], 'by_depth': r[1]})
            if val > CEIL7[l]:
                say(f'    !!!! HUNT FOUND A VIOLATION: depth-{depth_target}={val} '
                    f'> cap {CEIL7[l]} !!!!')
                violations.append({'file': 'hunt', 'l': l, 'depth': depth_target,
                                    'val': val, 'cap': CEIL7[l], 'quats': cur})
        hunts[l] = best
        say(f'  hunt l={l} (depth-{depth_target}) best = {best["val"]} (cap {CEIL7[l]})')
        if best['val'] > maxvals[l]['val']:
            maxvals[l] = {'val': best['val'], 'quats': best['quats'], 'source': 'hunt'}

    RESULTS['task3'] = {'ceil7': CEIL7, 'maxvals': {l: maxvals[l]['val'] for l in maxvals},
                         'violations': violations, 'scanned': scanned, 'hunts':
                         {l: hunts[l]['val'] for l in hunts}}
    say(f'TASK 3 done. Violations: {len(violations)}. Final observed caps: '
        f'{RESULTS["task3"]["maxvals"]}')
    return RESULTS['task3']


# =============================================================== TASK 4
def task4_extend_n8(n_candidates=300, seed=20260715):
    say('=== TASK 4: extend to n=8 ===')
    rng = random.Random(seed)
    base = RESULTS['record_n7']['quats']
    base_total = RESULTS['record_n7']['total']
    say(f'  base n=7 config: total={base_total}')

    cand8 = list(symmetric_candidates())
    while len(cand8) < n_candidates:
        cand8.append(random_quat(rng, maxc=200))
    configs8 = [[list(q) for q in base] + [list(c)] for c in cand8]
    res8 = batch_eval(configs8)
    best_total, best_i = -1, -1
    for i, rr in enumerate(res8):
        if rr is not None and rr[0] > best_total:
            best_total, best_i = rr[0], i
    say(f'  8th-cube sweep ({len(configs8)} candidates): best={best_total}')
    if best_i < 0:
        say('  no valid n=8 extension found?!')
        RESULTS['task4'] = {'best': None}
        return RESULTS['task4']

    # short climb: first just the 8th cube, then a short full climb
    cur8, r8 = climb(configs8[best_i], 'n8_swap8', 'task4', free_idx=[7], max_iters=60)
    say(f'  climb (8th cube only): {r8[0] if r8 else None}')
    cur8b, r8b = climb(cur8, 'n8_full', 'task4', max_iters=60)
    say(f'  short full climb: {r8b[0] if r8b else None}')
    best = r8b if (r8b and (not r8 or r8b[0] >= r8[0])) else r8
    best_cfg = cur8b if best is r8b else cur8

    total8, bd8 = best
    say(f'  FIRST n=8 RESULT: total={total8}  by_depth={bd8}')
    log({'task': 'task4', 'stage': 'n8_result', 'quats': best_cfg,
         'total': total8, 'by_depth': bd8})

    ceil8_violations = []
    for l in range(1, 8):
        depth = 8 - l
        val = bd8.get(depth, 0)
        if val > CEIL8[l]:
            ceil8_violations.append({'l': l, 'depth': depth, 'val': val, 'cap': CEIL8[l]})
    if ceil8_violations:
        say(f'  !!!! n=8 CEILING VIOLATIONS: {ceil8_violations} !!!!')
        log({'task': 'task4', 'FLAG': 'N8 CEILING VIOLATION', 'violations': ceil8_violations})
    else:
        say(f'  n=8 ceiling check: no violations (predictions {CEIL8})')

    RESULTS['task4'] = {'total': total8, 'quats': best_cfg, 'by_depth': bd8,
                         'ceil8': CEIL8, 'violations': ceil8_violations}
    say(f'TASK 4 done: first n=8 record = {total8}')
    return RESULTS['task4']


# =============================================================== TASK 5
def gather_top_n7_configs(top_k=50):
    """Best-known n=7 configs seen anywhere in this run: the cache (every
    config this script itself evaluated), plus explicit known records."""
    seen = {}
    for k, r in CACHE.items():
        if r is None or len(k) != 7:
            continue
        tot, bd = r
        seen[k] = (tot, bd)
    # ensure the known record(s) are present even if evicted/not in cache
    for total, quats in [(RECORD_N7, CFG_1207), (RESULTS['record_n7']['total'],
                                                    RESULTS['record_n7']['quats'])]:
        k = canon_quats(quats)
        if k not in seen:
            r = batch_eval([quats])[0]
            if r is not None:
                seen[k] = r
    ranked = sorted(seen.items(), key=lambda kv: -kv[1][0])
    return ranked[:top_k]


def task5_envelope(top_k=50):
    say('=== TASK 5: n=7 envelope (top configs -> 6-subsets) ===')
    top = gather_top_n7_configs(top_k)
    say(f'  {len(top)} top n=7 configs gathered (best={top[0][1][0] if top else None})')

    rows = []
    all_subset_cfgs = []
    idx_map = []
    for ci, (k, (tot, bd)) in enumerate(top):
        quats = [list(q) for q in k]
        for drop in range(7):
            sub = quats[:drop] + quats[drop + 1:]
            all_subset_cfgs.append(sub)
            idx_map.append((ci, drop))
    sub_res = batch_eval(all_subset_cfgs)

    max_deficit = -10 ** 9
    max_deficit_row = None
    deep_sat_count = {164: 0, 102: 0, 36: 0}
    deep_sat_total = 0
    for ci, (k, (tot, bd)) in enumerate(top):
        subtotals = []
        subbds = []
        for drop in range(7):
            # find matching index
            pass
        # collect this config's 7 subset results in order
        this = [sub_res[i] for i, (cci, drop) in enumerate(idx_map) if cci == ci]
        s_totals = [r[0] for r in this if r is not None]
        s_max = max(s_totals) if s_totals else None
        deficit = (tot - s_max) if s_max is not None else None
        for r in this:
            if r is None:
                continue
            _, sbd = r
            deep_sat_total += 1
            if sbd.get(3, 0) == 164:
                deep_sat_count[164] += 1
            if sbd.get(4, 0) == 102:
                deep_sat_count[102] += 1
            if sbd.get(5, 0) == 36:
                deep_sat_count[36] += 1
        rows.append({'total': tot, 'quats': list(k), 's_max': s_max, 'deficit': deficit})
        if deficit is not None and deficit > max_deficit:
            max_deficit = deficit
            max_deficit_row = rows[-1]

    say(f'  max(T - S_max) over top {len(top)} n=7 configs = {max_deficit} '
        f'(config total={max_deficit_row["total"] if max_deficit_row else None})')
    say(f'  n=6 deep-cap saturation among all {deep_sat_total} 6-subsets: '
        f'depth3=164: {deep_sat_count[164]}/{deep_sat_total}, '
        f'depth4=102: {deep_sat_count[102]}/{deep_sat_total}, '
        f'depth5=36: {deep_sat_count[36]}/{deep_sat_total}')

    RESULTS['task5'] = {'top_k': len(top), 'max_deficit': max_deficit,
                         'max_deficit_row': max_deficit_row,
                         'deep_sat_count': deep_sat_count, 'deep_sat_total': deep_sat_total,
                         'rows': rows}
    log({'task': 'task5', 'stage': 'summary', 'max_deficit': max_deficit,
         'deep_sat_count': deep_sat_count, 'deep_sat_total': deep_sat_total})
    say('TASK 5 done.')
    return RESULTS['task5']


# ================================================================ REPORT
def write_report():
    L = []
    L.append('# n=7 program report\n')
    L.append('Working principles: this file\'s own docstring + task brief; '
             'reuses shared_axis_search.py and blueprint_enum.py machinery '
             'unmodified. Generated by n7_program.py.\n')
    rec = RESULTS['record_n7']
    L.append('## 1. Best n=7 record found\n')
    L.append(f'- total = **{rec["total"]}** (starting record was 1207)')
    L.append(f'- quats = {rec["quats"]}')
    if rec.get('bd'):
        L.append(f'- by_depth = {rec["bd"]}')
    if rec['total'] > RECORD_N7:
        L.append(f'- **NEW RECORD**, +{rec["total"] - RECORD_N7} over 1207, '
                 f'source: {rec.get("source")}, oracle-verified.')
    else:
        L.append('- 1207 stood: no climb, restart, blueprint, or swap-7 attempt '
                  'found anything better.')
    L.append('')

    if RESULTS['task1']:
        t1 = RESULTS['task1']
        L.append('## 2. Task 1 -- deep climb of 1207\n')
        L.append(f'- base +-1/+-2 climb from 1207: {t1["base"]["total"] if t1["base"] else None}')
        L.append(f'- {len(t1["restarts"])} wide-perturbation restarts (5-12 '
                 f'simultaneous component moves) attempted')
        best_restart = max((r["total"] for r in t1["restarts"]), default=None)
        L.append(f'- best restart total: {best_restart}')
        if t1.get('swap7'):
            L.append(f'- 7th-cube-only swap/reoptimize: {t1["swap7"]["total"]}')
        L.append(f'- **task1 overall best: {t1["best"]["total"] if t1["best"] else None}**\n')

    if RESULTS['task2']:
        t2 = RESULTS['task2']
        L.append('## 3. Task 2 -- blueprint search at n=7\n')
        L.append(f'- catalog size: {t2["catalog_size"]} blueprints '
                 f'(N=7 generalization of blueprint_enum.py\'s N=6 catalog)')
        L.append(f'- gate (onaxis3+spoke3+free1 on (1,1,1), reproducing 1207): '
                 f'{"PASS" if t2["gate_ok"] else "FAIL"}')
        L.append(f'- {len(t2["done"])}/{t2["catalog_size"]} blueprints run '
                 f'({t2["dt"]:.0f}s)')
        L.append(f'- best blueprint: {t2["best"]}')
        L.append('\n| tag | axis | locked best | free best |')
        L.append('|---|---|---|---|')
        ordered = sorted(BP_RESULTS.items(), key=lambda kv: -(kv[1]['free_best'] or -1))
        for tag, r in ordered[:25]:
            L.append(f'| {tag} | {r["axis"]} | {r["locked_best"]} | {r["free_best"]} |')
        L.append('')

    if RESULTS['task3']:
        t3 = RESULTS['task3']
        L.append('## 4. Task 3 -- ceiling verification at n=7\n')
        L.append(f'- law: C(l,7) = {t3["ceil7"]}')
        L.append(f'- violations found: {len(t3["violations"])}')
        if t3['violations']:
            L.append('  **CEILING LAW VIOLATED** -- see n7_program.jsonl FLAG records.')
        L.append('\n| l | depth | cap C(l,7) | max observed | status |')
        L.append('|---|---|---|---|---|')
        for l in range(1, 7):
            depth = 7 - l
            cap = t3['ceil7'][l]
            val = t3['maxvals'][l]
            status = 'ATTAINED' if val == cap else f'short by {cap - val}'
            L.append(f'| {l} | {depth} | {cap} | {val} | {status} |')
        L.append(f'\n- files scanned: {t3["scanned"]}')
        L.append(f'- targeted hunt results (maximize depth-1 for l=6, depth-2 '
                 f'for l=5): {t3["hunts"]}\n')

    if RESULTS['task4']:
        t4 = RESULTS['task4']
        L.append('## 5. Task 4 -- extension to n=8\n')
        if t4.get('total') is not None:
            L.append(f'- first n=8 record: total={t4["total"]}')
            L.append(f'- quats = {t4["quats"]}')
            L.append(f'- by_depth = {t4["by_depth"]}')
            L.append(f'- ceiling predictions C(l,8) = {t4["ceil8"]}')
            L.append(f'- violations: {t4["violations"] or "none"}')
        else:
            L.append('- no valid n=8 extension found')
        L.append('')

    if RESULTS['task5']:
        t5 = RESULTS['task5']
        L.append('## 6. Task 5 -- n=7 envelope (cheap version)\n')
        L.append(f'- top {t5["top_k"]} n=7 configs, all seven 6-subsets counted exactly')
        L.append(f'- max(T - S_max) = **{t5["max_deficit"]}** '
                 f'(known point: 1207 - 723 = 484)')
        if t5['max_deficit_row']:
            L.append(f'  attained by config total={t5["max_deficit_row"]["total"]}, '
                     f'S_max={t5["max_deficit_row"]["s_max"]}')
        dsc, dst = t5['deep_sat_count'], t5['deep_sat_total']
        L.append(f'- n=6 deep-cap saturation across {dst} 6-subsets: '
                 f'depth3=164: {dsc[164]}/{dst}, depth4=102: {dsc[102]}/{dst}, '
                 f'depth5=36: {dsc[36]}/{dst}')
        L.append('')

    L.append(f'\nTotal evals this run: {STATS["evals"]} (cache hits: {STATS["cache_hits"]}). '
             f'Total wall time: {time.time()-_T0:.0f}s.')
    with open(REPORT_PATH, 'w') as f:
        f.write('\n'.join(L) + '\n')
    say(f'Report written -> {REPORT_PATH}')


# =================================================================== MAIN
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('tasks', nargs='*', default=['task1', 'task2', 'task3', 'task4', 'task5'])
    ap.add_argument('--t1-restarts', type=int, default=32)
    ap.add_argument('--t2-budget-s', type=int, default=5400)
    ap.add_argument('--t3-hunt-restarts', type=int, default=24)
    ap.add_argument('--t4-candidates', type=int, default=300)
    ap.add_argument('--t5-topk', type=int, default=50)
    args = ap.parse_args()

    say(f'n7_program starting. tasks={args.tasks}')
    log({'task': 'meta', 'stage': 'start', 'args': vars(args)})

    if 'task1' in args.tasks:
        task1_climb(n_restarts=args.t1_restarts)
        write_report()
    if 'task2' in args.tasks:
        task2_blueprint_search(time_budget_s=args.t2_budget_s)
        write_report()
    if 'task3' in args.tasks:
        task3_ceiling(hunt_restarts=args.t3_hunt_restarts)
        write_report()
    if 'task4' in args.tasks:
        task4_extend_n8(n_candidates=args.t4_candidates)
        write_report()
    if 'task5' in args.tasks:
        task5_envelope(top_k=args.t5_topk)
        write_report()

    say('ALL DONE.')
    log({'task': 'meta', 'stage': 'done', 'results_summary':
         {'record_n7': RESULTS['record_n7']['total'],
          'task4_n8': RESULTS['task4']['total'] if RESULTS.get('task4') else None,
          'task5_envelope': RESULTS['task5']['max_deficit'] if RESULTS.get('task5') else None}})


if __name__ == '__main__':
    main()
