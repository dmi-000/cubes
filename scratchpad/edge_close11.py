import numpy as np, itertools
exec(open("edge_close4.py").read().split("# locate s=0.06")[0])
delta=np.deg2rad(40.3060)

# 24 rotations of the cube group O
def gen_O():
    mats=set(); base=[np.eye(3)]
    axes=[np.array(a,float) for a in [(1,0,0),(0,1,0),(0,0,1),(1,1,1),(1,1,-1),(1,-1,1),(-1,1,1),
          (1,1,0),(1,-1,0),(1,0,1),(1,0,-1),(0,1,1),(0,1,-1)]]
    Rs=[np.eye(3)]
    for _ in range(4):
        new=[]
        for R in Rs:
            for ax in axes:
                for th in (np.pi/2,np.pi,2*np.pi/3):
                    K=ax/np.linalg.norm(ax)
                    Km=np.array([[0,-K[2],K[1]],[K[2],0,-K[0]],[-K[1],K[0],0]])
                    Q=np.eye(3)+np.sin(th)*Km+(1-np.cos(th))*(Km@Km)
                    new.append(R@Q)
        Rs=Rs+new
        uniq=[]
        for R in Rs:
            Ri=np.rint(R)
            if np.abs(R-Ri).max()<1e-9 and abs(np.linalg.det(Ri)-1)<1e-9:
                key=tuple(Ri.flatten().astype(int))
                if key not in mats: mats.add(key); uniq.append(Ri)
        Rs=uniq
        if len(uniq)==24: break
    return [np.array(k).reshape(3,3).astype(float) for k in mats]
O=gen_O(); print("O group size:",len(O))

def invariant(mats):
    # multiset over pairs of the O-reduced relative-rotation angle spectrum
    vals=[]
    for i in range(len(mats)):
        for j in range(i+1,len(mats)):
            Rrel=mats[i].T@mats[j]
            best=max(np.trace(Rrel@H) for H in O)
            vals.append(round(best,9))
    return sorted(vals)

S_end0=Rx45; S_end1=rot(AX,delta)@Rx45
E0=[S_end0,C@S_end0,C@C@S_end0]; E1=[S_end1,C@S_end1,C@C@S_end1]
inv0=invariant(E0); inv1=invariant(E1)
print("t=0 invariant:",inv0)
print("t=1 invariant:",inv1)
sols=np.load("edge_close_sols.npy")
for k,x in enumerate(sols):
    M=expso3(x)@S0; mats=[M,C@M,C@C@M]
    print(f"sol{k}:",invariant(mats))
# and the 2-condition min-norm solution
M2c=np.load("edge_close_M.npy"); mats=[M2c,C@M2c,C@C@M2c]
print("2-cond 1.66deg sol:",invariant(mats))
