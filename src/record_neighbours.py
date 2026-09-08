#!/usr/bin/env python3
"""The IMMEDIATE neighbours of a record: the count across each wall.

Full face enumeration settled the two 67s (728 and 2 196 faces) but does not
scale: the n=6 record has 27 distinct walls in ambient 15, a nominal 3^27 = 7.6e12
sign vectors, and the attempt died on memory with no output.  Reporting a partial
histogram from that would be worse than not running it.

What IS tractable, and is what "what surrounds it" asks first, is the codimension-1
layer: for each wall, the direction crossing THAT WALL ALONE is determined by the
geometry (null space of the others, non-orthogonal to this one), so no direction
is chosen and nothing is sampled.  Counts come from the infinitesimal engine, so
there is no step size either.

This is the FIRST layer only.  Faces of codimension >= 2 are NOT enumerated here,
and the histogram below must not be read as the full neighbourhood.
"""
import json, os, sys, time
from fractions import Fraction as F
import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sympy as sp
import dimension as D, provenance
from epscount import count_eps

BASE=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
R={6:BASE+[(7,14,1,-5)]}
R[7]=R[6]+[(4,-3,-4,-4)]; R[8]=R[7]+[(24,-24,24,-61)]; R[9]=R[8]+[(56,56,55,56)]

def run(n, log):
    D.set_field(0); quats=R[n]; D.QZERO[:]=[quats[0]]
    pt=D.point_of(quats); ncols=3*(len(quats)-1)
    base=D.count_at(pt,len(quats))
    vars_=sp.symbols('c0:%d'%ncols); Rs=D.frames(vars_,quats[0])
    tight,_=D.cached_conditions(Rs,len(quats),vars_,pt,D.quats_of(pt,quats[0]),quats[0])
    good=[t for t in tight if not t['degenerate']]
    def _norm(g):
        piv=next((x for x in g if x!=0),None)
        return tuple(str(x/piv) for x in g) if piv is not None else None
    seen,walls={},[]
    for t in good:
        k=_norm(t['grad'])
        if k is not None and k not in seen: seen[k]=True; walls.append(t['grad'])
    print('n=%d count %d | ambient %d | %d tight -> %d walls'
          %(n,base,ncols,len(good),len(walls)),file=log,flush=True)
    t0=time.time(); out=[]; uneval=0
    for i,wl in enumerate(walls):
        sub=[walls[t] for t in range(len(walls)) if t!=i]
        cross=None
        for v in D.nullspace(sub,ncols):
            if sum(wl[k]*v[k] for k in range(ncols))!=0: cross=v; break
        if cross is None:
            out.append({'wall':i,'beyond':None,'reason':'entangled: no direction crosses it alone'})
            uneval+=1; continue
        dv=D.normalize_dir(cross)
        plus=count_eps(pt,dv,0,quats[0]); minus=count_eps(pt,[-x for x in dv],0,quats[0])
        if plus is None and minus is None: uneval+=1
        out.append({'wall':i,'beyond':[plus,minus]})
        print('   wall %2d: %s / %s'%(i,plus,minus),file=log,flush=True)
    vals=[v for r in out if r.get('beyond') for v in r['beyond'] if v is not None]
    from collections import Counter
    h=dict(sorted(Counter(vals).items(),reverse=True))
    ev=sum(v for k,v in h.items() if k%2==0)
    print('   facet counts: %s'%h,file=log,flush=True)
    print('   best neighbour %s (drop %s) | %d unevaluable of %d walls | %d even (P121 shell) | %.0fs'
          %(max(h) if h else None,(base-max(h)) if h else None,uneval,len(walls),ev,time.time()-t0),
          file=log,flush=True)
    return {'n':n,'count':base,'walls':len(walls),'ambient':ncols,
            'facets':out,'histogram':{str(k):v for k,v in h.items()},
            'best_neighbour':max(h) if h else None,'unevaluable':uneval,
            'even_faces':ev,'codimension':'1 ONLY -- deeper faces not enumerated',
            'secs':round(time.time()-t0,1)}

def main():
    log=open(os.path.join(HERE,'record_neighbours.log'),'a')
    print('\n===== %s'%time.strftime('%Y-%m-%d %H:%M:%S'),file=log,flush=True)
    out=[]
    for n in [int(x) for x in (sys.argv[1:] or ['6'])]:
        out.append(run(n,log))
        json.dump(out,open(os.path.join(HERE,'record_neighbours.json'),'w'),indent=1)
    provenance.stamp(os.path.join(HERE,'record_neighbours.json'),
                     note='codimension-1 neighbours of the records, infinitesimal eps')

if __name__=='__main__': main()
