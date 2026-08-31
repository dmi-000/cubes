#!/usr/bin/env python3
"""A low-height representative of the 3921 region, for two-engine verification.

The witness found while mapping 3917's boundary has height 1.7e8 — `cube_regions_n`
refuses it, so only the wide engine has confirmed 3921. A record needs both. 3921
holds on a region, so a cheaper member exists; this searches simple rationals along
the same direction ([METHODS 15]).
"""
import json, subprocess, sys
sys.path.insert(0,'.')
from fractions import Fraction as F
from math import gcd
from qfield import Q
import dimension as D
from epscount import count_eps
from eps_null import walls_and_null
from lll import lll
BASE=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
C10=BASE+[(7,14,1,-5),(4,-3,-4,-4),(24,-24,24,-61),(57,57,56,57),
          (88787,-9061,74275,113786)]
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
def cnt(cfg,exe):
    st=";".join(",".join(map(str,q)) for q in cfg)
    cmd=[exe,'--quats',st] if exe.endswith('_n') else [exe,'--d','0','--quats',st]
    try:
        d=json.loads(subprocess.run(cmd,capture_output=True,text=True).stdout)
        return d['bounded'],d.get('by_depth')
    except Exception: return None,None
pt,walls,null,ncols=walls_and_null(C10)
rec=D.count_at(pt,len(C10))
B=[prim(b) for b in lll([list(prim(v)) for v in null])]
good=[]
for b in B:
    ok=True
    for sgn in (1,-1):
        c=count_eps(pt,[Q(sgn*F(x),0,0) for x in b],0,C10[0])
        if c is None: c=count_eps(pt,[Q(sgn*F(x),0,0) for x in b],0,C10[0],wide=True)
        if c!=rec: ok=False; break
    if ok: good.append(b)
v=good[1]
print('direction 1 (height %d); simple rationals near s=0.06807:'%max(abs(x) for x in v),flush=True)
best=None
for q in range(3,120):
    for p in range(1,q):
        s=F(p,q)
        if not (F(6,100) < s < F(76,1000)): continue
        cfg=cfg_at([pt[i]+s*v[i] for i in range(ncols)],C10[0])
        h=max(abs(x) for qq in cfg for x in qq)
        c,bd=cnt(cfg,'./cube_regions_q2w')
        if c==3921 and (best is None or h<best[0]):
            best=(h,s,cfg,bd)
            print('   s=%-10s height %-12d count %s'%(s,h,c),flush=True)
        break
if best:
    h,s,cfg,bd=best
    print('\nCHEAPEST 3921 found: s=%s  height %d'%(s,h))
    print('   %s'%';'.join(','.join(map(str,q)) for q in cfg))
    for exe in ('./cube_regions_n','./cube_regions_q2w'):
        c,b=cnt(cfg,exe); print('   %-22s -> %s'%(exe,c))
    print('   by_depth %s'%(bd,))
else:
    print('\nno 3921 found at simple rationals in this window')
