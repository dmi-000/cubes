#!/usr/bin/env python3
"""Which member of the 723 CONTINUUM extends best?

183 extends an isolated 63, so "which member" has no content at n=4.  At n=6 it
does: 723 is a wrapping half-line with 11 type-chambers and 21 degrees of extent,
and the offchain run tested exactly ONE arbitrary point of it (reaching 1209).
Different members may extend differently -- that is the two-parameter problem.
"""
import json, math, os, random, subprocess, sys
from fractions import Fraction as F
HERE=os.path.dirname(os.path.abspath(__file__))
B=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
def batch(cfgs):
    inp="\n".join(";".join(",".join(map(str,q)) for q in c) for c in cfgs)+"\n"
    p=subprocess.run([os.path.join(HERE,"cube_regions_n"),"--quats-stdin"],
                     input=inp,capture_output=True,text=True)
    o=[]
    for l in p.stdout.splitlines():
        try: o.append(json.loads(l)["bounded"])
        except Exception: o.append(None)
    return o
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
    rng=random.Random(23); log=open(os.path.join(HERE,"member723.log"),"a")
    # the 723 half-line: sixth cube at Cayley u*(1,1,1), 723 for u >= 55 and u <= -7/2
    us=[F(-4),F(-5),F(-8),F(-20),F(-60),F(-200),F(60),F(100),F(200),F(400)]
    for u in us:
        six=canon((u.denominator,u.numerator,u.numerator,u.numerator))
        if six is None: continue
        base=B+[six]
        if batch([base])[0]!=723: continue
        best=0
        for r in range(6):
            cands=[]
            while len(cands)<250:
                h=rng.choice([4,8,16,40,100,250,512])
                q=canon(tuple(rng.randint(-h,h) for _ in range(4)))
                if q: cands.append(q)
            for c in batch([base+[q] for q in cands]):
                if c and c>best: best=c
        print("723 member u=%-8s six=%-18s -> best n=7 = %d %s"
              %(str(u),str(six),best,"*** BEATS 1217 ***" if best>1217 else ""),
              file=log,flush=True)
if __name__=="__main__": main()
