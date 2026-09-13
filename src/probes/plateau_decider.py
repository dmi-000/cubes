import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json
from fractions import Fraction as F
import plateau_solve as P, dimension as D, concurrency_walls as CW, wall_keys as W
q=list(W.REC[6]); D.set_field(0); D.QZERO[:]=[q[0]]
pt=D.point_of(q); nc=len(pt)
z=[F(0)]*nc; P0=CW.planes_at(pt,z,q[0],F(0)); lab={tuple(x[0]):x[1] for x in P0}
doc=json.load(open('/Users/dmi/cube-compounds/data/plateau_leading_n6.json'))
gen=[]; par=0
for f in doc['flips']:
    rows=[lab[tuple(p)] for p in f['planes']]
    rn=P.rank([r[:3] for r in rows]); ra=P.rank(rows)
    if rn<3: par+=1; continue
    gen.append({'planes':f['planes'],'rank_normals':rn,'rank_aug':ra,
                'concurrent':rn==ra,'lambda':f['lambda'],'at_lambda':f['at_lambda']})
print('flips %d | rank-degenerate (no common point) %d | rank-3 %d'%(len(doc['flips']),par,len(gen)),flush=True)
ok=[g for g in gen if g['concurrent']]
print('GENUINE concurrency walls containing arc D but not the perturbation: %d'%len(ok),flush=True)
for g in ok[:6]: print('   ',g,flush=True)
json.dump({'flips':len(doc['flips']),'rank_degenerate':par,'rank3':len(gen),
           'genuine':len(ok),'examples':ok[:20]},
          open('/Users/dmi/cube-compounds/data/plateau_decider_n6.json','w'),indent=1)
print('done')
