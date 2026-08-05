#!/usr/bin/env python3
"""Tangent space from the TIGHT Step-A conditions, not from concurrences.

multicube2.py solved the wall/concurrence conditions and failed its own control:
most concurrences do not change the count, so treating each as binding drove the
rank to nearly full and no tangent survived.  The conditions that DO determine
the count are Step A's: a slab is nonempty iff ||n||_1 > 1, and two slabs meet
iff min over lambda of ||l n_i + (1-l) n_j||_1 > 1.  A STRICT inequality
constrains nothing -- it stays strict under perturbation.  Only the ones holding
with EQUALITY bind, and the tangent space is the null space of their gradients.
"""
import itertools, math
import numpy as np

def mat(c):
    x,y,z=c; n=1+x*x+y*y+z*z
    return np.array([[1+x*x-y*y-z*z,2*(x*y-z),2*(x*z+y)],
                     [2*(x*y+z),1-x*x+y*y-z*z,2*(y*z-x)],
                     [2*(x*z-y),2*(y*z+x),1-x*x-y*y+z*z]])/n

def normals(Ri,Rj):
    """face normals of cube j seen in cube i's frame"""
    R=Ri.T@Rj
    out=[]
    for k in range(3):
        v=R[:,k]; out.append(v); out.append(-v)
    return out

def l1(v): return float(np.abs(v).sum())

def maxmin(a,b):
    cands=[0.0,1.0]
    for k in range(3):
        d=a[k]-b[k]
        if abs(d)>1e-14:
            t=-b[k]/d
            if 0<t<1: cands.append(t)
    return min(l1(t*a+(1-t)*b) for t in cands)

def quantities(Rs):
    """every Step-A quantity for every ordered pair; count is fixed by these"""
    q=[]
    n=len(Rs)
    for i,j in itertools.permutations(range(n),2):
        N=normals(Rs[i],Rs[j])
        for k in range(6): q.append(l1(N[k]))
        for a,b in itertools.combinations(range(6),2):
            if a^1==b: continue
            q.append(maxmin(N[a],N[b]))
    return np.array(q)

def tangent(cays,label,fixed0=True):
    npar=3*(len(cays)-1)
    def build(p):
        cs=[list(cays[0])]+[[cays[i][j]+p[3*(i-1)+j] for j in range(3)] for i in range(1,len(cays))]
        return [mat(c) for c in cs]
    q0=quantities(build(np.zeros(npar)))
    tight=[i for i,v in enumerate(q0) if abs(v-1.0)<1e-9]
    J=np.zeros((len(tight),npar)); h=1e-7
    for k in range(npar):
        e=np.zeros(npar); e[k]=h
        qp=quantities(build(e)); qm=quantities(build(-e))
        J[:,k]=(qp[tight]-qm[tight])/(2*h)
    if len(tight)==0:
        print('%-26s no tight conditions -> tangent space is everything'%label); return
    sv=np.linalg.svd(J,compute_uv=False)
    rank=int((sv>1e-6*max(sv[0],1e-30)).sum())
    U,S,Vt=np.linalg.svd(J)
    null=[Vt[i] for i in range(npar) if i>=len(S) or S[i]<=1e-6*max(S[0],1e-30)]
    print('%-26s %d quantities, %d TIGHT, rank %d -> tangent dim %d'
          %(label,len(q0),len(tight),rank,len(null)))
    for v in null[:3]:
        v=v/np.max(np.abs(v))
        print('%-26s   direction %s'%('',np.array2string(v,precision=4,suppress_small=True)))

if __name__=='__main__':
    print('--- CONTROL: n=2 mirror-plane 13, known tangent (1,1,0) ---')
    tangent([[0.,0.,0.],[-12.,-11.,0.]],'n=2 at (-12,-11,0)')
    print()
    print('--- the two 67s ---')
    r2=math.sqrt(2)
    # R = quaternion (1,1,r2,0) -> Cayley (1, r2, 0); R^2 -> Cayley of (-1,1,r2,0)
    def cay(q):
        w,x,y,z=q; return [x/w,y/w,z/w]
    tangent([[0.,0.,0.],cay((1,1,r2,0)),cay((-1,1,r2,0))],'octahedral 67, Q(sqrt2)')
    r5=math.sqrt(5)
    tangent([[0.,0.,0.],cay((2,1+r5,-1+r5,0)),cay((-2,1+r5,-1+r5,0))],'golden 67, Q(sqrt5)')
