import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json
from fractions import Fraction as F
import plateau_solve as P, wall_keys as W, dimension as D, wall_solve as WS, map_arcs as M
q=list(W.REC[6]); D.set_field(0); D.QZERO[:]=[q[0]]
pt,nc,walls=P.tight_walls(q); G=[w['grad'] for w in walls]
rec=D.count_at(pt,6)
keys=[{k:c[k] for k in ('frame','group','sig','c0')} for c in WS.conditions_on(q)]
cont=json.load(open('/Users/dmi/cube-compounds/data/plateau_container_n6.json'))
F0=[int(x) for x in cont['flat']]
ns=P.nullspace([G[i] for i in F0],nc)
a0,v,lo,hi=M.ARCS['D']
d=[F(0)]*nc
for k in range(3): d[nc-3+k]=v[k]
# second stratum direction independent of d
u=None
for b in ns:
    if P.rank([d,b])==2: u=b; break
res=[]
for lam in [F(0),F(1,64),F(-1,64),F(1,16),F(-1,16),F(1,4),F(-1,4),F(1),F(-1)]:
    dd=[d[k]+lam*u[k] for k in range(nc)]
    if not any(dd): continue
    r=P.test_dir(q,pt,nc,keys,dd,rec)
    cross=sum(1 for g in G if sum(g[k]*dd[k] for k in range(nc))!=0)
    res.append({'lambda':str(lam),'holds':r['holds'],'crosses':cross,
                'counts':{k:x['count'] for k,x in r.items() if isinstance(x,dict)}})
    print('lam=%-7s crosses %2d holds %-5s %s'%(lam,cross,r['holds'],res[-1]['counts']),flush=True)
json.dump({'what':'is the plateau 2-dimensional: arc D perturbed inside its own stratum',
           'stratum_dimension':cont['stratum_dimension'],'probes':res},
          open('/Users/dmi/cube-compounds/data/plateau_sector_n6.json','w'),indent=1)
print('done')
