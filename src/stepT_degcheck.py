import numpy as np
def facet(nx,ny,nz,h):
    n=np.array([nx,ny,nz],float); nn=np.linalg.norm(n); return (n/nn,h/nn)
rho=1.0; mu=1.0; g=3.0; s=0.5; L=6.0; W=6.0
B=[facet(g,0,mu,1.0),facet(-g,0,mu,1.0),facet(0,1,0,W),facet(0,-1,0,W),facet(0,0,-1,L)]
C=[facet(0,g,mu,1.0),facet(0,-g,mu,1.0),facet(1,0,0,W),facet(-1,0,0,W),facet(0,0,-1,L)]
A=[]
for phi in (90,210,330):
    r=np.deg2rad(phi); A.append(facet(s*np.cos(r),s*np.sin(r),mu,1.0))
A.append(facet(0,0,-1,L))
cells=[A,B,C]
def reach(F,u):           # r=max t: t u in cell => min over facets of h/(n.u) for n.u>0
    t=np.inf
    for (n,h) in F:
        d=n@u
        if d>1e-12: t=min(t,h/d)
    return t
# sample a small circle of directions around u0=(0,0,1)
u0=np.array([0,0,1.0]); e1=np.array([1,0,0.0]); e2=np.array([0,1,0.0])
eps=1e-3
seq=[]
Nn=3600
for k in range(Nn):
    a=2*np.pi*k/Nn
    u=u0+eps*(np.cos(a)*e1+np.sin(a)*e2); u=u/np.linalg.norm(u)
    r=[reach(F,u) for F in cells]
    seq.append(int(np.argmax(r)))   # farthest cell = top diagram
seq=np.array(seq)
switch=np.sum(seq!=np.roll(seq,1))
# which cells appear
import collections
print('top-diagram (farthest cell) degree around u0 =', switch)
print('cells appearing in top diagram:', sorted(set(seq.tolist())), '(0=A corner,1=B blade,2=C blade)')
# bottom diagram
seqb=[]
for k in range(Nn):
    a=2*np.pi*k/Nn
    u=u0+eps*(np.cos(a)*e1+np.sin(a)*e2); u=u/np.linalg.norm(u)
    r=[reach(F,u) for F in cells]
    seqb.append(int(np.argmin(r)))   # nearest cell = bottom diagram
seqb=np.array(seqb); switchb=np.sum(seqb!=np.roll(seqb,1))
print('bottom-diagram (nearest cell) degree around u0 =', switchb)
print('=> deg_top > deg_bot on REAL 3D cells:', switch>switchb)
