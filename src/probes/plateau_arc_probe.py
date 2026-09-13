import sys, os; sys.path.insert(0, "/Users/dmi/cube-compounds/src")
from fractions import Fraction as F
import json, plateau_solve as P, wall_keys as W, dimension as D, wall_solve as WS, map_arcs as M
q=list(W.REC[6]); D.set_field(0); D.QZERO[:]=[q[0]]
pt,nc,walls=P.tight_walls(q); G=[w['grad'] for w in walls]
rec=D.count_at(pt,6)
keys=[{k:c[k] for k in ('frame','group','sig','c0')} for c in WS.conditions_on(q)]
out={'record':rec,'tight_walls':len(G),'rank':P.rank(G),'arcs':{}}
hold=[]
for name in ('D','A','B','C'):
    a0,v,lo,hi=M.ARCS[name]
    d=[F(0)]*nc
    for k in range(3): d[nc-3+k]=v[k]
    cross=[i for i,g in enumerate(G) if sum(g[k]*d[k] for k in range(nc))!=0]
    r=P.test_dir(q,pt,nc,keys,d,rec)
    out['arcs'][name]={'crosses':len(cross),'crossed_walls':cross,'holds':r['holds'],
                       'probe':{k:(v2 if not isinstance(v2,dict) else v2) for k,v2 in r.items()}}
    print(name,'crosses',len(cross),'holds',r['holds'],flush=True)
    if r['holds']: hold.append((name,d,cross))
un=set()
for _,_,c in hold: un|=set(c)
ind=[]
for _,d,_ in hold:
    if P.rank(ind+[d])>len(ind): ind.append(d)
out['provably_left']=sorted(un); out['n_provably_left']=len(un)
out['independent_holding_directions']=len(ind)
if len(ind)>1:
    mix=[sum(ind[j][k]*F(j+1) for j in range(len(ind))) for k in range(nc)]
    rm=P.test_dir(q,pt,nc,keys,mix,rec)
    out['generic_combination_holds']=rm['holds']; out['generic_combination']=rm
    print('generic combination holds',rm['holds'],flush=True)
json.dump(out,open('/Users/dmi/cube-compounds/data/plateau_arcs_n6.json','w'),indent=1,default=str)
print('done',out['n_provably_left'],'walls left,',len(ind),'independent directions')
