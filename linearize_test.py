#!/usr/bin/env python3
"""EMPTY by LINEAR ALGEBRA: 252 quadrics in 7 unknowns is over-determined.

The chart system turns out to be 252 polynomials, EVERY ONE of degree 2, in 7
unknowns.  Gröbner/`sp.solve` on that grinds for 10+ hours through coefficient
explosion (2078 of 2287 stack samples in Karatsuba multiply, 4.2 GB peak).

But a degree-2 system in 7 variables has only C(9,2) = 36 monomials, so treating
each monomial as an independent unknown makes it a LINEAR system: 252 equations
in 36 unknowns, solvable by exact Gaussian elimination with no coefficient blowup.

SOUNDNESS, which is the whole point.  Linearisation is a RELAXATION: every true
solution yields a monomial vector in the kernel, so
    kernel forces the constant monomial to 0  =>  NO solutions.  PROVED EMPTY.
    kernel admits constant = 1                =>  INCONCLUSIVE, fall back.
It can therefore prove emptiness but never nonemptiness, and it is reported that
way -- an inconclusive result is not a negative one.
"""
import sys, time
sys.path.insert(0,HERE)
import sympy as sp, dimension as D
from fractions import Fraction as F
import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__))

BASE=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
R9=BASE+[(7,14,1,-5),(4,-3,-4,-4),(24,-24,24,-61),(56,56,55,56)]

def build(idxs):
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
    return polys, us, d

def linear_empty(polys, us, chart):
    """(verdict, seconds): 'EMPTY' proved, or 'inconclusive'."""
    free=[u for i,u in enumerate(us) if i!=chart]
    ps=[q for q in (sp.expand(p.subs({us[chart]:1})) for p in polys) if q!=0]
    t0=time.time()
    mons=set()
    dicts=[]
    for q in ps:
        pd=sp.Poly(q,*free).as_dict()
        dicts.append(pd); mons |= set(pd)
    mons=sorted(mons)
    mi={m:i for i,m in enumerate(mons)}
    rows=[[sp.Rational(0)]*len(mons) for _ in dicts]
    for r,pd in enumerate(dicts):
        for m,c in pd.items(): rows[r][mi[m]]=sp.Rational(c)
    M=sp.Matrix(rows)
    const=tuple([0]*len(free))
    # A solution's monomial vector has constant-monomial entry 1, so emptiness
    # follows if every kernel vector has a ZERO there.
    ker=M.nullspace()
    ci=mi.get(const)
    if ci is None:
        return 'EMPTY (no constant monomial column)', time.time()-t0, len(mons), len(ps)
    if all(v[ci]==0 for v in ker):
        return 'EMPTY -- PROVED: every kernel vector kills the constant monomial', time.time()-t0, len(mons), len(ps)
    return 'inconclusive (kernel dim %d admits constant=1)'%len(ker), time.time()-t0, len(mons), len(ps)

for lbl,idxs in (('k5',(2,3,5,7,8)),('k6',(1,3,5,6,7,8))):
    t0=time.time(); polys,us,d=build(idxs)
    print('%s: %d polys built in %.0fs, lineality %d'%(lbl,len(polys),time.time()-t0,d),flush=True)
    for chart in range(d):
        v,el,nm,npq=linear_empty(polys,us,chart)
        print('   chart %d/%d: %3d monomials, %3d eqs -> %-64s %.1fs'%(chart+1,d,nm,npq,v,el),flush=True)
