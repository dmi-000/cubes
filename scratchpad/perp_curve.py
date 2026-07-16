import numpy as np
exec(open("edge_close4.py").read().split("# locate s=0.06")[0])
REPS2=[(0,1,5,4),(0,1,8,8)]
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
    for it in range(60):
        F=np.append(sg(expso3(xi)@S0,REPS2), t@xi-c)
        if np.abs(F).max()<1e-14: return xi,True
        xi=xi-np.linalg.solve(np.vstack([J2(xi),t]),F)
    return xi,False
xi=np.zeros(3)
for it in range(60):
    F=sg(expso3(xi)@S0,REPS2)
    if np.abs(F).max()<1e-14: break
    xi=xi-np.linalg.pinv(J2(xi))@F
prev=None
print("  n   |xi|deg   col3.(111)     col1.(111)   col2.(111)")
for n in range(120):
    t=np.linalg.svd(J2(xi))[2][2]
    if prev is not None and t@prev<0: t=-t
    prev=t
    pred=xi+0.01*t
    xi,ok=corrector(pred.copy(),t,t@pred)
    if n%10==0:
        M=expso3(xi)@S0
        s=np.array([1.0,1,1])
        print(f" {n:3d}  {np.rad2deg(np.linalg.norm(xi)):7.3f}  {M[:,2]@s:+.12f}  {M[:,0]@s:+.6f} {M[:,1]@s:+.6f}")
