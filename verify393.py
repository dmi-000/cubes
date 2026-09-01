#!/usr/bin/env python3
"""Is 393's locus really 0-dimensional? Verified with a pool that can see arcs.

`facets_any.py` reported preserving rank 0 at 393 and at 727. At 727 that was FALSE —
its pool was the NULL BASIS only, and 727's arcs are slice tangents that CROSS walls,
so they were never candidates, even though 727's locus is 1-dimensional with six solved
ends. 393's rank 0 rests on the same defective pool and is therefore unverified.

This uses the pool that DOES find arcs ([P190](LEDGER.md#p190)/[P196](LEDGER.md#p196)):
null-space directions, PLUS rank-2 null directions of the wall normals projected onto
EVERY cube's 3-slice, plus the full orthogonal complement when those normals span rank
< 2. Each candidate verified with eps, both signs, wide engine on refusal.

GATE: 727 must come back with at least TWO preserving directions (arc D's tangents),
which is exactly the case the null-only pool failed.
"""
import itertools, sys
sys.path.insert(0,'.')
from fractions import Fraction as F
from math import gcd
import sympy as sp
from qfield import Q
import dimension as D
from epscount import count_eps
from eps_null import walls_and_null

BASE=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
CASES=[('GATE 727 (n=6)', BASE+[(7,14,1,-5)], 2),
       ('393 (n=5)', BASE, None),
       ('183 (n=4)', [BASE[i] for i in (0,1,2,4)], None)]

def prim(v):
    den=1
    for x in v: den=den*F(x).denominator//gcd(den,F(x).denominator)
    iv=[int(F(x)*den) for x in v]; g=0
    for x in iv: g=gcd(g,abs(x))
    iv=[x//(g or 1) for x in iv]
    for x in iv:
        if x>0: break
        if x<0: iv=[-y for y in iv]; break
    return tuple(iv)

for label,cubes,expect in CASES:
    pt,walls,null,ncols=walls_and_null(cubes)
    rec=D.count_at(pt,len(cubes))
    z=count_eps(pt,[Q(0,0,0)]*ncols,0,cubes[0])
    if z is None: z=count_eps(pt,[Q(0,0,0)]*ncols,0,cubes[0],wide=True)
    w0=count_eps(pt,[Q(F(x),0,0) for x in walls[0]],0,cubes[0])
    if w0 is None: w0=count_eps(pt,[Q(F(x),0,0) for x in walls[0]],0,cubes[0],wide=True)
    ok=(z==rec) and (w0 is not None and w0!=rec)
    print('\n%s  record %d  ambient %d  walls %d  deficit %d   CONTROLS zero->%s wall->%s %s'
          %(label,rec,ncols,len(walls),len(null),z,w0,'OK' if ok else 'FAILED'),flush=True)
    if not ok: continue
    cands=[prim(v) for v in null]
    for j in range(1,len(cubes)):
        sl=slice(3*(j-1),3*j)
        proj=[]
        for g in walls:
            t=prim(list(g)[sl])
            if any(t) and t not in proj: proj.append(t)
        got=[]
        for u,w in itertools.combinations(proj,2):
            c=(u[1]*w[2]-u[2]*w[1],u[2]*w[0]-u[0]*w[2],u[0]*w[1]-u[1]*w[0])
            if any(c): got.append(prim(list(c)))
        if not got and proj:
            for b in sp.Matrix([list(v) for v in proj]).nullspace():
                d=prim([sp.Rational(x) for x in b])
                if any(d): got.append(d)
        for c in got:
            full=[0]*ncols; full[3*(j-1):3*j]=list(c)
            cands.append(prim(full))
    seen=set(); cands=[c for c in cands if c not in seen and not seen.add(c)]
    good=[]; unev=0
    for c in cands:
        vals=[]
        for sgn in (1,-1):
            v=count_eps(pt,[Q(sgn*F(x),0,0) for x in c],0,cubes[0])
            if v is None: v=count_eps(pt,[Q(sgn*F(x),0,0) for x in c],0,cubes[0],wide=True)
            vals.append(v)
        if None in vals: unev+=1
        elif vals[0]==rec and vals[1]==rec: good.append(c)
    rk=sp.Matrix([list(g) for g in good]).rank() if good else 0
    print('   pool %d candidates (null + every cube-slice), %d UNEVALUATED'%(len(cands),unev),flush=True)
    print('   preserving directions %d, RANK %d   (null-only pool gave rank %d)'
          %(len(good),rk,1 if any(prim(v) in good for v in null) else 0),flush=True)
    if expect is not None:
        print('   GATE: expected >= %d preserving, got %d -> %s'
              %(expect,len(good),'OK' if len(good)>=expect else 'FAILED'),flush=True)
    if good and rk>0:
        print('   witnesses: %s'%[g for g in good[:4]],flush=True)
    if rk==0 and unev==0:
        print('   => locus is 0-DIMENSIONAL here: a single point, whose boundary is itself',flush=True)
