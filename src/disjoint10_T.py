#!/usr/bin/env python3
"""The star is refuted -- so what is T on the configurations that refute it?

disjoint10_why.py found 5 configurations where the DISJOINT pairs (0,1) and (2,3)
are BOTH weight 10 in context.  The star property therefore does not hold in
general; it is a property of maximisers only.  That removes the k <= 3 argument
for T <= 48, and the assumption now stands or falls on what T actually reaches
on these configurations.

Two disjoint pairs at 10 already gives T >= 20; if the remaining four pairs can be
pushed the total could pass 48 and refute the assumption outright.  This prints
the full pair-weight vector, T, and the region count for every both-10 case.
"""
import collections, itertools, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from twobody_solve import pair_detail
from c_level import shares_plane, engine
from congruent import qmul

CORNER = [(w, 1, 1, 1) for w in range(2, 5)]
CROSS = [(w, a, -a, -(2 * a + w)) for w in (1, 2) for a in (2, 3)]
FREE = [(1, 0, 0, 0), (2, 1, 0, 0), (3, 1, 1, 0), (2, 1, 1, 0), (5, 2, 1, 1),
        (3, 2, 1, 0), (4, 1, 2, 1), (1, 1, 0, 0)]

print(f"{'T':>4} {'count':>6}  pair weights (0,1)(0,2)(0,3)(1,2)(1,3)(2,3)   configuration")
best = None
found = 0
for r1 in CORNER + CROSS:
    for r2 in CORNER + CROSS:
        for q2 in FREE:
            q3 = qmul(r2, q2)
            if max(abs(v) for v in q3) > 400:
                continue
            qs = [(1, 0, 0, 0), r1, q2, q3]
            if any(not any(q) for q in qs) or shares_plane(qs):
                continue
            try:
                det = pair_detail(qs)
            except Exception:
                continue
            w = {p: c[4] + 2 * c[6] for p, c in det.items()}
            allw = [w.get(p, 0) for p in itertools.combinations(range(4), 2)]
            if not (allw[0] == 10 and allw[5] == 10):
                continue
            found += 1
            T = sum(allw)
            e = engine(qs)
            spec = ";".join(",".join(str(x) for x in q) for q in qs)
            flag = "  *** T > 48 : ASSUMPTION REFUTED ***" if T > 48 else ""
            print(f"{T:>4} {e['bounded']:>6}  {allw}   {spec}{flag}")
            if best is None or T > best[0]:
                best = (T, allw, e["bounded"], spec)
print(f"\nboth-disjoint-10 configurations: {found}")
if best:
    print(f"max T among them: {best[0]}  (count {best[2]})")
    print(f"  {best[3]}")
print("assumption T <= 48 survives here iff max T <= 48.")
