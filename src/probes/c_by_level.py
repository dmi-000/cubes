import os
"""At WHICH levels does c > 1 occur?  And does c > 2 ever occur?"""
import sys, os, collections, random, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from c_level import level_graph, shares_plane
rng=random.Random(101)
bylevel=collections.Counter(); tot=collections.Counter(); cmax=collections.Counter()
inst=[]
for n_cubes in (4,5):
    for _ in range(700):
        qs=[(1,0,0,0)]+[tuple(rng.randint(-20,20) for _ in range(4)) for _ in range(n_cubes-1)]
        if any(all(v==0 for v in q) for q in qs) or shares_plane(qs): continue
        try: g=level_graph(qs)
        except Exception: continue
        for l,v in g.items():
            tot[(n_cubes,l)]+=1
            cmax[v['c']]+=1
            if v['c']>1:
                bylevel[(n_cubes,l)]+=1
                inst.append({'n':n_cubes,'level':l,'c':v['c'],'sizes':v['sizes'],
                             'quats':[list(q) for q in qs]})
print('c distribution over ALL level-instances:',dict(sorted(cmax.items())))
print()
print('%-6s %-6s %-10s %-8s %s'%('n','level','instances','c>1','rate'))
for k in sorted(tot):
    b=bylevel.get(k,0)
    print('%-6d %-6d %-10d %-8d %.2f%%'%(k[0],k[1],tot[k],b,100*b/tot[k]))
print()
print('total c>1 instances: %d   max c seen: %d'%(len(inst), max(cmax)))
json.dump({'c_distribution':{str(k):v for k,v in cmax.items()},
           'by_level':{str(k):v for k,v in bylevel.items()},
           'totals':{str(k):v for k,v in tot.items()},'instances':inst[:40]},
          open('/Users/dmi/cube-compounds/data/c_by_level.json','w'),indent=1)
