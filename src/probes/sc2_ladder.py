#!/usr/bin/env python3
"""SC2 = 10 is INFEASIBLE: imposing five corner-sharings FORCES the sixth.  [P351]

Continuing [P350]. The corner-sharing graph on four cubes with five edges is K4 minus an edge,
here minus (0,1); degrees (2,2,3,3). Solving the axis system as in [P334]:

    cube 3 standard, axes a, b, c to partners 0, 1, 2
    unknowns  y = l20,  z = l21
    |<a,y>| = |<c,y>| = 1/3 ,  |<b,z>| = |<c,z>| = 1/3 ,  |<y,z>| = 1/3

Two branches survive, e.g. `y = (p,0,q)`, `z = (0,q,-p)` with the SAME
`p, q = (sqrt3 +- sqrt15)/6`. Building the four cubes from those axes and then reading the
sharing structure back off the DIAGONALS:

    imposed   (0,2), (0,3), (1,2), (1,3), (2,3)      five
    realised  (0,1), (0,2), (0,3), (1,2), (1,3), (2,3)   SIX

**The pair (0,1) is never imposed and appears anyway.** So `SC2 = 10` does not exist: the graph
jumps from four sharings (the paw, [P350]) straight to six.

AND THE RESULT IS THE GOLDEN 177, re-derived. Its census here is
`{(1,1,1): 56, (1,1,1,1): 18, (2,2): 36, (3,3): 12}` -- identical to [P342]'s, reached from a
five-edge graph rather than from the A4 symmetry argument. Two independent derivations of the
same compound, which is the control [P342] did not have.
"""
import sys, itertools, collections
from fractions import Fraction as F
sys.path.insert(0,'src'); sys.path.insert(0,'src/probes')
s=open('/private/tmp/claude-502/-Users-dmi-cube-compounds/43a2fe45-06f5-4be7-aa71-da540c168dea/scratchpad/paw2.py').read()
exec(s[:s.index('a=[t3,t3,t3]')])          # helpers: dot, sm, add, cross, tet2, normals, qrot, ...
exec(s[s.index('def solve3('):s.index('print()\nprint(\'%-10s')])   # solve3, facets, census

a=[t3,t3,t3]; b=[t3,t3,-t3]; c=[t3,-t3,t3]
y=[P,K(0),Q]; z=[K(0),Q,-P]
C3=[[K(1),K(0),K(0)],[K(0),K(1),K(0)],[K(0),K(0),K(1)]]
C0=normals(tet2(a,y))
C1=normals(tet2(b,z))

def tet3(u1,u2,u3):
    """tetrahedron from THREE axes: sign them to pairwise -1/3, 4th is -(sum)"""
    M13=K(F(-1,3))
    for s1 in (1,-1):
        for s2 in (1,-1):
            for s3 in (1,-1):
                v=[sm(s1,u1),sm(s2,u2),sm(s3,u3)]
                if all(dot(v[m],v[n])==M13 for m,n in itertools.combinations(range(3),2)):
                    d4=sm(-1,add(add(v[0],v[1]),v[2]))
                    assert dot(d4,d4)==K(1)
                    return v+[d4]
    return None
t=tet3(c,y,z)
assert t is not None, 'cube 2 does not close'
C2=normals(t)
print('all four cubes built exactly; SC2 target = 10 (five sharings, K4 minus edge (0,1))')
sig,pts=census([C0,C1,C2,C3])
EE=sig.get((2,2),0); SC=sig.get((3,3),0); T3=sig.get((1,1,1),0)
Qg=sig.get((1,1,1,1),0); Q4=sum(v for k,v in sig.items() if len(k)==4)
tb=EE+2*SC; Bv=T3+4*Qg
print('   census:',{str(k):v for k,v in sorted(sig.items())})
print()
print('%-18s %4s %4s %5s %3s %9s %5s %5s'%('configuration','EE','SC2','T3','Q4','two-body','B','obj'))
for lbl,e,s2,t3v,q in [('n=4 RECORD',36,6,128,0),('PAW [P350]',24,8,128,0),
                       ('K4-minus-edge',EE,SC,T3,Q4),('K4 [P334]',36,12,74,0)]:
    print('%-18s %4d %4d %5d %3d %9d %5d %5d'%(lbl,e,s2,t3v,q,e+2*s2,t3v,e+2*s2+t3v-q))
