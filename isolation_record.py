#!/usr/bin/env python3
"""What surrounds the RATIONAL records — the same face enumeration that settled
the two 67s, pointed at 727 and its tower.

The 67s are the only maximisers whose neighbourhoods have ever been enumerated,
purely because `isolation67.py` hard-codes them.  The census says the higher
records are isolated (second-order variety EMPTY, dirs = 0) but records NO
neighbouring count, so "what is next to 727" has never been measured.  Nothing in
the method is specific to n = 3 or to Q(sqrt d).

Counts come from the INFINITESIMAL engine (Postscript 119), so there is no step
size to be wrong about, and the count returned is the eps -> 0 limit.
"""
import json, os, sys, time
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sympy as sp
import dimension as D, provenance
from isolation67 import faces
from epscount import count_eps

BASE=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
R={6:BASE+[(7,14,1,-5)]}
R[7]=R[6]+[(4,-3,-4,-4)]; R[8]=R[7]+[(24,-24,24,-61)]; R[9]=R[8]+[(56,56,55,56)]

def run(n, log):
    D.set_field(0)
    quats=R[n]; D.QZERO[:]=[quats[0]]
    pt=D.point_of(quats); ncols=3*(len(quats)-1)
    base=D.count_at(pt,len(quats))
    print('n=%d record: count %s, ambient %d'%(n,base,ncols),file=log,flush=True)
    vars_=sp.symbols('c0:%d'%ncols); Rs=D.frames(vars_,quats[0])
    tight,loose=D.cached_conditions(Rs,len(quats),vars_,pt,D.quats_of(pt,quats[0]),quats[0])
    good=[t for t in tight if not t['degenerate']]
    def _norm(g):
        piv=next((x for x in g if x!=0),None)
        return tuple(str(x/piv) for x in g) if piv is not None else None
    seen,walls={},[]
    for t in good:
        k=_norm(t['grad'])
        if k is not None and k not in seen: seen[k]=True; walls.append(t['grad'])
    print('   %d tight -> %d distinct walls'%(len(good),len(walls)),file=log,flush=True)
    t0=time.time()
    fs=faces(walls,ncols,F(0),log)
    hits,unres,by={},[],{}
    for sigma,dv in fs:
        d0=D.normalize_dir(dv)
        c=count_eps(pt,d0,0,quats[0])
        if c is None: unres.append(list(sigma)); continue
        by[c]=by.get(c,0)+1
        if c>=base: hits[tuple(sigma)]=c
    print('   faces by count: %s'%dict(sorted(by.items(),reverse=True)),file=log,flush=True)
    print('   %s -- %d reaching %d, %d unresolved, %.0fs'
          %('ISOLATED' if not hits else 'NOT ISOLATED',len(hits),base,len(unres),
            time.time()-t0),file=log,flush=True)
    ev=sum(v for k,v in by.items() if k%2==0)
    print('   parity: %d even of %d faces (P121: even => a SHELL)'
          %(ev,sum(by.values())),file=log,flush=True)
    return {'n':n,'count':base,'walls':len(walls),'faces':len(fs),
            'by_count':{str(k):v for k,v in sorted(by.items())},
            'n_hits':len(hits),'unresolved':len(unres),
            'even_faces':ev,'secs':round(time.time()-t0,1)}

def main():
    here=os.path.dirname(os.path.abspath(__file__))
    log=open(os.path.join(here,'isolation_record.log'),'a')
    print('\n===== %s'%time.strftime('%Y-%m-%d %H:%M:%S'),file=log,flush=True)
    out=[]
    for n in [int(x) for x in (sys.argv[1:] or ['6'])]:
        out.append(run(n,log))
        json.dump(out,open(os.path.join(here,'isolation_record.json'),'w'),indent=1)
    provenance.stamp(os.path.join(here,'isolation_record.json'),
                     note='face enumeration around the rational records, infinitesimal eps')

if __name__=='__main__':
    main()
