#!/usr/bin/env python3
"""Extend 727's arcs A, B and C to n = 7 — the two-parameter search never run.

[OQ 17](OPEN_QUESTIONS.md): the whole tower above n=6 extends ONE POINT of ONE ARC of a
four-arc node. 727's arcs A, B, C each carry 727 across solved extents and have never
been used as an extension base. `which_member.py` was written for this on 2026-08-09
and its log is 0 bytes.

MEMBERS ARE CHAMBERS, NOT SAMPLES. Each arc is a line a0 + s*v. The count can only
change at a wall, so the distinct members are the CHAMBERS between consecutive wall
roots. Roots are solved (W4 quadratics and W3 quartics via `wall_params`), and one
SIMPLEST rational is taken strictly inside each chamber ([METHODS 15] — midpoints of
roots with unrelated denominators compound past the engine's budget).

GATE, and it is the one [P186](LEDGER.md#p186) showed was missing: from arc D's point —
the recorded 727 — the same menu must rediscover 1217. Unlike the n=7->8 case where the
target had height 61, 1217's seventh cube is (4,-3,-4,-4), height 4, so an exhaustive
[-4,4]^4 menu provably contains it and the gate can be passed rather than excused.
"""
import itertools, json, os, subprocess, sys, time
sys.path.insert(0,'.')
from fractions import Fraction as F
from math import gcd, floor
import wall_params as W
from catcache import catalogue

BASE=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
ARCS={
 # arc D's documented extent is width 1/4 and 5/16, NOT a 1/100 window: a narrow
 # window forces chamber representatives with large denominators (s=1/128 gives
 # a height-3598 cube) which the height filter then discards, emptying the arc.
 'D (the recorded 727)': ([F(2),F(1,7),F(-5,7)], [F(-1),F(-1,7),F(3,14)], F(-1,8), F(1,4)),
 'A': ([F(19,3),F(-7),F(-11)], [F(1),F(-3),F(-6)], F(20639,10000), F(19,6)),
 'B': ([F(4,35),F(2,5),F(-41,35)], [F(1),F(1),F(-4)], F(43,105), F(5794,10000)),
 'C': ([F(245,29),F(-295,29),F(428,29)], [F(1),F(-3,2),F(9,4)], F(11675,10000), F(477720,10000)),
}
K=4

def q_of(c):
    L=1
    for v in c: L=L*v.denominator//gcd(L,v.denominator)
    iq=[L]+[int(v*L) for v in c]; g=0
    for v in iq: g=gcd(g,abs(v))
    return tuple(v//(g or 1) for v in iq)

from simplest import simplest_between as simplest   # one implementation, self-tested

def batch(cfgs):
    inp='\n'.join(';'.join(','.join(map(str,q)) for q in c) for c in cfgs)+'\n'
    big=any(abs(v)>512 for c in cfgs for q in c for v in q)
    exe=(['./cube_regions_q2w','--d','0','--quats-stdin'] if big
         else ['./cube_regions_n','--quats-stdin'])
    p=subprocess.run(exe,input=inp,capture_output=True,text=True)
    out=[]
    for l in p.stdout.splitlines():
        try: out.append(json.loads(l).get('bounded'))
        except Exception: out.append(None)
    return out+[None]*(len(cfgs)-len(out))

def qmul(p,r):
    w,x,y,z=p; e,f,g_,h=r
    return (w*e-x*f-y*g_-z*h, w*f+x*e+y*h-z*g_, w*g_-x*h+y*e+z*f, w*h+x*g_-y*f+z*e)

def canon(t):
    g=0
    for v in t: g=gcd(g,abs(v))
    t=tuple(v//(g or 1) for v in t)
    for v in t:
        if v>0: break
        if v<0: t=tuple(-x for x in t); break
    return t

# THE MENU IS A MENU OF CUBES, NOT OF QUATERNIONS. A cube is invariant under the 24
# octahedral rotations, so q and q*s describe the SAME cube and must give the same count
# -- the first version enumerated quaternions and paid for each redundant copy. Measured:
# 2928 primitive 4-tuples in [-4,4]^4 collapse to 405 distinct cubes, 7.2x fewer, with the
# class of (4,-3,-4,-4) still present and no representative taller than the original menu.
# That is the difference between ~15 h and ~2 h per arc before any parallelism.
OCT=sorted({canon(t) for t in itertools.product((-1,0,1),repeat=4)
            if any(t) and sum(v*v for v in t) in (1,2,4)})
assert len(OCT)==24, 'octahedral group should have 24 rotations, got %d'%len(OCT)

raw=[]
for t in itertools.product(range(-K,K+1),repeat=4):
    if not any(t): continue
    q=canon(t)
    if q not in raw: raw.append(q)
klass={}
for q in raw:
    key=min(canon(qmul(q,s)) for s in OCT)
    h=max(map(abs,q))
    if key not in klass or h<klass[key][0]: klass[key]=(h,q)
cand=sorted(v[1] for v in klass.values())
print('menu: [-%d,%d]^4 -> %d primitive quaternions -> %d distinct CUBES (%.1fx fewer); '
      'class of (4,-3,-4,-4) present: %s'
      %(K,K,len(raw),len(cand),len(raw)/len(cand),
        min(canon(qmul((4,-3,-4,-4),s)) for s in OCT) in klass),flush=True)

SHARD=int(os.environ.get('SHARD','0')); NSHARD=int(os.environ.get('NSHARD','1'))
CKPT='arcs_extend_s%d.jsonl'%SHARD
done=set()
if os.path.exists(CKPT):
    for l in open(CKPT):
        try: d=json.loads(l); done.add((d['arc'],d['s']))
        except Exception: pass
print('shard %d of %d; %d members already checkpointed in %s'%(SHARD,NSHARD,len(done),CKPT),flush=True)

# CONTROL, able to fail: the quotient claims q and q*s are the same cube. If that is
# wrong every number below is wrong, so it is checked against the engine before use, on
# classes chosen at random rather than on the convenient one.
import random as _rnd
_r=_rnd.Random(20260901)
_probe=[]
for q in _r.sample(cand,6):
    for s_ in _r.sample(OCT,3):
        q2=canon(qmul(q,s_))
        if max(map(abs,q2))<=512: _probe.append((q,q2))
_vals=batch([BASE+[a] for a,_ in _probe]+[BASE+[b] for _,b in _probe])
_n=len(_probe)
_bad=[(a,b,_vals[i],_vals[_n+i]) for i,(a,b) in enumerate(_probe) if _vals[i]!=_vals[_n+i]]
print('quotient control: %d octahedral pairs, %d disagreements %s'
      %(_n,len(_bad),_bad[:3] if _bad else ''),flush=True)
if _bad:
    sys.exit('QUOTIENT INVALID: octahedral images give different counts; menu reduction is unsound')

pts,lines=catalogue(BASE)
print('base catalogue: %d triple points, %d crossing lines\n'%(len(pts),len(lines)),flush=True)

for name,(a0,v,lo,hi) in ARCS.items():
    roots=sorted({r for r in list(W.w4_params(a0,v,pts))+list(W.w3_params(a0,v,lines))
                  if lo<r<hi})
    edges=[lo]+roots+[hi]
    reps=[]
    for i in range(len(edges)-1):
        if edges[i+1]-edges[i]<=0: continue
        try: s=simplest(edges[i],edges[i+1])
        except Exception: continue
        reps.append(s)
    six=[q_of([a0[k]+s*v[k] for k in range(3)]) for s in reps]
    keep=[(s,q) for s,q in zip(reps,six) if q and max(map(abs,q))<=4000]
    counts=batch([BASE+[q] for _,q in keep])
    mem=[(s,q) for (s,q),c in zip(keep,counts) if c==727]
    print('arc %-22s %d roots inside, %d chambers, %d representatives count 727'
          %(name,len(roots),len(reps),len(mem)),flush=True)
    best=(0,None,None)
    t0=time.time()
    ck=open(CKPT,'a')
    for mi,(s,q) in enumerate(mem):
        if mi%NSHARD!=SHARD: continue          # shard by member; members are independent
        if (name,str(s)) in done:
            continue
        base6=BASE+[q]
        vals=batch([base6+[x] for x in cand])
        m=max((v for v in vals if v),default=0)
        top=[x for x,v in zip(cand,vals) if v==m]
        # CHECKPOINT EVERY MEMBER. The first run spent 8 h on one arc and wrote nothing,
        # so a kill or a correction cost all of it. One line per member makes the campaign
        # restartable for the price of the correction, which is what makes it safe to fix
        # the method mid-run.
        ck.write(json.dumps({'arc':name,'s':str(s),'cube':list(q),'best':m,
                             'seventh':list(top[0]) if top else None,
                             'menu':len(cand),'secs':round(time.time()-t0,1)})+'\n'); ck.flush()
        print('   [%s] member %d/%d s=%s -> best %s (%.0fs elapsed)'
              %(name,mi+1,len(mem),s,m,time.time()-t0),flush=True)
        if m>best[0]:
            best=(m,s,top[0])
    ck.close()
    print('   best n=7 over this arc: %s at s=%s with seventh cube %s   (%.0fs)'
          %(best[0],best[1],best[2],time.time()-t0),flush=True)
    if name.startswith('D'):
        ok=best[0]>=1217
        print('   GATE (shard-local): arc D must reach 1217 -> %s'%('OK' if ok else 'not in this shard'),
              flush=True)
        # SHARDING BREAKS A GLOBAL GATE. Only the shard holding the member that reaches
        # 1217 can see it, so exiting on a shard-local miss would kill the other seven and
        # look like a failed gate. The gate is global and is evaluated by aggregating the
        # checkpoints (see arcs_report.py); a shard only reports what it saw.
        if NSHARD==1 and not ok:
            sys.exit('gate failed: the menu cannot rediscover the record; negatives would be void')
