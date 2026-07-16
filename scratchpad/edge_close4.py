import numpy as np, itertools

C = np.array([[0,0,1],[1,0,0],[0,1,0]],float)
cq=np.cos(np.pi/4); sq=np.sin(np.pi/4)
Rx45=np.array([[1,0,0],[0,cq,-sq],[0,sq,cq]])
delta=np.deg2rad(40.3060)
AX=np.array([-0.442177,-0.828653,0.343239]); AX/=np.linalg.norm(AX)
def rot(axis,th):
    K=np.array([[0,-axis[2],axis[1]],[axis[2],0,-axis[0]],[-axis[1],axis[0],0]])
    return np.eye(3)+np.sin(th)*K+(1-np.cos(th))*(K@K)
def expso3(xi):
    th=np.linalg.norm(xi)
    return np.eye(3) if th<1e-18 else rot(xi/th,th)
S0=rot(AX,0.5*delta)@Rx45

EDGES=[]
for a in range(3):
    o=[i for i in range(3) if i!=a]
    for s1,s2 in itertools.product([-1,1],repeat=2):
        cvec=np.zeros(3); cvec[o[0]]=s1; cvec[o[1]]=s2
        d=np.zeros(3); d[a]=1.0
        EDGES.append((cvec,d))

def seg_gap(c1,d1,c2,d2):
    w=c1-c2; b=d1@d2; f=w@d1; g=w@d2; den=1-b*b
    t1=np.clip((b*g-f)/den,-1,1) if abs(den)>1e-14 else 0.0
    t2=np.clip(b*t1+g,-1,1); t1=np.clip(b*t2-f,-1,1)
    return np.linalg.norm(c1+t1*d1-(c2+t2*d2)),t1,t2

def near_misses(M,tol):
    mats=[M,C@M,C@C@M]; out=[]
    for i in range(3):
        for j in range(i+1,3):
            for ei,(c1,d1) in enumerate(EDGES):
                for ej,(c2,d2) in enumerate(EDGES):
                    g,t1,t2=seg_gap(mats[i]@c1,mats[i]@d1,mats[j]@c2,mats[j]@d2)
                    if g<tol and abs(t1)<0.999 and abs(t2)<0.999:
                        out.append((g,i,j,ei,ej,t1,t2))
    return sorted(out)

# locate s=0.06 point from previous run by redoing the walk quickly
REPS2=[(0,1,5,4),(0,1,8,8)]
def sg(M,reps):
    mats=[M,C@M,C@C@M]; out=[]
    for i,j,ei,ej in reps:
        c1,d1=EDGES[ei]; c2,d2=EDGES[ej]
        n=np.cross(mats[i]@d1,mats[j]@d2)
        out.append((mats[j]@c2-mats[i]@c1)@n/np.linalg.norm(n))
    return np.array(out)
def solve(xi0,reps):
    xi=xi0.copy()
    for it in range(80):
        F=sg(expso3(xi)@S0,reps)
        if np.abs(F).max()<1e-14: break
        J=np.zeros((len(reps),3)); h=1e-7
        for k in range(3):
            e=np.zeros(3); e[k]=h
            J[:,k]=(sg(expso3(xi+e)@S0,reps)-sg(expso3(xi-e)@S0,reps))/(2*h)
        xi=xi-np.linalg.pinv(J)@F
    return xi,F
def tangent(xi,reps):
    J=np.zeros((len(reps),3)); h=1e-7
    for k in range(3):
        e=np.zeros(3); e[k]=h
        J[:,k]=(sg(expso3(xi+e)@S0,reps)-sg(expso3(xi-e)@S0,reps))/(2*h)
    return np.linalg.svd(J)[2][2]

xi,_=solve(np.zeros(3),REPS2)
cur=xi.copy()
for n in range(6):
    cur=cur+0.01*tangent(cur,REPS2); cur,_=solve(cur,REPS2)
M6=expso3(cur)@S0
nm=near_misses(M6,0.001)
third=[x for x in nm if x[0]>1e-9]
print("third-class members near closing at s=0.06:")
for g,i,j,ei,ej,t1,t2 in third[:4]: print(f"  gap={g:.6f} cubes({i},{j}) edges({ei},{ej})")
rep3=(third[0][1],third[0][2],third[0][3],third[0][4])
REPS3=REPS2+[rep3]
xi3,F3=solve(cur,REPS3)
M3=expso3(xi3)@S0
print("\n3-condition solve residuals:",F3)
print("|xi| from slide midpoint (deg):",np.rad2deg(np.linalg.norm(xi3)))
nm3=near_misses(M3,0.05)
ex=[x for x in nm3 if x[0]<1e-9]; gh=[x for x in nm3 if x[0]>=1e-9]
print(f"exact crossings: {len(ex)}   ghosts<0.05: {len(gh)}, min ghost gap:",min([g[0] for g in gh],default=None))
print("matrix:"); print(repr(M3))
np.save("edge_close_M3.npy",M3); np.save("edge_close_xi3.npy",xi3)

# how far is this from the two 67 endpoints and from the midpoint config?
Send=[rot(AX,0.0)@Rx45, rot(AX,delta)@Rx45]
for name,E in [("oct end t=0",Send[0]),("golden end t=1",Send[1]),("midpoint t=0.5",S0)]:
    Rrel=M3@E.T; angdeg=np.rad2deg(np.arccos(np.clip((np.trace(Rrel)-1)/2,-1,1)))
    print(f"rotation distance from {name}: {angdeg:.3f} deg")
# quaternion of M3 for identification
def mat2quat(R):
    w=np.sqrt(max(0,1+R[0,0]+R[1,1]+R[2,2]))/2
    x=(R[2,1]-R[1,2])/(4*w); y=(R[0,2]-R[2,0])/(4*w); z=(R[1,0]-R[0,1])/(4*w)
    return np.array([w,x,y,z])
q=mat2quat(M3); print("quaternion:",q, " normalized ratios x/w y/w z/w:", q[1]/q[0],q[2]/q[0],q[3]/q[0])
