#!/usr/bin/env python3
"""Dimension of the maximiser locus in the FULL gauge-fixed space, not a slice.

Every sweep in this project moves only the LAST cube — a 3-dimensional slice of the
3(n-1)-dimensional space. [P184] gives a lower bound on the true dimension,
max(0, deficit-1), and [P194] showed the slice can badly understate it: 2785 looks
1-dimensional in its slice and should be 3-dimensional overall.

METHOD. The count-preserving set is a union of relatively open cones, not necessarily
a subspace — 727's arc D is two curves crossing at a NODE, where both tangents
preserve but no combination does. So dimension is measured by GROWING A SUBSPACE:
keep a basis B; a new candidate joins only if it preserves AND enough integer
combinations with the existing basis also preserve. That returns a verified-preserving
SUBSPACE, hence a lower bound on the locus dimension, and it cannot merge a node.

Candidates, cheapest first: the null-space basis of the wall matrix (directions
crossing no wall at all), then rank-2 null directions within the last-cube slice
(which is where the 3917 surface lives), then coordinate directions.

Everything verified with eps, both signs, wide engine on refusal; unevaluable is
counted, never scored as a failure.

GATE: 727 must come back dimension 1 (two tangents, node, no 2-dimensional subspace).
"""
import itertools, sys
sys.path.insert(0, '.')
from fractions import Fraction as F
from math import gcd
from qfield import Q
import dimension as D
from epscount import count_eps
from eps_null import walls_and_null

BASE=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
CASES=[('GATE n=6  727', BASE+[(7,14,1,-5)], 1),
       ('n=8  1895', BASE+[(7,14,1,-5),(4,-3,-4,-4),(24,-24,24,-61)], None),
       ('n=9  2785', BASE+[(7,14,1,-5),(4,-3,-4,-4),(24,-24,24,-61),(56,56,55,56)], None),
       ('n=10 3917', BASE+[(7,14,1,-5),(4,-3,-4,-4),(24,-24,24,-61),(57,57,56,57),
                           (88787,-9061,74275,113786)], None)]
COMBOS=[(1,1),(1,-1),(2,1),(1,2),(3,-2)]


def primitive(v):
    den=1
    for x in v: den=den*F(x).denominator//gcd(den,F(x).denominator)
    iv=[int(F(x)*den) for x in v]; g=0
    for x in iv: g=gcd(g,abs(x))
    return tuple(x//(g or 1) for x in iv)


def preserves(pt, q0, ncols, rec, v):
    """True/False/None(unevaluable): count(pt +- eps*v) == rec on BOTH sides"""
    for sgn in (1,-1):
        c=count_eps(pt,[Q(sgn*F(x),0,0) for x in v],0,q0)
        if c is None:
            c=count_eps(pt,[Q(sgn*F(x),0,0) for x in v],0,q0,wide=True)
        if c is None: return None
        if c!=rec: return False
    return True


def run(label, cubes, expect):
    pt,walls,null,ncols=walls_and_null(cubes)
    rec=D.count_at(pt,len(cubes))
    z=count_eps(pt,[Q(0,0,0)]*ncols,0,cubes[0]) or \
      count_eps(pt,[Q(0,0,0)]*ncols,0,cubes[0],wide=True)
    print('\n%s: record %d  ambient %d  walls %d  deficit %d   zero-control %s'
          %(label,rec,ncols,len(walls),len(null),'OK' if z==rec else 'FAILED'),flush=True)
    if z!=rec: return
    cands=[primitive(v) for v in null]
    tail=slice(ncols-3,ncols)
    proj=[]
    for g in walls:
        t=primitive(list(g)[tail])
        if any(t) and t not in proj: proj.append(t)
    for u,w in itertools.combinations(proj,2):
        c=(u[1]*w[2]-u[2]*w[1], u[2]*w[0]-u[0]*w[2], u[0]*w[1]-u[1]*w[0])
        if any(c):
            cands.append(primitive([0]*(ncols-3)+list(c)))
    if len(proj)<2 and proj:
        import sympy as sp
        for b in sp.Matrix([list(v) for v in proj]).nullspace():
            cands.append(primitive([0]*(ncols-3)+[sp.Rational(x) for x in b]))
    seen=set(); cands=[c for c in cands if c not in seen and not seen.add(c)]
    B=[]; unev=0
    for c in cands:
        p=preserves(pt,cubes[0],ncols,rec,c)
        if p is None: unev+=1; continue
        if not p: continue
        ok=True
        for b in B:
            for a1,a2 in COMBOS:
                cc=primitive([a1*x+a2*y for x,y in zip(c,b)])
                r=preserves(pt,cubes[0],ncols,rec,cc)
                if r is not True: ok=False; break
            if not ok: break
        if ok: B.append(c)
    print('   %d candidates, %d UNEVALUATED, verified-preserving SUBSPACE dimension %d'
          %(len(cands),unev,len(B)),flush=True)
    print('   P184 lower bound (deficit-1) = %d'%max(0,len(null)-1),flush=True)
    if expect is not None:
        print('   GATE: expected %d -> %s'%(expect,'OK' if len(B)==expect else 'FAILED'),flush=True)
    return len(B)


for lbl,cubes,exp in CASES:
    run(lbl,cubes,exp)
