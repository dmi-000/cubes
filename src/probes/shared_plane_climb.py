#!/usr/bin/env python3
"""How high can a compound WITH a shared face plane count?  [P411]

Item 2 of the plan: 195 would become unconditional if degenerate compounds never beat nearby
generic ones.  This climbs the region count ON the shared-plane locus: cube 0 is the identity, and
cube 1 is a rotation about z, (a,0,0,b), so the two share their z face planes; cubes 2 and 3 are
free.  Starts: the 183 record's cubes 2 and 3 with cube 1 replaced, and random starts.  A count
above 183 is news; above 195 refutes item 2's goal; above 261 is a tool bug (261 is proved).
Engine refusals are retried under global rotations, and counted as unevaluated if they persist.
Cached; 16 runs on 8 processes.  Output: data/shared_plane_climb.json.
"""
import os, sys, json, random, multiprocessing as mp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import c_level as CL
from degenerate_counts import total

ROOT = os.path.dirname(os.path.dirname(HERE))
CACHE = os.path.join(ROOT, 'data', 'shared_plane_climb_cache.jsonl')


def run(args):
    start, seed, steps = args
    rnd = random.Random(seed)
    cache = {}
    if os.path.exists(CACHE):
        for line in open(CACHE):
            try:
                r = json.loads(line); cache[r['k']] = r['t']
            except ValueError:
                pass
    out = open(CACHE, 'a')

    def meas(qs):
        if any(not any(q) for q in qs):
            return None
        k = ';'.join(','.join(map(str, q)) for q in qs)
        if k not in cache:
            t, _ = total(qs)
            cache[k] = t
            out.write(json.dumps({'k': k, 't': t}) + '\n'); out.flush()
        return cache[k]

    cur = [tuple(q) for q in start]
    t = meas(cur)
    best, unev = (t, cur), 0
    for s in range(steps):
        k = rnd.randrange(1, 4)
        sz = rnd.choice([1, 2, 4])
        if k == 1:
            a, _, _, b = cur[1]
            q = (a + rnd.randint(-sz, sz), 0, 0, b + rnd.randint(-sz, sz))
        else:
            q = tuple(x + rnd.randint(-sz, sz) for x in cur[k])
        cand = cur[:k] + [q] + cur[k + 1:]
        tc = meas(cand)
        if tc is None:
            unev += 1; continue
        if tc >= t:
            cur, t = cand, tc
            if t > best[0]:
                best = (t, cur)
                print('seed %d step %d total %d %s' % (seed, s, t, cur), flush=True)
    return {'seed': seed, 'start': start, 'best': best[0], 'at': best[1], 'unevaluated': unev}


def main():
    steps = int(sys.argv[1]) if len(sys.argv) > 1 else 800
    rec = [(1, 0, 0, 0), (0, 5, 3, 2), (1, -4, -1, 1), (1, 1, -1, -4)]
    starts = []
    for a, b in [(1, 1), (2, 1), (5, 2), (3, 1)]:
        starts.append([rec[0], (a, 0, 0, b), rec[2], rec[3]])
    rnd = random.Random(411)
    while len(starts) < 16:
        starts.append([(1, 0, 0, 0), (rnd.randint(1, 9), 0, 0, rnd.randint(-9, 9))]
                      + [tuple(rnd.randint(-7, 7) for _ in range(4)) for _ in range(2)])
    with mp.Pool(8) as p:
        res = p.map(run, [(s, 100 + i, steps) for i, s in enumerate(starts)])
    print('\nbest per run:', [r['best'] for r in res])
    b = max(res, key=lambda r: r['best'])
    print('HIGHEST shared-plane count %s at %s; unevaluated moves %d'
          % (b['best'], b['at'], sum(r['unevaluated'] for r in res)))
    json.dump(res, open(os.path.join(ROOT, 'data', 'shared_plane_climb.json'), 'w'), indent=1, default=str)


if __name__ == '__main__':
    main()
