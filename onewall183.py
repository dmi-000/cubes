#!/usr/bin/env python3
"""What is ONE WALL from the 183 record?

The full face enumeration is the wrong tool and did not finish: 12 walls in
ambient 9 is a nominal 3^12 sign-vector tree, far larger than the 67s' 3^6 and
3^9, and it ran 3 hours without reporting.

"One wall away" does not need the arrangement. For each wall, the direction
crossing THAT WALL ALONE is determined: it lies in the null space of the other
eleven and is not orthogonal to this one. Twelve exact solves, not half a million
sign vectors. Where no such direction exists the wall is ENTANGLED and is reported
as such, never as absent -- at 727, 26 of 27 walls were entangled, so this is the
expected failure and must not be silently dropped.

Counts come from the infinitesimal engine: no step size.
"""
import json, sys
from fractions import Fraction as F
import os as _os
HERE=_os.path.dirname(_os.path.abspath(__file__)); sys.path.insert(0,HERE)
import sympy as sp, dimension as D
from epscount import count_eps, count_eps_err

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
base=D.count_at(pt,n)
print('183 record: count %s (gate: must be 183), ambient %d'%(base,ncols),flush=True)
assert base==183

vars_=sp.symbols('c0:%d'%ncols); Rs=D.frames(vars_,q[0])
tight,_=D.cached_conditions(Rs,n,vars_,pt,D.quats_of(pt,q[0]),q[0])
good=[t for t in tight if not t['degenerate']]
def _norm(g):
    piv=next((x for x in g if x!=0),None)
    return tuple(str(x/piv) for x in g) if piv is not None else None
seen,walls={},[]
for t in good:
    k=_norm(t['grad'])
    if k is not None and k not in seen: seen[k]=True; walls.append(t['grad'])
print('   %d distinct walls, rank %d of %d'
      %(len(walls),ncols-len(D.nullspace(walls,ncols)),ncols),flush=True)

out=[]; ent=0; uneval=0
for i,w in enumerate(walls):
    sub=[walls[t] for t in range(len(walls)) if t!=i]
    cross=None
    for v in D.nullspace(sub,ncols):
        if sum(w[k]*v[k] for k in range(ncols))!=0: cross=v; break
    if cross is None:
        out.append({'wall':i,'status':'ENTANGLED'}); ent+=1
        print('   wall %2d: ENTANGLED (no direction crosses it alone)'%i,flush=True); continue
    dv=D.normalize_dir(cross)
    plus=count_eps(pt,dv,0,q[0]); minus=count_eps(pt,[-x for x in dv],0,q[0])
    if plus is None and minus is None:
        uneval+=1; st='UNEVALUABLE'
    else: st='ok'
    out.append({'wall':i,'status':st,'beyond':[plus,minus],
                'height':max(abs(int(x)) for x in dv)})
    print('   wall %2d: %s / %s   (witness height %d)'
          %(i,plus,minus,max(abs(int(x)) for x in dv)),flush=True)
vals=[v for r in out if r.get('beyond') for v in r['beyond'] if v is not None]
print('\n   ONE-WALL NEIGHBOURS of 183: %s'%sorted(set(vals),reverse=True),flush=True)
if vals:
    print('   best %d -> DROP %d | %d entangled, %d unevaluable of %d walls'
          %(max(vals),base-max(vals),ent,uneval,len(walls)),flush=True)
json.dump({'base':base,'walls':len(walls),'entangled':ent,'unevaluable':uneval,
           'neighbours':sorted(set(vals),reverse=True),'detail':out},
          open(HERE+'/onewall183.json','w'),indent=1)
