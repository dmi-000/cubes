#!/usr/bin/env python3
"""GATE: is W1 really the deepest level's vertex count?

oq32_form.py restated [OQ 32] as `SUM(3 - deg) >= 2(c-1)` using the identification
W1 = V3(3) = V, the deepest-level graph's vertex count.  That identification was
ASSERTED, and everything downstream of it -- including the 15 apparent violations
-- is worthless if it is wrong.  So it is computed here a second way, from the
tagged triple points directly: W1 counts 3-body vertices contained in exactly ONE
other cube ([P262]).  A triple point lies on 3 bodies; at n=4 the fourth either
contains it (W1) or not (W0).

If the two disagree, oq32_form.py's restatement is void and must be withdrawn
before anything is concluded from its numbers.
"""
import collections, itertools, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from euler3 import rowsT, frames
from v3_outer import triple_points
from c_level import level_graph, shares_plane, parse, engine


def w1_direct(qs):
    """W0 and W1 from tagged triple points: 3-body vertices by how many cubes contain them"""
    Ms, node = triple_points(qs)
    n = len(qs)
    W = collections.Counter()
    for P, on in node.items():
        if len(on) != 3:
            continue                      # not a 3-body vertex
        s = 0
        for k in range(n):
            if k in on:
                continue
            v = [abs(sum(Ms[k][q][z] * P[z] for z in range(3))) for q in range(3)]
            if all(x < 1 for x in v):
                s += 1                    # strictly contained
        W[s] += 1
    return W


CASES = ["1,0,0,0;0,5,3,2;1,-4,-1,1;1,1,-1,-4",
         "1,0,0,0;76,86,80,-95;113,-103,44,-53;98,-87,23,53"]
rnd = random.Random(41)
for _ in range(14):
    qs = [(1, 0, 0, 0)] + [tuple(rnd.randint(-30, 30) for _ in range(4)) for _ in range(3)]
    if any(not any(q) for q in qs) or shares_plane(qs):
        continue
    CASES.append(";".join(",".join(str(v) for v in q) for q in qs))

print(f"{'V (deepest level graph)':>24} {'W1 (tagged triples)':>21} {'W0':>6} {'agree':>6}")
bad = 0
for spec in CASES:
    qs = parse(spec)
    g = level_graph(qs).get(len(qs) - 1)
    if g is None:
        continue
    W = w1_direct(qs)
    agree = g["V"] == W[1]
    bad += (not agree)
    print(f"{g['V']:>24} {W[1]:>21} {W[0]:>6} {'OK' if agree else '*** NO ***':>6}   {spec[:44]}")
print()
print("IDENTIFICATION HOLDS" if bad == 0 else
      f"IDENTIFICATION FAILS on {bad} -- oq32_form.py's restatement is VOID")
