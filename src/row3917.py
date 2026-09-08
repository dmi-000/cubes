#!/usr/bin/env python3
"""Full arrangement row for the new n=10 record 3917, beside 3913.

[P185] measured n=10 as walls 101 / tight 482 against P172's predicted 123 / 552 and
concluded the linear law breaks at n=10. That was measured on 3913, which [P191]
superseded. If 3917 restores 123/552 the law never broke — the record did. This
settles which.
"""
import sys
sys.path.insert(0, '.')
import sympy as sp, dimension as D

BASE=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
C9=BASE+[(7,14,1,-5),(4,-3,-4,-4),(24,-24,24,-61),(57,57,56,57)]
ROWS=[('n=10 3913 (P181)', C9+[(19,-2,15,24)]),
      ('n=10 3917 (P191)', C9+[(88787,-9061,74275,113786)])]
print('%-20s %7s %7s %7s %7s %6s %6s %8s'
      %('','count','tight','degen','walls','amb','rank','deficit'), flush=True)
for name,quats in ROWS:
    D.set_field(0); D.QZERO[:]=[quats[0]]
    pt=D.point_of(quats); ncols=3*(len(quats)-1)
    vars_=sp.symbols('c0:%d'%ncols); Rs=D.frames(vars_,quats[0])
    tight,loose=D.cached_conditions(Rs,len(quats),vars_,pt,D.quats_of(pt,quats[0]),quats[0])
    degen=sum(1 for t in tight if t['degenerate'])
    good=[t for t in tight if not t['degenerate']]
    seen,walls=set(),[]
    for t in good:
        g=t['grad']; piv=next((x for x in g if x!=0),None)
        if piv is None: continue
        k=tuple(str(x/piv) for x in g)
        if k not in seen: seen.add(k); walls.append(g)
    rank=ncols-len(D.nullspace(walls,ncols))
    print('%-20s %7d %7d %7d %7d %6d %6d %8d'
          %(name,D.count_at(pt,len(quats)),len(tight),degen,len(walls),ncols,rank,ncols-rank),
          flush=True)
print('\nP172 linear law predicts at n=10: walls 123, tight 552, rank 22, deficit 5', flush=True)
