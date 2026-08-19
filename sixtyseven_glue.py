#!/usr/bin/env python3
"""Solve for 4-cube compounds whose TRIPLES are 67s.

THE CONSTRAINT THAT POINTS HERE.  A record's subsets are all high: 183's triples
are [63,63,63,55], its pairs [13,13,13,9,9,9].  The maximum possible triple is 67
-- but 183 cannot contain one, because 67 needs irrational coordinates and every
subset of a rational compound is rational.  An IRRATIONAL 4-cube compound can.
No search has looked there: `extend67.py` samples a fourth cube against a FIXED
67 (11 927 tries, best 177), which is one triple, not several.

WHY THIS IS A SOLVE AND NOT A SEARCH.  The 67s are ISOLATED points -- full rank,
lineality 0 (Postscript 122/124).  So with two cubes fixed, the third cube making
that triple a 67 is determined up to finitely many completions.  Enumerating them
is exact.

METHOD.  Both 67s are known.  For each, and each ordered pair of its cubes, the
pair determines a congruence frame; mapping our fixed pair onto it yields the
third cube exactly.  Compose two such completions on a shared pair to get a
4-cube compound with (at least) two 67 triples, and count it.

Cube 0 is the identity throughout (global rotation is a gauge freedom).
"""
import itertools, json, os, subprocess, sys
from fractions import Fraction as F
import os as _os
HERE=_os.path.dirname(_os.path.abspath(__file__)); sys.path.insert(0,HERE)
from qfield import Q, rot as qrot, clear_denoms

REC={2:[((1,0),(0,0),(0,0),(0,0)),((1,0),(1,0),(0,1),(0,0)),((-1,0),(1,0),(0,1),(0,0))],
     5:[((1,0),(0,0),(0,0),(0,0)),((2,0),(1,1),(-1,1),(0,0)),((-2,0),(1,1),(-1,1),(0,0))]}

def qmul(a,b):
    w1,x1,y1,z1=a; w2,x2,y2,z2=b
    return (w1*w2-x1*x2-y1*y2-z1*z2, w1*x2+x1*w2+y1*z2-z1*y2,
            w1*y2-x1*z2+y1*w2+z1*x2, w1*z2+x1*y2-y1*x2+z1*w2)
def qconj(a): return (a[0],-a[1],-a[2],-a[3])

def count(cfgs,d):
    inp="\n".join(";".join(",".join("%d:%d"%t for t in q) for q in c) for c in cfgs)+"\n"
    p=subprocess.run([os.path.join(HERE,'cube_regions_q2w'),'--d',str(d),'--quats-stdin'],
                     input=inp,capture_output=True,text=True)
    out=[]
    for l in p.stdout.splitlines():
        try: out.append(json.loads(l)['bounded'])
        except Exception: out.append(None)
    return out

def norm(q,d):
    """primitive integer-pair form of a Q-quaternion"""
    _,ints=clear_denoms(list(q)); 
    from math import gcd
    g=0
    for a,b in ints: g=gcd(gcd(g,abs(a)),abs(b))
    return tuple((a//g,b//g) for a,b in ints) if g else tuple(ints)

def main():
    OCT=[]   # the 24 unit-quaternion rotations of the cube, as integer quaternions
    for s in itertools.product((1,-1),repeat=4):
        OCT.append((s[0],0,0,0)); OCT.append((0,s[0],0,0))
        OCT.append((0,0,s[0],0)); OCT.append((0,0,0,s[0]))
    for s in itertools.product((1,-1),repeat=4):
        OCT.append(s)
    for i,j in itertools.combinations(range(4),2):
        for si in (1,-1):
            for sj in (1,-1):
                v=[0,0,0,0]; v[i]=si; v[j]=sj; OCT.append(tuple(v))
    OCT=list(dict.fromkeys(OCT))
    print('octahedral quaternion candidates: %d'%len(OCT),flush=True)

    results=[]
    for d,base in REC.items():
        B=[tuple(Q(F(p),F(q),d) for p,q in quat) for quat in base]
        # completions of the pair (cube0, cube1) to a 67: apply g on the left so
        # that g*B[a] ~ B[0] and g*B[b] ~ B[1]; the image of the third cube is a
        # valid third cube for our fixed pair.
        cands=[]
        for a,b,c in itertools.permutations(range(3)):
            for u in OCT:
                for v in OCT:
                    U=tuple(Q(F(t),0,d) for t in u); V=tuple(Q(F(t),0,d) for t in v)
                    # g = B[0] * (B[a]*U)^-1  -- but conjugate suffices up to scale
                    g=qmul(B[0],qconj(qmul(B[a],U)))
                    t3=qmul(g,qmul(B[c],V))
                    if any(x.is_zero() for x in (t3[0],)) and all(x.is_zero() for x in t3):
                        continue
                    cands.append(norm(t3,d))
        cands=list(dict.fromkeys(cands))
        print('d=%d: %d distinct candidate third/fourth cubes'%(d,len(cands)),flush=True)
        # build 4-cube compounds: our 67 base plus each candidate as a 4th cube
        cfgs=[]; keep=[]
        for x in cands:
            if max(max(abs(p),abs(q)) for p,q in x)>60: continue
            cfgs.append([norm(q,d) for q in B]+[x]); keep.append(x)
        if not cfgs: continue
        cs=count(cfgs,d)
        ok=[(c,k) for c,k in zip(cs,keep) if c is not None]
        ref=sum(1 for c in cs if c is None)
        best=max((c for c,_ in ok),default=None)
        print('d=%d: %d counted, %d REFUSED, best %s (record 183)'%(d,len(ok),ref,best),flush=True)
        from collections import Counter
        print('   distribution %s'%dict(sorted(Counter(c for c,_ in ok).items(),reverse=True)),flush=True)
        results.append({'d':d,'counted':len(ok),'refused':ref,'best':best,
                        'best_cfg':[list(map(list,cfgs[[c for c,_ in ok].index(best)]))] if best else None})
    json.dump(results,open(os.path.join(HERE,'sixtyseven_glue.json'),'w'),indent=1)

if __name__=='__main__': main()
