#!/usr/bin/env python3
"""The PAIR term of [P236]: the part of d1 that three-body plane counting cannot see.

    d1 = (>=3-body gain) + (two-body gain) + c + 1

The second term is a sum over pairs of  2*(shared corners) + (edge-edge coincidences)  --
degree-6 and degree-4 vertices where both cubes supply 3 and 2 face planes respectively.
Bounding it is a question about TWO congruent cubes about a common centre, which is the one
case this project has proved outright (max(2) = 13).

Adding further cubes can only DELETE such vertices (by swallowing them), so the pair-alone
value is an upper bound for the same pair inside any larger configuration -- which is what
makes a per-pair constant usable in  d1 <= 108*C(n,3) + beta*C(n,2) + 2.
"""
import itertools, sys
from collections import Counter
sys.path.insert(0, '.')
from cellcomplex import on_bdry_params
from euler3 import rowsT, frames, segments
from v3_outer import strictly_inside


def pair_profile(qa, qb):
    """(corner-corner count, edge-edge count, gain) for the pair alone"""
    qs = [qa, qb]
    Ms = [rowsT(R) for R in frames(qs)]
    node = {}; arcs = []
    for p, d, lo, hi in segments(Ms[0], Ms[1]):
        cuts = sorted({lo, hi})
        for a, b in zip(cuts, cuts[1:]):
            if a >= b:
                continue
            ends = []
            for t in (a, b):
                P = tuple(p[z] + t * d[z] for z in range(3))
                node.setdefault(P, len(node)); ends.append(node[P])
            arcs.append(tuple(ends))
    deg = Counter()
    for a, b in arcs:
        deg[a] += 1; deg[b] += 1
    corner = edge = 0
    for P, idx in node.items():
        per = []
        for m in range(2):
            c = sum(1 for q in range(3)
                    if abs(sum(Ms[m][q][z] * P[z] for z in range(3))) == 1)
            if c:
                per.append(c)
        if deg[idx] / 2 - 1 <= 0:
            continue
        if sorted(per) == [3, 3]:
            corner += 1
        elif sorted(per) == [2, 2]:
            edge += 1
    return corner, edge, 2 * corner + edge


if __name__ == '__main__':
    import glob, json, random
    from sharedaxis import q_axis
    from fractions import Fraction as F
    from math import gcd

    best = (0, None); tab = Counter()
    seen = 0
    # 1. structured pairs: shared axis of every kind, many angles
    AXES = {'body diagonal': (1,1,1), 'face': (0,0,1), 'edge': (1,1,0),
            'coord-plane (1,2,0)': (1,2,0), 'generic (1,2,3)': (1,2,3)}
    print('STRUCTURED pairs, cube 0 = identity, cube 1 = rotation about an axis')
    print('%-22s %s' % ('axis', 'pair gain over t = 1/6 .. 6'))
    for name, ax in AXES.items():
        gains = Counter()
        for p in range(1, 13):
            for q in (1, 2, 3, 4, 6):
                if gcd(p, q) != 1: continue
                t = F(p, q)
                qb = q_axis(ax, t)
                try:
                    c, e, g = pair_profile((1,0,0,0), tuple(qb))
                except Exception:
                    continue
                gains[g] += 1; seen += 1
                if g > best[0]: best = (g, (name, str(t), c, e))
        print('%-22s %s' % (name, dict(sorted(gains.items(), reverse=True))))
    # 2. random census pairs
    rng = random.Random(5); gains = Counter()
    for fn in sorted(glob.glob('census_n4_*.jsonl'))[:4]:
        with open(fn) as f:
            for i, l in enumerate(f):
                if i > 700: break
                d = json.loads(l)
                if not d.get('count'): continue
                cfg = [tuple(x) for x in d['cfg']]
                i1, i2 = rng.sample(range(4), 2)
                try:
                    c, e, g = pair_profile(cfg[i1], cfg[i2])
                except Exception:
                    continue
                gains[g] += 1; seen += 1
                if g > best[0]: best = (g, ('census', '', c, e))
    print('\nRANDOM census pairs: %s' % dict(sorted(gains.items(), reverse=True)))
    print('\n%d pairs examined; MAX pair gain = %d  %s' % (seen, best[0], best[1]))
