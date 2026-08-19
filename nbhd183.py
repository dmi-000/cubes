#!/usr/bin/env python3
"""What lies ONE WALL from the n=4 record, and is it recognisable?

The neighbourhood of a maximiser is a CLIFF, not a slope: best adjacent counts are
63 from 67 (drop 4), 715 from 727 (drop 12), 1211 from 1217 (drop 6). There is no
uphill signal until you are already there, which is why gradient-like search
fails.

The consequence is a strategy rather than a compass. If neighbourhoods are cliffs
you cannot SMELL a max, but you can ENUMERATE one: the chambers adjacent to a
configuration are finitely many and exactly computable, so a jump to the best
adjacent chamber is a solve, and "every adjacent chamber is worse" is a
CERTIFICATE of local maximality rather than a guess.

This enumerates the chambers around the canonical 183 and asks two things:
  * what are the adjacent counts (the cliff's shape at n = 4)?
  * are the neighbours RECOGNISABLE -- do they share nearly all of 183's walls,
    so that "one wall from a max" could be screened for before enumerating?

Method as in `extension_chambers.py` (Postscript 125/131): the walls through the
point give a sign-vector arrangement; each realizable face is one combinatorially
distinct move; witnesses are chosen by SIMPLEST RATIONAL (Postscript 136's fix --
midpoint witnesses blew the engine's budget on 10 of 24 chambers); counts come
from the infinitesimal engine, so no step size enters.
"""
import itertools, json, os, sys
from fractions import Fraction as F
import os as _os
HERE=_os.path.dirname(_os.path.abspath(__file__)); sys.path.insert(0,HERE)
import sympy as sp, dimension as D
from isolation67 import faces
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
base=D.count_at(pt,n)
print('183 record: count %s, ambient %d'%(base,ncols),flush=True)
assert base==183, 'GATE FAILED: base is not 183'

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
print('   %d tight conditions -> %d distinct walls'%(len(good),len(walls)),flush=True)

class L:
    def write(s,*a): pass
    def flush(s): pass
fs=faces(walls,ncols,F(0),L())
print('   %d realizable faces (combinatorially distinct moves)'%len(fs),flush=True)

from collections import Counter
hist=Counter(); uneval=0; best=None; rows=[]
for sigma,dv in fs:
    d0=D.normalize_dir(dv)
    c=count_eps(pt,d0,0,q[0])
    if c is None: uneval+=1; continue
    hist[c]+=1
    codim=sum(1 for x in sigma if x==0)
    rows.append({'codim':codim,'count':c})
    if best is None or c>best: best=c
print('\n   adjacent counts: %s'%dict(sorted(hist.items(),reverse=True)),flush=True)
print('   best neighbour %s (drop %s) | %d unevaluable of %d'
      %(best,base-best if best else None,uneval,len(fs)),flush=True)
byco={}
for r in rows: byco.setdefault(r['codim'],Counter())[r['count']]+=1
for k in sorted(byco):
    print('   codim %d: %s'%(k,dict(sorted(byco[k].items(),reverse=True))),flush=True)
json.dump({'base':base,'walls':len(walls),'faces':len(fs),
           'hist':{str(k):v for k,v in hist.items()},'best':best,'uneval':uneval},
          open(HERE+'/nbhd183.json','w'),indent=1)
