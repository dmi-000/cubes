import numpy as np, itertools
from scipy.optimize import linprog
from scipy.spatial import HalfspaceIntersection, ConvexHull
import warnings; warnings.filterwarnings('ignore')
# correct region counter (n=3, containment overlap-graph) for d1
def feasible(hs):
    A=np.array([h[0] for h in hs]); b=np.array([h[1] for h in hs])
    r=linprog([0,0,0,-1],A_ub=np.hstack([A,np.linalg.norm(A,axis=1,keepdims=True)]),b_ub=b,bounds=[(-50,50)]*3+[(0,10)],method='highs')
    return r.success and r.x[3]>1e-7
def comps(pieces):
    P=[p for p in pieces if feasible(p)];k=len(P);par=list(range(k))
    def f(x):
        while par[x]!=x:par[x]=par[par[x]];x=par[x]
        return x
    for i in range(k):
        for j in range(i+1,k):
            if f(i)!=f(j) and feasible(P[i]+P[j]):par[f(i)]=f(j)
    return len(set(f(i) for i in range(k)))
def outside(F):return [(-np.array(n),-h) for (n,h) in F]
def d1_count(bodies):
    A,B,C=bodies
    return sum(comps([X+[oy]+[oz] for oy in outside(Y) for oz in outside(Z)]) for (X,Y,Z) in [(A,B,C),(B,A,C),(C,A,B)])
def triple_pts(bodies):
    def sols():
        Fs=bodies; pts=[]
        for fa in Fs[0]:
            for fb in Fs[1]:
                for fc in Fs[2]:
                    M=np.array([fa[0],fb[0],fc[0]]);rhs=np.array([fa[1],fb[1],fc[1]])
                    if abs(np.linalg.det(M))<1e-9:continue
                    x=np.linalg.solve(M,rhs)
                    def onb(x,F): # on boundary of body F (all planes<=, at least this one =0 already)
                        return all(n@x-h<=1e-7 for (n,h) in F)
                    if onb(x,Fs[0]) and onb(x,Fs[1]) and onb(x,Fs[2]):
                        if not any(np.linalg.norm(x-p)<1e-6 for p in pts):pts.append(x)
        return len(pts)
    return sols()
def Fcount(P12):
    hs=np.array([[*n,-h] for (n,h) in P12]);norm=np.linalg.norm(hs[:,:-1],axis=1)
    r=linprog([0,0,0,-1],A_ub=np.hstack([hs[:,:-1],norm[:,None]]),b_ub=-hs[:,-1],bounds=[(None,None)]*3+[(0,None)],method='highs')
    if not r.success or r.x[3]<1e-9:return 0
    hi=HalfspaceIntersection(hs,r.x[:3]);V=hi.intersections
    # count distinct facet planes actually used
    used=set()
    for k,(n,h) in enumerate(P12):
        if any(abs(n@v-h)<1e-6 for v in V):used.add(k)
    return len(used)
def cube(R): return [(R[:,a]*s,1.0) for a in range(3) for s in (1,-1)]
def hexa(R,eps,rng):
    return [((R[:,a]*s+eps*rng.standard_normal(3))/np.linalg.norm(R[:,a]*s+eps*rng.standard_normal(3)),1.0+eps*abs(rng.standard_normal())) for a in range(3) for s in (1,-1)]
def Rx(t):c,s=np.cos(t),np.sin(t);return np.array([[1,0,0],[0,c,-s],[0,s,c]])
def Ry(t):c,s=np.cos(t),np.sin(t);return np.array([[c,0,s],[0,1,0],[-s,0,c]])
def Rz(t):c,s=np.cos(t),np.sin(t);return np.array([[c,-s,0],[s,c,0],[0,0,1]])
def check(name,bodies):
    d1=d1_count(bodies); T=triple_pts(bodies)
    contact=2*(d1-2)-T
    SF=sum(2*Fcount(bodies[i]+bodies[j])-4 for (i,j) in [(0,1),(0,2),(1,2)])
    print(f'{name:16s} d1={d1:2d} T={T:2d} contact={contact:3d}  Sum(2F-4)={SF:3d}  contact<=bound? {contact<=SF+1e-6}')
check('octahedral',[cube(Rx(np.pi/4)),cube(Ry(np.pi/4)),cube(Rz(np.pi/4))])
phi=(1+np.sqrt(5))/2;S=np.array([[phi/2,.5,1/(2*phi)],[.5,-1/(2*phi),-phi/2],[-1/(2*phi),phi/2,-.5]])
check('golden',[cube(np.eye(3)),cube(S),cube(S@S)])
rng=np.random.default_rng(3)
def rr():
    A=rng.standard_normal((3,3));Q,_=np.linalg.qr(A);return Q if np.linalg.det(Q)>0 else Q@np.diag([-1.,1,1])
for i in range(6):
    check(f'hexa{i}',[hexa(rr(),0.25,rng) for _ in range(3)])
