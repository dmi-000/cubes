#!/usr/bin/env python3
"""Is the chart system solvable MODULO A PRIME in reasonable time?

The user's `sample` of the stuck process put 2078 of 2287 samples in k_mul --
Karatsuba big-integer multiply -- with a 4.2 GB peak.  The bottleneck is
COEFFICIENT EXPLOSION during the exact solve, not the algorithm's shape and not
the input scaling (the nullspace basis is <= 5 digits).

Modular arithmetic removes exactly that cost, and gives a SOUND emptiness test:
a rational solution reduces mod p for every p not dividing a denominator or a
leading coefficient, so NO solutions mod such a good p implies NO rational
solutions.  The converse needs lifting, so a modular hit means "candidates
exist, do the exact work"; a modular miss at a good prime is a proof of EMPTY.
"""
import sys, time
sys.path.insert(0,HERE)
import sympy as sp, dimension as D

BASE=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
R9=BASE+[(7,14,1,-5),(4,-3,-4,-4),(24,-24,24,-61),(56,56,55,56)]
idxs=(2,3,5,7,8)
cfg=[R9[i] for i in idxs]; pt=D.point_of(cfg); D.QZERO[:]=[cfg[0]]; N=len(cfg)
vars_=sp.symbols('c0:%d'%(3*(N-1))); Rs=D.frames(vars_,cfg[0])
tight,_=D.cached_conditions(Rs,N,vars_,pt,D.quats_of(pt,cfg[0]),cfg[0])
good=[t for t in tight if not t['degenerate']]
ns=D.nullspace([t['grad'] for t in good],3*(N-1))
d=len(ns); ncols=len(ns[0])
t_=sp.Symbol('t_'); us=sp.symbols('u0:%d'%d)
w=[sum(us[i]*sp.Rational(ns[i][k].numerator,ns[i][k].denominator) for i in range(d))
   for k in range(ncols)]
cvec=[[sp.Rational(pt[k+r].numerator,pt[k+r].denominator)+t_*w[k+r] for r in range(3)]
      for k in range(0,ncols,3)]
from fractions import Fraction as F
import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__))
c0v=[sp.Rational(F(cfg[0][r+1],cfg[0][0]).numerator,F(cfg[0][r+1],cfg[0][0]).denominator)
     for r in range(3)]
cvecs=[c0v]+cvec
t0=time.time(); polys=[]
for i in range(len(good)):
    pol=sp.Poly(D.branch_numerator(good[i],cvecs),t_)
    for c in pol.all_coeffs()[:-1]:
        c=sp.expand(c)
        if c!=0: polys.append(c)
print('%d polynomials built in %.0fs'%(len(polys),time.time()-t0),flush=True)

chart=0
free=[u for i,u in enumerate(us) if i!=chart]
ps=[q for q in (sp.expand(p.subs({us[chart]:1})) for p in polys) if q!=0]
ps_sorted=sorted(ps,key=lambda q: sp.Poly(q,*free).total_degree())
print('chart 1: %d polys, degrees %s'%(len(ps_sorted),
      [sp.Poly(q,*free).total_degree() for q in ps_sorted[:8]]),flush=True)
maxdig=max(len(str(abs(c))) for q in ps_sorted[:8] for c in sp.Poly(q,*free).coeffs())
print('   max coefficient digits in the seed: %d'%maxdig,flush=True)

for p in (32003, 1000003):
    t0=time.time()
    try:
        G=sp.groebner(ps_sorted[:12], *free, modulus=p, order='grevlex')
        el=time.time()-t0
        triv = list(G.exprs)==[sp.Integer(1)]
        print('mod %-8d groebner in %6.1fs -> %s (%d generators)'
              %(p,el,'{1}: NO solutions mod p' if triv else 'nontrivial',len(G.exprs)),
              flush=True)
    except Exception as e:
        print('mod %-8d FAILED %s after %.0fs'%(p,type(e).__name__,time.time()-t0),flush=True)
