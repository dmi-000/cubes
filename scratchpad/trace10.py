import numpy as np, itertools
exec(open("edge_close4.py").read().split("# locate s=0.06")[0])
sh=np.array([1.0,1,1])/np.sqrt(3)
A=np.array([1.0,-1,0])/np.sqrt(2); B=np.array([1.0,1,-2])/np.sqrt(6)
def cubeM(th,ps):
    u=np.cos(th)*A+np.sin(th)*B
    w=np.cross(sh,u)
    return np.column_stack([np.cos(ps)*w+np.sin(ps)*sh,-np.sin(ps)*w+np.cos(ps)*sh,u])
def seg_all(dth,ps,labels):
    MA=cubeM(0.0,ps); MB=cubeM(dth,ps); out=[]
    for ei,ej in labels:
        c1,d1=EDGES[ei]; c2,d2=EDGES[ej]
        C1,D1=MA@c1,MA@d1; C2,D2=MB@c2,MB@d2
        n=np.cross(D1,D2); lg=(C2-C1)@n/np.linalg.norm(n)
        w=C1-C2; b=D1@D2; f=w@D1; g=w@D2; den=1-b*b
        t1=(b*g-f)/den; t2=b*t1+g
        out.append((lg,t1,t2))
    return out
CORE=[(0,1),(3,2),(5,4),(6,7),(8,8),(11,11)]
EXTRAS=[(4,10),(7,9),(9,6),(10,5)]
PSI_OCT=np.arcsin(1/np.sqrt(3)); PHI=(1+np.sqrt(5))/2; PSI_G=np.arctan(PHI*PHI)
# trace zero curve of extra (4,10) coplanarity in (dth,psi) plane
def F(x): return seg_all(x[0],x[1],[(4,10)])[0][0]
x=np.array([np.deg2rad(120),PSI_OCT])
h=1e-7
def grad(x):
    g=np.zeros(2)
    for k in range(2):
        e=np.zeros(2); e[k]=h
        g[k]=(F(x+e)-F(x-e))/(2*h)
    return g
# both directions
for sgn in (+1,-1):
    x=np.array([np.deg2rad(120),PSI_OCT]); print(f"--- direction {sgn:+d} ---")
    dirprev=None
    for step in range(400):
        g=grad(x); t=np.array([-g[1],g[0]]); t/=np.linalg.norm(t)
        if dirprev is not None and t@dirprev<0: t=-t
        elif dirprev is None: t*=sgn
        dirprev=t
        x=x+0.004*t
        # newton correct
        for _ in range(30):
            v=F(x); g2=grad(x)
            if abs(v)<1e-13: break
            x=x-v*g2/(g2@g2)
        if step%40==0 or step==399:
            vals=seg_all(x[0],x[1],CORE+EXTRAS)
            resid=max(abs(v[0]) for v in vals[6:])
            nvalid=sum(1 for lg,t1,t2 in vals if abs(lg)<1e-9 and abs(t1)<=1.0001 and abs(t2)<=1.0001)
            tmax=max(max(abs(v[1]),abs(v[2])) for v in vals)
            print(f"  step{step:4d}: dth={np.rad2deg(x[0]):8.3f} psi={np.rad2deg(x[1]):7.3f}  all-extras-resid={resid:.1e} valid(10?)={nvalid} max|t|={tmax:.3f}")
        if not (0.02<x[1]<1.55): print("  left psi range"); break
