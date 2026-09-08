#!/usr/bin/env python3
"""C without counting: the arrangement complex, and its INCREMENT under extension.

C = V - E + F - c is exact (cellcomplex.py, 13 of 13 including every record), so
it is a handle for solving, bounding and filtering rather than a counter -- the
C++ engine will always count faster.  Two things fall out of it.

REWRITTEN.  Every 1-cell lies on exactly 2 bodies and every 0-cell on 2 (an
edge-face incidence) or 3 (a triple point), so sum_i E_i = 2E and
sum_i V_i = 2*V2 + 3*V3, giving F = 2E - 2*V2 - 3*V3 + sum_i c_i + n and

    C  =  E - V2 - 2*V3 + sum_i c_i + n - c

which is the same count in terms of incidences alone, with the triple points
carrying weight -2 and the edge-face incidences -1.

INCREMENTAL.  Extending a fixed base by one cube changes only the terms the new
cube touches: n new pairwise curves rather than all C(n,2), plus the triple
points it creates on the base's existing curves.  That is the filter -- screen
extension candidates on the incidence delta, and count only survivors.
"""
import itertools, json, os, subprocess, sys
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from cellcomplex import complexus, count
from euler3 import rowsT, frames, segments

def parts(qs):
    """(V2, V3, E, sum_i c_i, c) for the arrangement complex"""
    from cellcomplex import on_bdry_params
    Ms = [rowsT(R) for R in frames(qs)]; n = len(qs)
    node = {}; cells1 = []; onbody = {}
    for i, j in itertools.combinations(range(n), 2):
        for p, d, lo, hi in segments(Ms[i], Ms[j]):
            cuts = sorted({lo, hi} | {t for k in range(n) if k not in (i, j)
                                      for t in on_bdry_params(p, d, lo, hi, Ms[k])})
            for a, b in zip(cuts, cuts[1:]):
                if a >= b: continue
                ids = []
                for t in (a, b):
                    P = tuple(p[z]+t*d[z] for z in range(3))
                    if P not in node:
                        node[P] = len(node)
                        onbody[node[P]] = set()
                    onbody[node[P]] |= {i, j}
                    ids.append(node[P])
                cells1.append((tuple(ids), (i, j)))
    for P, idx in node.items():
        for k in range(n):
            if k in onbody[idx]: continue
            if all(abs(sum(Ms[k][q][z]*P[z] for z in range(3))) <= 1 for q in range(3)) and \
               any(abs(sum(Ms[k][q][z]*P[z] for z in range(3))) == 1 for q in range(3)):
                onbody[idx].add(k)
    V3 = sum(1 for idx in onbody if len(onbody[idx]) >= 3)
    V2 = len(node) - V3
    sc = 0
    for i in range(n):
        arcs = [cc for cc, pr in cells1 if i in pr]
        vs = {x for cc in arcs for x in cc}
        par = {x: x for x in vs}
        def f(x, par=par):
            while par[x] != x: par[x] = par[par[x]]; x = par[x]
            return x
        for a, b in arcs: par[f(a)] = f(b)
        sc += len({f(x) for x in vs}) if vs else 0
    par = {x: x for x in range(len(node))}
    def g(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for (a, b), pr in cells1: par[g(a)] = g(b)
    c = len({g(x) for x in range(len(node))}) if node else 0
    return V2, V3, len(cells1), sc, c

if __name__ == '__main__':
    B = [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
    cases = [("13 body diagonal", [(1,0,0,0),(10,3,3,3)]),
             ("183", [(1,0,0,0),(0,5,3,2),(1,-4,-1,1),(1,1,-1,-4)]),
             ("393", B), ("723", B+[(5,2,2,2)]), ("727 RECORD", B+[(7,14,1,-5)])]
    print("C = E - V2 - 2*V3 + sum_i c_i + n - c\n")
    print("   %-18s %5s %5s %6s %5s %3s %8s %7s"%("case","V2","V3","E","sum c","c","formula","actual"))
    for name, qs in cases:
        V2,V3,E,sc,c = parts(qs); n = len(qs)
        pred = E - V2 - 2*V3 + sc + n - c
        a = count(qs)
        print("   %-18s %5d %5d %6d %5d %3d %8d %7d  %s"
              %(name,V2,V3,E,sc,c,pred,a,"OK" if pred==a else "MISMATCH"))
