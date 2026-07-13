#!/usr/bin/env python3
# Working principles: PROJECT.md, NPLUS_SPEC.md, golden_wall_report.md (golden_six.py
# pattern generalized from n=6 to n=4). Project index: README.md
"""n=4 record hunt: establish/confirm the golden four-cube compound (177) and
search for anything that beats it.

Phases (each appends JSON-line records to n4_search.jsonl, field "phase"):
  0  validation gates:
       - golden four-cube = 177 via cube_compound_exact.run(4) (Q(sqrt5))
       - same 177 re-derived through certify_six.exact_count_config, feeding
         it the golden cubes' rotation matrices directly (no quaternion
         round-trip: the icosahedral double cover needs Q(sqrt2,sqrt5),
         degree 4, while the golden SO(3) matrices themselves live in the
         degree-2 field Q(sqrt5) -- see golden_rotations.py's docstring)
       - cube_regions_n --n 4 cross-checked against the certify_six oracle
         on 5 random seeds (exact match required, by_depth included)
  G  golden 3-subset + 1 free RATIONAL cube (family A: free cube's matrix
     Q(quat) world-relative; family B: Q(quat) composed with a genuinely
     irrational golden cube (index 1) -- both stay in Q(sqrt5) since it is
     closed under +,-,*,/). Mirrors golden_six.py's approach at n=6 (found
     681 there); symmetric-candidate quats + random batch + exact hillclimb.
  S1 octahedral-type family: 2 axis-pairs (+-theta about x, about y), theta
     swept EXACTLY via the integer-quaternion parameter t (quat (t,1,0,0)
     etc.), no floating point anywhere -- generalizes six6_mats (n=6) to
     n=4 without approximation.
  S2 shared-C4-axis orbit: cube_k = Rz(k*90deg) * Q0 for k=0..3 (Rz(90deg)
     is exactly rational, quat (1,0,0,1)), Q0 swept over symmetric +
     random candidates, then hillclimbed.
  S3 shared-C3-axis-(1,1,1) orbit of 3 + 1 free cube: cube_k = R111(k*120)
     * Q0 for k=0,1,2 (R111(120deg) = quat (1,1,1,1), exactly rational)
     + one free rational cube, mirroring the winning n=6 shape (C3-orbit-
     of-3 + 3 free) at n=4 scale (orbit-of-3 + 1 free). Q0 and the free
     cube both swept + hillclimbed.
  M  mod-4 parity check on every rational config this script evaluated
     (predicted bounded == 2*4-1 = 7 == 3 mod 4).

All rational evaluations go through the validated C++ engine
(./cube_regions_n --n 4, gated in phase 0); all golden (Q(sqrt5))
evaluations go through certify_six.exact_count_config (gated against
cube_compound_exact.run() in phase 0). No floating point decides a region
boundary anywhere in this file.

Usage: python3 n4_search.py [phase ...]   (default: all phases in order)
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
from cube_compound_exact import build_axes, find_cubes, run as golden_run
from certify_six import exact_count_config
from golden_rotations import Rot, rot_from_quat

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.join(HERE, 'cube_regions_n')
LOG_PATH = os.path.join(HERE, 'n4_search.jsonl')
N = 4
MAXC = 512
WORKERS = 4          # hard rule: <=4 cores
GOLDEN_TARGET = 177


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
    golden_six.py's symmetric_candidates (identity, 90/180 about coordinate
    axes, 60/120 about body diagonals -- all exactly rational rotations)."""
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

    # gate A: cube_compound_exact.run(4) == 177
    t0 = time.time()
    r = golden_run(4)
    okA = (r == GOLDEN_TARGET)
    print(f'  gate A (cube_compound_exact.run(4)): {r} '
          f'(expected {GOLDEN_TARGET})  {"OK" if okA else "FAIL"}  '
          f'({time.time()-t0:.1f}s)', flush=True)
    ok = ok and okA

    # gate B: same golden 4 cubes through certify_six.exact_count_config,
    # built directly from the axes (rotation matrix columns = the cube's own
    # 3 orthogonal unit axes), det fixed to +1 by swapping two columns if a
    # triple comes out left-handed.
    axes = build_axes()
    triples = find_cubes(axes)[:4]

    def det3(m):
        return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
                - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
                + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))

    rots = []
    triple_record = []
    for t in triples:
        cols = [axes[i] for i in t]
        m = [[cols[j][i] for j in range(3)] for i in range(3)]
        if det3(m).sign() < 0:
            cols = [cols[0], cols[2], cols[1]]
            m = [[cols[j][i] for j in range(3)] for i in range(3)]
        rots.append(Rot(m))
        triple_record.append(list(t))
    t0 = time.time()
    total, by_depth = exact_count_config(rots, verbose=False)
    by_depth = {int(k): v for k, v in by_depth.items()}
    by_depth_bounded = {k: v for k, v in by_depth.items() if k > 0}
    okB = (total == GOLDEN_TARGET
           and by_depth_bounded == {1: 104, 2: 48, 3: 24, 4: 1})
    print(f'  gate B (certify_six.exact_count_config on golden axes): '
          f'{total} by_depth={by_depth}  {"OK" if okB else "FAIL"}  '
          f'({time.time()-t0:.1f}s)', flush=True)
    ok = ok and okB
    log_rec(kind='golden', phase='0', total=total, by_depth=by_depth,
            triples=triple_record,
            matrices=[[[f'{e.a}+{e.b}r5' for e in row] for row in R.m]
                      for R in rots])

    # gate C: cube_regions_n --n 4 vs the oracle, 5 random seeds
    okC = True
    for s in (1, 2, 3, 17, 999):
        out = subprocess.run([BIN, '--n', '4', '--seed', str(s)],
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


# ---------------------------------------------------------------- phase G
def golden3():
    axes = build_axes()
    triples = find_cubes(axes)[:3]

    def det3(m):
        return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
                - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
                + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))

    rots = []
    for t in triples:
        cols = [axes[i] for i in t]
        m = [[cols[j][i] for j in range(3)] for i in range(3)]
        if det3(m).sign() < 0:
            cols = [cols[0], cols[2], cols[1]]
            m = [[cols[j][i] for j in range(3)] for i in range(3)]
        rots.append(Rot(m))
    return rots


def _g3_eval_worker(args):
    """Module-level (picklable) worker: golden 3-subset + 1 free rational
    cube, family A (world-relative) or B (anchored on the irrational golden
    cube index 1). Rebuilds golden3() itself -- cheap (no arrangement
    construction, just axis/matrix bookkeeping)."""
    family, quat = args
    g3 = golden3()
    Q = rot_from_quat(*quat)
    fourth = Q if family == 'A' else Q * g3[1]
    total, bd = exact_count_config(g3 + [fourth], verbose=False)
    return family, quat, total, {int(k): v for k, v in bd.items()}


def _neigh_quat(q):
    out = []
    for i in range(4):
        for d in (-2, -1, 1, 2):
            qq = list(q)
            qq[i] += d
            qq = gcd_reduce(qq)
            if all(abs(c) <= MAXC for c in qq):
                out.append(tuple(qq))
    return sorted(set(out))


def phaseG_golden3_plus_free(n_random=24, max_hillclimb_starts=3,
                              max_climb_steps=15):
    print('\n=== PHASE G: golden 3-subset + 1 free rational cube ===',
          flush=True)
    best = {'total': 0, 'family': None, 'quat': None, 'bd': None}
    cands = symmetric_quats() + random_quats(n_random, seed=4004)
    jobs = [(fam, q) for fam in ('A', 'B') for q in cands]
    results = {}
    t0 = time.time()
    with Pool(WORKERS) as pool:
        for family, quat, total, bd in pool.imap_unordered(_g3_eval_worker,
                                                             jobs):
            log_rec(kind='golden3_free', phase='G', family=family,
                    quat=list(quat), total=total, by_depth=bd)
            results[(family, quat)] = (total, bd)
            if total > best['total']:
                best.update(total=total, family=family, quat=quat, bd=bd)
                print(f'  [{family}] quat={quat} total={total}  '
                      f'<-- NEW BEST', flush=True)
        print(f'  ({len(jobs)} candidates in {time.time()-t0:.0f}s)',
              flush=True)

        # exact hillclimb (single free quaternion, +-1/+-2 moves), batched
        # per-step across the pool, from the top few starts of each family
        for fam in ('A', 'B'):
            fam_results = sorted(((v[0], q) for (f, q), v in results.items()
                                   if f == fam), reverse=True)
            for rank, (t0s, q0) in enumerate(fam_results[:max_hillclimb_starts]):
                cur, cur_total = q0, t0s
                for step in range(max_climb_steps):
                    nbrs = [nq for nq in _neigh_quat(cur)
                            if (fam, nq) not in results]
                    if nbrs:
                        for f2, q2, tot2, bd2 in pool.imap_unordered(
                                _g3_eval_worker, [(fam, nq) for nq in nbrs]):
                            log_rec(kind='golden3_free', phase='G', family=f2,
                                    quat=list(q2), total=tot2, by_depth=bd2,
                                    tag=f'climb_rank{rank}_step{step}')
                            results[(f2, q2)] = (tot2, bd2)
                    moved = False
                    for nq in _neigh_quat(cur):
                        tot, bd = results[(fam, nq)]
                        if tot > cur_total:
                            cur, cur_total = nq, tot
                            moved = True
                    if not moved:
                        break
                if cur_total > best['total']:
                    bd = results[(fam, cur)][1]
                    best.update(total=cur_total, family=fam, quat=cur, bd=bd)
                    print(f'  climb[{fam}] rank{rank} -> {cur} '
                          f'total={cur_total}  <-- NEW BEST', flush=True)
    print(f'PHASE G best: family={best["family"]} quat={best["quat"]} '
          f'total={best["total"]} by_depth={best["bd"]}', flush=True)
    return best


# --------------------------------------------------------------- phase S1
def phaseS1_octahedral_sweep(tmax=60):
    print('\n=== PHASE S1: exact-rational octahedral-type 2-axis-pair sweep '
          '===', flush=True)
    best = {'total': 0, 't': None, 'quats': None}
    for t in range(1, tmax + 1):
        quats = [(t, 1, 0, 0), (t, -1, 0, 0), (t, 0, 1, 0), (t, 0, -1, 0)]
        r = EV.eval_one([list(q) for q in quats], 'S1', f't={t}')
        if r is not None and r['bounded'] > best['total']:
            best.update(total=r['bounded'], t=t, quats=quats)
            print(f'  t={t}: total={r["bounded"]}  <-- NEW BEST', flush=True)
    print(f'PHASE S1 best: t={best["t"]} total={best["total"]} '
          f'quats={best["quats"]}', flush=True)
    if best['quats']:
        cur, r = hillclimb([list(q) for q in best['quats']], 'S1', 'climb')
        if r and r['bounded'] > best['total']:
            best.update(total=r['bounded'], quats=cur)
            print(f'  S1 climb -> total={r["bounded"]}  <-- NEW BEST',
                  flush=True)
    return best


RZ90_QUAT = (1, 0, 0, 1)   # exact 90 deg about z


def _c4_orbit_quats(q0):
    RZ90 = rot_from_quat(*RZ90_QUAT)
    Q0 = rot_from_quat(*q0)
    cubes = [Q0]
    cur = Q0
    for _ in range(3):
        cur = RZ90 * cur
        cubes.append(cur)
    return cubes


def _c4_eval_worker(q0):
    cubes = _c4_orbit_quats(q0)
    total, bd = exact_count_config(cubes, verbose=False)
    return q0, total, {int(k): v for k, v in bd.items()}


# --------------------------------------------------------------- phase S2
def phaseS2_c4_orbit(n_random=24, max_climb_steps=15):
    print('\n=== PHASE S2: shared-C4-axis orbit of a tilted base cube ===',
          flush=True)
    best = {'total': 0, 'q0': None, 'bd': None}
    cands = symmetric_quats() + random_quats(n_random, seed=5005)
    results = {}
    with Pool(WORKERS) as pool:
        for q0, total, bd in pool.imap_unordered(_c4_eval_worker, cands):
            log_rec(kind='c4_orbit', phase='S2', q0=list(q0), total=total,
                    by_depth=bd)
            results[q0] = (total, bd)
            if total > best['total']:
                best.update(total=total, q0=q0, bd=bd)
                print(f'  q0={q0}: total={total}  <-- NEW BEST', flush=True)

        cur, cur_total = best['q0'], best['total']
        if cur is not None:
            for step in range(max_climb_steps):
                nbrs = [nq for nq in _neigh_quat(cur) if nq not in results]
                if nbrs:
                    for q2, tot2, bd2 in pool.imap_unordered(_c4_eval_worker,
                                                              nbrs):
                        log_rec(kind='c4_orbit', phase='S2', q0=list(q2),
                                total=tot2, by_depth=bd2,
                                tag=f'climb_step{step}')
                        results[q2] = (tot2, bd2)
                moved = False
                for nq in _neigh_quat(cur):
                    tot, bd = results[nq]
                    if tot > cur_total:
                        cur, cur_total = nq, tot
                        moved = True
                if not moved:
                    break
            if cur_total > best['total']:
                best.update(total=cur_total, q0=cur, bd=results[cur][1])
                print(f'  S2 climb -> q0={cur} total={cur_total}  '
                      f'<-- NEW BEST', flush=True)
    print(f'PHASE S2 best: q0={best["q0"]} total={best["total"]}', flush=True)
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


def _c3_eval_worker(args):
    q0, qf = args
    orbit = _c3_orbit3(q0)
    free = rot_from_quat(*qf)
    total, bd = exact_count_config(orbit + [free], verbose=False)
    return q0, qf, total, {int(k): v for k, v in bd.items()}


# --------------------------------------------------------------- phase S3
def phaseS3_c3_orbit_plus_free(n_random=24, max_climb_steps=15):
    print('\n=== PHASE S3: shared-(1,1,1)-C3 orbit of 3 + 1 free cube ===',
          flush=True)
    best = {'total': 0, 'q0': None, 'qfree': None, 'bd': None}
    q0_cands = symmetric_quats()[:8] + random_quats(6, seed=6006)
    free_cands = symmetric_quats() + random_quats(n_random, seed=6007)
    jobs = [(q0, qf) for q0 in q0_cands for qf in free_cands]
    results = {}
    with Pool(WORKERS) as pool:
        for q0, qf, total, bd in pool.imap_unordered(_c3_eval_worker, jobs):
            log_rec(kind='c3_orbit_free', phase='S3', q0=list(q0),
                    qfree=list(qf), total=total, by_depth=bd)
            results[(q0, qf)] = (total, bd)
            if total > best['total']:
                best.update(total=total, q0=q0, qfree=qf, bd=bd)
                print(f'  q0={q0} qfree={qf}: total={total}  <-- NEW BEST',
                      flush=True)

        # hillclimb the free cube only, at the best q0
        if best['q0'] is not None:
            q0f = best['q0']
            cur, cur_total = best['qfree'], best['total']
            for step in range(max_climb_steps):
                nbrs = [nq for nq in _neigh_quat(cur)
                        if (q0f, nq) not in results]
                if nbrs:
                    for q0r, q2, tot2, bd2 in pool.imap_unordered(
                            _c3_eval_worker, [(q0f, nq) for nq in nbrs]):
                        log_rec(kind='c3_orbit_free', phase='S3',
                                q0=list(q0f), qfree=list(q2), total=tot2,
                                by_depth=bd2, tag=f'climb_step{step}')
                        results[(q0f, q2)] = (tot2, bd2)
                moved = False
                for nq in _neigh_quat(cur):
                    tot, bd = results[(q0f, nq)]
                    if tot > cur_total:
                        cur, cur_total = nq, tot
                        moved = True
                if not moved:
                    break
            if cur_total > best['total']:
                best.update(total=cur_total, qfree=cur,
                            bd=results[(q0f, cur)][1])
                print(f'  S3 climb -> qfree={cur} total={cur_total}  '
                      f'<-- NEW BEST', flush=True)
    print(f'PHASE S3 best: q0={best["q0"]} qfree={best["qfree"]} '
          f'total={best["total"]}', flush=True)
    return best


# ---------------------------------------------------------------- phase D
def phaseD_deepclimb(start_quats, n_restarts=60, seed=271828, deltas=(-2, -1, 1, 2),
                      perturb_deltas=(-4, -3, -2, -1, 1, 2, 3, 4)):
    """Deep rational hillclimb beyond a single +-1/+-2 greedy pass: from a
    starting config, (1) climb to a local max with +-1/+-2 moves, (2) certify
    it at radius 4 (+-1..+-4 single-component moves -- a strict superset of
    the local-max test), (3) fire n_restarts wide perturbations (1-6
    simultaneous components, each +-1..+-4) at the ORIGINAL start and climb
    each with +-1/+-2 moves, since escaping a radius-4 local max needs a
    multi-component jump a single-component search can never make.

    This is exactly the methodology that took the S1 structured family's
    159 champion to 183 in this project's own search: greedy climbing alone
    plateaus (159 -> 171 -> 173, each a genuine radius-4 local max), but
    repeated wide perturb-and-reclimb from the SAME starting region escapes
    each plateau into a richer one (173 -> 175 -> 179 -> 183), and 183
    recurs on ~20% of restarts once found -- the signature of a real
    (not lucky-single-hit) local basin, not a fluke."""
    print(f'\n=== PHASE D: deep multi-restart climb from {start_quats} ===',
          flush=True)
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

    cur, total = climb(start_quats, 'D:base')
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
        r4 = EV.eval_many(nbrs4, 'D', 'D:radius4')
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
        cur, total = climb(pq, f'D:restart{rs}')
        if total and total > best['total']:
            best.update(total=total, quats=cur)
            print(f'  restart {rs}: {total}  <-- NEW BEST', flush=True)

    print(f'PHASE D best: total={best["total"]} quats={best["quats"]}',
          flush=True)
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


# ------------------------------------------------------------------- main
S1_CHAMPION = [[2, 1, -2, 0], [2, -1, -2, 0], [2, 0, 1, 0], [2, 0, -1, 1]]  # =159


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('phases', nargs='*',
                     default=['0', 'G', 'S1', 'S2', 'S3', 'D', 'M'])
    args = ap.parse_args()

    if '0' in args.phases:
        ok = phase0_gates()
        if not ok:
            print('GATE FAILURE -- stopping before search.', flush=True)
            sys.exit(1)
    if 'G' in args.phases:
        phaseG_golden3_plus_free()
    if 'S1' in args.phases:
        phaseS1_octahedral_sweep()
    if 'S2' in args.phases:
        phaseS2_c4_orbit()
    if 'S3' in args.phases:
        phaseS3_c3_orbit_plus_free()
    if 'D' in args.phases:
        # seeded from the S1 champion (159); this chain is what actually
        # found the project's best n=4 config, 183 (see n4_search_report.md)
        phaseD_deepclimb(S1_CHAMPION, n_restarts=60)
    if 'M' in args.phases:
        phaseM_mod4_check()
    print(f'\ntotal rational evaluations this run: {EV.evals}', flush=True)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] in ('-h', '--help'):
        print(__doc__ or __file__)
        raise SystemExit(0)
    main()
