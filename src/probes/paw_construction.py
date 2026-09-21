#!/usr/bin/env python3
"""THE PAW: SC2 = 8 on DISTINCT corners with B = 128 -- constructed, and it still loses.  [P350]

Corner-sharing graph = the PAW: edges (3,0), (3,1), (3,2), (0,1).  Two cubes share a corner iff
they share a body-diagonal DIRECTION, and the axes at each cube must extend to a regular
tetrahedron.  Cube 3 supplies a, b, c; cubes 0 and 1 also share x with |<x,a>| = |<x,b>| = 1/3 --
the system [P334] solved -- so x = (p, q, 0), p, q = (sqrt3 +- sqrt15)/6.  Cube 2 is constrained
only by c, leaving the free parameter Rot((1,-1,1), psi).

    configuration    EE  SC2    T3  Q4   two-body     B   objective
    n = 4 RECORD     36    6   128   0         48   128       176
    PAW (this)       24    8   128   0         40   128       168

The target is MET and the objective still falls short: the fourth corner-sharing costs 12
edge-edge contacts to gain 4 in two-body, NET -8, with B untouched.

[P358] later explains why the paw keeps Q4 = 0: its cube 2 has only ONE shared axis, so it
retains a free rotation, and a 4-fold coincidence is codimension 1 in that rotation.  Measured
over 36 values of psi: Q4 = {0: 33, 2: 2, 32: 1}.

CONTAINMENT, fourth occurrence ([FAILURE_MODES 38], [FAILURE_MODES 44]).  The first census
returned EE = 0 and SC2 = 0 for a construction that FORCES four corner-sharings, because the
facet test discarded points outside any cube -- and a shared corner sits at distance sqrt3,
outside the others by construction.
"""
import sys, itertools, collections
from fractions import Fraction as F
sys.path.insert(0,'src'); sys.path.insert(0,'src/probes')
from kfield import K
R3=K(0,1,0,0); R15=K(0,0,0,1)
P=(R3+R15)*K(F(1,6)); Q=(R3-R15)*K(F(1,6)); t3=R3*K(F(1,3))
def dot(u,v): return u[0]*v[0]+u[1]*v[1]+u[2]*v[2]
def sm(s,u): return [K.lift(s)*t for t in u]
def add(u,v): return [u[i]+v[i] for i in range(3)]
def cross(u,v): return [u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]]
M13=K(F(-1,3))

def tet2(u1,u2):
    """regular tetrahedron containing u1 and (a signing of) u2"""
    for s in (1,-1):
        v=sm(s,u2)
        if dot(u1,v)==M13:
            ssum=sm(-1,add(u1,v))
            w=sm(K(F(1,2))*R3, cross(u1,v))          # |w|^2 = (3/4)(8/9) = 2/3
            assert dot(w,w)==K(F(2,3))
            h=[K(F(1,2))*ssum[i] for i in range(3)]
            u3=add(h,w); u4=add(h,sm(-1,w))
            ds=[u1,v,u3,u4]
            for m,n in itertools.combinations(range(4),2):
                assert dot(ds[m],ds[n])==M13, (m,n,dot(ds[m],ds[n]))
            return ds
    return None
def normals(ds):
    half=K(F(1,2))*R3
    N=[sm(half,add(ds[0],ds[k])) for k in (1,2,3)]
    for m,n in itertools.combinations(range(3),2): assert dot(N[m],N[n])==K(0)
    for m in range(3): assert dot(N[m],N[m])==K(1)
    return N
def qrot(w,x,y,z):
    """rotation matrix rows = face normals, from an integer quaternion"""
    w,x,y,z=[K(v) for v in (w,x,y,z)]
    N=w*w+x*x+y*y+z*z; Ni=N.inv()
    M=[[w*w+x*x-y*y-z*z,2*(x*y-w*z),2*(x*z+w*y)],
       [2*(x*y+w*z),w*w-x*x+y*y-z*z,2*(y*z-w*x)],
       [2*(x*z-w*y),2*(y*z+w*x),w*w-x*x-y*y+z*z]]
    return [[M[r][c]*Ni for r in range(3)] for c in range(3)]

a=[t3,t3,t3]; b=[t3,t3,-t3]; c=[t3,-t3,t3]; x=[P,Q,K(0)]
# cube 3: standard cube, normals e1,e2,e3
C3=[[K(1),K(0),K(0)],[K(0),K(1),K(0)],[K(0),K(0),K(1)]]
C0=normals(tet2(a,x))
C1=normals(tet2(b,x))
print('cubes 0,1,3 built exactly; cube 2 = Rot((1,-1,1),psi) is the free parameter')

def solve3(rows,rhs):
    A=rows
    det=(A[0][0]*(A[1][1]*A[2][2]-A[1][2]*A[2][1])-A[0][1]*(A[1][0]*A[2][2]-A[1][2]*A[2][0])
         +A[0][2]*(A[1][0]*A[2][1]-A[1][1]*A[2][0]))
    if det.is_zero(): return None
    out=[]
    for i in range(3):
        B=[r[:] for r in A]
        for k in range(3): B[k][i]=rhs[k]
        d=(B[0][0]*(B[1][1]*B[2][2]-B[1][2]*B[2][1])-B[0][1]*(B[1][0]*B[2][2]-B[1][2]*B[2][0])
           +B[0][2]*(B[1][0]*B[2][1]-B[1][1]*B[2][0]))
        out.append(d/det)
    return out
def facets(M,p):
    """(is p in the CLOSED cube?, how many facets pass through it).
    A vertex lies on the facets of its OWN cubes and may be OUTSIDE the others -- discarding
    points outside any cube kills every (3,3) shared corner, which sits at distance sqrt3.
    FAILURE_MODES 38, fourth occurrence."""
    cnt=0
    for r in range(3):
        h=dot(M[r],p)
        if h==K(1) or h==K(-1): cnt+=1; continue
        if (K(1)-h).sign()<0 or (K(1)+h).sign()<0: return False,0
    return True,cnt
def census(CUBES):
    planes=[]
    for ci,M in enumerate(CUBES):
        for r in range(3):
            for s in (1,-1): planes.append((ci,sm(s,M[r])))
    pts={}
    for t in itertools.combinations(range(len(planes)),3):
        if len({planes[i][0] for i in t})<2: continue
        rows=[planes[i][1] for i in t]
        p=solve3(rows,[K(1)]*3)
        if p is None: continue
        key=tuple((v.a,v.b,v.c,v.d) for v in p)
        if key in pts: continue
        sig=[]
        for M in CUBES:
            good,f=facets(M,p)
            if good and f: sig.append(f)
        if len(sig)>=2 and sum(sig)>=3: pts[key]=tuple(sorted(sig))
    return collections.Counter(pts.values()), pts

def _scan():
    print()
    print('%-10s %-30s %6s %5s %5s %4s %4s %5s'%('psi (w:k)','signatures','two-body','T3','Q4g','Q4','B','obj'))
    best=None
    for w in range(0,7):
        for k in range(1,7):
            from math import gcd
            if gcd(w,k)!=1: continue
            C2=qrot(w,k,-k,k)
            try: sig,_=census([C0,C1,C2,C3])
            except AssertionError: continue
            EE=sig.get((2,2),0); SC=sig.get((3,3),0); T3=sig.get((1,1,1),0)
            Qg=sig.get((1,1,1,1),0); Q4=sum(v for kk,v in sig.items() if len(kk)==4)
            tb=EE+2*SC; Bv=T3+4*Qg; obj=tb+Bv-Q4
            if best is None or obj>best[0]: best=(obj,w,k,dict(sig),tb,T3,Qg,Q4,Bv)
            print('%-10s %-30s %6d %5d %5d %4d %4d %5d'%('%d:%d'%(w,k),
                  str({str(a2):b2 for a2,b2 in sorted(sig.items())})[:30],tb,T3,Qg,Q4,Bv,obj))
    print()
    if best: print('BEST objective %d  (record 176)  at psi=(%d:%d)'%(best[0],best[1],best[2]))


if __name__ == "__main__":
    _scan()
