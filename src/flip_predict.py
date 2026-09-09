#!/usr/bin/env python3
"""Does ANY n=9-level invariant change where the n=10 count flips?

The walk showed the flip between t=4/12 and t=5/12, with n=9 count constant at
2787 and outer-VERTEX-COUNT constant at 1126 on both sides.  So the coarse
predictor failed.  The radius SIGNATURE is finer -- the full multiset of r^2 over
outer vertices, not its cardinality -- and it distinguished the two endpoints
([P285] follow-up).  If it also moves at t=4->5 it predicts the flip; if it is
constant there, then nothing measured at n=9 sees the change and the n=10 count is
a function of position in the continuum that no n=9 invariant tested resolves.
"""
import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from radii import radius_signature, vertices

SEVEN = [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1),
         (7,14,1,-5),(4,-3,-4,-4),(168,-168,168,-415)]
A = (88787,-9061,74275,113786); B = (88726,-8954,74074,113960); N = 12

def red(q):
    g = 0
    for v in q: g = math.gcd(g, abs(v))
    return tuple(v//g for v in q) if g else q

sigs = {}
for t in (0, 4, 5, 11, 12):
    q = red(tuple((N-t)*a + t*b for a,b in zip(A,B)))
    qs = SEVEN + [q]
    full = radius_signature(qs)
    sigs[t] = full
    print(f"t={t:>2}/12  outer V {len(vertices(qs)):>5}  distinct r^2 {len(full):>4}  "
          f"n=10 {'3925' if t < 5 else '3921'}")
print()
print(f"signature t=0 vs t=4  (both 3925) : {'SAME' if sigs[0]==sigs[4] else 'DIFFER'}")
print(f"signature t=4 vs t=5  (ACROSS FLIP): {'SAME' if sigs[4]==sigs[5] else 'DIFFER'}")
print(f"signature t=5 vs t=11 (both 3921) : {'SAME' if sigs[5]==sigs[11] else 'DIFFER'}")
print(f"signature t=11 vs t=12 (endpoint)  : {'SAME' if sigs[11]==sigs[12] else 'DIFFER'}")
print()
print("DIFFER across the flip and SAME within each side => radii signature PREDICTS it.")
print("SAME across the flip => no n=9 invariant tested resolves the n=10 change.")
