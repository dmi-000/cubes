#!/usr/bin/env python3
"""Index-INVARIANT wall comparison: does one configuration's wall set embed in
another's under some relabelling of cubes?

Postscript 137's matrix is index-dependent. 393 and 727 share 168/168 only because
727 is literally 393 plus a cube in the SAME ORDER; 183 shares just 56/108 with
393 despite the tower nesting, because the 183 measured is a different
representative with its own numbering. Off-diagonal entries therefore UNDERSTATE
sharing, and no conclusion about non-sharing can be drawn from them.

The invariant version maximises shared labels over relabellings. A label
(frame i, {(cube j, normal k, sign s)}) transports under a cube permutation sigma
to (sigma(i), {(sigma(j), k, s)}). Cube AXIS relabelling is NOT quotiented here --
stated as a limit, since a full invariant would also range over each cube's 24
self-symmetries.

TEST CASE: 183 against every 4-subset of 393, over all relabellings. The tower
says 183 is a subset of 393, so a good embedding should exist. If none does, the
tower's nesting is about counts and not about wall systems -- itself worth knowing.
"""
import itertools, sys
import os as _os
HERE=_os.path.dirname(_os.path.abspath(__file__)); sys.path.insert(0,HERE)
from wall_sharing import labels

def relabel(L, perm):
    """apply a cube permutation to a label set"""
    out=set()
    for i,g in L:
        out.add((perm[i], tuple(sorted((perm[c],k,s) for c,k,s in g))))
    return out

def best_overlap(LA, LB, nA, nB):
    """max |relabel(LA) & LB| over injections of A's cubes into B's"""
    best=(-1,None)
    for tgt in itertools.permutations(range(nB), nA):
        perm={i:tgt[i] for i in range(nA)}
        sh=len(relabel(LA,perm)&LB)
        if sh>best[0]: best=(sh,tgt)
    return best

BASE=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
A1=[(1,0,0,0),(0,5,3,2),(1,-4,-1,1),(1,1,-1,-4)]
A2=[(1,0,0,0),(-2,-2,5,-2),(3,11,-3,-3),(0,-7,4,-3)]
print('computing label sets...',flush=True)
L393=labels(BASE,0); print('  393: %d labels'%len(L393),flush=True)
L1=labels(A1,0); L2=labels(A2,0)
print('  183 class 1: %d, class 2: %d'%(len(L1),len(L2)),flush=True)
for nm,L in (('183 class 1',L1),('183 class 2',L2)):
    sh,tgt=best_overlap(L,L393,4,5)
    print('%s -> 393: BEST overlap %d of %d (%.0f%%) under cube map %s'
          %(nm,sh,len(L),100*sh/len(L),str(tgt)),flush=True)
sh,tgt=best_overlap(L1,L2,4,4)
print('183 class 1 -> class 2: best overlap %d of %d under %s (index-aligned was 88)'
      %(sh,len(L1),str(tgt)),flush=True)
