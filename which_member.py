#!/usr/bin/env python3
"""WHICH member of a continuum to extend is itself a variable.

n = 3 is the model: the 67s are {I, R, R^2} with R a specific 120-degree rotation
on the n = 2 13-continuum.  Getting there means choosing the right member of the
continuum, not extending an arbitrary one -- and that choice is a solve.

Every extension hunt in this project fixed the (n-1) record at ONE point --
727 = BASE + (7,14,1,-5), a single member of arc D -- and varied only the new
cube.  This sweeps the base along its own arc as well: a two-parameter search
where only one parameter was ever explored.
"""
import json, math, os, random, subprocess, sys, time
from fractions import Fraction as F
HERE=os.path.dirname(os.path.abspath(__file__))
B=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
ARCS={"A":([F(19,3),F(-7),F(-11)],[F(1),F(-3),F(-6)],F(2100,1000),F(3160,1000)),
      "B":([F(4,35),F(2,5),F(-41,35)],[F(1),F(1),F(-4)],F(420,1000),F(578,1000)),
      "C":([F(245,29),F(-295,29),F(428,29)],[F(1),F(-3,2),F(9,4)],F(1200,1000),F(4700,100))}
def q_of(c):
    L=1
    for v in c: L=L*v.denominator//math.gcd(L,v.denominator)
    iq=[L]+[int(v*L) for v in c]; g=0
    for v in iq: g=math.gcd(g,abs(v))
    return tuple(v//g for v in iq)
def batch(cfgs):
    inp="\n".join(";".join(",".join(map(str,q)) for q in c) for c in cfgs)+"\n"
    p=subprocess.run([os.path.join(HERE,"cube_regions_n"),"--quats-stdin"],
                     input=inp,capture_output=True,text=True)
    out=[]
    for l in p.stdout.splitlines():
        try: out.append(json.loads(l)["bounded"])
        except Exception: out.append(None)
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
    rng=random.Random(int(sys.argv[1]) if len(sys.argv)>1 else 17)
    log=open(os.path.join(HERE,"which_member.log"),"a")
    for name,(a0,d,lo,hi) in ARCS.items():
        for m in range(9):
            s=lo+(hi-lo)*F(m,8)
            six=q_of([a0[k]+s*d[k] for k in range(3)])
            if max(abs(v) for v in six)>512: continue
            base=B+[six]
            if batch([base])[0]!=727: continue
            best=0
            for r in range(4):
                cands=[]
                while len(cands)<250:
                    h=rng.choice([4,8,16,40,100,250,512])
                    q=canon(tuple(rng.randint(-h,h) for _ in range(4)))
                    if q: cands.append(q)
                for c in batch([base+[q] for q in cands]):
                    if c and c>best: best=c
            print("arc %s  s=%-10s six=%-22s -> best n=7 = %d %s"
                  %(name,str(s)[:10],str(six),best,"*** BEATS 1217 ***" if best>1217 else ""),
                  file=log,flush=True)
if __name__=="__main__": main()
