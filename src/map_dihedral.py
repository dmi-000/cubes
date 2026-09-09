#!/usr/bin/env python3
"""Map the whole 67<->67 dihedral family, not two hand-placed windows.

region_shape.py samples two windows chosen around the answers it expected, and
its LOWER window returns 55 at all nine points -- which is not an edge, it is a
window that missed.  That is the "choose controls that are hard for the method"
failure in miniature: the window was placed where the edge was believed to be.

This scans the FULL range of the family instead and reports every count change,
so the region's edges are found rather than confirmed.

WHAT THIS IS AND IS NOT.  The family is parameterised by an angle psi, and the
points available are those with a rational sine -- Pythagorean triples.  So every
edge below is a BRACKET between two adjacent sampled psi, and the true edge is an
algebraic number inside it.  A sampled edge is a lower bound on the region's
extent, never the region.  The two 67s are NOT samples: they are exact, at
arcsin(1/sqrt3) and the golden angle, and both are irrational, which is why no
rational scan will ever land on them.
"""
import math, json, sys, os
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
ROOT=os.path.dirname(HERE) if os.path.basename(HERE)=='src' else HERE
from q3_count import count_triple

OCT, GOLD = 35.26438968, 69.09484255           # arcsin(1/sqrt3), golden

def triples(rmax=4000):
    out=set()
    for m in range(2,300):
        for n in range(1,m):
            if (m-n)%2==1 and math.gcd(m,n)==1:
                a,b,c=m*m-n*n,2*m*n,m*m+n*n
                for k in range(1,rmax//c+1):
                    out.add((a*k,b*k,c*k)); out.add((b*k,a*k,c*k))
    return out

def main():
    pts=[]
    seen=set()
    for p,q,r in triples():
        psi=math.degrees(math.asin(p/r))
        key=round(psi,4)
        if key in seen: continue
        seen.add(key); pts.append((psi,p,q,r))
    pts.sort()
    print('%d distinct psi sampled, %.4f to %.4f deg'%(len(pts),pts[0][0],pts[-1][0]),
          flush=True)
    runs=[]; prev=None
    for psi,p,q,r in pts:
        c,_=count_triple(p,q,r)
        if prev is None or c!=prev[0]:
            runs.append({'count':c,'from_psi':psi,'to_psi':psi,
                         'from_triple':[p,q,r],'to_triple':[p,q,r],'n':1})
        else:
            runs[-1]['to_psi']=psi; runs[-1]['to_triple']=[p,q,r]; runs[-1]['n']+=1
        prev=(c,)
    print('\n%d maximal runs of constant count:'%len(runs))
    for i,rn in enumerate(runs):
        mark=''
        if rn['from_psi']<OCT<rn['to_psi']: mark+='   [contains octahedral 67]'
        if rn['from_psi']<GOLD<rn['to_psi']: mark+='   [contains GOLDEN 67]'
        print('  count %3d  psi in [%9.5f, %9.5f]  %5d samples%s'
              %(rn['count'],rn['from_psi'],rn['to_psi'],rn['n'],mark),flush=True)
    big=max(runs,key=lambda r:r['n'])
    out={'what':'the 67<->67 dihedral family, full scan',
         'IMPORTANT':('every edge is a BRACKET between adjacent sampled psi; the '
                      'true edge is algebraic and lies inside. A sampled edge is a '
                      'lower bound on extent. The two 67s are exact and irrational '
                      '-- no rational scan lands on them.'),
         'samples':len(pts),'octahedral_67_psi':OCT,'golden_67_psi':GOLD,
         'runs':runs,'largest_run':big}
    json.dump(out,open(os.path.join(ROOT,'data','dihedral_family_map.json'),'w'),indent=1)
    print('\nwritten data/dihedral_family_map.json')

if __name__=='__main__':
    main()
