#!/usr/bin/env python3
"""Iterated boundary climb: solve the region, walk out through its walls, repeat.

This is the loop that produced 3917 ([P191]) and then 3921 and 2787 ([P198]), made
self-sustaining. Per record:

  1. wall matrix -> null space -> LLL -> eps-verified PRESERVING basis (P196);
  2. directions = that basis and integer combinations, BOTH signs (regions are not
     symmetric: at 2785 one wall sits at 4.4e-6 and another at 0.101);
  3. for each direction, fine step 1/(D*M) and BISECT to the first count change —
     a coarse step lands past several walls and misreads the boundary (P198);
  4. any count ABOVE the record becomes the next base;
  5. before accepting, find a LOW-HEIGHT member of the new region by searching simple
     rationals along the same direction (METHODS 15), so both engines can verify it.

Every accepted record is gated: both engines agree, and the count is invariant under
three global rotations (it cannot depend on the counting box, P180).
"""
import json, random, subprocess, sys
sys.path.insert(0,'.')
from fractions import Fraction as F
from math import gcd
import sympy as sp
from qfield import Q
import dimension as D
from epscount import count_eps
from eps_null import walls_and_null
from lll import lll

M=4096; NDIR=18; ROTS=((2,1,0,0),(1,1,1,0),(3,0,1,2))

def prim(v):
    den=1
    for x in v: den=den*F(x).denominator//gcd(den,F(x).denominator)
    iv=[int(F(x)*den) for x in v]; g=0
    for x in iv: g=gcd(g,abs(x))
    return tuple(x//(g or 1) for x in iv)

def canon(t):
    g=0
    for v in t: g=gcd(g,abs(v))
    t=tuple(v//(g or 1) for v in t)
    for v in t:
        if v>0: break
        if v<0: t=tuple(-x for x in t); break
    return t

def qmul(p,r):
    w,x,y,z=p; e,f,g_,h=r
    return (w*e-x*f-y*g_-z*h,w*f+x*e+y*h-z*g_,w*g_-x*h+y*e+z*f,w*h+x*g_-y*f+z*e)

def run(cfg,exe):
    st=";".join(",".join(map(str,q)) for q in cfg)
    cmd=[exe,'--quats',st] if exe.endswith('_n') else [exe,'--d','0','--quats',st]
    try:
        d=json.loads(subprocess.run(cmd,capture_output=True,text=True).stdout)
        return d['bounded']
    except Exception: return None

def cnt(cfg):
    c=run(cfg,'./cube_regions_n')
    return c if c is not None else run(cfg,'./cube_regions_q2w')

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

def gate(cfg,c):
    a=run(cfg,'./cube_regions_n'); b=run(cfg,'./cube_regions_q2w')
    if b!=c or (a is not None and a!=c): return False,'engines disagree (%s,%s)'%(a,b)
    for rot in ROTS:
        if run([canon(qmul(rot,q)) for q in cfg],'./cube_regions_q2w')!=c:
            return False,'not rotation-invariant'
    return True,'both engines + 3 rotations agree'

def climb(cubes,label):
    for it in range(1,8):
        n=len(cubes)
        pt,walls,null,ncols=walls_and_null(cubes)
        rec=D.count_at(pt,n)
        Dden=max(abs(v) for v in cubes[-1]) or 1
        print('\n[%s iter %d] record %d  deficit %d  height %d'
              %(label,it,rec,len(null),max(abs(v) for q in cubes for v in q)),flush=True)
        B=[prim(b) for b in lll([list(prim(v)) for v in null])]
        good=[]
        for b in B:
            ok=True
            for sgn in (1,-1):
                c=count_eps(pt,[Q(sgn*F(x),0,0) for x in b],0,cubes[0])
                if c is None: c=count_eps(pt,[Q(sgn*F(x),0,0) for x in b],0,cubes[0],wide=True)
                if c!=rec: ok=False; break
            if ok: good.append(b)
        if not good:
            print('   no preserving direction; stop'); return cubes,rec
        print('   preserving rank %d'%sp.Matrix([list(g) for g in good]).rank(),flush=True)
        rnd=random.Random(17+it)
        dirs=[tuple(g) for g in good]
        while len(dirs)<NDIR:
            co=[rnd.randint(-2,2) for _ in good]
            if any(co): dirs.append(prim([sum(a*g[i] for a,g in zip(co,good)) for i in range(ncols)]))
        best=(rec,None)
        den=Dden*M
        for v0 in dirs[:NDIR]:
            for sgn in (1,-1):
                v=tuple(sgn*x for x in v0)
                lo,hi,c=0,1,None
                while hi<=den*8:
                    p2=[pt[i]+F(hi,den)*v[i] for i in range(ncols)]
                    c=cnt(cfg_at(p2,cubes[0]))
                    if c is None: hi*=2; continue
                    if c!=rec: break
                    lo=hi; hi*=2
                if c is None or c==rec: continue
                while hi-lo>1:
                    mid=(lo+hi)//2
                    cm=cnt(cfg_at([pt[i]+F(mid,den)*v[i] for i in range(ncols)],cubes[0]))
                    if cm is None: break
                    if cm==rec: lo=mid
                    else: hi=mid
                c=cnt(cfg_at([pt[i]+F(hi,den)*v[i] for i in range(ncols)],cubes[0]))
                if c and c>best[0]:
                    best=(c,(v,F(hi,den)))
                    print('   boundary crossing -> %d  (ABOVE %d)'%(c,rec),flush=True)
        if best[1] is None:
            print('   no crossing above the record; region is locally maximal'); return cubes,rec
        c,(v,s)=best
        cheap=None
        for q in range(2,200):
            for p in range(1,q):
                t=F(p,q)
                if abs(float(t)-float(s))>0.25*float(s) or t<=0: continue
                cf=cfg_at([pt[i]+t*v[i] for i in range(ncols)],cubes[0])
                h=max(abs(x) for qq in cf for x in qq)
                if cnt(cf)==c and (cheap is None or h<cheap[0]): cheap=(h,t,cf)
                break
        cf=cheap[2] if cheap else cfg_at([pt[i]+s*v[i] for i in range(ncols)],cubes[0])
        ok,why=gate(cf,c)
        print('   NEW RECORD %d  height %d  gate: %s'
              %(c,max(abs(x) for q in cf for x in q),why),flush=True)
        if not ok: return cubes,rec
        print('   %s'%';'.join(','.join(map(str,q)) for q in cf),flush=True)
        cubes=cf
    return cubes,rec

BASE=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
N9=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1),(7,14,1,-5),
    (4,-3,-4,-4),(168,-168,168,-415),(88787,-9061,74275,113786)]
N10=N9[:8]+[(57,57,56,57)]+[N9[8]]
climb(N9,'n=9')
climb(N10,'n=10')
