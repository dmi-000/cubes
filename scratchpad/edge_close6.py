import numpy as np, itertools
exec(open("edge_close4.py").read().split("# locate s=0.06")[0])

REPS2=[(0,1,5,4),(0,1,8,8)]
def sg(M,reps):
    mats=[M,C@M,C@C@M]; out=[]
    for i,j,ei,ej in reps:
        c1,d1=EDGES[ei]; c2,d2=EDGES[ej]
        n=np.cross(mats[i]@d1,mats[j]@d2)
        out.append((mats[j]@c2-mats[i]@c1)@n/np.linalg.norm(n))
    return np.array(out)
def solve(xi0,reps,extra=None):
    # solve reps=0 (and optionally pin arclength via extra plane)
    xi=xi0.copy()
    for it in range(100):
        F=sg(expso3(xi)@S0,reps)
        if extra is not None: F=np.append(F,extra[0]@xi-extra[1])
        if np.abs(F).max()<1e-14: break
        m=len(reps)+(1 if extra is not None else 0)
        J=np.zeros((m,3)); h=1e-7
        for k in range(3):
            e=np.zeros(3); e[k]=h
            d=(sg(expso3(xi+e)@S0,reps)-sg(expso3(xi-e)@S0,reps))/(2*h)
            J[:len(reps),k]=d
        if extra is not None: J[-1]=extra[0]
        xi=xi-np.linalg.pinv(J)@F
    return xi
def tangent(xi,reps):
    J=np.zeros((len(reps),3)); h=1e-7
    for k in range(3):
        e=np.zeros(3); e[k]=h
        J[:,k]=(sg(expso3(xi+e)@S0,reps)-sg(expso3(xi-e)@S0,reps))/(2*h)
    return np.linalg.svd(J)[2][2]

# identify the third pair at the dip: walk to ~step5 as before
xi=solve(np.zeros(3),REPS2)
prev=None; traj=[xi.copy()]
for n in range(7):
    t=tangent(xi,REPS2)
    if prev is not None and t@prev<0: t=-t
    prev=t
    xi=solve(xi+0.01*t,REPS2,extra=(t,t@(xi+0.01*t)))
    traj.append(xi.copy())
M=expso3(traj[5])@S0
nm=near_misses(M,0.03)
cand=[x for x in nm if x[0]>1e-9]
print("candidate third pairs at dip:",[(f"{g:.5f}",i,j,ei,ej) for g,i,j,ei,ej,_,_ in cand])
g,i,j,ei,ej,_,_=cand[0]; P3=(i,j,ei,ej)

# signed value of P3 along the curve, arclength-pinned continuation
def signed3(xi): return sg(expso3(xi)@S0,[P3])[0]
xi=solve(np.zeros(3),REPS2); prev=None
print("\n s      |xi|deg   signed g3")
vals=[]
for n in range(14):
    t=tangent(xi,REPS2)
    if prev is not None and t@prev<0: t=-t
    prev=t
    xi=solve(xi+0.008*t,REPS2,extra=(t,t@(xi+0.008*t)))
    v=signed3(xi); vals.append((n,xi.copy(),v))
    print(f" {0.008*(n+1):.3f}  {np.rad2deg(np.linalg.norm(xi)):7.3f}  {v:+.6f}")
# bisection if sign change
for (n1,x1,v1),(n2,x2,v2) in zip(vals,vals[1:]):
    if v1*v2<0:
        a,b=x1,x2
        for _ in range(60):
            mид=(a+b)/2
            t=tangent(a,REPS2)
            m=solve(mид,REPS2,extra=(t,t@mид))
            if signed3(m)*signed3(a)>=0 if False else (signed3(m)*sg(expso3(a)@S0,[P3])[0]>0): a=m
            else: b=m
        xiT=(a+b)/2
        xiT=solve(xiT,REPS2+[P3])
        MT=expso3(xiT)@S0
        F=sg(MT,REPS2+[P3])
        print("\nTRIPLE POINT residuals:",F)
        print("|xi| from midpoint (deg):",np.rad2deg(np.linalg.norm(xiT)))
        nm3=near_misses(MT,0.05)
        ex=[x for x in nm3 if x[0]<1e-9]; gh=sorted(x[0] for x in nm3 if x[0]>=1e-9)
        print(f"exact crossings: {len(ex)}   next ghosts: {['%.4f'%x for x in gh[:4]]}")
        print(repr(MT))
        np.save("edge_close_MT.npy",MT)
        break
else:
    print("\nno sign change: minimum of |g3| on curve is", min(abs(v) for _,_,v in vals),"-> tangency, no exact triple point on this branch")
