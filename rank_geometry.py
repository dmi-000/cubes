#!/usr/bin/env python3
"""CORRECTED dimension measurement: RANK of the preserving set, not a vector count.

`map_geometry.py` ([P195]) appended each verified direction to a list and reported
len(list) as the dimension. It never checked LINEAR INDEPENDENCE, so dependent
directions inflated the count — at 2785 the slice tangent (0,1,0) lies in the span of
the three preserving null vectors, giving a reported 4 where the rank is 3.

This measures rank, keeps only directions that increase it, and verifies random
integer combinations of the final independent set.
"""
import itertools, random, sys
sys.path.insert(0,'.')
from fractions import Fraction as F
from math import gcd
import sympy as sp
from qfield import Q
import dimension as D
from epscount import count_eps
from eps_null import walls_and_null
from lll import lll

BASE=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
CASES=[('n=6  727', BASE+[(7,14,1,-5)]),
       ('n=8  1895', BASE+[(7,14,1,-5),(4,-3,-4,-4),(24,-24,24,-61)]),
       ('n=9  2785', BASE+[(7,14,1,-5),(4,-3,-4,-4),(24,-24,24,-61),(56,56,55,56)]),
       ('n=10 3917', BASE+[(7,14,1,-5),(4,-3,-4,-4),(24,-24,24,-61),(57,57,56,57),
                           (88787,-9061,74275,113786)])]

def prim(v):
    den=1
    for x in v: den=den*F(x).denominator//gcd(den,F(x).denominator)
    iv=[int(F(x)*den) for x in v]; g=0
    for x in iv: g=gcd(g,abs(x))
    return tuple(x//(g or 1) for x in iv)

for lbl,cubes in CASES:
    pt,walls,null,ncols=walls_and_null(cubes)
    rec=D.count_at(pt,len(cubes))
    def pres(v):
        for sgn in (1,-1):
            c=count_eps(pt,[Q(sgn*F(x),0,0) for x in v],0,cubes[0])
            if c is None: c=count_eps(pt,[Q(sgn*F(x),0,0) for x in v],0,cubes[0],wide=True)
            if c is None: return None
            if c!=rec: return False
        return True
    cands=[prim(b) for b in lll([list(prim(v)) for v in null])]
    tail=slice(ncols-3,ncols)
    proj=[]
    for g in walls:
        t=prim(list(g)[tail])
        if any(t) and t not in proj: proj.append(t)
    for u,w in itertools.combinations(proj,2):
        c=(u[1]*w[2]-u[2]*w[1],u[2]*w[0]-u[0]*w[2],u[0]*w[1]-u[1]*w[0])
        if any(c): cands.append(prim([0]*(ncols-3)+list(c)))
    if len(proj)<2 and proj:
        for b in sp.Matrix([list(v) for v in proj]).nullspace():
            cands.append(prim([0]*(ncols-3)+[sp.Rational(x) for x in b]))
    seen=set(); cands=[c for c in cands if c not in seen and not seen.add(c)]
    ind=[]; unev=0
    for c in cands:
        if sp.Matrix([list(x) for x in ind]+[list(c)]).rank()<=len(ind): continue
        p=pres(c)
        if p is None: unev+=1; continue
        if p: ind.append(c)
    rnd=random.Random(11); bad=0
    for _ in range(8):
        if not ind: break
        co=[rnd.randint(-3,3) for _ in ind]
        if not any(co): continue
        v=prim([sum(a*b[i] for a,b in zip(co,ind)) for i in range(ncols)])
        if pres(v) is not True: bad+=1
    print('%-11s deficit %d | preserving RANK %d | %d unevaluated | %d combo failures | P184 says %d'
          %(lbl,len(null),len(ind),unev,bad,max(0,len(null)-1)),flush=True)
