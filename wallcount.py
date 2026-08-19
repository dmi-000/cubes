#!/usr/bin/env python3
"""How many walls does a configuration lie on, and does it predict isolation?

Uses the shared conditions cache, so this is nearly free.  Reports tight
conditions, DISTINCT walls (conditions grouped by gradient up to scale), the
rank of those walls, and the lineality = ambient - rank.
"""
import json, os, sys, itertools
import os as _os
HERE=_os.path.dirname(_os.path.abspath(__file__)); sys.path.insert(0,HERE)
import sympy as sp, dimension as D
from qfield import Q
from fractions import Fraction as F

BASE=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
R={6:BASE+[(7,14,1,-5)]}
R[7]=R[6]+[(4,-3,-4,-4)]; R[8]=R[7]+[(24,-24,24,-61)]; R[9]=R[8]+[(56,56,55,56)]

def walls_of(quats, d=0):
    D.set_field(d); D.QZERO[:]=[quats[0]]
    pt=D.point_of(quats) if d==0 else [x for q in quats[1:] for x in D.cayley_of(q)]
    ncols=3*(len(quats)-1)
    vars_=sp.symbols('c0:%d'%ncols); Rs=D.frames(vars_,quats[0])
    tight,loose=D.cached_conditions(Rs,len(quats),vars_,pt,D.quats_of(pt,quats[0]),quats[0])
    good=[t for t in tight if not t['degenerate']]
    def _norm(g):
        piv=next((x for x in g if x!=0),None)
        return tuple(str(x/piv) for x in g) if piv is not None else None
    seen,walls={},[]
    for t in good:
        k=_norm(t['grad'])
        if k is not None and k not in seen: seen[k]=True; walls.append(t['grad'])
    lin=len(D.nullspace(walls,ncols))
    return dict(tight=len(good),loose=loose,walls=len(walls),ambient=ncols,
                rank=ncols-lin,lineality=lin,count=D.count_at(pt,len(quats)))

if __name__=='__main__':
    rows=[]
    for d,name,quats in ((2,'octahedral 67',[tuple(Q(F(p),F(q),2) for p,q in x) for x in
                          [((1,0),(0,0),(0,0),(0,0)),((1,0),(1,0),(0,1),(0,0)),((-1,0),(1,0),(0,1),(0,0))]]),
                         (5,'golden 67',[tuple(Q(F(p),F(q),5) for p,q in x) for x in
                          [((1,0),(0,0),(0,0),(0,0)),((2,0),(1,1),(-1,1),(0,0)),((-2,0),(1,1),(-1,1),(0,0))]])):
        r=walls_of(quats,d); r['name']=name; rows.append(r)
    for n in (6,7,8,9):
        r=walls_of(R[n]); r['name']='n=%d record'%n; rows.append(r)
    print('%-16s %6s %6s %7s %7s %5s %6s'%('','count','tight','walls','ambient','rank','lin'))
    for r in rows:
        print('%-16s %6d %6d %7d %7d %5d %6d'
              %(r['name'],r['count'],r['tight'],r['walls'],r['ambient'],r['rank'],r['lineality']))
    json.dump(rows,open(os.path.join(HERE,'wallcount.json'),'w'),indent=1)
