#!/usr/bin/env python3
"""What is the MINIMAL wall-set crossable from the 183 record, and what lies beyond?

Postscript 140: all 12 of the record's walls are entangled -- no direction crosses
any one alone. The natural next question is not the whole arrangement (3^12 sign
vectors, a tree that ran 3 hours without finishing) but the SMALLEST crossable
subset: C(12,2) = 66 pairs, then C(12,3) = 220 triples, and so on. Polynomial, not
exponential, and it is what "minimal move away from the record" actually means.

For a subset S: a direction crossing EXACTLY S lies in the null space of the walls
NOT in S, and is non-orthogonal to every wall IN S. Exact rational solves
throughout; counts from the infinitesimal engine, so no step size.
"""
import itertools, json, sys
from fractions import Fraction as F
import os as _os
HERE=_os.path.dirname(_os.path.abspath(__file__)); sys.path.insert(0,HERE)
import sympy as sp, dimension as D
from epscount import count_eps

def qmul(a,b):
    w1,x1,y1,z1=a; w2,x2,y2,z2=b
    return (w1*w2-x1*x2-y1*y2-z1*z2, w1*x2+x1*w2+y1*z2-z1*y2,
            w1*y2-x1*z2+y1*w2+z1*x2, w1*z2+x1*y2-y1*x2+z1*w2)
def degauge(cfg):
    for g in ((1,0,0,0),(2,1,0,0),(3,1,1,0),(5,1,2,1)):
        out=[qmul(g,q) for q in cfg]
        if all(q[0]!=0 for q in out): return out
    raise RuntimeError

RAW=[(1,0,0,0),(0,5,3,2),(1,-4,-1,1),(1,1,-1,-4)]
q=degauge(RAW); D.set_field(0); D.QZERO[:]=[q[0]]
pt=D.point_of(q); n=len(q); ncols=3*(n-1)
base=D.count_at(pt,n); assert base==183, 'gate failed'
vars_=sp.symbols('c0:%d'%ncols); Rs=D.frames(vars_,q[0])
tight,_=D.cached_conditions(Rs,n,vars_,pt,D.quats_of(pt,q[0]),q[0])
good=[t for t in tight if not t['degenerate']]
def _norm(g):
    piv=next((x for x in g if x!=0),None)
    return tuple(str(x/piv) for x in g) if piv is not None else None
seen,W={},[]
for t in good:
    k=_norm(t['grad'])
    if k is not None and k not in seen: seen[k]=True; W.append(t['grad'])
m=len(W)
print('183: count %d | %d walls, rank %d of %d'
      %(base,m,ncols-len(D.nullspace(W,ncols)),ncols),flush=True)

from collections import Counter
results=[]
for k in range(2,7):
    subsets=list(itertools.combinations(range(m),k))
    found=0; hist=Counter(); uneval=0
    for S in subsets:
        rest=[W[t] for t in range(m) if t not in S]
        cross=None
        for v in (D.nullspace(rest,ncols) if rest else
                  [[F(1) if t==c else F(0) for t in range(ncols)] for c in range(ncols)]):
            if all(sum(W[i][t]*v[t] for t in range(ncols))!=0 for i in S):
                cross=v; break
        if cross is None: continue
        found+=1
        dv=D.normalize_dir(cross)
        for d in (dv,[-x for x in dv]):
            c=count_eps(pt,d,0,q[0])
            if c is None: uneval+=1
            else: hist[c]+=1
    print('k=%d: %4d subsets -> %3d crossable, counts beyond %s%s'
          %(k,len(subsets),found,dict(sorted(hist.items(),reverse=True)) or '{}',
            '  (%d unevaluable)'%uneval if uneval else ''),flush=True)
    results.append({'k':k,'subsets':len(subsets),'crossable':found,
                    'hist':{str(a):b for a,b in hist.items()},'uneval':uneval})
    if found and hist:
        print('     best beyond %d -> DROP %d from the record'
              %(max(hist),base-max(hist)),flush=True)
        break
json.dump({'base':base,'walls':m,'levels':results},open(HERE+'/minimal_cross.json','w'),indent=1)
