import numpy as np, itertools
exec(open("edge_close4.py").read().split("# locate s=0.06")[0])
C=np.array([[0,0,1],[1,0,0],[0,1,0]],float)
sh=np.array([1.0,1,1])/np.sqrt(3)
a=np.array([1.0,-1,0])/np.sqrt(2); b=np.array([1.0,1,-2])/np.sqrt(6)
def seedM(ps):
    u=a; w=np.cross(sh,u)
    return np.column_stack([np.cos(ps)*w+np.sin(ps)*sh,-np.sin(ps)*w+np.cos(ps)*sh,u])
def seg_gap(c1,d1,c2,d2):
    w=c1-c2; bb=d1@d2; f=w@d1; g=w@d2; den=1-bb*bb
    t1=np.clip((bb*g-f)/den,-1,1) if abs(den)>1e-14 else 0.0
    t2=np.clip(bb*t1+g,-1,1); t1=np.clip(bb*t2-f,-1,1)
    return np.linalg.norm(c1+t1*d1-(c2+t2*d2)),t1,t2
def xset(ps):
    M=seedM(np.deg2rad(ps)); mats=[M,C@M,C@C@M]; s=set()
    for i in range(3):
        for j in range(i+1,3):
            for ei,(cc1,d1) in enumerate(EDGES):
                for ej,(cc2,d2) in enumerate(EDGES):
                    g,t1,t2=seg_gap(mats[i]@cc1,mats[i]@d1,mats[j]@cc2,mats[j]@d2)
                    if g<1e-9 and abs(t1)<0.999 and abs(t2)<0.999:
                        s.add((i,j,ei,ej))
    return s

PSI_OCT=np.rad2deg(np.arcsin(1/np.sqrt(3))); PSI_MOCT=np.rad2deg(np.arctan(np.sqrt(2)))
PHI=(1+np.sqrt(5))/2; PSI_G=np.rad2deg(np.arctan(PHI*PHI))
print(f"oct={PSI_OCT:.4f} mirror-oct={PSI_MOCT:.4f} golden={PSI_G:.4f} mirror-golden={90-PSI_G:.4f}")

# where does the SET actually change on [20,70]? fine scan
grid=np.arange(20.0,70.01,0.1)
prev=None; changes=[]
sets={}
for ps in grid:
    s=xset(ps); sets[round(ps,2)]=s
    if prev is not None and s!=prev[1]:
        changes.append((prev[0],ps,len(prev[1]),len(s)))
    prev=(ps,s)
print("set changes (between grid pts):")
for lo,hi,n1,n2 in changes: print(f"  {lo:.1f} -> {hi:.1f}: {n1} -> {n2}")

# Route A: oct(35.264) -> golden(69.095): intersection of sets at all grid pts strictly between
def core(lo,hi):
    cs=None
    for ps in grid:
        if lo+0.05<ps<hi-0.05:
            cs=sets[round(ps,2)] if cs is None else cs & sets[round(ps,2)]
    return cs
S_oct=xset(PSI_OCT); S_moct=xset(PSI_MOCT); S_g_int=xset(PSI_G)
coreA=core(PSI_OCT,PSI_G)
print(f"\nRoute A oct(35.26)->golden(69.09): persistent core size={len(coreA)}")
print(f"  core ⊂ oct set: {coreA<=S_oct}   core ⊂ golden interior set: {coreA<=S_g_int}")
# Route B: mirror-oct(54.736) -> golden(69.095)
coreB=core(PSI_MOCT,PSI_G)
print(f"Route B mirror-oct(54.74)->golden(69.09): persistent core={len(coreB)}")
print(f"  core ⊂ mirror-oct set({len(S_moct)}): {coreB<=S_moct}   core ⊂ golden interior({len(S_g_int)}): {coreB<=S_g_int}")
# Route C (mirror of B): oct(35.264) -> mirror-golden(20.905)
coreC=core(90-PSI_G,PSI_OCT)
print(f"Route C oct(35.26)->mirror-golden(20.91): persistent core={len(coreC)}")
print(f"  core ⊂ oct set({len(S_oct)}): {coreC<=S_oct}")
# sanity: endpoint sets
print(f"\nendpoint interior sets: oct={len(S_oct)} mirror-oct={len(S_moct)} golden={len(S_g_int)}")
# is the 18-set on (45.4,69.09) constant through the mirror-oct spike?
s50=sets[50.0]; s60=sets[60.0]; s48=sets[48.0]; s68=sets[68.0]
print(f"18-plateau constancy: s(48)==s(50)=={s48==s50}, s(50)==s(60)=={s50==s60}, s(60)==s(68)=={s60==s68}")
print(f"mirror-oct set ⊇ plateau set: {s60<=S_moct}")
# and route A: does the set change at 45? compare s(40) vs s(50)
s40=sets[40.0]
print(f"s(40)==s(50)? {s40==s50}; |s40 ∩ s50|={len(s40&s50)} of {len(s40)}")
