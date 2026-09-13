import sys; sys.path.insert(0,"/Users/dmi/cube-compounds/src")
import json
from fractions import Fraction as F
from itertools import combinations
import plateau_solve as P, wall_keys as W, dimension as D, concurrency_walls as CW, map_arcs as M
q=list(W.REC[6]); D.set_field(0); D.QZERO[:]=[q[0]]
pt=D.point_of(q); nc=len(pt)
a0,v,lo,hi=M.ARCS['D']; d=[F(0)]*nc
for k in range(3): d[nc-3+k]=v[k]
_,_,walls=P.tight_walls(q)
cont=json.load(open('/Users/dmi/cube-compounds/data/plateau_container_n6.json'))
ns=P.nullspace([walls[i]['grad'] for i in [int(x) for x in cont['flat']]],nc)
u=next(b for b in ns if P.rank([d,b])==2)
z=[F(0)]*nc; P0=CW.planes_at(pt,z,q[0],F(0)); rows0=[x[1] for x in P0]
thru=[c for c in combinations(range(len(P0)),4) if CW.concur_det(*[rows0[i] for i in c])==0]
ts=[F(i+1,7)-F(1,3) for i in range(CW.DEG+1)]
def coeffs(dirn,c,snap):
    return CW.newton_poly(ts,[CW.concur_det(*[snap[si][i] for i in c]) for si in range(len(ts))])
def snapshot(dirn):
    return [[x[1] for x in CW.planes_at(pt,dirn,q[0],t)] for t in ts]
S0=snapshot(d)
lams=[F(1,64),F(-1,64),F(1,16)]
SL={l:snapshot([d[k]+l*u[k] for k in range(nc)]) for l in lams}
def lead(co):
    """(order of vanishing at t=0, sign of the leading coefficient)"""
    cs=list(reversed(co))               # ascending powers
    for i,x in enumerate(cs):
        if x!=0: return i,(1 if x>0 else -1)
    return None,0
flip=[]; degen=0
for c in thru:
    o0,s0=lead(coeffs(d,c,S0))
    g_is_zero = (o0 is not None and o0>=2)
    if g_is_zero: degen+=1
    for l in lams:
        o1,s1=lead(coeffs([d[k]+l*u[k] for k in range(nc)],c,SL[l]))
        if (o0,s0)!=(o1,s1):
            flip.append({'planes':[list(P0[i][0]) for i in c],'lambda':str(l),
                         'at_arcD':[o0,s0],'at_lambda':[o1,s1],'degenerate':g_is_zero})
            break
print('through-record quadruples %d | singular at the record (order>=2) %d'%(len(thru),degen),flush=True)
print('quadruples whose LEADING behaviour differs between arc D and the perturbation: %d'%len(flip),flush=True)
for f in flip[:6]: print('   ',f,flush=True)
json.dump({'through_record':len(thru),'singular':degen,'flips':flip},
          open('/Users/dmi/cube-compounds/data/plateau_leading_n6.json','w'),indent=1)
print('done')
