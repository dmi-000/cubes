import os
import sys, os, collections, itertools, random, json
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
rng=random.Random(31); tab=collections.Counter(); hits=[]
AX=[(1,1,1),(1,1,0),(2,1,1),(1,0,0),(3,1,2),(1,2,3)]
tried=0
while tried<700:
    tried+=1
    a=rng.choice(AX)
    w1,t1=rng.randint(0,9),rng.randint(1,9)
    w2,t2=rng.randint(0,9),rng.randint(1,9)
    q2=(w1,t1*a[0],t1*a[1],t1*a[2]); q3=(w2,t2*a[0],t2*a[1],t2*a[2])
    if q2==q3: continue
    qs=[(1,0,0,0), tuple(rng.randint(-14,14) for _ in range(4)), q2, q3]
    if any(all(v==0 for v in q) for q in qs) or shares_plane(qs): continue
    try: g=level_graph(qs); p=prof(qs)
    except Exception: continue
    hb=max(p); hc=max(v['c'] for v in g.values())
    tab[(hb>=4, hc>1)]+=1
    if hb>=4 and hc>1:
        hits.append({'quats':[list(q) for q in qs],'profile':dict(sorted(p.items())),
                     'c_by_level':{str(l):v['c'] for l,v in g.items()}})
print('ENRICHED sample: shared-axis pair forced into every configuration')
print('  (has b>=4, has c>1) -> count')
for k in sorted(tab): print('     quad=%-5s c>1=%-5s  %d'%(k[0],k[1],tab[k]))
n=sum(tab.values())
print('  configs %d | with b>=4: %d (%.0f%%) | with c>1: %d'%(n,
   sum(v for k,v in tab.items() if k[0]), 100*sum(v for k,v in tab.items() if k[0])/max(n,1),
   sum(v for k,v in tab.items() if k[1])))
print('  BOTH (c>1 AND a quadruple point): %d'%len(hits))
for h in hits[:4]: print('     ',h['profile'],h['c_by_level'],';'.join(','.join(map(str,q)) for q in h['quats']))
json.dump({'contingency':{str(k):v for k,v in tab.items()},'both':hits},
          open('/Users/dmi/cube-compounds/data/ctuple_enriched.json','w'),indent=1)
