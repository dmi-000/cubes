#!/usr/bin/env python3
"""Re-derive the second-order variety for every census class, validated route.

`variety_incremental` (Postscript 116) passed a non-vacuous control at lineality 4.
This applies it to all (count, profile) classes of the n=6..9 records, engine-
verifying every direction it returns.  Writes incrementally; conditions come from
the shared cache.   python3 census_variety.py <shard> <nshards> [seconds]
"""
import json, sys, time, glob
sys.path.insert(0, '/Users/dmi/cube-compounds')
import sympy as sp, dimension as D
from fractions import Fraction as F
from subset_topology import classes
BASE=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
R={6:BASE+[(7,14,1,-5)]}
R[7]=R[6]+[(4,-3,-4,-4)]; R[8]=R[7]+[(24,-24,24,-61)]; R[9]=R[8]+[(56,56,55,56)]
SH=int(sys.argv[1]); NS=int(sys.argv[2]); BUD=float(sys.argv[3]) if len(sys.argv)>3 else 200000
OUT='/Users/dmi/cube-compounds/census_variety_%d.json'%SH
LOG=open('/Users/dmi/cube-compounds/census_variety_%d.log'%SH,'w')
T0=time.time()
def log(m):
    LOG.write('[%7.1fs] %s\n'%(time.time()-T0,m)); LOG.flush()
todo=[(n,rep) for n in sorted(R) for rep in classes(R[n],n)]
out=[]
for idx,(n,rep) in enumerate(todo):
    if idx%NS!=SH: continue
    if time.time()-T0>BUD: log('budget reached'); break
    cfg=rep['cfg']
    pt=D.point_of(cfg)
    if pt is None: continue
    D.QZERO[:]=[cfg[0]]; N=len(cfg)
    try:
        vars_=sp.symbols('c0:%d'%(3*(N-1))); Rs=D.frames(vars_,cfg[0])
        tight,loose=D.cached_conditions(Rs,N,vars_,pt,D.quats_of(pt,cfg[0]),cfg[0])
        good=[t for t in tight if not t['degenerate']]
        ns=D.nullspace([t['grad'] for t in good],3*(N-1))
        st,dirs=D.variety_incremental(good,list(range(len(good))),pt,N,ns,cfg[0])
        base=D.count_at(pt,N); ok=0
        for dv in dirs:
            vals=[D.count_at(pt,N,dv,e) for e in (F(1,64),F(1,256))]
            if all(v==base for v in vals if v is not None) and any(v is not None for v in vals): ok+=1
    except Exception as e:
        log('n=%d k=%d c=%d CRASH %s'%(n,rep['k'],rep['count'],type(e).__name__)); continue
    rec=dict(n=n,k=rep['k'],count=rep['count'],lineality=len(ns),status=st,
             dirs=len(dirs),confirmed=ok,idxs=list(rep['idxs']))
    out.append(rec); json.dump(out,open(OUT,'w'),indent=1)
    log('n=%d k=%d c=%-5d lineality %d -> %-9s %d dirs, %d confirmed'
        %(n,rep['k'],rep['count'],len(ns),st,len(dirs),ok))
json.dump(out,open(OUT,'w'),indent=1); log('done: %d classes'%len(out))
