#!/usr/bin/env python3
"""Which configurations share walls with which?

A wall is a condition indexed by a combinatorial label (frame, group of
(cube, normal, sign)), so the SAME condition can be evaluated anywhere and two
configurations share a wall when one label is tight at both (Postscript 136).
The two 183s share 88 of 108. This asks the question across the tower and both
67s -- including the pair in DIFFERENT FIELDS, where labels are still comparable
because they are combinatorial, not numeric.
"""
import itertools, json, sys
import os as _os
HERE=_os.path.dirname(_os.path.abspath(__file__)); sys.path.insert(0,HERE)
from fractions import Fraction as F
import dimension as D
from qfield import Q

def qmul(a,b):
    w1,x1,y1,z1=a; w2,x2,y2,z2=b
    return (w1*w2-x1*x2-y1*y2-z1*z2, w1*x2+x1*w2+y1*z2-z1*y2,
            w1*y2-x1*z2+y1*w2+z1*x2, w1*z2+x1*y2-y1*x2+z1*w2)

def labels(cfg, d=0):
    """tight condition labels; works over Q and over Q(sqrt d)"""
    D.set_field(d)
    if d==0:
        for g in ((1,0,0,0),(2,1,0,0),(3,1,1,0),(5,1,2,1)):
            out=[qmul(g,q) for q in cfg]
            if all(q[0]!=0 for q in out): cfg=out; break
        D.QZERO[:]=[cfg[0]]; pt=D.point_of(cfg)
    else:
        qs=[tuple(Q(F(p),F(q),d) for p,q in quat) for quat in cfg]
        D.QZERO[:]=[qs[0]]
        pt=[]
        for q in qs[1:]: pt+=D.cayley_of(q)
        cfg=qs
    n=len(cfg); quats=D.quats_of(pt,cfg[0]); out=set()
    for i in range(n):
        Nval={}
        for j in [x for x in range(n) if x!=i]:
            Rij=D.mat_num(quats[i],quats[j])
            for k in range(3):
                col=[Rij[r][k] for r in range(3)]
                for sgn in (1,-1): Nval[(j,k,sgn)]=[sgn*e for e in col]
        keys=list(Nval)
        for g in [(kk,) for kk in keys]+[(a,b) for a,b in itertools.combinations(keys,2)]:
            got=D.min_l1_argmin([Nval[k] for k in g])
            if got is not None and got[0]==1: out.add((i,tuple(sorted(g))))
    return out

BASE=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
CASES=[
 ('67 octahedral', [((1,0),(0,0),(0,0),(0,0)),((1,0),(1,0),(0,1),(0,0)),((-1,0),(1,0),(0,1),(0,0))], 2),
 ('67 golden',     [((1,0),(0,0),(0,0),(0,0)),((2,0),(1,1),(-1,1),(0,0)),((-2,0),(1,1),(-1,1),(0,0))], 5),
 ('183 class 1', [(1,0,0,0),(0,5,3,2),(1,-4,-1,1),(1,1,-1,-4)], 0),
 ('183 class 2', [(1,0,0,0),(-2,-2,5,-2),(3,11,-3,-3),(0,-7,4,-3)], 0),
 ('393',  BASE, 0),
 ('727',  BASE+[(7,14,1,-5)], 0),
]
L={}
for nm,cfg,d in CASES:
    L[nm]=labels(cfg,d)
    print('%-14s %4d tight labels  (n=%d)'%(nm,len(L[nm]),len(cfg)),flush=True)
print()
print('%-14s %s'%('','  '.join('%-13s'%n for n,_,_ in CASES)))
for a,_,_ in CASES:
    row=[]
    for b,_,_ in CASES:
        sh=len(L[a]&L[b])
        row.append('%-13s'%('%d/%d'%(sh,len(L[a]))))
    print('%-14s %s'%(a,'  '.join(row)))
