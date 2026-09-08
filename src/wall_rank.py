#!/usr/bin/env python3
"""Does wall RANK separate a record from a near-record, where wall COUNT does not?

Postscript 139: wall label count correlates with region count but SATURATES --
179 and 183 are indistinguishable (106.9 vs 108.0 labels, 95.6 vs 95.3 overlap).
A filter, not a discriminator.

Dependency structure is the untested candidate, and it has form: what distinguishes
the two 67s is that the octahedral's 6 walls are INDEPENDENT (rank 6 = ambient,
pinned at first order) while the golden's 9 are DEPENDENT (rank 6 of 9), and that
difference tracked their neighbourhood structure (Postscripts 122, 129). Size said
nothing there either; dependency said everything.

So: for each retained configuration, compute the DISTINCT walls (labels grouped by
gradient up to scale), their RANK, and the resulting LINEALITY. If 183 differs from
179 in rank or lineality while matching in label count, that is the discriminator
wall counting misses.
"""
import itertools, os, sys
from collections import defaultdict
import os as _os
HERE=_os.path.dirname(_os.path.abspath(__file__)); sys.path.insert(0,HERE)
import sympy as sp, dimension as D

def qmul(a,b):
    w1,x1,y1,z1=a; w2,x2,y2,z2=b
    return (w1*w2-x1*x2-y1*y2-z1*z2, w1*x2+x1*w2+y1*z2-z1*y2,
            w1*y2-x1*z2+y1*w2+z1*x2, w1*z2+x1*y2-y1*x2+z1*w2)
def degauge(cfg):
    for g in ((1,0,0,0),(2,1,0,0),(3,1,1,0),(5,1,2,1),(7,2,3,1)):
        out=[qmul(g,q) for q in cfg]
        if all(q[0]!=0 for q in out): return out
    return None

def profile(cfg):
    q=degauge(cfg)
    if q is None: return None
    D.set_field(0); D.QZERO[:]=[q[0]]
    pt=D.point_of(q)
    if pt is None: return None
    n=len(q); ncols=3*(n-1)
    vars_=sp.symbols('c0:%d'%ncols); Rs=D.frames(vars_,q[0])
    tight,loose=D.cached_conditions(Rs,n,vars_,pt,D.quats_of(pt,q[0]),q[0])
    good=[t for t in tight if not t['degenerate']]
    def _norm(g):
        piv=next((x for x in g if x!=0),None)
        return tuple(str(x/piv) for x in g) if piv is not None else None
    seen,walls={},[]
    for t in good:
        k=_norm(t['grad'])
        if k is not None and k not in seen: seen[k]=True; walls.append(t['grad'])
    lin=len(D.nullspace(walls,ncols))
    return dict(tight=len(good),loose=loose,walls=len(walls),
                rank=ncols-lin,lineality=lin,ambient=ncols)

rows=[]; seen=set()
for l in open(HERE+'/wideclimb_n4.log'):
    if 'CFG peak=' not in l: continue
    head,c=l.split('CFG peak=')[1].split(' ',1)
    peak=int(head); cfg=tuple(tuple(int(x) for x in g.split(',')) for g in c.strip().split(';'))
    if cfg in seen: continue
    seen.add(cfg); rows.append((peak,cfg))
print('%d distinct configurations'%len(rows),flush=True)

by=defaultdict(list)
for peak,cfg in rows:
    p=profile(list(cfg))
    if p is None: print('   peak %d SKIPPED (half-turn unresolvable)'%peak,flush=True); continue
    by[peak].append(p)
    print('   peak %3d: %3d tight, %2d DISTINCT WALLS, rank %d of %d, lineality %d'
          %(peak,p['tight'],p['walls'],p['rank'],p['ambient'],p['lineality']),flush=True)
print()
print('peak | n | mean tight | mean distinct walls | mean rank | mean lineality')
for p in sorted(by):
    v=by[p]; f=lambda k: sum(x[k] for x in v)/len(v)
    print('%4d |%2d |   %6.1f   |       %5.2f        |   %4.2f   |     %4.2f'
          %(p,len(v),f('tight'),f('walls'),f('rank'),f('lineality')))
