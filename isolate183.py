#!/usr/bin/env python3
"""Are the two 183s ISOLATED points, like the 67s, or do they lie on continua?

Postscript 133 established that 183 is a plateau with at least two congruence
classes. That says nothing about whether each member is isolated: the n=2
maximiser 13 is a continuum, the 67s are isolated points, and 727 is isolated
while sitting in an uncountable plateau. Plateau membership and local isolation
are independent facts.

BOTH 183s CONTAIN A HALF-TURN (w = 0), which is at Cayley infinity. That is not an
obstruction (Postscript 126): only the PARAMETERISED cubes need finite
coordinates, since the gauge cube is frozen and never inverted. Reorder so the
half-turn is the frozen cube 0.
"""
import sys, time
import os as _os
HERE=_os.path.dirname(_os.path.abspath(__file__)); sys.path.insert(0,HERE)
import sympy as sp, dimension as D

A=[(1,0,0,0),(0,5,3,2),(1,-4,-1,1),(1,1,-1,-4)]          # canonical
B=[(1,0,0,0),(-2,-2,5,-2),(3,11,-3,-3),(0,-7,4,-3)]      # wide-climb, class 2

def qmul(a,b):
    w1,x1,y1,z1=a; w2,x2,y2,z2=b
    return (w1*w2-x1*x2-y1*y2-z1*z2, w1*x2+x1*w2+y1*z2-z1*y2,
            w1*y2-x1*z2+y1*w2+z1*x2, w1*z2+x1*y2-y1*x2+z1*w2)

def degauge(cfg):
    """rotate the whole configuration so NO cube is a half-turn.

    Reordering is not enough: the second-order step needs the GAUGE cube's own
    Cayley coordinates, and a half-turn has none.  A global rotation is a
    congruence, so it preserves every count while moving every cube off w = 0 --
    the same 'pick a better representative' move that fixed the eps step, the
    Fourier-Motzkin witness and the wall gradients earlier today.
    """
    for g in ((1,0,0,0),(2,1,0,0),(3,1,1,0),(5,1,2,1),(7,2,3,1),(11,3,1,2)):
        out=[qmul(g,q) for q in cfg]
        if all(q[0]!=0 for q in out):
            return out,g
    raise RuntimeError('no rotation cleared every half-turn')

for name,cfg in (('183 class 1 (canonical)',A),('183 class 2 (wide climb)',B)):
    q,g=degauge(cfg)
    if g!=(1,0,0,0): print('%-26s (rotated by %s to clear half-turns)'%(name,str(g)))
    D.set_field(0); D.QZERO[:]=[q[0]]
    pt=D.point_of(q)
    if pt is None:
        print('%-26s STILL at Cayley infinity after reorder'%name); continue
    n=len(q); ncols=3*(n-1)
    base=D.count_at(pt,n)
    vars_=sp.symbols('c0:%d'%ncols); Rs=D.frames(vars_,q[0])
    t0=time.time()
    tight,loose=D.cached_conditions(Rs,n,vars_,pt,D.quats_of(pt,q[0]),q[0])
    good=[t for t in tight if not t['degenerate']]
    ns=D.nullspace([t['grad'] for t in good],ncols)
    print('%-26s count %s | %d tight | lineality %d of %d | setup %.0fs'
          %(name,base,len(good),len(ns),ncols,time.time()-t0),flush=True)
    if not ns:
        print('%-26s   lineality 0 -> ISOLATED at FIRST order'%''); continue
    st,dirs=D.variety_incremental(good,list(range(len(good))),pt,n,ns,q[0],progress=False)
    print('%-26s   second-order variety: %s, %d directions -> %s'
          %('',st,len(dirs),'ISOLATED' if st=='empty' else 'NOT isolated (candidates)'),flush=True)
