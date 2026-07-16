import numpy as np, itertools
exec(open("edge_close4.py").read().split("# locate s=0.06")[0])
C=np.array([[0,0,1],[1,0,0],[0,1,0]],float)
sh=np.array([1.0,1,1])/np.sqrt(3)
a=np.array([1.0,-1,0])/np.sqrt(2)
def seedM(ps):
    u=a; w=np.cross(sh,u)
    return np.column_stack([np.cos(ps)*w+np.sin(ps)*sh,-np.sin(ps)*w+np.cos(ps)*sh,u])
def seg_gap(c1,d1,c2,d2):
    w=c1-c2; bb=d1@d2; f=w@d1; g=w@d2; den=1-bb*bb
    t1=np.clip((bb*g-f)/den,-1,1) if abs(den)>1e-14 else 0.0
    t2=np.clip(bb*t1+g,-1,1); t1=np.clip(bb*t2-f,-1,1)
    return np.linalg.norm(c1+t1*d1-(c2+t2*d2)),t1,t2
def status(ps,pairs):
    M=seedM(np.deg2rad(ps)); mats=[M,C@M,C@C@M]; out={}
    for (i,j,ei,ej) in pairs:
        cc1,d1=EDGES[ei]; cc2,d2=EDGES[ej]
        g,t1,t2=seg_gap(mats[i]@cc1,mats[i]@d1,mats[j]@cc2,mats[j]@d2)
        out[(i,j,ei,ej)]=(g,t1,t2)
    return out
# the 18-core = interior set at psi=50
def xset(ps):
    M=seedM(np.deg2rad(ps)); mats=[M,C@M,C@C@M]; s=set()
    for i in range(3):
        for j in range(i+1,3):
            for ei in range(12):
                for ej in range(12):
                    cc1,d1=EDGES[ei]; cc2,d2=EDGES[ej]
                    g,t1,t2=seg_gap(mats[i]@cc1,mats[i]@d1,mats[j]@cc2,mats[j]@d2)
                    if g<1e-9 and abs(t1)<0.999 and abs(t2)<0.999: s.add((i,j,ei,ej))
    return s
core=xset(50.0)
PHI=(1+np.sqrt(5))/2; PSI_G=np.rad2deg(np.arctan(PHI*PHI))
st=status(PSI_G,core)
n_int=sum(1 for g,t1,t2 in st.values() if g<1e-9 and abs(t1)<0.999 and abs(t2)<0.999)
n_corner=sum(1 for g,t1,t2 in st.values() if g<1e-9 and max(abs(t1),abs(t2))>0.999)
n_broken=sum(1 for g,t1,t2 in st.values() if g>=1e-9)
print(f"core 18 pairs at golden: interior={n_int}, docked-at-corner={n_corner}, broken(gap>0)={n_broken}")
for k,(g,t1,t2) in sorted(st.items()):
    tag="interior" if (g<1e-9 and abs(t1)<0.999 and abs(t2)<0.999) else ("corner" if g<1e-9 else f"GAP={g:.2e}")
    print(f"  {k}: gap={g:.1e} t=({t1:+.4f},{t2:+.4f}) {tag}")
# and at mirror-golden for route C
st2=status(90-PSI_G,core)
n2=[sum(1 for g,t1,t2 in st2.values() if cond(g,t1,t2)) for cond in
    [lambda g,t1,t2: g<1e-9 and abs(t1)<0.999 and abs(t2)<0.999,
     lambda g,t1,t2: g<1e-9 and max(abs(t1),abs(t2))>=0.999,
     lambda g,t1,t2: g>=1e-9]]
print(f"\ncore 18 at mirror-golden: interior={n2[0]}, corner={n2[1]}, broken={n2[2]}")
