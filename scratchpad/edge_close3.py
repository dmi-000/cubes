import numpy as np, itertools

C = np.array([[0,0,1],[1,0,0],[0,1,0]],float)
c=np.cos(np.pi/4); s=np.sin(np.pi/4)
Rx45=np.array([[1,0,0],[0,c,-s],[0,s,c]])
delta=np.deg2rad(40.3060)
AX=np.array([-0.442177,-0.828653,0.343239]); AX/=np.linalg.norm(AX)
def rot(axis,th):
    axis=np.asarray(axis,float); n=np.linalg.norm(axis)
    if n<1e-18: return np.eye(3)
    axis=axis/n
    K=np.array([[0,-axis[2],axis[1]],[axis[2],0,-axis[0]],[-axis[1],axis[0],0]])
    return np.eye(3)+np.sin(th*n if False else th)*K+(1-np.cos(th))*(K@K)
def expso3(xi):
    th=np.linalg.norm(xi)
    if th<1e-18: return np.eye(3)
    return rot(xi/th,th)
S0 = rot(AX,0.5*delta)@Rx45

EDGES=[]
for a in range(3):
    o=[i for i in range(3) if i!=a]
    for s1,s2 in itertools.product([-1,1],repeat=2):
        cvec=np.zeros(3); cvec[o[0]]=s1; cvec[o[1]]=s2
        d=np.zeros(3); d[a]=1.0
        EDGES.append((cvec,d))

# representatives: class A = cubes(0,1) edges(5,4); class B = cubes(0,1) edges(8,8)
REPS=[(0,1,5,4),(0,1,8,8)]
def signed_gaps(M):
    mats=[M,C@M,C@C@M]; out=[]
    for i,j,ei,ej in REPS:
        c1,d1=EDGES[ei]; c2,d2=EDGES[ej]
        C1,D1=mats[i]@c1,mats[i]@d1; C2,D2=mats[j]@c2,mats[j]@d2
        n=np.cross(D1,D2)
        out.append((C2-C1)@n/np.linalg.norm(n))
    return np.array(out)

def seg_gap(c1,d1,c2,d2):
    w=c1-c2; b=d1@d2; f=w@d1; g=w@d2; den=1-b*b
    t1=np.clip((b*g-f)/den,-1,1) if abs(den)>1e-14 else 0.0
    t2=np.clip(b*t1+g,-1,1); t1=np.clip(b*t2-f,-1,1)
    return np.linalg.norm(c1+t1*d1-(c2+t2*d2)),t1,t2

def near_misses(M,tol=0.02):
    mats=[M,C@M,C@C@M]; out=[]
    for i in range(3):
        for j in range(i+1,3):
            for ei,(c1,d1) in enumerate(EDGES):
                for ej,(c2,d2) in enumerate(EDGES):
                    g,t1,t2=seg_gap(mats[i]@c1,mats[i]@d1,mats[j]@c2,mats[j]@d2)
                    if g<tol and abs(t1)<0.999 and abs(t2)<0.999:
                        out.append((g,i,j,ei,ej))
    return sorted(out)

# Newton with pseudoinverse (min-norm step): close both classes
def solve(xi0):
    xi=xi0.copy()
    for it in range(60):
        M=expso3(xi)@S0
        F=signed_gaps(M)
        if np.abs(F).max()<1e-14: break
        J=np.zeros((2,3)); h=1e-7
        for k in range(3):
            e=np.zeros(3); e[k]=h
            J[:,k]=(signed_gaps(expso3(xi+e)@S0)-signed_gaps(expso3(xi-e)@S0))/(2*h)
        xi=xi-np.linalg.pinv(J)@F
    return xi,F

xi,F=solve(np.zeros(3))
M=expso3(xi)@S0
print("residual signed gaps:",F)
print("perturbation angle (deg):",np.rad2deg(np.linalg.norm(xi)))
print("perturbation axis:",xi/np.linalg.norm(xi))
nm=near_misses(M,0.02)
exact=[x for x in nm if x[0]<1e-9]; ghost=[x for x in nm if x[0]>=1e-9]
print(f"exact crossings: {len(exact)}   remaining ghosts <0.02: {len(ghost)}")
for g,i,j,ei,ej in ghost: print(f"   ghost gap={g:.6f} cubes({i},{j}) edges({ei},{ej})")
print("solution matrix M:"); print(M)
np.save("edge_close_M.npy",M); np.save("edge_close_xi.npy",xi)

# trace the 1-parameter solution curve: fix residual=0, move along null direction
print("\n--- curve exploration: null-space walk, both classes held at 0 ---")
def tangent(xi):
    J=np.zeros((2,3)); h=1e-7
    for k in range(3):
        e=np.zeros(3); e[k]=h
        J[:,k]=(signed_gaps(expso3(xi+e)@S0)-signed_gaps(expso3(xi-e)@S0))/(2*h)
    _,_,V=np.linalg.svd(J); return V[2]
cur=xi.copy(); step=0.01
for n in range(12):
    cur=cur+step*tangent(cur)
    cur,Fc=solve(cur)      # re-project onto the solution curve
    Mc=expso3(cur)@S0
    nmc=near_misses(Mc,0.05)
    ex=len([x for x in nmc if x[0]<1e-9])
    # distance from slide path & smallest other ghost
    others=sorted(x[0] for x in nmc if x[0]>=1e-9)
    print(f" s={0.01*(n+1):.2f} |xi|={np.rad2deg(np.linalg.norm(cur)):6.3f}deg exact={ex} next-gaps={['%.4f'%o for o in others[:3]]}")
