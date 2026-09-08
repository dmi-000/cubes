#!/usr/bin/env python3
"""GO / NO-GO for the 727 weekend run: how many chambers are there really?

The Zaslavsky/Buck bound is 77 509 464 chambers (27 walls, rank 14). Measured
engine cost at n = 6 is 85.8 ms per count -- 8.6x my earlier 10 ms assumption --
so the bound implies 1 847 core-hours, i.e. 19 days on 4 cores. A 4-core weekend
affords about 10 million chambers. **The run is feasible only if the true count is
~8x below general position.**

The arrangement is extremely degenerate (0 of 351 pairs crossable, Postscript 140),
so it plausibly is. This measures rather than assumes: incremental construction
adds walls one at a time, and the chamber count after each wall is exact. The
growth curve after k walls extrapolates to k = 27, and needs NO engine calls --
only exact LP -- so it costs minutes.

Reports the count after every wall so the curve is visible as it forms, and stops
on a time budget rather than running unbounded.
"""
import itertools, json, sys, time
from fractions import Fraction as F
import os as _os
HERE=_os.path.dirname(_os.path.abspath(__file__)); sys.path.insert(0,HERE)
import sympy as sp, dimension as D
from isolation67 import _fm
from arrangement import zaslavsky_bound

BASE=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
def qmul(a,b):
    w1,x1,y1,z1=a; w2,x2,y2,z2=b
    return (w1*w2-x1*x2-y1*y2-z1*z2,w1*x2+x1*w2+y1*z2-z1*y2,
            w1*y2-x1*z2+y1*w2+z1*x2,w1*z2+x1*y2-y1*x2+z1*w2)

def walls_of(cfg):
    q=cfg
    for g in ((1,0,0,0),(2,1,0,0),(3,1,1,0),(5,1,2,1)):
        o=[qmul(g,x) for x in cfg]
        if all(y[0]!=0 for y in o): q=o; break
    D.set_field(0); D.QZERO[:]=[q[0]]
    pt=D.point_of(q); n=len(q); ncols=3*(n-1)
    vars_=sp.symbols('c0:%d'%ncols); Rs=D.frames(vars_,q[0])
    tight,_=D.cached_conditions(Rs,n,vars_,pt,D.quats_of(pt,q[0]),q[0])
    good=[t for t in tight if not t['degenerate']]
    def _norm(g):
        piv=next((x for x in g if x!=0),None)
        return tuple(str(x/piv) for x in g) if piv is not None else None
    seen,W={},[]
    for t in good:
        k=_norm(t['grad'])
        if k is not None and k not in seen: seen[k]=True; W.append(t['grad'])
    return W,ncols

def grow(W,ncols,budget=900,label=''):
    """chamber count after each wall added; exact LP only, no engine calls"""
    m=len(W); rank=ncols-len(D.nullspace(W,ncols))
    print('%s: %d walls, rank %d of %d | Zaslavsky bound %s'
          %(label,m,rank,ncols,'{:,}'.format(zaslavsky_bound(m,rank))),flush=True)
    live=[()]                       # sign vectors over the walls added so far
    t0=time.time(); curve=[]
    for i,w in enumerate(W):
        nxt=[]
        for sv in live:
            rows=[]
            for j,s in enumerate(sv):
                rows.append([s*W[j][t] for t in range(ncols)])
            pos=_fm(rows+[[w[t] for t in range(ncols)]],ncols) is not None
            neg=_fm(rows+[[-w[t] for t in range(ncols)]],ncols) is not None
            if pos: nxt.append(sv+(1,))
            if neg: nxt.append(sv+(-1,))
        live=nxt; el=time.time()-t0
        curve.append({'walls':i+1,'chambers':len(live),'sec':round(el,1)})
        print('   after %2d walls: %9s chambers  (%.0fs)'
              %(i+1,'{:,}'.format(len(live)),el),flush=True)
        if el>budget:
            print('   TIME BUDGET reached; curve truncated at %d of %d walls'%(i+1,m),flush=True)
            break
    return curve,m,rank

def main():
    W,nc=walls_of(BASE+[(7,14,1,-5)])
    curve,m,rank=grow(W,nc,budget=float(sys.argv[1]) if len(sys.argv)>1 else 900,label='727')
    json.dump({'walls':m,'rank':rank,'ambient':nc,'bound':zaslavsky_bound(m,rank),
               'curve':curve},open(HERE+'/growth727.json','w'),indent=1)


# WITHOUT THIS GUARD, importing anything from this file RE-RUNS THE CAMPAIGN.
# A decomposition test that did `from growth727 import walls_of` restarted the
# whole growth curve -- the same failure this session already recorded for the
# multiprocessing spawn context, in a plainer form.
if __name__ == '__main__':
    main()
