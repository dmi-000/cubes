#!/usr/bin/env python3
"""Which cubes does each wall involve, and do subset walls lift to the full set?

A wall is FOUR FACE PLANES CONCURRENT (Postscript 57), and the four are supplied
by at most 4 cubes -- (3,1), (2,2), (2,1,1), (1,1,1,1).  So every wall of an
n-cube configuration should already be a wall of some subset of size <= 4, and
conversely a subset's wall should survive into the full configuration.

Measured here rather than assumed: the gradient of a wall lives in the full
ambient R^(3(n-1)), one 3-block per non-frozen cube, so the BLOCKS THAT ARE
NONZERO name the cubes the wall constrains.  Cube 0 is frozen as the gauge, so a
wall involving cube 0 and cube j shows support on j alone -- the count of
supported blocks is a LOWER bound on the cubes involved, by exactly one when
cube 0 participates.
"""
import json, os, sys
from collections import Counter
import os as _os
HERE=_os.path.dirname(_os.path.abspath(__file__)); sys.path.insert(0,HERE)
import sympy as sp, dimension as D

BASE=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
R={5:BASE,6:BASE+[(7,14,1,-5)]}
R[7]=R[6]+[(4,-3,-4,-4)]; R[8]=R[7]+[(24,-24,24,-61)]; R[9]=R[8]+[(56,56,55,56)]

def walls_and_support(quats):
    D.set_field(0); D.QZERO[:]=[quats[0]]
    pt=D.point_of(quats); ncols=3*(len(quats)-1)
    vars_=sp.symbols('c0:%d'%ncols); Rs=D.frames(vars_,quats[0])
    tight,_=D.cached_conditions(Rs,len(quats),vars_,pt,D.quats_of(pt,quats[0]),quats[0])
    good=[t for t in tight if not t['degenerate']]
    def _norm(g):
        piv=next((x for x in g if x!=0),None)
        return tuple(str(x/piv) for x in g) if piv is not None else None
    seen,walls={},[]
    for t in good:
        k=_norm(t['grad'])
        if k is not None and k not in seen:
            seen[k]=True; walls.append((k,t['grad'],t['frame'],t['group']))
    out=[]
    for key,g,frame,grp in walls:
        blocks=tuple(b for b in range(ncols//3)
                     if any(g[3*b+r]!=0 for r in range(3)))
        out.append({'key':key,'blocks':blocks,'frame':frame,
                    'cubes_in_group':sorted(set([frame]+[x[0] for x in grp]))})
    return out, ncols

if __name__=='__main__':
    res={}
    for n in (5,6,7,8,9):
        w,ncols=walls_and_support(R[n])
        sup=Counter(len(x['blocks']) for x in w)
        cub=Counter(len(x['cubes_in_group']) for x in w)
        print('n=%d: %d walls | support blocks %s | cubes named by the condition %s'
              %(n,len(w),dict(sorted(sup.items())),dict(sorted(cub.items()))))
        res[n]=[{'blocks':list(x['blocks']),'cubes':x['cubes_in_group']} for x in w]
    json.dump(res,open(os.path.join(HERE,'wall_support.json'),'w'),indent=1)
    # do the n=6 walls appear among the n=7 walls?
    w6,_=walls_and_support(R[6]); w7,_=walls_and_support(R[7])
    k6={x['key'] for x in w6}
    # a wall of the 6-config, padded with zeros, should be a wall of the 7-config
    def pad(key,to):
        v=list(key)+['0']*(to-len(key)); return tuple(v)
    k7={x['key'] for x in w7}
    lifted=sum(1 for x in w6 if pad(x['key'],3*6) in k7)
    print('\nn=6 walls that reappear (zero-padded) among n=7 walls: %d of %d'
          %(lifted,len(w6)))
