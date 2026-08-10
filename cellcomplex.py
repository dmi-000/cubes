#!/usr/bin/env python3
"""The total region count as one Euler characteristic of the arrangement complex.

U = A_1 u ... u A_n is a ball, so chi(U) = 1 and the arrangement gives it a CW
structure whose 3-cells ARE the bounded regions:

    0-cells   endpoints of the pairwise intersection curves, and the triple
              points where a curve meets a third boundary
    1-cells   the arcs between consecutive 0-cells (each shared by two dA_i)
    2-cells   the faces the arcs cut on each dA_i
    3-cells   the regions

Built against the control: a body-diagonal pair must return 13.
"""
import itertools, json, os, subprocess, sys
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from euler3 import rowsT, frames, segments

def on_bdry_params(p, d, lo, hi, M):
    """t in (lo,hi) where p+td lies ON the boundary of the body with frame M"""
    out = []
    for r in range(3):
        a = sum(M[r][k]*d[k] for k in range(3)); b = sum(M[r][k]*p[k] for k in range(3))
        if a == 0: continue
        for s in (F(1), F(-1)):
            t = (s-b)/a
            if not (lo < t < hi): continue
            P = [p[k]+t*d[k] for k in range(3)]
            if all(abs(sum(M[q][k]*P[k] for k in range(3))) <= 1 for q in range(3)):
                out.append(t)
    return out

def complexus(qs):
    Ms = [rowsT(R) for R in frames(qs)]; n = len(qs)
    node = {}; cells1 = []; on_body = {}
    for i, j in itertools.combinations(range(n), 2):
        for p, d, lo, hi in segments(Ms[i], Ms[j]):
            cuts = sorted({lo, hi} | {t for k in range(n) if k not in (i, j)
                                      for t in on_bdry_params(p, d, lo, hi, Ms[k])})
            for a, b in zip(cuts, cuts[1:]):
                if a >= b: continue
                ids = []
                for t in (a, b):
                    P = tuple(p[z]+t*d[z] for z in range(3))
                    node.setdefault(P, len(node)); ids.append(node[P])
                cells1.append((tuple(ids), (i, j)))
    V = len(node); E = len(cells1)
    Ftot = 0
    for i in range(n):
        arcs = [c for c, pr in cells1 if i in pr]
        vs = {x for c in arcs for x in c}
        par = {x: x for x in vs}
        def f(x):
            while par[x] != x: par[x] = par[par[x]]; x = par[x]
            return x
        for a, b in arcs: par[f(a)] = f(b)
        ci = len({f(x) for x in vs}) if vs else 0
        Ftot += len(arcs) - len(vs) + ci + 1
    # components of the whole 1-skeleton
    par = {x: x for x in range(V)}
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for (a, b), pr in cells1: par[f(a)] = f(b)
    c = len({f(x) for x in range(V)}) if V else 0
    return V, E, Ftot, c

def count(qs):
    p = subprocess.run(["./cube_regions_n", "--quats",
                        ";".join(",".join(map(str,q)) for q in qs)],
                       capture_output=True, text=True, cwd=HERE)
    return json.loads(p.stdout)["bounded"]

if __name__ == '__main__':
    print("CONTROL FIRST: a body-diagonal pair must return 13\n")
    tests = [("13 body diagonal", [(1,0,0,0),(10,3,3,3)]),
             ("13 edge arc",      [(1,0,0,0),(4,3,3,0)]),
             ("9",                [(1,0,0,0),(10,3,3,4)]),
             ("5",                [(1,0,0,0),(2,-23,-22,1)]),
             ("4 generic",        [(1,0,0,0),(10,3,5,7)])]
    print("   %-18s %4s %4s %5s %3s   %-24s %s" % ("case","V","E","F","c","V-E+F-c","actual"))
    for name, qs in tests:
        V,E,Ft,c = complexus(qs); a = count(qs)
        print("   %-18s %4d %4d %5d %3d   %-24d %d  %s"
              % (name,V,E,Ft,c,V-E+Ft-c,a,"OK" if V-E+Ft-c==a else "MISMATCH"))
