#!/usr/bin/env python3
"""The 4-CYCLE sharing graph -- the OTHER SC2 = 8 family, and a new point on the frontier. [P353]

[P350] built the paw; there are exactly TWO connected 4-edge graphs on four vertices, and the
4-cycle was never built. Here it is: cube0 = I shares diagonal a with cube1 = Rot(a,alpha) and b
with cube3 = Rot(b,beta) -- a rotation about a diagonal keeps that diagonal -- and cube2 is the
tetrahedron completing a diagonal of cube1 and one of cube3. Everything is RATIONAL using
e-representatives: |e|^2 = 3, <e_i,e_j> = -1, normals (e_i+e_j)/2, completion (-(u+v) +- u x v)/2.

RESULT: 608 non-degenerate C4 configurations, all with SC2 = 8. Best objective 162, with
**two-body = 52 -- the first value above the record's 48 at B = 128** -- but Q4 = 18.

TWO TRAPS ON THE WAY, both already in FAILURE_MODES.
  * `q = (1,1,1,1)` is a 120-degree rotation about a body diagonal, which is a CUBE SYMMETRY, so
    cube1 IS cube0. Unfiltered, this polluted the first run and no configuration reached SC2 = 8.
  * Face normals are the COLUMNS of `mat(q)`; `apply(M,e) = M.e` correctly ROTATES a diagonal,
    but the normal matrix needs the TRANSPOSE. Untransposed, one of the four shared corners
    reported signature `(3,)` instead of `(3,3)` -- FIFTH occurrence of the rows/columns
    confusion in this session ([FAILURE_MODES 38]). The tell was the same as always: a count the
    construction guarantees (SC2 = 8) coming back wrong (6).
"""
import sys, itertools, collections
from math import gcd
from fractions import Fraction as F
sys.path.insert(0,'src'); sys.path.insert(0,'src/probes')
s=open('/private/tmp/claude-502/-Users-dmi-cube-compounds/43a2fe45-06f5-4be7-aa71-da540c168dea/scratchpad/c4b.py').read()
exec(s[:s.index('RA=list(')])
def key(e):
    for t in e:
        if t!=0:
            if t<0: e=tuple(-x for x in e)
            break
    return e
def NORM(M): return [tuple(F(M[r][c]) for r in range(3)) for c in range(3)]
RA=list(dict.fromkeys(prim((m,k,k,k)) for m in range(0,8) for k in range(-7,8) if (m,k)!=(0,0)))
RB=list(dict.fromkeys(prim((m,k,k,-k)) for m in range(0,8) for k in range(-7,8) if (m,k)!=(0,0)))
N0=[(F(1),F(0),F(0)),(F(0),F(1),F(0)),(F(0),F(0),F(1))]
S0={key(e) for e in E0}
best=(-99,None); tried=0; scd=collections.Counter(); objd=collections.Counter()
for q1 in RA:
    M1=mat(q1); E1=[apply(M1,e) for e in E0]; S1={key(e) for e in E1}
    if S1==S0: continue
    for q3 in RB:
        M3=mat(q3); E3=[apply(M3,e) for e in E0]; S3={key(e) for e in E3}
        if S3==S0 or S3==S1: continue
        for u in sgn_set(E1):
            for v in sgn_set(E3):
                if dot(u,v)!=-1: continue
                t=tet2(u,v)
                if t is None: continue
                S2={key(e) for e in t}
                if S2 in (S0,S1,S3): continue
                sets=[S0,S1,S2,S3]
                cnt=collections.Counter()
                for st in sets:
                    for e in st: cnt[e]+=1
                if any(c>=3 for c in cnt.values()): continue
                sh=[(i,j) for i,j in itertools.combinations(range(4),2) if sets[i]&sets[j]]
                if len(sh)!=4: continue
                tried+=1
                CUB=[N0,NORM(M1),normals(t),NORM(M3)]
                try: sig=census(CUB)
                except Exception: continue
                EE=sig.get((2,2),0); SC=sig.get((3,3),0); T3=sig.get((1,1,1),0)
                Qg=sig.get((1,1,1,1),0); Q4=sum(x for k2,x in sig.items() if len(k2)==4)
                scd[SC]+=1
                obj=EE+2*SC+T3+4*Qg-Q4
                objd[obj]+=1
                if obj>best[0]: best=(obj,EE,SC,T3,Q4,EE+2*SC,T3+4*Qg,sorted(sh),q1,q3)
print('non-degenerate 4-sharing (C4) configurations: %d'%tried)
print('SC2 distribution:',dict(sorted(scd.items())))
print('objective distribution (top):',dict(sorted(objd.items(),reverse=True)[:6]))
if best[1] is not None:
    obj,EE,SC,T3,Q4,tb,Bv,sh,q1,q3=best
    print('BEST objective %d   EE %d  SC2 %d  T3 %d  Q4 %d  two-body %d  B %d'%(obj,EE,SC,T3,Q4,tb,Bv))
    print('   graph %s  rot a %s  rot b %s'%(sh,str(q1),str(q3)))
print('   record 176 (SC2 6, EE 36);  paw 168 (SC2 8, EE 24)')
