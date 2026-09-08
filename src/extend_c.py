#!/usr/bin/env python3
"""C for an EXTENSION, without rebuilding the base.

The exact count is C = V + E - M + sum_i c_i + n - c over the arrangement complex
(delta_c.py, verified on every record).  For extension search the base is fixed
and only the new cube's interactions change, so the base's pairwise curves --
the expensive part, 36 face-plane intersections per pair -- are computed ONCE and
cached.  Per candidate the work is n new curves plus re-cutting the cached ones
against a single extra body.

This is the filter: an exact C from incidence data, with the base amortised.
"""
import itertools, json, os, subprocess, sys, time
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from euler3 import rowsT, frames, segments
from cellcomplex import on_bdry_params

class Base:
    def __init__(self, quats):
        self.q = list(quats)
        self.M = [rowsT(R) for R in frames(self.q)]
        self.n = len(self.q)
        self.seg = {}                                   # cached, never recomputed
        for i, j in itertools.combinations(range(self.n), 2):
            self.seg[(i, j)] = segments(self.M[i], self.M[j])

    def C(self, newq):
        Ms = self.M + [rowsT(frames([newq])[0])]
        n = self.n + 1
        seg = dict(self.seg)
        for i in range(self.n):                         # only the new pairs
            seg[(i, self.n)] = segments(Ms[i], Ms[self.n])
        node = {}; onb = {}; cells1 = []
        for (i, j), lst in seg.items():
            for p, d, lo, hi in lst:
                cuts = sorted({lo, hi} | {t for k in range(n) if k not in (i, j)
                                          for t in on_bdry_params(p, d, lo, hi, Ms[k])})
                for a, b in zip(cuts, cuts[1:]):
                    if a >= b: continue
                    ids = []
                    for t in (a, b):
                        P = tuple(p[z]+t*d[z] for z in range(3))
                        if P not in node:
                            node[P] = len(node); onb[node[P]] = set()
                        onb[node[P]] |= {i, j}; ids.append(node[P])
                    cells1.append((tuple(ids), (i, j)))
        for P, idx in node.items():
            for k in range(n):
                if k in onb[idx]: continue
                v = [abs(sum(Ms[k][r][z]*P[z] for z in range(3))) for r in range(3)]
                if max(v) == 1 and all(x <= 1 for x in v): onb[idx].add(k)
        V = len(node); E = len(cells1); M = sum(len(onb[i]) for i in onb)
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
        par = {x: x for x in range(V)}
        def g(x):
            while par[x] != x: par[x] = par[par[x]]; x = par[x]
            return x
        for (a, b), pr in cells1: par[g(a)] = g(b)
        c = len({g(x) for x in range(V)}) if V else 0
        return V + E - M + sc + n - c

def engine(qs):
    p = subprocess.run(["./cube_regions_n", "--quats",
                        ";".join(",".join(map(str,q)) for q in qs)],
                       capture_output=True, text=True, cwd=HERE)
    return json.loads(p.stdout)["bounded"]

if __name__ == '__main__':
    B5 = [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
    tests = [(5,2,2,2), (7,14,1,-5), (4,-4,4,1), (6,-6,-5,6), (1,1,1,1), (3,1,0,2)]
    t0 = time.time(); base = Base(B5); tbuild = time.time()-t0
    print("base built once in %.2f s (its %d pairwise curve sets cached)\n"
          % (tbuild, len(base.seg)))
    print("   %-16s %8s %8s   %s" % ("sixth cube", "C (incid.)", "engine", ""))
    ok = 0
    t0 = time.time()
    for q in tests:
        c = base.C(q); a = engine(B5+[q])
        ok += (c == a)
        print("   %-16s %8s %8d   %s" % (str(q), c, a, "OK" if c == a else "MISMATCH"))
    print("\n   %d of %d exact;  %.2f s for %d candidates (%.2f s each)"
          % (ok, len(tests), time.time()-t0, len(tests), (time.time()-t0)/len(tests)))
