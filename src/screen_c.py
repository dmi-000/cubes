#!/usr/bin/env python3
"""Two-stage screen: reject a candidate before assembling its complex.

C = V + E - M + sum_i c_i + n - c.  Adding a cube q to a fixed base contributes
in two ways, with very different costs:

  CHEAP   the n new pairwise curves G_{q,i} -- one 36-face-plane intersection per
          base cube, and nothing touches the cached base curves;
  DEAR    cutting every cached base curve against dq, which is where a candidate's
          time actually goes.

RESULT: THIS DOES NOT WORK, and the direction of the error is the point.

The reasoning was that a new triple point on a base curve adds one 0-cell and one
1-cell and at least three to M, so contributes at most -1, making the cheap stage
an UPPER bound.  Wrong.  In C = V - E + F - c the added vertex and arc cancel in
V - E, while the cut SUBDIVIDES faces on both bodies sharing that curve, so F
grows and C grows with it.  Skipping the dear stage is therefore a LOWER bound,
and a low value says nothing:

    sixth cube        U(q)     C(q)
    (5,2,2,2)          121      723
    (7,14,1,-5)        118      727
    (4,-4,4,1)         124      717

Roughly a sixth of the true value -- far too loose to certify from below either.
A genuine cheap UPPER bound would have to bound the face growth, which means
bounding the number of cut points, which is exactly the expensive computation.
The only q-independent cap available (each base segment is cut at most 6 times by
the new cube's 6 planes) does not vary with the candidate and so cannot screen.

So the two-stage screen is not available by this route.  What survives from
extend_c.py is the exact incidence identity with the base amortised; making it
FASTER than the engine needs a different decomposition, not a cheaper first pass.
"""
import itertools, json, os, subprocess, sys, time
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from euler3 import rowsT, frames, segments
from cellcomplex import on_bdry_params
from extend_c import Base, engine

def assemble(Ms, seg, n, cut_pairs):
    node = {}; onb = {}; cells1 = []
    for (i, j), lst in seg.items():
        for p, d, lo, hi in lst:
            ks = [k for k in range(n) if k not in (i, j)] if (i, j) in cut_pairs else []
            cuts = sorted({lo, hi} | {t for k in ks
                                      for t in on_bdry_params(p, d, lo, hi, Ms[k])})
            for a, b in zip(cuts, cuts[1:]):
                if a >= b: continue
                ids = []
                for t in (a, b):
                    P = tuple(p[z]+t*d[z] for z in range(3))
                    if P not in node: node[P] = len(node); onb[node[P]] = set()
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

class Screen(Base):
    def bound(self, newq):
        """U(q) >= C(q), from the new curves only -- base curves left uncut"""
        Ms = self.M + [rowsT(frames([newq])[0])]; n = self.n + 1
        seg = dict(self.seg)
        for i in range(self.n): seg[(i, self.n)] = segments(Ms[i], Ms[self.n])
        new_pairs = {(i, self.n) for i in range(self.n)}
        return assemble(Ms, seg, n, new_pairs)
    def exact(self, newq):
        Ms = self.M + [rowsT(frames([newq])[0])]; n = self.n + 1
        seg = dict(self.seg)
        for i in range(self.n): seg[(i, self.n)] = segments(Ms[i], Ms[self.n])
        return assemble(Ms, seg, n, set(seg))

if __name__ == '__main__':
    import random, math
    B5 = [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
    S = Screen(B5)
    print("is U(q) an upper bound, and how tight?\n")
    print("   %-16s %8s %8s %8s"%("sixth cube","U(q)","C(q)","engine"))
    for q in [(5,2,2,2),(7,14,1,-5),(4,-4,4,1),(3,1,0,2),(6,-6,-5,6)]:
        u = S.bound(q); c = S.exact(q); a = engine(B5+[q])
        print("   %-16s %8s %8s %8d   %s"%(str(q),u,c,a,
              "bound OK" if u>=c else "*** NOT A BOUND ***"))
    rng = random.Random(3); tb=te=0.0; N=25; rej=0
    for _ in range(N):
        h=rng.choice([4,16,100]); q=tuple(rng.randint(-h,h) for _ in range(4))
        if not any(q): continue
        g=0
        for v in q: g=math.gcd(g,abs(v))
        q=tuple(v//g for v in q)
        t0=time.time(); u=S.bound(q); tb+=time.time()-t0
        if u < 727: rej+=1; continue
        t0=time.time(); S.exact(q); te+=time.time()-t0
    print("\n   screening at U >= 727 over %d candidates: %d rejected cheaply"%(N,rej))
    print("   stage-1 cost %.3f s total, stage-2 cost %.3f s on the %d survivors"%(tb,te,N-rej))
