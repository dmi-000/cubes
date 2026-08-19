#!/usr/bin/env python3
"""Do (1,1,1,1) walls -- four face planes from FOUR DIFFERENT cubes concurrent --
actually pass through the records?

WHY THIS MATTERS.  Every Jacobian in this project is built from Step A (pairs of
normals) and Step B (triples), so a condition can name at most THREE cubes BY
CONSTRUCTION.  Measured on the tower (`wall_support.py`): every one of the 18,
27, 51, 75, 99 walls at n = 5..9 involves 2 or 3 cubes and none involves 4.  That
is a property of the INSTRUMENT, not evidence about the geometry, and Postscript
57 lists (1,1,1,1) as a genuine codimension-1 type -- with 12 real 4-plane/
4-cube points already found in the 393 base.

If such a wall passes through a record, the record lies on MORE walls than the
Jacobian knows, so the measured rank is too low and the measured lineality too
high.  Isolation conclusions are unaffected (a larger search space returning
EMPTY still gives empty), but the rank/lineality NUMBERS would be wrong.

METHOD.  Directly, with no reference to the condition machinery: take all face
planes of all n cubes, enumerate concurrent plane triples, and for each resulting
point ask how many DISTINCT CUBES have a real face through it -- real meaning the
point lies in the closed cube, not merely on the infinite plane extension.  A
point with 4 planes from 4 distinct cubes IS a (1,1,1,1) coincidence.
"""
import collections, itertools, json, os, sys
from fractions import Fraction as F
import os as _os
HERE=_os.path.dirname(_os.path.abspath(__file__)); sys.path.insert(0,HERE)

BASE=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
R={3:BASE[:3],4:BASE[:4],5:BASE,6:BASE+[(7,14,1,-5)]}
R[7]=R[6]+[(4,-3,-4,-4)]; R[8]=R[7]+[(24,-24,24,-61)]; R[9]=R[8]+[(56,56,55,56)]

def mat(q):
    w,x,y,z=[F(v) for v in q]; n=w*w+x*x+y*y+z*z
    return [[(w*w+x*x-y*y-z*z)/n,2*(x*y-w*z)/n,2*(x*z+w*y)/n],
            [2*(x*y+w*z)/n,(w*w-x*x+y*y-z*z)/n,2*(y*z-w*x)/n],
            [2*(x*z-w*y)/n,2*(y*z+w*x)/n,(w*w-x*x-y*y+z*z)/n]]

def planes(cfg):
    """(normal, offset, cube) for all 6 faces of each cube"""
    out=[]
    for c,q in enumerate(cfg):
        M=mat(q)
        for a in range(3):
            nrm=[M[i][a] for i in range(3)]
            for s in (1,-1):
                out.append(([s*t for t in nrm],F(1),c))
    return out

def det3(a,b,c):
    return (a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])
            +a[2]*(b[0]*c[1]-b[1]*c[0]))

def solve3(p,q,r):
    A=[p[0],q[0],r[0]]; d=det3(*A)
    if d==0: return None
    b=[p[1],q[1],r[1]]
    def rep(i):
        M=[row[:] for row in A]
        for k in range(3): M[k][i]=b[k]
        return det3(*M)
    return tuple(rep(i)/d for i in range(3))

def in_cube(pt,Mt):
    """is pt inside the closed cube with rotation whose transpose rows are Mt"""
    loc=[sum(Mt[i][k]*pt[k] for k in range(3)) for i in range(3)]
    return all(abs(v)<=1 for v in loc)

def run(n):
    cfg=R[n]; P=planes(cfg)
    mats=[mat(q) for q in cfg]
    trans=[[[M[k][i] for k in range(3)] for i in range(3)] for M in mats]
    pts=collections.defaultdict(set)
    for i,j,k in itertools.combinations(range(len(P)),3):
        s=solve3(P[i],P[j],P[k])
        if s is None: continue
        if max(abs(x) for x in s)>2: continue      # outside every unit cube
        pts[s]|={i,j,k}
    hist=collections.Counter(); quad=[]
    for s in pts:
        on=[t for t in range(len(P))
            if sum(P[t][0][u]*s[u] for u in range(3))==P[t][1]]
        cubes={P[t][2] for t in on}
        if not all(in_cube(s,trans[c]) for c in cubes): continue   # not REAL
        hist[(len(on),len(cubes))]+=1
        if len(on)>=4 and len(cubes)>=4:
            quad.append({'point':[str(x) for x in s],'planes':len(on),
                         'cubes':sorted(cubes)})
    return hist,quad

if __name__=='__main__':
    # MERGE, DO NOT OVERWRITE.  Running `check_4cube_walls.py 7 8 9` after
    # `... 5 6` replaced the file and silently destroyed the n=5 and n=6 entries
    # (2026-08-18); a delegated agent then had to substitute the n=7 list for
    # n=6.  Same class of failure as a shard output opened with 'w'.
    OUTF=os.path.join(HERE,'check_4cube_walls.json')
    out=json.load(open(OUTF)) if os.path.exists(OUTF) else {}
    for n in [int(x) for x in (sys.argv[1:] or ['5','6'])]:
        hist,quad=run(n)
        tot=sum(hist.values())
        print('n=%d: %d REAL concurrence points'%(n,tot),flush=True)
        for k in sorted(hist): print('     %d planes / %d cubes: %d'%(k[0],k[1],hist[k]))
        print('   (1,1,1,1)-type points [>=4 planes from >=4 distinct cubes]: %d'
              %len(quad),flush=True)
        for q in quad[:4]: print('      %s  cubes %s'%(q['point'],q['cubes']))
        out[n]={'hist':{str(k):v for k,v in hist.items()},'quad':quad}
        json.dump(out,open(OUTF,'w'),indent=1)
