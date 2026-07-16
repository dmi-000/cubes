import numpy as np, itertools
exec(open("edge_close4.py").read().split("# locate t")[0].split("# locate s=0.06")[0])
C=np.array([[0,0,1],[1,0,0],[0,1,0]],float)
one=np.array([1.0,1,1])/np.sqrt(3)

def seg_gap(c1,d1,c2,d2):
    w=c1-c2; b=d1@d2; f=w@d1; g=w@d2; den=1-b*b
    t1=np.clip((b*g-f)/den,-1,1) if abs(den)>1e-14 else 0.0
    t2=np.clip(b*t1+g,-1,1); t1=np.clip(b*t2-f,-1,1)
    return np.linalg.norm(c1+t1*d1-(c2+t2*d2)),t1,t2

def crossings(M,tol=1e-9):
    mats=[M,C@M,C@C@M]; out=[]
    for i in range(3):
        for j in range(i+1,3):
            for ei,(c1,d1) in enumerate(EDGES):
                for ej,(c2,d2) in enumerate(EDGES):
                    D1,D2=mats[i]@d1,mats[j]@d2
                    g,t1,t2=seg_gap(mats[i]@c1,D1,mats[j]@c2,D2)
                    if g<tol and abs(t1)<0.999 and abs(t2)<0.999:
                        p=mats[i]@c1+t1*D1
                        out.append((i,j,ei,ej,p,D1,D2))
    return out

M=np.load("edge_close_M.npy")
cr=crossings(M)
print(f"{len(cr)} exact crossings at the 1.66-deg solution")
seen=set()
for i,j,ei,ej,p,D1,D2 in cr:
    key=(i,j,ei,ej)
    print(f" cubes({i},{j}) edges({ei:2d},{ej:2d})  d1.(111)={D1@one:+.6f}  d2.(111)={D2@one:+.6f}   p.(111)={p@one:+.6f}  |p|={np.linalg.norm(p):.6f}")
