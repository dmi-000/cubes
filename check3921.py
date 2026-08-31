#!/usr/bin/env python3
"""Verify the count 3921 seen while mapping 3917's boundary — a candidate new record."""
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
n=len(C10)
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
def cnt(cfg,exe=None):
    st=";".join(",".join(map(str,q)) for q in cfg)
    m=max(abs(v) for q in cfg for v in q)
    cmd=([exe,'--quats',st] if exe=='./cube_regions_n' else
         ['./cube_regions_q2w','--d','0','--quats',st]) if exe else \
        (['./cube_regions_n','--quats',st] if m<=512 else ['./cube_regions_q2w','--d','0','--quats',st])
    try:
        d=json.loads(subprocess.run(cmd,capture_output=True,text=True).stdout)
        return d['bounded'], d.get('by_depth')
    except Exception: return None,None
pt,walls,null,ncols=walls_and_null(C10)
rec=D.count_at(pt,n)
B=[prim(b) for b in lll([list(prim(v)) for v in null])]
good=[]
for b in B:
    ok=True
    for sgn in (1,-1):
        c=count_eps(pt,[Q(sgn*F(x),0,0) for x in b],0,C10[0])
        if c is None: c=count_eps(pt,[Q(sgn*F(x),0,0) for x in b],0,C10[0],wide=True)
        if c!=rec: ok=False; break
    if ok: good.append(b)
print('preserving basis size %d; scanning each direction outward for counts > %d'%(len(good),rec),flush=True)
den=88787*4096
best=(rec,None,None)
for idx,v in enumerate(good):
    for k in [24754768]+[int(den*x) for x in (0.02,0.04,0.05,0.06,0.065,0.07,0.075,0.08,0.1)]:
        p2=[pt[i]+F(k,den)*v[i] for i in range(ncols)]
        cfg=cfg_at(p2,C10[0]); c,bd=cnt(cfg)
        if c and c>best[0]:
            best=(c,cfg,bd)
            print('   dir %d  k/den=%.5f  count %d  <== ABOVE %d'%(idx,k/den,c,rec),flush=True)
c,cfg,bd=best
if cfg is None:
    print('\nno count above %d reproduced'%rec)
else:
    print('\nCANDIDATE n=10 = %d'%c)
    print('   config: %s'%';'.join(','.join(map(str,q)) for q in cfg))
    print('   heights: %d'%max(abs(v) for q in cfg for v in q))
    for exe in ('./cube_regions_n','./cube_regions_q2w'):
        cc,bb=cnt(cfg,exe); print('   %-22s -> %s  by_depth %s'%(exe,cc,bb))
