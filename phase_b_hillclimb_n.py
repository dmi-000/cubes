#!/usr/bin/env python3
# Working principles: NPLUS_SPEC.md. Project index: README.md
"""Phase B (n-general): exact hill-climbing on integer quaternion configs
for arbitrary cube count n. Adapted from phase_b_hillclimb.py (which stays
untouched, n=6-only, reading exact_search_results.jsonl/campaign_results
.jsonl) per NPLUS_SPEC.md section 4.

Starts from the top-K configs found in campaign_n<n>.jsonl (+ hillclimb_n
<n>_log.jsonl for resumability), applies integer component moves (add
{-2,-1,+1,+2} to one component of one quaternion, re-gcd, reject if any
|component| > 512), evaluates EXACTLY with cube_regions_n --n <n>, and
climbs greedily. Variant objectives: total, depth-1 alone, depth-2 alone.

Every evaluated config is logged with explicit quats to
hillclimb_n<n>_log.jsonl (reproducible without the seed chain).

Usage: python3 phase_b_hillclimb_n.py --n 7 [--topk 20] [--workers 8]
                                       [--objectives total,d1,d2]
                                       [--restarts 2]
"""
import argparse
import json
import math
import os
import random
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.join(HERE, 'cube_regions_n')


def canon(quats):
    """Canonical form: per-quat gcd reduction + sign (first nonzero > 0).
    q and -q are the same rotation, so fix the sign for dedup."""
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


def evaluate(n, quats):
    """Exact count via the validated C++ counter. Returns dict or None."""
    try:
        out = subprocess.run([BIN, '--n', str(n), '--quats', quats_str(quats)],
                             capture_output=True, text=True, timeout=120)
        r = json.loads(out.stdout.strip())
        if 'error' in r:
            return None
        return r
    except Exception:
        return None


class Evaluator:
    """Memoized parallel evaluator; logs every new evaluation."""

    def __init__(self, n, workers, logf, preload=None):
        self.n = n
        self.pool = ThreadPoolExecutor(max_workers=workers)
        self.memo = {}
        self.logf = logf
        self.evals = 0
        if preload and os.path.exists(preload):
            for line in open(preload):
                try:
                    r = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if 'quats' not in r:
                    continue
                k = tuple(tuple(q) for q in r['quats'])
                if 'bounded' in r:
                    self.memo[k] = {'bounded': r['bounded'],
                                    'by_depth': r['by_depth'],
                                    'per_label': r['per_label']}
                else:
                    self.memo[k] = None
            print(f'preloaded {len(self.memo)} memoized evals', flush=True)

    def eval_many(self, quats_list, tag):
        keys = [canon(q) for q in quats_list]
        todo = []
        seen_now = set()
        for k in keys:
            if k not in self.memo and k not in seen_now:
                seen_now.add(k)
                todo.append(k)
        results = list(self.pool.map(lambda k: evaluate(self.n, list(map(list, k))),
                                     todo))
        for k, r in zip(todo, results):
            self.memo[k] = r
            self.evals += 1
            if r is not None:
                rec = {'quats': [list(q) for q in k],
                       'bounded': r['bounded'], 'by_depth': r['by_depth'],
                       'per_label': r['per_label'], 'tag': tag}
                self.logf.write(json.dumps(rec) + '\n')
            else:
                self.logf.write(json.dumps(
                    {'quats': [list(q) for q in k], 'error': 'degenerate',
                     'tag': tag}) + '\n')
        self.logf.flush()
        return [self.memo[k] for k in keys]


def objective_fn(name):
    if name == 'total':
        return lambda r: r['bounded']
    if name == 'd1':
        return lambda r: (r['by_depth'].get('1', 0), r['bounded'])
    if name == 'd2':
        return lambda r: (r['by_depth'].get('2', 0), r['bounded'])
    raise ValueError(name)


def neighbors(quats, n):
    """All single-component integer moves (re-gcd'd, |c|<=512)."""
    out = []
    for i in range(n):
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


def climb(ev, n, start_quats, obj_name, tag, max_iters=200):
    obj = objective_fn(obj_name)
    cur = [list(q) for q in canon(start_quats)]
    r = ev.eval_many([cur], tag + ':start')[0]
    if r is None:
        print(f'  {tag}: start config degenerate, skipping', flush=True)
        return None, None
    cur_score = obj(r)
    cur_r = r
    it = 0
    while it < max_iters:
        it += 1
        nbrs = neighbors(cur, n)
        results = ev.eval_many(nbrs, tag + f':it{it}')
        best_i, best_score = -1, cur_score
        for i, rr in enumerate(results):
            if rr is None:
                continue
            s = obj(rr)
            if s > best_score:
                best_i, best_score = i, s
        if best_i < 0:
            break
        cur = nbrs[best_i]
        cur_score = best_score
        cur_r = results[best_i]
        print(f'  {tag} it{it}: {obj_name}={cur_score} '
              f'bounded={cur_r["bounded"]} '
              f'd={dict(sorted((int(k), v) for k, v in cur_r["by_depth"].items()))}',
              flush=True)
    return cur, cur_r


def perturb(quats, n, nmoves, rng):
    q = [list(x) for x in quats]
    for _ in range(nmoves):
        i, j = rng.randrange(n), rng.randrange(4)
        q[i][j] += rng.choice((-2, -1, 1, 2))
        if all(c == 0 for c in q[i]):
            q[i][j] += 1
    cq = canon(q)
    if any(abs(c) > 512 for qq in cq for c in qq):
        return None
    return [list(x) for x in cq]


def sim_quats_for_seed(n, seed):
    out = subprocess.run([BIN, '--n', str(n), '--seed', str(seed)],
                         capture_output=True, text=True, timeout=120)
    r = json.loads(out.stdout.strip())
    return r['quats'], r


def scan_records(n):
    """Best-known (bounded, d1, d2) per seed from campaign_n<n>.jsonl."""
    cands = {}  # seed -> dict(bounded, d1, d2)

    def add(r):
        s = r.get('seed')
        if s is None or 'bounded' not in r:
            return
        bd = {int(k): v for k, v in r.get('by_depth', {}).items()}
        cur = cands.get(s)
        rec = dict(bounded=r['bounded'], d1=bd.get(1, 0), d2=bd.get(2, 0))
        if cur is None or rec['bounded'] > cur['bounded']:
            cands[s] = rec

    import glob
    paths = [os.path.join(HERE, f'campaign_n{n}.jsonl')]
    paths += glob.glob(os.path.join(HERE, f'campaign_n{n}_shard_*.jsonl'))
    for p in paths:
        if not os.path.exists(p):
            continue
        with open(p) as f:
            for line in f:
                try:
                    add(json.loads(line))
                except json.JSONDecodeError:
                    continue  # partial trailing line of a live shard
    return cands


def top_starts(n, topk, key='bounded'):
    cands = scan_records(n)
    top = sorted(cands.items(), key=lambda kv: -kv[1][key])[:topk]
    return [(s, v[key]) for s, v in top]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, required=True)
    ap.add_argument('--topk', type=int, default=20)
    ap.add_argument('--workers', type=int, default=8)
    ap.add_argument('--objectives', default='total,d1,d2')
    ap.add_argument('--restarts', type=int, default=2)
    ap.add_argument('--out', default=None)
    ap.add_argument('--max-iters', type=int, default=200)
    args = ap.parse_args()
    n = args.n
    out_name = args.out or f'hillclimb_n{n}_log.jsonl'

    rng = random.Random(12345)
    objectives = args.objectives.split(',')
    starts = {}
    for o in objectives:
        key = {'total': 'bounded', 'd1': 'd1', 'd2': 'd2'}[o]
        k = args.topk if o == 'total' else min(args.topk, 8)
        starts[o] = top_starts(n, k, key)
        print(f'{o} starts: ' +
              ', '.join(f's{s}={b}' for s, b in starts[o]), flush=True)

    logf = open(os.path.join(HERE, out_name), 'a')
    ev = Evaluator(n, args.workers, logf, preload=os.path.join(HERE, out_name))

    champions = {o: (None, None, None) for o in objectives}

    def consider(o, q, r):
        if r is None:
            return
        s = objective_fn(o)(r)
        if champions[o][2] is None or s > champions[o][2]:
            champions[o] = (q, r, s)

    for obj_name in objectives:
        for rank, (seed, b0) in enumerate(starts[obj_name]):
            quats, _ = sim_quats_for_seed(n, seed)
            tag = f'seed{seed}:{obj_name}'
            print(f'== climb {tag} (rank {rank}, start {obj_name}={b0})',
                  flush=True)
            q, r = climb(ev, n, quats, obj_name, tag, args.max_iters)
            consider(obj_name, q, r)
            for rs in range(args.restarts):
                pq = perturb(quats, n, 4, rng)
                if pq is None:
                    continue
                tag2 = f'{tag}:restart{rs}'
                q, r = climb(ev, n, pq, obj_name, tag2, args.max_iters)
                consider(obj_name, q, r)
    print('\n=== CHAMPIONS ===', flush=True)
    for o, (q, r, s) in champions.items():
        if q is None:
            continue
        print(f'{o}: score={s} bounded={r["bounded"]} '
              f'by_depth={dict(sorted((int(k), v) for k, v in r["by_depth"].items()))}')
        print(f'  quats={q}')
    print(f'total exact evaluations: {ev.evals}', flush=True)
    logf.close()


if __name__ == '__main__':
    import sys as _sys
    if len(_sys.argv) > 1 and _sys.argv[1] in ('-h', '--help'):
        print(__doc__ or __file__); raise SystemExit(0)
    main()
