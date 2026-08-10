#!/usr/bin/env python3
"""Give ONE 1217-arc member the search that actually found a record.

The member sweep gave each arc member 1 200 random extensions and read the
resulting 1879-1893 as "members are interchangeable".  That inference does not
hold: 1 200 is the scale that succeeds at n=6->7, and n=7->8 needed far more
(1895 was missed for months).  So spend the search where it can decide -- take
the best-looking member, s = -9/200 (which reached 1893 on 1 200 candidates), and
run the near-symmetry family that found 2785: q = k*S + P over the 24 cube
symmetries, |P| <= 1.
"""
import itertools, json, math, os, subprocess, sys, time
from fractions import Fraction as F
HERE=os.path.dirname(os.path.abspath(__file__))
B=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
def q_of(c):
    L=1
    for v in c: L=L*v.denominator//math.gcd(L,v.denominator)
    iq=[L]+[int(v*L) for v in c]; g=0
    for v in iq: g=math.gcd(g,abs(v))
    return tuple(v//g for v in iq)
SIX=(7,14,1,-5)
c0=[F(-3,4)+F(-9,200),F(-1),F(-1)]
SEVEN=q_of(c0)
BASE=B+[SIX,SEVEN]
SYM=[q for q in itertools.product((-1,0,1),repeat=4) if any(q) and sum(v*v for v in q) in (1,2,4)]
def canon(q):
    g=0
    for v in q: g=math.gcd(g,abs(v))
    if g==0: return None
    q=tuple(v//g for v in q)
    for v in q:
        if v>0: break
        if v<0: q=tuple(-x for x in q); break
    return q if max(abs(v) for v in q)<=512 else None
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
def main():
    log=open(os.path.join(HERE,"n8_nearsym.log"),"a")
    print("base: 1217 arc member s=-9/200, seventh cube %s -> n=7 count %s"
          %(str(SEVEN),batch([BASE])[0]),file=log,flush=True)
    seen=set(); best=0; tried=0; t0=time.time(); buf=[]
    for k in range(1,401):
        for S in SYM:
            for P in itertools.product((-1,0,1),repeat=4):
                if not any(P): continue
                q=canon(tuple(k*S[i]+P[i] for i in range(4)))
                if q is None or q in seen: continue
                seen.add(q); buf.append(q)
                if len(buf)>=300:
                    for c,x in zip(batch([BASE+[y] for y in buf]),buf):
                        tried+=1
                        if c and c>best:
                            best=c
                            if c>1895:
                                print("*** BEATS 1895: %d  eighth cube %s"%(c,x),file=log,flush=True)
                    buf=[]
                    print("[%5.0fs] %6d tried, best %d"%(time.time()-t0,tried,best),file=log,flush=True)
if __name__=="__main__": main()
