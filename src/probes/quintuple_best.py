import os
"""How close to a record can a QUINTUPLE-point configuration get?  n = 5.

Five cubes all rotating about the (1,1,1) body diagonal fix its corner, so all five boundaries
pass through it: b = 5, a quintuple point, guaranteed by construction and verified per case.
The first sweep enumerated every 4-subset of 45 candidate rotations -- ~148 000 engine calls --
and never finished.  Bounded sample instead, with the candidate list kept small and the best
kept.
"""
import sys, os, collections, itertools, json, random
from math import gcd
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")); sys.path.insert(0,"/Users/dmi/cube-compounds/src/probes")
from euler3 import rowsT, frames, segments
from cellcomplex import on_bdry_params
from c_level import engine, shares_plane
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
cand=[(w,t,t,t) for w in range(0,6) for t in range(1,6) if gcd(w,t)==1]
rng=random.Random(5); seen=set(); rows=[]
for _ in range(4000):
    combo=tuple(sorted(rng.sample(cand,4)))
    if combo in seen: continue
    seen.add(combo)
    qs=[(1,0,0,0)]+list(combo)
    if shares_plane(qs): continue
    try: r=engine(qs)
    except Exception: continue
    tot=sum(v for k,v in (r.get('by_depth') or {}).items() if k!='0')
    rows.append((tot,qs))
    if len(rows)>=220: break
rows.sort(key=lambda x:-x[0])
print('n=5 all-on-(1,1,1)-axis: %d configurations counted; record is 393'%len(rows))
out=[]
for tot,qs in rows[:4]:
    p=prof(qs)
    out.append({'count':tot,'quats':[list(q) for q in qs],'profile':dict(sorted(p.items()))})
    print('  count %-5d  max b=%d  profile %s  %s'%(tot,max(p),dict(sorted(p.items())),
          ';'.join(','.join(map(str,q)) for q in qs)), flush=True)
print('  best %d of 393 = %.1f%% of the record'%(rows[0][0],100*rows[0][0]/393))
json.dump({'what':'best n=5 configurations carrying a quintuple point','record':393,
           'counted':len(rows),'best':out},
          open('/Users/dmi/cube-compounds/data/quintuple_best.json','w'),indent=1)
