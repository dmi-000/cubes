#!/usr/bin/env python3
"""The recursion: does the face-vector argument reach depth k, not just depth 1?

A region of depth exactly k with membership S is a component of
K_S \\ (union of the others), where K_S = intersection of the bodies in S is
CONVEX.  So the depth-1 argument should apply verbatim with K_S in the role of a
single body -- the sphere is now dK_S, and the graph on it is dK_S n dC for the
remaining bodies C.

For k = 2 at n = 3 that graph is computable with the existing pieces: it is
G_AC clipped to the INSIDE of B, together with G_BC clipped to the inside of A,
and the two parts meet exactly at the triple points of dA n dB n dC.
"""
import itertools, json, os, subprocess, sys, collections
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from euler3 import rowsT, frames, segments

def clip_inside(p, d, lo, hi, M):
    """the sub-interval of [lo,hi] lying INSIDE the body with frame M"""
    a_, b_ = lo, hi
    for r in range(3):
        a = sum(M[r][t]*d[t] for t in range(3)); b = sum(M[r][t]*p[t] for t in range(3))
        if a == 0:
            if abs(b) > 1: return []
            continue
        t1, t2 = (F(-1)-b)/a, (F(1)-b)/a
        if t1 > t2: t1, t2 = t2, t1
        a_ = max(a_, t1); b_ = min(b_, t2)
    return [(a_, b_)] if a_ < b_ else []

def boundary_graph_K(qs, S, others):
    """the graph dK_S n (union of the other boundaries), drawn on the sphere dK_S"""
    Ms = [rowsT(R) for R in frames(qs)]
    pts = {}; links = []
    for i in S:
        for j in others:
            for p, d, lo, hi in segments(Ms[i], Ms[j]):
                parts = [(lo, hi)]
                for m in S:                       # keep only the part inside the OTHER members of S
                    if m == i: continue
                    nxt = []
                    for a, b in parts: nxt += clip_inside(p, d, a, b, Ms[m])
                    parts = nxt
                for a, b in parts:
                    if a >= b: continue
                    e = []
                    for t in (a, b):
                        P = tuple(p[z]+t*d[z] for z in range(3))
                        pts.setdefault(P, len(pts)); e.append(pts[P])
                    links.append(tuple(e))
    par = list(range(len(pts)))
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for a, b in links: par[f(a)] = f(b)
    c = len({f(x) for x in range(len(pts))}) if pts else 0
    return len(pts), len(links), c

if __name__ == '__main__':
    import random
    from edgecross import crossing_set
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 8)
    print("k = 2 at n = 3: the graph on dK_AB, against the depth-2 count with label {A,B}\n")
    print("   %5s %5s %3s %8s %10s %10s   %s" % ("V","E","c","E-V+c+1","N({A,B})","d2 total",""))
    hits = tot = 0
    for _ in range(400):
        qs = [(1,0,0,0)] + [tuple(rng.randint(-h,h) for _ in range(4)) for h in (rng.choice([7,11]),)*2]
        if any(all(v == 0 for v in q) for q in qs): continue
        if any(crossing_set([qs[a],qs[b]]) for a,b in itertools.combinations(range(3),2)): continue
        s = ";".join(",".join(map(str,q)) for q in qs)
        p = subprocess.run(["./cube_regions_n","--quats",s], capture_output=True, text=True,
                           cwd=os.path.dirname(os.path.abspath(__file__)))
        try: o = json.loads(p.stdout)
        except Exception: continue
        pl = o["per_label"]
        nAB = int(pl.get("3", 0))                     # bits 0 and 1 -> cubes A and B
        d2 = sum(int(v) for k, v in pl.items() if bin(int(k)).count("1") == 2)
        V, E, c = boundary_graph_K(qs, [0,1], [2])
        tot += 1
        ok = (E - V + c + 1 == nAB)
        hits += ok
        if tot <= 10:
            print("   %5d %5d %3d %8d %10d %10d   %s" % (V,E,c,E-V+c+1,nAB,d2,"YES" if ok else "no"))
        if tot >= 40: break
    print("\n   E - V + c + 1 == N({A,B}) in %d of %d coincidence-free triples" % (hits, tot))
