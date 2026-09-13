import sys; sys.path.insert(0,"/Users/dmi/cube-compounds/src")
import json
from fractions import Fraction as F
from itertools import combinations
import plateau_solve as P, wall_keys as W, dimension as D, concurrency_walls as CW, map_arcs as M
q=list(W.REC[6]); D.set_field(0); D.QZERO[:]=[q[0]]
pt,nc,walls=P.tight_walls(q); Gc=[w['grad'] for w in walls]
a0,v,lo,hi=M.ARCS['D']; d=[F(0)]*nc
for k in range(3): d[nc-3+k]=v[k]
cont=json.load(open('/Users/dmi/cube-compounds/data/plateau_container_n6.json'))
F0=[int(x) for x in cont['flat']]
ns=P.nullspace([Gc[i] for i in F0],nc)
u=None
for b in ns:
    if P.rank([d,b])==2: u=b; break
# concurrency gradients through the record
z=[F(0)]*nc; P0=CW.planes_at(pt,z,q[0],F(0)); rows0=[x[1] for x in P0]
thru=[c for c in combinations(range(len(P0)),4) if CW.concur_det(*[rows0[i] for i in c])==0]
ts=[F(i+1,7)-F(1,3) for i in range(CW.DEG+1)]
snap={k:[[x[1] for x in CW.planes_at(pt,[F(1) if j==k else F(0) for j in range(nc)],q[0],t)] for t in ts] for k in range(nc)}
Gq=[]
for c in thru:
    g=[]
    for k in range(nc):
        co=CW.newton_poly(ts,[CW.concur_det(*[snap[k][si][i] for i in c]) for si in range(len(ts))])
        g.append(co[-2] if len(co)>=2 else F(0))
    if any(g): Gq.append(g)
crit=[]
for nm,G in (('coincidence',Gc),('concurrency',Gq)):
    for g in G:
        a=sum(g[k]*d[k] for k in range(nc)); b=sum(g[k]*u[k] for k in range(nc))
        if a!=0 and b!=0:
            crit.append((abs(F(-a,1)/b), nm))
crit.sort()
print('walls crossed by arc D that the perturbation can reach:',len(crit),flush=True)
print('smallest |lambda| at which the face is LEFT:',crit[0][0],float(crit[0][0]),crit[0][1],flush=True)
print('next few:',[(str(x[0]),x[1]) for x in crit[1:5]],flush=True)
json.dump({'n_critical':len(crit),'lambda_min':str(crit[0][0]),'lambda_min_float':float(crit[0][0]),
           'family':crit[0][1],'next':[[str(x[0]),x[1]] for x in crit[1:8]]},
          open('/Users/dmi/cube-compounds/data/plateau_face_extent_n6.json','w'),indent=1)
print('done')
