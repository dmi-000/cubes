#!/usr/bin/env python3
"""Name the wall at the lower end of the n = 9 continuum, exactly.

In quaternion form the ninth cube runs q(k) = k*(1,1,1,1) + (1,1,0,1)
           = (k+1, k+1, k, k+1),
so in CAYLEY coordinates it is simply

    (1, t, 1)      with t = k/(k+1),

a coordinate-axis line.  2785 holds for k >= 55, i.e. t >= 55/56, and t = 1 is the
degeneracy where the ninth cube duplicates the base's fifth.  So the continuum is
t in [55/56, 1) and its one wall end sits just below 55/56.  Solve for it: build
the W3/W4 catalogue of the EIGHT-cube base and take the roots on this line.
"""
import sys, os
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solve_ends import catalogue, q_of, count
import wall_params as W

EIGHT = [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1),
         (7,14,1,-5),(4,-3,-4,-4),(24,-24,24,-61)]
a0 = [F(1), F(0), F(1)]; d = [F(0), F(1), F(0)]

print("building the 8-cube catalogue ...", flush=True)
pts, lines = catalogue(EIGHT)
print("   %d real triple points, %d crossing lines" % (len(pts), len(lines)), flush=True)
w4 = W.w4_params(a0, d, pts); w3 = W.w3_params(a0, d, lines)
kind = {}
for s in w3: kind[s] = 'W3'
for s in w4: kind[s] = 'W4'
print("   %d W4 + %d W3 roots on the line (1, t, 1)" % (len(w4), len(w3)), flush=True)

LO, HI = F(9, 10), F(1)
roots = sorted(s for s in set(w3) | set(w4) if LO < s < HI)
print("   %d roots in t in (%s, 1)\n" % (len(roots), LO), flush=True)

def between(a, b):
    for k in range(1, 60):
        D = 2**k
        m = F(int(float(a+b)/2*D), D)
        if a < m < b: return m
    return (a+b)/2

pos = [LO] + roots + [HI]
prev = None
for i in range(len(pos)-1):
    m = between(pos[i], pos[i+1])
    c = count(EIGHT + [q_of([a0[j]+m*d[j] for j in range(3)])])
    if c != prev:
        k = kind.get(pos[i], 'window')
        print("   count %-6s from t = %.12f  (%s)   k = %.4f"
              % (c, float(pos[i]), k, float(pos[i]/(1-pos[i])) if pos[i] < 1 else float('inf')),
              flush=True)
        prev = c
print("\n   55/56 = %.12f  (k = 55)" % float(F(55,56)))
print("   the degeneracy t = 1 counts", count(EIGHT + [(1,1,1,1)]))
