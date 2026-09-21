#!/usr/bin/env python3
"""[OQ 39] Extending the `sum EE = 26` triple to four cubes -- does the new envelope reach 183?

The triple `1,0,0,0 ; 3,2,2,0 ; 3,-4,0,-3` holds `E_S = 32` with `sum EE = 26`, refuting the
per-triple maximum of 20 that [P359], [P360] and [P366] all rest on.  If that triple extends to
a 4-compound keeping `B = 128`, the record's `EE = 36` is under direct attack: two of its four
triples would already carry 26.

This searches the extension exactly -- fourth cubes drawn from the `EE = 10` family (so the new
pairs are at the per-pair maximum) and from random rotations as a control, reporting the best
`TOTAL` and the distribution of `B`.  Nothing is assumed about the outcome; a zero here is a
lower bound, not a closure ([METHODS 1]).
"""
import sys, os, json, random, itertools, collections
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import ee_bound_refute as EB
import ee_determinantal as D
from c_level import shares_plane
import provenance as PROV

ROOT = os.path.dirname(os.path.dirname(HERE))
BASE = [(1, 0, 0, 0), (3, 2, 2, 0), (3, -4, 0, -3)]


def anat(qs):
    sig, _ = EB.vertices(qs)
    EE = sig.get((2, 2), 0); SC = sig.get((3, 3), 0)
    T3 = sig.get((1, 1, 1), 0); Qg = sig.get((1, 1, 1, 1), 0)
    Q4 = sum(v for k, v in sig.items() if len(k) == 4)
    return EE, SC, T3 + 4 * Qg, Q4, 7 + EE + 2 * SC + T3 + 4 * Qg - Q4


def main():
    rng = random.Random(626)
    fam = []
    for q in itertools.product(range(-5, 6), repeat=4):
        if not any(q):
            continue
        g = 0
        for v in q:
            g = gcd(g, abs(v))
        if g != 1:
            continue
        neg = False
        for v in q:
            if v:
                neg = v < 0
                break
        if neg or shares_plane([(1, 0, 0, 0), q]):
            continue
        if D.ee_exact(q) == 10:
            fam.append(q)
    print('EE = 10 family (height <= 5): %d' % len(fam), flush=True)

    cands = list(fam) + [tuple(rng.randint(-9, 9) for _ in range(4)) for _ in range(600)]
    best = (0, None); byB = collections.Counter(); bestEE = (0, None)
    n = refused = 0
    for q in cands:
        qs = BASE + [q]
        if not any(q) or shares_plane(qs):
            continue
        try:
            EE, SC, B, Q4, tot = anat(qs)
        except Exception:
            refused += 1
            continue
        n += 1
        byB[B] += 1
        if tot > best[0]:
            best = (tot, (q, EE, SC, B, Q4))
        if EE > bestEE[0]:
            bestEE = (EE, (q, B, Q4, tot))
    print('fourth cubes evaluated: %d   unevaluable: %d' % (n, refused), flush=True)
    print('best TOTAL: %d   (record 183)' % best[0], flush=True)
    if best[1]:
        q, EE, SC, B, Q4 = best[1]
        print('   fourth cube %s   EE %d  SC2 %d  B %d  Q4 %d' % (str(q), EE, SC, B, Q4),
              flush=True)
    print('best EE_total: %d   at B = %d, Q4 = %d, TOTAL %d'
          % (bestEE[0], bestEE[1][1], bestEE[1][2], bestEE[1][3]) if bestEE[1] else '', flush=True)
    top = sorted(byB, reverse=True)[:8]
    print('B distribution (top): %s' % [(b, byB[b]) for b in top], flush=True)

    out = {'what': 'extending the EE = 26 triple to four cubes', 'supports': 'OQ 39',
           'base': [list(q) for q in BASE], 'evaluated': n, 'unevaluable': refused,
           'best_TOTAL': best[0],
           'best': {'q4': list(best[1][0]), 'EE': best[1][1], 'SC2': best[1][2],
                    'B': best[1][3], 'Q4': best[1][4]} if best[1] else None,
           'best_EE_total': bestEE[0],
           'B_distribution': {str(k): v for k, v in sorted(byB.items())}}
    out['reproduce'] = PROV.stamp(parameters={'seed': 626, 'family_height': 5, 'random': 600})
    json.dump(out, open(os.path.join(ROOT, 'data', 'extend_ee26.json'), 'w'), indent=1)
    print('wrote data/extend_ee26.json', flush=True)


if __name__ == '__main__':
    main()
