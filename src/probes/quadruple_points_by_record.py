import os
import sys, os, collections, itertools, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")); sys.path.insert(0,"/Users/dmi/cube-compounds/src/probes")
from euler3 import rowsT, frames, segments
from cellcomplex import on_bdry_params
import wall_keys as W
from math import comb
def anat(qs):
    Ms=[rowsT(R) for R in frames(qs)]; n=len(qs); verts=set()
    for i,j in itertools.combinations(range(n),2):
        for p,d,lo,hi in segments(Ms[i],Ms[j]):
            cuts={lo,hi}|{t for k in range(n) if k not in (i,j) for t in on_bdry_params(p,d,lo,hi,Ms[k])}
            for t in cuts: verts.add(tuple(p[z]+t*d[z] for z in range(3)))
    prof=collections.Counter()
    for P in verts:
        b=sum(1 for M in Ms if all(abs(sum(M[r][z]*P[z] for z in range(3)))<=1 for r in range(3))
              and any(abs(sum(M[r][z]*P[z] for z in range(3)))==1 for r in range(3)))
        prof[b]+=1
    return prof
out={}
for n in (4,5,6,7,8):
    qs=[tuple(q) for q in W.REC[n]]
    p=anat(qs)
    q4=sum(v for k,v in p.items() if k>=4)
    out[n]={'profile':dict(sorted(p.items())),'quadruple_or_more':q4,
            'triples':p.get(3,0),'cap':32*comb(n,3)}
    print('n=%d  vertices on b boundaries %s | 4-or-more: %d | triples %d | cap %d'%(
        n, dict(sorted(p.items())), q4, p.get(3,0), 32*comb(n,3)), flush=True)
json.dump(out, open('/Users/dmi/cube-compounds/data/quadruple_points.json','w'), indent=1)
