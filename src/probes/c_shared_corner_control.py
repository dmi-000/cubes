import os
"""CONTROL for the shared-corner test: same family, one cube fewer on the axis.

150 configurations with four cubes on the (1,1,1) axis all gave c = 1, but every one also
shares the AXIS, so the suppression could be the axis rather than the quadruple point.  Here
two cubes sit on the axis and one is generic: the corner then carries THREE boundaries
(identity + the two on-axis), so there is no quadruple point while the shared-axis structure
remains.  If c > 1 appears here at its usual rate, the quadruple point is what suppresses it;
if c = 1 here too, the axis is.
"""
import sys, os, collections, itertools, random, json
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
rng=random.Random(19)
tab=collections.Counter(); hits=[]; tested=0; withquad=0
for a,b in itertools.combinations(cand,2):
    for _ in range(2):
        qs=[(1,0,0,0),a,b,tuple(rng.randint(-12,12) for _ in range(4))]
        if any(all(v==0 for v in q) for q in qs) or shares_plane(qs): continue
        try:
            p=prof(qs); g=level_graph(qs)
        except Exception: continue
        if max(p)>=4: withquad+=1; continue      # keep the control quadruple-free
        tested+=1
        hc=max(v['c'] for v in g.values())
        tab[hc]+=1
        if hc>1:
            hits.append({'quats':[list(q) for q in qs],'profile':dict(sorted(p.items())),
                         'c':{str(l):v['c'] for l,v in g.items()}})
    if tested>=150: break
print('CONTROL: shared axis, NO quadruple point: %d configs (%d discarded for having one)'%(tested,withquad))
print('  c distribution:',dict(sorted(tab.items())))
print('  c>1 found: %d  (%.1f%%)'%(len(hits),100*len(hits)/max(tested,1)))
json.dump({'what':'control - shared axis without a quadruple point','tested':tested,
           'c_distribution':{str(k):v for k,v in tab.items()},'n_c_gt_1':len(hits)},
          open('/Users/dmi/cube-compounds/data/c_shared_corner_control.json','w'),indent=1)
