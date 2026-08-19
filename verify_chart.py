#!/usr/bin/env python3
"""Does the chart ORIGIN satisfy every polynomial?  Decides what "no constant
monomial" actually means, by evaluation rather than by my reading of it."""
import sys, time
sys.path.insert(0,HERE)
import sympy as sp, dimension as D
from fractions import Fraction as F
exec(open('linearize_test.py').read().split('def linear_empty')[0].split("BASE=")[1].join(['BASE=','']) if False else '')
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
c0v=[sp.Rational(F(cfg[0][r+1],cfg[0][0]).numerator,F(cfg[0][r+1],cfg[0][0]).denominator)
     for r in range(3)]
polys=[]
for i in range(len(good)):
    pol=sp.Poly(D.branch_numerator(good[i],[c0v]+cvec),t_)
    for c in pol.all_coeffs()[:-1]:
        c=sp.expand(c)
        if c!=0: polys.append(c)
print('%d polynomials'%len(polys),flush=True)
degs=[sp.Poly(p,*us).total_degree() for p in polys]
from collections import Counter
import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__))
print('TRUE degree distribution over all polys:',dict(sorted(Counter(degs).items())),flush=True)
for chart in (0,2):
    sub={u:(sp.Integer(1) if i==chart else sp.Integer(0)) for i,u in enumerate(us)}
    vals=[sp.expand(p.subs(sub)) for p in polys]
    nz=[v for v in vals if v!=0]
    print('chart %d origin (direction = ns[%d]): %d of %d polynomials NONZERO -> %s'
          %(chart+1,chart,len(nz),len(vals),
            'NOT a solution' if nz else 'IS A SOLUTION (chart origin survives)'),flush=True)
