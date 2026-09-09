#!/usr/bin/env python3
"""Is the wall a property of the BASE, or of the (base, added cube) PAIR?

extend_across_continuum.py found all 11 tenth cubes dropping by 4 at the same t --
but those cubes were 0.03% apart (components ~6555 differing by 1-2), so it tested
ONE cube eleven times.  Cube-independence is unanswered.

Here the tenth cubes are genuinely different -- different magnitudes and directions,
not perturbations.  Their COUNTS will be far below 3925 and that does not matter:
the question is WHERE each one's count changes along t.  Same wall position for
unrelated cubes => the wall belongs to the base, and a single good sub-region of the
continuum serves every extension.  Different positions => base and added cube must
be chosen together, and "the right point of the plateau" is not well defined alone.
"""
import math, subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
ENG = os.path.join(HERE, "cube_regions_n")
SEVEN = [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1),
         (7,14,1,-5),(4,-3,-4,-4),(168,-168,168,-415)]
A = (88787,-9061,74275,113786); B = (88726,-8954,74074,113960); N = 12
CUBES = [("record", (6555,6555,6497,6555)),
         ("small A", (3,1,-2,1)),
         ("small B", (5,-2,3,1)),
         ("mid",     (41,17,-23,9)),
         ("far",     (1000,-997,13,5)),
         ("axis",    (7,0,0,-3))]

def count(qs):
    spec = ";".join(",".join(str(v) for v in q) for q in qs)
    out = subprocess.run([ENG,"--quats",spec],capture_output=True,text=True).stdout
    i = out.find('"bounded":')
    return int(out[i+10:out.find(",",i)]) if i >= 0 else None

def red(q):
    g = 0
    for v in q: g = math.gcd(g, abs(v))
    return tuple(v//g for v in q) if g else q

TS = [0, 3, 6, 9, 12, 15, 18, 21, 24]
print(f"{'cube':>9}  " + " ".join(f"t={t:<4}" for t in TS) + "   wall between")
for name, c in CUBES:
    row = []
    for t in TS:
        q = red(tuple((N-t)*a + t*b for a,b in zip(A,B)))
        row.append(count(SEVEN + [q, c]))
    walls = [f"{TS[i]}-{TS[i+1]}" for i in range(len(row)-1)
             if row[i] is not None and row[i+1] is not None and row[i] != row[i+1]]
    print(f"{name:>9}  " + " ".join(f"{str(v):<6}" for v in row) +
          f"   {', '.join(walls) if walls else 'NONE (flat)'}")
print("\nsame wall position for unrelated cubes => the wall belongs to the BASE.")
