#!/usr/bin/env python3
"""Local shape of every record, probed in a chart with NO singularity.

Two earlier probes were wrong in different ways:
  * n4_183_extent.py perturbs Cayley coordinates as x*den + d*w, which is INERT
    where w = 0 -- exactly the half-turns the 183 contains ([P287]).
  * map_all_shapes.py perturbed raw quaternion components including w, which is
    the GAUGE direction (scaling q does not move the rotation), so it wasted a
    quarter of its probes and used a basis unaligned with anything.

Here each cube is perturbed along its own TANGENT SPACE.  For integer q = (w,x,y,z)
the three quaternion products q*i, q*j, q*k are integer and orthogonal to q:

    v1 = (-x,  w, -z,  y)      v2 = (-y,  z,  w, -x)      v3 = (-z, -y,  x,  w)

so q -> K*q + d*v_t is a genuine rotation perturbation of size ~1/K, valid at EVERY
q including half-turns.  Three directions per free cube, matching the true 3
degrees of freedom, with no chart singularity to create no-ops.

Stage 1 probes each of the 3(n-1) axes; stage 2 probes pairs among the survivors,
which separates a genuine SUBSPACE from a NODE (dim2785.log found 727 arc D to be
a node: two directions hold, no combination does).

GATES: the 183 must come out 0-dimensional ([P287]) and every probe must actually
MOVE the configuration -- no-ops are counted and reported, since that is the exact
failure [P287] was.
"""
import math, subprocess, sys, os, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
ENG = os.path.join(HERE, "cube_regions_n")

def count(qs):
    spec = ";".join(",".join(str(v) for v in q) for q in qs)
    out = subprocess.run([ENG,"--quats",spec],capture_output=True,text=True).stdout
    i = out.find('"bounded":')
    return int(out[i+10:out.find(",",i)]) if i >= 0 else None

def tang(q):
    w,x,y,z = q
    return [(-x,w,-z,y), (-y,z,w,-x), (-z,-y,x,w)]

def red(q):
    g=0
    for v in q: g=math.gcd(g,abs(v))
    return tuple(v//g for v in q) if g else q

def build(base, K, deltas):
    out=[red(tuple(v*K for v in base[0]))]
    for c,q in enumerate(base[1:]):
        nq=[v*K for v in q]
        for t in range(3):
            d=deltas.get((c,t),0)
            if d:
                for k in range(4): nq[k]+=d*tang(q)[t][k]
        out.append(red(tuple(nq)))
    return out

def probe(name, base, K):
    n=len(base); ref=count(base); D=3*(n-1)
    hold=[]; noop=0
    for c in range(n-1):
        for t in range(3):
            pts=[build(base,K,{(c,t):s}) for s in (1,-1)]
            if any(p==build(base,K,{}) for p in pts): noop+=1; continue
            if all(count(p)==ref for p in pts): hold.append((c,t))
    ph=pt=0
    for a,b in itertools.combinations(hold,2):
        for sa,sb in ((1,1),(1,-1)):
            pt+=1
            if count(build(base,K,{a:sa,b:sb}))==ref: ph+=1
    shape=("0-dimensional" if not hold else
           "subspace dim %d"%len(hold) if pt and ph==pt else
           "NODE: %d arcs, no combination holds"%len(hold) if pt and ph==0 else
           "mixed (%d/%d combos)"%(ph,pt) if pt else "single direction")
    print(f"{name:14s} K={K:<5} count={ref:<6} axes {len(hold):>2}/{D:<3} "
          f"combos {ph}/{pt:<4} no-ops {noop:<3} -> {shape}", flush=True)

B5=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
R9=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1),(7,14,1,-5),
    (4,-3,-4,-4),(168,-168,168,-415),(109,-11,91,140)]
for name,cfg in [("183 GATE",[(1,0,0,0),(0,5,3,2),(1,-4,-1,1),(1,1,-1,-4)]),
                 ("393 n=5",B5), ("727 n=6",B5+[(7,14,1,-5)]),
                 ("1217 n=7",B5+[(7,14,1,-5),(4,-3,-4,-4)]),
                 ("1895 n=8",B5+[(7,14,1,-5),(4,-3,-4,-4),(24,-24,24,-61)]),
                 ("2787 n=9",R9)]:
    for K in (64,256):
        try: probe(name,cfg,K)
        except Exception as e: print(f"{name:14s} K={K} error {e}")
