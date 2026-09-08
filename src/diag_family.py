#!/usr/bin/env python3
"""SOLVE along the body-diagonal family instead of sampling the pair space.

[P278]/wall_types: the record's hub pairs carry 6 edge-edge crossings + 2
COINCIDENT CORNERS.  Two concentric equal cubes share a corner exactly when R
maps a corner direction to a corner direction -- codimension 2 in the 3-dim pair
space, so a CURVE, not a point.  The record's hub axis is (1,1,1), i.e. R fixes
the corner (1,1,1) and the curve is "rotate about a body diagonal by theta".

That family is exactly parameterised by rational quaternions q = (w, t, t, t), so
the whole curve can be walked EXACTLY rather than sampled: every member has the
corner coincidence by construction, and the only question is what weight it
carries.  This is the 'solve, don't sample' version of the weight-10 hunt -- the
condition is imposed, not stumbled upon.

If weight 10 holds along an interval of the curve, weight 10 is codimension 2 and
six pairs would need 12 conditions in the 9 degrees of freedom of three free
cubes -- overdetermined, which would say T = 60 is impossible and max(4) < 195.
If instead weight 10 occurs only at isolated theta, the codimension is 3 and the
count is even worse.  Either way the answer is a dimension, not a sweep.
"""
import collections, math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from twobody_solve import pair_detail
from c_level import engine

print("body-diagonal family  q = (w,t,t,t):  rotation about (1,1,1) by theta")
print("cube 0 = identity, cube 1 = q.  Corner (1,1,1) is FIXED, so the corner")
print("coincidence holds identically along the whole curve.\n")
print(f"{'w':>4} {'t':>4} {'theta':>8}  {'(deg2,deg4,deg6)':>18} {'weight':>7}  n=2 count")
rows = []
for t in (1,):
    for w in range(0, 25):
        if w == 0 and t == 0:
            continue
        q = (w, t, t, t)
        n2 = w * w + 3 * t * t
        theta = math.degrees(2 * math.acos(min(1.0, abs(w) / math.sqrt(n2))))
        qs = [(1, 0, 0, 0), q]
        try:
            det = pair_detail(qs)
            e = engine(qs)
        except Exception as ex:
            print(f"{w:>4} {t:>4} {theta:>8.3f}  error {ex}")
            continue
        c = det.get((0, 1), collections.Counter())
        wt = c[4] + 2 * c[6]
        rows.append((theta, wt))
        print(f"{w:>4} {t:>4} {theta:>8.3f}  ({c[2]:>3},{c[4]:>3},{c[6]:>3})"
              f"{'':>6} {wt:>7}  {e['bounded']}")
best = max(rows, key=lambda r: r[1]) if rows else None
print(f"\nmax weight along the family: {best[1]} at theta = {best[0]:.3f} deg")
print("record hub pairs are theta = 46.826 deg with weight 10.")
