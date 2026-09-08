#!/usr/bin/env python3
"""Codimension of the SECOND weight-10 realisation, (0,10,0): 10 edge-edge, no corner.

diag_family.py showed the (0,6,2) realisation is codimension 2 -- weight 10 holds
along the whole "rotate about a body diagonal" curve, because the single corner
coincidence is the only condition and the 6 crossings come free.

The (0,10,0) family has NO corner coincidence, so nothing forces it that way, and
its codimension has to be found rather than assumed.  The same solve applies: FIX
THE AXIS and walk the angle exactly along rational quaternions q = (w, a, b, c).
If weight 10 persists along the curve the realisation is codimension 2 like the
first; if it appears only at isolated w it is codimension 3 and cannot help build
T = 60.

Note on orbit sizes: -I is always a symmetry, so coincidences come in antipodal
pairs and 10 crossings is 5 orbits.  Five independent conditions in a 3-dimensional
pair space is impossible, so either the conditions are dependent or the pair
carries extra symmetry -- and which it is, is exactly what the curve shows.
"""
import collections, math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from twobody_solve import pair_detail
from c_level import engine

AXES = [("(-5,-2,2)  [the (2,2,1)-axis witness]", (-5, -2, 2)),
        ("(2,2,1)   exact", (2, 2, 1)),
        ("(1,1,0)   edge axis", (1, 1, 0))]

for label, ax in AXES:
    print(f"\naxis {label}")
    print(f"{'w':>5} {'theta':>8}  {'(deg2,deg4,deg6)':>18} {'weight':>7}  count")
    seen = collections.Counter()
    for w in list(range(0, 16)):
        q = (w,) + ax
        n2 = sum(v * v for v in q)
        if n2 == 0:
            continue
        theta = math.degrees(2 * math.acos(min(1.0, abs(w) / math.sqrt(n2))))
        qs = [(1, 0, 0, 0), q]
        try:
            det = pair_detail(qs)
            e = engine(qs)
        except Exception as ex:
            print(f"{w:>5} {theta:>8.3f}  error")
            continue
        c = det.get((0, 1), collections.Counter())
        wt = c[4] + 2 * c[6]
        seen[wt] += 1
        print(f"{w:>5} {theta:>8.3f}  ({c[2]:>3},{c[4]:>3},{c[6]:>3})"
              f"{'':>6} {wt:>7}  {e['bounded']}")
    print(f"  weights along this axis-family: {dict(sorted(seen.items()))}")
print("\nconstant weight along a curve => codimension 2 (the axis choice is the condition)")
print("weight 10 only at isolated w => codimension 3, useless for building T = 60")
