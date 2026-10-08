#!/usr/bin/env python3
"""The shared-plane families never measured: how high does d2 go on each?  [P418]

Plan item 2 (195 unconditional) needs `d2 <= 70` on every compound with a shared face plane, with
`d1 <= 104` and ANCHOR's `d3 <= 20`.  [P411]/[P414]/[P415] measured only ONE sharing pair (cube 1
a rotation of cube 0 about z).  The other sharing structures:
    two_disjoint   0~1 about z, 3 = 2 rotated about 2's own z axis
    two_at_hub     0~1 about z, 0~2 about x; cube 3 free
    three_on_axis  0, 1, 2 all about z; cube 3 free
    four_on_axis   all four about z
Each family is climbed on the objective d2 (ties broken by the total), with the engine (retried
under global rotations, as in [P411]). Each family's best is then re-counted with sphere_count's
exact D-set counter, which is valid on the locus (the level-graph tools are not, [P246]), and the
two must agree.
- A first version climbed with sphere_count directly.
  - At about 30 s per evaluation, it would have needed about 7 hours, so it was stopped after 362.
  - Its cache, `shared_plane_scope_sc_cache.jsonl`, is kept.  A climb gives
a LOWER bound on each family's ceiling, never an upper one.  d2 > 70 refutes item 2's route; a
total > 261 is a tool bug (261 is proved).  Cached by quaternions; 0 unevaluated is reported, not
assumed.  Output: data/shared_plane_scope.json.
    python3 shared_plane_scope.py [steps]          run 1: the four families above
    python3 shared_plane_scope.py [steps] --new    run 2 (P419): star, path, axis3_pair
                                                   -> data/shared_plane_scope2.json
"""
import os, sys, json, random, multiprocessing as mp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
from sphere_count import Compound
from degenerate_counts import total

ROOT = os.path.dirname(os.path.dirname(HERE))
CACHE = os.path.join(ROOT, 'data', 'shared_plane_scope_cache.jsonl')   # engine counts
SC_CACHE = os.path.join(ROOT, 'data', 'shared_plane_scope_sc_cache.jsonl')


def qmul(p, q):
    a1, b1, c1, d1 = p; a2, b2, c2, d2 = q
    return (a1*a2 - b1*b2 - c1*c2 - d1*d2, a1*b2 + b1*a2 + c1*d2 - d1*c2,
            a1*c2 - b1*d2 + c1*a2 + d1*b2, a1*d2 + b1*c2 - c1*b2 + d1*a2)


# A family is a map from free integer parameters to four quaternions.  Rotations about an axis
# are (a,0,0,b) for z and (a,b,0,0) for x; right-multiplying cube 2 by (a,0,0,b) rotates it about
# its OWN z axis, so the result shares cube 2's z face plane.
FAMILIES = {
    'two_disjoint':  (8, lambda p: [(1, 0, 0, 0), (p[0], 0, 0, p[1]), tuple(p[2:6]),
                                     qmul(tuple(p[2:6]), (p[6], 0, 0, p[7]))]),
    'two_at_hub':    (8, lambda p: [(1, 0, 0, 0), (p[0], 0, 0, p[1]), (p[2], p[3], 0, 0), tuple(p[4:8])]),
    'three_on_axis': (8, lambda p: [(1, 0, 0, 0), (p[0], 0, 0, p[1]), (p[2], 0, 0, p[3]), tuple(p[4:8])]),
    'four_on_axis':  (6, lambda p: [(1, 0, 0, 0), (p[0], 0, 0, p[1]), (p[2], 0, 0, p[3]), (p[4], 0, 0, p[5])]),
    # added for P419: the three remaining realisable structures
    'star':          (6, lambda p: [(1, 0, 0, 0), (p[0], 0, 0, p[1]), (p[2], p[3], 0, 0), (p[4], 0, p[5], 0)]),
    'path':          (6, lambda p: [(1, 0, 0, 0), (p[0], 0, 0, p[1]),
                                     qmul((p[0], 0, 0, p[1]), (p[2], p[3], 0, 0)),
                                     qmul(qmul((p[0], 0, 0, p[1]), (p[2], p[3], 0, 0)), (p[4], 0, p[5], 0))]),
    'axis3_pair':    (6, lambda p: [(1, 0, 0, 0), (p[0], 0, 0, p[1]), (p[2], 0, 0, p[3]), (p[4], p[5], 0, 0)]),
}
FIRST = ('two_disjoint', 'two_at_hub', 'three_on_axis', 'four_on_axis')   # run 1 (P418)


def shared(q1, q2):
    """How many face planes the two cubes share (exact).  1 = a shared plane; 3 = the same cube
    (sharing two perpendicular planes forces the third)."""
    from sphere_count import normals
    from fractions import Fraction as F
    n1, n2 = normals(q1, F(1)), normals(q2, F(1))
    return sum(any(all(a == s * b for a, b in zip(u, v)) for v in n2 for s in (1, -1)) for u in n1)


def run(args):
    fam, seed, steps = args
    npar, build = FAMILIES[fam]
    rnd = random.Random(seed)
    cache = {}
    if os.path.exists(CACHE):
        for line in open(CACHE):
            try:
                r = json.loads(line); cache[r['k']] = r['m']
            except ValueError:
                pass
    out = open(CACHE, 'a')

    def meas(p):
        qs = build(p)
        if any(not any(q) for q in qs):
            return None
        # distinct cubes only: a cube symmetry (e.g. 90 degrees about z) gives the SAME cube,
        # which is a different object from a shared plane
        if any(shared(qs[i], qs[j]) > 1 for i in range(4) for j in range(i)):
            return None
        k = ';'.join(','.join(map(str, q)) for q in qs)
        if k not in cache:
            try:
                t, bd = total(qs)
                if t is None:
                    raise ValueError('engine refused under every rotation')
                m = {'t': t, 'bd': {str(a): b for a, b in bd.items()},
                     'pairs': [[i, j] for i in range(4) for j in range(i) if shared(qs[i], qs[j])]}
            except Exception as e:
                m = {'error': type(e).__name__}
            cache[k] = m
            out.write(json.dumps({'k': k, 'm': m}) + '\n'); out.flush()
        return cache[k]

    def key(m):
        return (m['bd']['2'], m['t'])

    cur = [rnd.randint(-6, 6) or 1 for _ in range(npar)]
    m = meas(cur)
    while m is None or 'error' in m:
        cur = [rnd.randint(-6, 6) or 1 for _ in range(npar)]; m = meas(cur)
    best, unev, excl = (key(m), cur, m), 0, 0
    for s in range(steps):
        i = rnd.randrange(npar)
        sz = rnd.choice([1, 2, 4])
        cand = cur[:]; cand[i] += rnd.randint(-sz, sz)
        mc = meas(cand)
        if mc is None:
            excl += 1; continue
        if 'error' in mc:
            unev += 1; continue
        if key(mc) >= key(m):
            cur, m = cand, mc
            if key(m) > best[0]:
                best = (key(m), cur, m)
    return {'family': fam, 'seed': seed, 'best_d2': best[0][0], 'best_total': best[0][1],
            'at': build(best[1]), 'measure': best[2], 'unevaluated': unev, 'excluded': excl}


def main():
    steps = int(sys.argv[1]) if len(sys.argv) > 1 else 600
    # run 2 (P419) climbs only the families added after run 1, into its own output file
    fams = [f for f in FAMILIES if f not in FIRST] if '--new' in sys.argv else list(FIRST)
    jobs = [(f, 1000 * list(FAMILIES).index(f) + r, steps) for f in fams for r in range(4)]
    with mp.Pool(8) as p:
        res = p.map(run, jobs)
    for f in fams:
        rs = [r for r in res if r['family'] == f]
        b = max(rs, key=lambda r: (r['best_d2'], r['best_total']))
        t, bd = Compound(b['at']).count()
        b['sphere_count'] = {'t': t, 'bd': bd}
        print('%-14s sphere_count %d %s  %s' % (f, t, bd, 'AGREE' if t == b['best_total']
              and bd[2] == b['best_d2'] else 'DISAGREE'), flush=True)
        print('%-14s d2 per run %s; best d2 %d (total %d, depths %s, sharing pairs %s) at %s; '
              'unevaluated %d' % (f, [r['best_d2'] for r in rs], b['best_d2'], b['best_total'],
                                  b['measure']['bd'], b['measure']['pairs'], b['at'],
                                  sum(r['unevaluated'] for r in rs)))
    out = 'shared_plane_scope2.json' if '--new' in sys.argv else 'shared_plane_scope.json'
    json.dump(res, open(os.path.join(ROOT, 'data', out), 'w'), indent=1, default=str)


if __name__ == '__main__':
    main()
