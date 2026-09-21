#!/usr/bin/env python3
"""[OQ 39] A broad hunt for 185 at n = 4 — the first count that could beat the record.

`TOTAL` is ODD ([P375]: central symmetry pairs every region except the convex depth-n core), so
beating 183 means reaching **185**, not 184.

WHAT THIS DOES DIFFERENTLY from the searches this session has already refuted:

  * the objective is the ENGINE count, never the identity ([P374] — and the engine is CHEAPER,
    18 ms against the census's 66);
  * seeds come from five structurally different places, including the two that produced every
    earlier false ceiling AND the two that broke them, so no single family dominates;
  * restarts are many and short rather than few and long, because [P373] showed the failure
    mode is a deep climb inside one basin.

A null result here is a LOWER bound and nothing more ([METHODS 1]); what would end it is 185.
"""
import sys, os, json, random, itertools, collections
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import ee_determinantal as D
from c_level import shares_plane, engine
import wall_keys as WK
import provenance as PROV

ROOT = os.path.dirname(os.path.dirname(HERE))
CACHE = os.path.join(ROOT, 'data', 'hunt185_cache.jsonl')

REC = [tuple(q) for q in WK.REC[4]]
REFUTER = [(1, 0, 0, 0), (0, 2, -3, -2), (0, 2, -3, 2), (-4, -2, -5, -6)]
FACEDIAG = [(3, 2, 2, 0), (5, 3, 3, 0), (7, 2, 2, 0), (4, 3, 3, 0), (5, 2, 2, 0),
            (2, 1, 1, 0), (9, 4, 4, 0), (5, 4, 4, 0), (8, 3, 3, 0)]


def count(qs):
    r = engine(qs)
    if 'error' in r or not r.get('by_depth'):
        return None
    return sum(v for k, v in r['by_depth'].items() if k != '0')


def main():
    rng = random.Random(185185)
    stats = collections.Counter()
    hist = collections.Counter()
    best = (0, None)
    seen = set()

    def ev(qs):
        k = tuple(sorted(qs))
        if k in seen:
            return None
        seen.add(k)
        if any(not any(q) for q in qs) or shares_plane(qs):
            return None
        stats['tried'] += 1
        v = count(qs)
        if v is None:
            stats['refused'] += 1
            return None
        hist[v] += 1
        return v

    def perturb(qs, scale):
        c = [list(q) for q in qs]
        for _ in range(rng.choice([1, 1, 2, 3])):
            i = rng.randrange(1, 4); j = rng.randrange(4)
            c[i][j] += rng.choice([-scale, scale, -1, 1])
        return [tuple(q) for q in c]

    def seed():
        r = rng.random()
        if r < 0.25:
            return perturb(REC, rng.choice([1, 2, 5]))
        if r < 0.45:
            return perturb(REFUTER, rng.choice([1, 2, 5]))
        if r < 0.60:
            return [(1, 0, 0, 0)] + [rng.choice(FACEDIAG) for _ in range(3)]
        if r < 0.80:
            return [REC[0], REC[1]] + [tuple(rng.randint(-9, 9) for _ in range(4))
                                       for _ in range(2)]
        return [(1, 0, 0, 0)] + [tuple(rng.randint(-12, 12) for _ in range(4))
                                 for _ in range(3)]

    RESTARTS, STEPS = 400, 90
    print('hunting 185 -- %d restarts x %d steps, engine objective' % (RESTARTS, STEPS),
          flush=True)
    for rs in range(RESTARTS):
        cur = seed()
        cv = ev(cur)
        if cv is None:
            continue
        for _ in range(STEPS):
            cand = perturb(cur, rng.choice([1, 1, 2, 3]))
            v = ev(cand)
            if v is None:
                continue
            if v > best[0]:
                best = (v, cand)
                print('   new best %d  %s'
                      % (v, ';'.join(','.join(map(str, q)) for q in cand)), flush=True)
                if v >= 185:
                    print('   *** RECORD BEATEN ***', flush=True)
            if v >= cv - 2:
                cur, cv = cand, v
        if rs % 80 == 79:
            print('   restart %d: evaluated %d, refusals %d, best %d'
                  % (rs + 1, stats['tried'] - stats['refused'], stats['refused'], best[0]),
                  flush=True)

    print('\nevaluated %d   unevaluable %d   distinct configurations %d'
          % (stats['tried'] - stats['refused'], stats['refused'], len(seen)), flush=True)
    print('BEST: %d   %s' % (best[0], 'BEATS 183' if best[0] > 183 else 'does not beat 183'),
          flush=True)
    if best[1]:
        print('   %s' % ';'.join(','.join(map(str, q)) for q in best[1]), flush=True)
    print('top counts: %s' % sorted(hist.items(), reverse=True)[:10], flush=True)
    evens = [c for c in hist if c % 2 == 0]
    print('even counts observed (parity check, [P375] says none): %s' % evens, flush=True)

    out = {'what': 'broad hunt for 185 at n = 4', 'supports': 'OQ 39',
           'evaluated': stats['tried'] - stats['refused'], 'unevaluable': stats['refused'],
           'distinct': len(seen), 'best': best[0],
           'best_quats': [list(q) for q in best[1]] if best[1] else None,
           'even_counts_seen': evens,
           'distribution': {str(k): v for k, v in sorted(hist.items())}}
    out['reproduce'] = PROV.stamp(parameters={'seed': 185185, 'restarts': RESTARTS,
                                              'steps': STEPS},
                                  note='engine objective; a null result is a lower bound')
    json.dump(out, open(os.path.join(ROOT, 'data', 'hunt_185.json'), 'w'), indent=1)
    print('\nwrote data/hunt_185.json', flush=True)


if __name__ == '__main__':
    main()
