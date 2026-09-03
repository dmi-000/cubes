#!/usr/bin/env python3
"""Iterated boundary climb: solve the region, walk out through its walls, repeat.

This is the loop that produced 3917 ([P191]) and then 3921 and 2787 ([P198]), made
self-sustaining. Per record:

  1. wall matrix -> null space -> LLL -> eps-verified PRESERVING basis (P196);
  2. directions = that basis and integer combinations, BOTH signs (regions are not
     symmetric: at 2785 one wall sits at 4.4e-6 and another at 0.101);
  3. for each direction, fine step 1/(D*M) and BISECT to the first count change —
     a coarse step lands past several walls and misreads the boundary (P198);
  4. every crossing is RECORDED with its (n-1)-subset signature and distance, so the
     facet census of each region comes free from the walk that was happening anyway —
     at termination the last census IS the local maximum's boundary, and no separate
     `record_boundaries.py` run is needed (it is superseded);
  5. any count ABOVE the record becomes the next base;
  6. before accepting, find a LOW-HEIGHT member of the new region by searching simple
     rationals along the same direction (METHODS 15), so both engines can verify it.

Every accepted record is gated: both engines agree, and the count is invariant under
three global rotations (it cannot depend on the counting box, P180).
"""
import json, random, subprocess, sys
sys.path.insert(0,'.')
from fractions import Fraction as F
from math import gcd
import sympy as sp
from qfield import Q
import dimension as D
from epscount import count_eps
from eps_null import walls_and_null
from lll import lll
from simplest import simplest_between

SIMPLE_H=4096      # above this height the dyadic representative is re-done by
SIMPLE_ROUNDS=4    # continued fractions, per coordinate (see simplify_point)
M=4096; NDIR=18; ROTS=((2,1,0,0),(1,1,1,0),(3,0,1,2))

def prim(v):
    den=1
    for x in v: den=den*F(x).denominator//gcd(den,F(x).denominator)
    iv=[int(F(x)*den) for x in v]; g=0
    for x in iv: g=gcd(g,abs(x))
    return tuple(x//(g or 1) for x in iv)

def canon(t):
    g=0
    for v in t: g=gcd(g,abs(v))
    t=tuple(v//(g or 1) for v in t)
    for v in t:
        if v>0: break
        if v<0: t=tuple(-x for x in t); break
    return t

def qmul(p,r):
    w,x,y,z=p; e,f,g_,h=r
    return (w*e-x*f-y*g_-z*h,w*f+x*e+y*h-z*g_,w*g_-x*h+y*e+z*f,w*h+x*g_-y*f+z*e)

def run(cfg,exe):
    st=";".join(",".join(map(str,q)) for q in cfg)
    cmd=[exe,'--quats',st] if exe.endswith('_n') else [exe,'--d','0','--quats',st]
    try:
        d=json.loads(subprocess.run(cmd,capture_output=True,text=True).stdout)
        return d['bounded']
    except Exception: return None

def cnt(cfg):
    c=run(cfg,'./cube_regions_n')
    return c if c is not None else run(cfg,'./cube_regions_q2w')

def cfg_at(pt,q0):
    D.set_field(0); D.QZERO[:]=[q0]
    out=[]
    for q in D.quats_of(list(pt),q0):
        iv=[F(x) for x in q]; L=1
        for x in iv: L=L*x.denominator//gcd(L,x.denominator)
        w=[int(x*L) for x in iv]; g=0
        for x in w: g=gcd(g,abs(x))
        out.append(tuple(x//(g or 1) for x in w))
    return out

def gate(cfg,c):
    """both engines and three global rotations, with UNEVALUABLE kept distinct.

    The old text scored a refusal as 'not rotation-invariant'. Those are different
    facts: a rotated configuration whose height exceeds the engine's chain budget
    says nothing about invariance, and calling it a failure is a negative result
    wearing a real one's clothes. Both still block acceptance -- an ungated count is
    not a record -- but the reason reported is now the true one, and a refusal points
    at the REPRESENTATIVE (see rerep) rather than at the mathematics."""
    a=run(cfg,'./cube_regions_n'); b=run(cfg,'./cube_regions_q2w')
    if b is None: return False,'wide engine UNEVALUATED (not a disagreement)'
    if b!=c or (a is not None and a!=c): return False,'engines disagree (%s,%s)'%(a,b)
    une=0
    for rot in ROTS:
        r=run([canon(qmul(rot,q)) for q in cfg],'./cube_regions_q2w')
        if r is None: une+=1; continue
        if r!=c: return False,'not rotation-invariant'
    if une: return False,'%d of %d rotations UNEVALUATED (not a disagreement)'%(une,len(ROTS))
    return True,'both engines + 3 rotations agree'


def rerep(pt,v,t1,c,q0,ncols):
    """simplest representative of the chamber the walk just entered, or None.

    Stepping just PAST the first wall is the right MOVE and the wrong POINT to keep.
    At a generic start the first wall is ~1e-6 away, so the crossing point carries the
    denominator of the bisection; at n=4 that gave height 1.1e8, every global rotation
    of it overflowed both engines, and gate() reported 'not rotation-invariant' for a
    configuration nothing had actually tested. The chamber is OPEN, so it contains a
    simple rational: find a far end of it along the same ray, take the simplest
    rational strictly between the two ends, and verify the count there. The anchor is
    the count itself, so a wrong guess is rejected rather than trusted."""
    at=lambda t: cfg_at([pt[i]+t*v[i] for i in range(ncols)],q0)
    hi=t1*2
    for _ in range(40):
        cc=cnt(at(hi))
        if cc is None or cc!=c: break
        hi*=2
    else:
        return None
    for _ in range(24):
        t=simplest_between(t1,hi)
        cf=at(t)
        if cnt(cf)==c: return t,cf
        hi=(t1+hi)/2
    return None


def simplify_point(pt,c,q0,ncols):
    """simplest point carrying this count, coordinate-wise.

    Height control is not cosmetic here, it is what stops the walk dying: `den` below
    is Dden*M, tied to the CURRENT representative's height, so a tall representative
    makes the next iteration's probes taller still, until both engines refuse every
    one of them -- and a refused probe reads to the walk as 'no crossing', i.e. as
    LOCAL MAXIMALITY. That runaway ended the first n=4 basin climb with a false
    'locally maximal' at height 1.6e6. Rounding every coordinate to the coarsest
    dyadic that still carries count c breaks it.

    This is a MOVE OF THE CLIMBER, declared as such: no claim is made that the
    simplified point lies in the same chamber, only that it carries the same count."""
    best=None
    for k in range(3,34):
        den=2**k
        p2=[F(round(x*den),den) for x in pt]
        cf=cfg_at(p2,q0)
        if cnt(cf)==c: best=(p2,cf); break
    if best is None: best=(list(pt),cfg_at(pt,q0))
    h=max(abs(x) for q in best[1] for x in q)
    if h<=SIMPLE_H: return best
    # DYADIC ROUNDING IS THE WRONG LATTICE and this is where the climbs were dying.
    # One denominator 2^k is shared by all 3(n-1) coordinates, so the single tightest
    # direction sets the height of every other one. Giving each coordinate its own
    # interval and its own CONTINUED-FRACTION simplest rational (simplify_box, via
    # simplest_between -- the same Stern-Brocot descent the endpoint solver uses) cut a
    # dead climb's representative from 44 462 to 2 697, 16x, and the climb that had
    # ended UNDETERMINED there then resumed 119 -> 123 -> 127 -> 131 with 0 of 24 rays
    # refused at every iteration. Tried only when the dyadic answer is expensive, since
    # it costs a slack bisection per coordinate.
    from simplify_box import simplify_box            # lazy: simplify_box imports climb
    p3=simplify_box(best[0],c,q0,ncols,rounds=SIMPLE_ROUNDS)
    cf3=cfg_at(p3,q0)
    if cnt(cf3)==c and max(abs(x) for q in cf3 for x in q)<h: return p3,cf3
    return best

REFUSED = []      # heights of probes both engines refused -- see climb.required_bits


def required_bits(h):
    """chain capacity a probe of coordinate height h needs, in bits.

    Measured, not assumed: bisecting each engine's refusal height gives
    cube_regions_n (capacity 2^112) refusing above 2^16.1 and cube_regions_q2w
    (capacity 2^240) above 2^28.5, so the pipeline grows as h^k with k = 6.96 and 8.41
    respectively. The wide engine binds, so k = 8.41 is used. This turns every refusal
    from "unevaluable" into a NUMBER -- the width that would have evaluated it -- which
    is what makes the cost of removing the ceiling estimable instead of arguable.
    """
    import math
    return 8.41 * math.log2(max(h, 2))


def first_crossing(pt,v,den,rec,q0,ncols,n,bsub):
    """Walk out along v to the FIRST wall and name it. Extracted from climb() so the
    facet walk uses the same walk rather than a second copy of it.

    Returns {'why', 't', 'count', 'sig', 'cfg'}. `why` distinguishes the four outcomes
    that must never be conflated: a crossing, no wall within t<=8, and the two ways the
    engine can REFUSE (before or after bisection). A refusal is not a wall and not its
    absence.
    """
    lo,hi,c=0,1,None
    while hi<=den*8:
        p2=[pt[i]+F(hi,den)*v[i] for i in range(ncols)]
        cf_=cfg_at(p2,q0)
        c=cnt(cf_)
        if c is None:
            REFUSED.append(max(abs(x) for q_ in cf_ for x in q_)); hi*=2; continue
        if c!=rec: break
        lo=hi; hi*=2
    if c is None: return {'why':'unevaluable'}
    if c==rec: return {'why':'no wall'}
    while hi-lo>1:
        mid=(lo+hi)//2
        cm=cnt(cfg_at([pt[i]+F(mid,den)*v[i] for i in range(ncols)],q0))
        if cm is None: break
        if cm==rec: lo=mid
        else: hi=mid
    p2=[pt[i]+F(hi,den)*v[i] for i in range(ncols)]
    full=cfg_at(p2,q0); c=cnt(full)
    if c is None:
        REFUSED.append(max(abs(x) for q_ in full for x in q_))
        return {'why':'unevaluable after bisection'}
    if c==rec: return {'why':'back at count'}
    sub=tuple(cnt([full[i] for i in range(n) if i!=j]) for j in range(n))
    sig=tuple(j for j in range(n) if sub[j]==bsub[j])
    return {'why':'crossed','t':F(hi,den),'count':c,'sig':sig,'cfg':full}


def climb(cubes,label,menu=None,iters=8,quiet=False):
    """walk out of the current region through its walls, repeat.

    `menu` selects the DIRECTION MENU, which is the only thing that changes between
    the record climb and a climb from a random start.  menu=None is the record climb:
    directions come from the null space of the tight walls, eps-verified to preserve
    the count.  That machinery is vacuous at a generic point -- a Haar-random
    configuration has 0 tight walls and nullity = ambient (measured, n=4: 0 walls,
    nullity 9 of 9) -- so a caller climbing from a random start passes
    menu(ncols,it) -> list of integer directions instead, and the expensive symbolic
    conditions step is skipped along with it.  Everything below the menu (the ray
    walk, the bisection to the FIRST crossing, the facet signature, the low-height
    re-representation, the two-engine + three-rotation gate) is shared, so a basin
    measured here is the basin of the climber that found the records."""
    for it in range(1,iters+1):
        n=len(cubes)
        Dden=max(abs(v) for v in cubes[-1]) or 1
        if menu is None:
            pt,walls,null,ncols=walls_and_null(cubes)
            rec=D.count_at(pt,n)
            print('\n[%s iter %d] record %d  deficit %d  height %d'
                  %(label,it,rec,len(null),max(abs(v) for q in cubes for v in q)),flush=True)
            B=[prim(b) for b in lll([list(prim(v)) for v in null])]
            good=[]
            for b in B:
                ok=True
                for sgn in (1,-1):
                    c=count_eps(pt,[Q(sgn*F(x),0,0) for x in b],0,cubes[0])
                    if c is None: c=count_eps(pt,[Q(sgn*F(x),0,0) for x in b],0,cubes[0],wide=True)
                    if c!=rec: ok=False; break
                if ok: good.append(b)
            if not good:
                print('   no preserving direction; stop'); return cubes,rec
            print('   preserving rank %d'%sp.Matrix([list(g) for g in good]).rank(),flush=True)
            rnd=random.Random(17+it)
            dirs=[tuple(g) for g in good]
            while len(dirs)<NDIR:
                co=[rnd.randint(-2,2) for _ in good]
                if any(co): dirs.append(prim([sum(a*g[i] for a,g in zip(co,good)) for i in range(ncols)]))
        else:
            D.set_field(0); D.QZERO[:]=[cubes[0]]
            pt=D.point_of(cubes); ncols=3*(n-1)
            if pt is None: return cubes,None
            rec=D.count_at(pt,n)
            dirs=menu(ncols,it)
            if not quiet:
                print('\n[%s iter %d] count %d  menu %d dirs  height %d'
                      %(label,it,rec,len(dirs),max(abs(v) for q in cubes for v in q)),flush=True)
        best=(rec,None); unev=0; crossed=0; nocross=0; unev_b=0; nocross_b=0
        facets={}
        base=cfg_at(pt,cubes[0])
        bsub=tuple(cnt([base[i] for i in range(n) if i!=j]) for j in range(n))
        den=Dden*M
        for v0 in dirs[:NDIR]:
            for sgn in (1,-1):
                v=tuple(sgn*x for x in v0)
                r=first_crossing(pt,v,den,rec,cubes[0],ncols,n,bsub)
                if r['why']=='unevaluable': unev+=1; continue
                if r['why']=='no wall': nocross+=1; continue
                crossed+=1
                if r['why']=='unevaluable after bisection': unev_b+=1; continue
                if r['why']=='back at count': nocross_b+=1; continue
                c,sig=r['count'],r['sig']
                if sig not in facets: facets[sig]=(float(r['t']),c)
                if c>best[0]:
                    best=(c,(v,r['t']))
                    print('   boundary crossing -> %d  (ABOVE %d)'%(c,rec),flush=True)
        print('   rays: %d of %d crossed, %d found no wall within t<=8, %d UNEVALUABLE'
              '  (after bisection: %d back at count, %d unevaluable)'
              %(crossed,2*len(dirs[:NDIR]),nocross,unev,nocross_b,unev_b),flush=True)
        print('   FACET CENSUS of this region: %d distinct walls'%len(facets),flush=True)
        for sig,(d,c) in sorted(facets.items(),key=lambda kv:kv[1][0]):
            print('      cubes %-16s at %.5g   count outside %d'%(str(list(sig)),d,c),flush=True)
        if best[1] is None and (unev or unev_b):
            print('   UNDETERMINED: %d of %d rays ended UNEVALUABLE (engine refused '
                  'every probe); this is NOT local maximality'%(unev+unev_b,2*len(dirs[:NDIR])),
                  flush=True)
            return cubes,None
        if best[1] is None:
            print('   no crossing above the record; region is locally maximal '
                  'OVER THE DIRECTIONS WALKED (not a proof — see facets.py for the '
                  'saturation curve and vertex probes)',flush=True)
            return cubes,rec
        c,(v,s)=best
        rr=rerep(pt,v,s,c,cubes[0],ncols)
        if rr is not None:
            t,cf=rr
            _,cf=simplify_point([pt[i]+t*v[i] for i in range(ncols)],c,cubes[0],ncols)
            ok,why=gate(cf,c)
            print('   NEW RECORD %d  height %d  gate: %s'
                  %(c,max(abs(x) for q in cf for x in q),why),flush=True)
            if not ok: return cubes,rec
            print('   %s'%';'.join(','.join(map(str,q)) for q in cf),flush=True)
            cubes=cf; continue
        cheap=None
        for q in range(2,200):
            for p in range(1,q):
                t=F(p,q)
                if abs(float(t)-float(s))>0.25*float(s) or t<=0: continue
                cf=cfg_at([pt[i]+t*v[i] for i in range(ncols)],cubes[0])
                h=max(abs(x) for qq in cf for x in qq)
                if cnt(cf)==c and (cheap is None or h<cheap[0]): cheap=(h,t,cf)
                break
        cf=cheap[2] if cheap else cfg_at([pt[i]+s*v[i] for i in range(ncols)],cubes[0])
        ok,why=gate(cf,c)
        print('   NEW RECORD %d  height %d  gate: %s'
              %(c,max(abs(x) for q in cf for x in q),why),flush=True)
        if not ok: return cubes,rec
        print('   %s'%';'.join(','.join(map(str,q)) for q in cf),flush=True)
        cubes=cf
    return cubes,rec

BASE=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
N9=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1),(7,14,1,-5),
    (4,-3,-4,-4),(168,-168,168,-415),(88787,-9061,74275,113786)]
N10=N9[:8]+[(57,57,56,57)]+[N9[8]]
if __name__=='__main__':
    climb(N9,'n=9')
    climb(N10,'n=10')
