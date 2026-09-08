#!/usr/bin/env python3
"""EXTEND THE 67s -- never attempted, because they are irrational.

183 was found by rational hill-climbing and contains no 67 (its best triple is
63).  So nobody has ever asked the obvious question: what do you get by adding a
fourth cube to an actual n = 3 record?  The 67s live in Q(sqrt2) and Q(sqrt5), so
the fourth cube is searched in the same ring and counted with cube_regions_q2w.

A same-axis fourth member gives 133 (the single-axis family caps low).  The
ledger's own finding is that records are family pairs GLUED ACROSS DIFFERENT
AXES, so the fourth cube must leave the axis -- which is what this searches.
"""
import json, os, random, subprocess, sys, time
HERE=os.path.dirname(os.path.abspath(__file__))
BASES={2:[((1,0),(0,0),(0,0),(0,0)),((1,0),(1,0),(0,1),(0,0)),((-1,0),(1,0),(0,1),(0,0))],
       5:[((1,0),(0,0),(0,0),(0,0)),((2,0),(1,1),(-1,1),(0,0)),((-2,0),(1,1),(-1,1),(0,0))]}
def batch(cfgs,d):
    inp="\n".join(";".join(",".join("%d:%d"%t for t in q) for q in c) for c in cfgs)+"\n"
    p=subprocess.run([os.path.join(HERE,"cube_regions_q2w"),"--d",str(d),"--quats-stdin"],
                     input=inp,capture_output=True,text=True)
    out=[]
    for l in p.stdout.splitlines():
        try: out.append((json.loads(l)["bounded"],l))
        except Exception: pass
    return out
def main():
    rng=random.Random(int(sys.argv[1]) if len(sys.argv)>1 else 31)
    log=open(os.path.join(HERE,"extend67.log"),"a")
    for d in (2,5):
        base=BASES[d]; best=0; tot=0; t0=time.time()
        for rnd in range(40):
            cfgs=[]
            for _ in range(300):
                h=rng.choice([2,3,4,6,9])
                q=tuple((rng.randint(-h,h),rng.randint(-h,h)) for _ in range(4))
                if all(c==(0,0) for c in q): continue
                cfgs.append(base+[q])
            for c,line in batch(cfgs,d):
                tot+=1
                if c>best:
                    best=c
                    if c>183:
                        print("*** d=%d BEATS 183: %d   %s"%(d,c,line[:150]),file=log,flush=True)
            print("d=%d  [%4.0fs] %6d counted, best %d %s"
                  %(d,time.time()-t0,tot,best,"** BEATS 183 **" if best>183 else ""),
                  file=log,flush=True)
if __name__=="__main__": main()
