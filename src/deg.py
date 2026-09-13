import sys; sys.path.insert(0,"/Users/dmi/cube-compounds/src")
import json
from fractions import Fraction as F
from itertools import combinations
import plateau_solve as P, wall_keys as W, dimension as D, concurrency_walls as CW, map_arcs as M, wall_solve as WS
q=list(W.REC[6]); D.set_field(0); D.QZERO[:]=[q[0]]
pt=D.point_of(q); nc=len(pt)
a0,v,lo,hi=M.ARCS['D']; d=[F(0)]*nc
for k in range(3): d[nc-3+k]=v[k]
_,_,walls=P.tight_walls(q)
cont=json.load(open('/Users/dmi/cube-compounds/data/plateau_container_n6.json'))
ns=P.nullspace([walls[i]['grad'] for i in [int(x) for x in cont['flat']]],nc)
u=next(b for b in ns if P.rank([d,b])==2)

# coincidence conditions with a VANISHING gradient at the record
deg_coin=0; tot_tight=0
for c in WS.conditions_on(q):
    if not c['tight']: continue
    tot_tight+=1
    key={k:c[k] for k in ('frame','group','sig','c0')}
    g=[]
    for k in range(nc):
        e=[F(0)]*nc; e[k]=F(1)
        try: co=W.on_line(key,q[0],pt,e)
        except Exception: g=None; break
        g.append(F(co[1]) if len(co)>1 else F(0))
    if g is not None and not any(g): deg_coin+=1
print('tight coincidence conditions %d | with VANISHING gradient %d'%(tot_tight,deg_coin),flush=True)

# a degenerate concurrency wall that CONTAINS arc D but not the perturbation
z=[F(0)]*nc; P0=CW.planes_at(pt,z,q[0],F(0)); rows0=[x[1] for x in P0]
thru=[c for c in combinations(range(len(P0)),4) if CW.concur_det(*[rows0[i] for i in c])==0]
ts=[F(i+1,7)-F(1,3) for i in range(CW.DEG+1)]
def poly_on(dirn,c):
    snap=[[x[1] for x in CW.planes_at(pt,dirn,q[0],t)] for t in ts]
    return CW.newton_poly(ts,[CW.concur_det(*[snap[si][i] for i in c]) for si in range(len(ts))])
found=[]
dd=[d[k]+F(1,64)*u[k] for k in range(nc)]
for c in thru:
    c0=poly_on(d,c)
    if len(c0)==1 and c0[0]==0:                 # identically zero along arc D
        c1=poly_on(dd,c)
        if not(len(c1)==1 and c1[0]==0):
            found.append((c,[str(x) for x in c1]))
            if len(found)>=3: break
print('concurrency walls CONTAINING arc D but not the perturbed ray:',len(found),flush=True)
for c,p in found: print('   planes',[list(P0[i][0]) for i in c],'| poly off-arc',p,flush=True)
json.dump({'tight_coincidence':tot_tight,'coincidence_vanishing_gradient':deg_coin,
           'concurrency_through_record':len(thru),
           'containing_arcD_not_perturbation':len(found),
           'examples':[[[list(P0[i][0]) for i in c],p] for c,p in found]},
          open('/Users/dmi/cube-compounds/data/plateau_second_order_n6.json','w'),indent=1)
print('done')
