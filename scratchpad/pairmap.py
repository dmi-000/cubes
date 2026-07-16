import numpy as np, itertools
exec(open("edge_close4.py").read().split("# locate s=0.06")[0])
sh=np.array([1.0,1,1])/np.sqrt(3)
A=np.array([1.0,-1,0])/np.sqrt(2); B=np.array([1.0,1,-2])/np.sqrt(6)
def cubeM(th,ps):
    u=np.cos(th)*A+np.sin(th)*B
    w=np.cross(sh,u)
    return np.column_stack([np.cos(ps)*w+np.sin(ps)*sh,-np.sin(ps)*w+np.cos(ps)*sh,u])
E_C=np.array([e[0] for e in EDGES]); E_D=np.array([e[1] for e in EDGES])
def pair_valid(dth,ps,strict=0.9999):
    MA=cubeM(0.0,ps); MB=cubeM(dth,ps)
    C1=E_C@MA.T; D1=E_D@MA.T; C2=E_C@MB.T; D2=E_D@MB.T
    # all 144 pairs vectorized
    c1=C1[:,None,:]; d1=D1[:,None,:]; c2=C2[None,:,:]; d2=D2[None,:,:]
    w=c1-c2
    b=np.sum(d1*d2,axis=2); f=np.sum(w*d1,axis=2); g=np.sum(w*d2,axis=2)
    den=1-b*b
    t1=np.where(np.abs(den)>1e-14,np.clip((b*g-f)/np.where(np.abs(den)>1e-14,den,1),-1,1),0.0)
    t2=np.clip(b*t1+g,-1,1); t1=np.clip(b*t2-f,-1,1)
    P=c1+t1[:,:,None]*d1; Q=c2+t2[:,:,None]*d2
    gap=np.linalg.norm(P-Q,axis=2)
    interior=(gap<1e-9)&(np.abs(t1)<strict)&(np.abs(t2)<strict)
    contact=(gap<1e-9)   # includes corner touches
    return interior,contact

PSI_OCT=np.arcsin(1/np.sqrt(3)); PHI=(1+np.sqrt(5))/2; PSI_G=np.arctan(PHI*PHI)
D120=np.deg2rad(120)
io,co=pair_valid(D120,PSI_OCT); ig,cg=pair_valid(D120,PSI_G)
oct_lab=set(zip(*np.where(io))); gold_int=set(zip(*np.where(ig))); gold_con=set(zip(*np.where(cg)))
print(f"oct pair: interior labels={len(oct_lab)}; golden pair: interior={len(gold_int)}, contacts(incl corner)={len(gold_con)}")
print(f"oct ∩ golden-contacts = {len(oct_lab & gold_con)}  (labels that COULD be carried end-to-end)")
core=oct_lab & gold_con
extras=oct_lab - gold_con
print(f"oct extras NOT in golden contact set: {len(extras)}")

# region structure: for each oct label, map validity over (dth, psi) grid
dths=np.deg2rad(np.arange(0,360,1.0)); pss=np.deg2rad(np.arange(2,89,0.5))
nl=len(oct_lab); labs=sorted(oct_lab)
V=np.zeros((len(dths),len(pss),nl),bool)
for a_,dt in enumerate(dths):
    for b_,ps in enumerate(pss):
        I,_=pair_valid(dt,ps)
        for k,(ei,ej) in enumerate(labs): V[a_,b_,k]=I[ei,ej]
    # progress
np.save("pair_V.npy",V); np.save("pair_labs.npy",np.array(labs))
cnt=V.sum(axis=2)
print("\ncount map c(dth,psi): max =",cnt.max()," at:")
mx=np.argwhere(cnt==cnt.max())[:5]
for a_,b_ in mx: print(f"  dth={np.rad2deg(dths[a_]):.0f} psi={np.rad2deg(pss[b_]):.1f}")
print("count at (120, psi_oct-grid), (120, psi_gold-grid):",
      cnt[120, int(round((35.264-2)/0.5))], cnt[120, int(round((69.095-2)/0.5))])
# how many of oct's 10 labels are valid on large regions (area fraction)?
print("\nper-label validity area fraction and value at (120,50deg):")
for k,(ei,ej) in enumerate(labs):
    frac=V[:,:,k].mean()
    tag="CORE" if (ei,ej) in core and V[120,int(round((50-2)/0.5)),k] else ""
    print(f"  label ({ei:2d},{ej:2d}): area={frac:.3f} in-goldcontact={(ei,ej) in gold_con} {tag}")
