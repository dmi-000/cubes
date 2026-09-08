#!/usr/bin/env python3
"""A 6th independent preserving direction at 3917, from OUTSIDE the null space.

[P195] left n=10 at dimension >= 5 of a deficit 6. `resolve3917.py` LLL-reduced the
null basis and verified 5 of the 6, leaving ONE direction whose shortest known
representative has height 8.8e8 — refused by the eps engine, and LLL could not shorten
it further.

That vector is not needed. [P195]'s own finding is that the dimension beyond the null
space comes from directions that CROSS walls without changing the count. So the pool
is widened from "the last cube's 3-slice" to EVERY cube's 3-slice: for each cube j,
project the wall normals onto its three coordinates, take rank-2 null directions, and
embed. Any one of these that preserves and is independent of the verified 5 settles
the question at 6.

Cheapest candidates first, and stop at the first success.
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
from lll import lll

BASE=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
C10=BASE+[(7,14,1,-5),(4,-3,-4,-4),(24,-24,24,-61),(57,57,56,57),
          (88787,-9061,74275,113786)]
def prim(v):
    den=1
    for x in v: den=den*F(x).denominator//gcd(den,F(x).denominator)
    iv=[int(F(x)*den) for x in v]; g=0
    for x in iv: g=gcd(g,abs(x))
    return tuple(x//(g or 1) for x in iv)
pt,walls,null,ncols=walls_and_null(C10)
rec=D.count_at(pt,len(C10))
B=[list(prim(v)) for v in null]
B=[list(prim(b)) for b in lll(B)]
verified=[prim(b) for b in B if max(abs(x) for x in b)<10**6]
print('carried over from resolve3917.py: %d verified directions (heights %s)'
      %(len(verified),[max(abs(x) for x in v) for v in verified]),flush=True)
V=sp.Matrix([list(v) for v in verified]); r0=V.rank()
print('their rank: %d ; need one more independent preserving direction\n'%r0,flush=True)

cands=[]
for j in range(1,len(C10)):                       # cube j's three coordinates
    sl=slice(3*(j-1),3*j)
    proj=[]
    for g in walls:
        t=prim(list(g)[sl])
        if any(t) and t not in proj: proj.append(t)
    for u,w in itertools.combinations(proj,2):
        c=(u[1]*w[2]-u[2]*w[1],u[2]*w[0]-u[0]*w[2],u[0]*w[1]-u[1]*w[0])
        if not any(c): continue
        full=[0]*ncols
        full[3*(j-1):3*j]=list(c)
        v=prim(full)
        if sp.Matrix([list(x) for x in verified]+[list(v)]).rank()>r0:
            cands.append((max(abs(x) for x in v),j,v))
cands=sorted(set(cands))
print('%d independent candidates across all 9 cube-slices; cheapest heights %s\n'
      %(len(cands),[c[0] for c in cands[:8]]),flush=True)

def pres(v):
    for sgn in (1,-1):
        c=count_eps(pt,[Q(sgn*F(x),0,0) for x in v],0,C10[0])
        if c is None:
            c=count_eps(pt,[Q(sgn*F(x),0,0) for x in v],0,C10[0],wide=True)
        if c is None: return None
        if c!=rec: return False
    return True

found=None; unev=0
for h,j,v in cands[:40]:
    p=pres(v)
    if p is None: unev+=1; continue
    if p:
        ok=all(pres(prim([a*x+b*y for x,y in zip(v,e)])) is True
               for e in verified for a,b in ((1,1),(1,-1)))
        print('   cube %d, height %-8d preserves; combinations %s'
              %(j,h,'hold' if ok else 'FAIL'),flush=True)
        if ok: found=v; break
    else:
        print('   cube %d, height %-8d changes'%(j,h),flush=True)
print('\n%s'%('DIMENSION 6 = DEFICIT CONFIRMED at n=10; witness %s'%(found,) if found
      else 'no 6th direction found in the first 40 candidates (%d unevaluated)'%unev),flush=True)
