#!/usr/bin/env python3
"""The 88 walls COMMON to both 183s: what is their intersection, and what lies on it?

Postscript 133 found 183 is a plateau with (at least) two non-congruent isolated
members. Shared-wall analysis then found they lie on 88 COMMON walls of 108 each
-- 81.5%, spread over all four frames, all of them pair conditions.

If a plateau's members share a large wall system, that system is where the rest of
the plateau lives. The intersection of 88 conditions is a LOW-DIMENSIONAL LOCUS
containing both known 183s, and enumerating what else sits on it turns "at least
two members" into a count -- a solve, not a search.

THIS FILE MEASURES THE LOCUS, honestly:
  * rank of the 88 shared gradients at each 183 -> the locus dimension THERE
  * whether the shared set is the SAME linear system at both points, or merely
    the same combinatorial labels realised differently
That second question is the one that decides whether "shared wall" means shared
hypersurface or only shared index.
"""
import itertools, json, os, sys, time
import os as _os
HERE=_os.path.dirname(_os.path.abspath(__file__)); sys.path.insert(0,HERE)
import sympy as sp, dimension as D
from fractions import Fraction as F

def qmul(a,b):
    w1,x1,y1,z1=a; w2,x2,y2,z2=b
    return (w1*w2-x1*x2-y1*y2-z1*z2, w1*x2+x1*w2+y1*z2-z1*y2,
            w1*y2-x1*z2+y1*w2+z1*x2, w1*z2+x1*y2-y1*x2+z1*w2)
def degauge(cfg):
    for g in ((1,0,0,0),(2,1,0,0),(3,1,1,0),(5,1,2,1)):
        out=[qmul(g,q) for q in cfg]
        if all(q[0]!=0 for q in out): return out
    raise RuntimeError

A=[(1,0,0,0),(0,5,3,2),(1,-4,-1,1),(1,1,-1,-4)]
B=[(1,0,0,0),(-2,-2,5,-2),(3,11,-3,-3),(0,-7,4,-3)]

def analyse(cfg,label):
    q=degauge(cfg); D.set_field(0); D.QZERO[:]=[q[0]]
    pt=D.point_of(q); n=len(q); ncols=3*(n-1)
    vars_=sp.symbols('c0:%d'%ncols); Rs=D.frames(vars_,q[0])
    tight,_=D.cached_conditions(Rs,n,vars_,pt,D.quats_of(pt,q[0]),q[0])
    good=[t for t in tight if not t['degenerate']]
    # index each condition by its combinatorial label so the two points compare
    by={}
    for t in good:
        by[(t['frame'],tuple(sorted(t['group'])))]=t['grad']
    print('%s: %d non-degenerate conditions, %d distinct labels'%(label,len(good),len(by)),flush=True)
    return by,pt,ncols,q

byA,ptA,ncols,qA=analyse(A,'183 class 1')
byB,ptB,_,qB=analyse(B,'183 class 2')
shared=sorted(set(byA)&set(byB))
print('shared labels among NON-DEGENERATE conditions: %d'%len(shared),flush=True)

for lbl,by,pt in (('class 1',byA,ptA),('class 2',byB,ptB)):
    rows=[by[k] for k in shared]
    ns=D.nullspace(rows,ncols)
    print('%s: the %d shared conditions have rank %d of %d -> their common locus '
          'has dimension %d THERE'%(lbl,len(rows),ncols-len(ns),ncols,len(ns)),flush=True)

# Are the shared conditions the SAME hypersurfaces, or only the same labels?
# Compare the gradient directions up to scale at the two points.
def norm(g):
    piv=next((x for x in g if x!=0),None)
    return tuple(x/piv for x in g) if piv is not None else None
same=sum(1 for k in shared if norm(byA[k])==norm(byB[k]))
print('\nshared labels whose GRADIENT DIRECTION agrees at both points: %d of %d'
      %(same,len(shared)),flush=True)
print('(agreement would mean the same hypersurface locally; disagreement means the'
      ' same CONDITION realised at different points of moduli space)',flush=True)
json.dump({'shared_labels':len(shared),'gradient_agree':same},
          open(os.path.join(HERE,'shared_locus.json') if False else HERE+'/shared_locus.json','w'),indent=1)
