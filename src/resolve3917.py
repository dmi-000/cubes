#!/usr/bin/env python3
"""Resolve the n=10 dimension question left open by [P195]: is it 5 or 6?

[P195] verified a 5-dimensional preserving subspace at 3917 and left 3 of 8 candidates
UNEVALUATED, the eps engine refusing them. Diagnosis: the candidate pool has rank 6,
so it CAN reach the deficit — the block was the engine. And the block was self-
inflicted: three null-space basis vectors had heights ~1e9, which is a property of
sympy's arbitrary basis, not of the subspace ([METHODS 15]).

LLL-reducing that basis drops them to 14 (and one stubborn vector), after which the
directions are cheap enough for the engine. Same subspace, different representatives.
"""
import sys
sys.path.insert(0, '.')
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
COMBOS=[(1,1),(1,-1),(2,1)]

def prim(v):
    den=1
    for x in v: den=den*F(x).denominator//gcd(den,F(x).denominator)
    iv=[int(F(x)*den) for x in v]; g=0
    for x in iv: g=gcd(g,abs(x))
    return tuple(x//(g or 1) for x in iv)

pt,walls,null,ncols=walls_and_null(C10)
rec=D.count_at(pt,len(C10))
B=[list(prim(v)) for v in null]
for it in range(4):
    B=[list(prim(b)) for b in lll(B)]
    print('LLL pass %d heights: %s'%(it+1,[max(abs(x) for x in b) for b in B]),flush=True)
assert sp.Matrix(B).rank()==len(null), 'LLL changed the subspace'
print('rank preserved: %d\n'%sp.Matrix(B).rank(),flush=True)

def pres(v):
    for sgn in (1,-1):
        c=count_eps(pt,[Q(sgn*F(x),0,0) for x in v],0,C10[0])
        if c is None:
            c=count_eps(pt,[Q(sgn*F(x),0,0) for x in v],0,C10[0],wide=True)
        if c is None: return None
        if c!=rec: return False
    return True

z=count_eps(pt,[Q(0,0,0)]*ncols,0,C10[0]) or count_eps(pt,[Q(0,0,0)]*ncols,0,C10[0],wide=True)
print('zero-control -> %s %s'%(z,'OK' if z==rec else 'FAILED'),flush=True)
basis=[]; unev=[]
for b in B:
    v=prim(b); p=pres(v)
    tag={True:'preserves',False:'CHANGES',None:'UNEVALUATED'}[p]
    print('   height %-11d %s'%(max(abs(x) for x in v),tag),flush=True)
    if p is None: unev.append(v); continue
    if not p: continue
    ok=True
    for e in basis:
        for a1,a2 in COMBOS:
            if pres(prim([a1*x+a2*y for x,y in zip(v,e)])) is not True: ok=False; break
        if not ok: break
    if ok: basis.append(v)
print('\nverified-preserving subspace dimension: %d   (deficit %d, %d still unevaluated)'
      %(len(basis),len(null),len(unev)),flush=True)
print('VERDICT: %s'%('dimension = deficit CONFIRMED at n=10' if len(basis)==len(null)
      else 'still short by %d; %d unevaluated'%(len(null)-len(basis),len(unev))),flush=True)
