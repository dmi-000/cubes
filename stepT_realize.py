import numpy as np, itertools
from scipy.optimize import linprog
import warnings; warnings.filterwarnings('ignore')

def feasible(hs):
    A=np.array([h[0] for h in hs],float); b=np.array([h[1] for h in hs],float)
    r=linprog([0,0,0,-1],A_ub=np.hstack([A,np.linalg.norm(A,axis=1,keepdims=True)]),
              b_ub=b,bounds=[(-50,50)]*3+[(0,10)],method='highs')
    return r.success and r.x[3]>1e-7
def comps(pieces):
    P=[p for p in pieces if feasible(p)];k=len(P);par=list(range(k))
    def f(x):
        while par[x]!=x:par[x]=par[par[x]];x=par[x]
        return x
    for i in range(k):
        for j in range(i+1,k):
            if f(i)!=f(j) and feasible(P[i]+P[j]):par[f(i)]=f(j)
    return len(set(f(i) for i in range(k)))
def outside(F):return [(-np.array(n,float),-h) for (n,h) in F]
def d1_count(bodies):
    A,B,C=bodies
    return sum(comps([X+[oy]+[oz] for oy in outside(Y) for oz in outside(Z)])
               for (X,Y,Z) in [(A,B,C),(B,A,C),(C,A,B)])
def d2_count(bodies):
    A,B,C=bodies; tot=0
    for (X,Y,Z) in [(A,B,C),(A,C,B),(B,C,A)]:  # in X,Y not Z
        tot+=comps([X+Y+[oz] for oz in outside(Z)])
    return tot
def d3_count(bodies):
    A,B,C=bodies
    return comps([A+B+C])
def total(bodies):
    d1=d1_count(bodies);d2=d2_count(bodies);d3=d3_count(bodies)
    return d1,d2,d3,d1+d2+d3

def facet(nx,ny,nz,h):
    n=np.array([nx,ny,nz],float); nn=np.linalg.norm(n); return (n/nn, h/nn)

rho=1.0; mu=1.0/rho; g=3.0; s=0.5; L=6.0; W=6.0
# Blade B: mu z + g|x| <=1  -> two facets (+/-g,0,mu); plus +/-y caps and bottom
B=[facet(g,0,mu,1.0), facet(-g,0,mu,1.0),
   facet(0,1,0,W), facet(0,-1,0,W), facet(0,0,-1,L)]
# Blade C: mu z + g|y| <=1
C=[facet(0,g,mu,1.0), facet(0,-g,mu,1.0),
   facet(1,0,0,W), facet(-1,0,0,W), facet(0,0,-1,L)]
# Corner A: three facets mu z + s(x cosphi + y sinphi) <=1, phi=90,210,330 ; bottom cap
A=[]
for phi in (90,210,330):
    r=np.deg2rad(phi); A.append(facet(s*np.cos(r), s*np.sin(r), mu, 1.0))
A.append(facet(0,0,-1,L))

for nm,F in [('A corner',A),('B blade',B),('C blade',C)]:
    # check O interior and x0 on boundary
    x0=np.array([0,0,rho])
    onb=[abs(n@x0-h) for (n,h) in F]
    print(nm, 'facets=',len(F), 'O interior?', all(n@np.zeros(3)<h for (n,h) in F),
          'x0 on # facets=', sum(v<1e-9 for v in onb))

d1,d2,d3,tot=total([A,B,C])
print(f'\\nConstructed degenerate triple:  d1={d1} d2={d2} d3={d3}  TOTAL={tot}')
print('record for n=3 is 67; d1 record is 48')

# ---- search: can any 3 cells (<=6 facets), incl. thin / near-degenerate, beat d1=48 or total=67? ----
def rot():
    A=np.random.standard_normal((3,3));Q,_=np.linalg.qr(A)
    return Q if np.linalg.det(Q)>0 else Q@np.diag([-1.,1,1])
def box(scale):           # rotated axis box with per-axis half-widths -> 6 facets
    R=rot()
    return [ (R[:,a]*sg, scale[a]) for a in range(3) for sg in (1,-1) ]
np.random.seed(7)
best_d1=0; best_tot=0; bd=None; bt=None
import sys
NT=250
for t in range(NT):
    mode=t%3
    if mode==0:      # three generic rotated unit boxes
        cells=[box(np.ones(3)) for _ in range(3)]
    elif mode==1:    # thin boxes (one short axis) -> near-degenerate blades
        cells=[box(np.array([1.0,1.0,np.random.uniform(0.15,0.5)])) for _ in range(3)]
    else:            # near-coincident triple: base box + tiny rotations (forces near-degenerate triple pts)
        R=rot(); base=[ (R[:,a]*sg,1.0) for a in range(3) for sg in (1,-1)]
        cells=[]
        for _ in range(3):
            d=0.06*np.random.standard_normal(3)
            from scipy.linalg import expm
            K=np.array([[0,-d[2],d[1]],[d[2],0,-d[0]],[-d[1],d[0],0]])
            Rp=expm(K)@R
            cells.append([ (Rp[:,a]*sg,1.0) for a in range(3) for sg in (1,-1)])
    try:
        d1=d1_count(cells)
        if d1>best_d1: best_d1=d1; bd=cells
        # only pay for full total if d1 is high
        if d1>=44:
            d2=d2_count(cells); d3=d3_count(cells); tot=d1+d2+d3
            if tot>best_tot: best_tot=tot; bt=cells
    except Exception as e:
        pass
    if t%50==0: print(f'...{t}/{NT} best_d1={best_d1} best_tot={best_tot}',flush=True)
print(f'\\nSEARCH DONE ({NT} configs): best d1={best_d1} (cap 48?), best total={best_tot} (cap 67?)')
