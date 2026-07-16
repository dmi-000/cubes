import numpy as np, itertools
exec(open("edge_close4.py").read().split("# locate s=0.06")[0])
C=np.array([[0,0,1],[1,0,0],[0,1,0]],float)
sh=np.array([1.0,1,1])/np.sqrt(3)
a=np.array([1.0,-1,0])/np.sqrt(2); b=np.array([1.0,1,-2])/np.sqrt(6)
def seedM(th,ps):
    u=np.cos(th)*a+np.sin(th)*b
    w=np.cross(sh,u)
    c1=np.cos(ps)*w+np.sin(ps)*sh
    c2=-np.sin(ps)*w+np.cos(ps)*sh
    return np.column_stack([c1,c2,u])
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
def line_gaps(M):
    # infinite-line signed gaps for the three class representatives
    mats=[M,C@M,C@C@M]; out=[]
    for (i,j,ei,ej) in [(0,1,0,1),(0,1,5,4),(0,1,8,8)]:
        cc1,d1=EDGES[ei]; cc2,d2=EDGES[ej]
        n=np.cross(mats[i]@d1,mats[j]@d2)
        out.append((mats[j]@cc2-mats[i]@cc1)@n/np.linalg.norm(n))
    return out

rng=np.random.default_rng(1)
print("random family members: line-gaps (x-,y-,z-edge classes) and exact segment crossings")
for _ in range(6):
    th,ps=rng.uniform(0,2*np.pi,2)
    M=seedM(th,ps)
    assert np.abs(M@M.T-np.eye(3)).max()<1e-12 and np.linalg.det(M)>0
    lg=line_gaps(M)
    print(f" th={np.rad2deg(th):7.2f} ps={np.rad2deg(ps):7.2f}  line-gaps={['%.2e'%abs(x) for x in lg]}  exact crossings={count_exact(M)}")

# endpoints in F?
delta=np.deg2rad(40.3060)
E0=Rx45; E1=rot(AX,delta)@Rx45
for name,E in [("octahedral t=0",E0),("golden t=1",E1)]:
    perp=[abs(E[:,k]@sh) for k in range(3)]
    print(f"{name}: |col_k . (111)| = {['%.2e'%p for p in perp]}  -> in F: {min(perp)<1e-9}")

# where does the min-norm 1.66deg solution sit? recover (th,ps)
M=np.load("edge_close_M.npy")
u=M[:,2]; th=np.arctan2(u@b,u@a); ps=np.arctan2(M[:,0]@sh,(np.cross(sh,u))@M[:,0])
print(f"\n1.66deg solution: theta={np.rad2deg(th):.4f} deg  psi={np.rad2deg(ps):.4f} deg")
print("reconstruction err:",np.abs(seedM(th,ps)-M).max())

# crossing-count map over the family
print("\ncrossing-count map (rows theta 0..120 deg, cols psi 0..90 deg):")
ths=np.linspace(0,np.deg2rad(120),13); pss=np.linspace(0,np.pi/2,13)
for th in ths:
    print(" ".join(f"{count_exact(seedM(th,ps)):2d}" for ps in pss))
