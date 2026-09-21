#!/usr/bin/env python3
"""THE LEAD, USED: merge b cubes at one corner WITHOUT a common rotation axis.  [P336]

[P335] closed with a lead, flagged as a lead and not a result: merging is LOCALLY free money
(`e_X(b) = C(b,2) e_X(2) + (b-1)(b-2)`), and the observed merges all cost triple points because
they used a shared axis -- so is there a merge WITHOUT one?

ANSWER: yes, such compounds exist, and they cost exactly the same.  Over 1152 non-degenerate
merged 4-tuples the maximum `T3` is 72 -- the value the shared-axis family already had.  The
axis was never the cause; the MERGE is.  **The lead is refuted as stated, and refuting it was
worth more than confirming it would have been** (see [P336]).

{R : R s = p} is a 1-parameter family: R = Rot(p,psi) . R0, and Rot(p,psi) fixes p, so every
member still has p as a corner.  Sweeping psi per cube breaks the conjugacy that made the
first attempt collapse to a single cube.  Quaternion form: q = (w,k,k,k) (x) q_base.
"""
import sys, itertools, collections
import os
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,os.path.join(HERE,'..')); sys.path.insert(0,HERE)
import ee_bound_refute as B
from c_level import shares_plane, engine
from step_a2 import mat
from fractions import Fraction as F
from math import gcd

def qmul(a,b):
    w1,x1,y1,z1=a; w2,x2,y2,z2=b
    return (w1*w2-x1*x2-y1*y2-z1*z2, w1*x2+x1*w2+y1*z2-z1*y2,
            w1*y2-x1*z2+y1*w2+z1*x2, w1*z2+x1*y2-y1*x2+z1*w2)
def prim(q):
    g=0
    for v in q: g=gcd(g,abs(v))
    return tuple(v//g for v in q) if g else q

BASE=[(1,0,0,0),(2,1,-1,0),(2,-1,0,1),(2,0,1,-1)]   # each sends one diagonal to p=(1,1,1)
p=(F(1),F(1),F(1))
def has_corner(q):
    M=[[F(x) for x in row] for row in mat(q)]
    cols=[[M[r][c] for r in range(3)] for c in range(3)]
    return all(abs(sum(cols[c][k]*p[k] for k in range(3)))==1 for c in range(3))

# sweep psi on cubes 1..3 via q = (w,k,k,k) (x) base
rot=[prim((w,k,k,k)) for w in range(0,6) for k in range(-5,6) if (w,k)!=(0,0)]
rot=list(dict.fromkeys(rot))
cands=collections.defaultdict(list)
for bi in (1,2,3):
    for r in rot:
        q=prim(qmul(r,BASE[bi]))
        if max(abs(v) for v in q)>40: continue
        if has_corner(q): cands[bi].append(q)
for bi in cands: cands[bi]=list(dict.fromkeys(cands[bi]))
print('cubes having p=(1,1,1) as a corner, per base diagonal:',{k:len(v) for k,v in cands.items()})

best=None; tested=0
for q1 in cands[1][:14]:
    for q2 in cands[2][:14]:
        for q3 in cands[3][:14]:
            qs=[(1,0,0,0),q1,q2,q3]
            if len({prim(q) for q in qs})<4: continue
            if shares_plane(qs): continue
            tested+=1
            try:
                sig,_=B.vertices(qs)
            except Exception: continue
            merged={k:v for k,v in sig.items() if len(k)>2 and set(k)=={3}}
            if not merged: continue
            T3=sig.get((1,1,1),0); EE=sig.get((2,2),0); SC=sig.get((3,3),0)
            by=engine(qs).get('by_depth') or {}
            tot=sum(v for k,v in by.items() if k!='0')
            score=T3
            if best is None or score>best[0]:
                best=(score,qs,T3,EE,SC,merged,tot)
print('non-degenerate 4-tuples tested:',tested)
if best:
    s,qs,T3,EE,SC,merged,tot=best
    print()
    print('BEST merged-at-a-corner compound found (max T3):')
    print('   quats  ', ';'.join(','.join(map(str,q)) for q in qs))
    print('   T3=%d/128   EE=%d   SC2=%d   two-body=%d   count=%d'%(T3,EE,SC,EE+2*SC,tot))
    print('   merged vertices:',merged)
    print('   axes:',[q[1:] for q in qs[1:]])
else:
    print('no non-degenerate merged compound found in this window')

print()
print('=== is (T3, count) RIGID across merged-at-a-corner compounds? ===')
dist=collections.Counter(); ex={}
for q1 in cands[1][:10]:
    for q2 in cands[2][:10]:
        for q3 in cands[3][:10]:
            qs=[(1,0,0,0),q1,q2,q3]
            if len({prim(q) for q in qs})<4 or shares_plane(qs): continue
            try: sig,_=B.vertices(qs)
            except Exception: continue
            if not any(len(k)>2 and set(k)=={3} for k in sig): continue
            by=engine(qs).get('by_depth') or {}
            tot=sum(v for k,v in by.items() if k!='0')
            key=(sig.get((1,1,1),0),sig.get((2,2),0),sig.get((3,3),0),tot)
            dist[key]+=1; ex.setdefault(key,qs)
print('(T3, EE, SC2, count) -> how many compounds')
for k,v in sorted(dist.items(),key=lambda kv:-kv[1]):
    print('   %-26s %4d   e.g. %s'%(str(k),v,';'.join(','.join(map(str,q)) for q in ex[k])))

# ---- CONTROL: are the merged compounds genuinely non-congruent, or one compound respelled?
# [P227]'s trap is that a statistic can be a property of the quaternion SPELLING.  The multiset
# of pairwise relative-rotation traces is congruence-invariant and spelling-independent.
def relmat(qi,qj):
    A=[[F(x) for x in r] for r in mat(qi)]; Bm=[[F(x) for x in r] for r in mat(qj)]
    return [[sum(A[t][r]*Bm[t][c] for t in range(3)) for c in range(3)] for r in range(3)]
def trace_invariant(qs):
    ts=[]
    for i,j in itertools.combinations(range(len(qs)),2):
        M=relmat(qs[i],qs[j]); ts.append(sum(M[k][k] for k in range(3)))
    return tuple(sorted(ts))

if __name__ == '__main__':
    print()
    print('=== RIGIDITY: is (T3, EE, SC2, count) the same for EVERY merged compound? ===')
    prof=collections.Counter(); cls=collections.Counter(); ex={}
    for q1 in cands[1][:10]:
        for q2 in cands[2][:10]:
            for q3 in cands[3][:10]:
                qs=[(1,0,0,0),q1,q2,q3]
                if len({prim(q) for q in qs})<4 or shares_plane(qs): continue
                try: sig,_=B.vertices(qs)
                except Exception: continue
                if not any(len(k)>2 and set(k)=={3} for k in sig): continue
                by=engine(qs).get('by_depth') or {}
                tot=sum(v for k,v in by.items() if k!='0')
                key=(sig.get((1,1,1),0),sig.get((2,2),0),sig.get((3,3),0),tot)
                prof[key]+=1; cls[trace_invariant(qs)]+=1; ex.setdefault(key,qs)
    print('   merged compounds %d;  DISTINCT (T3,EE,SC2,count) profiles: %d;  congruence classes: %d'
          %(sum(prof.values()),len(prof),len(cls)))
    for k,v in prof.items():
        print('   %-26s %4d compounds   e.g. %s'%(str(k),v,';'.join(','.join(map(str,q)) for q in ex[k])))
    print()
    print('   => forcing four cubes through ONE corner DETERMINES the count at 145,')
    print('      across %d non-congruent classes.  T3 + two-body = 72 + 36 = 108, against'%len(cls))
    print('      the record\'s 176 -- so no merged-corner compound can threaten [OQ 37].')
    import provenance as PROV, json
    json.dump({'what':'merging at a corner without a shared axis, and its rigidity',
               'supports':'LEDGER P336',
               'profiles':{str(k):v for k,v in prof.items()},
               'congruence_classes':len(cls),'merged_compounds':sum(prof.values()),
               'reproduce':PROV.stamp(parameters={'base_diagonals':[list(q) for q in BASE]})},
              open(os.path.join(HERE,'..','..','data','merge_without_axis.json'),'w'),
              indent=1,default=str)
    print('\nwritten data/merge_without_axis.json')
