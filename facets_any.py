#!/usr/bin/env python3
"""Facet census of any record, to test how far the shared walls reach down the tower.

[P202] found the coincidences {1,3,6} and {0,5,6} bounding the record region at n=8,
at both n=9 records, and at n=10 — literally the same walls, since cubes 0-6 are the
same quaternion in all of them.

Both need cube 6 = (4,-3,-4,-4), which first appears at n=7. So **1217 is the only
lower rung where the question is well posed**; at 727 and 393 those walls do not exist
and the question becomes what bounds them instead, and whether any of it is shared
upward.
"""
import itertools, json, random, subprocess, sys
sys.path.insert(0,'.')
from fractions import Fraction as F
from math import gcd
import sympy as sp
from qfield import Q
import dimension as D
from epscount import count_eps
from eps_null import walls_and_null
from lll import lll

M=4096; NDIR=48; REACH=64
BASE=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
CASES=[('1217 (n=7)', BASE+[(7,14,1,-5),(4,-3,-4,-4)]),
       ('727  (n=6)', BASE+[(7,14,1,-5)]),
       ('393  (n=5)', BASE)]

def prim(v):
    den=1
    for x in v: den=den*F(x).denominator//gcd(den,F(x).denominator)
    iv=[int(F(x)*den) for x in v]; g=0
    for x in iv: g=gcd(g,abs(x))
    return tuple(x//(g or 1) for x in iv)

def cfg_at(pt,q0):
    D.set_field(0); D.QZERO[:]=[q0]
    out=[]
    for q in D.quats_of(list(pt),q0):
        iv=[F(x) for x in q]; L=1
        for x in iv: L=L*x.denominator//gcd(L,x.denominator)
        w=[int(x*L) for x in iv]; g=0
        for x in w: g=gcd(g,abs(x))
        out.append(tuple(x//(g or 1) for x in w))
    return out

def cnt(cfg):
    st=";".join(",".join(map(str,q)) for q in cfg)
    m=max(abs(v) for q in cfg for v in q)
    for exe in ([['./cube_regions_n','--quats',st]] if m<=200000 else [])+[['./cube_regions_q2w','--d','0','--quats',st]]:
        try: return json.loads(subprocess.run(exe,capture_output=True,text=True).stdout)['bounded']
        except Exception: pass
    return None

for label,cubes in CASES:
    n=len(cubes)
    pt,walls,null,ncols=walls_and_null(cubes)
    rec=D.count_at(pt,n)
    B=[prim(b) for b in lll([list(prim(v)) for v in null])]
    good=[]
    for b in B:
        ok=True
        for sgn in (1,-1):
            c=count_eps(pt,[Q(sgn*F(x),0,0) for x in b],0,cubes[0])
            if c is None: c=count_eps(pt,[Q(sgn*F(x),0,0) for x in b],0,cubes[0],wide=True)
            if c!=rec: ok=False; break
        if ok: good.append(b)
    rk=sp.Matrix([list(g) for g in good]).rank() if good else 0
    print('\n%s  record %d  deficit %d  preserving rank %d'%(label,rec,len(null),rk),flush=True)
    if not good:
        print('   no preserving direction (the locus is a NODE or a point) — '
              'the facet walk does not apply here',flush=True); continue
    base=cfg_at(pt,cubes[0])
    bsub=tuple(cnt([base[i] for i in range(n) if i!=j]) for j in range(n))
    Dden=max(abs(v) for v in cubes[-1]); den=Dden*M
    rnd=random.Random(41)
    dirs=[]
    for g in good: dirs += [tuple(g),tuple(-x for x in g)]
    while len(dirs)<NDIR:
        co=[rnd.randint(-3,3) for _ in good]
        if any(co): dirs.append(prim([sum(a*g[i] for a,g in zip(co,good)) for i in range(ncols)]))
    facets={}
    for i,v in enumerate(dirs[:NDIR],1):
        lo,hi,c=0,1,None
        while hi<=den*REACH:
            c=cnt(cfg_at([pt[i2]+F(hi,den)*v[i2] for i2 in range(ncols)],cubes[0]))
            if c is None: hi*=2; continue
            if c!=rec: break
            lo=hi; hi*=2
        if c is None or c==rec: continue
        while hi-lo>1:
            mid=(lo+hi)//2
            cm=cnt(cfg_at([pt[i2]+F(mid,den)*v[i2] for i2 in range(ncols)],cubes[0]))
            if cm is None: break
            if cm==rec: lo=mid
            else: hi=mid
        full=cfg_at([pt[i2]+F(hi,den)*v[i2] for i2 in range(ncols)],cubes[0]); c=cnt(full)
        if c is None or c==rec: continue
        sub=tuple(cnt([full[i2] for i2 in range(n) if i2!=j]) for j in range(n))
        sig=tuple(j for j in range(n) if sub[j]==bsub[j])
        if sig not in facets: facets[sig]=(float(hi)/den,c)
    print('   %d facets:'%len(facets),flush=True)
    for sig,(d,c) in sorted(facets.items(),key=lambda kv:kv[1][0]):
        mark=''
        if sig==(1,3,6): mark='   <== the wall shared by n=8,9,10'
        if sig==(0,5,6): mark='   <== the other shared wall'
        print('      cubes %-14s at %.5g   count outside %d%s'%(str(list(sig)),d,c,mark),flush=True)
