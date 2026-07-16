import numpy as np, itertools
exec(open("edge_close4.py").read().split("# locate s=0.06")[0])
sh=np.array([1.0,1,1])/np.sqrt(3)
A=np.array([1.0,-1,0])/np.sqrt(2); B=np.array([1.0,1,-2])/np.sqrt(6)
def cubeM(th,ps):
    u=np.cos(th)*A+np.sin(th)*B
    w=np.cross(sh,u)
    return np.column_stack([np.cos(ps)*w+np.sin(ps)*sh,-np.sin(ps)*w+np.cos(ps)*sh,u])
def linegap(dth,ps,ei,ej):
    MA=cubeM(0.0,ps); MB=cubeM(dth,ps)
    c1,d1=EDGES[ei]; c2,d2=EDGES[ej]
    C1,D1=MA@c1,MA@d1; C2,D2=MB@c2,MB@d2
    n=np.cross(D1,D2)
    return (C2-C1)@n/np.linalg.norm(n)
PSI_OCT=np.arcsin(1/np.sqrt(3)); D120=np.deg2rad(120)
extras=[(4,10),(7,9),(9,6),(10,5)]
print("TEST 1: in-plane structure of extras' coplanarity residual around oct point")
print("(sign changes on a small circle => a zero CURVE passes through; none => isolated)")
for ei,ej in extras:
    vals=[]
    for phi in np.linspace(0,2*np.pi,73)[:-1]:
        dth=D120+np.deg2rad(0.3)*np.cos(phi); ps=PSI_OCT+np.deg2rad(0.3)*np.sin(phi)
        vals.append(linegap(dth,ps,ei,ej))
    vals=np.array(vals); sc=np.sum(np.abs(np.diff(np.sign(vals)))>0)
    print(f"  extra ({ei},{ej}): center residual={linegap(D120,PSI_OCT,ei,ej):.2e}, sign changes on circle={sc}, |min|={np.abs(vals).min():.2e}")

print("\nTEST 2: full 3-DOF pair space -- Jacobian of the 10 oct labels at the oct pair config")
MA0=cubeM(0.0,PSI_OCT); MB0=cubeM(D120,PSI_OCT)
labs=[(0,1),(3,2),(5,4),(6,7),(8,8),(11,11)]+extras
def gaps(xi):
    th=np.linalg.norm(xi)
    if th<1e-18: R=np.eye(3)
    else:
        K=xi/th; Km=np.array([[0,-K[2],K[1]],[K[2],0,-K[0]],[-K[1],K[0],0]])
        R=np.eye(3)+np.sin(th)*Km+(1-np.cos(th))*(Km@Km)
    MB=R@MB0
    out=[]
    for ei,ej in labs:
        c1,d1=EDGES[ei]; c2,d2=EDGES[ej]
        C1,D1=MA0@c1,MA0@d1; C2,D2=MB@c2,MB@d2
        n=np.cross(D1,D2)
        out.append((C2-C1)@n/np.linalg.norm(n))
    return np.array(out)
J=np.zeros((10,3)); h=1e-6
for k in range(3):
    e=np.zeros(3); e[k]=h
    J[:,k]=(gaps(e)-gaps(-e))/(2*h)
u_,s_,vt=np.linalg.svd(J)
print("  singular values of 10x3 Jacobian:",s_.round(8))
rank=(s_>1e-6).sum()
print(f"  rank={rank} -> local solution-variety dimension for keeping all 10 = {3-rank}")
# which subsets can be kept? core-6 gradients rank:
Jc=J[:6]; Je=J[6:]
print("  core-6 gradient rank:",(np.linalg.svd(Jc)[1]>1e-6).sum(),
      "| extras-4 gradient rank:",(np.linalg.svd(Je)[1]>1e-6).sum())
# can we keep core6 + ONE extra? rank of stacked 7
for k,(ei,ej) in enumerate(extras):
    r=(np.linalg.svd(np.vstack([Jc,Je[k:k+1]]))[1]>1e-6).sum()
    print(f"  core6+extra({ei},{ej}): rank={r} -> variety dim={3-r}")
