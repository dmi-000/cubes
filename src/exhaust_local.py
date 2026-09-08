#!/usr/bin/env python3
"""Local maximality of 2787, EXHAUSTED over a stated family — not 18 sampled directions.

`climb.py` reported 2787 locally maximal from 18 directions in a 4-dimensional
preserving subspace. That is sampling, and [METHODS 1](METHODS.md) names it.

**Why the cheap solve does not exist here.** If preserving directions crossed walls,
the count at pt + eps*v would be fixed by the sign vector of v against the tight
walls, giving finitely many chambers and a PROOF from one representative each —
`zaslavsky.py` already counts such chambers. But all 76 tight walls at 2787 vanish
IDENTICALLY on the null space, so every preserving direction has the zero sign vector
and there is no linear chamber structure. The variation is higher-order, which is the
same fact behind P175's finite steps disagreeing with P184's eps limit.

So the available upgrade is EXHAUSTION over a family that is stated rather than
sampled: every primitive integer direction with |coefficient| <= 2 in the preserving
basis, both signs, walked out to its first wall by bisection. That is not a proof of
local maximality; it is a complete search of a named set, and it is reported as such.
"""
import itertools, json, subprocess, sys
sys.path.insert(0,'.')
from fractions import Fraction as F
from math import gcd
import sympy as sp
from qfield import Q
import dimension as D
from epscount import count_eps
from eps_null import walls_and_null
from lll import lll

K=2; M=4096
N9=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1),(7,14,1,-5),
    (4,-3,-4,-4),(168,-168,168,-415),(88787,-9061,74275,113786)]

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

pt,walls,null,ncols=walls_and_null(N9)
rec=D.count_at(pt,len(N9))
B=[prim(b) for b in lll([list(prim(v)) for v in null])]
good=[]
for b in B:
    ok=True
    for sgn in (1,-1):
        c=count_eps(pt,[Q(sgn*F(x),0,0) for x in b],0,N9[0])
        if c is None: c=count_eps(pt,[Q(sgn*F(x),0,0) for x in b],0,N9[0],wide=True)
        if c!=rec: ok=False; break
    if ok: good.append(b)
d=len(good)
print('2787: preserving basis %d vectors, rank %d'%(d,sp.Matrix([list(g) for g in good]).rank()),flush=True)
fam=[]
seen=set()
for co in itertools.product(range(-K,K+1),repeat=d):
    if not any(co): continue
    v=prim([sum(a*g[i] for a,g in zip(co,good)) for i in range(ncols)])
    nv=tuple(-x for x in v)
    if v in seen or nv in seen: continue
    seen.add(v); fam.append(v)
print('FAMILY: all primitive integer directions with |coeff| <= %d, both signs deduped: %d'
      %(K,len(fam)),flush=True)
Dden=max(abs(v) for v in N9[-1]); den=Dden*M
best=(rec,None); done=0; unev=0
for v0 in fam:
    for sgn in (1,-1):
        v=tuple(sgn*x for x in v0)
        lo,hi,c=0,1,None
        while hi<=den*8:
            c=cnt(cfg_at([pt[i]+F(hi,den)*v[i] for i in range(ncols)],N9[0]))
            if c is None: hi*=2; continue
            if c!=rec: break
            lo=hi; hi*=2
        if c is None: unev+=1; continue
        if c==rec: continue
        while hi-lo>1:
            mid=(lo+hi)//2
            cm=cnt(cfg_at([pt[i]+F(mid,den)*v[i] for i in range(ncols)],N9[0]))
            if cm is None: break
            if cm==rec: lo=mid
            else: hi=mid
        c=cnt(cfg_at([pt[i]+F(hi,den)*v[i] for i in range(ncols)],N9[0]))
        if c and c>best[0]:
            best=(c,v); print('   *** crossing to %d (ABOVE %d)'%(c,rec),flush=True)
    done+=1
    if done%25==0: print('   %d/%d directions done, best %d'%(done,len(fam),best[0]),flush=True)
print('\nEXHAUSTED %d directions x 2 signs, %d unevaluated'%(len(fam),unev),flush=True)
print('best count found across any first crossing: %d  (record %d)'%(best[0],rec),flush=True)
print('VERDICT: %s'%('2787 is a LOCAL MAXIMUM over this stated family (not a proof)'
      if best[1] is None else 'HIGHER COUNT FOUND: %d'%best[0]),flush=True)
