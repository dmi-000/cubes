#!/usr/bin/env python3
"""Map the local shape of every record: dimension AND node structure.

n4_183_dim.out enumerated all 3^9-1 signed lattice directions at n=4 and read the
dimension off 26 = 3^3-1.  That does not scale: n=6 is 3^15, n=9 is 3^24.  So probe
in two stages, which is also what distinguishes a SUBSPACE from a NODE:

  stage 1  each coordinate axis +-e_i          -> the set S of directions that hold
  stage 2  each pair e_i +- e_j for i,j in S   -> do COMBINATIONS hold?

    all pairs hold  => S spans a genuine |S|-dimensional plateau
    no pair holds   => |S| separate arcs crossing at the record: a NODE
                       (dim2785.log found exactly this on 727 arc D)
    some hold       => mixed; the surviving pairs name the actual tangent structure

Perturbation is exact: scale every quaternion by K, then add +-1 to one component,
i.e. a step of about 1/K.  Two values of K guard against a step artefact -- the
n=4 measurement was stable at 1/32, 1/128 and 1/512, and anything that moves with
K is a step effect, not geometry.

GATE: n=4 must return dimension 3, reproducing n4_183_dim.out by a different route.
"""
import math, subprocess, sys, os, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
ENG = os.path.join(HERE, "cube_regions_n")

def count(qs):
    spec = ";".join(",".join(str(v) for v in q) for q in qs)
    out = subprocess.run([ENG,"--quats",spec],capture_output=True,text=True).stdout
    i = out.find('"bounded":')
    return int(out[i+10:out.find(",",i)]) if i >= 0 else None

def perturb(base, K, deltas):
    """scale by K, then apply {coord index -> delta}; coord j indexes cubes 1.. only"""
    out = [tuple(v*K for v in base[0])]
    for c, q in enumerate(base[1:]):
        q = [v*K for v in q]
        for (ci, comp), d in deltas.items():
            if ci == c: q[comp] += d
        out.append(tuple(q))
    return out

def probe(name, base, K):
    n = len(base)
    D = 4*(n-1)                      # quaternion components of the non-gauge cubes
    ref = count(base)
    hold = []
    for c in range(n-1):
        for comp in range(4):
            ok = all(count(perturb(base, K, {(c,comp): s})) == ref for s in (1,-1))
            if ok: hold.append((c,comp))
    pairs_hold = pairs_tot = 0
    for a,b in itertools.combinations(hold, 2):
        for sa,sb in ((1,1),(1,-1)):
            pairs_tot += 1
            if count(perturb(base, K, {a:sa, b:sb})) == ref: pairs_hold += 1
    shape = ("subspace" if pairs_tot and pairs_hold == pairs_tot else
             "NODE (no combination holds)" if pairs_tot and pairs_hold == 0 else
             "mixed" if pairs_tot else "isolated along axes")
    print(f"{name:22s} K={K:<5} count={ref:<5} axes holding {len(hold):>2}/{D:<3} "
          f"pair-combos holding {pairs_hold}/{pairs_tot:<4} -> {shape}", flush=True)
    return len(hold), shape

BASE5 = [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
TARGETS = [
  ("183 n=4 GATE", [(1,0,0,0),(0,5,3,2),(1,-4,-1,1),(1,1,-1,-4)]),
  ("393 n=5",      BASE5),
  ("727 n=6",      BASE5+[(7,14,1,-5)]),
  ("1217 n=7",     BASE5+[(7,14,1,-5),(4,-3,-4,-4)]),
  ("1895 n=8",     BASE5+[(7,14,1,-5),(4,-3,-4,-4),(24,-24,24,-61)]),
]
print("record shapes: axis probe then pair probe (n4_183_dim reference: n=4 is dim 3)\n")
for name, cfg in TARGETS:
    for K in (64, 256):
        try: probe(name, cfg, K)
        except Exception as e: print(f"{name:22s} K={K} error {e}")
