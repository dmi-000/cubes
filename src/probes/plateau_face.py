import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json, time
from fractions import Fraction as F
from itertools import combinations
import plateau_solve as P, wall_keys as W, dimension as D, concurrency_walls as CW, map_arcs as M

n=6
q=list(W.REC[n]); D.set_field(0); D.QZERO[:]=[q[0]]
pt,nc,walls=P.tight_walls(q); Gc=[w['grad'] for w in walls]
a0,v,lo,hi=M.ARCS['D']; d=[F(0)]*nc
for k in range(3): d[nc-3+k]=v[k]

z=[F(0)]*nc
P0=CW.planes_at(pt,z,q[0],F(0))          # planes AT the record
labs=[x[0] for x in P0]; rows0=[x[1] for x in P0]
t0=time.time()
thru=[c for c in combinations(range(len(P0)),4)
      if CW.concur_det(*[rows0[i] for i in c])==0]
print('concurrency quadruples through the record:',len(thru),'(%.0fs)'%(time.time()-t0),flush=True)

# gradient of each such determinant: linear coefficient along each axis, exact
ts=[F(i+1,7)-F(1,3) for i in range(CW.DEG+1)]
snap={}
for k in range(nc):
    e=[F(0)]*nc; e[k]=F(1)
    snap[k]=[ [x[1] for x in CW.planes_at(pt,e,q[0],t)] for t in ts]
print('snapshots built (%.0fs)'%(time.time()-t0),flush=True)

Gq=[]
for c in thru:
    g=[]
    for k in range(nc):
        vals=[CW.concur_det(*[snap[k][si][i] for i in c]) for si in range(len(ts))]
        co=CW.newton_poly(ts,vals)
        g.append(co[-2] if len(co)>=2 else F(0))    # coefficient of t
    if any(g): Gq.append(g)
print('concurrency gradients:',len(Gq),'(%.0fs)'%(time.time()-t0),flush=True)

def face(G):
    zero=[g for g in G if sum(g[k]*d[k] for k in range(nc))==0]
    nonz=len(G)-len(zero)
    return zero, nonz

zc,nzc=face(Gc); zq,nzq=face(Gq)
rc=P.rank(zc); rb=P.rank(zc+zq)
print()
print('coincidence walls through record: %d | vanish on arc D: %d | crossed: %d | rank %d -> face dim %d'
      %(len(Gc),len(zc),nzc,rc,nc-rc),flush=True)
print('concurrency walls through record: %d | vanish on arc D: %d | crossed: %d'
      %(len(Gq),len(zq),nzq),flush=True)
print('BOTH families: rank %d -> face containing arc D has dimension %d'%(rb,nc-rb),flush=True)
json.dump({'n':n,'ambient':nc,'coincidence_walls':len(Gc),'concurrency_walls_through_record':len(Gq),
  'coincidence_vanishing_on_arcD':len(zc),'coincidence_crossed':nzc,
  'concurrency_vanishing_on_arcD':len(zq),'concurrency_crossed':nzq,
  'rank_coincidence_face':rc,'dim_coincidence_face':nc-rc,
  'rank_both':rb,'plateau_face_dimension':nc-rb},
  open('/Users/dmi/cube-compounds/data/plateau_face_n6.json','w'),indent=1)
print('done')
