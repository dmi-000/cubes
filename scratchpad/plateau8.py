import sys, json, subprocess
from fractions import Fraction as F
sys.path.insert(0,'.')
from axis_sweep import q_of, cay
BASE=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
REC=BASE+[(7,14,1,-5),(4,-3,-4,-4),(24,-24,24,-61)]
def cnt_pl(cfg):
    s=";".join(",".join(map(str,q)) for q in cfg)
    m=max(abs(v) for q in cfg for v in q)
    cmd=["/Users/dmi/cube-compounds/cube_regions_n","--quats",s] if m<=512 else ["/Users/dmi/cube-compounds/cube_regions_q2w","--d","0","--quats",s]
    o=json.loads(subprocess.run(cmd,capture_output=True,text=True).stdout)
    pl=o["per_label"]
    return o["bounded"],tuple(pl.get(str(k),0) for k in range(2**len(cfg)))
c0=cay(REC[7])
rows=[]
for k in range(-64,65):
    s=F(k,512)
    c=list(c0); c[2]+=s
    cfg=[REC[i] if i!=7 else q_of(c) for i in range(8)]
    rows.append((s,)+cnt_pl(cfg))
prev=None
for s,cnt,pl in rows:
    if cnt!=prev: print("  count %-6s from s=%s"%(cnt,s)); prev=cnt
hits=[r for r in rows if r[1]==1895]
ch=0; pv=None
for s,cnt,pl in rows:
    if cnt==1895:
        if pl!=pv: ch+=1; pv=pl
    else: pv=None
print("1895 on s in [%s,%s] of the sampled window, %d chambers, %d of %d samples"%(hits[0][0],hits[-1][0],ch,len(hits),len(rows)))
