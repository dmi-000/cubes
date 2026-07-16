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
def J2(xi):
    J=np.zeros((2,3)); h=1e-7
    for k in range(3):
        e=np.zeros(3); e[k]=h
        J[:,k]=(sg(expso3(xi+e)@S0,REPS2)-sg(expso3(xi-e)@S0,REPS2))/(2*h)
    return J
def corrector(xi,t,c):
    # solve REPS2=0 and t.xi=c
    for it in range(60):
        F=np.append(sg(expso3(xi)@S0,REPS2), t@xi-c)
        if np.abs(F).max()<1e-14: return xi,True
        A=np.vstack([J2(xi),t])
        xi=xi-np.linalg.solve(A,F)
    return xi,np.abs(F).max()<1e-10
def g3(xi): return sg(expso3(xi)@S0,[P3])[0]

# start on curve
xi=np.zeros(3)
for it in range(60):
    F=sg(expso3(xi)@S0,REPS2)
    if np.abs(F).max()<1e-14: break
    xi=xi-np.linalg.pinv(J2(xi))@F
prev=None; h=0.004; pts=[(xi.copy(),g3(xi))]
for n in range(400):
    t=np.linalg.svd(J2(xi))[2][2]
    if prev is not None and t@prev<0: t=-t
    prev=t
    pred=xi+h*t
    xi2,ok=corrector(pred.copy(),t,t@pred)
    if not ok:
        h*=0.5
        if h<1e-5: print("step collapse at n",n); break
        continue
    xi=xi2; pts.append((xi.copy(),g3(xi)))
vals=[v for _,v in pts]
print("g3 range along curve:",min(vals),max(vals),"  points:",len(pts))
# every sign change
sols=[]
for (xa,va),(xb,vb) in zip(pts,pts[1:]):
    if va*vb<0:
        a,b,fa=xa.copy(),xb.copy(),va
        tloc=np.linalg.svd(J2(a))[2][2]
        for _ in range(70):
            c=tloc@((a+b)/2)
            m,ok=corrector(((a+b)/2).copy(),tloc,c)
            vm=g3(m)
            if vm*fa>0: a=m
            else: b=m
        sols.append(m.copy())
        print(f"zero at |xi|={np.rad2deg(np.linalg.norm(m)):.4f} deg, g3={g3(m):+.2e}")
np.save("edge_close_sols.npy",np.array(sols))

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
for k,x in enumerate(sols):
    MT=expso3(x)@S0
    nm=near_misses(MT,0.05)
    ex=len([y for y in nm if y[0]<1e-9]); gh=sorted(y[0] for y in nm if y[0]>=1e-9)
    print(f"\nsol {k}: exact crossings={ex} next ghosts={['%.4f'%y for y in gh[:3]]}")
    print(repr(MT)); print("quat:",mat2quat(MT))
