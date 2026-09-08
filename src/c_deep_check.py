#!/usr/bin/env python3
"""Verify the deepest-level c=2 witness and read off what it does to [OQ 32].

[P262]/[P263] convert Theorem S into `W0 <= 84` via `W1 = 2(d3 - 2)`, which is
`d3 = V3(3)/2 + c3 + 1` with TWO hypotheses fused: c3 = 1, and every triple point
having degree 3 so that E = 3V/2.  This witness is non-degenerate and has c3 = 2,
so it tests the first; E vs 3V/2 tests the second.  Both are checked here rather
than inferred, and the witness is perturbed to confirm it is not a hidden
coincidence.
"""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_level import level_graph, shares_plane, parse, engine

SPEC = "1,0,0,0;76,86,80,-95;113,-103,44,-53;98,-87,23,53"
qs = parse(SPEC)
n = len(qs)
ell = n - 1
lv = level_graph(qs)[ell]
e = engine(qs)
d = e["by_depth"][str(ell)]
V, E, c = lv["V"], lv["E"], lv["c"]

print(f"witness  {SPEC}")
print(f"  n={n}  total={e['bounded']}  by_depth={e['by_depth']}")
print(f"  shares a face plane : {shares_plane(qs)}")
print(f"  ell={ell}: V={V} E={E} c={c}  component sizes {lv['sizes']}")
print(f"  identity  E-V+c+1 = {E-V+c+1}   engine d_{ell} = {d}   "
      f"{'HOLDS' if E-V+c+1 == d else 'FAILS'}")
print()
print("  [P262]/[P263] chain step, which assumes c3 = 1 and E = 3V/2:")
print(f"    E = {E},  3V/2 = {3*V//2}   -> degree-3 hypothesis "
      f"{'holds' if 2*E == 3*V else 'FAILS'}")
print(f"    chain's  W1 = 2(d3-2)      = {2*(d-2)}")
# WITHDRAWN: W1 is NOT the level graph's V.  w1_gate.py refutes that on 4 of 16
# configurations -- V counts arc endpoints on cube EDGES as well as triple points,
# and is 44 at n=4 in every case measured while W1 is 44, 40 or 36.  W1 must be
# computed from the tagged triple points; see oq32_test.py.  On THIS witness the
# direct value is W1 = 36 against 2(d3-2) = 38, so the step fails by 2.
from w1_gate import w1_direct
W = w1_direct(qs)
print(f"    actual   W1 (tagged triples) = {W[1]}   W0 = {W[0]}")
print(f"    step W1 - 2(d3-2)            = {W[1] - 2*(d-2)}")
print()
rnd = random.Random(23)
print("  perturbation (is c=2 here open, or a coincidence?):")
for scale in (10, 100, 1000):
    keep = tot = 0
    for _ in range(10):
        cand = [qs[0]] + [tuple(v * scale + rnd.randint(-1, 1) for v in q) for q in qs[1:]]
        if shares_plane(cand):
            continue
        g = level_graph(cand).get(ell)
        if g is None:
            continue
        tot += 1
        if g["c"] == 2:
            keep += 1
    print(f"    1/{scale:<5}: kept c=2 in {keep}/{tot}")
