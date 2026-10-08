#!/usr/bin/env python3
"""The n = 5 chain as an oracle on shared-plane compounds.  [P433]

Without a shared face plane, [P425]–[P430] give two statements (up to component terms):
- L2-total: `d2 + d4 <= Σ_tri d2(S) − 16 − [Σ_tri (c_S − 1) − (c2 − 1) − (c4 − 1)]`;
- L3-total: `d3 + d4 <= Σ_4 d3(S) − 6 − [Σ_4 (c'_S − 1) − (c3 − 1) − (c4 − 1)]`.

The bracketed component terms are >= −(c4 − 1) by L2/L3 (each bracket ends in −(c4 − 1), which L2/L3
do not control; corrected 2026-10-06), and the H1 slack is >= 0. So the generic PREDICTIONS
`Σ_tri d2(S) − 16 − (d2 + d4)` and `Σ_4 d3(S) − 6 − (d3 + d4)` are >= −(c4 − 1) there, and >= 0
when c4 = 1.

With a shared face plane, two-dimensional tie patches change the accounting, as at n = 4 ([P418],
[P421]). This measures the two predicted slacks on shared-plane compounds. A negative value is the
size of the patch correction a proof must supply. They are compared with the anchor caps the
sharing lowers:
- `d2(S) <= 14` for triples containing the pair;
- `d3(S) <= 20` for 4-subsets containing it;
- `d4 <= 26`.

**Counts.** The engine in the generic frame (3,1,1,1), for the compound and its 15 subsets.
Shared-plane compounds: the cache of [P432]. Control: rows with no shared plane, where both slacks
must be >= 0.

Output: data/shared_n5_oracle.json.
"""
import os, sys, json, random, itertools, collections, multiprocessing as mp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import c_level as CL
from depth2_charging import qmul
from shared_n5_scope import classes

ROOT = os.path.dirname(os.path.dirname(HERE))
GENERIC = (3, 1, 1, 1)


def eng(qs):
    e = CL.engine([qmul(GENERIC, q) for q in qs])
    return e['by_depth'] if 'by_depth' in e else None


def measure(qs):
    qs = [tuple(q) for q in qs]
    bd = eng(qs)
    if bd is None:
        return None
    tri, four = [], []
    for S in itertools.combinations(range(5), 3):
        b = eng([qs[i] for i in S])
        if b is None:
            return None
        tri.append((S, b['2']))
    for S in itertools.combinations(range(5), 4):
        b = eng([qs[i] for i in S])
        if b is None:
            return None
        four.append((S, b['3']))
    d = {k: bd[str(k)] for k in range(1, 6)}
    cl = classes(qs)
    return {'qs': qs, 'd': d, 'total': sum(d.values()), 'classes': cl,
            'tri': tri, 'four': four,
            'slack24': sum(x for _, x in tri) - 16 - (d[2] + d[4]),
            'slack34': sum(x for _, x in four) - 6 - (d[3] + d[4])}


def main():
    rnd = random.Random(433)
    rows = [json.loads(l) for l in open(os.path.join(ROOT, 'data', 'shared_n5_scope_cache.jsonl'))]
    rows.sort(key=lambda r: -r['total'])
    keys, seen = [], set()
    for r in rows:
        k = json.dumps(r['qs'])
        if k not in seen:
            seen.add(k); keys.append(r['qs'])
    pick = keys[:150] + rnd.sample(keys[150:], min(450, len(keys) - 150))
    ctrl = []
    for l, _ in zip(open(os.path.join(ROOT, 'data', 'campaign_n5.jsonl')), range(80)):
        ctrl.append(json.loads(l)['quats'])
    with mp.Pool(8) as p:
        res = p.map(measure, pick + ctrl)
    sh = [r for r in res[:len(pick)] if r]
    co = [r for r in res[len(pick):] if r and not CL.shares_plane(r['qs'])]
    unev = sum(r is None for r in res)
    print('shared-plane rows %d, control rows %d, unevaluated %d' % (len(sh), len(co), unev))
    for name, rs in (('control (no shared plane)', co), ('shared plane', sh)):
        print('%s: slack24 %s' % (name, sorted(collections.Counter(r['slack24'] for r in rs).items())))
        print('%s: slack34 %s' % (name, sorted(collections.Counter(r['slack34'] for r in rs).items())))
    # per-subset caps in the shared rows
    pairs = collections.Counter()
    mx_in, mx_out = collections.Counter(), collections.Counter()
    for r in sh:
        cl = [set(c) for c in r['classes']]
        for S, v in r['tri']:
            inside = any(len(c & set(S)) >= 2 for c in cl)
            mx_in['tri'] = max(mx_in['tri'], v) if inside else mx_in['tri']
            mx_out['tri'] = max(mx_out['tri'], v) if not inside else mx_out['tri']
        for S, v in r['four']:
            inside = any(len(c & set(S)) >= 2 for c in cl)
            mx_in['four'] = max(mx_in['four'], v) if inside else mx_in['four']
            mx_out['four'] = max(mx_out['four'], v) if not inside else mx_out['four']
        pairs[str(r['classes'])] += 1
    print('max subset counts, subsets containing a sharing class: %s; not containing: %s' % (dict(mx_in), dict(mx_out)))
    print('max d4 on shared rows: %d; structures %s' % (max(r['d'][4] for r in sh), dict(pairs)))
    json.dump({'shared': sh, 'control': co, 'unevaluated': unev},
              open(os.path.join(ROOT, 'data', 'shared_n5_oracle.json'), 'w'), indent=1, default=str)


if __name__ == '__main__' and '--recount' not in sys.argv:
    main()


def _sc(args):
    from sphere_count import Compound
    qs, l = args
    t, bd = Compound([tuple(q) for q in qs]).count()
    return bd[l]


def recount(k=24):
    """frame-free recount (sphere_count) of the subset counts that set the budget: k triples and k
    4-subsets containing the sharing pair {0, 1}, from the highest-total rows.
    Output: data/shared_n5_oracle_recount.json (the oracle's own file is left as written)."""
    d = json.load(open(os.path.join(ROOT, 'data', 'shared_n5_oracle.json')))
    rows = sorted(d['shared'], key=lambda r: -r['total'])
    jobs, meta = [], []
    for kind, key, l in (('tri', 'tri', 2), ('four', 'four', 3)):
        got = 0
        for r in rows:
            for S, v in r[key]:
                if 0 in S and 1 in S and got < k:
                    jobs.append(([r['qs'][i] for i in S], l)); meta.append((kind, S, v)); got += 1
                    break
    with mp.Pool(8) as p:
        res = p.map(_sc, jobs)
    diff = [(m, x) for m, x in zip(meta, res) if m[2] != x]
    print('recounted %d subset counts with sphere_count: %d differ from the engine' % (len(res), len(diff)))
    for m, x in diff[:10]:
        print('   ', m, 'sphere_count', x)
    json.dump({'n': len(res), 'jobs': [[m, x] for m, x in zip(meta, res)], 'differ': [[m, x] for m, x in diff]},
              open(os.path.join(ROOT, 'data', 'shared_n5_oracle_recount.json'), 'w'), indent=1, default=str)


if __name__ == '__main__' and '--recount' in sys.argv:
    recount()
