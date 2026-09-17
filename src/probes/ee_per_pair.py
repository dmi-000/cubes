import os
"""Is EE <= 6 per pair of concentric congruent cubes?  [OQ 35]'s lead.

DERIVATION: an edge-edge contact is a point on two facets of each cube -- 4 equations in 3
unknowns, codimension 1, so one condition on R in SO(3).  Central symmetry pairs contacts, so
each antipodal pair costs one condition, and SO(3) is 3-dimensional: at most 3 independent
conditions, hence at most 3 pairs, hence EE <= 6.  It fails only if the conditions become
DEPENDENT on a special locus -- which is what this searches for.
"""
import sys, os, json, collections, random, itertools
from fractions import Fraction as F
from math import gcd
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from step_a2 import mat
from c_level import shares_plane
SG=[(a,b,c) for a in(1,-1) for b in(1,-1) for c in(1,-1)]
def edges(M):
    """the 12 edges as (point, direction), exact, for the cube with rotation rows M"""
    out=[]
    cols=[[M[r][c] for r in range(3)] for c in range(3)]   # face normals are the COLUMNS
    for k in range(3):
        o=[j for j in range(3) if j!=k]
        for s0 in (1,-1):
            for s1 in (1,-1):
                p=[s0*cols[o[0]][z]+s1*cols[o[1]][z] for z in range(3)]
                out.append((p,[cols[k][z] for z in range(3)]))
    return out
def det3(a,b,c): return (a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0]))
def contacts(q):
    M0=[[F(1) if r==c else F(0) for c in range(3)] for r in range(3)]
    M1=[[F(x) for x in row] for row in mat(q)]
    E0=edges(M0); E1=edges(M1); n=0
    for (a,u) in E0:
        for (b,v) in E1:
            d=[b[z]-a[z] for z in range(3)]
            if det3(u,v,d)!=0: continue                 # not coplanar: no meeting
            # solve a + s u = b + t v  in the plane
            best=None
            for (i,j) in ((0,1),(0,2),(1,2)):
                den=u[i]*(-v[j])-u[j]*(-v[i])
                if den==0: continue
                s=(d[i]*(-v[j])-d[j]*(-v[i]))/den
                t=(u[i]*d[j]-u[j]*d[i])/den
                best=(s,t); break
            if best is None: continue
            s,t=best
            if abs(s)<=1 and abs(t)<=1: n+=1
    return n
rng=random.Random(7); hist=collections.Counter(); worst=(0,None)
cands=[]
for w in range(0,7):
    for x in range(0,7):
        for y in range(0,7):
            for z in range(0,7):
                if (w,x,y,z)!=(0,0,0,0) and gcd(gcd(w,x),gcd(y,z))==1: cands.append((w,x,y,z))
for q in cands:
    # EXCLUDE the degeneracy the project always excludes: two cubes sharing a face plane.
    # The unfiltered maximum was 48 at q = (0,0,0,1), a 180-degree rotation that maps the cube
    # to ITSELF -- coincident cubes, where every edge meets its own image.
    if shares_plane([(1,0,0,0),q]): continue
    c=contacts(q); hist[c]+=1
    if c>worst[0]: worst=(c,q)
print('pairs tested: %d  (all coprime integer quaternions with entries 0..6)'%len(cands))
print('edge-edge contact counts:',dict(sorted(hist.items())))
print('MAX EE per pair: %d   at q=%s'%worst)
json.dump({'what':'edge-edge contacts per pair of concentric cubes','tested':len(cands),
           'distribution':{str(k):v for k,v in hist.items()},'max':worst[0],'argmax':list(worst[1])},
          open('/Users/dmi/cube-compounds/data/ee_per_pair.json','w'),indent=1)
