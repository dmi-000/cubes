#!/usr/bin/env python3
"""SOLVE for ninth cubes making 13-pairs, instead of sampling and testing.

A pair of cubes counts 13 exactly when their relative rotation lies on one of the
two known n = 2 arcs (MAXIMISER_TAXONOMY section 3) or at one of the isolated
half-turns.  The body-diagonal arc is the whole one-parameter family

    r(t) = (1, t*a)     for a a body diagonal, any t, t != 0, +-1

so the set of ninth cubes forming a 13-pair with base cube b is exactly the curve
q = b * r(t) -- known in closed form, not something to search for.  Asking for
TWO 13-pairs at once intersects two such curves:

    q = b_i * (1, t*a1)  ~  b_j * (1, u*a2)      (projectively)

Writing m = conj(b_j) * b_i, the condition is that the vector part of
m*(1, t*a1) be parallel to a2, i.e. A + tB = 0 with A = mv x a2 and
B = (mw*a1 + mv x a1) x a2 -- two linear equations in one unknown.  Consistent
systems give exact solutions; that is the whole search, 28 base pairs x 16 axis
pairs, no sampling anywhere.
"""
import itertools, json, os, subprocess, sys
from fractions import Fraction as F
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
EIGHT = [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1),
         (7,14,1,-5),(4,-3,-4,-4),(24,-24,24,-61)]
DIAG = [(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]

def qmul(p,q):
    w,x,y,z=p; e,f,g,h=q
    return (w*e-x*f-y*g-z*h, w*f+x*e+y*h-z*g, w*g-x*h+y*e+z*f, w*h+x*g-y*f+z*e)
def conj(q): return (q[0],-q[1],-q[2],-q[3])
def cross(a,b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def red(v):
    g=0
    for x in v: g=gcd(g,abs(x))
    v=tuple(x//g for x in v) if g else v
    for x in v:
        if x>0: break
        if x<0: return tuple(-y for y in v)
    return v
def intq(fq):
    L=1
    for x in fq: L=L*x.denominator//gcd(L,x.denominator)
    return red(tuple(int(x*L) for x in fq))

def solve(bi, bj, a1, a2):
    """t with conj(bj)*bi*(1,t a1) having vector part parallel to a2"""
    m = qmul(conj(bj), bi); mw, mv = m[0], m[1:]
    A = cross(mv, a2)
    B = cross(tuple(mw*a1[k] for k in range(3)), a2)
    B = tuple(B[k] + cross(cross(mv,a1), a2)[k] for k in range(3))
    t = None
    for k in range(3):
        if B[k] == 0:
            if A[k] != 0: return None
        else:
            tk = F(-A[k], B[k])
            if t is None: t = tk
            elif t != tk: return None
    return t

def count(cfg):
    m = max(abs(v) for q in cfg for v in q)
    eng = ["./cube_regions_n"] if m <= 512 else ["./cube_regions_q2w","--d","0"]
    p = subprocess.run(eng+["--quats", ";".join(",".join(map(str,q)) for q in cfg)],
                       capture_output=True, text=True, cwd=HERE)
    try: return json.loads(p.stdout)["bounded"]
    except Exception: return None

sols = {}
for (i,j) in itertools.combinations(range(8),2):
    for a1 in DIAG:
        for a2 in DIAG:
            t = solve(EIGHT[i], EIGHT[j], a1, a2)
            if t is None or t == 0 or abs(t) == 1: continue
            q = intq([F(x) for x in qmul(EIGHT[i], (1, t*a1[0], t*a1[1], t*a1[2]))])
            if max(abs(v) for v in q) > 512: continue
            sols.setdefault(q, []).append((i,j,a1,a2,t))
print("exact solutions of the two-simultaneous-13-pair system: %d distinct ninth cubes"
      % len(sols), flush=True)
res = []
for q, why in sorted(sols.items()):
    lab = [count([b, q]) for b in EIGHT]
    c = count(EIGHT+[q])
    res.append((c, q, lab.count(13), lab.count(9)))
res.sort(reverse=True)
print("\n   %-6s %-22s %s" % ("count", "ninth cube", "pair profile"))
for c, q, n13, n9 in res[:14]:
    print("   %-6s %-22s %dx13 %dx9" % (c, str(q), n13, n9), flush=True)
print("\nbest from the solve: %s   (random near-symmetry search reached 2785)"
      % (res[0][0] if res else None))
