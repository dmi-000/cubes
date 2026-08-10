#!/usr/bin/env python3
"""Is 183 beaten by an IRRATIONAL n=4 configuration?

Continua contain irrationals, so a rational record on a continuum is not evidence
of anything -- the 727 arcs carry members in every Q(sqrt d), d <= 97, all
counting 727.  What rational search genuinely cannot reach is an ISOLATED
irrational optimum, which is exactly what n = 3 is: dimension 0, two classes,
both irrational, and rational search caps at 63.

n = 4 and n = 5 also have 0-dimensional maximisers, and the Q(sqrt d) campaign was
only ever run at n = 6.  So this is the untested case.
"""
import json, os, random, subprocess, sys, time
HERE=os.path.dirname(os.path.abspath(__file__))
def batchq(cfgs,d):
    inp="\n".join(";".join(",".join("%d:%d"%c for c in q) for q in cfg) for cfg in cfgs)+"\n"
    p=subprocess.run([os.path.join(HERE,"cube_regions_q2w"),"--d",str(d),"--quats-stdin"],
                     input=inp,capture_output=True,text=True)
    out=[]
    for l in p.stdout.splitlines():
        try: out.append((json.loads(l)["bounded"], l))
        except Exception: pass
    return out
def main():
    rng=random.Random(int(sys.argv[1]) if len(sys.argv)>1 else 11)
    log=open(os.path.join(HERE,"irr4.log"),"a")
    for d in (2,3,5,6,7,10,13):
        best=0; tot=0; t0=time.time()
        for rounds in range(8):
            cfgs=[]
            for _ in range(250):
                cfg=[((1,0),(0,0),(0,0),(0,0))]
                for _ in range(3):
                    cfg.append(tuple((rng.randint(-4,4),rng.randint(-3,3)) for _ in range(4)))
                cfgs.append(cfg)
            for c,line in batchq(cfgs,d):
                tot+=1
                if c>best:
                    best=c
                    if c>183: print("*** d=%d BEATS 183: %d  %s"%(d,c,line[:160]),file=log,flush=True)
        print("d=%-3d  %5d counted in %4.0fs   best %-5d %s"
              %(d,tot,time.time()-t0,best,"** BEATS 183 **" if best>183 else ""),file=log,flush=True)
if __name__=="__main__": main()
