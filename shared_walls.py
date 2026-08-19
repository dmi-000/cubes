#!/usr/bin/env python3
"""Do isolated points lie on SHARED walls?

A wall is not a local object: the condition "these four planes are concurrent" is
a function on the whole moduli space, indexed by a combinatorial label -- which
frame, which other cubes, which face normals, which signs.  So the SAME condition
can be evaluated at two different configurations, and two isolated points share a
wall exactly when one condition is tight at both.

Tested on the two non-congruent 183s (Postscript 133), which have identical wall
COUNTS (108 tight, lineality 1) but were never checked for identical wall
MEMBERSHIP.
"""
import itertools, sys
import os as _os
HERE=_os.path.dirname(_os.path.abspath(__file__)); sys.path.insert(0,HERE)
import sympy as sp, dimension as D

def qmul(a,b):
    w1,x1,y1,z1=a; w2,x2,y2,z2=b
    return (w1*w2-x1*x2-y1*y2-z1*z2, w1*x2+x1*w2+y1*z2-z1*y2,
            w1*y2-x1*z2+y1*w2+z1*x2, w1*z2+x1*y2-y1*x2+z1*w2)

def degauge(cfg):
    for g in ((1,0,0,0),(2,1,0,0),(3,1,1,0),(5,1,2,1)):
        out=[qmul(g,q) for q in cfg]
        if all(q[0]!=0 for q in out): return out
    raise RuntimeError

def tight_labels(cfg):
    """the LABEL of every tight condition: (frame, sorted group of (cube,normal,sign))"""
    q=degauge(cfg); D.set_field(0); D.QZERO[:]=[q[0]]
    pt=D.point_of(q); n=len(q)
    quats=D.quats_of(pt,q[0])
    labels=set()
    for i in range(n):
        others=[j for j in range(n) if j!=i]
        Nval={}
        for j in others:
            Rij=D.mat_num(quats[i],quats[j])
            for k in range(3):
                col=[Rij[r][k] for r in range(3)]
                for sgn in (1,-1):
                    Nval[(j,k,sgn)]=[sgn*e for e in col]
        keys=list(Nval)
        groups=[(kk,) for kk in keys]+[(a,b) for a,b in itertools.combinations(keys,2)]
        for g in groups:
            got=D.min_l1_argmin([Nval[k] for k in g])
            if got is None: continue
            if got[0]==1:
                labels.add((i,tuple(sorted(g))))
    return labels

A=[(1,0,0,0),(0,5,3,2),(1,-4,-1,1),(1,1,-1,-4)]
B=[(1,0,0,0),(-2,-2,5,-2),(3,11,-3,-3),(0,-7,4,-3)]
la=tight_labels(A); lb=tight_labels(B)
print('183 class 1: %d tight condition labels'%len(la))
print('183 class 2: %d tight condition labels'%len(lb))
sh=la&lb
print('SHARED labels: %d  (%.1f%% of class 1)'%(len(sh),100*len(sh)/max(len(la),1)))
print()
bysize={}
for i,g in sh: bysize[len(g)]=bysize.get(len(g),0)+1
print('shared by group size (1 = single normal, 2 = pair):',bysize)
byframe={}
for i,g in sh: byframe[i]=byframe.get(i,0)+1
print('shared by frame:',byframe)
