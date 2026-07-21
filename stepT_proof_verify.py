# Verification of the complete Step-T local inequality (diamond) and its case analysis.
# Local model at a triple point: 3 convex polygons P_i (active-facet tangential gradients);
# m_i = support function; top diagram = argmin_i m_i (farthest cell), bottom = argmax_i (nearest).
import numpy as np
from scipy.spatial import ConvexHull
Ns=9000; TH=np.linspace(0,2*np.pi,Ns,endpoint=False); U=np.c_[np.cos(TH),np.sin(TH)]
def supp(P): return (P@U.T).max(axis=0)
def sc(f):
    s=np.sign(f); s[s==0]=1; return int(np.sum(s!=np.roll(s,1)))
def rand_poly(a,rng,spread,center):
    if a==1: return center.reshape(1,2)
    for _ in range(300):
        pts=center+rng.standard_normal((a+4,2))*spread
        try:
            h=ConvexHull(pts)
            if len(h.vertices)>=a: return pts[h.vertices]
        except Exception: pass
    return center.reshape(1,2)
rng=np.random.default_rng(2026)
T=50000
v_diamond=v_L1=v_db0=v_db2=v_zij2=0; nb0=nb2=0
for t in range(T):
    Ps=[rand_poly(int(rng.integers(1,6)),rng,rng.uniform(0.1,4.0),rng.standard_normal(2)*rng.uniform(0.03,4.0)) for _ in range(3)]
    AA=[len(P) for P in Ps]; sig=sum(AA)
    M=np.array([supp(P) for P in Ps])
    amin=np.argmin(M,0); amax=np.argmax(M,0)
    dt=int(np.sum(amin!=np.roll(amin,1))); db=int(np.sum(amax!=np.roll(amax,1)))
    z={(i,j):sc(M[i]-M[j]) for (i,j) in [(0,1),(0,2),(1,2)]}
    # L1: z_ij <= 2 min(a_i,a_j)
    if any(z[(i,j)]>2*min(AA[i],AA[j]) for (i,j) in z): v_L1+=1
    if dt<3 and db<3: continue
    # (diamond)
    if dt-2 > max(db-2,0)+(2*sig-6): v_diamond+=1
    # case checks
    if db==0:
        nb0+=1
        # one cell always nearest (const argmax); top only between other two: deg_top==that pair's z
        k=int(amax[0]); ij=[x for x in (0,1,2) if x!=k]
        if dt!=z[tuple(sorted(ij))]: v_db0+=1
    if db==2:
        nb2+=1
        # never-nearest cell k; the two nearest cells' z must equal 2
        cells_seen=set(amax.tolist()); 
        if len(cells_seen)==2:
            k=[x for x in (0,1,2) if x not in cells_seen][0]
            ij=tuple(sorted(x for x in (0,1,2) if x!=k))
            if z[ij]!=2: v_zij2+=1
        else:
            v_db2+=1  # unexpected
print(f"trials={T}")
print(f"L1  z_ij<=2min(a_i,a_j)                         violations: {v_L1}")
print(f"(diamond) deg_top-2<=(deg_bot-2)^+ +(2σ-6)      violations: {v_diamond}")
print(f"deg_bot=0 cases: {nb0}, 'deg_top==z_ij(other pair)' failures: {v_db0}")
print(f"deg_bot=2 cases: {nb2}, 'z of two-nearest-cells==2' failures: {v_zij2} (non-2-cell argmax: {v_db2})")
