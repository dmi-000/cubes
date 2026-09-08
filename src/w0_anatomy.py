#!/usr/bin/env python3
"""What IS W0, inside the level-1 graph?  Anatomy before any formula.

[P262]'s route to W0 <= 84 goes through W1 and is broken generically ([P271]).
The user's redirection: find what determines W0 directly.  Step one is not a
candidate formula but an ANATOMY -- W0 is a subset of the level-1 graph's
vertices, and until it is known WHICH subset, and what the rest are, any formula
is a guess fitted to two numbers.

At the n=4 record the level-1 graph has V=150, E=240, d1=92, and W0=84.  So 66
vertices are not triple points, and 240 arcs is not 3*84/2.  This classifies every
vertex by how many cube boundaries it lies on and by its degree, so the 150 splits
into named parts that can be checked against W0 = 84 rather than assumed.
"""
import collections, itertools, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from euler3 import rowsT, frames, segments
from cellcomplex import on_bdry_params
from c_level import strictly_inside, parse, engine, level_graph
from w1_gate import w1_direct


def anatomy(qs, ell):
    Ms = [rowsT(R) for R in frames(qs)]
    n = len(qs)
    deg = collections.Counter()
    on = collections.defaultdict(set)
    for i, j in itertools.combinations(range(n), 2):
        for p, d, lo, hi in segments(Ms[i], Ms[j]):
            cuts = sorted({lo, hi} | {t for k in range(n) if k not in (i, j)
                                      for t in on_bdry_params(p, d, lo, hi, Ms[k])})
            for a, b in zip(cuts, cuts[1:]):
                if a >= b:
                    continue
                mid = tuple(p[z] + ((a + b) / 2) * d[z] for z in range(3))
                s = sum(1 for k in range(n) if k not in (i, j) and strictly_inside(mid, Ms[k]))
                if s + 1 != ell:
                    continue
                for t in (a, b):
                    P = tuple(p[z] + t * d[z] for z in range(3))
                    deg[P] += 1
                    on[P].update((i, j))
    # how many cube boundaries each vertex actually lies on
    for P in list(on):
        for k in range(n):
            if k in on[P]:
                continue
            v = [abs(sum(Ms[k][q][z] * P[z] for z in range(3))) for q in range(3)]
            if all(x <= 1 for x in v) and any(x == 1 for x in v):
                on[P].add(k)
    cls = collections.Counter()
    for P in on:
        cls[(len(on[P]), deg[P])] += 1
    return cls, deg, on


CASES = [("n=4 record 183", "1,0,0,0;0,5,3,2;1,-4,-1,1;1,1,-1,-4"),
         ("deep c=2 witness", "1,0,0,0;76,86,80,-95;113,-103,44,-53;98,-87,23,53"),
         ("worst step failure", "1,0,0,0;1,2,3,2;-3,1,1,1;2,-1,1,0")]

for label, spec in CASES:
    qs = parse(spec)
    e = engine(qs)
    W = w1_direct(qs)
    g = level_graph(qs)[1]
    cls, deg, on = anatomy(qs, 1)
    tri = sum(v for k, v in cls.items() if k[0] >= 3)
    two = sum(v for k, v in cls.items() if k[0] == 2)
    print(f"{label}   {spec}")
    print(f"  d1={e['by_depth'].get('1')}  level-1 graph V={g['V']} E={g['E']} c={g['c']}"
          f"   W0={W[0]} W1={W[1]}")
    print(f"  vertices by (bodies on, degree): {dict(sorted(cls.items()))}")
    print(f"  on >=3 bodies : {tri}      on exactly 2 : {two}      total {tri+two}")
    print(f"  W0 == (vertices on >=3 bodies at level 1)?  {W[0]} vs {tri}  "
          f"{'YES' if W[0] == tri else 'NO'}")
    print()
