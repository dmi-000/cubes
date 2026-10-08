#!/usr/bin/env python3
"""Falsification climb for the per-cube pattern of [P423]:  #D({i}) <= 20 + 2 a_i ?

[P423] saw per-cube d1 = 20 + 2 a_i (a_i = body diagonals cube i shares with the others) on every
top-d1 row, but never with a_i = 0 near any cap. Here climbs push the EXCESS

    x(C) = max_i ( #D({i}) - 2 a_i )

and stop at x > 20, which refutes the pattern. If it survives, the measured envelope per a_i is
reported, a lower bound as every search is.

**Counts.** The c_level engine's per-label counts in the generic frame (3,1,1,1) (single-bit labels
are the per-cube sets). The engine is frame-dependent on shared-face-plane compounds ([P419]), so
those are rejected. Each run's best, and every compound with x >= 20, is recounted with
sphere_count.

**Starts** (the advisor's hard cases):
- `n3sub`: the n = 3 record subset, its three cubes at [P401]'s n = 3 cap 16 with no sharing, plus
  a random fourth cube.
- `nudged`: the 183 record with the hub perturbed off its three shared axes, so the leaves have
  a_i = 0 and must fall to 20 or below.
- `record`: the record itself; can a leaf with a_i = 1 pass 22?
- `random`.

**Moves.** One coordinate of one quaternion by +-1..+-3, or a quaternion doubled before the step
(refinement). Accept if (x, sum of excesses) does not decrease.

**`--sum`**: the milestone test instead. Climb d1 itself (tie-break: total), from the same starts
plus the 96 four-cycle of [P423]. Nothing rational on file has d1 from 97 to 103; any rational
compound with d1 >= 97 refutes "d1 >= 97 only at the golden" (the golden is in Q(sqrt5)).
Cache: data/d1_sum_climb_cache.jsonl. Output: data/d1_sum_climb.json.

**`--table`**: the summed form `d1 <= 80 + 4s` (s = shared body diagonals) over BOTH climbs'
caches: the largest `d1 − 4s` for each s, with its witness. Engine counts; the s = 0 witness is
recounted by `d1_gap.py --extra`. Output: data/d1_sum_table.json.

Cache: data/d1_cap_climb_cache.jsonl. Output: data/d1_cap_climb.json.
"""
import os, sys, json, random, collections, multiprocessing as mp
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..'))
import c_level as CL
from depth2_charging import qmul
from d1_gap import sharing, measure
from frontier_n4 import DATA

GENERIC = (3, 1, 1, 1)
RECORD = [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5), (1, 1, 1, 1)]
STEPS = 1500
SUM = '--sum' in sys.argv
CACHE = os.path.join(DATA, 'd1_sum_climb_cache.jsonl' if SUM else 'd1_cap_climb_cache.jsonl')
OUT = os.path.join(DATA, 'd1_sum_climb.json' if SUM else 'd1_cap_climb.json')
# a 96 four-cycle from data/d1_gap.json; loaded at import so spawned workers see it
CYCLE4 = (next(r['qs'] for r in json.load(open(os.path.join(DATA, 'd1_gap.json')))['rows']
               if r['bd']['1'] == 96) if SUM else None)


def key(qs):
    return ';'.join(','.join(map(str, q)) for q in qs)


def evaluate(qs):
    planes, axes = sharing(qs, F(1))
    if planes:
        return None
    try:
        e = CL.engine([qmul(GENERIC, q) for q in qs])
    except Exception:
        return None
    if 'per_label' not in e:
        return None
    pc = [e['per_label'].get(str(1 << i), 0) for i in range(4)]
    if sum(pc) != e['by_depth']['1']:
        return None
    a = [sum(i in P for P in axes) for i in range(4)]
    ex = [p - 2 * ai for p, ai in zip(pc, a)]
    return {'pc': pc, 'a': a, 'ex': ex, 'x': max(ex), 'total': e['bounded'], 'd1': sum(pc)}


def score(m):
    return (m['d1'], m['total']) if SUM else (m['x'], sum(m['ex']))


def hit(m):
    return m['d1'] >= 97 if SUM else m['x'] > 20


def move(rnd, qs):
    qs = [list(q) for q in qs]
    i = rnd.randrange(4)
    if rnd.random() < 0.1:
        qs[i] = [2 * c for c in qs[i]]
    j = rnd.randrange(4)
    qs[i][j] += rnd.choice((-3, -2, -1, 1, 2, 3))
    if not any(qs[i]):
        qs[i][j] = 1
    return [tuple(q) for q in qs]


def start(rnd, kind):
    if kind == 'n3sub':
        return RECORD[:3] + [tuple(rnd.randint(-7, 7) or 1 for _ in range(4))]
    if kind == 'nudged':
        h = list(RECORD[3])
        h[rnd.randrange(4)] += rnd.choice((-1, 1))
        return RECORD[:3] + [tuple(h)]
    if kind == 'record':
        return list(RECORD)
    if kind == 'cycle4':
        return [tuple(q) for q in CYCLE4]
    return [tuple(rnd.randint(-7, 7) or 1 for _ in range(4)) for _ in range(4)]


def run(args):
    kind, seed = args
    rnd = random.Random(seed)
    cur = start(rnd, kind)
    m = evaluate(cur)
    while m is None:
        cur = move(rnd, cur)
        m = evaluate(cur)
    best, bm = cur, m
    log = []
    hits = []
    for step in range(STEPS):
        nxt = move(rnd, cur)
        nm = evaluate(nxt)
        if nm is None:
            continue
        log.append((key(nxt), nm))
        if hit(nm):
            hits.append((nxt, nm))
        if score(nm) >= score(m):
            cur, m = nxt, nm
            if score(m) > score(bm):
                best, bm = cur, m
    env = collections.defaultdict(int)
    for k, mm in log:
        for p, ai in zip(mm['pc'], mm['a']):
            env[ai] = max(env[ai], p)
    return {'kind': kind, 'seed': seed, 'best': best, 'bm': bm, 'hits': hits[:5],
            'envelope': dict(env), 'evaluated': len(log)}, log


def main():
    kinds = ('cycle4', 'record', 'n3sub', 'random') if SUM else ('n3sub', 'nudged', 'record', 'random')
    jobs = [(k, s) for k in kinds for s in range(4)]
    res = []
    with mp.Pool(8) as p, open(CACHE, 'a') as fc:
        for r, log in p.imap_unordered(run, jobs):
            for k, mm in log:
                fc.write(json.dumps({'k': k, 'm': mm}) + '\n')
            res.append(r)
            print('%-7s seed %d  evaluated %4d  best x %d  per-cube %s a %s total %d  hits %d  envelope %s'
                  % (r['kind'], r['seed'], r['evaluated'], r['bm']['x'], r['bm']['pc'], r['bm']['a'],
                     r['bm']['total'], len(r['hits']), sorted(r['envelope'].items())), flush=True)
    # exact recount of every run's best and of every hit
    tocheck = {key(r['best']): r['best'] for r in res}
    for r in res:
        for q, _ in r['hits']:
            tocheck[key(q)] = q
    with mp.Pool(8) as p:
        sc = dict(zip(tocheck, p.map(measure, [tuple(map(tuple, q)) for q in tocheck.values()])))
    agree = 0
    for r in res:
        s = sc[key(r['best'])]
        r['sphere'] = {'per_cube': s['per_cube'], 'total': s['total']}
        agree += s['per_cube'] == r['bm']['pc']
    if SUM:
        refuting = [k for k, s in sc.items() if s['bd'][1] >= 97]
    else:
        refuting = [k for k, s in sc.items()
                    if any(p - 2 * sum(i in P for P in s['shared_axes']) > 20 for i, p in enumerate(s['per_cube']))]
    env = collections.defaultdict(int)
    for r in res:
        for ai, p in r['envelope'].items():
            env[int(ai)] = max(env[int(ai)], p)
    print('sphere_count agrees on per-cube d1 for %d of %d run-bests' % (agree, len(res)))
    print('best d1 per run (engine): %s' % sorted(r['bm']['d1'] for r in res))
    print('engine hits (%s): %d; confirmed by sphere_count: %d' % ('d1 >= 97' if SUM else 'x > 20', sum(len(r['hits']) for r in res), len(refuting)))
    print('envelope, max per-cube d1 by a_i (engine): %s' % sorted(env.items()))
    json.dump({'runs': res, 'sphere_agree': agree, 'refuting_sphere': refuting, 'envelope': env},
              open(OUT, 'w'), indent=1, default=str)


def table():
    mx, cnt = {}, collections.Counter()
    for f in ('d1_cap_climb_cache.jsonl', 'd1_sum_climb_cache.jsonl'):
        for l in open(os.path.join(DATA, f)):
            r = json.loads(l)
            m = r['m']
            d1 = sum(m['pc'])
            s = sum(m['a']) // 2
            cnt[s] += 1
            if s not in mx or d1 - 4 * s > mx[s]['excess']:
                mx[s] = {'excess': d1 - 4 * s, 'k': r['k'], 'pc': m['pc'], 'a': m['a'], 'total': m['total']}
    print('evaluated %d; by s: %s' % (sum(cnt.values()), dict(sorted(cnt.items()))))
    for s in sorted(mx):
        print('  s %d  max d1 - 4s = %d  %s' % (s, mx[s]['excess'], mx[s]))
    json.dump({'count': cnt, 'max': mx}, open(os.path.join(DATA, 'd1_sum_table.json'), 'w'), indent=1)


if __name__ == '__main__':
    table() if '--table' in sys.argv else main()
