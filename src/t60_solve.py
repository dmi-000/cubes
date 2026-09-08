#!/usr/bin/env python3
"""Can T = 60 be reached?  Solve over the weight-10 loci, don't sample the space.

[P280] gives both weight-10 families explicitly.  T = 60 needs all SIX pairs at
weight 10, and for cubes (0=identity, 1, 2, 3) the pairs are

    hub    (0,i):  relative rotation  q_i
    mutual (i,j):  relative rotation  q_j * conj(q_i)

so the question is: three quaternions, each in the weight-10 set W, whose pairwise
QUOTIENTS are also in W.  That is a K4 containing the identity in the graph on W
with edges "quotient is in W" -- a clique problem, not a sweep.

Step one, here: the record's own construction generalised exactly.  Its three
cubes are rotations about three different BODY DIAGONALS, which puts every hub
pair on the (w,1,1,1) curve and hence at weight 10 for FREE, at any angles.  So
the whole question collapses to the three mutual pairs, as a function of the three
angles and the choice of diagonals -- a 3-parameter exact solve.  If the mutual
pairs can be driven to 10 the record's family reaches T = 60; if they are capped
below, that family cannot and [P279]'s overdetermination is being felt.
"""
import collections, itertools, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from twobody_solve import pair_detail
from c_level import engine

DIAGS = [(1, 1, 1), (1, 1, -1), (1, -1, 1), (-1, 1, 1)]


def rot(diag, w):
    """integer quaternion: rotation about `diag` with cos(theta/2) ~ w"""
    return (w,) + diag


def weight(qa, qb):
    det = pair_detail([qa, qb])
    c = det.get((0, 1), collections.Counter())
    return c[4] + 2 * c[6], (c[2], c[4], c[6])


print("hub pairs are weight 10 automatically (body-diagonal curve, [P280]).")
print("so T = 6*10 = 60 iff the three MUTUAL pairs also reach 10.\n")
print(f"{'diagonals':>12} {'w1':>3} {'w2':>3} {'w3':>3}  {'mutual weights':>16} {'T':>4} {'count':>6}")
best = None
seen = collections.Counter()
for trio in itertools.combinations(range(4), 3):
    for w1 in range(1, 6):
        for w2 in range(1, 6):
            for w3 in range(1, 6):
                qs = [(1, 0, 0, 0), rot(DIAGS[trio[0]], w1),
                      rot(DIAGS[trio[1]], w2), rot(DIAGS[trio[2]], w3)]
                try:
                    det = pair_detail(qs)
                except Exception:
                    continue
                wts = {}
                for p in itertools.combinations(range(4), 2):
                    c = det.get(p, collections.Counter())
                    wts[p] = c[4] + 2 * c[6]
                hub = [wts[(0, i)] for i in (1, 2, 3)]
                mut = [wts[(1, 2)], wts[(1, 3)], wts[(2, 3)]]
                T = sum(wts.values())
                seen[tuple(sorted(mut))] += 1
                if best is None or T > best[0]:
                    e = engine(qs)
                    best = (T, trio, (w1, w2, w3), hub, mut, e["bounded"],
                            ";".join(",".join(str(x) for x in q) for q in qs))
                    print(f"{str(trio):>12} {w1:>3} {w2:>3} {w3:>3}  {str(mut):>16} {T:>4} "
                          f"{e['bounded']:>6}   hub {hub}")
print()
print("census of mutual-pair weight triples:", dict(sorted(seen.items(), key=lambda kv: -kv[1])[:8]))
if best:
    print(f"\nbest T over the body-diagonal construction: {best[0]}  (count {best[5]})")
    print(f"  {best[6]}")
print("T = 60 needs mutual weights [10,10,10].")
