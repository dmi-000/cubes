#!/usr/bin/env python3
"""The n = 5 chain's budget per sharing structure: how much room is left for glued-patch hole
terms and charging deficits.  [P437]

A structure is a set of CLASSES (sets of >= 2 cubes sharing one face plane), any two meeting in at
most one cube (two shared planes make two cubes identical). Unrealisable ones (triangles,
4-cycles, [P419]) are included: a superset.

With H1′ (no deficit), L2′/L3′ with hole terms H, and the top-level tree
`c4′ <= d4 + p4 − 1` (PROOF_N5 Part 4.4):

    total  <=  181 + Σ_tri cap2(S) + Σ_4 cap3(S) − 24 + Σ_S p_S − 2p4 + 2c4′ − d4 + H
           <=  155 + Σ_tri cap2(S) + Σ_4 cap3(S) + Σ_S p_S + cap4 + H,

where:
- `cap(S) = 6|S| − 2·Σ_{classes with k >= 2 members in S} k` (strengthened ANCHOR, [P413]);
- `p_S <= 2` per class with >= 2 members in S (one convex or star-shaped piece per ±n; merging
  only lowers it).

ROOM = 485 − (that without H). One sharing pair gives base 469, matching Part 4.

Output: data/budget_n5_structures.json.
"""
import os, json
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import itertools
N=5
cubes=range(N)
cands=[frozenset(c) for k in range(2,6) for c in itertools.combinations(cubes,k)]
structs=set()
def ok(cl):
    for a,b in itertools.combinations(cl,2):
        if len(a&b)>1: return False
    return True
def canon(cl):
    best=None
    for perm in itertools.permutations(cubes):
        key=tuple(sorted(tuple(sorted(perm[x] for x in c)) for c in cl))
        if best is None or key<best: best=key
    return best
for r in range(1,6):
    for cl in itertools.combinations(cands,r):
        if ok(cl):
            npairs=sum(len(c)*(len(c)-1)//2 for c in cl)
            if npairs>=2 or r>=2 or any(len(c)>=3 for c in cl):
                structs.add(canon(cl))
def cap(S,cl,base):
    return base-2*sum(len(set(S)&set(c)) for c in cl if len(set(S)&set(c))>=2)
def patches(S,cl):
    return 2*sum(1 for c in cl if len(set(S)&set(c))>=2)
rows=[]
for st in structs:
    cl=[set(c) for c in st]
    tri=sum(cap(S,cl,18) for S in itertools.combinations(cubes,3))
    four=sum(cap(S,cl,24) for S in itertools.combinations(cubes,4))
    ps=sum(patches(S,cl) for S in itertools.combinations(cubes,3))+sum(patches(S,cl) for S in itertools.combinations(cubes,4))
    c4=cap(tuple(cubes),cl,30)
    base=155+tri+four+ps+c4
    rows.append((485-base,st,tri,four,ps,c4,base))
rows.sort()


for r in rows:
    print('room %4d  base %3d  classes %s  (tri %d, four %d, patches %d, d4 cap %d)' % (r[0], r[6], r[1], r[2], r[3], r[4], r[5]))
print('%d structures; minimum room %d' % (len(rows), rows[0][0]))
json.dump([{'room': r[0], 'base': r[6], 'classes': r[1], 'tri': r[2], 'four': r[3], 'patches': r[4], 'd4cap': r[5]}
           for r in rows], open(os.path.join(ROOT, 'data', 'budget_n5_structures.json'), 'w'), indent=1)
