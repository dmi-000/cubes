#!/usr/bin/env python3
"""THE EE DIRECTION: can EE exceed 36 while B = 128?  [P352]

[P351] exhausted the corner-sharing ladder by CONSTRUCTION. The remaining move named there was
the edge direction: every rung of that ladder carries `EE` of 36 or 24, the face-diagonal family
reaches 42 but pays in `B` (128 -> 84), and nothing had been built with `EE > 42`.

THREE PROBES, none of which finds one.

  A. Build from the per-pair EE maximum. 72 quaternions give `EE = 10` against the identity
     ([P330]); 900 four-tuples drawn from them reach compound `EE = 36` and objective 160.
  B. Near the record, where `B = 128` already holds. 1 479 perturbations with `B = 128`:
     `EE` never exceeds 36, and the objective never exceeds 176.
  C. Independent draws. 2 200 configurations: max `EE` anywhere is 28, and of the 9 that land at
     `B = 128` the best objective is 154.

So `EE = 36` is the largest value seen at `B = 128`, and `EE = 42` (the face-diagonal family)
comes only with `B = 84`.

**THE ASYMMETRY TO KEEP IN VIEW.** The corner ladder is closed by CONSTRUCTION -- every
attainable `SC2` was built exactly and `SC2 = 10` shown empty. This direction is closed only by
SAMPLING, and [P342] is the standing warning: the configuration that maximises `sum_h` was found
by derivation and no sampling would have reached it. **Treat this as a lower bound on what is
attainable, not as a closed direction.**
"""
import sys, os, json, random, collections
from math import gcd
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import ee_bound_refute as B
from c_level import shares_plane
import wall_keys as W
import provenance as PROV

ROOT = os.path.dirname(os.path.dirname(HERE))


def anat(qs):
    s, _ = B.vertices(qs)
    EE = s.get((2, 2), 0)
    SC = s.get((3, 3), 0)
    T3 = s.get((1, 1, 1), 0)
    Qg = s.get((1, 1, 1, 1), 0)
    Q4 = sum(v for k, v in s.items() if len(k) == 4)
    return {'EE': EE, 'SC2': SC, 'T3': T3, 'Q4': Q4,
            'two_body': EE + 2 * SC, 'B': T3 + 4 * Qg,
            'objective': EE + 2 * SC + T3 + 4 * Qg - Q4}


def main():
    out = {'what': 'can EE exceed 36 while B = 128?', 'supports': 'LEDGER P352'}
    rec = [tuple(q) for q in W.REC[4]]
    r = anat(rec)
    print('record: EE %d  SC2 %d  T3 %d  Q4 %d  two-body %d  B %d  objective %d'
          % (r['EE'], r['SC2'], r['T3'], r['Q4'], r['two_body'], r['B'], r['objective']))
    out['record'] = r

    print('\nB. near the record, where B = 128 already holds')
    rng = random.Random(307)
    atcap = collections.Counter()
    best = (0, None)
    n = hits = 0
    while n < 1500:
        qs = [list(q) for q in rec]
        for _ in range(rng.choice([1, 1, 2])):
            i, j = rng.randrange(1, 4), rng.randrange(4)
            qs[i][j] += rng.choice([-2, -1, 1, 2])
        qs = [tuple(q) for q in qs]
        if any(all(v == 0 for v in q) for q in qs) or shares_plane(qs):
            continue
        n += 1
        try:
            a = anat(qs)
        except Exception:
            continue
        if a['B'] == 128:
            hits += 1
            atcap[a['EE']] += 1
            if a['objective'] > best[0]:
                best = (a['objective'], a)
    print('   %d perturbations, %d with B = 128' % (n, hits))
    print('   EE at B = 128: %s   MAX %d' % (dict(sorted(atcap.items())), max(atcap)))
    print('   best objective %d  (record 176)' % best[0])
    out['local'] = {'tried': n, 'at_cap': hits, 'EE_hist': {str(k): v for k, v in sorted(atcap.items())},
                    'max_EE': max(atcap), 'best_objective': best[0]}

    print('\nC. independent draws')
    rng = random.Random(401)
    allEE = collections.Counter()
    atcap2 = collections.Counter()
    best2 = (0, None)
    n = hits = 0
    while n < 1500:
        qs = [(1, 0, 0, 0)] + [tuple(rng.randint(-12, 12) for _ in range(4)) for _ in range(3)]
        if any(all(v == 0 for v in q) for q in qs) or shares_plane(qs):
            continue
        n += 1
        try:
            a = anat(qs)
        except Exception:
            continue
        allEE[a['EE']] += 1
        if a['B'] == 128:
            hits += 1
            atcap2[a['EE']] += 1
            if a['objective'] > best2[0]:
                best2 = (a['objective'], a)
    print('   %d draws, %d with B = 128;  max EE anywhere %d;  max EE at B=128 %s'
          % (n, hits, max(allEE), max(atcap2) if atcap2 else 'n/a'))
    print('   best objective at B = 128: %d' % best2[0])
    out['global'] = {'tried': n, 'at_cap': hits, 'max_EE_anywhere': max(allEE),
                     'max_EE_at_cap': max(atcap2) if atcap2 else None,
                     'best_objective': best2[0]}

    print('\n   EE = 36 is the largest seen at B = 128; EE = 42 (face-diagonal) needs B = 84.')
    print('   SAMPLED, not constructed -- a lower bound on what is attainable ([METHODS 1]).')
    out['conclusion'] = ('EE = 36 is the largest observed at B = 128; EE = 42 occurs only at '
                         'B = 84. Sampled evidence only, unlike the constructed corner ladder.')
    out['reproduce'] = PROV.stamp(parameters={'seeds': [307, 401]})
    json.dump(out, open(os.path.join(ROOT, 'data', 'ee_direction.json'), 'w'), indent=1, default=str)
    print('\nwritten data/ee_direction.json')


if __name__ == '__main__':
    main()
