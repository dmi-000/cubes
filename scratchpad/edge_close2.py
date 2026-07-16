import numpy as np, itertools

C = np.array([[0,0,1],[1,0,0],[0,1,0]],float)
c=np.cos(np.pi/4); s=np.sin(np.pi/4)
Rx45=np.array([[1,0,0],[0,c,-s],[0,s,c]])
delta=np.deg2rad(40.3060)
AX=np.array([-0.442177,-0.828653,0.343239]); AX/=np.linalg.norm(AX)
def rot(axis,th):
    K=np.array([[0,-axis[2],axis[1]],[axis[2],0,-axis[0]],[-axis[1],axis[0],0]])
    return np.eye(3)+np.sin(th)*K+(1-np.cos(th))*(K@K)
S0 = rot(AX,0.5*delta)@Rx45          # clean t=0.5 seed (replaces user's 6-digit rounding)

# 12 edges of [-1,1]^3: (free axis a, fixed signs on other two)
EDGES=[]
for a in range(3):
    o=[i for i in range(3) if i!=a]
    for s1,s2 in itertools.product([-1,1],repeat=2):
        cvec=np.zeros(3); cvec[o[0]]=s1; cvec[o[1]]=s2
        d=np.zeros(3); d[a]=1.0
        EDGES.append((cvec,d))

def seg_gap(c1,d1,c2,d2):
    # min distance between segments c+t d, t in [-1,1]
    w=c1-c2; a=1.0; b=d1@d2; e=1.0; f=w@d1; g=w@d2
    den=a*e-b*b
    if abs(den)<1e-14: t1=0.0
    else: t1=np.clip((b*g-e*f)/den,-1,1)
    t2=np.clip((b*t1+g)/e,-1,1)
    t1=np.clip((b*t2-f)/a,-1,1)
    p=c1+t1*d1; q=c2+t2*d2
    return np.linalg.norm(p-q),t1,t2

def near_misses(M,tol=0.02):
    mats=[M,C@M,C@C@M]; out=[]
    for i in range(3):
        for j in range(i+1,3):
            for ei,(c1,d1) in enumerate(EDGES):
                for ej,(c2,d2) in enumerate(EDGES):
                    g,t1,t2=seg_gap(mats[i]@c1,mats[i]@d1,mats[j]@c2,mats[j]@d2)
                    if 1e-9<g<tol and abs(t1)<0.999 and abs(t2)<0.999:
                        out.append((g,i,j,ei,ej,t1,t2))
    return sorted(out)

nm=near_misses(S0)
print(f"{len(nm)} near-miss edge pairs (gap<0.02), interior of both segments:")
for g,i,j,ei,ej,t1,t2 in nm:
    print(f"  gap={g:.6f} cubes({i},{j}) edges({ei},{ej}) params({t1:+.3f},{t2:+.3f})")
