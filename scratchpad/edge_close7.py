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

xi0,_=solve(np.zeros(3),REPS2)
# direction +1 walk exactly as in edge_close5 (which found the dip)
cur=xi0.copy(); prev=None; snap=None
for n in range(8):
    t=tangent(cur,REPS2)
    if prev is not None and t@prev<0: t=-t
    prev=t
    cur=cur+0.01*t
    cur,_=solve(cur,REPS2)
    M=expso3(cur)@S0
    nm=near_misses(M,0.08)
    gh=[x for x in nm if x[0]>1e-9]
    gmin=min(x[0] for x in gh)
    rep=[x for x in gh if x[0]==gmin][0]
    print(f" step {n+1} |xi|={np.rad2deg(np.linalg.norm(cur)):6.3f} min-ghost={gmin:.5f} pair=cubes({rep[1]},{rep[2]}) edges({rep[3]},{rep[4]})")
    if n==4: snap=(cur.copy(),(rep[1],rep[2],rep[3],rep[4]))
xiD,P3=snap
print("third pair:",P3)
def g3(xi): return sg(expso3(xi)@S0,[P3])[0]
# scan signed g3 along the curve finely around the dip
cur=xi0.copy(); prev=None
print("\n  s      signed g3")
vals=[]
for n in range(80):
    t=tangent(cur,REPS2)
    if prev is not None and t@prev<0: t=-t
    prev=t
    cur,_=solve(cur+0.002*t,REPS2)
    vals.append((cur.copy(),g3(cur)))
    if n%5==4: print(f" {0.002*(n+1):.3f}  {g3(cur):+.7f}")
sign_changed=False
for (x1,v1),(x2,v2) in zip(vals,vals[1:]):
    if v1*v2<0:
        sign_changed=True
        xiT,F=solve((x1+x2)/2,REPS2+[P3])
        MT=expso3(xiT)@S0
        print("\nTRIPLE POINT residuals:",F," |xi|deg:",np.rad2deg(np.linalg.norm(xiT)))
        nm3=near_misses(MT,0.05)
        ex=[x for x in nm3 if x[0]<1e-9]; gh=sorted(x[0] for x in nm3 if x[0]>=1e-9)
        print(f"exact crossings: {len(ex)}  next ghosts: {['%.4f'%x for x in gh[:4]]}")
        print(repr(MT)); np.save("edge_close_MT.npy",MT)
        break
if not sign_changed:
    mn=min(abs(v) for _,v in vals)
    print(f"\nno sign change; min |g3| along curve = {mn:.6f} -> tangency (no exact triple point on branch)")
