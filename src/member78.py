#!/usr/bin/env python3
"""Extend the n=7 and n=8 CONTINUA, not just their record representatives.

1895 was found by extending one point of the 1217 arc; 2785 by extending one
point of the 1895 plateau.  Both loci are continua, exactly characterised:

    1217   cube 7 Cayley x, s in (-0.045258752, +0.002550224), 32 chambers
    1895   cube 8 Cayley z, s in (-0.025621840, +0.101360158), 29 chambers

Which member to extend has never been varied at either level.
"""
import json, math, os, random, subprocess, sys, time
from fractions import Fraction as F
HERE=os.path.dirname(os.path.abspath(__file__))
B=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
N7=B+[(7,14,1,-5),(4,-3,-4,-4)]
N8=N7+[(24,-24,24,-61)]
def q_of(c):
    L=1
    for v in c: L=L*v.denominator//math.gcd(L,v.denominator)
    iq=[L]+[int(v*L) for v in c]; g=0
    for v in iq: g=math.gcd(g,abs(v))
    return tuple(v//g for v in iq)
def batch(cfgs):
    inp="\n".join(";".join(",".join(map(str,q)) for q in c) for c in cfgs)+"\n"
    m=max(abs(v) for c in cfgs for q in c for v in q)
    eng=[os.path.join(HERE,"cube_regions_n"),"--quats-stdin"] if m<=512 else \
        [os.path.join(HERE,"cube_regions_q2w"),"--d","0","--quats-stdin"]
    p=subprocess.run(eng,input=inp,capture_output=True,text=True)
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
def sweep(base, ci, axis, lo, hi, hold, target, label, rng, log):
    c0=[F(base[ci][k+1],base[ci][0]) for k in range(3)]
    for m in range(11):
        s=lo+(hi-lo)*F(m,10)
        c=list(c0); c[axis]+=s
        q=q_of(c)
        if max(abs(v) for v in q)>512: continue
        bb=[base[k] if k!=ci else q for k in range(len(base))]
        if batch([bb])[0]!=hold: continue
        best=0
        for r in range(6):
            cands=[]
            while len(cands)<200:
                h=rng.choice([4,8,16,40,100,250,512])
                x=canon(tuple(rng.randint(-h,h) for _ in range(4)))
                if x: cands.append(x)
            for v in batch([bb+[x] for x in cands]):
                if v and v>best: best=v
        print("%s member s=%-12s -> best = %d %s"%(label,str(s)[:12],best,
              "*** BEATS %d ***"%target if best>target else ""),file=log,flush=True)
def main():
    rng=random.Random(41); log=open(os.path.join(HERE,"member78.log"),"a")
    sweep(N7,6,0,F(-45,1000),F(25,10000),1217,1895,"n=7 1217",rng,log)
    sweep(N8,7,2,F(-25,1000),F(100,1000),1895,2785,"n=8 1895",rng,log)
if __name__=="__main__": main()
