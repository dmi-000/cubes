import os
"""Does the RECONNECTION observation generalise?  Test dV = dE = 0 at every c-transition.

[P320] addendum found one c-transition where V and E were identical either side and only F
moved.  Since c = V - E + F - 1 that is equivalent to dV = dE = 0, which is what this checks
across many instances and rays: sample c coarsely, narrow to an interval where it changes,
solve BOTH wall families inside it, and compare the two adjacent cells exactly.
"""
import sys, os, json, collections, random
from fractions import Fraction as F
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")); sys.path.insert(0,"/Users/dmi/cube-compounds/src/probes")
import sympy as sp
import dimension as D, wall_keys as W, wall_solve as WS, wall_census as C, concurrency_walls as CW
from c_level import level_graph, engine
from itertools import combinations
T=sp.Symbol('t')
def cvec(pt,d,nc,q0,s):
    """(V, E, F, c) per level, with NO engine call and NO height cap.

    The engine has a component budget, and stepping to an exact cell point clears denominators
    past it -- so asking it for F rejected every cell and the test returned 0 transitions twice.
    `level_graph` is pure Python and has no such limit, and F follows from the verified identity
    F = E - V + c + 1, so the engine was never needed here.
    """
    qs=D.quats_of([pt[k]+s*d[k] for k in range(nc)], q0)
    try: g=level_graph(qs)
    except Exception: return None
    return {l:(v['V'],v['E'],v['E']-v['V']+v['c']+1,v['c']) for l,v in g.items()}
def roots_in(pt,d,nc,q0,base,lo,hi):
    out=[]
    keys=[{k:c[k] for k in ('frame','group','sig','c0')} for c in WS.conditions_on(base)]
    for key in keys:
        try: co=W.on_line(key,q0,pt,d)
        except Exception: continue
        if len(co)<2: continue
        P=sp.Poly([sp.Rational(x) for x in reversed(co)],T)
        out+= [(F(a),F(b),'coincidence') for a,b in C.root_intervals(P,float(lo),float(hi))]
    ts=[F(i+1,7)-F(1,3) for i in range(CW.DEG+1+CW.CHECK)]
    snap=[[x[1] for x in CW.planes_at(pt,d,q0,t)] for t in ts]
    lab=[x[0] for x in CW.planes_at(pt,d,q0,F(0))]
    mov=CW.moving_cubes(d)
    for c4 in combinations(range(len(lab)),4):
        if not any(lab[i][0] in mov for i in c4): continue
        vals=[CW.concur_det(*[snap[si][i] for i in c4]) for si in range(len(ts))]
        co=CW.newton_poly(ts[:CW.DEG+1],vals[:CW.DEG+1])
        if not all(CW._polyval(co,ts[CW.DEG+1+j])==vals[CW.DEG+1+j] for j in range(CW.CHECK)): continue
        if len(co)<2 or CW.sturm_count(co,F(lo),F(hi))==0: continue
        P=sp.Poly([sp.Rational(x) for x in co],T)
        out+= [(F(a),F(b),'concurrency') for a,b in C.root_intervals(P,float(lo),float(hi))]
    out.sort(key=lambda x:(x[0],x[1]))
    return out
src=json.load(open('/Users/dmi/cube-compounds/data/c_by_level.json'))['instances']
rng=random.Random(9); results=[]
for inst in src[:8]:
    base=[tuple(q) for q in inst['quats']]
    D.set_field(0); D.QZERO[:]=[base[0]]; pt=D.point_of(base); nc=len(pt)
    for attempt in range(3):
        d=[F(rng.choice((-1,0,1))) for _ in range(nc)]
        if not any(d): continue
        pts=[F(i,20) for i in list(range(-10,0))+list(range(1,11))]
        vals=[(s,cvec(pt,d,nc,base[0],s)) for s in pts]
        vals=[(s,v) for s,v in vals if v]
        trans=None
        for (s1,v1),(s2,v2) in zip(vals,vals[1:]):
            if max(x[3] for x in v1.values())!=max(x[3] for x in v2.values()):
                trans=(s1,s2); break
        if not trans: continue
        lo,hi=trans
        rr=roots_in(pt,d,nc,base[0],base,lo,hi)
        if not rr: continue
        # CLUSTER OVERLAPPING ROOT INTERVALS FIRST.  Without this the edge list is not
        # monotonic, every cell computes a > b and returns None, and the run reports zero
        # transitions -- which is what it did three times.
        cl=[]
        for a_,b_,fam_ in rr:
            if cl and a_<=cl[-1][1]: cl[-1][1]=max(cl[-1][1],b_); cl[-1][2].append(fam_)
            else: cl.append([a_,b_,[fam_]])
        edges=[lo]+[x for c_ in cl for x in (c_[0],c_[1])]+[hi]
        cells=[]
        for i in range(0,len(edges)-1,2):
            a,b=edges[i],edges[i+1]
            s=C.simplest_in(a,b) if a<b else None
            cells.append((s,cvec(pt,d,nc,base[0],s) if s else None))
        for j in range(len(cells)-1):
            s1,v1=cells[j]; s2,v2=cells[j+1]
            if not v1 or not v2: continue
            c1=max(x[3] for x in v1.values()); c2=max(x[3] for x in v2.values())
            if c1==c2: continue
            L=[l for l in v1 if v1[l][3]!=v2[l][3]][0]
            dV=v2[L][0]-v1[L][0]; dE=v2[L][1]-v1[L][1]
            dF=(v2[L][2]-v1[L][2]) if (v1[L][2] is not None and v2[L][2] is not None) else None
            fam=collections.Counter(r[2] for r in rr if r[0]>=min(s1,s2) and r[1]<=max(s1,s2))
            results.append({'level':L,'c':[c1,c2],'dV':dV,'dE':dE,'dF':dF,'families':dict(fam)})
            print('  level %d  c %d->%d   dV=%+d dE=%+d dF=%s   walls at crossing %s'%(
                L,c1,c2,dV,dE,dF,dict(fam)), flush=True)
            break
        break
print()
print('transitions analysed: %d'%len(results))
print('  dV=0 and dE=0 in %d of %d'%(sum(1 for r in results if r['dV']==0 and r['dE']==0),len(results)))
print('  |dF|=1        in %d of %d'%(sum(1 for r in results if r['dF'] in (1,-1)),len(results)))
json.dump({'what':'does dV=dE=0 hold at every c-transition','results':results},
          open('/Users/dmi/cube-compounds/data/c_transition_general.json','w'),indent=1)
