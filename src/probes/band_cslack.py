#!/usr/bin/env python3
"""Climb on the COMPONENT slack of a depth-2 band, and look for c2 >= 3.  [P410]

The band lemma (P410) says  c2 - 1 <= sum_S (c_S - 1)  when no two band pairs share a cube.  The
margin climbs (band_climb, band_climb2) press on the ANCHOR slack sum_S (18 - d2(S)) and never on
this one, which sat at exactly 1 in all 8 known bands.  Here the objective is
    cslack = sum_S (c_S - 1) - (c2 - 1),
minimised over integer quaternion moves keeping c2 >= 2; a move that RAISES c2 is always accepted
(the shared-cube case needs c2 >= 3).  cslack < 0 would refute the lemma's conclusion and is
reported with the configuration.  Exact level graphs; cached on disk; 16 runs on 8 processes.
    python3 band_cslack.py [steps]
"""
import os, sys, json, random, itertools, multiprocessing as mp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import c_level as CL
from depth2_charging import level_s1
from euler3 import rowsT, frames

ROOT = os.path.dirname(os.path.dirname(HERE))
CACHE = os.path.join(ROOT, 'data', 'band_cslack_cache.jsonl')


def measure(qs):
    if any(not any(q) for q in qs) or CL.shares_plane(qs):
        return None
    Ms = [rowsT(R) for R in frames(qs)]
    G, EG, c2 = level_s1(Ms, [0, 1, 2, 3])
    cs, budget = [], 0
    for S in itertools.combinations(range(4), 3):
        dS, ES, cS = level_s1(Ms, list(S))
        cs.append(cS); budget += ES - len(dS)
    return {'c2': c2, 'cS': cs, 'cslack': sum(c - 1 for c in cs) - (c2 - 1),
            'margin': 64 - budget - (c2 - 1)}


def load_cache():
    c = {}
    if os.path.exists(CACHE):
        for line in open(CACHE):
            try:
                r = json.loads(line)
            except ValueError:          # a torn line from a concurrent append: recompute it
                continue
            c[r['k']] = r['m']
    return c


def run(args):
    start, seed, steps = args
    rnd = random.Random(seed)
    cache, out = load_cache(), open(CACHE, 'a')

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
    best, maxc2 = (m['cslack'], cur, m), (m['c2'], cur, m)
    st = {'accepted': 0, 'lost_band': 0, 'excluded': 0, 'unevaluated': 0, 'worse': 0}
    for t in range(steps):
        k = rnd.randrange(1, 4)
        s = rnd.choice([1, 2, 4, 8])
        cand = cur[:k] + [tuple(x + rnd.randint(-s, s) for x in cur[k])] + cur[k + 1:]
        mc = meas(cand)
        if mc is None:
            st['excluded'] += 1; continue
        if 'error' in mc:
            st['unevaluated'] += 1; continue
        if mc['c2'] < 2:
            st['lost_band'] += 1; continue
        if mc['c2'] <= m['c2'] and mc['cslack'] > m['cslack'] and rnd.random() > 0.1:
            st['worse'] += 1; continue
        st['accepted'] += 1
        cur, m = cand, mc
        if m['cslack'] < best[0]:
            best = (m['cslack'], cur, m)
        if m['c2'] > maxc2[0]:
            maxc2 = (m['c2'], cur, m)
            print('seed %d step %d: c2 = %d  %s  %s' % (seed, t, m['c2'], m, cur), flush=True)
        if m['cslack'] < 0:
            print('seed %d step %d: NEGATIVE COMPONENT SLACK %s %s' % (seed, t, m, cur), flush=True)
    return {'start': start, 'seed': seed, 'best_cslack': best[0], 'best': best[1], 'best_m': best[2],
            'max_c2': maxc2[0], 'max_c2_at': maxc2[1], 'max_c2_m': maxc2[2], 'stats': st}


def main():
    steps = int(sys.argv[1]) if len(sys.argv) > 1 else 1500
    starts = [r['qs'] for r in json.load(open(os.path.join(ROOT, 'data', 'band_components.json')))]
    jobs = [(s, 7000 + 10 * i + r, steps) for i, s in enumerate(starts) for r in range(2)]
    with mp.Pool(8) as p:
        res = p.map(run, jobs)
    print('\nbest cslack per run:', [r['best_cslack'] for r in res])
    print('max c2 per run:', [r['max_c2'] for r in res])
    lo = min(res, key=lambda r: r['best_cslack'])
    print('LOWEST COMPONENT SLACK %d at %s (%s)' % (lo['best_cslack'], lo['best'], lo['best_m']))
    print('moves:', {k: sum(r['stats'][k] for r in res) for k in res[0]['stats']})
    json.dump(res, open(os.path.join(ROOT, 'data', 'band_cslack.json'), 'w'), indent=1, default=str)


if __name__ == '__main__':
    main()
