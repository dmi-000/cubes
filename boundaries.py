#!/usr/bin/env python3
"""Boundaries of the record REGIONS, identified by WHICH CUBES make each wall.

The loci are (deficit-1)-dimensional ([P196]): 1895 rank 2, 2785 rank 3, 3917 rank 5.
Their boundaries are walls. Rather than map the geometry point by point, each wall is
identified by the tool [P194] found: at a point just OUTSIDE, compute all n subset
counts of size n-1 and see which ones change. A wall whose coincidence involves cubes
{i,j} is invisible to the subsets that delete i or j, so the SIGNATURE of unchanged
subsets names the cubes that make the wall.

Method per record:
  1. take the verified preserving basis (eps-verified, [P196]);
  2. sample directions in that subspace;
  3. walk out in steps of 1/D, D the record's own denominator, so heights stay put
     ([METHODS 15] - probes in a foreign denominator blow the engine budget);
  4. at the first point where the count changes, take the subset signature;
  5. group directions by signature -> the distinct bounding walls.

Gate: s = 0 must reproduce the record, and every direction must hold for at least one
step (it is a verified preserving direction).
"""
import itertools, random, sys
sys.path.insert(0,'.')
from fractions import Fraction as F
from math import gcd
import sympy as sp
from qfield import Q
import dimension as D
from epscount import count_eps
from eps_null import walls_and_null
from lll import lll

BASE=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
CASES=[('n=8  1895', BASE+[(7,14,1,-5),(4,-3,-4,-4),(24,-24,24,-61)], 24),
       ('n=9  2785', BASE+[(7,14,1,-5),(4,-3,-4,-4),(24,-24,24,-61),(56,56,55,56)], 56),
       ('n=10 3917', BASE+[(7,14,1,-5),(4,-3,-4,-4),(24,-24,24,-61),(57,57,56,57),
                           (88787,-9061,74275,113786)], 88787)]
NDIR=14; MAXK=400

def prim(v):
    den=1
    for x in v: den=den*F(x).denominator//gcd(den,F(x).denominator)
    iv=[int(F(x)*den) for x in v]; g=0
    for x in iv: g=gcd(g,abs(x))
    return tuple(x//(g or 1) for x in iv)

def cfg_at(pt, q0, n):
    D.set_field(0); D.QZERO[:]=[q0]
    qs=D.quats_of(list(pt), q0)
    out=[]
    for q in qs:
        iv=[F(x) for x in q]; L=1
        for x in iv: L=L*x.denominator//gcd(L,x.denominator)
        w=[int(x*L) for x in iv]; g=0
        for x in w: g=gcd(g,abs(x))
        out.append(tuple(x//(g or 1) for x in w))
    return out

def count(cfg):
    import json, subprocess
    st=";".join(",".join(map(str,q)) for q in cfg)
    m=max(abs(v) for q in cfg for v in q)
    cmd=(['./cube_regions_n','--quats',st] if m<=512 else ['./cube_regions_q2w','--d','0','--quats',st])
    try: return json.loads(subprocess.run(cmd,capture_output=True,text=True).stdout)['bounded']
    except Exception: return None

for lbl,cubes,Dden in CASES:
    n=len(cubes)
    pt,walls,null,ncols=walls_and_null(cubes)
    rec=D.count_at(pt,n)
    print('\n%s  record %d  deficit %d'%(lbl,rec,len(null)),flush=True)
    if count(cfg_at(pt,cubes[0],n))!=rec:
        print('   GATE FAILED: adapter does not reproduce the record'); continue
    # verified preserving basis: LLL null basis, keep the ones that preserve
    B=[prim(b) for b in lll([list(prim(v)) for v in null])]
    good=[]
    for b in B:
        ok=True
        for sgn in (1,-1):
            c=count_eps(pt,[Q(sgn*F(x),0,0) for x in b],0,cubes[0])
            if c is None: c=count_eps(pt,[Q(sgn*F(x),0,0) for x in b],0,cubes[0],wide=True)
            if c!=rec: ok=False; break
        if ok: good.append(b)
    print('   preserving basis: rank %d'%sp.Matrix([list(g) for g in good]).rank(),flush=True)
    rnd=random.Random(5); sigs={}
    dirs=[tuple(g) for g in good]
    while len(dirs)<NDIR:
        co=[rnd.randint(-2,2) for _ in good]
        if any(co): dirs.append(prim([sum(a*g[i] for a,g in zip(co,good)) for i in range(ncols)]))
    # FINE step plus BISECTION. A step of 1/D with D the record denominator is far
    # too coarse below n=10: at 1895 (D=24) and 2785 (D=56) EVERY direction left the
    # region on step 1, so the signature described a point several walls out rather
    # than the bounding wall. The step is refined by M and the first crossing is then
    # bisected, so the reported wall is the one actually bounding the region.
    M=4096
    for v in dirs[:NDIR]:
        den=Dden*M
        def cnt_at(k):
            p2=[pt[i]+F(k,den)*v[i] for i in range(ncols)]
            return count(cfg_at(p2,cubes[0],n)), p2
        lo=0; hi=1; c=None
        while hi<=den*4:
            c,_=cnt_at(hi)
            if c is None: hi*=2; continue
            if c!=rec: break
            lo=hi; hi*=2
        if c is None or c==rec:
            print('   dir height %-6d : still %d out to k/%d = %.3g (no boundary)'
                  %(max(abs(x) for x in v),rec,den,hi/den),flush=True); continue
        while hi-lo>1:                       # bisect to the FIRST crossing
            mid=(lo+hi)//2
            cm,_=cnt_at(mid)
            if cm is None: break
            if cm==rec: lo=mid
            else: hi=mid
        k=hi; c,p2=cnt_at(k)
        if c is None or c==rec: continue
        full=cfg_at(p2,cubes[0],n)
        subs=tuple(count([full[i] for i in range(n) if i!=j]) for j in range(n))
        base=cfg_at(pt,cubes[0],n)
        bsub=tuple(count([base[i] for i in range(n) if i!=j]) for j in range(n))
        unch=tuple(j for j in range(n) if subs[j]==bsub[j])
        sigs.setdefault(unch,[]).append((max(abs(x) for x in v),k,c))
        print('   dir h=%-6d boundary at %s = %.3g -> count %d, unchanged subsets %s'
              %(max(abs(x) for x in v),'%d/%d'%(k,den),k/den,c,unch),flush=True)
    print('   DISTINCT BOUNDING WALLS (by unchanged-subset signature): %d'%len(sigs),flush=True)
    for s,v in sigs.items():
        print('      cubes %s make this wall   (%d directions hit it)'%(list(s),len(v)),flush=True)
