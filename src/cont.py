import sys; sys.path.insert(0,"/Users/dmi/cube-compounds/src")
import json
from fractions import Fraction as F
import plateau_solve as P, wall_keys as W, dimension as D, wall_solve as WS
q=list(W.REC[6]); D.set_field(0); D.QZERO[:]=[q[0]]
pt,nc,walls=P.tight_walls(q); G=[w['grad'] for w in walls]
rec=D.count_at(pt,6)
crossed=set(json.load(open('/Users/dmi/cube-compounds/data/plateau_arcs_n6.json'))['arcs']['D']['crossed_walls'])
S=[i for i in range(len(G)) if i not in crossed]
F0=P.closure(G,S,nc)
rS=P.rank([G[i] for i in S]); rF=P.rank([G[i] for i in F0])
print('not-crossed walls',len(S),'rank',rS,'| closure',len(F0),'rank',rF,'| stratum dim',nc-rF, flush=True)
ns=P.nullspace([G[i] for i in F0],nc)
print('null basis',len(ns),flush=True)
keys=[{k:c[k] for k in ('frame','group','sig','c0')} for c in WS.conditions_on(q)]
res=[]
for j,v in enumerate(ns):
    r=P.test_dir(q,pt,nc,keys,v,rec)
    res.append({'dir':j,'holds':r['holds'],'counts':{k:x['count'] for k,x in r.items() if isinstance(x,dict)}})
    print('basis dir',j,'holds',r['holds'],res[-1]['counts'], flush=True)
if len(ns)>1:
    mix=[sum(ns[j][k]*F(j+1) for j in range(len(ns))) for k in range(nc)]
    rm=P.test_dir(q,pt,nc,keys,mix,rec)
    print('generic point of the stratum holds',rm['holds'],{k:x['count'] for k,x in rm.items() if isinstance(x,dict)}, flush=True)
    res.append({'generic':True,'holds':rm['holds']})
json.dump({'not_crossed':len(S),'rank_not_crossed':rS,'flat':sorted(F0),'rank_flat':rF,
           'stratum_dimension':nc-rF,'probes':res},
          open('/Users/dmi/cube-compounds/data/plateau_container_n6.json','w'),indent=1,default=str)
print('done')
