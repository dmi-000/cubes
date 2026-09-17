import os
"""c where a quadruple point is GUARANTEED: four cubes sharing a corner.

Solving for concurrency along a ray failed -- 12 of 12 rational roots were rank-degenerate,
determinant zeros with no common point ([P304]'s 264-of-486 phenomenon).  Constructing the
point directly instead: every rotation about the (1,1,1) body diagonal fixes the corner
(1,1,1), so four such cubes put four boundaries through it.  Genuineness is verified per
configuration, never assumed.
"""
import sys, os, collections, itertools, json
from math import gcd
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")); sys.path.insert(0,"/Users/dmi/cube-compounds/src/probes")
from euler3 import rowsT, frames, segments
from cellcomplex import on_bdry_params
from c_level import level_graph, shares_plane
def prof(qs):
    Ms=[rowsT(R) for R in frames(qs)]; n=len(qs); verts=set()
    for i,j in itertools.combinations(range(n),2):
        for p,d,lo,hi in segments(Ms[i],Ms[j]):
            for t in {lo,hi}|{t for k in range(n) if k not in (i,j) for t in on_bdry_params(p,d,lo,hi,Ms[k])}:
                verts.add(tuple(p[z]+t*d[z] for z in range(3)))
    c=collections.Counter()
    for P in verts:
        b=sum(1 for M in Ms if all(abs(sum(M[r][z]*P[z] for z in range(3)))<=1 for r in range(3))
              and any(abs(sum(M[r][z]*P[z] for z in range(3)))==1 for r in range(3)))
        c[b]+=1
    return c
cand=[(w,t,t,t) for w in range(0,8) for t in range(1,8) if gcd(w,t)==1]
tab=collections.Counter(); hits=[]; tested=0; noquad=0
for combo in itertools.combinations(cand,3):
    qs=[(1,0,0,0)]+list(combo)
    if shares_plane(qs): continue
    try:
        p=prof(qs); g=level_graph(qs)
    except Exception: continue
    if max(p)<4: noquad+=1; continue
    tested+=1
    hc=max(v['c'] for v in g.values())
    tab[hc]+=1
    if hc>1:
        hits.append({'quats':[list(q) for q in qs],'profile':dict(sorted(p.items())),
                     'c':{str(l):v['c'] for l,v in g.items()}})
        print('  *** c=%d WITH quadruple point: %s  %s'%(hc,dict(sorted(p.items())),
              ';'.join(','.join(map(str,q)) for q in qs)), flush=True)
    if tested>=150: break
print('configs with a GENUINE quadruple point: %d   (rejected for having none: %d)'%(tested,noquad))
print('  c distribution:',dict(sorted(tab.items())))
print('  c>1 found: %d'%len(hits))
json.dump({'what':'c on four-cubes-sharing-a-corner configurations','tested':tested,
           'c_distribution':{str(k):v for k,v in tab.items()},'hits':hits},
          open('/Users/dmi/cube-compounds/data/c_shared_corner.json','w'),indent=1)
