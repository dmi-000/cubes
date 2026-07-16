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
def count_exact(M):
    mats=[M,C@M,C@C@M]; ex=0
    for i in range(3):
        for j in range(i+1,3):
            for ei,(cc1,d1) in enumerate(EDGES):
                for ej,(cc2,d2) in enumerate(EDGES):
                    g,t1,t2=seg_gap(mats[i]@cc1,mats[i]@d1,mats[j]@cc2,mats[j]@d2)
                    if g<1e-9 and abs(t1)<0.9999 and abs(t2)<0.9999: ex+=1
    return ex

# fine psi scan (theta=0), record plateau changes
prev=None
print("psi scan:")
for psd in np.arange(0,90.01,0.5):
    c=count_exact(seedM(0,np.deg2rad(psd)))
    if c!=prev: print(f"  psi={psd:6.2f}  crossings={c}")
    prev=c
# exact special candidates
for name,ps in [("arctan(1/sqrt2)=35.264",np.arctan(1/np.sqrt(2))),("45",np.pi/4),
                ("arctan(sqrt2)=54.736",np.arctan(np.sqrt(2)))]:
    print(f"  psi={name}: crossings={count_exact(seedM(0,ps))}")

# where is the golden endpoint? project E1 into the family
delta=np.deg2rad(40.3060)
E1=rot(AX,delta)@Rx45
u=E1[:,2]-(E1[:,2]@sh)*sh; u/=np.linalg.norm(u)
th=np.arctan2(u@b,u@a); w=np.cross(sh,u)
ps=np.arctan2(E1[:,0]@sh,w@E1[:,0])
print(f"\ngolden endpoint fits family at theta={np.rad2deg(th):.5f} psi={np.rad2deg(ps):.5f} deg")
print("  fit residual:",np.abs(seedM(th,ps)-E1).max(),"(consistent with 1e-6 rounded slide constants)")
print("  crossings at that exact family point:",count_exact(seedM(th,ps)))
# guess exact psi_golden: print trig values
print("  sin(psi)=",np.sin(ps)," cos(psi)=",np.cos(ps)," tan(psi)=",np.tan(ps))
# octahedral: col1=e1 -> sin(psi)=e1.sh=1/sqrt3
ps0=np.arcsin(1/np.sqrt(3))
print(f"\noctahedral endpoint: psi={np.rad2deg(ps0):.5f} = arcsin(1/sqrt3), crossings={count_exact(seedM(0,ps0))}")

# congruence invariants of the special points
def gen_O():
    import itertools as it
    Os=[]
    for perm in it.permutations(range(3)):
        for signs in it.product([1,-1],repeat=3):
            P=np.zeros((3,3))
            for r,(p,s) in enumerate(zip(perm,signs)): P[r,p]=s
            if np.linalg.det(P)>0: Os.append(P)
    return Os
O=gen_O()
def invariant(M):
    mats=[M,C@M,C@C@M]; vals=[]
    for i in range(3):
        for j in range(i+1,3):
            vals.append(round(max(np.trace(mats[i].T@mats[j]@H) for H in O),9))
    return sorted(vals)
for name,ps in [("psi=0 (shared axis)",0.0),("psi=45",np.pi/4),
                ("psi_oct=arcsin(1/sqrt3)",ps0),("psi_golden",ps)]:
    print(f"{name}: invariant={invariant(seedM(0,ps))}")
print("known: octahedral 1.914213562=1/2+sqrt2, golden 2.427050707")
print("check (1+3*sqrt5)/... : phi=",(1+np.sqrt(5))/2," (3+sqrt5)/2-... 2.427050983=(1+sqrt5+...)?")
print("  1/2+sqrt2 =",0.5+np.sqrt(2)," (3*phi)/2=",3*(1+np.sqrt(5))/4)
