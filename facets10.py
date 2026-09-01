#!/usr/bin/env python3
"""FACETS of a record region, and its VERTICES — the finite object, not sampled directions.

User's observation: the region is a cell, so every direction's first crossing lands on
some FACET. Facets are finite; directions are a continuum. Enumerating facets is the
finite question, and probing near VERTICES reaches cells that no interior direction's
first crossing can — cells across two walls at once.

This supersedes the direction-sampling in `climb.py` and `exhaust_local.py`.

  1. walk many directions, recording each first crossing's (n-1)-subset SIGNATURE
     (METHODS 22) and distance -> the facet list, with a SATURATION curve so the
     enumeration reports its own completeness rather than asserting it;
  2. for each pair of facets found, aim at their intersection — scale two directions so
     both walls sit at t = 1, add them, and step just past — reaching the VERTEX
     neighbourhood and the cells that meet there.

Distances are bisected, never stepped: a coarse step lands several walls out ([P198]).

CAVEAT on completeness. "Every direction exits through a facet" holds if the region is
STAR-SHAPED about the record. A cell of a HYPERPLANE arrangement is convex and this is
automatic, but these boundaries are quadrics, so the region is a cell of a semialgebraic
arrangement and convexity is not guaranteed. A direction could in principle leave and
re-enter, in which case its first crossing is still a facet but the facet list built
this way could miss some. The saturation curve is evidence about that, not proof.
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

M=4096; NDIR=64; REACH=64
N9=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1),(7,14,1,-5),(4,-3,-4,-4),(168,-168,168,-415),(6555,6555,6497,6555),(88787,-9061,74275,113786)]


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
n=len(N9); rec=D.count_at(pt,n)
B=[prim(b) for b in lll([list(prim(v)) for v in null])]
good=[]
for b in B:
    ok=True
    for sgn in (1,-1):
        c=count_eps(pt,[Q(sgn*F(x),0,0) for x in b],0,N9[0])
        if c is None: c=count_eps(pt,[Q(sgn*F(x),0,0) for x in b],0,N9[0],wide=True)
        if c!=rec: ok=False; break
    if ok: good.append(b)
base=cfg_at(pt,N9[0])
bsub=tuple(cnt([base[i] for i in range(n) if i!=j]) for j in range(n))
Dden=max(abs(v) for v in N9[-1]); den=Dden*M

def cross(v):
    """(distance as Fraction, count outside, signature) at the first crossing, or None"""
    lo,hi,c=0,1,None
    while hi<=den*REACH:
        c=cnt(cfg_at([pt[i]+F(hi,den)*v[i] for i in range(ncols)],N9[0]))
        if c is None: hi*=2; continue
        if c!=rec: break
        lo=hi; hi*=2
    if c is None or c==rec: return None
    while hi-lo>1:
        mid=(lo+hi)//2
        cm=cnt(cfg_at([pt[i]+F(mid,den)*v[i] for i in range(ncols)],N9[0]))
        if cm is None: break
        if cm==rec: lo=mid
        else: hi=mid
    p2=[pt[i]+F(hi,den)*v[i] for i in range(ncols)]
    full=cfg_at(p2,N9[0]); c=cnt(full)
    if c is None or c==rec: return None
    sub=tuple(cnt([full[i] for i in range(n) if i!=j]) for j in range(n))
    return F(hi,den), c, tuple(j for j in range(n) if sub[j]==bsub[j])

rnd=random.Random(31)
dirs=[]
for g in good: dirs += [tuple(g),tuple(-x for x in g)]
while len(dirs)<NDIR:
    co=[rnd.randint(-3,3) for _ in good]
    if any(co): dirs.append(prim([sum(a*g[i] for a,g in zip(co,good)) for i in range(ncols)]))
facets={}; curve=[]
print('FACET ENUMERATION (saturation curve: new facets vs directions walked)',flush=True)
for i,v in enumerate(dirs[:NDIR],1):
    r=cross(v)
    if r:
        d,c,sig=r
        if sig not in facets: facets[sig]=(d,c,v)
    curve.append(len(facets))
    if i%8==0: print('   %3d directions -> %d distinct facets'%(i,len(facets)),flush=True)
print('\n%d FACETS found:'%len(facets),flush=True)
for sig,(d,c,v) in sorted(facets.items(),key=lambda kv:kv[1][0]):
    print('   cubes %-14s at %.5g   count outside %d'%(str(list(sig)),float(d),c),flush=True)
print('   saturation tail: %s'%curve[-16:],flush=True)

print('\nVERTEX PROBES (aim where two facets meet; both walls crossed at once):',flush=True)
best=(rec,None)
items=list(facets.items())
for (s1,(d1,c1,v1)),(s2,(d2,c2,v2)) in itertools.combinations(items,2):
    # scale each direction so ITS wall sits at t = 1, then add: the sum aims at the
    # corner where both walls are met together.
    w=prim([v1[i]/d1+v2[i]/d2 for i in range(ncols)])
    r=cross(w)
    if r:
        d,c,sig=r
        tag='NEW facet' if sig not in facets else 'facet %s'%(list(sig),)
        print('   %s + %s -> %.5g count %d  (%s)'%(list(s1),list(s2),float(d),c,tag),flush=True)
        if c>best[0]: best=(c,w); print('      *** ABOVE the record: %d'%c,flush=True)
print('\nbest over all vertex probes: %d (record %d)'%(best[0],rec),flush=True)
