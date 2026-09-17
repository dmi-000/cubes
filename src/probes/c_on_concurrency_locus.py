import os
"""c on the CONCURRENCY LOCUS: configurations solved to have a quadruple point.

3% enrichment by shared axis was useless (expected co-occurrence 0.8, observed 0). Here the
sample is 100% enriched: each configuration is a SOLVED rational root of a four-plane
concurrency determinant ([P304]), so it carries a quadruple point by construction.
"""
import sys, os, collections, itertools, random, json
from fractions import Fraction as F
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")); sys.path.insert(0,"/Users/dmi/cube-compounds/src/probes")
import sympy as sp
import dimension as D, concurrency_walls as CW, wall_census as C
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
rng=random.Random(2)
tab=collections.Counter(); hits=[]; tested=0
for trial in range(40):
    base=[(1,0,0,0)]+[tuple(rng.randint(-9,9) for _ in range(4)) for _ in range(3)]
    if any(all(v==0 for v in q) for q in base) or shares_plane(base): continue
    try:
        D.set_field(0); D.QZERO[:]=[base[0]]
        pt=D.point_of(base); nc=len(pt)
    except Exception: continue
    d=[F(rng.choice((-1,0,1))) for _ in range(nc)]
    if not any(d): continue
    try: r=CW.concurrency_walls(base,d,-0.6,0.6,verbose=False)
    except Exception: continue
    roots=sorted({x['rational'] for w in r['walls'] for x in w['roots'] if x['rational']})
    for s in roots[:6]:
        s=F(s)
        if s==0: continue
        qs=D.quats_of([pt[k]+s*d[k] for k in range(nc)], base[0])
        if any(all(v==0 for v in q) for q in qs) or shares_plane(qs): continue
        if max(abs(v) for q in qs for v in q) > 4000: continue
        try:
            p=prof(qs); g=level_graph(qs)
        except Exception: continue
        if max(p) < 4: continue          # root was spurious: no genuine quadruple point
        tested+=1
        hc=max(v['c'] for v in g.values())
        tab[hc]+=1
        if hc>1:
            hits.append({'quats':[list(q) for q in qs],'profile':dict(sorted(p.items())),
                         'c':{str(l):v['c'] for l,v in g.items()}})
            print('  *** c>1 WITH a quadruple point:',dict(sorted(p.items())),
                  {str(l):v['c'] for l,v in g.items()}, flush=True)
    if tested>=60: break
print('configurations ON the concurrency locus (all carry a quadruple point): %d'%tested)
print('  c distribution:',dict(sorted(tab.items())))
print('  c>1 found: %d'%len(hits))
json.dump({'what':'c on solved concurrency-locus configurations','tested':tested,
           'c_distribution':{str(k):v for k,v in tab.items()},'hits':hits},
          open('/Users/dmi/cube-compounds/data/c_on_concurrency_locus.json','w'),indent=1)
