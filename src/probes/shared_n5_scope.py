#!/usr/bin/env python3
"""Five cubes with a shared face plane: how high do they count?  (Scoping the n = 5 shared-plane case.)

[P430]'s bound `max(5) <= 485` covers compounds with no shared face plane. Before building the
shared-plane argument at n = 5 (P413–P422 at n = 4), this measures what such compounds reach.

**Construction.** Cubes 0 and 1 share the face plane with normal z: q0 = (1, 0, 0, 0) and
q1 = (a, 0, 0, b). Cubes 2–4 are free. Climbs on the total move cubes 2–4 freely and q1 only
within its family, so the sharing is kept. Each compound's sharing structure is recorded. Extra
sharings that appear are allowed and labelled.

**Counts.**
- The c_level engine in the GENERIC frame (3,1,1,1), since the identity frame is unreliable on
  this locus ([P419]).
- The best of each run is recounted with sphere_count, which is frame-free.

**What it decides** (rule set before the run):
- If the bests sit well below 457, the shared-plane case at n = 5 has room, and a one-pair chain
  is worth building.
- If they come near 457, report before building anything.

Output: data/shared_n5_scope.json; cache data/shared_n5_scope_cache.jsonl.
"""
import os, sys, json, random, itertools, collections, multiprocessing as mp
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import c_level as CL
from depth2_charging import qmul
from sphere_count import Compound, normals

ROOT = os.path.dirname(os.path.dirname(HERE))
GENERIC = (3, 1, 1, 1)
STEPS = 700
CACHE = os.path.join(ROOT, 'data', 'shared_n5_scope_cache.jsonl')


def classes(qs):
    nv = [normals(q, F(1)) for q in qs]
    out = {}
    for i, j in itertools.combinations(range(len(qs)), 2):
        for u in nv[i]:
            for v in nv[j]:
                if all(a == b for a, b in zip(u, v)) or all(a == -b for a, b in zip(u, v)):
                    key = tuple(u) if u > [-c for c in u] else tuple(-c for c in u)
                    out.setdefault(key, set()).update((i, j))
    return sorted(sorted(c) for c in out.values())


def count(qs):
    try:
        e = CL.engine([qmul(GENERIC, q) for q in qs])
    except Exception:
        return None
    if 'by_depth' not in e:
        return None
    return e['bounded'], [e['by_depth'][str(k)] for k in range(1, 6)]


def move(rnd, qs):
    qs = [list(q) for q in qs]
    if rnd.random() < 0.15:
        a, b = qs[1][0], qs[1][3]
        if rnd.random() < 0.5:
            a += rnd.choice((-2, -1, 1, 2))
        else:
            b += rnd.choice((-2, -1, 1, 2))
        if b == 0:
            b = 1
        qs[1] = [a, 0, 0, b]
    else:
        i = rnd.randrange(2, 5)
        if rnd.random() < 0.1:
            qs[i] = [2 * x for x in qs[i]]
        qs[i][rnd.randrange(4)] += rnd.choice((-3, -2, -1, 1, 2, 3))
        if not any(qs[i]):
            qs[i][0] = 1
    return [tuple(q) for q in qs]


def run(seed):
    rnd = random.Random(seed)
    if seed % 2 == 0:
        # start from the n = 4 record's three non-hub cubes plus a sharing pair
        cur = [(1, 0, 0, 0), (rnd.randint(1, 6), 0, 0, rnd.randint(1, 6)),
               (4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5)]
    else:
        cur = [(1, 0, 0, 0), (rnd.randint(1, 6), 0, 0, rnd.randint(1, 6))] + \
              [tuple(rnd.randint(-7, 7) or 1 for _ in range(4)) for _ in range(3)]
    m = count(cur)
    while m is None:
        cur = move(rnd, cur)
        m = count(cur)
    best = (m[0], m[1], cur)
    log = []
    for _ in range(STEPS):
        nxt = move(rnd, cur)
        nm = count(nxt)
        if nm is None:
            continue
        log.append({'qs': nxt, 'total': nm[0], 'bd': nm[1]})
        if nm[0] >= m[0]:
            cur, m = nxt, nm
            if m[0] > best[0]:
                best = (m[0], m[1], cur)
    return {'seed': seed, 'best': best, 'log': log}


def main():
    with mp.Pool(8) as p:
        res = p.map(run, range(16))
    with open(CACHE, 'w') as f:
        for r in res:
            for row in r['log']:
                f.write(json.dumps(row) + '\n')
    rows = []
    for r in res:
        t, bd, qs = r['best']
        cl = classes(qs)
        rows.append({'seed': r['seed'], 'total': t, 'bd': bd, 'qs': qs, 'classes': cl})
    rows.sort(key=lambda x: -x['total'])
    for x in rows:
        print('seed %2d  total %3d  depths %s  sharing %s' % (x['seed'], x['total'], x['bd'], x['classes']), flush=True)
    json.dump({'runs': rows}, open(os.path.join(ROOT, 'data', 'shared_n5_scope.json'), 'w'), indent=1, default=str)
    recount()


def sc(qs):
    t, bd = Compound([tuple(q) for q in qs]).count()
    return t, [bd[k] for k in range(1, 6)]


def recount():
    """frame-free recount of the three best distinct compounds, from the saved runs"""
    path = os.path.join(ROOT, 'data', 'shared_n5_scope.json')
    d = json.load(open(path))
    rows = d['runs']
    top, seen = [], set()
    for x in rows:
        k = json.dumps(x['qs'])
        if k not in seen:
            seen.add(k); top.append(x)
        if len(top) == 3:
            break
    with mp.Pool(3) as p:
        rec = p.map(sc, [x['qs'] for x in top])
    for x, (t, bd) in zip(top, rec):
        x['sphere_count'] = {'total': t, 'bd': bd}
        print('sphere_count recount: engine %d %s, sphere_count %d %s' % (x['total'], x['bd'], t, bd), flush=True)
    json.dump(d, open(path, 'w'), indent=1, default=str)


if __name__ == '__main__':
    recount() if '--recount' in sys.argv else main()
