import sys, os, random, json, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")); sys.path.insert(0,"/Users/dmi/cube-compounds/src/probes")
from c_level import shares_plane, level_graph
from facet_radial import full_skeleton, facet_centre_lemma
import wall_keys as W
rng=random.Random(5)
odd=even=0; bad=[]; hist=collections.Counter(); wallc=collections.Counter()
cfgs=[[tuple(q) for q in W.REC[n]] for n in (4,5,6)]
for _ in range(500):
    qs=[(1,0,0,0)]+[tuple(rng.randint(-30,30) for _ in range(4)) for _ in range(3)]
    if any(all(v==0 for v in q) for q in qs) or shares_plane(qs): continue
    cfgs.append(qs)
for qs in cfgs:
    try: g=full_skeleton(qs); w=level_graph(qs)
    except Exception: continue
    for l,v in g.items():
        hist[v['c']]+=1
        if v['c']%2==1: odd+=1
        else:
            even+=1; bad.append((qs,l,v['c'],v['sizes']))
    for l,v in w.items(): wallc[v['c']]+=1
print('full-skeleton level-instances: odd c %d | EVEN c %d'%(odd,even))
print('full c distribution :',dict(sorted(hist.items())))
print('wall c distribution :',dict(sorted(wallc.items())))
for b in bad[:5]: print('  EVEN:',';'.join(','.join(map(str,q)) for q in b[0]),'level',b[1],'c',b[2],b[3])
json.dump({'odd':odd,'even':even,'full_c_distribution':{str(k):v for k,v in hist.items()},
           'wall_c_distribution':{str(k):v for k,v in wallc.items()},
           'counterexamples':[[[list(q) for q in b[0]],b[1],b[2],b[3]] for b in bad[:20]]},
          open('/Users/dmi/cube-compounds/data/parity_gate3.json','w'),indent=1)
