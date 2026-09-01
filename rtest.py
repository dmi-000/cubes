#!/usr/bin/env python3
"""Does a LESS constrained added cube give a HIGHER count? A test that can fail.

[P206](LEDGER.md#p206) noticed that in both same-n pairs the winning record has the
less constrained added cube (r=1 vs r=2), where r is the rank of the tight-wall
gradients on that cube's own three columns. Two pairs is not a pattern.

There is already a counter-indication: **727's added cube has r = 3**, the MAXIMUM,
and 727 is the n=6 record. So if the correlation were general it would already be
broken. This measures it properly instead of arguing.

DESIGN. Fix the base at 393's five cubes. Vary the sixth cube over a sample spanning a
range of counts. For each, compute r (rank of the wall gradients on the sixth cube's
columns) and the region count, then correlate. Cheap enough at n=6 to sample honestly.

GATE: the record sixth cube (7,14,1,-5) must return count 727 and r = 3.
"""
import json, random, subprocess, sys
sys.path.insert(0,'.')
from fractions import Fraction as F
from math import gcd
import sympy as sp
import dimension as D
from eps_null import walls_and_null

BASE=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]

def canon(q):
    g=0
    for v in q: g=gcd(g,abs(v))
    if g==0: return None
    q=tuple(v//g for v in q)
    for v in q:
        if v>0: break
        if v<0: q=tuple(-x for x in q); break
    return q

def cnt(cfg):
    st=";".join(",".join(map(str,q)) for q in cfg)
    try: return json.loads(subprocess.run(['./cube_regions_n','--quats',st],
                capture_output=True,text=True).stdout)['bounded']
    except Exception: return None

def rank_of_added(cfg):
    pt,walls,null,ncols=walls_and_null(cfg)
    W=sp.Matrix([[sp.Rational(x) for x in w] for w in walls])
    j=len(cfg)-1                      # last cube
    return W[:,3*(j-1):3*j].rank(), ncols-W.rank()

rec=(7,14,1,-5)
c=cnt(BASE+[rec]); r,d=rank_of_added(BASE+[rec])
print('GATE: record sixth cube %s -> count %s, r = %d, deficit %d  %s'
      %(str(rec),c,r,d,'OK' if (c==727 and r==3) else 'FAILED'),flush=True)
if not (c==727 and r==3): sys.exit('gate failed')

rnd=random.Random(9)
cands=set()
while len(cands)<70:
    q=canon(tuple(rnd.randint(-9,9) for _ in range(4)))
    # w = 0 is a half-turn: it has NO Cayley representation, so point_of returns
    # None and the wall computation cannot run. Excluded, and the exclusion is a
    # property of the CHART, not of the configuration.
    if q and q[0]!=0 and max(map(abs,q))<=9: cands.add(q)
scored=[]
for q in cands:
    v=cnt(BASE+[q])
    if v: scored.append((v,q))
scored.sort(reverse=True)
pick=scored[:6]+scored[len(scored)//2-3:len(scored)//2+3]+scored[-6:]
seen=set(); pick=[p for p in pick if p[1] not in seen and not seen.add(p[1])]
print('\n%d candidates counted; measuring r on %d spanning the range'%(len(scored),len(pick)),flush=True)
print('   %-18s %6s %4s %8s'%('sixth cube','count','r','deficit'),flush=True)
rows=[]
skipped=0
for v,q in pick:
    try:
        r,d=rank_of_added(BASE+[q])
    except Exception as e:
        skipped+=1; print('   %-18s %6d   UNEVALUATED (%s)'%(str(q),v,type(e).__name__),flush=True)
        continue
    rows.append((v,r,q))
    print('   %-18s %6d %4d %8d'%(str(q),v,r,d),flush=True)
rows.append((727,3,rec))
print('   (%d candidates unevaluated)'%skipped,flush=True)
print('\nby r:',flush=True)
for rv in (1,2,3):
    g=[x[0] for x in rows if x[1]==rv]
    if g: print('   r=%d : %d cubes, counts %d..%d, mean %.0f'%(rv,len(g),min(g),max(g),sum(g)/len(g)),flush=True)
import statistics
if len({x[1] for x in rows})>1:
    cs=[x[0] for x in rows]; rs=[x[1] for x in rows]
    print('\nrank correlation (count vs r): %.3f'%statistics.correlation(cs,rs,method='ranked'),flush=True)
    print('hypothesis predicts NEGATIVE (lower r -> higher count)',flush=True)
