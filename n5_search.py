#!/usr/bin/env python3
# Working principles: PROJECT.md, NPLUS_SPEC.md, n4_search.py (mirrored
# methodology, n=4 -> n=5), six_cube_search_results.md Postscript 15.
# Project index: README.md
"""n=5 record hunt: confirm the golden five-cube compound (351) and the
723-record's 5-subset (393, found by the coordinator before this script's
structured phases ran), then push the wide-perturbation deep-climb -- the
technique that took n=4 from 159 to 183 -- from 393 and other structured
seeds to see how much further n=5 goes.

Phases (each appends JSON-line records to n5_search.jsonl, field "phase"):
  0  validation gates:
       - golden five-cube = 351 via cube_compound_exact.run(5) (Q(sqrt5))
       - same 351 re-derived through certify_six.exact_count_config, feeding
         it the golden cubes' rotation matrices directly (all 5 orthogonal
         triples among the 15 icosahedral axes)
       - cube_regions_n --n 5 cross-checked against the certify_six oracle
         on 5 random seeds (exact match required, by_depth included)
  R  723-record 5-subsets: the six ways to drop one cube from the six-cube
     record (4,1,1,-1;3,3,7,3;5,-1,-5,-5;2,1,1,1;1,1,1,1;5,2,2,2, total
     723). All six subsets already beat golden's 351; the best (drop cube
     5) is 393. Logged here for the record; this is the seed phase D uses.
  P  golden five, RATIONALIZED: round the golden five's Q(sqrt5) rotation
     matrices to nearby rational quaternions (certify_six.rationalize,
     N=512) and evaluate the resulting all-rational 5-cube config exactly
     -- probes the immediate rational neighborhood of the golden wall
     itself, a seed family n4_search.py did not need (n=4's golden
     sub-compound wasn't the full symmetric compound; n=5's is).
  S1 octahedral-type family: 2 axis-pairs (4 cubes, integer parameter t,
     exactly rational, generalizing six6_mats/n4's S1) + 1 free rational
     cube, swept + hillclimbed.
  S2 shared-C4-axis orbit of a tilted base cube (4 cubes, k=0..3) + 1 free
     rational cube (C5 has no exact rational realization -- cos(2pi/5) is
     irrational -- so the natural n=5 shared-axis family is C4-orbit-of-4
     plus one free cube, not a literal 5-fold orbit).
  S3 shared-(1,1,1)-C3 orbit of 3 + 2 free cubes -- directly downsizes the
     n=6 RECORD's own shape (3-about-a-diagonal + 3 free) to n=5 (3+2),
     the most directly record-motivated structured family here.
  D  deep multi-restart climb (n4_search.py's phaseD_deepclimb, verbatim --
     it is already written generically in terms of len(quats) and needs no
     n=5-specific changes) applied from EVERY structured champion above:
     the 393 record-subset (highest priority / most restarts), the other
     five 723-subsets, the golden-rationalized seed, and the S1/S2/S3
     champions.
  M  mod-4 parity check on every rational config this script evaluated
     (predicted bounded == 2*5-1 = 9 == 1 mod 4).

All rational evaluations go through the validated C++ engine
(./cube_regions_n --n 5, gated in phase 0); all golden (Q(sqrt5))
evaluations go through certify_six.exact_count_config (gated against
cube_compound_exact.run() in phase 0). No floating point decides a region
boundary anywhere in this file (rationalize() rounds floats to build a
RATIONAL seed in phase P, but the seed's own region count is then only
ever evaluated exactly).

Usage: python3 n5_search.py [phase ...]   (default: all phases in order)
"""
import argparse
import itertools
import json
import math
import os
import random
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cube_compound_exact import build_axes, find_cubes
from certify_six import exact_count_config, rationalize
from golden_rotations import Rot, rot_from_quat

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.join(HERE, 'cube_regions_n')
LOG_PATH = os.path.join(HERE, 'n5_search.jsonl')
N = 5
MAXC = 512
WORKERS = 4          # hard rule: <=4 cores
GOLDEN_TARGET = 351
GOLDEN_BY_DEPTH = {1: 180, 2: 80, 3: 60, 4: 30, 5: 1}

RECORD6_QUATS = [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5),
                 (2, 1, 1, 1), (1, 1, 1, 1), (5, 2, 2, 2)]   # n=6 record, 723


# --------------------------------------------------------------- utilities
def gcd_reduce(ints):
    g = math.gcd(*[abs(c) for c in ints])
    if g > 1:
        ints = [c // g for c in ints]
    if not any(ints):
        ints = [1, 0, 0, 0]
    return list(ints)


def canon(quats):
    out = []
    for q in quats:
        q = gcd_reduce(list(q))
        for c in q:
            if c != 0:
                if c < 0:
                    q = [-x for x in q]
                break
        out.append(tuple(q))
    return tuple(out)


def quats_str(quats):
    return ';'.join(','.join(str(c) for c in q) for q in quats)


def det3(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def golden_rots(k=5):
    """First k of the 5 golden cubes as Rot objects (handedness fixed)."""
    axes = build_axes()
    triples = find_cubes(axes)[:k]
    rots = []
    for t in triples:
        cols = [axes[i] for i in t]
        m = [[cols[j][i] for j in range(3)] for i in range(3)]
        if det3(m).sign() < 0:
            cols = [cols[0], cols[2], cols[1]]
            m = [[cols[j][i] for j in range(3)] for i in range(3)]
        rots.append(Rot(m))
    return rots


_LOGF = open(LOG_PATH, 'a')


def log_rec(**kw):
    _LOGF.write(json.dumps(kw) + '\n')
    _LOGF.flush()


def cpp_eval(quats):
    """Exact rational count via the validated C++ engine. Returns dict or
    None on degeneracy."""
    try:
        out = subprocess.run([BIN, '--n', str(N), '--quats', quats_str(quats)],
                              capture_output=True, text=True, timeout=60)
        r = json.loads(out.stdout.strip())
        if 'error' in r:
            return None
        return r
    except Exception:
        return None


class Evaluator:
    """Memoized, <=4-way parallel rational evaluator; logs every fresh eval."""

    def __init__(self, workers=WORKERS):
        self.pool = ThreadPoolExecutor(max_workers=workers)
        self.memo = {}
        self.evals = 0
        if os.path.exists(LOG_PATH):
            for line in open(LOG_PATH):
                try:
                    r = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if r.get('kind') != 'rational' or 'quats' not in r:
                    continue
                k = tuple(tuple(q) for q in r['quats'])
                self.memo[k] = r if 'bounded' in r else None

    def eval_many(self, quats_list, phase, tag=''):
        keys = [canon(q) for q in quats_list]
        todo, seen_now = [], set()
        for k in keys:
            if k not in self.memo and k not in seen_now:
                seen_now.add(k)
                todo.append(k)
        results = list(self.pool.map(lambda k: cpp_eval(list(map(list, k))), todo))
        for k, r in zip(todo, results):
            self.memo[k] = r
            self.evals += 1
            if r is not None:
                log_rec(kind='rational', phase=phase, tag=tag,
                        quats=[list(q) for q in k], bounded=r['bounded'],
                        by_depth=r['by_depth'])
            else:
                log_rec(kind='rational', phase=phase, tag=tag,
                        quats=[list(q) for q in k], error='degenerate')
        return [self.memo[k] for k in keys]

    def eval_one(self, quats, phase, tag=''):
        return self.eval_many([quats], phase, tag)[0]


EV = Evaluator()


def neighbors(quats, free_idx=None, max_c=MAXC):
    """All single-component +-1/+-2 moves. If free_idx given, only that
    cube's quaternion is varied (structured families: fixed symmetric part,
    free part explored)."""
    idxs = range(len(quats)) if free_idx is None else [free_idx]
    out = []
    for i in idxs:
        for j in range(4):
            for d in (-2, -1, 1, 2):
                q = [list(x) for x in quats]
                q[i][j] += d
                if all(c == 0 for c in q[i]):
                    continue
                cq = canon(q)
                if any(abs(c) > max_c for qq in cq for c in qq):
                    continue
                out.append([list(x) for x in cq])
    return out


def hillclimb(quats0, phase, tag, free_idx=None, max_iters=60):
    cur = [list(q) for q in canon(quats0)]
    r = EV.eval_one(cur, phase, tag + ':start')
    if r is None:
        return cur, None
    cur_total = r['bounded']
    it = 0
    while it < max_iters:
        it += 1
        nbrs = neighbors(cur, free_idx)
        results = EV.eval_many(nbrs, phase, f'{tag}:it{it}')
        best_i, best_score = -1, cur_total
        for i, rr in enumerate(results):
            if rr is not None and rr['bounded'] > best_score:
                best_i, best_score = i, rr['bounded']
        if best_i < 0:
            break
        cur, cur_total, r = nbrs[best_i], best_score, results[best_i]
    return cur, r


def symmetric_quats():
    """Same hand-picked exact-rational special-angle quaternions as
    golden_six.py / n4_search.py's symmetric_candidates (identity, 90/180
    about coordinate axes, 60/120 about body diagonals -- all exactly
    rational rotations)."""
    cands = [(1, 0, 0, 0)]
    for i in range(3):
        q90 = [1, 0, 0, 0]; q90[i + 1] = 1; cands.append(tuple(q90))
        qm90 = [1, 0, 0, 0]; qm90[i + 1] = -1; cands.append(tuple(qm90))
        q180 = [0, 0, 0, 0]; q180[i + 1] = 1; cands.append(tuple(q180))
    for s1, s2 in itertools.product((1, -1), repeat=2):
        cands.append((1, 1, s1, s2))
        cands.append((1, -1, -s1, -s2))
        cands.append((3, 1, s1, s2))
        cands.append((3, -1, -s1, -s2))
    out, seen = [], set()
    for q in cands:
        q = tuple(gcd_reduce(list(q)))
        if q not in seen:
            seen.add(q)
            out.append(q)
    return out


def random_quats(n, seed, maxc=MAXC):
    rng = random.Random(seed)
    out, seen = [], set()
    while len(out) < n:
        q = tuple(gcd_reduce([rng.randint(-maxc, maxc) for _ in range(4)]))
        if q not in seen:
            seen.add(q)
            out.append(q)
    return out


# ---------------------------------------------------------------- phase 0
def phase0_gates():
    print('=== PHASE 0: validation gates ===', flush=True)
    ok = True

    # gate A: cube_compound_exact.run(5) == 351
    import cube_compound_exact as cce
    t0 = time.time()
    r = cce.run(5)
    okA = (r == GOLDEN_TARGET)
    print(f'  gate A (cube_compound_exact.run(5)): {r} '
          f'(expected {GOLDEN_TARGET})  {"OK" if okA else "FAIL"}  '
          f'({time.time()-t0:.1f}s)', flush=True)
    ok = ok and okA

    # gate B: same golden 5 cubes through certify_six.exact_count_config,
    # built directly from the axes (all 5 orthogonal triples).
    rots = golden_rots(5)
    t0 = time.time()
    total, by_depth = exact_count_config(rots, verbose=False)
    by_depth = {int(k): v for k, v in by_depth.items()}
    by_depth_bounded = {k: v for k, v in by_depth.items() if k > 0}
    okB = (total == GOLDEN_TARGET and by_depth_bounded == GOLDEN_BY_DEPTH)
    print(f'  gate B (certify_six.exact_count_config on golden axes): '
          f'{total} by_depth={by_depth}  {"OK" if okB else "FAIL"}  '
          f'({time.time()-t0:.1f}s)', flush=True)
    ok = ok and okB
    log_rec(kind='golden', phase='0', total=total, by_depth=by_depth,
            matrices=[[[f'{e.a}+{e.b}r5' for e in row] for row in R.m]
                      for R in rots])

    # gate C: cube_regions_n --n 5 vs the oracle, 5 random seeds
    okC = True
    for s in (1, 2, 3, 17, 999):
        out = subprocess.run([BIN, '--n', '5', '--seed', str(s)],
                              capture_output=True, text=True, timeout=30).stdout
        d = json.loads(out)
        rots_s = [rot_from_quat(*q) for q in d['quats']]
        total_s, bd_s = exact_count_config(rots_s, verbose=False)
        bd_s = {int(k): v for k, v in bd_s.items()}
        cpp_bd = {int(k): v for k, v in d['by_depth'].items()}
        match = (total_s == d['bounded'] and bd_s == cpp_bd)
        okC = okC and match
        print(f'  gate C seed {s}: cpp={d["bounded"]} oracle={total_s}  '
              f'{"MATCH" if match else "MISMATCH"}', flush=True)
    print(f'PHASE 0: {"ALL GATES PASS" if ok and okC else "GATE FAILURE"}',
          flush=True)
    return ok and okC


# ---------------------------------------------------------------- phase R
def phaseR_record6_subsets():
    """The six 5-subsets of the n=6 record (723). Confirms the coordinator's
    393 finding independently through this script's own evaluator/log, and
    records the full ranked table -- this is the seed set phase D anchors
    on."""
    print('\n=== PHASE R: 723-record 5-subsets ===', flush=True)
    results = []
    for drop in range(6):
        subset = [RECORD6_QUATS[i] for i in range(6) if i != drop]
        r = EV.eval_one([list(q) for q in subset], 'R', f'drop{drop}')
        results.append((drop, subset, r))
        print(f'  drop cube {drop} ({RECORD6_QUATS[drop]}): '
              f'total={r["bounded"] if r else None} '
              f'by_depth={r["by_depth"] if r else None}', flush=True)
    best_drop, best_subset, best_r = max(
        (x for x in results if x[2] is not None), key=lambda x: x[2]['bounded'])
    print(f'PHASE R best: drop={best_drop} total={best_r["bounded"]} '
          f'quats={best_subset}', flush=True)
    return results, (best_subset, best_r)


# ---------------------------------------------------------------- phase P
def phaseP_golden_rationalized():
    """Round the golden five's Q(sqrt5) matrices to a nearby all-rational
    5-cube config (certify_six.rationalize, N=512) and evaluate it exactly
    -- probes the immediate rational neighborhood of the golden wall."""
    print('\n=== PHASE P: golden five, rationalized ===', flush=True)
    rots = golden_rots(5)
    float_mats = [[[float(e) for e in row] for row in R.m] for R in rots]
    import numpy as np
    rat_rots = rationalize([np.array(m) for m in float_mats], N=512)
    # rat_rots are Rot objects with all-rational (b=0) Q5 entries; recover
    # an integer quaternion per cube by reading off the matrix numerically
    # is unnecessary -- rationalize() already stores exact Fr entries, so
    # go straight to exact_count_config on these Rot objects AND also
    # extract an integer-quaternion form for the C++ engine + phase D.
    total, bd = exact_count_config(rat_rots, verbose=False)
    bd = {int(k): v for k, v in bd.items()}
    print(f'  oracle count of rationalized golden-5: total={total} '
          f'by_depth={bd}', flush=True)
    log_rec(kind='golden_rationalized', phase='P', total=total, by_depth=bd)

    # recover integer quaternions for the cube_regions_n engine: scipy round
    # -trip identical to rationalize()'s own construction (see certify_six.py)
    from scipy.spatial.transform import Rotation
    quats = []
    for m in float_mats:
        q = Rotation.from_matrix(m).as_quat()
        comps = (q[3], q[0], q[1], q[2])
        ints = [round(c * 512) for c in comps]
        if not any(ints):
            ints = [1, 0, 0, 0]
        g = math.gcd(*[abs(x) for x in ints])
        if g > 1:
            ints = [x // g for x in ints]
        quats.append(ints)
    r = EV.eval_one(quats, 'P', 'cpp_crosscheck')
    match = (r is not None and r['bounded'] == total
             and {int(k): v for k, v in r['by_depth'].items()} == bd)
    print(f'  cube_regions_n cross-check: total={r["bounded"] if r else None} '
          f'{"MATCH" if match else "MISMATCH/degenerate-tolerance"}', flush=True)
    return quats, r


# --------------------------------------------------------------- phase S1
def phaseS1_octahedral_plus_free(tmax=40, n_free=16, max_climb_steps=15):
    """2 axis-pairs (4 cubes, integer t, exactly rational) + 1 free rational
    cube, swept over t and free-cube candidates, then hillclimbed (free
    cube only, then all 5)."""
    print('\n=== PHASE S1: octahedral-type 2-axis-pair (4 cubes) + 1 free '
          '===', flush=True)
    best = {'total': 0, 't': None, 'free': None, 'quats': None}
    free_cands = symmetric_quats() + random_quats(n_free, seed=15015)
    for t in range(1, tmax + 1, 3):     # coarse sweep over t first
        base = [(t, 1, 0, 0), (t, -1, 0, 0), (t, 0, 1, 0), (t, 0, -1, 0)]
        jobs = [base + [list(f)] for f in free_cands[:6]]
        results = EV.eval_many(jobs, 'S1', f't={t}:coarse')
        for f, job, r in zip(free_cands[:6], jobs, results):
            if r is not None and r['bounded'] > best['total']:
                best.update(total=r['bounded'], t=t, free=f, quats=job)
                print(f'  t={t} free={f}: total={r["bounded"]}  <-- NEW BEST',
                      flush=True)
    if best['t'] is not None:
        t = best['t']
        base = [(t, 1, 0, 0), (t, -1, 0, 0), (t, 0, 1, 0), (t, 0, -1, 0)]
        jobs = [[list(q) for q in base] + [list(f)] for f in free_cands]
        results = EV.eval_many(jobs, 'S1', f't={t}:fine')
        for f, r in zip(free_cands, results):
            if r is not None and r['bounded'] > best['total']:
                best.update(total=r['bounded'], t=t, free=f,
                            quats=[list(q) for q in base] + [list(f)])
                print(f'  t={t} free={f}: total={r["bounded"]}  <-- NEW BEST',
                      flush=True)
        cur, r = hillclimb(best['quats'], 'S1', 'climb_free', free_idx=4,
                            max_iters=max_climb_steps)
        if r and r['bounded'] > best['total']:
            best.update(total=r['bounded'], quats=cur)
            print(f'  S1 free-only climb -> total={r["bounded"]}  '
                  f'<-- NEW BEST', flush=True)
        cur, r = hillclimb(best['quats'], 'S1', 'climb_all',
                            max_iters=max_climb_steps)
        if r and r['bounded'] > best['total']:
            best.update(total=r['bounded'], quats=cur)
            print(f'  S1 all-free climb -> total={r["bounded"]}  '
                  f'<-- NEW BEST', flush=True)
    print(f'PHASE S1 best: total={best["total"]} quats={best["quats"]}',
          flush=True)
    return best


RZ90_QUAT = (1, 0, 0, 1)   # exact 90 deg about z


def _c4_orbit_quats_mats(q0):
    RZ90 = rot_from_quat(*RZ90_QUAT)
    Q0 = rot_from_quat(*q0)
    cubes = [Q0]
    cur = Q0
    for _ in range(3):
        cur = RZ90 * cur
        cubes.append(cur)
    return cubes


def _c4_free_eval_worker(args):
    """Module-level (picklable) worker: shared-C4-axis orbit (4 cubes) + 1
    free rational cube, evaluated via the Python oracle (exact Q(sqrt5)/
    rational arithmetic)."""
    q0, free = args
    orbit = _c4_orbit_quats_mats(q0)
    free_r = rot_from_quat(*free)
    total, bd = exact_count_config(orbit + [free_r], verbose=False)
    return q0, free, total, {int(k): v for k, v in bd.items()}


# --------------------------------------------------------------- phase S2
def phaseS2_c4_orbit_plus_free(n_random=16, max_climb_steps=15):
    """Shared-C4-axis orbit of a tilted base cube (4 cubes) + 1 free
    rational cube. C5 has no exact rational realization, so this (not a
    literal 5-fold orbit) is the natural n=5 shared-axis family."""
    print('\n=== PHASE S2: shared-C4-axis orbit (4 cubes) + 1 free ===',
          flush=True)
    best = {'total': 0, 'q0': None, 'free': None, 'quats': None}
    q0_cands = symmetric_quats()[:8] + random_quats(6, seed=25025)
    free_cands = symmetric_quats() + random_quats(n_random, seed=25026)

    jobs = [(q0, f) for q0 in q0_cands for f in free_cands[:6]]
    with Pool(WORKERS) as pool:
        for q0, f, total, bd in pool.imap_unordered(_c4_free_eval_worker, jobs):
            log_rec(kind='c4_orbit_free', phase='S2', q0=list(q0), free=list(f),
                    total=total, by_depth=bd)
            if total > best['total']:
                best.update(total=total, q0=q0, free=f)
                print(f'  q0={q0} free={f}: total={total}  <-- NEW BEST',
                      flush=True)

        if best['q0'] is not None:
            fine_jobs = [(best['q0'], f) for f in free_cands]
            for q0, f, total, bd in pool.imap_unordered(_c4_free_eval_worker,
                                                          fine_jobs):
                log_rec(kind='c4_orbit_free', phase='S2', q0=list(q0),
                        free=list(f), total=total, by_depth=bd, tag='fine_free')
                if total > best['total']:
                    best.update(total=total, free=f)
                    print(f'  q0={q0} free={f}: total={total}  '
                          f'<-- NEW BEST', flush=True)

    if best['q0'] is not None:
        orbit = _c4_orbit_quats_mats(best['q0'])
        # cross to integer quats for the C++ engine + phase D reuse: use
        # scipy round-trip like phase P
        from scipy.spatial.transform import Rotation
        ints_list = []
        for R in orbit + [rot_from_quat(*best['free'])]:
            m = [[float(e) for e in row] for row in R.m]
            q = Rotation.from_matrix(m).as_quat()
            comps = (q[3], q[0], q[1], q[2])
            ints = [round(c * 512) for c in comps]
            if not any(ints):
                ints = [1, 0, 0, 0]
            g = math.gcd(*[abs(x) for x in ints])
            if g > 1:
                ints = [x // g for x in ints]
            ints_list.append(ints)
        r = EV.eval_one(ints_list, 'S2', 'cpp_crosscheck')
        print(f'  cube_regions_n cross-check of best S2 config: '
              f'total={r["bounded"] if r else None} (oracle {best["total"]})',
              flush=True)
        best['quats'] = ints_list
        if r is not None:
            cur, r2 = hillclimb(ints_list, 'S2', 'climb_all',
                                 max_iters=max_climb_steps)
            if r2 and r2['bounded'] > best['total']:
                best.update(total=r2['bounded'], quats=cur)
                print(f'  S2 all-free climb -> total={r2["bounded"]}  '
                      f'<-- NEW BEST', flush=True)
    print(f'PHASE S2 best: q0={best["q0"]} free={best["free"]} '
          f'total={best["total"]}', flush=True)
    return best


R111_QUAT = (1, 1, 1, 1)   # exact 120 deg about (1,1,1)


def _c3_orbit3(q0):
    R111 = rot_from_quat(*R111_QUAT)
    Q0 = rot_from_quat(*q0)
    cubes = [Q0]
    cur = Q0
    for _ in range(2):
        cur = R111 * cur
        cubes.append(cur)
    return cubes


IDENT_QUAT = (1, 0, 0, 0)


def _c3_2free_eval_worker(args):
    """Module-level (picklable) worker: shared-(1,1,1)-C3 orbit of 3 + 2
    free rational cubes, evaluated via the Python oracle."""
    q0, f1, f2 = args
    orbit = _c3_orbit3(q0)
    r1, r2 = rot_from_quat(*f1), rot_from_quat(*f2)
    total, bd = exact_count_config(orbit + [r1, r2], verbose=False)
    return q0, f1, f2, total, {int(k): v for k, v in bd.items()}


# --------------------------------------------------------------- phase S3
def phaseS3_c3_orbit_plus_2free(n_free=10, max_climb_steps=15):
    """Shared-(1,1,1)-C3 orbit of 3 + 2 free cubes -- directly downsizes the
    n=6 record's own shape (3-about-a-diagonal + 3 free) to n=5 (3+2)."""
    print('\n=== PHASE S3: shared-(1,1,1)-C3 orbit of 3 + 2 free ===',
          flush=True)
    best = {'total': 0, 'q0': None, 'f1': None, 'f2': None, 'quats': None}
    q0_cands = symmetric_quats()[:6] + random_quats(4, seed=35035)
    free_cands = symmetric_quats()[:12] + random_quats(n_free, seed=35036)

    with Pool(WORKERS) as pool:
        # stage 1: coarse -- fix f2=identity, sweep q0 x f1
        jobs = [(q0, f1, IDENT_QUAT) for q0 in q0_cands for f1 in free_cands]
        for q0, f1, f2, total, bd in pool.imap_unordered(
                _c3_2free_eval_worker, jobs):
            log_rec(kind='c3_orbit_2free', phase='S3', q0=list(q0),
                    f1=list(f1), f2=list(f2), total=total, by_depth=bd,
                    tag='stage1')
            if total > best['total']:
                best.update(total=total, q0=q0, f1=f1, f2=f2)
                print(f'  [s1] q0={q0} f1={f1} f2=ident: total={total}  '
                      f'<-- NEW BEST', flush=True)

        # stage 2: fix q0,f1 at stage-1 best, sweep f2
        if best['q0'] is not None:
            jobs2 = [(best['q0'], best['f1'], f2) for f2 in free_cands]
            for q0, f1, f2, total, bd in pool.imap_unordered(
                    _c3_2free_eval_worker, jobs2):
                log_rec(kind='c3_orbit_2free', phase='S3', q0=list(q0),
                        f1=list(f1), f2=list(f2), total=total,
                        by_depth=bd, tag='stage2')
                if total > best['total']:
                    best.update(total=total, f2=f2)
                    print(f'  [s2] f2={f2}: total={total}  <-- NEW BEST',
                          flush=True)

    if best['q0'] is not None:
        from scipy.spatial.transform import Rotation
        orbit = _c3_orbit3(best['q0'])
        allR = orbit + [rot_from_quat(*best['f1']), rot_from_quat(*best['f2'])]
        ints_list = []
        for R in allR:
            m = [[float(e) for e in row] for row in R.m]
            q = Rotation.from_matrix(m).as_quat()
            comps = (q[3], q[0], q[1], q[2])
            ints = [round(c * 512) for c in comps]
            if not any(ints):
                ints = [1, 0, 0, 0]
            g = math.gcd(*[abs(x) for x in ints])
            if g > 1:
                ints = [x // g for x in ints]
            ints_list.append(ints)
        r = EV.eval_one(ints_list, 'S3', 'cpp_crosscheck')
        print(f'  cube_regions_n cross-check of best S3 config: '
              f'total={r["bounded"] if r else None} (oracle {best["total"]})',
              flush=True)
        best['quats'] = ints_list
        if r is not None:
            cur, r2 = hillclimb(ints_list, 'S3', 'climb_all',
                                 max_iters=max_climb_steps)
            if r2 and r2['bounded'] > best['total']:
                best.update(total=r2['bounded'], quats=cur)
                print(f'  S3 all-free climb -> total={r2["bounded"]}  '
                      f'<-- NEW BEST', flush=True)
    print(f'PHASE S3 best: q0={best["q0"]} f1={best["f1"]} f2={best["f2"]} '
          f'total={best["total"]}', flush=True)
    return best


# ---------------------------------------------------------------- phase D
def phaseD_deepclimb(start_quats, tag_prefix, n_restarts=40, seed=271828,
                      deltas=(-2, -1, 1, 2),
                      perturb_deltas=(-4, -3, -2, -1, 1, 2, 3, 4)):
    """Deep rational hillclimb beyond a single +-1/+-2 greedy pass -- VERBATIM
    methodology from n4_search.py's phaseD_deepclimb (already written
    generically in terms of len(quats), no n=5-specific change needed):
    (1) climb to a local max, (2) certify at radius 4, (3) fire many wide
    (1-6 simultaneous components, each +-1..+-4) perturbations at the
    ORIGINAL start and re-climb each -- the only way to escape a genuine
    radius-4 local max, since a single-component search can never make a
    multi-component jump. This is exactly the technique that took n=4's
    S1 champion (159) to the new record (183); applied here from n=5's
    723-record-subset champion (393) and other structured seeds."""
    print(f'\n=== PHASE D [{tag_prefix}]: deep multi-restart climb from '
          f'{start_quats} ===', flush=True)
    rng = random.Random(seed)
    best = {'total': 0, 'quats': None}

    def climb(start, tag, max_iters=200, mv=deltas):
        cur = [list(q) for q in canon(start)]
        r = EV.eval_one(cur, 'D', tag + ':start')
        if r is None:
            return None, None
        cur_total = r['bounded']
        it = 0
        while it < max_iters:
            it += 1
            nbrs = neighbors(cur, max_c=MAXC)
            results = EV.eval_many(nbrs, 'D', f'{tag}:it{it}')
            best_i, best_score = -1, cur_total
            for i, rr in enumerate(results):
                if rr is not None and rr['bounded'] > best_score:
                    best_i, best_score = i, rr['bounded']
            if best_i < 0:
                break
            cur, cur_total = nbrs[best_i], best_score
        return cur, cur_total

    def wide_perturb(quats, nmoves):
        q = [list(x) for x in quats]
        for _ in range(nmoves):
            i, j = rng.randrange(len(q)), rng.randrange(4)
            q[i][j] += rng.choice(perturb_deltas)
            if all(c == 0 for c in q[i]):
                q[i][j] += 1
        cq = canon(q)
        if any(abs(c) > MAXC for qq in cq for c in qq):
            return None
        return [list(x) for x in cq]

    cur, total = climb(start_quats, f'D:{tag_prefix}:base')
    if total:
        best.update(total=total, quats=cur)
        print(f'  base climb: {total}', flush=True)

    # radius-4 single-component certification of the base local max
    if cur is not None:
        nbrs4 = []
        for i in range(len(cur)):
            for j in range(4):
                for d in (-4, -3, -2, -1, 1, 2, 3, 4):
                    q = [list(x) for x in cur]
                    q[i][j] += d
                    if all(c == 0 for c in q[i]):
                        continue
                    cq = canon(q)
                    if any(abs(c) > MAXC for qq in cq for c in qq):
                        continue
                    nbrs4.append([list(x) for x in cq])
        r4 = EV.eval_many(nbrs4, 'D', f'{tag_prefix}:radius4')
        improved = any(rr is not None and rr['bounded'] > best['total']
                        for rr in r4)
        print(f'  radius-4 certification of base climb: '
              f'{"IMPROVED" if improved else "confirmed local max"}',
              flush=True)
        for i, rr in enumerate(r4):
            if rr is not None and rr['bounded'] > best['total']:
                best.update(total=rr['bounded'], quats=nbrs4[i])

    for rs in range(n_restarts):
        pq = wide_perturb(start_quats, rng.randrange(1, 7))
        if pq is None:
            continue
        cur, total = climb(pq, f'D:{tag_prefix}:restart{rs}')
        if total and total > best['total']:
            best.update(total=total, quats=cur)
            print(f'  restart {rs}: {total}  <-- NEW BEST', flush=True)

    print(f'PHASE D [{tag_prefix}] best: total={best["total"]} '
          f'quats={best["quats"]}', flush=True)
    return best


# ---------------------------------------------------------------- phase M
def phaseM_mod4_check():
    print('\n=== PHASE M: mod-4 parity check (this script\'s own log) ===',
          flush=True)
    predicted = (2 * N - 1) % 4
    total, exc = 0, 0
    for line in open(LOG_PATH):
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        if r.get('kind') != 'rational' or 'bounded' not in r:
            continue
        total += 1
        if r['bounded'] % 4 != predicted:
            exc += 1
    rate = exc / total if total else float('nan')
    print(f'  {total} rational configs, predicted bounded == {predicted} '
          f'(mod 4), {exc} exceptions ({rate:.2%})', flush=True)
    return dict(total=total, exceptions=exc, rate=rate)


def d4_report():
    """Report the max depth-4 (=n-1) count ever observed in this log --
    the n=5 analog of n4_search's d3<=24 ceiling check (task item 5:
    conjectured d4 <= 30, golden hits exactly 30)."""
    print('\n=== depth-(n-1)=4 ceiling check ===', flush=True)
    maxd4, cnt_at_cap, total = 0, 0, 0
    exceed = []
    for line in open(LOG_PATH):
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        if r.get('kind') != 'rational' or 'by_depth' not in r:
            continue
        total += 1
        bd = r['by_depth']
        d4 = bd.get('4', bd.get(4, 0))
        if d4 > maxd4:
            maxd4 = d4
        if d4 == 30:
            cnt_at_cap += 1
        if d4 > 30:
            exceed.append((r.get('quats'), d4))
    print(f'  {total} rational configs with by_depth; max d4 observed = '
          f'{maxd4}; #at cap(30) = {cnt_at_cap}; #exceeding 30 = '
          f'{len(exceed)}', flush=True)
    if exceed:
        print(f'  FIRST EXCEEDANCE: {exceed[0]}', flush=True)
    return dict(total=total, max_d4=maxd4, at_cap=cnt_at_cap,
                exceed=len(exceed))


# ------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('phases', nargs='*',
                     default=['0', 'R', 'P', 'S1', 'S2', 'S3', 'D', 'M'])
    ap.add_argument('--restarts-primary', type=int, default=40)
    ap.add_argument('--restarts-secondary', type=int, default=15)
    args = ap.parse_args()

    if '0' in args.phases:
        ok = phase0_gates()
        if not ok:
            print('GATE FAILURE -- stopping before search.', flush=True)
            sys.exit(1)

    seeds_for_D = []   # list of (tag, quats)

    if 'R' in args.phases:
        results, (best_subset, best_r) = phaseR_record6_subsets()
        seeds_for_D.append(('record393', [list(q) for q in best_subset]))
        # also keep the runner-up (387) as a secondary D seed
        ranked = sorted(
            ((r['bounded'], drop, subset) for drop, subset, r in results
             if r is not None),
            reverse=True)
        if len(ranked) > 1:
            _, _, second_subset = ranked[1]
            seeds_for_D.append(('record387', [list(q) for q in second_subset]))

    if 'P' in args.phases:
        quats, r = phaseP_golden_rationalized()
        if r is not None:
            seeds_for_D.append(('golden_rationalized', quats))

    if 'S1' in args.phases:
        b = phaseS1_octahedral_plus_free()
        if b['quats'] is not None:
            seeds_for_D.append(('S1', b['quats']))

    if 'S2' in args.phases:
        b = phaseS2_c4_orbit_plus_free()
        if b.get('quats') is not None:
            seeds_for_D.append(('S2', b['quats']))

    if 'S3' in args.phases:
        b = phaseS3_c3_orbit_plus_2free()
        if b.get('quats') is not None:
            seeds_for_D.append(('S3', b['quats']))

    if 'D' in args.phases:
        overall_best = {'total': 0, 'quats': None, 'tag': None}
        for i, (tag, quats) in enumerate(seeds_for_D):
            n_restarts = args.restarts_primary if i == 0 else args.restarts_secondary
            b = phaseD_deepclimb(quats, tag, n_restarts=n_restarts)
            if b['total'] and b['total'] > overall_best['total']:
                overall_best.update(total=b['total'], quats=b['quats'], tag=tag)
        print(f'\n=== PHASE D OVERALL BEST: total={overall_best["total"]} '
              f'tag={overall_best["tag"]} quats={overall_best["quats"]} ===',
              flush=True)

    if 'M' in args.phases:
        phaseM_mod4_check()
        d4_report()

    print(f'\ntotal rational evaluations this run: {EV.evals}', flush=True)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] in ('-h', '--help'):
        print(__doc__ or __file__)
        raise SystemExit(0)
    main()
