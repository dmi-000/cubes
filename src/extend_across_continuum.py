#!/usr/bin/env python3
"""Extend OTHER members of the n=9 continuum upward, and measure how much the
continuum shrinks when it is.

Two questions, one grid.

(1) DOES ANOTHER POINT EXTEND BETTER?  3925 was found by extending ONE point of a
    4-dimensional n=9 continuum ([P200], "automated boundary climb"), and that
    point sits at the EDGE of the continuum (t=0; t=-3 already leaves it).  Nothing
    has asked whether a different member extends further.  A count above 3925 here
    is a new n=10 record.

(2) HOW MUCH DOES THE CONTINUUM SHRINK?  Along this line the n=9 plateau is
    t in [0,24] and the sub-segment extending to 3925 is t in [0,~5] -- about a
    fifth.  Measured per tenth cube, that ratio is a statistic about how much
    freedom a level costs, and if it is roughly constant it is a law about the
    tower rather than a fact about this arc.

Grid: t across the continuum x a small set of tenth cubes (the record's, plus
perturbations of it).  For each t the MAX over cubes is what matters for (1); for
each cube the width of its good set is what matters for (2).
"""
import math, subprocess, sys, os, collections
HERE = os.path.dirname(os.path.abspath(__file__))
ENG = os.path.join(HERE, "cube_regions_n")
SEVEN = [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1),
         (7,14,1,-5),(4,-3,-4,-4),(168,-168,168,-415)]
A = (88787,-9061,74275,113786); B = (88726,-8954,74074,113960); N = 12
BASE10 = (6555,6555,6497,6555)
CUBES = [BASE10] + [tuple(c + d for c, d in zip(BASE10, off)) for off in
                    ((1,0,0,0),(-1,0,0,0),(0,1,0,0),(0,-1,0,0),(0,0,1,0),
                     (0,0,-1,0),(0,0,0,1),(0,0,0,-1),(2,0,0,-2),(-2,2,0,0))]

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
best_by_cube = collections.defaultdict(list)
print(f"{'t':>4} {'n=9':>6} {'best n=10':>10} {'by cube':>8}  counts across the 11 tenth cubes")
overall = None
for t in TS:
    q = red(tuple((N-t)*a + t*b for a,b in zip(A,B)))
    nine = SEVEN + [q]
    c9 = count(nine)
    res = []
    for c in CUBES:
        v = count(nine + [c])
        res.append(v)
        best_by_cube[c].append((t, v))
    m = max(x for x in res if x)
    if overall is None or m > overall[0]:
        overall = (m, t, CUBES[res.index(m)])
    print(f"{t:>4} {str(c9):>6} {m:>10} {res.index(m):>8}  {res}")

print(f"\nbest overall: {overall[0]} at t={overall[1]} with tenth cube {overall[2]}")
print(f"  (the published n=10 record is 3925)")
print("\nCONTINUUM SHRINKAGE -- for each tenth cube, how many of the 9 sampled t")
print("values reach that cube's own maximum:")
for c, rows in best_by_cube.items():
    vals = [v for _, v in rows if v]
    if not vals:
        continue
    mx = max(vals)
    w = sum(1 for v in vals if v == mx)
    print(f"  cube {str(c):<28} max {mx}  attained at {w}/{len(vals)} points "
          f"({w/len(vals):.0%} of the continuum sampled)")
