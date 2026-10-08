#!/usr/bin/env python3
"""Climb the Mayer-Vietoris bound on d2 over the shared-plane locus: does it pass 70?  [P415]

MV gives d2 <= sum_S d2(S) + sum_P (m_P - 2) (shared_mv.py).  On shared-plane compounds that is a
route to d2 <= 70, hence 195, only if this bound never exceeds 70.  This maximises the bound itself,
seeded from shared_mv.json's highest rows, with shared_plane_climb's moves (cube 1 rotates about
cube 0's z axis, so the two share their z face planes).  A value above 70 ends the route.
Only the six pair rows are computed.  Cached.  Output: data/shared_mv_climb.json.
"""
import os, sys, json, random, itertools, multiprocessing as mp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..'))
from sphere_count import Compound

ROOT = os.path.dirname(os.path.dirname(HERE))
CACHE = os.path.join(ROOT, 'data', 'shared_mv_climb_cache.jsonl')


def mvb(qs):
    C = Compound(qs, 'Q')
    tot = 0
    for i, j in itertools.combinations(range(4), 2):
        k, l = [x for x in range(4) if x not in (i, j)]
        a = C.components(C.beat_pieces([i, j], [k]))
        b = C.components(C.beat_pieces([i, j], [l]))
        m = C.components(C.geq_pieces(i, [k, l]) + C.geq_pieces(j, [k, l]))
        tot += a + b + m - 2
    return tot


def run(args):
    start, seed, steps = args
    rnd = random.Random(seed)
    cache = {}
    if os.path.exists(CACHE):
        for line in open(CACHE):
            try:
                r = json.loads(line); cache[r['k']] = r['v']
            except ValueError:
                pass
    out = open(CACHE, 'a')

    def meas(qs):
        if any(not any(q) for q in qs):
            return None
        k = ';'.join(','.join(map(str, q)) for q in qs)
        if k not in cache:
            try:
                v = mvb(qs)
            except Exception:
                v = None
            cache[k] = v
            out.write(json.dumps({'k': k, 'v': v}) + '\n'); out.flush()
        return cache[k]

    cur = [tuple(q) for q in start]
    v = meas(cur)
    best, unev = (v, cur), 0
    for s in range(steps):
        k = rnd.randrange(1, 4)
        sz = rnd.choice([1, 2, 4])
        if k == 1:
            a, _, _, b = cur[1]
            q = (a + rnd.randint(-sz, sz), 0, 0, b + rnd.randint(-sz, sz))
        else:
            q = tuple(x + rnd.randint(-sz, sz) for x in cur[k])
        cand = cur[:k] + [q] + cur[k + 1:]
        vc = meas(cand)
        if vc is None:
            unev += 1; continue
        if vc >= v:
            cur, v = cand, vc
            if v > best[0]:
                best = (v, cur)
                print('seed %d step %d MV bound %d %s%s' % (seed, s, v, cur, '   ABOVE 70' if v > 70 else ''), flush=True)
    return {'seed': seed, 'best': best[0], 'at': best[1], 'unevaluated': unev}


def main():
    steps = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    rows = json.load(open(os.path.join(ROOT, 'data', 'shared_mv.json')))[:-1]
    rows.sort(key=lambda r: -r['mv_bound'])
    starts = [r['qs'] for r in rows[:8]]
    jobs = [(s, 900 + 10 * i + r, steps) for i, s in enumerate(starts) for r in range(2)]
    with mp.Pool(8) as p:
        res = p.map(run, jobs)
    print('\nbest per run:', [r['best'] for r in res])
    b = max(res, key=lambda r: r['best'])
    print('HIGHEST MV bound on the shared-plane locus: %d at %s; unevaluated %d; route %s'
          % (b['best'], b['at'], sum(r['unevaluated'] for r in res), 'DEAD (> 70)' if b['best'] > 70 else 'not refuted'))
    json.dump(res, open(os.path.join(ROOT, 'data', 'shared_mv_climb.json'), 'w'), indent=1, default=str)


if __name__ == '__main__':
    main()
