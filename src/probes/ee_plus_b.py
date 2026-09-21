#!/usr/bin/env python3
"""[OQ 39] A candidate law found while exploring the band: `EE + B <= 164` at n = 4.

Exploring the `B = 118..126` band ([P367]) produced the frontier

    B = 128  ->  EE 36        B = 124  ->  EE 40        B = 120  ->  EE 44

and `36 + 128 = 40 + 124 = 44 + 120 = 164`.  FOUR structurally different compounds sit exactly
on it -- the record, the golden, the 4-cycle, and the `EE = 44` compound found in the band --
which is the signature of a real constraint rather than a sampling artefact.

WHY IT MATTERS.  `TOTAL = 7 + EE + 2*SC2 + B - Q4`, so `EE + B <= 164` gives

    TOTAL <= 171 + 2*SC2 - Q4

and the record is `171 + 12 - 0 = 183` EXACTLY.  This is a single inequality covering every
column of [P367]'s grid, where `EE <= 36 at B = 128` covers one.  It is NOT sufficient on its
own: a paw (`SC2 = 8`, `Q4 = 0`) sitting on the line would give 187.  The paw's measured
`EE + B` is 152.

THIS PROBE TRIES TO BREAK IT, which is the only useful thing to do with a candidate law
([P361]).  Climbs from five seed families, each chosen to be hard for it: the record (on the
line), the face-diagonal family (highest known EE), the paw and 4-cycle (highest SC2 with
Q4 = 0 and the band's other extreme), and random.
"""
import sys, os, json, random, itertools, collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import ee_bound_refute as EB
from c_level import shares_plane
import wall_keys as WK
import provenance as PROV
from band_frontier import anat, load_cache, FACEDIAG, key, _mem

ROOT = os.path.dirname(os.path.dirname(HERE))
LIMIT = 164


def climb(start, steps, rng, stats):
    cur = [tuple(q) for q in start]
    try:
        ca = anat(cur)
    except Exception:
        return None
    best = (ca['EE'] + ca['ES'], cur, ca)
    for _ in range(steps):
        cand = [list(q) for q in cur]
        for _ in range(rng.choice([1, 1, 2])):
            i = rng.randrange(1, len(cand)); j = rng.randrange(4)
            cand[i][j] += rng.choice([-3, -2, -1, 1, 2, 3])
        cand = [tuple(q) for q in cand]
        if any(not any(q) for q in cand) or shares_plane(cand) or key(cand) is None:
            continue
        stats['tried'] += 1
        try:
            a = anat(cand)
        except Exception:
            stats['refused'] += 1
            continue
        v = a['EE'] + a['ES']
        if v > best[0]:
            best = (v, cand, a)
        if v >= best[0] - 2:
            cur, ca = cand, a
    return best


def main():
    load_cache()
    rng = random.Random(164164)
    rec = [tuple(q) for q in WK.REC[4]]
    seeds = {'record': rec,
             'face-diagonal': [(1, 0, 0, 0)] + [rng.choice(FACEDIAG) for _ in range(3)],
             'EE=44 band': [(1, 0, 0, 0), (3, 2, 2, 0), (3, -4, 0, -3), (1, 1, 0, 3)],
             'mixed': [rec[0], rec[1], (3, 2, 2, 0), (3, -4, 0, -3)],
             'random': [(1, 0, 0, 0)] + [tuple(rng.randint(-9, 9) for _ in range(4))
                                         for _ in range(3)]}
    stats = collections.Counter()
    out = {'what': 'candidate law EE + B <= 164 at n = 4', 'supports': 'OQ 39',
            'limit': LIMIT, 'climbs': {}}
    print('CLIMBS on EE + B     (limit under test: %d)' % LIMIT)
    worst = (0, None)
    for name, st in seeds.items():
        r = climb(st, 700, rng, stats)
        if r is None:
            print('   %-15s  seed unevaluable' % name)
            continue
        v, qs, a = r
        flag = '  *** EXCEEDS ***' if v > LIMIT else ''
        print('   %-15s  best EE + B = %3d   (EE %2d  B %3d  SC2 %2d  Q4 %2d  TOTAL %3d)%s'
              % (name, v, a['EE'], a['ES'], a['SC2'], a['Q4'], 7 + a['obj'], flag))
        out['climbs'][name] = {'best': v, 'EE': a['EE'], 'B': a['ES'], 'SC2': a['SC2'],
                               'Q4': a['Q4'], 'TOTAL': 7 + a['obj'],
                               'quats': [list(q) for q in qs]}
        if v > worst[0]:
            worst = (v, qs)
    print('   evaluated %d   unevaluable %d' % (stats['tried'] - stats['refused'],
                                                stats['refused']))

    print('\nTHE KNOWN CONSTRUCTIONS against the line:')
    known = [('record', 36, 6, 128, 0), ('paw', 24, 8, 128, 0), ('4-cycle', 36, 8, 128, 18),
             ('golden 177', 36, 12, 128, 18), ('K4', 36, 12, 74, 0),
             ('face-diagonal', 42, 0, 84, 0), ('EE=44 band', 44, 0, 120, 2)]
    print('   %-15s  EE   B   EE+B   slack   TOTAL' % 'construction')
    for nm, ee, sc, B, q4 in known:
        print('   %-15s  %2d  %3d   %3d    %3d     %3d'
              % (nm, ee, B, ee + B, LIMIT - ee - B, 7 + ee + 2 * sc + B - q4))
    out['known'] = [{'name': k[0], 'EE': k[1], 'SC2': k[2], 'B': k[3], 'Q4': k[4],
                     'EE_plus_B': k[1] + k[3]} for k in known]

    allm = [v for k, v in _mem.items() if len(json.loads(k)) == 4]
    mx = max((v['EE'] + v['ES'] for v in allm), default=0)
    print('\n   over every 4-compound in the cache (%d): max EE + B = %d' % (len(allm), mx))
    out['cache'] = {'n': len(allm), 'max_EE_plus_B': mx}
    print('   %s' % ('HOLDS in everything measured -- and is UNPROVED ([METHODS 1])'
                     if mx <= LIMIT else 'REFUTED'))

    out['reproduce'] = PROV.stamp(parameters={'seed': 164164, 'steps': 700},
                                  inputs=['data/band_cache.jsonl'])
    json.dump(out, open(os.path.join(ROOT, 'data', 'ee_plus_b.json'), 'w'), indent=1)
    print('\nwrote data/ee_plus_b.json')


if __name__ == '__main__':
    main()
