import numpy as np, itertools
exec(open("edge_close4.py").read().split("# locate s=0.06")[0])
REPS2=[(0,1,5,4),(0,1,8,8)]; P3=(0,2,0,9)
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
        if np.abs(F).max()<1e-15: break
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
def g3(xi): return sg(expso3(xi)@S0,[P3])[0]

# identical deterministic scan to edge_close7
cur,_=solve(np.zeros(3),REPS2); prev=None; pts=[]
for n in range(80):
    t=tangent(cur,REPS2)
    if prev is not None and t@prev<0: t=-t
    prev=t
    cur,_=solve(cur+0.002*t,REPS2)
    pts.append((cur.copy(),g3(cur),t.copy()))
brackets=[(a,b) for a,b in zip(pts,pts[1:]) if a[1]*b[1]<0]
print("sign-change brackets:",len(brackets))
sols=[]
for (xa,va,ta),(xb,vb,tb) in brackets:
    a,b=xa.copy(),xb.copy()
    for _ in range(80):
        m,_=solve((a+b)/2,REPS2)   # min-norm projection back to curve
        vm=g3(m)
        if abs(vm)<1e-15: break
        if vm*g3(a)>0: a=m
        else: b=m
    xiT,_=solve(m,REPS2+[P3])
    F=sg(expso3(xiT)@S0,REPS2+[P3])
    sols.append(xiT)
    print("residuals:",F," |xi|deg:",np.rad2deg(np.linalg.norm(xiT)))

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
                        out.append((g,i,j,ei,ej))
    return sorted(out)
def mat2quat(R):
    w=np.sqrt(max(0,1+R[0,0]+R[1,1]+R[2,2]))/2
    return np.array([w,(R[2,1]-R[1,2])/(4*w),(R[0,2]-R[2,0])/(4*w),(R[1,0]-R[0,1])/(4*w)])
for k,xiT in enumerate(sols):
    MT=expso3(xiT)@S0
    nm=near_misses(MT,0.05)
    ex=[x for x in nm if x[0]<1e-9]; gh=sorted(x[0] for x in nm if x[0]>=1e-9)
    print(f"\nsolution {k}: exact={len(ex)} nextghosts={['%.4f'%x for x in gh[:3]]}")
    print(repr(MT)); print("quat:",mat2quat(MT))
    np.save(f"edge_close_MT{k}.npy",MT)

# diagnostic: print the g3 trajectory of this scan
print("\ntrajectory:")
for n,(x,v,t) in enumerate(pts):
    if n%4==0: print(f" {n:3d}  |xi|={np.rad2deg(np.linalg.norm(x)):6.3f}  g3={v:+.6f}")
