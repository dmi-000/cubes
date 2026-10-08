#!/usr/bin/env python3
"""PROOF_67 Lemma 1a's caveat: is every triple point a degree->=3 vertex of the bottom diagram?  [P417]

Claim (P417, from the circle lemma P405): with no shared face plane, at a point where all three
cubes of a triple reach equally far, their active normals project to DISTINCT points of one
circle, so each cube is strictly innermost in some direction: the bottom diagram's colours cycle
through all three and the degree is >= 3.  No tangential triple points.  Checked on exact level
graphs (level_s1 on the triple = its bottom diagram B_S): every node lying on all three cube
boundaries must have degree >= 3.  Triples: random, near-coincident (one cube a tiny rotation of
another), the triples of the 183 record and of the 8 bands; shared face planes excluded.
Output: data/triple_point_degree.json.
"""
import os, sys, json, random, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..'))
import c_level as CL
from euler3 import rowsT, frames
from depth2_charging import level_s1, on_boundary, engine_d2

ROOT = os.path.dirname(os.path.dirname(HERE))


def main():
    rnd = random.Random(417)
    triples = []
    for _ in range(150):
        triples.append([(1, 0, 0, 0)] + [tuple(rnd.randint(-7, 7) for _ in range(4)) for _ in range(2)])
    for _ in range(100):                       # near-coincident: hard for a tangency claim
        q = tuple(rnd.randint(-5, 5) for _ in range(4))
        triples.append([(1, 0, 0, 0), q, tuple(40 * x + rnd.randint(-1, 1) for x in q)])
    four = [[(1, 0, 0, 0), (0, 5, 3, 2), (1, -4, -1, 1), (1, 1, -1, -4)]]
    four += [r['qs'] for r in json.load(open(os.path.join(ROOT, 'data', 'band_components.json')))]
    for qs in four:
        triples += [[qs[i] for i in S] for S in itertools.combinations(range(4), 3)]
    checked = excluded = tp = bad = euler_bad = 0
    worst = []
    for qs in triples:
        qs = [tuple(q) for q in qs]
        if any(not any(q) for q in qs) or CL.shares_plane(qs):
            excluded += 1; continue
        Ms = [rowsT(R) for R in frames(qs)]
        deg, E, c = level_s1(Ms, [0, 1, 2])
        checked += 1
        # the detector's intermediate object, against Euler: sum (deg/2 - 1) = d2 - 1 - c (engine d2)
        euler_bad += sum(d / 2 - 1 for d in deg.values()) != engine_d2(list(qs)) - 1 - c
        for P, d in deg.items():
            if all(on_boundary(P, M) for M in Ms):
                tp += 1
                if d < 3:
                    bad += 1; worst.append({'qs': qs, 'point': str(P), 'degree': d})
    print('%d triples checked, %d excluded (shared plane); %d triple points; %d of degree < 3; '
          'Euler check against the engine failed in %d' % (checked, excluded, tp, bad, euler_bad))
    json.dump({'euler_failures': euler_bad, 'checked': checked, 'excluded': excluded, 'triple_points': tp, 'low_degree': worst},
              open(os.path.join(ROOT, 'data', 'triple_point_degree.json'), 'w'), indent=1)
    sys.exit(1 if bad or euler_bad else 0)


if __name__ == '__main__':
    main()
