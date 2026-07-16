import numpy as np, itertools
exec(open("edge_close4.py").read().split("# locate s=0.06")[0])
sh=np.array([1.0,1,1])/np.sqrt(3)
A=np.array([1.0,-1,0])/np.sqrt(2); B=np.array([1.0,1,-2])/np.sqrt(6)
def cubeM(th,ps):
    u=np.cos(th)*A+np.sin(th)*B
    w=np.cross(sh,u)
    return np.column_stack([np.cos(ps)*w+np.sin(ps)*sh,-np.sin(ps)*w+np.cos(ps)*sh,u])
def status_pair(MA,MB,labels,tcap=1.0):
    ok=0
    for ei,ej in labels:
        c1,d1=EDGES[ei]; c2,d2=EDGES[ej]
        C1,D1=MA@c1,MA@d1; C2,D2=MB@c2,MB@d2
        n=np.cross(D1,D2); lg=(C2-C1)@n/np.linalg.norm(n)
        w=C1-C2; b=D1@D2; f=w@D1; g=w@D2; den=1-b*b
        t1=(b*g-f)/den; t2=b*t1+g
        if abs(lg)<1e-9 and abs(t1)<=tcap and abs(t2)<=tcap: ok+=1
    return ok
CORE=[(0,1),(3,2),(5,4),(6,7),(8,8),(11,11)]
EXTRAS=[(4,10),(7,9),(9,6),(10,5)]
PSI_OCT=np.arcsin(1/np.sqrt(3))
# curve: solve extra(4,10) linegap=0 for dth at given psi (Newton from previous)
def lg410(dth,ps):
    MA=cubeM(0.0,ps); MB=cubeM(dth,ps)
    c1,d1=EDGES[4]; c2,d2=EDGES[10]
    C1,D1=MA@c1,MA@d1; C2,D2=MB@c2,MB@d2
    n=np.cross(D1,D2); return (C2-C1)@n/np.linalg.norm(n)
def solve_dc(ps,d0):
    d=d0
    for _ in range(60):
        v=lg410(d,ps)
        if abs(v)<1e-13: break
        h=1e-7; dv=(lg410(d+h,ps)-lg410(d-h,ps))/(2*h)
        d-=v/dv
    return d
print(" psi   Delta_c  pair12(10 labels) pair13-core(at 2Dc)  TOTAL")
d=np.deg2rad(120)
for psd in [35.264,36,38,40,42,44,45,46,46.5,47,48]:
    ps=np.deg2rad(psd)
    d=solve_dc(ps,d)
    M1=cubeM(0,ps); M2=cubeM(d,ps); M3=cubeM(2*d,ps)
    n12=status_pair(M1,M2,CORE+EXTRAS)
    n23=status_pair(M2,M3,CORE+EXTRAS)
    n13all=0
    # pair13: count ALL exact labels (full 144 scan)
    for ei in range(12):
        for ej in range(12):
            n13all+=status_pair(M1,M3,[(ei,ej)])
    print(f" {psd:6.3f}  {np.rad2deg(d):7.3f}   {n12}/{n23}              {n13all}                {n12+n23+n13all}")
