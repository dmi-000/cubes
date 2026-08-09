#!/usr/bin/env python3
"""Is a wall a STRATUM with its own constant count, or an isolated value?

At the 727 arc A end, s = 19/6, the count is 725 -- between the 727 inside and
the 723 beyond.  Scanning 290 integer Cayley directions from there finds NOTHING
holding 725, but that is the section 5 trap rather than a result: a W4 wall is an
algebraic surface whose tangent plane at a point is irrational, so integer
directions essentially never lie in it.

The right test moves to a NEIGHBOURING LINE and solves for its crossing of the
SAME wall.  Take the parallel line a0 + delta*e + s*d, find the W4 root near
19/6 belonging to the same triple point and face, and evaluate the count there.
If the wall carries 725 along two independent offsets, it is a 2-dimensional
stratum with a constant count of its own, not an isolated point.
"""
import json, os, subprocess, sys
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solve_ends import catalogue
from wall_params import line_polys, padd, pscale
from n78_ends import squarefree, exact_root, qstr, run

BASE = [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
a0 = [F(19,3), F(-7), F(-11)]; d = [F(1), F(-3), F(-6)]

def w4_terms(A, dv, pts):
    """(coefficients, identity) for every W4 quadratic on the line A + s*dv"""
    M, N = line_polys(A, dv)
    out = []
    for idx, (s_pt, npl, ncub) in enumerate(pts):
        for i in range(3):
            col = padd(*[pscale(M[k][i], F(s_pt[k])) for k in range(3)])
            for sign in (1, -1):
                p = padd(col, pscale(N, -sign))
                while p and p[-1] == 0: p = p[:-1]
                if len(p) >= 2: out.append((p, (idx, i, sign)))
    return out

pts, lines = catalogue(BASE)
base_s = ";".join(",".join("%d:0" % v for v in q) for q in BASE)

# which W4 condition is exactly satisfied at s = 19/6 on the original line?
active = []
for p, ident in w4_terms(a0, d, pts):
    v = sum(c * F(19,6)**k for k, c in enumerate(p))
    if v == 0: active.append(ident)
print("W4 conditions exactly active at the arc A end s = 19/6:", active, flush=True)

for e, ename in (([F(0),F(1),F(0)], "e=(0,1,0)"), ([F(0),F(0),F(1)], "e=(0,0,1)")):
    print("\noffsetting the line by delta*%s and re-solving the SAME wall:" % ename, flush=True)
    for delta in (F(0), F(1,64), F(1,32), F(1,16), F(-1,32)):
        A = [a0[i] + delta*e[i] for i in range(3)]
        hit = None
        for p, ident in w4_terms(A, d, pts):
            if ident not in active: continue
            if len(p) == 2:                         # linear: rational root
                r = -p[0]/p[1]
                hit = (r, F(0), 1, float(r)); break
            got = exact_root(p, 19/6, tol=0.05)
            if got: hit = (got[0], got[1], got[2], float(got[0])+float(got[1])*got[2]**0.5); break
        if not hit:
            print("   delta=%-7s no root of the same wall nearby" % delta); continue
        rp, rq, dd, sval = hit
        cay = [(A[i] + rp*d[i], rq*d[i]) for i in range(3)]
        qs, mag = qstr([(F(1), F(0))] + cay)
        c = run(base_s + ";" + qs, dd)
        print("   delta=%-7s s = %.9f in Q(sqrt %d), max component %-6d -> count %s"
              % (delta, sval, dd, mag, c), flush=True)
