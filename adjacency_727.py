#!/usr/bin/env python3
"""Classify the 727 plateau by REGION ADJACENCY, not by region counts.

The plateau holds at least 600 configurations (Postscript 52 addendum 4) but
only three DEPTH profiles, and every class count so far has measured the
instrument rather than the plateau: depth profile (3), O-reduced pair invariant
(12), per-label vector (>=21).  Adjacency is the finest invariant the project
can currently compute -- two arrangements can distribute regions identically
across all 64 containment classes and still glue them together differently.

This runs region_adjacency.py over the rational 727 configurations recovered
from the 727-producing lines, and reports how many distinct types each
invariant sees, coarse to fine.

INVARIANT: region_adjacency asserts that every edge joins containment sets
differing in exactly one bit -- a hard abort, not a filter.  If that fires,
the phantom/real classification is wrong and the run is void.
"""
import collections, json, math, pickle, subprocess, sys, time
from fractions import Fraction as F
import record_hunt as R
from region_adjacency import region_adjacency
from golden_rotations import rot_from_quat

FIVE = [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
FIVES = "4,1,1,-1;3,3,7,3;5,-1,-5,-5;2,1,1,1;1,1,1,1"
planes = pickle.load(open('locus_planes.pkl','rb'))
P = json.load(open('provenance_727.json'))

def line_of(p,q):
    n1,n2=p[:3],q[:3]
    d=(n1[1]*n2[2]-n1[2]*n2[1],n1[2]*n2[0]-n1[0]*n2[2],n1[0]*n2[1]-n1[1]*n2[0])
    if not any(d): return None
    k=max(range(3),key=lambda i:abs(d[i])); i,j=[t for t in range(3) if t!=k]
    det=n1[i]*n2[j]-n1[j]*n2[i]
    if det==0: return None
    pt=[F(0)]*3
    pt[i]=F(-p[3]*n2[j]+q[3]*n1[j],det); pt[j]=F(-n1[i]*q[3]+n2[i]*p[3],det)
    return tuple(pt),tuple(F(x) for x in d)

def to_quat(pt):
    den=1
    for v in pt: den=den*v.denominator//math.gcd(den,v.denominator)
    q=(den,int(pt[0]*den),int(pt[1]*den),int(pt[2]*den))
    g=0
    for x in q: g=math.gcd(g,abs(x))
    q=tuple(x//g for x in q) if g>1 else q
    return q if any(q) and max(abs(x) for x in q)<=512 else None

def qmul(p,q):
    w,x,y,z=p; e,f,g,h=q
    return (w*e-x*f-y*g-z*h,w*f+x*e+y*h-z*g,w*g-x*h+y*e+z*f,w*h+x*g-y*f+z*e)
SYMS=list(dict.fromkeys(R.canon([t])[0] for t in
  [(w,x,y,z) for w in(-1,0,1) for x in(-1,0,1) for y in(-1,0,1) for z in(-1,0,1)
   if (w,x,y,z)!=(0,0,0,0) and w*w+x*x+y*y+z*z in (1,2,4)]))
def symkey(q): return min(R.canon([qmul(tuple(q),h)])[0] for h in SYMS)

# recover the 417 rational 727s
seen=set(); cfgs={}
for rec in P:
    k=(tuple(rec['cubes_planes']),tuple(rec['plane_idx']))
    if k in seen: continue
    seen.add(k)
    pi,pj=rec['cubes_planes']; i1,i2=rec['plane_idx']
    Ln=line_of(planes[pi][i1],planes[pj][i2])
    if Ln is None: continue
    p0,dd=Ln; qs=[]
    for num in range(-500,501):
        for den in (1,2,3,4,5,7,9):
            q=to_quat(tuple(p0[u]+F(num,den)*dd[u] for u in range(3)))
            if q: qs.append(q)
    qs=list(dict.fromkeys(qs))
    out=subprocess.run(['./cube_regions_n','--quats-stdin'],
        input='\n'.join(FIVES+';'+','.join(map(str,q)) for q in qs)+'\n',
        capture_output=True,text=True).stdout
    for ln,q in zip([l for l in out.splitlines() if l.startswith('{')],qs):
        if json.loads(ln).get('bounded')==727: cfgs[symkey(q)]=q
print('rational 727 configurations to classify: %d' % len(cfgs), flush=True)

depth=collections.Counter(); label=collections.Counter(); adj=collections.Counter()
t0=time.time(); done=0
LIMIT=int(sys.argv[1]) if len(sys.argv)>1 else len(cfgs)
for q in list(cfgs.values())[:LIMIT]:
    r=region_adjacency([rot_from_quat(*x) for x in FIVE]+[rot_from_quat(*q)],verbose=False)
    assert r['total']==727, 'count mismatch %s' % r['total']
    depth[tuple(sorted(r['by_depth'].items()))]+=1
    label[tuple(sorted(r['per_label'].items()))]+=1
    adj[r['profile'] if isinstance(r['profile'],tuple) else repr(r['profile'])]+=1
    done+=1
    if done%25==0:
        print('  %d/%d  (%.0fs, depth=%d label=%d adjacency=%d)'
              % (done,LIMIT,time.time()-t0,len(depth),len(label),len(adj)),flush=True)
print()
print('classified %d rational 727 configurations in %.0f s' % (done,time.time()-t0))
print('  distinct DEPTH profiles     : %d' % len(depth))
print('  distinct PER-LABEL vectors  : %d' % len(label))
print('  distinct ADJACENCY profiles : %d   <- finest invariant available' % len(adj))

