#!/usr/bin/env python3
"""Does the FIELD explain shells?  Q(sqrt2) vs Q(sqrt5), away from the 67s.

The octahedral 67 (Q(sqrt2)) has 0 shells in 728 neighbouring faces; the golden
67 (Q(sqrt5)) has 148 in 2196.  Symmetry, size and codimension are eliminated
(Postscript 127).  The field is the last standing explanation -- but with only two
configurations, ANY binary property of the pair explains it equally well.

Postscript 128 removed that blocker in principle by showing irrational maximisers
are plentiful.  This tests the field hypothesis directly and at scale: random
3-cube configurations in each field, counted exactly, and the EVEN fraction
compared.  An even count is a shell (Postscript 121).

    field hypothesis  ->  Q(sqrt5) shows a higher even rate than Q(sqrt2)
    null              ->  the two rates agree

This is a SAMPLE, so it bounds nothing; it is a test of a stated difference, and
a large gap or its absence is informative either way.
"""
import json, os, random, subprocess, sys
import os as _os
HERE=_os.path.dirname(_os.path.abspath(__file__))
ENG=os.path.join(HERE,'cube_regions_q2w')

def batch(cfgs,d):
    inp="\n".join(";".join(",".join("%d:%d"%t for t in q) for q in c) for c in cfgs)+"\n"
    p=subprocess.run([ENG,'--d',str(d),'--quats-stdin'],input=inp,capture_output=True,text=True)
    out=[]
    for l in p.stdout.splitlines():
        try: out.append(json.loads(l)['bounded'])
        except Exception: pass
    return out

def main():
    rng=random.Random(int(sys.argv[1]) if len(sys.argv)>1 else 11)
    N=int(sys.argv[2]) if len(sys.argv)>2 else 4000
    res={}
    for d in (2,5):
        cfgs=[]
        while len(cfgs)<N:
            c=[((1,0),(0,0),(0,0),(0,0))]
            ok=True
            for _ in range(2):
                h=rng.choice([2,3,4,6])
                q=tuple((rng.randint(-h,h),rng.randint(-h,h)) for _ in range(4))
                if all(t==(0,0) for t in q): ok=False; break
                c.append(q)
            if ok: cfgs.append(c)
        cs=[x for x in batch(cfgs,d) if x is not None]
        ev=sum(1 for x in cs if x%2==0)
        res[d]={'counted':len(cs),'even':ev,'rate':ev/max(len(cs),1),
                'even_values':sorted(set(x for x in cs if x%2==0))[:12]}
        print('d=%d: %5d counted, %4d EVEN (%.2f%%)  even values %s'
              %(d,len(cs),ev,100*ev/max(len(cs),1),res[d]['even_values']),flush=True)
    json.dump(res,open(os.path.join(HERE,'shell_field.json'),'w'),indent=1)
    r2,r5=res[2]['rate'],res[5]['rate']
    print('\nQ(sqrt5) even rate / Q(sqrt2) even rate = %.2f'%(r5/r2 if r2 else float('inf')))
    print('field hypothesis predicts >> 1; null predicts ~1')

if __name__=='__main__': main()
