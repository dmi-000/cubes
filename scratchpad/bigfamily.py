import numpy as np, itertools
exec(open("edge_close4.py").read().split("# locate s=0.06")[0])
sh=np.array([1.0,1,1])/np.sqrt(3)
A=np.array([1.0,-1,0])/np.sqrt(2); B=np.array([1.0,1,-2])/np.sqrt(6)
def cubeM(th,ps):
    u=np.cos(th)*A+np.sin(th)*B
    w=np.cross(sh,u)
    return np.column_stack([np.cos(ps)*w+np.sin(ps)*sh,-np.sin(ps)*w+np.cos(ps)*sh,u])
def seg_gap(c1,d1,c2,d2):
    w=c1-c2; bb=d1@d2; f=w@d1; g=w@d2; den=1-bb*bb
    t1=np.clip((bb*g-f)/den,-1,1) if abs(den)>1e-14 else 0.0
    t2=np.clip(bb*t1+g,-1,1); t1=np.clip(bb*t2-f,-1,1)
    return np.linalg.norm(c1+t1*d1-(c2+t2*d2)),t1,t2
def analyze(mats,verbose=False):
    ncross=0; linegap_max={0:0.0,1:0.0,2:0.0}
    for i in range(len(mats)):
        for j in range(i+1,len(mats)):
            for ei in range(12):
                for ej in range(12):
                    cc1,d1=EDGES[ei]; cc2,d2=EDGES[ej]
                    C1,D1=mats[i]@cc1,mats[i]@d1; C2,D2=mats[j]@cc2,mats[j]@d2
                    n=np.cross(D1,D2)
                    nn=np.linalg.norm(n)
                    if nn>1e-9:
                        lg=abs((C2-C1)@n/nn)
                        cls=ei//4
                        if ej//4==cls: linegap_max[cls]=max(linegap_max[cls],min(lg,1.0)) if False else linegap_max[cls]
                        # track same-class line gaps
                        if ei//4==ej//4: linegap_max[cls]=max(linegap_max[cls],lg)
                    g,t1,t2=seg_gap(C1,D1,C2,D2)
                    if g<1e-9 and abs(t1)<0.999 and abs(t2)<0.999: ncross+=1
    return ncross,linegap_max

rng=np.random.default_rng(7)
print("BIG FAMILY TEST: per-cube theta_k (arbitrary), COMMON psi")
print(" same-class line-gap maxima (0 => identity persists) and interior crossings:")
for trial in range(6):
    ths=rng.uniform(0,2*np.pi,3); ps=rng.uniform(0.1,1.4)
    mats=[cubeM(t,ps) for t in ths]
    n,lg=analyze(mats)
    print(f"  th={np.rad2deg(ths).round(1)} psi={np.rad2deg(ps):6.2f}  linegaps x/y/z={lg[0]:.2e}/{lg[1]:.2e}/{lg[2]:.2e}  crossings={n}")
print()
print("CONTROL: different psi per cube (should break):")
for trial in range(2):
    ths=rng.uniform(0,2*np.pi,3); pss=rng.uniform(0.1,1.4,3)
    mats=[cubeM(t,p) for t,p in zip(ths,pss)]
    n,lg=analyze(mats)
    print(f"  psi={np.rad2deg(pss).round(1)}  linegaps={lg[0]:.2e}/{lg[1]:.2e}/{lg[2]:.2e}  crossings={n}")
