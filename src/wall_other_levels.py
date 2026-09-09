#!/usr/bin/env python3
"""Does the same structure appear at ANOTHER level?  The 727 arc, n=6 -> n=7.

Everything so far is the n=9 -> n=10 step on a single arc.  The 727 continuum is
the other fully mapped one (MAXIMISERS): sixth cube at Cayley point
(19/3,-7,-11) + s*(1,-3,-6), count 727 for s in [9/4, 3], 721 at s=2, 723 at 13/4.
A Cayley point (x,y,z) is the quaternion (1,x,y,z), so P(s) = (1, 19/3+s, -7-3s,
-11-6s), cleared to integers.  (Check: s=5/2 -> (6,53,-87,-156) and s=3 ->
(3,28,-48,-87), both listed in MAXIMISERS.)

Measured across and beyond the arc: the n=6 count (locating the continuum's own
edges) and the n=7 count with the record's seventh cube 4,-3,-4,-4 (locating the
extension wall).  If the good sub-region is again a fraction of the continuum, the
n=9 finding is a level-independent phenomenon; if the n=7 count is flat across the
arc, it was specific to that step.

NOTE: the tower's own sixth cube is 7,14,1,-5, which is NOT on this arc, so the
n=7 counts here need not reach 1217.  What matters is whether they VARY.
"""
import math, subprocess, sys, os
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
ENG = os.path.join(HERE, "cube_regions_n")
BASE = [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
SEVENTH = (4,-3,-4,-4)

def count(qs):
    spec = ";".join(",".join(str(v) for v in q) for q in qs)
    out = subprocess.run([ENG,"--quats",spec],capture_output=True,text=True).stdout
    i = out.find('"bounded":')
    return int(out[i+10:out.find(",",i)]) if i >= 0 else None

def P(s):
    c = [F(1), F(19,3)+s, F(-7)-3*s, F(-11)-6*s]
    d = 1
    for x in c: d = d*x.denominator // math.gcd(d, x.denominator)
    q = tuple(int(x*d) for x in c)
    g = 0
    for v in q: g = math.gcd(g, abs(v))
    return tuple(v//g for v in q) if g else q

print(f"{'s':>8} {'sixth cube':>22} {'n=6':>6} {'n=7':>6}   arc / extension")
prev6 = prev7 = None
for k in range(14, 30):
    s = F(k, 6)
    q = P(s)
    six = BASE + [q]
    c6, c7 = count(six), count(six + [SEVENTH])
    marks = []
    if prev6 is not None and (c6 == 727) != (prev6 == 727): marks.append("<< n=6 ARC edge")
    if prev7 is not None and c7 != prev7 and c6 == 727 == prev6: marks.append("<< n=7 WALL inside the arc")
    print(f"{str(s):>8} {str(q):>22} {str(c6):>6} {str(c7):>6}   "
          f"{'arc' if c6 == 727 else '---':>3}  {' '.join(marks)}")
    prev6, prev7 = c6, c7
print("\nn=7 varying while n=6 stays 727 => the same structure at another level.")
