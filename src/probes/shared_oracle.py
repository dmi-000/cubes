#!/usr/bin/env python3
"""The sharp per-compound oracle for PROOF_SHARED's charging chain.  [P418]

PROOF_SHARED §4's chain, before the band and patch terms are dropped, says

    d2  <=  sum_S d2(S) + sum_S p_S - 6,

with p_S = 2 for each triple containing a sharing pair. For exactly one sharing pair, sum_S p_S = 4,
so d2 <= sum_S d2(S) - 2.
- The headline 62 against an observed 54 tests nothing. This tests the chain per compound.
- One violation means a hole in the charging or in the band step, whatever the circle model says.
- For two or more sharing pairs the analogue, with p_S = 2 per (triple, sharing pair in it), is
  exploratory. That case is not derived (PROOF_SHARED §5).

**Data.**
- Single pair: [P411]'s climb cache, the 200 highest totals and 200 more at random.
- Several pairs: shared_plane_scope's cache, the 60 highest d2 per sharing structure and 60 more at
  random.

**Counter.** The engine, retried under rotations, for the compound and its four triples. 25 rows,
chosen at random, are re-counted with sphere_count, and any disagreement is reported.
Output: data/shared_oracle.json.
"""
import os, sys, json, random, itertools, collections, multiprocessing as mp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
from degenerate_counts import total
from shared_plane_scope import shared
from sphere_count import Compound

ROOT = os.path.dirname(os.path.dirname(HERE))


def parse(k):
    return [tuple(map(int, g.split(','))) for g in k.split(';')]


def measure(qs):
    t, bd = total(qs)
    if t is None:
        return None
    d2S = []
    for S in itertools.combinations(range(4), 3):
        ts, bs = total([qs[i] for i in S])
        if ts is None:
            return None
        d2S.append(bs['2'])
    pairs = [(i, j) for i, j in itertools.combinations(range(4), 2) if shared(qs[i], qs[j]) == 1]
    psum = sum(2 for S in itertools.combinations(range(4), 3) for (i, j) in pairs if i in S and j in S)
    pred = sum(d2S) + psum - 6
    return {'qs': qs, 'd2': bd['2'], 'd2S': d2S, 'pairs': pairs, 'sum_pS': psum,
            'pred': pred, 'slack': pred - bd['2'], 'total': t}


def crosscheck(r):
    t, bd = Compound(r['qs']).count()
    d2S = [Compound([r['qs'][i] for i in S]).count()[1][2] for S in itertools.combinations(range(4), 3)]
    return bd[2] == r['d2'] and d2S == r['d2S']


def main():
    rnd = random.Random(418)
    rows = {}
    for line in open(os.path.join(ROOT, 'data', 'shared_plane_climb_cache.jsonl')):
        try:
            r = json.loads(line)
        except ValueError:
            continue
        if r.get('t') is not None:
            rows[r['k']] = r['t']
    keys = sorted(rows, key=lambda k: -rows[k])
    single = keys[:200] + rnd.sample(keys[200:], 200)
    by_struct = collections.defaultdict(list)
    for line in open(os.path.join(ROOT, 'data', 'shared_plane_scope_cache.jsonl')):
        try:
            r = json.loads(line)
        except ValueError:
            continue
        m = r['m']
        if 'error' in m:
            continue
        by_struct[len(m['pairs'])].append((m['bd']['2'], r['k']))
    multi = []
    for s, lst in by_struct.items():
        lst = sorted(set(lst), reverse=True)
        multi += [k for _, k in lst[:60]] + [k for _, k in rnd.sample(lst[60:], min(60, len(lst[60:])))]
    jobs = [parse(k) for k in single + multi]
    with mp.Pool(8) as p:
        res = p.map(measure, jobs)
    unev = sum(r is None for r in res)
    res = [r for r in res if r]
    groups = collections.defaultdict(list)
    for r in res:
        groups[len(r['pairs'])].append(r)
    for g in sorted(groups):
        rs = groups[g]
        sl = collections.Counter(r['slack'] for r in rs)
        worst = min(rs, key=lambda r: r['slack'])
        print('%d sharing pair(s): %d rows; slack histogram %s; violations %d; max d2 %d; tightest %s'
              % (g, len(rs), sorted(sl.items()), sum(r['slack'] < 0 for r in rs),
                 max(r['d2'] for r in rs), {k: worst[k] for k in ('qs', 'd2', 'd2S', 'sum_pS')}))
    print('unevaluated:', unev)
    sample = rnd.sample(res, 25)
    with mp.Pool(8) as p:
        ok = p.map(crosscheck, sample)
    print('sphere_count crosscheck: %d of %d agree' % (sum(ok), len(ok)))
    json.dump({'rows': res, 'unevaluated': unev, 'crosscheck_agree': sum(ok), 'crosscheck_n': len(ok)},
              open(os.path.join(ROOT, 'data', 'shared_oracle.json'), 'w'), indent=1, default=str)


if __name__ == '__main__':
    main()
