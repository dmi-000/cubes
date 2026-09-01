#!/usr/bin/env python3
"""Do 2787's facets BOUND 3925's region too? A test that can fail.

The claim first written was "2787's four facets embed in 3925's wall set" — nearly
trivial: cubes 0-7 and 9 are identical in both compounds, so a coincidence among
{1,3,6} exists in 3925 by construction. It could not fail.

The sharp version CAN. A wall may exist without BOUNDING: 3925's region could be cut
off nearer by some other wall in every direction, in which case 2787's facets are
interior to it and bound nothing.

TEST. Walk 2787 to each of its facet crossings — a point just OUTSIDE that wall —
then re-insert cube 8 and count the 10-cube compound there.

    count still 3925  ->  the wall does NOT bound 3925's region  (claim FALSIFIED
                          for that facet: crossing it leaves the 10-cube count intact)
    count != 3925     ->  the wall bounds both

Uses 2787's cached wall data, so it does not duplicate the walls_and_null the climb is
computing for 3925 ([METHODS 2] — and the user's point that the climb already has it).
"""
import itertools, json, random, subprocess, sys
sys.path.insert(0,'.')
from fractions import Fraction as F
from math import gcd
from qfield import Q
import dimension as D
from epscount import count_eps
from eps_null import walls_and_null
from lll import lll

C10=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1),(7,14,1,-5),
     (4,-3,-4,-4),(168,-168,168,-415),(6555,6555,6497,6555),(88787,-9061,74275,113786)]
C9=[C10[i] for i in range(10) if i!=8]          # 2787
CUBE8=C10[8]
M=4096; NDIR=40

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

pt,walls,null,ncols=walls_and_null(C9)
n=len(C9); rec9=D.count_at(pt,n)
print('2787 = %d ; 3925 = %d (re-inserting cube 8 = %s)'%(rec9,cnt(C10),CUBE8),flush=True)
B=[prim(b) for b in lll([list(prim(v)) for v in null])]
good=[]
for b in B:
    ok=True
    for sgn in (1,-1):
        c=count_eps(pt,[Q(sgn*F(x),0,0) for x in b],0,C9[0])
        if c is None: c=count_eps(pt,[Q(sgn*F(x),0,0) for x in b],0,C9[0],wide=True)
        if c!=rec9: ok=False; break
    if ok: good.append(b)
base=cfg_at(pt,C9[0])
bsub=tuple(cnt([base[i] for i in range(n) if i!=j]) for j in range(n))
Dden=max(abs(v) for v in C9[-1]); den=Dden*M
rnd=random.Random(31)
dirs=[]
for g in good: dirs += [tuple(g),tuple(-x for x in g)]
while len(dirs)<NDIR:
    co=[rnd.randint(-3,3) for _ in good]
    if any(co): dirs.append(prim([sum(a*g[i] for a,g in zip(co,good)) for i in range(ncols)]))

seen={}
for v in dirs[:NDIR]:
    lo,hi,c=0,1,None
    while hi<=den*64:
        c=cnt(cfg_at([pt[i]+F(hi,den)*v[i] for i in range(ncols)],C9[0]))
        if c is None: hi*=2; continue
        if c!=rec9: break
        lo=hi; hi*=2
    if c is None or c==rec9: continue
    while hi-lo>1:
        mid=(lo+hi)//2
        cm=cnt(cfg_at([pt[i]+F(mid,den)*v[i] for i in range(ncols)],C9[0]))
        if cm is None: break
        if cm==rec9: lo=mid
        else: hi=mid
    p2=[pt[i]+F(hi,den)*v[i] for i in range(ncols)]
    nine=cfg_at(p2,C9[0]); c9=cnt(nine)
    if c9 is None or c9==rec9: continue
    sub=tuple(cnt([nine[i] for i in range(n) if i!=j]) for j in range(n))
    sig=tuple(j for j in range(n) if sub[j]==bsub[j])
    if sig in seen: continue
    ten=list(nine[:8])+[CUBE8]+[nine[8]]      # re-insert cube 8 in its original slot
    c10=cnt(ten)
    seen[sig]=(float(hi)/den,c9,c10)
    verdict=('does NOT bound 3925 — FALSIFIED for this facet' if c10==3925
             else 'bounds BOTH (3925 -> %s)'%c10)
    print('   facet %-14s at %.5g   2787->%d   10-cube %s   %s'
          %(str(list(sig)),float(hi)/den,c9,c10,verdict),flush=True)
print('\n%d facets tested'%len(seen),flush=True)
bad=[s for s,(d,a,b) in seen.items() if b==3925]
print('facets that do NOT bound 3925: %d of %d  ->  %s'
      %(len(bad),len(seen),'prediction FALSIFIED' if bad else 'prediction SURVIVES'),flush=True)
