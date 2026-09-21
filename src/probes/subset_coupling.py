#!/usr/bin/env python3
"""The 3-SUBSET COUPLING: an argument that raising two-body PREVENTS raising T3.  [P338]

Claim:
  excess(v) depends only on v's SUPPORTING cubes, so for any 3-subset S the vertices supported
  inside S have the same excess in the full arrangement as in S's own 3-cube arrangement.
  Then max(3)=67 and TOTAL = 1+L+sum c+(1/2)sum excess with L=2, sum c >= 2 give

      Q(S) := (1/2) sum of excess over S-supported vertices  <=  67-1-2-2 = 62

WHY EXCESS IS INTRINSIC (the load-bearing step, argued then verified).  deg(v) counts the wall
ARCS through v.  An arc through v lies on ddA_i ^ ddA_j for two cubes whose boundaries contain
v -- i.e. two SUPPORTING cubes.  A non-supporting cube does not contain v on its boundary and so
contributes no arc through v.  And [P248] gives m_v = b_v - 1 levels, independent of n.  So both
the number of levels and the degree at each are properties of the supporting cubes alone, hence
so is excess(v) = sum_levels (deg - 2).

TEST 1 verifies exactly that, by recomputing each vertex's excess inside the sub-arrangement of
its own supporting cubes: 0 mismatches in 936 vertices over records AND degenerate families.
TEST 2 checks Q(S) <= 62 directly.

THE CONSEQUENCE.  Summing Q(S) over all 3-subsets counts each triple point once and each pair
(n-2) times, so

    T3 + (n-2) * two-body  <=  62 * C(n,3)

and since (n-2)*C(n,2) = 3*C(n,3), the right side is EXACTLY 32*C(n,3) + 10*(n-2)*C(n,2) --
the two known caps, summed.  **So attaining both caps at once is equivalent to every 3-subset
attaining Q(S) = 62, i.e. to every 3-subset being a 67-maximiser.**
"""
import sys, itertools, collections
import os
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,os.path.join(HERE,'..')); sys.path.insert(0,HERE)
import ee_bound_refute as B
from c_level import shares_plane, engine
import wall_keys as W

def excess_map(qs):
    """point -> (supporting cube indices within qs, measured excess)"""
    import euler3, cellcomplex
    from euler3 import rowsT, frames, segments
    from cellcomplex import on_bdry_params
    from c_level import strictly_inside
    Ms=[rowsT(R) for R in frames(qs)]; n=len(qs)
    deg=collections.defaultdict(collections.Counter)
    for i,j in itertools.combinations(range(n),2):
        for p,d,lo,hi in segments(Ms[i],Ms[j]):
            cuts=sorted({lo,hi}|{t for k in range(n) if k not in (i,j) for t in on_bdry_params(p,d,lo,hi,Ms[k])})
            for a,b in zip(cuts,cuts[1:]):
                if a>=b: continue
                mid=tuple(p[z]+((a+b)/2)*d[z] for z in range(3))
                s=sum(1 for k in range(n) if k not in (i,j) and strictly_inside(mid,Ms[k]))
                for t in (a,b): deg[s+1][tuple(p[z]+t*d[z] for z in range(3))]+=1
    exc=collections.Counter()
    for ell,dd in deg.items():
        for P,g in dd.items(): exc[P]+=g-2
    out={}
    for P in exc:
        sup=[]
        for idx,M in enumerate(Ms):
            h=[abs(sum(M[r][z]*P[z] for z in range(3))) for r in range(3)]
            if all(v<=1 for v in h) and any(v==1 for v in h): sup.append(idx)
        out[P]=(tuple(sup),exc[P])
    return out

def test(lbl,qs):
    n=len(qs)
    full=excess_map(qs)
    # TEST 1: recompute each vertex's excess inside its own supporting sub-arrangement
    bad=0; checked=0
    subcache={}
    for P,(sup,e) in full.items():
        if len(sup)<2 or len(sup)>3: continue
        key=tuple(sup)
        if key not in subcache: subcache[key]=excess_map([qs[i] for i in key])
        sub=subcache[key]
        if P in sub:
            checked+=1
            if sub[P][1]!=e: bad+=1
    # TEST 2: Q(S) for every 3-subset
    worst=0; rows=[]
    for S in itertools.combinations(range(n),3):
        q=0
        for P,(sup,e) in full.items():
            if set(sup)<=set(S) and len(sup)>=2: q+=e
        q//=2
        rows.append((S,q)); worst=max(worst,q)
    print('%-26s vertices re-checked in sub-arrangement: %3d   MISMATCHES: %d'%(lbl,checked,bad))
    print('%-26s Q(S) over 3-subsets: %s   max %d   (claim <= 62)  %s'
          %('',[q for _,q in rows],worst,'OK' if worst<=62 else '*** VIOLATED ***'))
    return worst

test('n=4 RECORD',[tuple(q) for q in W.REC[4]])
test('K4-ish merged',[(1,0,0,0),(1,-7,-8,0),(2,-13,0,-11),(1,0,-4,-5)])
test('body-diagonal',[(1,0,0,0),(3,1,1,1),(2,1,1,1),(5,2,2,2)])
test('face-diagonal',[(1,0,0,0),(3,2,2,0),(5,4,4,0),(4,3,3,0)])
test('n=5 RECORD',[tuple(q) for q in W.REC[5]])

from math import comb
print()
print('=== the aggregate is EXACTLY the two known caps summed ===')
for n in range(3,9):
    a=62*comb(n,3); b=32*comb(n,3); c=10*(n-2)*comb(n,2)
    print('   n=%-2d  62*C(n,3)=%-6d  32*C(n,3)+10*(n-2)*C(n,2)=%-6d  %s'%(n,a,b+c,'EQUAL' if a==b+c else 'DIFFER'))
print('   because (n-2)*C(n,2) = 3*C(n,3).')
print()
print('   => both caps attained  <=>  every 3-subset attains Q(S)=62  <=>  every 3-subset is a 67.')
