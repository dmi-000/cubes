#!/usr/bin/env python3
"""SUPERSEDED 2026-08-31 by climb.py, which now emits this census per iteration.

Kept only because its output is cited in the ledger. The walk it performs is the same
walk the climb was already doing, so running it separately duplicated the expensive
part for no new information.

Boundary census of a LOCAL MAXIMUM: every wall, named, measured, and counted across.

Run on a configuration `climb.py` has certified locally maximal (no boundary crossing
raises the count). For each direction in the eps-verified preserving subspace, both
signs, bisect to the first crossing and record:

    distance to the wall, the count just outside, and the (n-1)-subset SIGNATURE,
    which names the cubes essential to that wall's coincidence (METHODS 22 —
    derivable as essential=>unchanged, HEURISTIC in the converse actually used).

Fine step plus bisection is not optional: at 1895 and 2785 a step of 1/D left the
region on the first move, so a coarse walk reports whatever lies several walls out
([P198]).
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

M=4096; NDIR=20

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
    for exe in (['./cube_regions_n','--quats',st] if m<=200000 else [],
                ['./cube_regions_q2w','--d','0','--quats',st]):
        if not exe: continue
        try: return json.loads(subprocess.run(exe,capture_output=True,text=True).stdout)['bounded']
        except Exception: pass
    return None

def census(cubes,label):
    n=len(cubes)
    pt,walls,null,ncols=walls_and_null(cubes)
    rec=D.count_at(pt,n)
    print('\n%s  record %d  deficit %d'%(label,rec,len(null)),flush=True)
    B=[prim(b) for b in lll([list(prim(v)) for v in null])]
    good=[]
    for b in B:
        ok=True
        for sgn in (1,-1):
            c=count_eps(pt,[Q(sgn*F(x),0,0) for x in b],0,cubes[0])
            if c is None: c=count_eps(pt,[Q(sgn*F(x),0,0) for x in b],0,cubes[0],wide=True)
            if c!=rec: ok=False; break
        if ok: good.append(b)
    print('   preserving rank %d  (deficit-1 = %d)'
          %(sp.Matrix([list(g) for g in good]).rank(),len(null)-1),flush=True)
    base=cfg_at(pt,cubes[0])
    bsub=tuple(cnt([base[i] for i in range(n) if i!=j]) for j in range(n))
    Dden=max(abs(v) for v in cubes[-1]) or 1
    den=Dden*M
    rnd=random.Random(23)
    dirs=[tuple(g) for g in good]
    while len(dirs)<NDIR:
        co=[rnd.randint(-2,2) for _ in good]
        if any(co): dirs.append(prim([sum(a*g[i] for a,g in zip(co,good)) for i in range(ncols)]))
    sigs={}
    for v0 in dirs[:NDIR]:
        for sgn in (1,-1):
            v=tuple(sgn*x for x in v0)
            lo,hi,c=0,1,None
            while hi<=den*8:
                c=cnt(cfg_at([pt[i]+F(hi,den)*v[i] for i in range(ncols)],cubes[0]))
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
            p2=[pt[i]+F(hi,den)*v[i] for i in range(ncols)]
            full=cfg_at(p2,cubes[0]); c=cnt(full)
            if c is None or c==rec: continue
            sub=tuple(cnt([full[i] for i in range(n) if i!=j]) for j in range(n))
            unch=tuple(j for j in range(n) if sub[j]==bsub[j])
            sigs.setdefault(unch,[]).append((float(hi)/den,c))
    print('   %d DISTINCT BOUNDING WALLS'%len(sigs),flush=True)
    for s,v in sorted(sigs.items(),key=lambda kv:min(x[0] for x in kv[1])):
        ds=[x[0] for x in v]; cs=sorted({x[1] for x in v})
        print('      cubes %-16s distance %.3g..%.3g   count outside %s   (%d hits)'
              %(str(list(s)),min(ds),max(ds),cs,len(v)),flush=True)
    alld=[x[0] for v in sigs.values() for x in v]
    if alld:
        print('   anisotropy: nearest wall %.3g, farthest %.3g, ratio %.0fx'
              %(min(alld),max(alld),max(alld)/min(alld)),flush=True)

N9=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1),(7,14,1,-5),
    (4,-3,-4,-4),(168,-168,168,-415),(88787,-9061,74275,113786)]
census(N9,'n=9 2787 (LOCAL MAXIMUM per climb.py)')
