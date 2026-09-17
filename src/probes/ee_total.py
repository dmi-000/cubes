import os
"""Is the TOTAL edge-edge count bounded by 6*C(n,2), even though PER PAIR it is not?

Per pair EE reaches 24 (at a 180-degree body-diagonal rotation), refuting EE <= 6 per pair.
But substituting that rotation into the n = 4 record LOWERS the total EE from 36 to 24 and the
region count from 183 to 171 -- exactly the EE difference.  So contacts concentrated on one pair
are lost elsewhere.  This searches for the largest TOTAL EE at n = 4, where 6*C(4,2) = 36.
"""
import sys, os, json, collections, random, itertools
from fractions import Fraction as F
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from euler3 import rowsT, frames, segments
from cellcomplex import on_bdry_params
from c_level import strictly_inside, shares_plane, engine
def ee_and_total(qs):
    Ms=[rowsT(R) for R in frames(qs)]; n=len(qs)
    deg=collections.defaultdict(collections.Counter)
    for i,j in itertools.combinations(range(n),2):
        for p,dd,lo,hi in segments(Ms[i],Ms[j]):
            cuts=sorted({lo,hi}|{t for k in range(n) if k not in (i,j) for t in on_bdry_params(p,dd,lo,hi,Ms[k])})
            for a,b in zip(cuts,cuts[1:]):
                if a>=b: continue
                mid=tuple(p[z]+((a+b)/2)*dd[z] for z in range(3))
                s=sum(1 for k in range(n) if k not in (i,j) and strictly_inside(mid,Ms[k]))
                for t in (a,b): deg[s+1][tuple(p[z]+t*dd[z] for z in range(3))]+=1
    allv=set().union(*[set(x) for x in deg.values()]); r=collections.Counter()
    for P in allv:
        onb=[M for M in Ms if all(abs(sum(M[rr][z]*P[z] for z in range(3)))<=1 for rr in range(3))
             and any(abs(sum(M[rr][z]*P[z] for z in range(3)))==1 for rr in range(3))]
        r[tuple(sorted(sum(1 for rr in range(3) if abs(sum(M[rr][z]*P[z] for z in range(3)))==1) for M in onb))]+=1
    tot=sum(v for k,v in (engine(qs).get('by_depth') or {}).items() if k!='0')
    return r.get((2,2),0), r.get((1,1,1),0), tot
rng=random.Random(11)
# quaternions known to give high per-pair EE, plus small integers
hi=[(0,1,1,1),(1,1,1,1),(0,1,1,0),(1,1,0,0),(0,0,1,1),(1,0,1,1),(2,1,1,1),(1,2,1,1)]
small=[(w,x,y,z) for w in range(0,4) for x in range(0,4) for y in range(0,4) for z in range(0,4)
       if (w,x,y,z)!=(0,0,0,0)]
best=(0,None); bestT=(0,None); seen=set(); tried=0
for _ in range(2500):
    qs=[(1,0,0,0)]+[rng.choice(hi+small) for _ in range(3)]
    k=tuple(sorted(qs))
    if k in seen: continue
    seen.add(k)
    if any(all(v==0 for v in q) for q in qs) or shares_plane(qs): continue
    try: ee,t3,tot=ee_and_total(qs)
    except Exception: continue
    tried+=1
    if ee>best[0]: best=(ee,(qs,t3,tot))
    if tot>bestT[0]: bestT=(tot,(qs,ee,t3))
    if tried>=400: break
print('n=4, configurations tried: %d   (6*C(4,2) = 36)'%tried)
print('MAX total EE: %d   with T3=%d, count=%d'%(best[0],best[1][1],best[1][2]))
print('   quats:',';'.join(','.join(map(str,q)) for q in best[1][0]))
print('best COUNT found: %d  (EE=%d, T3=%d)   record 183 has EE=36, T3=128'%(bestT[0],bestT[1][1],bestT[1][2]))
json.dump({'what':'max total EE at n=4','tried':tried,'max_EE':best[0],
           'max_EE_quats':[list(q) for q in best[1][0]],'best_count':bestT[0]},
          open('/Users/dmi/cube-compounds/data/ee_total.json','w'),indent=1)
