#!/usr/bin/env python3
"""The per-compound oracle, sharpened: patches counted per sharing CLASS, all eight structures.
[P421]

shared_oracle ([P418]) predicted `d2 <= Σ_S d2(S) + Σ_S p_S − 6` with `p_S = 2` per sharing PAIR
in each triple.
- That overcounts axis structures: an axis triple's own triple got 6 instead of 2, since its
  three cubes tie on ONE patch per `±n`.
- Here `p_S = 2` per sharing CLASS (the cubes on one plane) with `>= 2` members in `S`.

The prediction leaves out the hole term `Σ_Q (j_Q − 2)` and any G3 loss. So the minimum slack per
structure is an upper bound on what those terms can be in the data, and a negative slack would
show them positive there.

**Counts.** The engine in a GENERIC frame (the rotation (3,1,1,1); [P419] found the identity frame
unreliable on this locus), for each compound and its four triples. 25 random rows are re-counted
with sphere_count.

**Rows.**
- shared_plane_scope runs 1 and 2: per structure, the 60 highest `d2` and 60 more at random.
- [P411]'s climb cache: the 200 highest totals and 200 more at random.

Output: data/shared_oracle2.json.
"""
import os, sys, json, random, itertools, collections, multiprocessing as mp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import c_level as CL
from depth2_charging import qmul
from sphere_count import Compound, normals
from fractions import Fraction as F

ROOT = os.path.dirname(os.path.dirname(HERE))
GENERIC = (3, 1, 1, 1)


def eng(qs):
    e = CL.engine([qmul(GENERIC, q) for q in qs])
    return (e['bounded'], e['by_depth']) if 'by_depth' in e else (None, None)


def classes(qs):
    """sharing classes: for each shared normal (up to sign), the set of cubes having it"""
    nv = [normals(q, F(1)) for q in qs]
    out = {}
    for i, j in itertools.combinations(range(len(qs)), 2):
        for u in nv[i]:
            for v in nv[j]:
                for s in (1, -1):
                    if all(a == s * b for a, b in zip(u, v)):
                        key = tuple(u) if u > [-c for c in u] else tuple(-c for c in u)
                        out.setdefault(key, set()).update((i, j))
    return [sorted(c) for c in out.values()]


def structure(cls):
    sizes = sorted(len(c) for c in cls)
    deg = collections.Counter(x for c in cls for x in c)
    if not cls:
        return 'none'
    if sizes == [2]:
        return 'pair'
    if sizes == [3]:
        return 'axis3'
    if sizes == [4]:
        return 'axis4'
    if sizes == [2, 3]:
        return 'axis3+pair'
    if sizes == [2, 2]:
        return 'hub' if max(deg.values()) == 2 else 'two_disjoint'
    if sizes == [2, 2, 2]:
        return 'star' if max(deg.values()) == 3 else 'path'
    return 'other:' + str(cls)


def measure(qs):
    t, bd = eng(qs)
    if t is None:
        return None
    d2S = []
    for S in itertools.combinations(range(4), 3):
        ts, bs = eng([qs[i] for i in S])
        if ts is None:
            return None
        d2S.append(bs['2'])
    cls = classes(qs)
    pS = [2 * sum(1 for c in cls if len(set(c) & set(S)) >= 2) for S in itertools.combinations(range(4), 3)]
    pred = sum(d2S) + sum(pS) - 6
    return {'qs': qs, 'structure': structure(cls), 'd2': bd['2'], 'd2S': d2S, 'pS': pS,
            'pred': pred, 'slack': pred - bd['2'], 'total': t}


def parse(k):
    return [tuple(map(int, g.split(','))) for g in k.split(';')]


def main():
    rnd = random.Random(421)
    keys = []
    by = collections.defaultdict(list)
    for line in open(os.path.join(ROOT, 'data', 'shared_plane_scope_cache.jsonl')):
        try:
            r = json.loads(line)
        except ValueError:
            continue
        if 'error' not in r['m']:
            by[len(r['m']['pairs'])].append((r['m']['bd']['2'], r['k']))
    for lst in by.values():
        lst = sorted(set(lst), reverse=True)
        keys += [k for _, k in lst[:60]] + [k for _, k in rnd.sample(lst[60:], min(60, len(lst) - 60))]
    climb = {}
    for line in open(os.path.join(ROOT, 'data', 'shared_plane_climb_cache.jsonl')):
        try:
            r = json.loads(line)
        except ValueError:
            continue
        if r.get('t') is not None:
            climb[r['k']] = r['t']
    ck = sorted(climb, key=lambda k: -climb[k])
    keys += ck[:200] + rnd.sample(ck[200:], 200)
    jobs = [parse(k) for k in dict.fromkeys(keys)]
    with mp.Pool(8) as p:
        res = p.map(measure, jobs)
    unev = sum(r is None for r in res)
    res = [r for r in res if r]
    g = collections.defaultdict(list)
    for r in res:
        g[r['structure']].append(r)
    for s in sorted(g):
        rs = g[s]
        sl = collections.Counter(r['slack'] for r in rs)
        print('%-12s %4d rows  min slack %3d  max d2 %3d  violations %d  slack histogram %s'
              % (s, len(rs), min(sl), max(r['d2'] for r in rs), sum(r['slack'] < 0 for r in rs),
                 sorted(sl.items())))
    print('unevaluated: %d' % unev)
    sample = rnd.sample(res, 25)
    ok = 0
    for r in sample:
        t, bd = Compound(r['qs']).count()
        ok += bd[2] == r['d2']
    print('sphere_count d2 re-count: %d of 25 agree' % ok)
    json.dump({'rows': res, 'unevaluated': unev, 'sphere_count_agree': ok},
              open(os.path.join(ROOT, 'data', 'shared_oracle2.json'), 'w'), indent=1, default=str)


if __name__ == '__main__':
    main()
