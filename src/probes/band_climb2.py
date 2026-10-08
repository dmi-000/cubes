#!/usr/bin/env python3
"""A longer, more aggressive climb on the band margin.  [P410]

[P409]'s climb (4 runs x 300 steps, steps of +-2) reached margin 7 and was still falling.  This one:
starts from all 7 known depth-2 bands; 16 runs x 1500 steps on 8 processes; step size drawn from
{1, 2, 4, 8} per move; a move that RAISES the margin by 1 is accepted with probability 0.1, so a run
can leave a local minimum (the best is kept separately).  AS RUN (P410), THAT RULE NEVER FIRED: every
margin observed is odd, so no move raised it by exactly 1, and the runs were pure greedy descent.  Every evaluation is exact (band_climb's
`measure`) and cached on disk keyed by the quaternions, so a killed run restarts for free.
A margin < 0 is re-checked with the engine before anything is said about it.
    python3 band_climb2.py [steps]
"""
import os, sys, json, random, multiprocessing as mp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import c_level as CL
from band_climb import measure

ROOT = os.path.dirname(os.path.dirname(HERE))
CACHE = os.path.join(ROOT, 'data', 'band_climb2_cache.jsonl')


def load_cache():
    c = {}
    if os.path.exists(CACHE):
        for line in open(CACHE):
            r = json.loads(line)
            c[r['k']] = r['m']
    return c


def run(args):
    start, seed, steps = args
    rnd = random.Random(seed)
    cache = load_cache()
    out = open(CACHE, 'a')

    def meas(qs):
        k = ';'.join(','.join(map(str, q)) for q in qs)
        if k not in cache:
            try:
                m = measure(qs)
            except Exception as e:
                m = {'error': type(e).__name__}
            cache[k] = m
            out.write(json.dumps({'k': k, 'm': m}) + '\n'); out.flush()
        return cache[k]

    cur = [tuple(q) for q in start]
    m = meas(cur)
    best = (m['margin'], cur, m)
    stats = {'accepted': 0, 'uphill': 0, 'lost_band': 0, 'excluded': 0, 'unevaluated': 0, 'worse': 0}
    for t in range(steps):
        k = rnd.randrange(1, 4)
        s = rnd.choice([1, 2, 4, 8])
        q = tuple(x + rnd.randint(-s, s) for x in cur[k])
        cand = cur[:k] + [q] + cur[k + 1:]
        mc = meas(cand)
        if mc is None:
            stats['excluded'] += 1; continue
        if 'error' in mc:
            stats['unevaluated'] += 1; continue
        if mc['c2'] < 2:
            stats['lost_band'] += 1; continue
        if mc['margin'] > m['margin'] + 1 or (mc['margin'] == m['margin'] + 1 and rnd.random() > 0.1):
            stats['worse'] += 1; continue
        stats['uphill' if mc['margin'] > m['margin'] else 'accepted'] += 1
        cur, m = cand, mc
        if m['margin'] < best[0]:
            best = (m['margin'], cur, m)
            print('seed %d step %4d  margin %3d  budget %3d  c2 %d  d2 %d  %s'
                  % (seed, t, m['margin'], m['budget'], m['c2'], m['d2'], cur), flush=True)
    return {'start': start, 'seed': seed, 'best_margin': best[0], 'best': best[1],
            'measure': best[2], 'stats': stats}


def main():
    steps = int(sys.argv[1]) if len(sys.argv) > 1 else 1500
    starts = []
    for f in ('band_hunt.json', 'band_hunt_7.json'):
        starts += [h['qs'] for h in json.load(open(os.path.join(ROOT, 'data', f)))['hits']]
    starts.append([[1, 0, 0, 0], [16, 0, 1, -1], [43, 33, 3, 52], [81, 27, -32, -10]])  # P409's 7
    jobs = [(s, 1000 * i + r, steps) for i, s in enumerate(starts) for r in range(2)]
    with mp.Pool(8) as p:
        res = p.map(run, jobs)
    best = min(res, key=lambda r: r['best_margin'])
    print('\nper run:', [r['best_margin'] for r in res])
    print('LOWEST MARGIN %d at %s (%s)' % (best['best_margin'], best['best'], best['measure']))
    tot = {k: sum(r['stats'][k] for r in res) for k in res[0]['stats']}
    print('moves:', tot)
    if best['best_margin'] < 0:
        e = CL.engine(best['best'])
        print('engine total %s, by_depth %s' % (e.get('bounded'), e.get('by_depth')))
    json.dump(res, open(os.path.join(ROOT, 'data', 'band_climb2.json'), 'w'), indent=1, default=str)


if __name__ == '__main__':
    main()
