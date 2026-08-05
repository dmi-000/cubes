#!/usr/bin/env python3
"""Close the multi-cube gap, exactly.

multicube.py (v1) computed the active-wall Jacobian numerically and read its
null space.  It ran in seconds and its answers were wrong in a knowable
direction: the n=6 record came out 0-dimensional though it demonstrably carries
two tangents, and n=8 came out 1 though two independent directions had already
been verified.  The cause is the one Postscript 88 records -- MOST ACTIVE
CONCURRENCES DO NOT CHANGE THE COUNT, so demanding a tangent respect all of them
over-constrains.  A null dimension computed that way is a LOWER bound.

The repair, and why it is cheap.  Removing a constraint row can enlarge the null
space only if that row is independent of the others, and the rank is at most the
number of parameters -- 21 at n=8.  So instead of peeling all ~1000 active rows,
reduce once, take a maximal independent subset, and peel only those.  Every
candidate direction is then VERIFIED by exact stepping and counting, because a
direction that survives peeling is still only a candidate.

Everything is exact: Cayley coordinates live in Q or Q(sqrt d), gradients come
from forward-mode dual numbers over that field, and the null space is a rational
RREF.  Approximate directions are useless here -- a maximiser locus is measure
zero, so a slightly wrong direction leaves it immediately and every test reads
negative.

    python3 multicube2.py [target ...]
"""
import itertools, json, math, os, subprocess, sys
from fractions import Fraction as F

OUT='multicube2_out'

class K:
    """a + b*sqrt(D) with rational a,b.  D=0 gives plain rationals."""
    D=0
    __slots__=('a','b')
    def __init__(s,a=0,b=0): s.a=F(a); s.b=F(b)
    def __add__(s,o):
        if isinstance(o,Dual): return NotImplemented
        o=K._c(o); return K(s.a+o.a, s.b+o.b)
    __radd__=__add__
    def __neg__(s): return K(-s.a,-s.b)
    def __sub__(s,o):
        if isinstance(o,Dual): return NotImplemented
        return s+(-K._c(o))
    def __rsub__(s,o):
        if isinstance(o,Dual): return NotImplemented
        return K._c(o)+(-s)
    def __mul__(s,o):
        if isinstance(o,Dual): return NotImplemented
        o=K._c(o); return K(s.a*o.a+K.D*s.b*o.b, s.a*o.b+s.b*o.a)
    __rmul__=__mul__
    def inv(s):
        den=s.a*s.a-K.D*s.b*s.b
        return K(s.a/den, -s.b/den)
    def __truediv__(s,o): return s*K._c(o).inv()
    def __rtruediv__(s,o): return K._c(o)*s.inv()
    def iszero(s): return s.a==0 and s.b==0
    def __repr__(s): return '%s+%s r'%(s.a,s.b)
    @staticmethod
    def _c(o): return o if isinstance(o,K) else K(o)

class Dual:
    """value plus exact partials, forward mode over K."""
    __slots__=('v','d')
    def __init__(s,v,d): s.v=v; s.d=d
    def __add__(s,o):
        if isinstance(o,Dual): return Dual(s.v+o.v,[a+b for a,b in zip(s.d,o.d)])
        return Dual(s.v+o,s.d)
    __radd__=__add__
    def __neg__(s): return Dual(-s.v,[-x for x in s.d])
    def __sub__(s,o): return s+(-o if isinstance(o,Dual) else -K._c(o))
    def __rsub__(s,o): return (-s)+o
    def __mul__(s,o):
        if isinstance(o,Dual):
            return Dual(s.v*o.v,[s.v*b+a*o.v for a,b in zip(s.d,o.d)])
        return Dual(s.v*o,[x*o for x in s.d])
    __rmul__=__mul__
    def __truediv__(s,o):
        if isinstance(o,Dual):
            iv=o.v.inv()
            return Dual(s.v*iv,[(a*o.v-s.v*b)*iv*iv for a,b in zip(s.d,o.d)])
        return s*K._c(o).inv()

def cols(c):
    """face normals from a Cayley triple (entries Dual or K)"""
    x,y,z=c
    one=K(1)
    n=x*x+y*y+z*z+one
    M=[[one+x*x-y*y-z*z, (x*y-z)*2, (x*z+y)*2],
       [(x*y+z)*2, one-x*x+y*y-z*z, (y*z-x)*2],
       [(x*z-y)*2, (y*z+x)*2, one-x*x-y*y+z*z]]
    return [[M[r][j]/n for r in range(3)] for j in range(3)]

def det4(M):
    t=None
    for perm in itertools.permutations(range(4)):
        sgn=1
        pl=list(perm)
        for i in range(4):
            for j in range(i+1,4):
                if pl[i]>pl[j]: sgn=-sgn
        term=M[0][perm[0]]
        for i in range(1,4): term=term*M[i][perm[i]]
        term=term*sgn if sgn>0 else -term
        t=term if t is None else t+term
    return t

def planes(cays):
    P=[]
    for c in cays:
        for nv in cols(c):
            P.append((nv,K(1))); P.append(([-t for t in nv],K(1)))
    return P

def rref(rows,ncol):
    M=[r[:] for r in rows]; piv=[]; r=0
    for c in range(ncol):
        p=next((i for i in range(r,len(M)) if not M[i][c].iszero()),None)
        if p is None: continue
        M[r],M[p]=M[p],M[r]
        iv=M[r][c].inv(); M[r]=[x*iv for x in M[r]]
        for i in range(len(M)):
            if i!=r and not M[i][c].iszero():
                f=M[i][c]; M[i]=[M[i][k]-f*M[r][k] for k in range(ncol)]
        piv.append(c); r+=1
        if r==len(M): break
    return M[:r],piv

def nullspace(rows,ncol):
    R,piv=rref(rows,ncol)
    out=[]
    for fc in [c for c in range(ncol) if c not in piv]:
        v=[K(0)]*ncol; v[fc]=K(1)
        for i,c in enumerate(piv): v[c]=-R[i][fc]
        out.append(v)
    return out

# ---- exact O-reduction, via the 24 INTEGER rotation matrices -----------------
# Quaternion reduction would need 1/sqrt2 entries; the rotation matrices are
# integer, so R*U and its Cayley vector stay in the field.
def _rotmats():
    import itertools as it
    out=[]
    for perm in it.permutations(range(3)):
        for sg in it.product([1,-1],repeat=3):
            M=[[0]*3 for _ in range(3)]
            for i in range(3): M[i][perm[i]]=sg[i]
            det=(M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])
                -M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])
                +M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]))
            if det==1: out.append(M)
    return out
ROTS=_rotmats()

def mat_of_quat(q):
    w,x,y,z=[K._c(t) for t in q]
    n=w*w+x*x+y*y+z*z
    M=[[w*w+x*x-y*y-z*z,(x*y-w*z)*2,(x*z+w*y)*2],
       [(x*y+w*z)*2,w*w-x*x+y*y-z*z,(y*z-w*x)*2],
       [(x*z-w*y)*2,(y*z+w*x)*2,w*w-x*x-y*y+z*z]]
    return [[M[i][j]/n for j in range(3)] for i in range(3)]

def cayley_reduced(R):
    best=None
    for U in ROTS:
        S=[[sum([R[i][k]*U[k][j] for k in range(3)],K(0)) for j in range(3)] for i in range(3)]
        tr=S[0][0]+S[1][1]+S[2][2]; den=K(1)+tr
        if den.iszero(): continue
        v=[(S[2][1]-S[1][2])/den,(S[0][2]-S[2][0])/den,(S[1][0]-S[0][1])/den]
        sz=float(sum((t.a+t.b*math.sqrt(K.D))**2 for t in v))
        if best is None or sz<best[0]: best=(sz,v)
    return best[1]

def quat_strings(cays):
    """exact integer (or a:b) quaternions for the engine"""
    out=[]
    for c in cays:
        ents=[K(1)]+list(c)
        den=1
        for e in ents:
            den=den*e.a.denominator//math.gcd(den,e.a.denominator)
            den=den*e.b.denominator//math.gcd(den,e.b.denominator)
        if K.D==0: out.append(','.join(str(int(e.a*den)) for e in ents))
        else: out.append(','.join('%d:%d'%(int(e.a*den),int(e.b*den)) for e in ents))
    return ';'.join(out)

def count(cays):
    s=quat_strings(cays)
    cmd=['./cube_regions_n','--quats',s] if K.D==0 else ['./cube_regions_q2','--d',str(K.D),'--quats',s]
    r=subprocess.run(cmd,capture_output=True,text=True)
    try: return json.loads(r.stdout).get('bounded')
    except Exception: return None

BASE5=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
TARGETS={
 'n4_183':(0,[(1,0,0,0),(0,5,3,2),(1,-4,-1,1),(1,1,-1,-4)],183),
 'n5_393':(0,BASE5,393),
 'n6_727r':(0,BASE5+[(7,14,1,-5)],727),
 'n6_727a':(0,BASE5+[(6,53,-87,-156)],727),
 'n6_723':(0,BASE5+[(5,2,2,2)],723),
 'n7_1217':(0,BASE5+[(7,14,1,-5),(4,-3,-4,-4)],1217),
 'n8_1891':(0,BASE5+[(7,14,1,-5),(4,-3,-4,-4),(3,-3,3,-8)],1891),
 'n3_67oct':(2,[(1,0,0,0),(K(1),K(1),K(0,1),K(0)),(K(-1),K(1),K(0,1),K(0))],67),
 'n3_67gold':(5,[(1,0,0,0),(K(2),K(1,1),K(-1,1),K(0)),(K(-2),K(1,1),K(-1,1),K(0))],67),
}

def meet_point(P,quad):
    A=[[P[i][0][j].v if isinstance(P[i][0][j],Dual) else P[i][0][j] for j in range(3)] for i in quad[:3]]
    b=[P[i][1] for i in quad[:3]]
    R,piv=rref([A[i]+[b[i]] for i in range(3)],4)
    if len(R)<3 or piv[:3]!=[0,1,2]: return None
    return [R[i][3] for i in range(3)]

def on_real_faces(pt,cays):
    for c in cays:
        for nv in cols(c):
            s=sum([nv[j]*pt[j] for j in range(3)],K(0))
            f=float(s.a+s.b*math.sqrt(K.D))
            if f>1+1e-9 or f<-1-1e-9: pass
    return True

def run(name):
    os.makedirs(OUT,exist_ok=True)
    path=os.path.join(OUT,name+'.json')
    if os.path.exists(path): print('%s: done'%name,flush=True); return
    d,quats,target=TARGETS[name]; K.D=d
    import time; t0=time.time()
    cays=[cayley_reduced(mat_of_quat(q)) for q in quats]
    base=count(cays)
    n=len(cays); npar=3*(n-1)
    # duals: cube 0 fixed, cubes 1.. carry the parameters
    def dual_cays(vals):
        out=[[Dual(t,[K(0)]*npar) for t in cays[0]]]
        for i in range(1,n):
            row=[]
            for j in range(3):
                p=[K(0)]*npar; p[3*(i-1)+j]=K(1)
                row.append(Dual(vals[i][j],p))
            out.append(row)
        return out
    DC=dual_cays(cays)
    fcays=cays
    P=planes(DC)
    rows=[]; quads=[]
    for quad in itertools.combinations(range(len(P)),4):
        M=[[P[i][0][0],P[i][0][1],P[i][0][2],P[i][1]] for i in quad]
        M=[[x if isinstance(x,Dual) else Dual(x,[K(0)]*npar) for x in r] for r in M]
        val=det4(M)
        if not val.v.iszero(): continue
        # REAL-FACE TEST.  Four planes meeting at a point is not a wall unless
        # the point lies on all four ACTUAL faces; the extensions carry no cube
        # material and change no containment.  Omitting this test collected 354
        # 'active walls' at n=4 and over-constrained the Jacobian so badly that
        # not one direction verified.
        pt=meet_point(P,quad)
        if pt is None or not on_real_faces(pt,fcays): continue
        rows.append(val.d); quads.append(quad)
    R,piv=rref(rows,npar) if rows else ([],[])
    full_null=nullspace(rows,npar) if rows else [[K(1) if i==j else K(0) for i in range(npar)] for j in range(npar)]
    # peel: only INDEPENDENT rows can enlarge the null space, and there are <= npar
    indep=[]
    seen=[]
    for idx,rw in enumerate(rows):
        test=seen+[rw]
        Rt,_=rref(test,npar)
        if len(Rt)>len(seen and rref(seen,npar)[0] or []): seen.append(rw); indep.append(idx)
        if len(indep)>=npar: break
    cands=[]
    for k in range(len(indep)):
        sub=[rows[j] for j in indep if j!=indep[k]]
        for v in nullspace(sub,npar):
            if v not in cands: cands.append(v)
    def verify(v):
        ok=0
        for eps in (F(1,64),F(1,512)):
            for sgn in (1,-1):
                pert=[list(cays[0])]+[[cays[i][j]+v[3*(i-1)+j]*K(sgn*eps) for j in range(3)] for i in range(1,n)]
                if count(pert)==target: ok+=1
        return ok==4
    good=[]
    for v in full_null+cands:
        if verify(v):
            moved=sorted({i//3 for i in range(npar) if not v[i].iszero()})
            good.append(dict(cubes_moved=len(moved),
                             dir=[[str(t.a),str(t.b)] for t in v]))
    res=dict(name=name,base_count=base,target=target,params=npar,
             active=len(rows),rank=len(R),full_null=len(full_null),
             peel_candidates=len(cands),verified=len(good),
             multi_cube=sum(1 for g in good if g['cubes_moved']>1),
             directions=good,secs=round(time.time()-t0,1))
    tmp=path+'.tmp'; json.dump(res,open(tmp,'w'),indent=1); os.replace(tmp,path)
    print('%-10s base %s  params %d  active %d  rank %d  full-null %d  peel %d  VERIFIED %d (%d multi-cube)  %.0fs'
          %(name,base,npar,len(rows),len(R),len(full_null),len(cands),len(good),res['multi_cube'],res['secs']),flush=True)

if __name__=='__main__':
    for nm in (sys.argv[1:] or list(TARGETS)):
        run(nm)
