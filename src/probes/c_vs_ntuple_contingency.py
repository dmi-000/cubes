import os
import sys, os, collections, itertools, random, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")); sys.path.insert(0,"/Users/dmi/cube-compounds/src/probes")
from euler3 import rowsT, frames, segments
from cellcomplex import on_bdry_params
from c_level import level_graph, shares_plane
def maxb(qs):
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
rng=random.Random(23); tab=collections.Counter(); ex=[]
for _ in range(900):
    qs=[(1,0,0,0)]+[tuple(rng.randint(-22,22) for _ in range(4)) for _ in range(3)]
    if any(all(v==0 for v in q) for q in qs) or shares_plane(qs): continue
    try:
        g=level_graph(qs); prof=maxb(qs)
    except Exception: continue
    hi_c = max(v['c'] for v in g.values())
    has_q = max(prof) >= 4
    tab[(has_q, hi_c>1)] += 1
    if hi_c>1: ex.append({'quats':[list(q) for q in qs],'max_c':hi_c,'profile':dict(sorted(prof.items()))})
print('contingency (has quadruple+ point, has c>1) -> count')
for k in sorted(tab): print('   quad=%-5s  c>1=%-5s  %d'%(k[0],k[1],tab[k]))
n=sum(tab.values())
print('configs %d | with quad+ %d | with c>1 %d'%(n, sum(v for k,v in tab.items() if k[0]), sum(v for k,v in tab.items() if k[1])))
print()
print('every c>1 instance, max-b profile:')
for e in ex[:8]: print('   max_c=%d  profile %s'%(e['max_c'],e['profile']))
json.dump({'contingency':{str(k):v for k,v in tab.items()},'c_gt_1_instances':ex},
          open('/Users/dmi/cube-compounds/data/ctuple_contingency.json','w'),indent=1)
