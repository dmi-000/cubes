import os
"""Can configurations be built with MANY holes?  c >= 3 has never been observed.

A hole is a depth-band encircling a cube (GLOSSARY 8b).  Bands should be easiest to close when
the cubes are NEARLY ALIGNED -- a small rotation leaves ∂A_0 mostly inside its neighbour, with
thin strips of lower depth near the edges, which is the shape a ring wants.  Random sampling
has produced 0 of ~9700 level-instances with c >= 3, so this searches the near-identity family
deliberately instead.
"""
import sys, os, json, collections, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from c_level import level_graph, shares_plane
best=(0,None); hist=collections.Counter(); tried=0
rng=random.Random(4)
def trial(qs):
    global best
    if any(all(v==0 for v in q) for q in qs) or shares_plane(qs): return
    try: g=level_graph(qs)
    except Exception: return
    m=max(v['c'] for v in g.values())
    hist[m]+=1
    if m>best[0]: best=(m,(qs,{l:v['c'] for l,v in g.items()},{l:v['sizes'] for l,v in g.items()}))
# family 1: near-identity, increasing alignment
for N in (3,5,8,12,20,40):
    for _ in range(60):
        qs=[(1,0,0,0)]+[tuple([N]+[rng.randint(-2,2) for _ in range(3)]) for _ in range(3)]
        trial(qs); tried+=1
# family 2: near-identity at n=5 and n=6 (more levels, more chances)
for ncub in (5,6):
    for N in (5,10,20):
        for _ in range(40):
            qs=[(1,0,0,0)]+[tuple([N]+[rng.randint(-2,2) for _ in range(3)]) for _ in range(ncub-1)]
            trial(qs); tried+=1
# family 3: one cube far, the rest tightly clustered
for _ in range(120):
    N=rng.choice((8,15,30))
    qs=[(1,0,0,0)]+[tuple([N]+[rng.randint(-2,2) for _ in range(3)]) for _ in range(2)]+[tuple(rng.randint(-9,9) for _ in range(4))]
    trial(qs); tried+=1
print('configurations tried: %d'%tried)
print('max c per configuration, distribution:',dict(sorted(hist.items())))
print('BEST c found: %d'%best[0])
if best[1]:
    qs,cs,sz=best[1]
    print('  quats:',';'.join(','.join(map(str,q)) for q in qs))
    print('  c per level:',cs)
    print('  component sizes:',sz)
json.dump({'what':'search for c>=3 in near-aligned families','tried':tried,
           'distribution':{str(k):v for k,v in hist.items()},'best_c':best[0],
           'best':{'quats':[list(q) for q in best[1][0]],'c':{str(k):v for k,v in best[1][1].items()},
                   'sizes':{str(k):v for k,v in best[1][2].items()}} if best[1] else None},
          open('/Users/dmi/cube-compounds/data/hole_search.json','w'),indent=1)
