#!/usr/bin/env python3
"""Is EE <= 36 at B = 128?  [P359], [P360], [P361] -- the last underived link in [P354]'s chain.

WHY IT IS LIVE.  The UNCONDITIONAL `EE <= 6*C(4,2) = 36` was REFUTED in [P330]: the
face-diagonal family reaches 42.  So the conditional form has a precedent for being false, and
[P352]'s evidence was a sampling maximum from draws that never reach 36.

[P359]  The per-3-subset method -- which carried [P338], [P346], [P348] -- does NOT reach it.
        B = 128 forces E_S = 32 on all four subsets, and each pair lies in two of them, so a
        bound `sum EE <= m` per subset gives EE_total <= 2m.  The record and the golden both have
        sum EE = 18, which would give exactly 36 -- but the true maximum at E_S = 32 is **20**
        (witness 1,0,0,0;-2,-8,3,-3;0,4,-6,7 with pairs [10,6,4]), so the route yields only
        EE <= 40.  A subset can even hold E_S = 32 with a full EE = 10 pair; its NEIGHBOURS
        collapse instead (e.g. pairs [(10,0),(4,0),(0,0)]).

[P360]  The residual 4 is GEOMETRIC, not combinatorial.  Maximising the six pair-EE values
        subject to every 3-subset summing to <= 20, values from the observed set {0,4,6,8,10}:
        MAXIMUM 40, attained by (0,1)=0, (2,3)=0 and the four cross pairs at 10, with 15
        assignments hitting all four triples exactly.  So no counting argument over the subset
        lattice improves 40.  A targeted search for that exact pattern found ZERO configurations
        -- in a narrow window, so weak evidence.

[P361]  TWO DIRECTED CLIMBS, and they do not meet:
            A.  hold B = 128, maximise EE   ->  36   (no improvement on the record)
            B.  hold EE >= 38, maximise B   ->  84   (target 128)
        Random seeding never reached EE >= 38 at all (best 34), so B was re-seeded from the known
        EE = 42 face-diagonal family.  That family's B is RIGID: over 35 seeds,
        (EE,B) takes only (42,84) x20, (40,84) x10, (40,80) x5.

        B = 128 pins EE at 36;  EE >= 40 pins B at 84.

STATUS: measured and underived.  A climb that tries to break a ceiling and fails is stronger
evidence than a maximum over draws, but it is still a search ([METHODS 1]).
"""
import sys, os, json, random, itertools, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import ee_bound_refute as B
from c_level import shares_plane
import wall_keys as W
import provenance as PROV

ROOT = os.path.dirname(os.path.dirname(HERE))
FACE = [(1, 0, 0, 0), (3, 2, 2, 0), (5, 4, 4, 0), (4, 3, 3, 0), (5, 3, 3, 0),
        (6, 5, 5, 0), (5, 2, 2, 0), (7, 5, 5, 0)]


def anat(qs):
    s, _ = B.vertices(qs)
    return (s.get((2, 2), 0), s.get((1, 1, 1), 0) + 4 * s.get((1, 1, 1, 1), 0))


def ok(qs):
    return not (any(all(v == 0 for v in q) for q in qs) or shares_plane(qs))


def climb(start, rng, keep, better, steps=60):
    cur = start
    e, b = anat(cur)
    for _ in range(steps):
        moved = False
        for _ in range(40):
            n = [list(q) for q in cur]
            i, j = rng.randrange(1, 4), rng.randrange(4)
            n[i][j] += rng.choice([-2, -1, 1, 2])
            n = [tuple(q) for q in n]
            if not ok(n):
                continue
            try:
                e2, b2 = anat(n)
            except Exception:
                continue
            if keep(e2, b2) and better(e2, b2, e, b):
                cur, e, b = n, e2, b2
                moved = True
                break
        if not moved:
            break
    return e, b, cur


def main():
    out = {'what': 'is EE <= 36 at B = 128?', 'supports': 'LEDGER P359-P361'}
    rng = random.Random(4211)

    print('CLIMB A: hold B = 128, maximise EE')
    bestA = (0, None)
    for st in [[tuple(q) for q in W.REC[4]]]:
        e, b, c = climb(st, rng, lambda e2, b2: b2 == 128, lambda e2, b2, e, b: e2 > e)
        if e > bestA[0]:
            bestA = (e, c)
    print('   best EE with B = 128: %d   (record 36)' % bestA[0])

    print('\nCLIMB B: hold EE >= 38, maximise B -- seeded from the known EE = 42 family')
    seeds = []
    for c in itertools.combinations(FACE[1:], 3):
        qs = [(1, 0, 0, 0)] + list(c)
        if ok(qs):
            try:
                seeds.append((anat(qs), qs))
            except Exception:
                pass
    dist = collections.Counter(s[0] for s in seeds)
    print('   face-diagonal seeds: %d;  (EE,B) values: %s'
          % (len(seeds), dict(sorted(dist.items(), reverse=True))))
    bestB = (0, 0, None)
    for (e0, b0), st in sorted(seeds, reverse=True)[:10]:
        if e0 < 38:
            continue
        e, b, c = climb(st, rng, lambda e2, b2: e2 >= 38, lambda e2, b2, e, b: b2 > b)
        if b > bestB[0]:
            bestB = (b, e, c)
    print('   best B with EE >= 38: %d   (target 128)' % bestB[0])
    print('\n   B = 128 pins EE at 36;  EE >= 40 pins B at 84.  The regimes do not meet.')

    out['climb_A'] = {'best_EE_at_B128': bestA[0]}
    out['climb_B'] = {'best_B_at_EE38': bestB[0],
                      'face_seed_distribution': {str(k): v for k, v in sorted(dist.items())}}
    out['combinatorial_max'] = {'value': 40,
                                'pattern': '(0,1)=0, (2,3)=0, four cross pairs = 10',
                                'note': 'so the 36-vs-40 residual is geometric, not combinatorial'}
    out['status'] = 'measured and underived; the last link in the P354 chain'
    out['reproduce'] = PROV.stamp(parameters={'seed': 4211})
    json.dump(out, open(os.path.join(ROOT, 'data', 'ee_ceiling.json'), 'w'), indent=1, default=str)
    print('\nwritten data/ee_ceiling.json')


if __name__ == '__main__':
    main()
