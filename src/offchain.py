#!/usr/bin/env python3
"""Is the extension chain the only route? Extend NON-record bases.

At n = 4 the record 183 contains no 67 -- its best triple is 63, four short --
so the tower took a WORSE sub-configuration to reach a better total.  Every hunt
in this project fixes the (n-1) record as a base, which cannot find that.

Test: extend n = 6 configurations counting 717-725 rather than 727, and see what
n = 7 they reach.  If any gets to 1217 or beyond, the chain is not unique.
"""
import json, math, os, random, subprocess, sys, time
HERE=os.path.dirname(os.path.abspath(__file__))
B=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
SIX={"727 (record)":(7,14,1,-5),"723":(5,2,2,2),"721":(1,-3,-2,10),
     "719":(7,0,-6,1),"717":(4,-4,4,1),"715":(1,1,1,-3)}
def batch(cfgs):
    inp="\n".join(";".join(",".join(map(str,q)) for q in c) for c in cfgs)+"\n"
    p=subprocess.run([os.path.join(HERE,"cube_regions_n"),"--quats-stdin"],
                     input=inp,capture_output=True,text=True)
    out=[]
    for l in p.stdout.splitlines():
        try: out.append(json.loads(l)["bounded"])
        except Exception: pass
    return out
def canon(q):
    g=0
    for v in q: g=math.gcd(g,abs(v))
    if g==0: return None
    q=tuple(v//g for v in q)
    for v in q:
        if v>0: break
        if v<0: q=tuple(-x for x in q); break
    return q if max(abs(v) for v in q)<=512 else None
def main():
    rng=random.Random(int(sys.argv[1]) if len(sys.argv)>1 else 5)
    log=open(os.path.join(HERE,"offchain.log"),"a")
    for name,six in SIX.items():
        base=B+[six]
        b0=batch([base])[0]
        best=0; t0=time.time(); seen=set()
        for rounds in range(12):
            cands=[]
            while len(cands)<400:
                h=rng.choice([4,8,16,40,100,250,512])
                q=canon(tuple(rng.randint(-h,h) for _ in range(4)))
                if q and q not in seen: seen.add(q); cands.append(q)
            for c,q in zip(batch([base+[q] for q in cands]),cands):
                if c>best: best=c; bq=q
        print("base %-14s (n=6 count %d) -> best n=7 from %d extensions: %d   %s"
              %(name,b0,len(seen),best,"** REACHES 1217 **" if best>=1217 else ""),
              file=log,flush=True)
if __name__=="__main__": main()
