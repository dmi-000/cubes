#!/usr/bin/env python3
"""Map the 183 plateau: is it ONE shape or two, and does position affect extension?

RESULTS records two 183s that are NOT congruent yet agree on every invariant
available -- by_depth {92,66,24,1}, pairs [13,13,13,9,9,9], triples [63,63,63,55],
symmetry order 3:

    A = 1,0,0,0;0,5,3,2;1,-4,-1,1;1,1,-1,-4        canonical
    B = 1,0,0,0;-2,-2,5,-2;3,11,-3,-3;0,-7,4,-3    wide-perturbation restart

Two questions, one walk.  Interpolating cubes 1..3 (both are gauge-fixed with cube
0 = identity) and clearing to integers:

  * is the count 183 along the path?  yes => one connected plateau, and their
    non-congruence is position on it.  no => at least two components, and
    "the 183 plateau" is really several.
  * does the n=5 EXTENSION vary along it?  the tower's 393 came from ONE point of
    this shape, so if extension varies the fifth cube was fitted to that point.

Extension here uses a small fixed set of fifth cubes; what matters is whether the
counts MOVE along the path, not whether they reach 393 (which needs the tower's own
gauge and cube).
"""
import math, subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
ENG = os.path.join(HERE, "cube_regions_n")
A = [(1,0,0,0),(0,5,3,2),(1,-4,-1,1),(1,1,-1,-4)]
B = [(1,0,0,0),(-2,-2,5,-2),(3,11,-3,-3),(0,-7,4,-3)]
FIFTH = [(2,1,1,1),(1,1,1,1),(3,1,-2,1),(5,-2,3,1),(7,3,-1,2)]

def count(qs):
    spec = ";".join(",".join(str(v) for v in q) for q in qs)
    out = subprocess.run([ENG,"--quats",spec],capture_output=True,text=True).stdout
    i = out.find('"bounded":')
    return int(out[i+10:out.find(",",i)]) if i >= 0 else None

def red(q):
    g = 0
    for v in q: g = math.gcd(g, abs(v))
    return tuple(v//g for v in q) if g else q

N = 10
print(f"{'t':>5} {'n=4':>5}   n=5 counts for five fifth cubes")
prev4 = None; prev5 = None
for t in range(0, N+1):
    cfg = [(1,0,0,0)] + [red(tuple((N-t)*a + t*b for a,b in zip(qa,qb)))
                         for qa,qb in zip(A[1:],B[1:])]
    c4 = count(cfg)
    c5 = [count(cfg+[f]) for f in FIFTH]
    mark = ""
    if prev4 is not None and (c4==183) != (prev4==183): mark += "  << n=4 count leaves 183"
    if prev5 is not None and c5 != prev5: mark += "  << n=5 changes"
    print(f"{t:>3}/{N} {str(c4):>5}   {c5}{mark}")
    prev4, prev5 = c4, c5
print("\n183 throughout => one connected plateau; n=5 varying => extension depends on position.")
