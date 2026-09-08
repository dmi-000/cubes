#!/usr/bin/env python3
"""Two-body weight is a WALL COUNT, so it should be solved, not sampled.

A degree-4 two-body vertex at level 1 is a point lying on an EDGE of cube i and an
EDGE of cube j at once: four seam segments (a1,b1),(a1,b2),(a2,b1),(a2,b2) meet
there.  Two skew lines in space meet only in codimension 1, so each such vertex is
a COINCIDENCE -- one of the project's walls -- not a generic feature.  Degree 6 is
the corner-contact case, weight 2.  Hence

    two-body weight of a pair  =  (edge-edge coincidences) + 2*(corner contacts)

and the histogram bears this out: 1373 of 2046 pairs have weight 0, because a
generic pair sits on no wall at all.  Sampling configurations and hoping to land
on weight 10 is sampling a measure-zero set -- which is why the pool that found
the 46.8 deg family could not find the ~61 deg one, and why [P277]'s "T = 48 was
still the maximum" is a statement about the pool.

The project already has the solver for this: coincidence conditions are quadrics
in Cayley coordinates, edge-edge ones factoring into pairs of rational planes
(RESULTS), and `multiwall_*` solves several at once.  Step one, done here, is to
find how many walls weight 10 actually is -- the decomposition (n24, n26) per pair
-- because that is the number the solver has to be given.
"""
import collections, itertools, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from euler3 import rowsT, frames, segments
from cellcomplex import on_bdry_params
from c_level import strictly_inside, parse, engine


def pair_detail(qs, ell=1):
    """per pair: counts of two-body vertices by degree, and the resulting weight"""
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
    out = collections.defaultdict(collections.Counter)
    for P in on:
        if len(on[P]) == 2:
            out[pair[P]][deg[P]] += 1
    return out


CASES = [("record 183", "1,0,0,0;0,5,3,2;1,-4,-1,1;1,1,-1,-4"),
         ("edge-axis w10", "1,0,0,0;6,4,6,-2;-3,6,0,-3;1,4,-6,-2"),
         ("(2,2,1)-axis w10", "1,0,0,0;0,13,3,1;1,-5,-2,2;1,4,-5,-11"),
         ("61.15 family", "1,0,0,0;5,3,4,-1;-2,5,-3,3;0,5,-4,-4"),
         ("17.9deg outlier", "1,0,0,0;-3,8,4,2;-1,-2,-2,3;4,0,-4,-4")]
print("two-body weight decomposed: deg4 = edge-edge coincidence (wt 1),")
print("                            deg6 = corner contact      (wt 2)")
print()
print(f"{'case':18s} {'total':>6}  per pair: (deg2, deg4, deg6) -> weight")
for label, spec in CASES:
    qs = parse(spec)
    e = engine(qs)
    det = pair_detail(qs)
    parts = []
    for p in itertools.combinations(range(4), 2):
        c = det.get(p, collections.Counter())
        w = c[4] * 1 + c[6] * 2
        parts.append(f"({c[2]},{c[4]},{c[6]})={w}")
    print(f"{label:18s} {e['bounded']:>6}  " + "  ".join(parts))
print()
print("weight 10 = how many simultaneous walls?  read off the deg4/deg6 columns:")
print("that count is what a multiwall SOLVE must be asked for, per pair.")
