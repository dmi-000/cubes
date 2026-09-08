#!/usr/bin/env python3
"""Locate the cost in the two n=9 classes that ran 10+ hours without output.

Uses the SHARED CONDITIONS CACHE, so reaching the slow step costs nothing and the
expensive symbolic build is not repeated.  Per chart, with a budget: a chart that
exceeds it is reported UNEVALUATED, never as "no solutions".
"""
import sys, time
sys.path.insert(0, HERE)
import sympy as sp, dimension as D
import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__))

BASE=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
R9=BASE+[(7,14,1,-5),(4,-3,-4,-4),(24,-24,24,-61),(56,56,55,56)]
CASES={'k5':(9,5,(2,3,5,7,8)),'k6':(9,6,(1,3,5,6,7,8))}

def main():
    which=sys.argv[1] if len(sys.argv)>1 else 'k5'
    budget=float(sys.argv[2]) if len(sys.argv)>2 else 300
    n,k,idxs=CASES[which]
    cfg=[R9[i] for i in idxs]
    pt=D.point_of(cfg); D.QZERO[:]=[cfg[0]]; N=len(cfg)
    vars_=sp.symbols('c0:%d'%(3*(N-1))); Rs=D.frames(vars_,cfg[0])
    t0=time.time()
    tight,loose=D.cached_conditions(Rs,N,vars_,pt,D.quats_of(pt,cfg[0]),cfg[0])
    good=[t for t in tight if not t['degenerate']]
    ns=D.nullspace([t['grad'] for t in good],3*(N-1))
    print('%s: n=%d k=%d ambient %d | %d tight | lineality %d | setup %.1fs'
          %(which,n,k,3*(N-1),len(good),len(ns),time.time()-t0),flush=True)
    st,dirs=D.variety_incremental(good,list(range(len(good))),pt,N,ns,cfg[0],
                                  chart_budget=budget,progress=True)
    print('RESULT %s: status=%s dirs=%d total %.0fs'%(which,st,len(dirs),time.time()-t0))


if __name__ == '__main__':
    main()
