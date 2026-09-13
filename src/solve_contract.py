import sys, subprocess; sys.path.insert(0,'src')
import dimension as D, wall_keys as W, map_arcs as M, wall_solve as WS
from fractions import Fraction as F
import sympy as sp
B5=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
REC={7:W.REC[7],8:W.REC[8],
     9:B5+[(7,14,1,-5),(4,-3,-4,-4),(168,-168,168,-415),(109,-11,91,140)]}
a0,vv,lo,hi=M.ARCS['D']
MOV=5                                  # the base direction moves cube 5
t=sp.Symbol('t')
for n,q in REC.items():
    D.set_field(0); D.QZERO[:]=[q[0]]
    pt=D.point_of(q); nc=3*(len(q)-1)
    d=[F(0)]*nc
    for k in range(3): d[12+k]=vv[k]
    conds=[c for c in WS.conditions_on(q)
           if c['frame']==MOV or any(x[0]==MOV for x in c['group'])]
    hits=[]
    for c in conds:
        key={k:c[k] for k in ('frame','group','sig','c0')}
        try: co=W.on_line(key,q[0],pt,d)
        except Exception: continue
        if len(co)<2: continue
        for r in WS._roots_exact(co,t):
            if -0.06 < r['decimal'] < -0.012:
                hits.append((r,c))
    hits.sort(key=lambda x:-x[0]['decimal'])
    print("n=%d: %d conditions touch cube %d | %d roots in (-0.06,-0.012)"%(n,len(conds),MOV,len(hits)))
    seen=set()
    for r,c in hits:
        k=round(r['decimal'],10)
        if k in seen: continue
        seen.add(k)
        involves_new = [x[0] for x in c['group'] if x[0]>6] + ([c['frame']] if c['frame']>6 else [])
        ex=r.get('value') or r.get('minimal_polynomial')
        print("    t=%.10f  %-9s frame %d group %s  new-cube? %s"
              %(r['decimal'],r['kind'],c['frame'],[list(x) for x in c['group']],
                'YES %s'%sorted(set(involves_new)) if involves_new else 'no'))
    print()
