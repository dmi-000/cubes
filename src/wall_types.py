#!/usr/bin/env python3
"""What ARE the weight-carrying two-body vertices, geometrically and exactly?

Before the weight-10 locus can be SOLVED, the conditions have to be named.  For
each two-body vertex of a pair, its position relative to EACH cube is classified
by how many of that cube's three face constraints are tight:

    3 tight = a CORNER of that cube
    2 tight = on an EDGE
    1 tight = interior to a FACE

so a vertex is e.g. (edge, edge) -- an edge-edge crossing -- or (corner, edge),
or (corner, corner).  The seam-segment count at such a vertex is the product of
the faces meeting there: edge x edge = 2 x 2 = 4 (degree 4), corner x edge =
3 x 2 = 6 (degree 6), corner x corner = 3 x 3 = 9.

[P237] calls the degree-6 class "shared-corner (3,3)", which would be corner x
corner and predicts degree 9, not 6.  That is worth checking rather than
inheriting, because the SOLVE's equations differ: edge-edge is
det[q-p, u, v] = 0 for two lines, corner-on-edge is a point-on-line condition
(two equations), corner-on-corner is three.  Getting the type wrong gets the
codimension wrong.
"""
import collections, itertools, sys, os
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from euler3 import rowsT, frames, segments
from cellcomplex import on_bdry_params
from c_level import strictly_inside, parse


def tightness(P, M):
    """how many of this cube's three face constraints |M[r].P| = 1 are tight"""
    return sum(1 for r in range(3)
               if abs(sum(M[r][k] * P[k] for k in range(3))) == 1)


NAME = {3: "corner", 2: "edge", 1: "face", 0: "interior"}


def classify(qs, ell=1):
    Ms = [rowsT(R) for R in frames(qs)]
    n = len(qs)
    deg = collections.Counter()
    pair = {}
    on = collections.defaultdict(set)
    for i, j in itertools.combinations(range(n), 2):
        for p, d, lo, hi in segments(Ms[i], Ms[j]):
            cuts = sorted({lo, hi} | {t for k in range(n) if k not in (i, j)
                                      for t in on_bdry_params(p, d, lo, hi, Ms[k])})
            for a, b in zip(cuts, cuts[1:]):
                if a >= b:
                    continue
                mid = tuple(p[z] + ((a + b) / 2) * d[z] for z in range(3))
                s = sum(1 for k in range(n) if k not in (i, j) and strictly_inside(mid, Ms[k]))
                if s + 1 != ell:
                    continue
                for t in (a, b):
                    P = tuple(p[z] + t * d[z] for z in range(3))
                    deg[P] += 1
                    on[P].update((i, j))
                    pair[P] = (i, j)
    for P in list(on):
        for k in range(n):
            if k in on[P]:
                continue
            v = [abs(sum(Ms[k][q][z] * P[z] for z in range(3))) for q in range(3)]
            if all(x <= 1 for x in v) and any(x == 1 for x in v):
                on[P].add(k)
    out = collections.Counter()
    for P in on:
        if len(on[P]) != 2:
            continue
        i, j = pair[P]
        ti, tj = tightness(P, Ms[i]), tightness(P, Ms[j])
        out[(deg[P], tuple(sorted((NAME[ti], NAME[tj]))))] += 1
    return out


for label, spec in (("record 183", "1,0,0,0;0,5,3,2;1,-4,-1,1;1,1,-1,-4"),
                    ("(2,2,1)-axis w10", "1,0,0,0;0,13,3,1;1,-5,-2,2;1,4,-5,-11"),
                    ("edge-axis w10", "1,0,0,0;6,4,6,-2;-3,6,0,-3;1,4,-6,-2")):
    c = classify(parse(spec))
    print(f"{label}:")
    for (d, kinds), cnt in sorted(c.items()):
        prod = {"corner": 3, "edge": 2, "face": 1}
        pred = prod[kinds[0]] * prod[kinds[1]]
        print(f"   degree {d:>2}  {kinds[0]:8s} x {kinds[1]:8s}  count {cnt:>3}   "
              f"faces-product predicts degree {pred} {'OK' if pred == d else '<-- MISMATCH'}")
    print()
