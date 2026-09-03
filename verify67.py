#!/usr/bin/env python3
"""Are the two 67s really 0-dimensional? The Jacobian-rank plan, unblocked.

`MAXIMISER_TAXONOMY.md` §5 has listed this as an open gap: "**The two 67s' Jacobian
rank** — would upgrade their isolation from a codimension heuristic to a computation.
Representatives are in `MAXIMISERS.md`; the obstacle is that the walls must be
differentiated in Q(sqrt 2) and Q(sqrt 5) rather than Q."

**The obstacle is gone.** `verify393.py` did exactly this computation in Q on
2026-09-01 ([P204](LEDGER.md#p204)), and both `dimension.set_field(d)` and
`epscount.count_eps(point, direction, d, q0)` already take the field. So the same
method runs over Q(sqrt 2) and Q(sqrt 5) unchanged.

METHOD, identical to P204: candidates from the null space AND every cube's 3-slice
(rank-2 null directions, or the full orthogonal complement where those span rank < 2),
each verified with eps on BOTH signs. A null-space-only pool gives a FALSE negative at
727, so the gate is 727 — but 727 lives in Q, and these live in Q(sqrt d), so the gate
is run in its own field and the field-dependence is what is being trusted.

If both come back rank 0 with nothing unevaluated, the 67s' isolation stops being a
codimension heuristic and becomes a measurement.
"""
import itertools, sys
sys.path.insert(0,'.')
from fractions import Fraction as F
from math import gcd
import sympy as sp
from qfield import Q as QF
import dimension as D
from epscount import count_eps

CASES=[(2,'octahedral 67 (Q(sqrt2))',
        [((1,0),(0,0),(0,0),(0,0)),((1,0),(1,0),(0,1),(0,0)),((-1,0),(1,0),(0,1),(0,0))]),
       (5,'golden 67 (Q(sqrt5))',
        [((1,0),(0,0),(0,0),(0,0)),((2,0),(1,1),(-1,1),(0,0)),((-2,0),(1,1),(-1,1),(0,0))])]

def prim(v):
    den=1
    for x in v: den=den*F(x).denominator//gcd(den,F(x).denominator)
    iv=[int(F(x)*den) for x in v]; g=0
    for x in iv: g=gcd(g,abs(x))
    iv=[x//(g or 1) for x in iv]
    for x in iv:
        if x>0: break
        if x<0: iv=[-y for y in iv]; break
    return tuple(iv)

for d,label,raw in CASES:
    quats=[tuple(QF(F(p),F(q),d) for p,q in x) for x in raw]
    D.set_field(d); D.QZERO[:]=[quats[0]]
    pt=[x for q in quats[1:] for x in D.cayley_of(q)]
    ncols=3*(len(quats)-1)
    vars_=sp.symbols('c0:%d'%ncols); Rs=D.frames(vars_,quats[0])
    tight,loose=D.cached_conditions(Rs,len(quats),vars_,pt,D.quats_of(pt,quats[0]),quats[0])
    good_t=[t for t in tight if not t['degenerate']]
    seen,walls=set(),[]
    for t in good_t:
        g=t['grad']; piv=next((x for x in g if x!=0),None)
        if piv is None: continue
        k=tuple(str(x/piv) for x in g)
        if k not in seen: seen.add(k); walls.append(g)
    null=D.nullspace(walls,ncols)
    rec=D.count_at(pt,len(quats))
    z=count_eps(pt,[QF(F(0),F(0),d)]*ncols,d,quats[0])
    if z is None: z=count_eps(pt,[QF(F(0),F(0),d)]*ncols,d,quats[0],wide=True)
    w0=count_eps(pt,[QF(F(x),F(0),d) if not hasattr(x,'a') else x for x in walls[0]],d,quats[0])
    if w0 is None:
        w0=count_eps(pt,[QF(F(x),F(0),d) if not hasattr(x,'a') else x for x in walls[0]],d,quats[0],wide=True)
    print('\n%s  record %s  ambient %d  walls %d  deficit %d'
          %(label,rec,ncols,len(walls),len(null)),flush=True)
    print('   CONTROLS zero->%s  wall-gradient->%s  %s'
          %(z,w0,'OK' if (z==rec and w0 is not None and w0!=rec) else 'FAILED'),flush=True)
    if not (z==rec and w0 is not None and w0!=rec):
        print('   controls failed — nothing below would mean anything',flush=True); continue
    cands=[prim([F(str(x)) if not hasattr(x,'a') else F(x.a) for x in v]) for v in null]
    for j in range(1,len(quats)):
        sl=slice(3*(j-1),3*j)
        proj=[]
        for g in walls:
            t=prim([F(x.a) if hasattr(x,'a') else F(x) for x in list(g)[sl]])
            if any(t) and t not in proj: proj.append(t)
        got=[]
        for u,w in itertools.combinations(proj,2):
            c=(u[1]*w[2]-u[2]*w[1],u[2]*w[0]-u[0]*w[2],u[0]*w[1]-u[1]*w[0])
            if any(c): got.append(prim(list(c)))
        if not got and proj:
            for b in sp.Matrix([list(v) for v in proj]).nullspace():
                dd=prim([sp.Rational(x) for x in b])
                if any(dd): got.append(dd)
        for c in got:
            full=[0]*ncols; full[3*(j-1):3*j]=list(c)
            cands.append(prim(full))
    seen2=set(); cands=[c for c in cands if c not in seen2 and not seen2.add(c)]
    good=[]; unev=0
    for c in cands:
        vals=[]
        for sgn in (1,-1):
            v=count_eps(pt,[QF(F(sgn*x),F(0),d) for x in c],d,quats[0])
            if v is None: v=count_eps(pt,[QF(F(sgn*x),F(0),d) for x in c],d,quats[0],wide=True)
            vals.append(v)
        if None in vals: unev+=1
        elif vals[0]==rec and vals[1]==rec: good.append(c)
    rk=sp.Matrix([list(g) for g in good]).rank() if good else 0
    print('   pool %d candidates (null + every cube-slice), %d UNEVALUATED'%(len(cands),unev),flush=True)
    print('   preserving directions %d, RANK %d'%(len(good),rk),flush=True)
    if rk==0 and unev==0:
        print('   => 0-DIMENSIONAL: a single point. Isolation is now a MEASUREMENT,',flush=True)
        print('      not a codimension heuristic.',flush=True)
