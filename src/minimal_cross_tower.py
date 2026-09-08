#!/usr/bin/env python3
"""The minimal crossable wall-set at EVERY record — closing the neighbourhood
question the full enumeration could not.

Postscript 122 recorded the rational records' neighbourhoods as UNCHARACTERISED:
the face enumeration is 3^27 at 727 and died on memory, and the codimension-1
fallback found 26 of 27 walls entangled so single crossings do not exist.

Both obstacles dissolve at the right question. Single crossings are impossible, so
ask for the SMALLEST crossable subset: C(27,2) = 351 pairs, C(27,3) = 2 925
triples. Polynomial in the wall count, not exponential. At 183 this returned the
answer in 66 solves after 3^12 had run 3 hours without finishing.

For a subset S: a direction crossing EXACTLY S lies in the null space of the walls
NOT in S and is non-orthogonal to every wall IN S. Counts from the infinitesimal
engine; witnesses via normalize_dir (simplest-rational, Postscript 136's fix).
Engine refusals are counted separately and NEVER scored as "no change".
"""
import itertools, json, sys, time
from collections import Counter
from fractions import Fraction as F
import os as _os
HERE=_os.path.dirname(_os.path.abspath(__file__)); sys.path.insert(0,HERE)
import sympy as sp, dimension as D
from epscount import count_eps

BASE=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
R={5:BASE,6:BASE+[(7,14,1,-5)]}
R[7]=R[6]+[(4,-3,-4,-4)]; R[8]=R[7]+[(24,-24,24,-61)]; R[9]=R[8]+[(56,56,55,56)]

def qmul(a,b):
    w1,x1,y1,z1=a; w2,x2,y2,z2=b
    return (w1*w2-x1*x2-y1*y2-z1*z2, w1*x2+x1*w2+y1*z2-z1*y2,
            w1*y2-x1*z2+y1*w2+z1*x2, w1*z2+x1*y2-y1*x2+z1*w2)
def degauge(cfg):
    for g in ((1,0,0,0),(2,1,0,0),(3,1,1,0),(5,1,2,1)):
        out=[qmul(g,q) for q in cfg]
        if all(x[0]!=0 for x in out): return out
    return list(cfg)

def analyse(nn, cap_pairs=200000):
    cfg=degauge(R[nn]); D.set_field(0); D.QZERO[:]=[cfg[0]]
    pt=D.point_of(cfg); n=len(cfg); ncols=3*(n-1)
    base=D.count_at(pt,n)
    vars_=sp.symbols('c0:%d'%ncols); Rs=D.frames(vars_,cfg[0])
    tight,_=D.cached_conditions(Rs,n,vars_,pt,D.quats_of(pt,cfg[0]),cfg[0])
    good=[t for t in tight if not t['degenerate']]
    def _norm(g):
        piv=next((x for x in g if x!=0),None)
        return tuple(str(x/piv) for x in g) if piv is not None else None
    seen,W={},[]
    for t in good:
        k=_norm(t['grad'])
        if k is not None and k not in seen: seen[k]=True; W.append(t['grad'])
    m=len(W); rank=ncols-len(D.nullspace(W,ncols))
    print('n=%d record %d: %d walls, rank %d of %d'%(nn,base,m,rank,ncols),flush=True)
    t0=time.time()
    for k in (2,3):
        subs=list(itertools.combinations(range(m),k))
        if len(subs)>cap_pairs:
            print('   k=%d: %d subsets exceeds the cap, skipped'%(k,len(subs)),flush=True); continue
        found=0; hist=Counter(); uneval=0
        for S in subs:
            rest=[W[t] for t in range(m) if t not in S]
            cross=None
            for v in D.nullspace(rest,ncols):
                if all(sum(W[i][t]*v[t] for t in range(ncols))!=0 for i in S):
                    cross=v; break
            if cross is None: continue
            found+=1
            dv=D.normalize_dir(cross)
            for d in (dv,[-x for x in dv]):
                c=count_eps(pt,d,0,cfg[0])
                if c is None: uneval+=1
                else: hist[c]+=1
        best=max(hist) if hist else None
        print('   k=%d: %5d subsets -> %3d crossable | beyond %s | best %s (DROP %s) | %d uneval | %.0fs'
              %(k,len(subs),found,dict(sorted(hist.items(),reverse=True)) or '{}',
                best,(base-best) if best else '-',uneval,time.time()-t0),flush=True)
        if found and hist:
            return {'n':nn,'count':base,'walls':m,'rank':rank,'k':k,'crossable':found,
                    'hist':{str(a):b for a,b in hist.items()},'best':best,
                    'drop':base-best,'uneval':uneval}
    return {'n':nn,'count':base,'walls':m,'rank':rank,'k':None}

out=[]
for nn in [int(x) for x in (sys.argv[1:] or ['6','7'])]:
    out.append(analyse(nn))
    json.dump(out,open(HERE+'/minimal_cross_tower.json','w'),indent=1)
