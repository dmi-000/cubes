import numpy as np
from scipy.spatial import HalfspaceIntersection, ConvexHull
from scipy.optimize import linprog
def Rx(t):c,s=np.cos(t),np.sin(t);return np.array([[1,0,0],[0,c,-s],[0,s,c]])
def Ry(t):c,s=np.cos(t),np.sin(t);return np.array([[c,0,s],[0,1,0],[-s,0,c]])
def Rz(t):c,s=np.cos(t),np.sin(t);return np.array([[c,-s,0],[s,c,0],[0,0,1]])
def planes(R): return [(R[:,a]*s,1.0) for a in range(3) for s in (1,-1)]
def poly_stats(P12):  # halfspaces for intersection: n.x<=h -> [n,-h]
    hs=np.array([[*n,-h] for (n,h) in P12])
    # interior pt
    norm=np.linalg.norm(hs[:,:-1],axis=1)
    r=linprog([0,0,0,-1],A_ub=np.hstack([hs[:,:-1],norm[:,None]]),b_ub=-hs[:,-1],bounds=[(None,None)]*3+[(0,None)],method='highs')
    if not r.success or r.x[3]<1e-9: return None
    hi=HalfspaceIntersection(hs,r.x[:3]); V=hi.intersections
    # merge duplicate vertices
    uniq=[]
    for v in V:
        if not any(np.linalg.norm(v-u)<1e-6 for u in uniq): uniq.append(v)
    V=np.array(uniq)
    hull=ConvexHull(V)
    # degree of each vertex = number of distinct faces (hull.equations) it lies on
    F=hull.equations
    deg=[]
    for v in V:
        onf=sum(1 for e in F if abs(e[:3]@v+e[3])<1e-6)
        deg.append(onf)
    from collections import Counter
    dc=Counter(deg)
    nF=len({tuple(np.round(e,5)) for e in F})
    return len(V),nF,dict(sorted(dc.items())),sum(d-3 for d in deg)
def report(name,cubes):
    print(f'=== {name} ===')
    tot4=0; tot6w=0
    for (i,j) in [(0,1),(0,2),(1,2)]:
        s=poly_stats(planes(cubes[i])+planes(cubes[j]))
        if s is None: print(f'  pair {i}{j}: empty'); continue
        V,F,dc,exc=s
        print(f'  pair {i}{j}: V={V} F={F} deg-spectrum={dc}  Sum(deg-3)={exc}  deg4={dc.get(4,0)} deg6={dc.get(6,0)}')
        tot4+=dc.get(4,0)
    print(f'  total deg-4 (edge-edge) over 3 pairs = {tot4}  [bound: <=30]')
report('octahedral',[Rx(np.pi/4),Ry(np.pi/4),Rz(np.pi/4)])
phi=(1+np.sqrt(5))/2
S=np.array([[phi/2,0.5,1/(2*phi)],[0.5,-1/(2*phi),-phi/2],[-1/(2*phi),phi/2,-0.5]])
report('golden',[np.eye(3),S,S@S])
