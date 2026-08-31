#!/usr/bin/env python3
"""Is 3917's locus a 2-D SURFACE, or two curves crossing at a NODE?

Two verified tangents do not imply a 2-dimensional locus. The project's own
precedent is 727's arc D: `MAXIMISER_TAXONOMY.md` records "the record carries two
independent tangents ... whose combinations all fail — two arcs meeting at a node,
not a surface." So the discriminating test is whether COMBINATIONS a*v1 + b*v2
preserve the count.

Run exactly the way [P184] tests directions: eps a positive infinitesimal, both
signs, wide engine on refusal. Gated on 727 reproducing the NODE verdict — if the
test says 727 is a surface, it is not discriminating.
"""
import sys
sys.path.insert(0, '.')
from fractions import Fraction as F
from math import gcd
from qfield import Q
import dimension as D
from epscount import count_eps
from eps_null import walls_and_null

BASE=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
C6 = BASE+[(7,14,1,-5)]
C10 = BASE+[(7,14,1,-5),(4,-3,-4,-4),(24,-24,24,-61),(57,57,56,57),
            (88787,-9061,74275,113786)]
COMBOS = [(1,1),(1,-1),(2,1),(1,2),(3,1),(1,3),(2,-1),(-1,2),(3,2),(5,3)]


def primitive(v):
    den=1
    for x in v: den=den*F(x).denominator//gcd(den,F(x).denominator)
    iv=[int(F(x)*den) for x in v]; g=0
    for x in iv: g=gcd(g,abs(x))
    return [x//(g or 1) for x in iv]


def holds(cubes, pt, ncols, rec, q0, d3):
    full=[F(0)]*(ncols-3)+[F(x) for x in d3]
    out=[]
    for sgn in (1,-1):
        v=count_eps(pt,[Q(sgn*x,0,0) for x in full],0,q0)
        if v is None:
            v=count_eps(pt,[Q(sgn*x,0,0) for x in full],0,q0,wide=True)
        out.append(v)
    return out


def verdict(cubes, t1, t2, label):
    pt,walls,null,ncols = walls_and_null(cubes)
    rec = D.count_at(pt, len(cubes))
    z = count_eps(pt,[Q(0,0,0)]*ncols,0,cubes[0]) or \
        count_eps(pt,[Q(0,0,0)]*ncols,0,cubes[0],wide=True)
    print('\n%s: record %d   zero-control -> %s %s'
          %(label,rec,z,'OK' if z==rec else 'CONTROL FAILED'),flush=True)
    if z!=rec: return
    for name,d in (('v1',t1),('v2',t2)):
        r=holds(cubes,pt,ncols,rec,cubes[0],d)
        print('   %-8s %-16s +eps %-6s -eps %-6s  %s'
              %(name,str(d),r[0],r[1],'holds' if r==[rec,rec] else 'CHANGES'),flush=True)
    nh=nc=nu=0
    for a,b in COMBOS:
        d=primitive([a*x+b*y for x,y in zip(t1,t2)])
        r=holds(cubes,pt,ncols,rec,cubes[0],d)
        if None in r: nu+=1; tag='UNEVALUATED'
        elif r==[rec,rec]: nh+=1; tag='holds'
        else: nc+=1; tag='CHANGES'
        print('   %dv1%+dv2  %-16s +eps %-6s -eps %-6s  %s'
              %(a,b,str(d),r[0],r[1],tag),flush=True)
    print('   -> %d of %d combinations hold, %d change, %d unevaluated'%(nh,len(COMBOS),nc,nu),
          flush=True)
    print('   VERDICT: %s'%('2-DIMENSIONAL surface (combinations survive)' if nc==0 and nu==0
                            else 'NODE — two curves crossing, combinations fail'
                            if nh==0 and nu==0 else 'MIXED/INCONCLUSIVE'),flush=True)


verdict(C6, (14,2,-3), (21,4,-6), 'GATE  n=6 727 arc D (known to be a NODE)')
verdict(C10, (1,-14,0), (5,0,14), 'n=10 3917')
