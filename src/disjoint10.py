#!/usr/bin/env python3
"""CONSTRUCT two disjoint weight-10 pairs.  If they assemble, the star falls.

The star property holds at every record but cannot be a theorem in that form: at
n=4 the pairs (0,1) and (2,3) are DISJOINT, so making each weight 10 constrains
q1 and q3*conj(q2) independently -- 2 + 2 conditions on 9 degrees of freedom.
There is no dimensional obstruction.

So build it directly instead of sweeping for it:

    q1 = r1                  -> pair (0,1) has relative rotation r1
    q3 = r2 * q2             -> pair (2,3) has relative rotation r2

with r1, r2 each taken from a known weight-10 curve ([P280]):
    corner family    (w, 1, 1, 1)
    crossing family  (w, a, -a, -(2a+w)),  a > w
and q2 free.  Both disjoint pairs are then weight 10 STANDALONE by construction;
the only question is what survives IN CONTEXT ([P281] -- other cubes can swallow
coincidence vertices), which is exactly the escape the star property would need.

Outcomes:
  both pairs still 10 in context -> the star is refuted as a general property
  T > 48                         -> the assumption T <= 48 is refuted outright
  weights collapse under assembly -> swallowing IS the mechanism, and the star
                                     property has a reason rather than being a
                                     coincidence of maximisers
"""
import collections, itertools, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from twobody_solve import pair_detail
from c_level import engine, shares_plane
from congruent import qmul

CORNER = [(w, 1, 1, 1) for w in range(2, 7)]
CROSS = [(w, a, -a, -(2 * a + w)) for w in (1, 2) for a in (2, 3, 4)]
FREE = [(1, 0, 0, 0), (2, 1, 0, 0), (3, 1, 1, 0), (2, 1, 1, 0), (5, 2, 1, 1),
        (3, 2, 1, 0), (4, 1, 2, 1), (1, 1, 0, 0)]

print("constructing q1 = r1,  q3 = r2*q2   so pairs (0,1) and (2,3) are both")
print("weight-10 loci by construction.  measuring what survives in context.\n")
print(f"{'r1':>14} {'r2':>16} {'q2':>12} {'w(0,1)':>7} {'w(2,3)':>7} {'T':>4} {'count':>6}")
best = None
both10 = 0
tried = 0
for r1 in CORNER[:3] + CROSS[:3]:
    for r2 in CORNER[:3] + CROSS[:3]:
        for q2 in FREE:
            q3 = qmul(r2, q2)
            if max(abs(v) for v in q3) > 400:
                continue
            qs = [(1, 0, 0, 0), r1, q2, q3]
            if any(not any(q) for q in qs) or shares_plane(qs):
                continue
            tried += 1
            try:
                det = pair_detail(qs)
                e = engine(qs)
            except Exception:
                continue
            w = {p: c[4] + 2 * c[6] for p, c in det.items()}
            allw = {p: w.get(p, 0) for p in itertools.combinations(range(4), 2)}
            T = sum(allw.values())
            a, b = allw[(0, 1)], allw[(2, 3)]
            if a == 10 and b == 10:
                both10 += 1
            if (a == 10 and b == 10) or T > 48:
                print(f"{str(r1):>14} {str(r2):>16} {str(q2):>12} {a:>7} {b:>7} {T:>4} "
                      f"{e['bounded']:>6}   {'T>48!' if T > 48 else 'DISJOINT PAIR'}")
            if best is None or T > best[0]:
                best = (T, dict(allw), e["bounded"],
                        ";".join(",".join(str(x) for x in q) for q in qs))
print()
print(f"configurations built: {tried}")
print(f"with BOTH disjoint pairs at weight 10 in context: {both10}")
if best:
    print(f"max T: {best[0]}  (count {best[2]})   weights {sorted(best[1].values(), reverse=True)}")
    print(f"  {best[3]}")
print("\nboth10 > 0 => star refuted as a general property")
print("both10 = 0 => swallowing collapses disjoint weight-10 pairs; the star has a mechanism")
