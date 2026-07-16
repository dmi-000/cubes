import numpy as np, itertools
exec(open("edge_close4.py").read().split("# locate s=0.06")[0])
C=np.array([[0,0,1],[1,0,0],[0,1,0]],float)
sh=np.array([1.0,1,1])/np.sqrt(3)
a=np.array([1.0,-1,0])/np.sqrt(2); b=np.array([1.0,1,-2])/np.sqrt(6)
def seedM(th,ps):
    u=np.cos(th)*a+np.sin(th)*b
    w=np.cross(sh,u)
    return np.column_stack([np.cos(ps)*w+np.sin(ps)*sh,-np.sin(ps)*w+np.cos(ps)*sh,u])
def seg_gap(c1,d1,c2,d2):
    w=c1-c2; bb=d1@d2; f=w@d1; g=w@d2; den=1-bb*bb
    t1=np.clip((bb*g-f)/den,-1,1) if abs(den)>1e-14 else 0.0
    t2=np.clip(bb*t1+g,-1,1); t1=np.clip(bb*t2-f,-1,1)
    return np.linalg.norm(c1+t1*d1-(c2+t2*d2)),t1,t2
def count_exact(M,tcap):
    mats=[M,C@M,C@C@M]; ex=0; corner=0
    for i in range(3):
        for j in range(i+1,3):
            for ei,(cc1,d1) in enumerate(EDGES):
                for ej,(cc2,d2) in enumerate(EDGES):
                    g,t1,t2=seg_gap(mats[i]@cc1,mats[i]@d1,mats[j]@cc2,mats[j]@d2)
                    if g<1e-9:
                        if abs(t1)<tcap and abs(t2)<tcap: ex+=1
                        elif max(abs(t1),abs(t2))>0.999999: corner+=1
    return ex,corner
phi=(1+np.sqrt(5))/2
psg=np.arctan(phi**2)
Mg=seedM(0,psg)
exi,cor=count_exact(Mg,0.9999)
print(f"golden exact point tan(psi)=phi^2: interior crossings={exi}, at-corner contacts={cor}")
# invariant check == 3phi/2 ?
import itertools as it
O=[]
for perm in it.permutations(range(3)):
    for signs in it.product([1,-1],repeat=3):
        P=np.zeros((3,3))
        for r,(p,s) in enumerate(zip(perm,signs)): P[r,p]=s
        if np.linalg.det(P)>0: O.append(P)
inv=max(np.trace(Mg.T@(C@Mg)@H) for H in O)
print("invariant:",inv," 3phi/2 =",3*phi/2," diff:",inv-3*phi/2)
# sin/cos identity
print("sin(psi)-phi/sqrt3:",np.sin(psg)-phi/np.sqrt(3)," cos(psi)-1/(phi*sqrt3):",np.cos(psg)-1/(phi*np.sqrt(3)))
# fine scan near golden
for psd in [68.9,69.0,69.05,69.09,69.0948,69.1,69.2,69.5]:
    e,c=count_exact(seedM(0,np.deg2rad(psd)),0.9999)
    print(f"  psi={psd:8.4f} interior={e:2d} corner={c}")
