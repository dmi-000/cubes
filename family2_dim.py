#!/usr/bin/env python3
"""Local DIMENSION of the (0,10,0) weight-10 locus, probed directly.

family2.py sliced pair space by FIXING AN AXIS and walking the angle.  That slice
is transversal to most of the corner-coincidence variety, so it shows isolated
points even where the variety is a curve -- which is why (2,2,1) and (1,1,0)
showed weight 10 only at isolated w while the body diagonal showed it everywhere.
The body-diagonal curve IS a component of the corner locus (it fixes the corner
(1,1,1)); the other axes cut that same 1-dimensional variety transversally.  So
(0,6,2) is codimension 2, confirmed, and my "isolated => codimension 3" reading of
those two rows was the SLICE talking, not the geometry.

(0,10,0) carries no corner coincidence, so it is a different variety and its
dimension is still unknown.  This probes it locally: from a known (0,10,0) point,
walk a small exact lattice in all three quaternion directions and count how many
neighbours keep (0,10,0).  A curve through the point leaves a 1-parameter trail;
an isolated point leaves none.
"""
import collections, itertools, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from twobody_solve import pair_detail

SEEDS = [("(2,2,1) w=5", (5, 2, 2, 1)), ("(-5,-2,2) w=1", (1, -5, -2, 2))]
for label, q0 in SEEDS:
    hits = []
    tally = collections.Counter()
    for d in itertools.product(range(-3, 4), repeat=4):
        q = tuple(a + b for a, b in zip(q0, d))
        if not any(q):
            continue
        try:
            det = pair_detail([(1, 0, 0, 0), q])
        except Exception:
            continue
        c = det.get((0, 1), collections.Counter())
        w = c[4] + 2 * c[6]
        sig = (c[2], c[4], c[6])
        tally[(w, sig)] += 1
        if sig == (0, 10, 0):
            hits.append(q)
    print(f"{label}: lattice box +-3 in all four components, {sum(tally.values())} points")
    print(f"  (0,10,0) neighbours found: {len(hits)}")
    for q in hits[:10]:
        print(f"     {q}")
    top = sorted(tally.items(), key=lambda kv: -kv[1])[:6]
    print(f"  most common (weight, signature): {[(k, v) for k, v in top]}")
    print()
print("many (0,10,0) points spread through the box => positive-dimensional (codim <= 2)")
print("only scaled copies of the seed => the point is isolated, codimension 3")
