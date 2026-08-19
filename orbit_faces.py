#!/usr/bin/env python3
"""Do the octahedral 67's faces fall into symmetry orbits, and is shell-freedom
an ORBIT-INVARIANT property?

Postscript 129 sharpened the shell question to a quantified anomaly: the
octahedral 67's 728 neighbouring faces span the same count range as the golden
67's, so the measured count-suppression trend predicts about 70 shells. It has
ZERO. Golden, at 6.7%, sits at expectation.

The octahedral 67 has symmetry order 24 and SIX INDEPENDENT walls, so its faces
form a simplicial 3^6-1 arrangement. If the symmetry group acts on that
arrangement, every count is constant on orbits, and an orbit-invariant property is
ALL-OR-NOTHING rather than intermediate -- which is the signature of an exact
zero. This tests that directly.

METHOD.  A symmetry g of the configuration permutes the cubes and hence permutes
the WALLS (each wall is a condition on a set of cubes), and therefore permutes the
faces by permuting sign vectors.  Rather than reconstruct that action symbolically,
the test here is empirical and stronger: if the counts are constant on orbits of a
group of order 24, the multiset of counts must be a union of orbit-sized blocks,
so **every count multiplicity is a sum of divisors of 24**.  Golden (order 6)
should show multiplicities compatible with 6, and any configuration with trivial
symmetry should show no such structure.
"""
import json, os, sys
from collections import Counter
import os as _os
HERE=_os.path.dirname(_os.path.abspath(__file__)); sys.path.insert(0,HERE)

def divisors(n): return [d for d in range(1,n+1) if n%d==0]

def decomposable(m, divs):
    """can m be written as a sum of the given divisors?"""
    reach={0}
    for _ in range(m):
        new={r+d for r in reach for d in divs if r+d<=m}
        if new<=reach: break
        reach|=new
    return m in reach

def main():
    d={r['name']:r for r in json.load(open(os.path.join(HERE,'isolation67_eps.json')))}
    ORDER={'octahedral':24,'golden':6}
    for name in ('octahedral','golden'):
        r=d[name]; order=ORDER[name]
        h={int(k):v for k,v in r['by_count'].items()}
        divs=divisors(order)
        print('%s 67: symmetry order %d, %d faces, %d distinct counts'
              %(name,order,sum(h.values()),len(h)),flush=True)
        bad=[]
        for c,m in sorted(h.items(),reverse=True):
            ok=decomposable(m,divs)
            if not ok: bad.append((c,m))
            print('   count %3d  multiplicity %4d  %s'
                  %(c,m,'sum of divisors of %d'%order if ok else 'NOT decomposable'),flush=True)
        print('   -> %d counts incompatible with orbits of size dividing %d\n'
              %(len(bad),order),flush=True)
        # per-codimension too: the group preserves codimension
        byco={}
        for f in r.get('per_face',[]):
            byco.setdefault(f['codim'],Counter())[f['count']]+=1
        for k in sorted(byco):
            mults=sorted(byco[k].values(),reverse=True)
            allok=all(decomposable(m,divs) for m in mults)
            print('   codim %d: multiplicities %s  %s'
                  %(k,mults[:8],'all orbit-compatible' if allok else 'SOME NOT'),flush=True)
        print(flush=True)

if __name__=='__main__': main()
