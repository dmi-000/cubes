#!/usr/bin/env python3
"""WHERE along the continuum does the n=10 extension flip, and does anything at n=9 predict it?

[P285]: two n=9 representatives, same count and by_depth, extend to 3925 and 3921.
They are nearly parallel as quaternions -- scaling (109,-11,91,140) by ~814 gives
(88726,-8954,74074,113960) against (88787,-9061,74275,113786) -- so the segment
between them is short and can be walked exactly with integer interpolation
q(t) = (N-t)*A + t*B, which is projectively the straight path.

Three things measured at each step:
  n=9 count      -- must stay 2787 to confirm we are INSIDE the continuum
  n=10 count     -- with 6555,6555,6497,6555 appended; where does 3925 become 3921?
  outer vertices -- the candidate PREDICTOR.  A new cube is cut by the existing
                    ones' planes, so what it meets is the outer boundary; and the
                    better extender has MORE outer vertices (1126 vs 1108).  If that
                    tracks the flip, the n=9 level does predict the n=10 change.
"""
import math, subprocess, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from radii import vertices

HERE = os.path.dirname(os.path.abspath(__file__))
ENG = os.path.join(HERE, "cube_regions_n")
SEVEN = [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1),
         (7,14,1,-5),(4,-3,-4,-4),(168,-168,168,-415)]
TENTH = (6555,6555,6497,6555)
A = (88787,-9061,74275,113786)
B = (88726,-8954,74074,113960)          # (109,-11,91,140) scaled by 814

def count(qs):
    spec = ";".join(",".join(str(v) for v in q) for q in qs)
    out = subprocess.run([ENG,"--quats",spec],capture_output=True,text=True).stdout
    i = out.find('"bounded":')
    return int(out[i+10:out.find(",",i)]) if i >= 0 else None

def red(q):
    g = 0
    for v in q: g = math.gcd(g, abs(v))
    return tuple(v//g for v in q) if g else q

N = int(sys.argv[1]) if len(sys.argv) > 1 else 12
print(f"{'t/N':>6} {'n=9':>6} {'n=10':>6} {'outer V':>8}  height")
prev = None
for t in range(N+1):
    q = red(tuple((N-t)*a + t*b for a,b in zip(A,B)))
    nine = SEVEN + [q]
    c9 = count(nine)
    c10 = count(nine + [TENTH])
    try:
        ov = len(vertices(nine))
    except Exception:
        ov = None
    flag = ""
    if prev is not None and c10 != prev: flag = "   <-- n=10 FLIPS here"
    prev = c10
    print(f"{t:>3}/{N:<2} {str(c9):>6} {str(c10):>6} {str(ov):>8}  {max(abs(v) for v in q)}{flag}")
print("\nn=9 constant at 2787 => the whole path is inside the continuum.")
print("outer-vertex count tracking the n=10 flip => the n=9 level predicts it.")
