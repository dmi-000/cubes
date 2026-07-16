import numpy as np, itertools
exec(open("edge_close4.py").read().split("# locate s=0.06")[0])
REPS2=[(0,1,5,4),(0,1,8,8)]; P3=(0,2,0,9)
REPS3=REPS2+[P3]
def sg(M,reps):
    mats=[M,C@M,C@C@M]; out=[]
    for i,j,ei,ej in reps:
        c1,d1=EDGES[ei]; c2,d2=EDGES[ej]
        n=np.cross(mats[i]@d1,mats[j]@d2)
        out.append((mats[j]@c2-mats[i]@c1)@n/np.linalg.norm(n))
    return np.array(out)
def solve(xi0,reps,maxstep=0.01):
    xi=xi0.copy()
    for it in range(200):
        F=sg(expso3(xi)@S0,reps)
        if np.abs(F).max()<1e-15: break
        J=np.zeros((len(reps),3)); h=1e-7
        for k in range(3):
            e=np.zeros(3); e[k]=h
            J[:,k]=(sg(expso3(xi+e)@S0,reps)-sg(expso3(xi-e)@S0,reps))/(2*h)
        step=-np.linalg.pinv(J)@F
        nrm=np.linalg.norm(step)
        if nrm>maxstep: step*=maxstep/nrm
        xi=xi+step
    return xi,sg(expso3(xi)@S0,reps)
def tangent(xi,reps):
    J=np.zeros((len(reps),3)); h=1e-7
    for k in range(3):
        e=np.zeros(3); e[k]=h
        J[:,k]=(sg(expso3(xi+e)@S0,reps)-sg(expso3(xi-e)@S0,reps))/(2*h)
    return np.linalg.svd(J)[2][2]
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

# regenerate the curve to s=0.105 then damped 3-solve
xi,_=solve(np.zeros(3),REPS2,maxstep=0.05)
prev=None
best=None
for n in range(80):
    t=tangent(xi,REPS2)
    if prev is not None and t@prev<0: t=-t
    prev=t
    xi,_=solve(xi+0.002*t,REPS2,maxstep=0.02)
    v=sg(expso3(xi)@S0,[P3])[0]
    if best is None or abs(v)<abs(best[1]): best=(xi.copy(),v)
xi0,v0=best
print("start |g3|:",abs(v0)," |xi| deg:",np.rad2deg(np.linalg.norm(xi0)))
xiT,F=solve(xi0,REPS3,maxstep=0.005)
MT=expso3(xiT)@S0
print("residuals:",F," |xi| deg:",np.rad2deg(np.linalg.norm(xiT)))
nm=near_misses(MT,0.05)
ex=[x for x in nm if x[0]<1e-9]; gh=sorted(x[0] for x in nm if x[0]>=1e-9)
print(f"exact crossings: {len(ex)}  next ghosts: {['%.4f'%x for x in gh[:4]]}")
print(repr(MT)); np.save("edge_close_MT.npy",MT); np.save("edge_close_xiT.npy",xiT)
def mat2quat(R):
    w=np.sqrt(max(0,1+R[0,0]+R[1,1]+R[2,2]))/2
    return np.array([w,(R[2,1]-R[1,2])/(4*w),(R[0,2]-R[2,0])/(4*w),(R[1,0]-R[0,1])/(4*w)])
print("quat:",mat2quat(MT))
# distances to endpoints
delta=np.deg2rad(40.3060)
for name,E in [("oct t=0",Rx45),("golden t=1",rot(AX,delta)@Rx45),("mid t=0.5",S0)]:
    Rrel=MT@E.T; print(f"rot dist from {name}: {np.rad2deg(np.arccos(np.clip((np.trace(Rrel)-1)/2,-1,1))):.3f} deg")
