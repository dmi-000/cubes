import sys; sys.path.insert(0,"/Users/dmi/carroll")
import numpy as np, math
from cube_compound_exact import build_axes, find_cubes, ONE
from golden_rotations import Rot, A, B, closure
import sys; sys.path.insert(0,'/Users/dmi/carroll')
from slide3_q2 import Rx45
axes=build_axes(); triples=find_cubes(axes)
g5=[Rot([[axes[t[j]][i] for j in range(3)] for i in range(3)]) for t in triples]
def make_proper(M):
    if (M.det()-ONE).sign()==0: return M
    return Rot([[(-M.m[i][0] if j==0 else M.m[i][j]) for j in range(3)] for i in range(3)])
def fl(M): return np.array([[float(e) for e in row] for row in M.m])
O=[fl(g) for g in closure([A,B])]
S_oct=fl(Rx45()); S_dod=fl(make_proper(g5[1])); Bf=fl(B)
def Raxis(a,ang):
    x,y,z=a;c,s=math.cos(ang),math.sin(ang);C=1-c
    return np.array([[c+x*x*C,x*y*C-z*s,x*z*C+y*s],[y*x*C+z*s,c+y*y*C,y*z*C-x*s],[z*x*C-y*s,z*y*C+x*s,c+z*z*C]])
def cube_edges(M):
    sg=[(sx,sy,sz) for sx in(-1,1) for sy in(-1,1) for sz in(-1,1)]
    v=[M@np.array(s,dtype=float) for s in sg]
    return [(v[i],v[j]) for i in range(8) for j in range(i+1,8) if sum(a!=b for a,b in zip(sg[i],sg[j]))==1]
def closest(p1,p2,q1,q2):
    d1=p2-p1;d2=q2-q1;r=p1-q1;a=d1@d1;e=d2@d2;f=d2@r;c=d1@r;bb=d1@d2;den=a*e-bb*bb
    if abs(den)<1e-12:return None
    s=(bb*f-c*e)/den;tt=(a*f-bb*c)/den
    if not(0<=s<=1 and 0<=tt<=1):return None
    return s,tt,np.linalg.norm((p1+s*d1)-(q1+tt*d2))
def analyze(So,Sd):
    Delta=Sd@So.T; tr=np.trace(Delta)
    if (tr-1)/2>1-1e-9: return None
    delta=math.acos(np.clip((tr-1)/2,-1,1))
    ax=np.array([Delta[2,1]-Delta[1,2],Delta[0,2]-Delta[2,0],Delta[1,0]-Delta[0,1]])
    if np.linalg.norm(ax)<1e-9: return None
    ax/=np.linalg.norm(ax)
    E1=cube_edges(So);E2=cube_edges(Bf@So)
    best=None
    for i,(a1,a2) in enumerate(E1):
        for j,(b1,b2) in enumerate(E2):
            r=closest(a1,a2,b1,b2)
            if r and r[2]<1e-6 and abs(min(r[0],1-r[0])-0.5)<1e-3:
                worst=0; frac1=None
                for t in np.linspace(0,1,11):
                    St=Raxis(ax,t*delta)@So
                    rr=closest(*cube_edges(St)[i], *cube_edges(Bf@St)[j])
                    if rr is None: worst=9;break
                    worst=max(worst,rr[2])
                    if abs(t-1)<1e-9: frac1=min(rr[0],1-rr[0])
                if best is None or worst<best[0]:
                    best=(worst,frac1,delta*180/math.pi)
    return best
phi=(1+5**.5)/2; gs=1/phi/phi
res=[]
for go in O:
    for gd in O:
        b=analyze(S_oct@go, S_dod@gd)
        if b and b[0]<0.06: res.append(b)
res.sort()
print(f"gauges with edge pair staying near-incident (worst gap<0.06): {len(res)}")
for wg,frac1,dang in res[:12]:
    print(f"  worst_gap={wg:.4f} frac_at_t1={frac1:.4f} (golden-sec {gs:.4f}) Delta_angle={dang:.2f}")
