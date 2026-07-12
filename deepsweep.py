#!/usr/bin/env python3
# Working principles: six_cube_search_results.md Postscript 14 (deep-sacrifice
# trade-off structure). Project index: README.md
"""Deep-sacrifice trade-off surface mapper for six-cube region records.

Postscript 14 established that d3/d4/d5 are QUANTIZED (a config either
saturates the generic cap 164/102/36 or falls to a lower merged value)
while d1/d2 are UNCAPPED and grow with arrangement complexity. The
maximum-total problem is therefore: saturate the deep caps, maximize
d1+d2, and spend deep "sacrifices" only where they buy disproportionate
shallow gain. 723 already sacrifices d4 (102->96) for roughly +45 in d1
versus the best d4=102 config; 717 sacrifices d3 (164->158) instead.
This script maps that trade-off surface and hunts for a total > 723.

Two families of climb, sharing one exact hill-climbing engine:

  1. Plain objectives -- climb to maximize total, d1 alone, or d1+d2,
     with no constraint on the deep layers. Move set (identical to
     phase_b_hillclimb.py / symmetry_search2.py): add {-2,-1,+1,+2} to
     one component of one quaternion, re-gcd, reject |component| > 512,
     evaluate EXACTLY with ./cube_regions.

  2. Stratum (deep-sacrifice) objectives -- climb to maximize d1+d2
     SUBJECT TO a target ceiling (d3cap, d4cap, d5cap) on the deep
     layers, via an exact-penalty score:
         score = (d1+d2) - PENALTY * sum(max(0, depth_k - cap_k))
     PENALTY is large enough (>> any achievable d1+d2) that the climb
     first pays down any violation of the target stratum, then
     maximizes d1+d2 within it. Sweeping the target stratum below the
     known caps (164,102,36) is how this script deliberately explores
     configs with LOWER d3 and/or d4 than their ceiling, to see whether
     some sacrificed-deep profile beats 723's total.

Every single exact evaluation (full by_depth histogram + total) is
appended to deepsweep.jsonl, memoized in-process so no config is ever
evaluated twice in one run (and evals persist across resumed runs via
--out preload). Any total > 723 is printed immediately with
'*** NEW RECORD ***' and appended to deepsweep_RECORD_BEATEN.flag.

Runs entirely on the validated ./cube_regions binary; never touches
exact_search_results.jsonl, six_cube_search_results.md, or README.md.

Usage:
  python3 deepsweep.py [--workers 4] [--max-iters 60] [--strata-iters 100]
                        [--restarts 20] [--out deepsweep.jsonl]
                        [--objectives d1d2,total,d1] [--smoke-test]
"""
import argparse
import json
import math
import os
import random
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.join(HERE, 'cube_regions')
RECORD_FLAG = os.path.join(HERE, 'deepsweep_RECORD_BEATEN.flag')

RECORD_723 = [[4, 1, 1, -1], [3, 3, 7, 3], [5, -1, -5, -5],
              [2, 1, 1, 1], [1, 1, 1, 1], [5, 2, 2, 2]]
RECORD_717 = [[5, 2, 2, 2], [-2, -2, 2, 5], [-2, 5, -2, 2],
              [-2, 2, 5, -2], [2, 1, 1, 1], [1, 0, 0, 0]]

CAPS = {1: 224, 2: 222, 3: 164, 4: 102, 5: 36, 6: 1}  # observed/known ceilings, for reference only

# The deep-profile strata to sweep from 723, per the task spec: saturated
# caps, then progressively sacrificing d4 and/or d3 below their ceilings.
STRATA = [
    (164, 102, 36),  # full saturation -- does unconstrained-deep d1+d2 beat 723's?
    (164, 96, 36),   # 723's own profile
    (158, 102, 36),  # 717's own profile
    (158, 96, 36),   # both sacrificed, 717-ish depth
    (150, 102, 36),  # deeper d3 sacrifice alone
    (150, 96, 36),   # both sacrificed, deeper
    (164, 90, 36),   # deeper d4-only sacrifice
    (140, 102, 36),  # much deeper d3-only sacrifice
    (164, 102, 30),  # d5 sacrifice alone
    (130, 80, 36),   # aggressive joint sacrifice
]


# ---------------------------------------------------------------- canon --

def canon(quats):
    """Canonical form: per-quat gcd reduction + sign fix (q and -q are the
    same rotation). Matches phase_b_hillclimb.py's canon() exactly, so
    memoization/dedup is consistent with the rest of the project's logs."""
    out = []
    for q in quats:
        g = math.gcd(*[abs(c) for c in q])
        if g > 1:
            q = [c // g for c in q]
        else:
            q = list(q)
        for c in q:
            if c != 0:
                if c < 0:
                    q = [-x for x in q]
                break
        out.append(tuple(q))
    return tuple(out)


def quats_str(quats):
    return ';'.join(','.join(str(c) for c in q) for q in quats)


def evaluate(quats):
    try:
        out = subprocess.run([BIN, '--quats', quats_str(quats)],
                              capture_output=True, text=True, timeout=120)
        r = json.loads(out.stdout.strip())
        if 'error' in r:
            return None
        return r
    except Exception:
        return None


def bd_int(r):
    return {int(k): v for k, v in r['by_depth'].items()}


# ------------------------------------------------------------ Evaluator --

class Evaluator:
    """Memoized parallel evaluator; logs every NEW evaluation to
    deepsweep.jsonl (flushed after every batch, so a killed/crashed run
    keeps all results up to the last completed neighbor batch)."""

    def __init__(self, workers, logf, preload=None):
        self.pool = ThreadPoolExecutor(max_workers=workers)
        self.memo = {}
        self.logf = logf
        self.evals = 0
        self.best_total = 0
        self.best_d1d2 = (0, None)
        self.best_d1 = (0, None)
        if preload and os.path.exists(preload):
            for line in open(preload):
                try:
                    r = json.loads(line)
                except json.JSONDecodeError:
                    continue
                k = tuple(tuple(q) for q in r['quats'])
                if 'bounded' in r:
                    self.memo[k] = {'bounded': r['bounded'],
                                    'by_depth': r['by_depth']}
                    self._track(k, self.memo[k])
                else:
                    self.memo[k] = None
            print(f'preloaded {len(self.memo)} memoized evals', flush=True)

    def _track(self, k, r):
        if r is None:
            return
        bd = bd_int(r)
        tot = r['bounded']
        if tot > self.best_total:
            self.best_total = tot
        d1d2 = bd.get(1, 0) + bd.get(2, 0)
        if d1d2 > self.best_d1d2[0]:
            self.best_d1d2 = (d1d2, k)
        if bd.get(1, 0) > self.best_d1[0]:
            self.best_d1 = (bd.get(1, 0), k)
        if tot > 723:
            print(f'*** NEW RECORD *** total={tot} quats={list(map(list, k))} '
                  f'by_depth={bd}', flush=True)
            with open(RECORD_FLAG, 'a') as fl:
                fl.write(json.dumps({'quats': list(map(list, k)),
                                      'bounded': tot, 'by_depth': r['by_depth']}) + '\n')

    def eval_many(self, quats_list, tag):
        keys = [canon(q) for q in quats_list]
        todo = []
        seen_now = set()
        for k in keys:
            if k not in self.memo and k not in seen_now:
                seen_now.add(k)
                todo.append(k)
        results = list(self.pool.map(lambda k: evaluate(list(map(list, k))),
                                      todo))
        for k, r in zip(todo, results):
            self.memo[k] = r
            self.evals += 1
            self._track(k, r)
            if r is not None:
                rec = {'quats': [list(q) for q in k],
                       'bounded': r['bounded'], 'by_depth': r['by_depth'],
                       'tag': tag}
                self.logf.write(json.dumps(rec) + '\n')
            else:
                self.logf.write(json.dumps(
                    {'quats': [list(q) for q in k], 'error': 'degenerate',
                     'tag': tag}) + '\n')
        self.logf.flush()
        return [self.memo[k] for k in keys]


# ------------------------------------------------------------- scorers --

def scorer_total(r):
    return float(r['bounded'])


def scorer_d1(r):
    return float(bd_int(r).get(1, 0))


def scorer_d1d2(r):
    bd = bd_int(r)
    return float(bd.get(1, 0) + bd.get(2, 0))


def scorer_stratum(d3cap, d4cap, d5cap, penalty=1000.0):
    def f(r):
        bd = bd_int(r)
        d1d2 = bd.get(1, 0) + bd.get(2, 0)
        viol = (max(0, bd.get(3, 0) - d3cap) + max(0, bd.get(4, 0) - d4cap)
                + max(0, bd.get(5, 0) - d5cap))
        return d1d2 - penalty * viol
    return f


PLAIN_OBJECTIVES = {'total': scorer_total, 'd1': scorer_d1, 'd1d2': scorer_d1d2}


# ------------------------------------------------------------ movement --

def neighbors(quats):
    """All single-component +-1/+-2 integer moves (re-gcd'd, |c|<=512).
    Identical move set to phase_b_hillclimb.py / symmetry_search2.py."""
    out = []
    for i in range(6):
        for j in range(4):
            for d in (-2, -1, 1, 2):
                q = [list(x) for x in quats]
                q[i][j] += d
                if all(c == 0 for c in q[i]):
                    continue
                cq = canon(q)
                if any(abs(c) > 512 for qq in cq for c in qq):
                    continue
                out.append([list(x) for x in cq])
    return out


def perturb(quats, nmoves, rng):
    q = [list(x) for x in quats]
    for _ in range(nmoves):
        i, j = rng.randrange(6), rng.randrange(4)
        q[i][j] += rng.choice((-2, -1, 1, 2))
        if all(c == 0 for c in q[i]):
            q[i][j] += 1
    cq = canon(q)
    if any(abs(c) > 512 for qq in cq for c in qq):
        return None
    return [list(x) for x in cq]


def climb(ev, start_quats, scorer, tag, max_iters):
    cur = [list(q) for q in canon(start_quats)]
    r = ev.eval_many([cur], tag + ':start')[0]
    if r is None:
        print(f'  {tag}: start config degenerate, skipping', flush=True)
        return None, None
    cur_score = scorer(r)
    cur_r = r
    it = 0
    while it < max_iters:
        it += 1
        nbrs = neighbors(cur)
        results = ev.eval_many(nbrs, tag + f':it{it}')
        best_i, best_score = -1, cur_score
        for i, rr in enumerate(results):
            if rr is None:
                continue
            s = scorer(rr)
            if s > best_score:
                best_i, best_score = i, s
        if best_i < 0:
            break
        cur = nbrs[best_i]
        cur_score = best_score
        cur_r = results[best_i]
    bd = bd_int(cur_r)
    print(f'  {tag}: converged it={it} total={cur_r["bounded"]} '
          f'by_depth={dict(sorted(bd.items()))} score={cur_score:.1f}',
          flush=True)
    return cur, cur_r


# --------------------------------------------------------------- starts --

def load_starts(rng, n_random):
    starts = [('record723', RECORD_723), ('record717', RECORD_717)]
    gpath = os.path.join(HERE, 'groebner_solutions.json')
    if os.path.exists(gpath):
        g = json.load(open(gpath))
        base5 = g['base5']
        for i, aq in enumerate(g['Aquats']):
            starts.append((f'groebner_aq{i}', base5 + [aq]))
    # ~20 random restarts: perturbations of the two known records at
    # varying strength, so the restarts probe different basins without
    # being pure noise (which the C++ engine calls "generic" and which
    # tops out around 635 per PROJECT.md section 4).
    strengths = [2, 3, 4, 5, 6, 8, 10, 12]
    bases = [('723', RECORD_723), ('717', RECORD_717)]
    count = 0
    bi = 0
    si = 0
    while count < n_random:
        bname, bq = bases[bi % len(bases)]
        strength = strengths[si % len(strengths)]
        pq = perturb(bq, strength, rng)
        bi += 1
        si += 1
        if pq is None:
            continue
        starts.append((f'random_{bname}_s{strength}_{count}', pq))
        count += 1
    return starts


# ---------------------------------------------------------------- main --

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--workers', type=int, default=4)
    ap.add_argument('--max-iters', type=int, default=60)
    ap.add_argument('--strata-iters', type=int, default=100)
    ap.add_argument('--restarts', type=int, default=20)
    ap.add_argument('--out', default='deepsweep.jsonl')
    ap.add_argument('--objectives', default='d1d2,total,d1')
    ap.add_argument('--smoke-test', action='store_true',
                     help='tiny run (2 starts, 3 iters) to validate wiring')
    args = ap.parse_args()

    if args.workers > 4:
        print(f'WARNING: capping workers at 4 (project hard rule), '
              f'requested {args.workers}', flush=True)
        args.workers = 4

    rng = random.Random(20260712)
    t0 = time.time()

    logf = open(os.path.join(HERE, args.out), 'a')
    ev = Evaluator(args.workers, logf, preload=os.path.join(HERE, args.out))

    if args.smoke_test:
        starts = [('record723', RECORD_723), ('record717', RECORD_717)]
        objs = ['d1d2']
        max_iters = 3
        strata = STRATA[:1]
        strata_iters = 3
    else:
        starts = load_starts(rng, args.restarts)
        objs = args.objectives.split(',')
        max_iters = args.max_iters
        strata = STRATA
        strata_iters = args.strata_iters

    print(f'=== deepsweep: {len(starts)} starts x {len(objs)} plain '
          f'objectives + {len(strata)} strata ===', flush=True)

    champions = {}  # obj_name -> (quats, r, score)

    def consider(obj_name, scorer, q, r):
        if r is None:
            return
        s = scorer(r)
        cur = champions.get(obj_name)
        if cur is None or s > cur[2]:
            champions[obj_name] = (q, r, s)

    # --- 1. plain objectives from every start ---
    for obj_name in objs:
        scorer = PLAIN_OBJECTIVES[obj_name]
        for sname, sq in starts:
            tag = f'{sname}:{obj_name}'
            q, r = climb(ev, sq, scorer, tag, max_iters)
            consider(obj_name, scorer, q, r)
        best = champions.get(obj_name)
        if best:
            print(f'-- objective {obj_name} champion: total={best[1]["bounded"]} '
                  f'by_depth={dict(sorted(bd_int(best[1]).items()))}', flush=True)

    # --- 2. deep-sacrifice stratum sweep, from 723 (and 717 for two extra) --
    stratum_results = {}  # (d3cap,d4cap,d5cap) -> (quats, r, score)
    strata_starts = [('record723', RECORD_723), ('record717', RECORD_717)]
    for caps in strata:
        scorer = scorer_stratum(*caps)
        best_here = None
        for sname, sq in strata_starts:
            tag = f'stratum{caps}:{sname}'
            q, r = climb(ev, sq, scorer, tag, strata_iters)
            if r is None:
                continue
            s = scorer(r)
            if best_here is None or s > best_here[2]:
                best_here = (q, r, s)
            consider(f'stratum{caps}', scorer, q, r)
        if best_here:
            stratum_results[caps] = best_here
            bd = bd_int(best_here[1])
            print(f'-- stratum {caps} best: total={best_here[1]["bounded"]} '
                  f'd1+d2={bd.get(1,0)+bd.get(2,0)} by_depth={dict(sorted(bd.items()))}',
                  flush=True)

    elapsed = time.time() - t0
    print(f'\n=== SUMMARY (elapsed {elapsed:.0f}s, {ev.evals} exact evals) ===',
          flush=True)
    print(f'overall best total seen: {ev.best_total}', flush=True)
    print(f'overall best d1+d2 seen: {ev.best_d1d2[0]}', flush=True)
    print(f'overall best d1 seen: {ev.best_d1[0]}', flush=True)
    for obj_name, (q, r, s) in champions.items():
        print(f'CHAMPION {obj_name}: total={r["bounded"]} score={s:.1f} '
              f'by_depth={dict(sorted(bd_int(r).items()))} quats={q}', flush=True)
    print('DONE', flush=True)
    logf.close()


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] in ('-h', '--help'):
        print(__doc__ or __file__)
        raise SystemExit(0)
    main()
