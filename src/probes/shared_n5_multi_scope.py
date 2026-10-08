#!/usr/bin/env python3
"""Five cubes with two or more sharing pairs: how high do they count?  [P436]

[PROOF_N5](../../PROOF_N5.md) Parts 3–4 give `max(5) <= 485` for at most one sharing pair. Before
building the multi-pair argument (P419–P422 at n = 4), this measures what the multi-pair compounds
reach, as [P432] did for one pair.

**Construction.** A random sharing forest on cubes 0–4 with 2–4 edges. A root is a free integer
quaternion. A child is `q_parent ⊗ (a, b·e_k)`, a rotation about the parent's own k-th face
normal, so it shares that face plane with its parent (convention checked: `qmul(p, r)` is the
body-frame rotation). Siblings rotated about the same axis form an axis class. The structure
that actually results is recorded with `classes()`; extra coincidental sharings are allowed and
labelled.
- Climbs on the total move the roots' entries and the edges' (a, b), keeping the forest.
- Identical cubes (a class sharing two planes) are rejected, since they reduce to n = 4.

**Counts.**
- The c_level engine in the generic frame (3,1,1,1), as in [P432] ([P419]: the identity frame is
  unreliable here).
- The best of each run is recounted frame-free with sphere_count.

**What it decides** (rule set before the run).
- If every structure's best sits far below 485 (under ~400), report: a coarser argument may close
  the multi-pair case.
- If any comes near 457, report before building anything.
- Either way this gives lower bounds only; it bounds nothing.

Output: data/shared_n5_multi_scope.json; every evaluation is cached in
data/shared_n5_multi_scope_cache.jsonl.
"""
import os, sys, json, random, itertools, collections, multiprocessing as mp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import c_level as CL
from depth2_charging import qmul
from shared_n5_scope import classes, sc

ROOT = os.path.dirname(os.path.dirname(HERE))
GENERIC = (3, 1, 1, 1)
STEPS = 3000
CACHE = os.path.join(ROOT, 'data', 'shared_n5_multi_scope_cache.jsonl')


def build(forest, roots, edges):
    """forest: list of (parent, child, k) in build order; roots: {cube: quat}; edges: {child: (a, b)}"""
    q = dict(roots)
    for p, ch, k in forest:
        a, b = edges[ch]
        e = [0, 0, 0]; e[k] = b
        q[ch] = qmul(q[p], (a,) + tuple(e))
    return [tuple(q[i]) for i in range(5)]


def count(qs):
    try:
        e = CL.engine([qmul(GENERIC, q) for q in qs])
    except Exception:
        return None
    if 'by_depth' not in e:
        return None
    return e['bounded'], [e['by_depth'][str(k)] for k in range(1, 6)]


def identical(cl, qs):
    # two cubes sharing all three planes share two classes
    pairs = collections.Counter()
    for c in cl:
        for i, j in itertools.combinations(c, 2):
            pairs[(i, j)] += 1
    return any(v >= 2 for v in pairs.values())


def random_forest(rnd):
    m = rnd.choice((2, 2, 3, 3, 4))
    order = list(range(5)); rnd.shuffle(order)
    forest, inside = [], {order[0]}
    for ch in order[1:]:
        if len(forest) < m and rnd.random() < 0.8:
            forest.append((rnd.choice(sorted(inside)), ch, rnd.randrange(3)))
        inside.add(ch)
    if len(forest) < 2:
        return random_forest(rnd)
    children = {ch for _, ch, _ in forest}
    return forest, [i for i in range(5) if i not in children]


def rq(rnd):
    return tuple(rnd.randint(-7, 7) or 1 for _ in range(4))


def move(rnd, roots, edges):
    roots, edges = dict(roots), dict(edges)
    if rnd.random() < 0.4:
        ch = rnd.choice(sorted(edges))
        a, b = edges[ch]
        if rnd.random() < 0.5:
            a += rnd.choice((-2, -1, 1, 2))
        else:
            b += rnd.choice((-2, -1, 1, 2))
        edges[ch] = (a, b or 1)
    else:
        i = rnd.choice(sorted(roots))
        q = list(roots[i])
        if rnd.random() < 0.1:
            q = [2 * x for x in q]
        q[rnd.randrange(4)] += rnd.choice((-3, -2, -1, 1, 2, 3))
        if not any(q):
            q[0] = 1
        roots[i] = tuple(q)
    return roots, edges


def run(seed):
    rnd = random.Random(seed)
    forest, rts = random_forest(rnd)
    while True:
        roots = {i: rq(rnd) for i in rts}
        edges = {ch: (rnd.randint(1, 6), rnd.randint(1, 6)) for _, ch, _ in forest}
        qs = build(forest, roots, edges)
        cl = classes(qs)
        if not identical(cl, qs):
            m = count(qs)
            if m is not None:
                break
    best = (m[0], m[1], qs, cl)
    log = []
    for _ in range(STEPS):
        r2, e2 = move(rnd, roots, edges)
        q2 = build(forest, r2, e2)
        cl2 = classes(q2)
        if identical(cl2, q2):
            continue
        nm = count(q2)
        if nm is None:
            continue
        log.append({'qs': q2, 'total': nm[0], 'bd': nm[1], 'classes': cl2})
        if nm[0] >= m[0]:
            roots, edges, m = r2, e2, nm
            if nm[0] > best[0]:
                best = (nm[0], nm[1], q2, cl2)
    return {'seed': seed, 'forest': forest, 'best': best, 'log': log}


def signature(cl):
    """structure up to relabelling: sorted class sizes and the overlap pattern"""
    sizes = sorted(len(c) for c in cl)
    hub = sum(1 for i in range(5) if sum(i in c for c in cl) >= 2)
    return '%s classes of sizes %s; cubes in >= 2 classes: %d' % (len(cl), sizes, hub)


def main():
    with mp.Pool(8) as p:
        res = p.map(run, range(32))
    with open(CACHE, 'w') as f:
        for r in res:
            for row in r['log']:
                f.write(json.dumps(row) + '\n')
    # best per structure, over every evaluation (not just the run bests)
    bys = {}
    for r in res:
        for row in r['log'] + [{'qs': r['best'][2], 'total': r['best'][0], 'bd': r['best'][1], 'classes': r['best'][3]}]:
            sg = signature(row['classes'])
            if sg not in bys or row['total'] > bys[sg]['total']:
                bys[sg] = row
    out = sorted(bys.items(), key=lambda kv: -kv[1]['total'])
    for sg, row in out:
        print('%-55s best %3d  depths %s' % (sg, row['total'], row['bd']), flush=True)
    with mp.Pool(8) as p:
        rec = p.map(sc, [row['qs'] for _, row in out])
    for (sg, row), (t, bd) in zip(out, rec):
        row['sphere_count'] = {'total': t, 'bd': bd}
        print('recount %-47s engine %3d, sphere_count %3d %s' % (sg, row['total'], t, bd), flush=True)
    json.dump({'by_structure': dict(out), 'runs': [{'seed': r['seed'], 'forest': r['forest'], 'best_total': r['best'][0]}
                                                    for r in res]},
              open(os.path.join(ROOT, 'data', 'shared_n5_multi_scope.json'), 'w'), indent=1, default=str)


if __name__ == '__main__':
    main()
