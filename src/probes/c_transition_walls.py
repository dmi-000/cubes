import os
"""Are there WALLS between c = 1 and c = 2, and which family are they?

[P269] showed c = 2 survives perturbation, so {c = 2} is OPEN and must have a boundary.  This
locates one exactly: from a c = 2 configuration, restrict BOTH wall families to a ray, take all
roots, and evaluate c in every cell between consecutive roots.  A cell boundary where c changes
IS a wall between c = 1 and c = 2, and whatever vanishes there names its family.
"""
import sys, os, json, collections, random
from fractions import Fraction as F
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")); sys.path.insert(0,"/Users/dmi/cube-compounds/src/probes")
import sympy as sp
import dimension as D, wall_keys as W, wall_solve as WS, wall_census as C, concurrency_walls as CW
from c_level import level_graph, shares_plane
from itertools import combinations
T=sp.Symbol('t')
src=json.load(open('/Users/dmi/cube-compounds/data/c_by_level.json'))['instances']
base=[tuple(q) for q in src[0]['quats']]
print('base config c-profile:', {l:v['c'] for l,v in level_graph(base).items()}, flush=True)
D.set_field(0); D.QZERO[:]=[base[0]]
pt=D.point_of(base); nc=len(pt)
rng=random.Random(3)
d=[F(rng.choice((-1,0,1))) for _ in range(nc)]
while not any(d): d=[F(rng.choice((-1,0,1))) for _ in range(nc)]
W_=F(1,6)
items=[]
keys=[{k:c[k] for k in ('frame','group','sig','c0')} for c in WS.conditions_on(base)]
for key in keys:
    try: co=W.on_line(key,base[0],pt,d)
    except Exception: continue
    if len(co)<2: continue
    P=sp.Poly([sp.Rational(x) for x in reversed(co)],T)
    for a,b in C.root_intervals(P,-float(W_),float(W_)):
        items.append((F(a),F(b),('coincidence',key['frame'],tuple(map(tuple,key['group'])))))
ts=[F(i+1,7)-F(1,3) for i in range(CW.DEG+1+CW.CHECK)]
snap=[[x[1] for x in CW.planes_at(pt,d,base[0],t)] for t in ts]
lab=[x[0] for x in CW.planes_at(pt,d,base[0],F(0))]
mov=CW.moving_cubes(d)
for c4 in combinations(range(len(lab)),4):
    if not any(lab[i][0] in mov for i in c4): continue
    vals=[CW.concur_det(*[snap[si][i] for i in c4]) for si in range(len(ts))]
    co=CW.newton_poly(ts[:CW.DEG+1],vals[:CW.DEG+1])
    if not all(CW._polyval(co,ts[CW.DEG+1+j])==vals[CW.DEG+1+j] for j in range(CW.CHECK)): continue
    if len(co)<2 or CW.sturm_count(co,-W_,W_)==0: continue
    P=sp.Poly([sp.Rational(x) for x in co],T)
    for a,b in C.root_intervals(P,-float(W_),float(W_)):
        items.append((F(a),F(b),('concurrency',tuple(lab[i] for i in c4))))
items.sort(key=lambda x:(x[0],x[1]))
cl=[]
for a,b,info in items:
    if cl and a<=cl[-1]['hi']: cl[-1]['hi']=max(cl[-1]['hi'],b); cl[-1]['w'].append(info)
    else: cl.append({'lo':a,'hi':b,'w':[info]})
print('%d crossings on the ray'%len(cl), flush=True)
edges=[-W_]+[x for c in cl for x in (c['lo'],c['hi'])]+[W_]
cs=[]
for i in range(0,len(edges)-1,2):
    a,b=edges[i],edges[i+1]
    s=C.simplest_in(a,b) if a<b else None
    if s is None: cs.append(None); continue
    qs=D.quats_of([pt[k]+s*d[k] for k in range(nc)], base[0])
    try: cs.append(max(v['c'] for v in level_graph(qs).items().__iter__().__next__()[1:]) if False else max(v['c'] for v in level_graph(qs).values()))
    except Exception: cs.append(None)
print('c per cell:',cs, flush=True)
tr=[]
for j,c in enumerate(cl):
    before=cs[j] if j<len(cs) else None; after=cs[j+1] if j+1<len(cs) else None
    if before is not None and after is not None and before!=after:
        fam=collections.Counter(w[0] for w in c['w'])
        tr.append({'bracket':[str(c['lo']),str(c['hi'])],'from':before,'to':after,
                   'families':dict(fam),'n_walls':len(c['w'])})
        print('  c %d -> %d at t in [%s, %s]  families %s  (%d walls at this crossing)'%(
            before,after,str(c['lo'])[:14],str(c['hi'])[:14],dict(fam),len(c['w'])), flush=True)
print('transitions found: %d'%len(tr))
json.dump({'what':'walls between c=1 and c=2','direction':[str(x) for x in d],
           'crossings':len(cl),'c_per_cell':cs,'transitions':tr},
          open('/Users/dmi/cube-compounds/data/c_transition_walls.json','w'),indent=1)
