#!/usr/bin/env python3
"""Project the n=10 continuum DOWN to find the bounds of its n=9 base.

User's observation: a continuum does not extend UPWARD -- the n=10 count is not
constant on the n=9 continuum (it flips 3925 -> 3921 at t ~ 4.5/12) -- but it does
project DOWNWARD.  The n=10 region where the count is 3925, with the tenth cube
deleted, is exactly the set of n=9 bases that extend to 3925.  Its boundary is the
wall the walk found.  So mapping the n=10 region's extent gives the BASE's bounds.

This runs the walk past BOTH endpoints, so one pass finds two different boundaries:

    n=9 count leaves 2787   -> the edge of the n=9 CONTINUUM itself
    n=10 count leaves 3925  -> the edge of the PROJECTED n=10 region, i.e. the
                               sub-segment of that continuum which is a safe base

The second is contained in the first, and the gap between them is the region that
is a legitimate n=9 record but a WORSE base -- the thing representative choice has
been picking blind.
"""
import math, subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
ENG = os.path.join(HERE, "cube_regions_n")
SEVEN = [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1),
         (7,14,1,-5),(4,-3,-4,-4),(168,-168,168,-415)]
TENTH = (6555,6555,6497,6555)
A = (88787,-9061,74275,113786); B = (88726,-8954,74074,113960); N = 12

def count(qs):
    spec = ";".join(",".join(str(v) for v in q) for q in qs)
    out = subprocess.run([ENG,"--quats",spec],capture_output=True,text=True).stdout
    i = out.find('"bounded":')
    return int(out[i+10:out.find(",",i)]) if i >= 0 else None

def red(q):
    g = 0
    for v in q: g = math.gcd(g, abs(v))
    return tuple(v//g for v in q) if g else q

print(f"{'t':>5} {'n=9':>6} {'n=10':>6}   in continuum / good base")
prev9 = prev10 = None
for t in range(-24, 49, 3):
    q = red(tuple((N-t)*a + t*b for a,b in zip(A,B)))
    if not any(q) or max(abs(v) for v in q) > 10**8:
        continue
    nine = SEVEN + [q]
    c9, c10 = count(nine), count(nine + [TENTH])
    marks = []
    if prev9 is not None and (c9 == 2787) != (prev9 == 2787): marks.append("<< n=9 CONTINUUM edge")
    if prev10 is not None and (c10 == 3925) != (prev10 == 3925): marks.append("<< n=10 REGION edge")
    print(f"{t:>5} {str(c9):>6} {str(c10):>6}   "
          f"{'in' if c9 == 2787 else '--':>3} {'good' if c10 == 3925 else '    ':>5}  "
          f"{' '.join(marks)}")
    prev9, prev10 = c9, c10
print("\nthe n=9 continuum is the wider bracket; the 3925 base region sits inside it.")
