#!/usr/bin/env python3
"""Does the face-vector relation of METHODS section 11 survive to n = 3?

At n = 2 the derivation was: d(A u B) is a sphere tiled by the OUTSIDE faces of
both bodies, so d1 = O_A + O_B = E - V + c + 1 for the curve G = dA n dB.

Nothing in that argument used n = 2 except the shape of the union.  For n cubes,
d(A_1 u ... u A_n) is still a sphere (the union is a ball whenever it is
connected), and it is tiled by the faces of each dA_i lying OUTSIDE every other
body.  So the prediction is

    d1 = E - V + c + 1

for the graph drawn on that outer sphere: the pairwise intersection curves
CLIPPED to the exterior of all the other bodies, whose new endpoints are exactly
the triple points where three boundaries meet.
"""
import itertools, json, os, subprocess, sys, collections
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from edgecross import rotF

def frames(qs): return [rotF(q) for q in qs]
def rowsT(R): return [[R[k][i] for k in range(3)] for i in range(3)]

def inside(M, P, strict=False):
    for r in range(3):
        v = sum(M[r][k]*P[k] for k in range(3))
        if (v > 1 or v < -1) if not strict else (v >= 1 or v <= -1): return False
    return True

def segments(Ma, Mb):
    """the segments of dA n dB, as (point, direction, t_lo, t_hi)"""
    out = []
    for i in range(3):
      for si in (1, -1):
        for j in range(3):
          for sj in (1, -1):
            n1, c1 = Ma[i], F(si); n2, c2 = Mb[j], F(sj)
            d = [n1[1]*n2[2]-n1[2]*n2[1], n1[2]*n2[0]-n1[0]*n2[2], n1[0]*n2[1]-n1[1]*n2[0]]
            if not any(d): continue
            k = max(range(3), key=lambda t: abs(d[t])); u, v = [t for t in range(3) if t != k]
            det = n1[u]*n2[v] - n1[v]*n2[u]
            if det == 0: continue
            p = [F(0)]*3
            p[u] = (c1*n2[v]-c2*n1[v])/det; p[v] = (n1[u]*c2-n2[u]*c1)/det
            lo = hi = None
            for M in (Ma, Mb):
                for r in range(3):
                    a = sum(M[r][t]*d[t] for t in range(3)); b = sum(M[r][t]*p[t] for t in range(3))
                    if a == 0:
                        if abs(b) > 1: lo, hi = F(1), F(0)
                        continue
                    t1, t2 = (F(-1)-b)/a, (F(1)-b)/a
                    if t1 > t2: t1, t2 = t2, t1
                    lo = t1 if lo is None else max(lo, t1); hi = t2 if hi is None else min(hi, t2)
            if lo is None or lo >= hi: continue
            out.append((p, d, lo, hi))
    return out

def clip_outside(p, d, lo, hi, M):
    """the sub-intervals of [lo,hi] lying OUTSIDE the body with frame M"""
    ins_lo, ins_hi = lo, hi
    for r in range(3):
        a = sum(M[r][t]*d[t] for t in range(3)); b = sum(M[r][t]*p[t] for t in range(3))
        if a == 0:
            if abs(b) > 1: return [(lo, hi)]
            continue
        t1, t2 = (F(-1)-b)/a, (F(1)-b)/a
        if t1 > t2: t1, t2 = t2, t1
        ins_lo = max(ins_lo, t1); ins_hi = min(ins_hi, t2)
    if ins_lo >= ins_hi: return [(lo, hi)]
    out = []
    if lo < ins_lo: out.append((lo, ins_lo))
    if ins_hi < hi: out.append((ins_hi, hi))
    return out

def outer_graph(qs):
    Ms = [rowsT(R) for R in frames(qs)]
    n = len(qs)
    pts = {}; edges = 0; links = []
    for i, j in itertools.combinations(range(n), 2):
        for p, d, lo, hi in segments(Ms[i], Ms[j]):
            parts = [(lo, hi)]
            for k in range(n):
                if k in (i, j): continue
                nxt = []
                for a, b in parts: nxt += clip_outside(p, d, a, b, Ms[k])
                parts = nxt
            for a, b in parts:
                if a >= b: continue
                e = []
                for t in (a, b):
                    P = tuple(p[z] + t*d[z] for z in range(3))
                    pts.setdefault(P, len(pts)); e.append(pts[P])
                links.append(tuple(e)); edges += 1
    par = list(range(len(pts)))
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for a, b in links: par[f(a)] = f(b)
    c = len({f(x) for x in range(len(pts))}) if pts else 0
    return pts, edges, c

def run(qs):
    s = ";".join(",".join(map(str, q)) for q in qs)
    p = subprocess.run(["./cube_regions_n", "--quats", s], capture_output=True, text=True,
                       cwd=os.path.dirname(os.path.abspath(__file__)))
    return json.loads(p.stdout)

if __name__ == '__main__':
    import random
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 4)
    print("n = 3: d1 against the Euler count on the OUTER sphere d(A u B u C)\n")
    print("   %-30s %5s %5s %3s %6s %6s   %s" % ("quaternions", "V", "E", "c", "E-V+c+1", "d1", "match"))
    ok = bad = 0
    for trial in range(20):
        qs = [(1,0,0,0)]
        for _ in range(2):
            h = rng.choice([2,3,5]); qs.append(tuple(rng.randint(-h,h) for _ in range(4)))
        if any(all(v == 0 for v in q) for q in qs): continue
        o = run(qs)
        pl = o["per_label"]
        d1 = sum(int(v) for k, v in pl.items() if bin(int(k)).count("1") == 1)
        pts, E, c = outer_graph(qs)
        V = len(pts); pred = E - V + c + 1
        print("   %-30s %5d %5d %3d %6d %6d   %s"
              % (";".join(",".join(map(str,q)) for q in qs[1:]), V, E, c, pred, d1,
                 "YES" if pred == d1 else "NO"))
        if pred == d1: ok += 1
        else: bad += 1
    print("\n   d1 = E - V + c + 1 holds in %d of %d" % (ok, ok+bad))
