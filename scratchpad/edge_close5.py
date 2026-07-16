import numpy as np, itertools
exec(open("edge_close4.py").read().split("# locate s=0.06")[0])  # reuse defs

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
for sgn in (+1,-1):
    cur=xi0.copy(); prev=None
    print(f"--- direction {sgn:+d} ---")
    for n in range(15):
        t=tangent(cur,REPS2)
        if prev is not None and t@prev<0: t=-t
        prev=t
        cur=cur+sgn*0.01*t if n==0 else cur+0.01*t
        cur,_=solve(cur,REPS2)
        M=expso3(cur)@S0
        nm=near_misses(M,0.08)
        gh=sorted(x[0] for x in nm if x[0]>1e-9)
        print(f" step {n+1:2d} |xi|={np.rad2deg(np.linalg.norm(cur)):6.3f}deg min-ghost={gh[0] if gh else None:.5f}")
        if gh and gh[0]<3e-4:
            # grab representative and solve 3 conditions
            g,i,j,ei,ej,t1,t2=[x for x in nm if x[0]>1e-9][0]
            print(f"   closing third class: cubes({i},{j}) edges({ei},{ej}) gap={g:.6f}")
            xi3,F3=solve(cur,REPS2+[(i,j,ei,ej)])
            M3=expso3(xi3)@S0
            print("   residuals:",F3,"  |xi3| deg:",np.rad2deg(np.linalg.norm(xi3)))
            nm3=near_misses(M3,0.05)
            ex=[x for x in nm3 if x[0]<1e-9]; gh3=sorted(x[0] for x in nm3 if x[0]>=1e-9)
            print(f"   exact crossings: {len(ex)}  next ghosts: {['%.4f'%x for x in gh3[:3]]}")
            print("   matrix:"); print(repr(M3))
            np.save("edge_close_M3.npy",M3); np.save("edge_close_xi3.npy",xi3)
            def mat2quat(R):
                w=np.sqrt(max(0,1+R[0,0]+R[1,1]+R[2,2]))/2
                return np.array([w,(R[2,1]-R[1,2])/(4*w),(R[0,2]-R[2,0])/(4*w),(R[1,0]-R[0,1])/(4*w)])
            q=mat2quat(M3); print("   quaternion:",q)
            raise SystemExit
