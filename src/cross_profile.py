#!/usr/bin/env python3
"""Does the CROSSABILITY PROFILE discriminate a record from a near-record?

Wall count, wall rank and lineality all saturate: 179 and 183 are identical on
every one (12 walls, rank 8, lineality 1, ~108 tight conditions) -- Postscripts
139, 140. Nothing measured so far separates them.

But those are counts of the wall SET. The crossability profile is a count of the
wall SYSTEM's degeneracy: how many k-subsets admit a direction crossing exactly
those k walls and no others. At 183 only 3 of 66 pairs are crossable, so the
profile is far from saturated even where the totals are.

This measures, per configuration: the number of crossable pairs, and the counts
reachable beyond them. If records have systematically fewer (or more) crossable
pairs than near-records, that is the discriminator the totals miss.
"""
import itertools, json, sys, time
from collections import Counter, defaultdict
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
    for g in ((1,0,0,0),(2,1,0,0),(3,1,1,0),(5,1,2,1),(7,2,3,1)):
        out=[qmul(g,q) for q in cfg]
        if all(x[0]!=0 for x in out): return out
    return None

def profile(cfg):
    q=degauge(list(cfg))
    if q is None: return None
    D.set_field(0); D.QZERO[:]=[q[0]]
    pt=D.point_of(q)
    if pt is None: return None
    n=len(q); ncols=3*(n-1)
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
    m=len(W); rank=ncols-len(D.nullspace(W,ncols))
    pairs=list(itertools.combinations(range(m),2))
    cross=0; beyond=Counter()
    for S in pairs:
        rest=[W[t] for t in range(m) if t not in S]
        v=None
        for u in D.nullspace(rest,ncols):
            if all(sum(W[i][t]*u[t] for t in range(ncols))!=0 for i in S): v=u; break
        if v is None: continue
        cross+=1
        dv=D.normalize_dir(v)
        for d in (dv,[-x for x in dv]):
            c=count_eps(pt,d,0,q[0])
            if c is not None: beyond[c]+=1
    return dict(walls=m,rank=rank,pairs=len(pairs),crossable=cross,
                beyond=dict(sorted(beyond.items(),reverse=True)),
                best=max(beyond) if beyond else None)

rows=[]; seen=set()
for l in open(HERE+'/wideclimb_n4.log'):
    if 'CFG peak=' not in l: continue
    h,c=l.split('CFG peak=')[1].split(' ',1)
    peak=int(h); cfg=tuple(tuple(int(x) for x in g.split(',')) for g in c.strip().split(';'))
    if cfg in seen: continue
    seen.add(cfg); rows.append((peak,cfg))
KN=(((1,0,0,0),(0,5,3,2),(1,-4,-1,1),(1,1,-1,-4)))
if KN not in seen: rows.append((183,KN))
print('%d configurations'%len(rows),flush=True)

agg=defaultdict(list)
for peak,cfg in sorted(rows,key=lambda r:-r[0]):
    p=profile(cfg)
    if p is None: continue
    agg[peak].append(p)
    print('  peak %3d: %2d walls rank %d | crossable pairs %2d of %2d | best beyond %s (drop %s)'
          %(peak,p['walls'],p['rank'],p['crossable'],p['pairs'],p['best'],
            (peak-p['best']) if p['best'] else '-'),flush=True)
print()
print('peak | n | mean walls | mean crossable pairs | mean drop to best neighbour')
for k in sorted(agg):
    v=agg[k]; f=lambda key: sum(x[key] for x in v)/len(v)
    drops=[k-x['best'] for x in v if x['best']]
    print('%4d |%2d |   %5.2f    |        %5.2f         |      %s'
          %(k,len(v),f('walls'),f('crossable'),
            '%.2f'%(sum(drops)/len(drops)) if drops else '-'))
json.dump({str(k):v for k,v in agg.items()},open(HERE+'/cross_profile.json','w'),indent=1)
