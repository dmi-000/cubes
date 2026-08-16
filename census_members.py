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
import itertools
BASE=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
R={6:BASE+[(7,14,1,-5)]}
R[7]=R[6]+[(4,-3,-4,-4)]; R[8]=R[7]+[(24,-24,24,-61)]; R[9]=R[8]+[(56,56,55,56)]
SH=int(sys.argv[1]); NS=int(sys.argv[2]); BUD=float(sys.argv[3]) if len(sys.argv)>3 else 200000
OUT='/Users/dmi/cube-compounds/members_%d.json'%SH
LOG=open('/Users/dmi/cube-compounds/members_%d.log'%SH,'w')
T0=time.time()
def log(m):
    LOG.write('[%7.1fs] %s\n'%(time.time()-T0,m)); LOG.flush()
# ALL MEMBERS, not one representative per (count, profile) class.  That class is
# an equivalence by INVARIANT, not by congruence -- necessary, not sufficient --
# so a result at one member does not transfer to another.  Only CONGRUENT members
# share a locus, and congruence is not what was being deduped.
todo=[]
for n in sorted(R):
    for k in range(3, n+1):
        for idxs in itertools.combinations(range(n), k):
            todo.append((n, {'k':k,'count':None,'idxs':idxs,'cfg':[R[n][i] for i in idxs]}))
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
        base=D.count_at(pt,N); ok=0; uneval=0; changed=0; wraps=[]
        for dv in dirs:
            vals=[D.count_at(pt,N,dv,e) for e in (F(1,64),F(1,256),F(1,1024))]
            seen=[v for v in vals if v is not None]
            if not seen:
                uneval+=1                     # NOT "wrong": unevaluable, recorded
            elif all(v==base for v in seen):
                ok+=1
                # ARC-OR-LOOP, and its LIMIT.  METHODS section 3 decides this at
                # the line's point at infinity, the half-turn (0,d) -- but that
                # construction is for a line in ONE cube's Cayley space.  These
                # directions generally move SEVERAL cubes at once, and the point
                # at infinity of such a line is not a single half-turn
                # substitution.  So the test applies only to single-cube
                # directions; the rest are marked, not guessed.
                blocks=[k for k in range(0,3*(N-1),3)
                        if any(dv[k+r]!=0 for r in range(3))]
                if len(blocks)!=1:
                    w='multi-cube'
                else:
                    try:
                        import subprocess, json as _j
                        from math import gcd as _gcd
                        k0=blocks[0]
                        dd=[dv[k0+r] for r in range(3)]
                        L=1
                        for x in dd: L=L*x.denominator//_gcd(L,x.denominator)
                        dd=[int(x*L) for x in dd]
                        g=0
                        for x in dd: g=_gcd(g,abs(x))
                        if g: dd=[x//g for x in dd]
                        cfgw=[tuple(cfg[0])]+[D.q_of(pt[k:k+3]) for k in range(0,3*(N-1),3)]
                        cfgw[1+k0//3]=tuple([0]+dd)
                        ss=';'.join(','.join(map(str,qq)) for qq in cfgw)
                        eng=D.ENG if max(abs(v) for qq in cfgw for v in qq)<=512 else D.ENGW
                        cmd=[eng,'--quats',ss] if eng==D.ENG else [eng,'--d','0','--quats',ss]
                        pr=subprocess.run(cmd,capture_output=True,text=True)
                        w=_j.loads(pr.stdout.strip().splitlines()[-1])['bounded']
                    except Exception: w=None
                wraps.append(w)
            else:
                changed+=1
    except Exception as e:
        log('n=%d k=%d c=%d CRASH %s'%(n,rep['k'],rep['count'],type(e).__name__)); continue
    rec=dict(n=n,k=rep['k'],count=base,lineality=len(ns),status=st,
             dirs=len(dirs),confirmed=ok,unevaluable=uneval,changed=changed,
             wraps=wraps,idxs=list(rep['idxs']))
    out.append(rec); json.dump(out,open(OUT,'w'),indent=1)
    log('n=%d k=%d c=%-5s lin %d -> %-9s %d dirs: %d confirmed, %d unevaluable, %d changed; wraps %s'
        %(n,rep['k'],base,len(ns),st,len(dirs),ok,uneval,changed,wraps[:6]))
json.dump(out,open(OUT,'w'),indent=1); log('done: %d classes'%len(out))
