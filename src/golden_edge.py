#!/usr/bin/env python3
"""Is the GOLDEN 67 inside the 55 region or ON its edge?

The full scan (map_dihedral.py) puts the octahedral 67 deep inside the 55 run and
the golden 67 in the 55 -> 43 BOUNDARY BRACKET, width 0.108 deg.  That is a real
structural asymmetry between the two n=3 maximisers, but a bracket is not an
answer: the 55 run's edge is a sampled value, so the region could extend past it
and contain the golden angle after all.

METHOD.  Approach the golden angle from BOTH sides with rational psi (Pythagorean
triples, which is what "rational sine" means here), taking the closest available
on each side and going as fine as the triple supply allows.  If the counts differ
across the golden angle, it sits ON the wall.  If both sides read 55, the region
contains it and the scan's edge was simply the last sample.

WHAT THIS CANNOT DO.  Land on the golden angle.  It is irrational, so no triple
reaches it; that is why it is a PUNCTURE.  The answer here is about the region's
edge, not about the point.
"""
import math, json, sys, os
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
ROOT=os.path.dirname(HERE) if os.path.basename(HERE)=='src' else HERE
from q3_count import count_triple

GOLD = 69.09484255

def triples(rmax, lo, hi):
    out=[]
    for m in range(2, 1400):
        for n in range(1, m):
            if (m-n)%2 or math.gcd(m,n)!=1:
                continue
            a,b,c=m*m-n*n,2*m*n,m*m+n*n
            if c>rmax: continue
            for p,q in ((a,b),(b,a)):
                psi=math.degrees(math.asin(p/c))
                if lo<psi<hi: out.append((psi,p,q,c))
    return sorted(out)

def main():
    lo,hi=68.90,69.30
    ts=triples(60000, lo, hi)
    below=[t for t in ts if t[0]<GOLD][-6:]
    above=[t for t in ts if t[0]>GOLD][:6]
    print('%d triples with psi in (%.2f, %.2f), r <= 60000'%(len(ts),lo,hi),flush=True)
    print('golden angle %.8f\n'%GOLD,flush=True)
    rows=[]
    for tag,lst in (('BELOW',below),('ABOVE',above)):
        for psi,p,q,r in lst:
            c,_=count_triple(p,q,r)
            rows.append({'side':tag,'psi':psi,'gap':abs(psi-GOLD),
                         'triple':[p,q,r],'count':c})
            print('  %-5s psi=%12.8f  gap %.8f  (%d,%d,%d)  count %d'
                  %(tag,psi,abs(psi-GOLD),p,q,r,c),flush=True)
    b=[x for x in rows if x['side']=='BELOW']; a=[x for x in rows if x['side']=='ABOVE']
    bc={x['count'] for x in b}; ac={x['count'] for x in a}
    print('\nbelow the golden angle: counts %s' % sorted(bc))
    print('above the golden angle: counts %s' % sorted(ac))
    if bc!=ac:
        verdict=('the golden 67 sits ON the 55/43 wall: rational approaches give '
                 'different counts on the two sides')
    elif bc=={55}:
        verdict=('the 55 region CONTAINS the golden angle; map_dihedral.py\'s edge '
                 'was just its last sample')
    else:
        verdict='both sides agree at %s -- neither of the expected cases'%sorted(bc)
    print('\nVERDICT: '+verdict)
    json.dump({'what':'which side of the 55/43 edge the golden 67 is on',
               'golden_psi':GOLD,'rows':rows,'verdict':verdict,
               'CANNOT':'land on the golden angle -- it is irrational, hence a puncture'},
              open(os.path.join(ROOT,'data','golden_edge.json'),'w'),indent=1)
    print('written data/golden_edge.json')

if __name__=='__main__':
    main()
