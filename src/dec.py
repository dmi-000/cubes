import sys; sys.path.insert(0,"/Users/dmi/cube-compounds/src")
import json
from fractions import Fraction as F
from itertools import combinations
import sympy as sp
import plateau_solve as P, wall_keys as W, dimension as D, wall_solve as WS
import wall_census as C, concurrency_walls as CW, map_arcs as M
q=list(W.REC[6]); D.set_field(0); D.QZERO[:]=[q[0]]
pt,nc,walls=P.tight_walls(q); rec=D.count_at(pt,6)
a0,v,lo,hi=M.ARCS['D']; d=[F(0)]*nc
for k in range(3): d[nc-3+k]=v[k]
cont=json.load(open('/Users/dmi/cube-compounds/data/plateau_container_n6.json'))
ns=P.nullspace([[w['grad'][k] for k in range(nc)] for i,w in enumerate(walls) if i in [int(x) for x in cont['flat']]],nc)
u=next(b for b in ns if P.rank([d,b])==2)
keys=[{k:c[k] for k in ('frame','group','sig','c0')} for c in WS.conditions_on(q)]
T=sp.Symbol('t')
def nearest(dirn):
    lo_b,hi_b=F(-1,2),F(1,2)
    for key in keys:                                   # coincidence family
        try: co=W.on_line(key,q[0],pt,dirn)
        except Exception: continue
        if len(co)<2: continue
        Pp=sp.Poly([sp.Rational(x) for x in reversed(co)],T)
        for a,b in C.root_intervals(Pp,-0.5,0.5):
            if a<=0<=b: continue
            if b<0: lo_b=max(lo_b,b)
            elif a>0: hi_b=min(hi_b,a)
    ts=[F(i+1,7)-F(1,3) for i in range(CW.DEG+1+CW.CHECK)]
    snap=[[x[1] for x in CW.planes_at(pt,dirn,q[0],t)] for t in ts]
    lab=[x[0] for x in CW.planes_at(pt,dirn,q[0],F(0))]
    mov=CW.moving_cubes(dirn)
    for c in combinations(range(len(lab)),4):          # concurrency family
        if not any(lab[i][0] in mov for i in c): continue
        vals=[CW.concur_det(*[snap[si][i] for i in c]) for si in range(len(ts))]
        co=CW.newton_poly(ts[:CW.DEG+1],vals[:CW.DEG+1])
        if not all(CW._polyval(co,ts[CW.DEG+1+j])==vals[CW.DEG+1+j] for j in range(CW.CHECK)): continue
        if len(co)<2: continue
        if CW.sturm_count(co,F(-1,2),F(1,2))==0: continue
        Pp=sp.Poly([sp.Rational(x) for x in co],T)
        for a,b in C.root_intervals(Pp,-0.5,0.5):
            if a<=0<=b: continue
            if b<0: lo_b=max(lo_b,b)
            elif a>0: hi_b=min(hi_b,a)
    return lo_b,hi_b
for lam in [F(0),F(1,64),F(1,16)]:
    dd=[d[k]+lam*u[k] for k in range(nc)]
    lb,hb=nearest(dd)
    out={}
    for nm,bnd,other in (('neg',lb,F(0)),('pos',F(0),hb)):
        s=C.simplest_in(bnd,other) if bnd<other else None
        out[nm]=(str(s), None if s is None else D.count_at([pt[k]+s*dd[k] for k in range(nc)],6))
    print('lam=%-6s first cell (%s, %s) -> %s'%(lam,lb,hb,out),flush=True)
print('done')
