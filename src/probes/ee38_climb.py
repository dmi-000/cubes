#!/usr/bin/env python3
"""[OQ 39] How far do `EE` at `B = 128` and `EE + B` actually go?  Climbing from the refuter.

[P373] refuted both `EE <= 36 at B = 128` ([P352], [P361]) and `EE + B <= 164` ([P368]) with

    1,0,0,0 ; 0,2,-3,-2 ; 0,2,-3,2 ; -4,-2,-5,-6      EE 38, B 128, SC2 0, Q4 0, TOTAL 173

Both refuted ceilings were MAXIMA OVER SEARCHES, and the searches were seeded from the record
and the face-diagonal family.  So the honest next question is not "what is the new ceiling" --
which would repeat the error -- but "how far does a climb from the refuter go", reported as the
lower bound it is ([METHODS 1]).
"""
import sys, os, json, random, itertools, collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import ee_bound_refute as EB
from c_level import shares_plane
import provenance as PROV

ROOT = os.path.dirname(os.path.dirname(HERE))
SEED = [(1, 0, 0, 0), (0, 2, -3, -2), (0, 2, -3, 2), (-4, -2, -5, -6)]


def anat(qs):
    sig, _ = EB.vertices(qs)
    EE = sig.get((2, 2), 0); SC = sig.get((3, 3), 0)
    T3 = sig.get((1, 1, 1), 0); Qg = sig.get((1, 1, 1, 1), 0)
    Q4 = sum(v for k, v in sig.items() if len(k) >= 4)
    B = T3 + 4 * Qg
    return {'EE': EE, 'SC2': SC, 'B': B, 'Q4': Q4, 'sum': EE + B,
            'TOTAL': 7 + EE + 2 * SC + B - Q4}


def climb(start, key, steps, rng, stats):
    cur = [tuple(q) for q in start]
    ca = anat(cur)
    best = (key(ca), cur, ca)
    for _ in range(steps):
        cand = [list(q) for q in cur]
        for _ in range(rng.choice([1, 1, 2])):
            i = rng.randrange(1, 4); j = rng.randrange(4)
            cand[i][j] += rng.choice([-3, -2, -1, 1, 2, 3])
        cand = [tuple(q) for q in cand]
        if any(not any(q) for q in cand) or shares_plane(cand):
            continue
        stats['tried'] += 1
        try:
            a = anat(cand)
        except Exception:
            stats['refused'] += 1
            continue
        if key(a) > best[0]:
            best = (key(a), cand, a)
        if key(a) >= best[0] - 2:
            cur, ca = cand, a
    return best


def main():
    rng = random.Random(38128)
    stats = collections.Counter()
    out = {'what': 'how far EE at B=128, EE+B and TOTAL go from the refuter',
           'supports': 'OQ 39; follows P373', 'seed': [list(q) for q in SEED], 'climbs': {}}
    objectives = {
        'EE + B': lambda a: a['sum'],
        'EE, holding B = 128': lambda a: a['EE'] if a['B'] == 128 else -1,
        'TOTAL': lambda a: a['TOTAL'],
    }
    for name, key in objectives.items():
        b = climb(SEED, key, 1200, rng, stats)
        v, qs, a = b
        print('   %-22s best %4d    EE %2d  SC2 %2d  B %3d  Q4 %2d  EE+B %3d  TOTAL %3d'
              % (name, v, a['EE'], a['SC2'], a['B'], a['Q4'], a['sum'], a['TOTAL']), flush=True)
        out['climbs'][name] = {'best': v, **{k: a[k] for k in a},
                               'quats': [list(q) for q in qs]}
    print('   evaluated %d   unevaluable %d' % (stats['tried'] - stats['refused'],
                                                stats['refused']), flush=True)
    out['evaluated'] = stats['tried'] - stats['refused']
    out['unevaluable'] = stats['refused']
    out['reproduce'] = PROV.stamp(parameters={'seed': 38128, 'steps': 1200})
    json.dump(out, open(os.path.join(ROOT, 'data', 'ee38_climb.json'), 'w'), indent=1)
    print('wrote data/ee38_climb.json', flush=True)


if __name__ == '__main__':
    main()
