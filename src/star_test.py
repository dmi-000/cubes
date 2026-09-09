#!/usr/bin/env python3
"""Do the weight-10 pairs form a STAR?  If so, k <= 3 at n=4 and T <= 48 follows.

The 4-subset scan showed the n=5 record's four weight-10 pairs are all incident to
cube 4: dropping that cube leaves k = 0, dropping any other leaves k = 3.  That is
a star.  A star on n vertices has at most n-1 edges, so at n = 4 it gives k <= 3 --
which is the cap the assumption T <= 48 needs.

Tested here on every record: WHICH pairs carry weight 10, and whether they share a
common cube.  Reported as the weight-10 graph's degree sequence, so a star shows as
one vertex of degree k and the rest of degree 1, while any triangle or disjoint
pair shows immediately.

Also reported: the full pair-weight multiset, because T <= 48 needs more than
k <= 3.  With k = 3 the remaining three pairs must sum to <= 18, and weight 8 DOES
occur (the (0,4,2) signature), so 10+10+10+8+8+8 = 54 is not excluded by the star
property alone.  Whether weight 8 ever coexists with k = 3 is the second question.
"""
import collections, itertools, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from twobody_solve import pair_detail
from c_level import parse, engine

BASE = "4,1,1,-1;3,3,7,3;5,-1,-5,-5;2,1,1,1;1,1,1,1"
RECORDS = {4: "1,0,0,0;0,5,3,2;1,-4,-1,1;1,1,-1,-4",
           5: BASE, 6: BASE + ";7,14,1,-5",
           7: BASE + ";7,14,1,-5;4,-3,-4,-4",
           8: BASE + ";7,14,1,-5;4,-3,-4,-4;24,-24,24,-61"}

for n, spec in sorted(RECORDS.items()):
    qs = parse(spec)
    det = pair_detail(qs)
    w = {p: c[4] + 2 * c[6] for p, c in det.items()}
    allw = {p: w.get(p, 0) for p in itertools.combinations(range(n), 2)}
    ten = [p for p, v in allw.items() if v == 10]
    deg = collections.Counter()
    for p in ten:
        deg[p[0]] += 1
        deg[p[1]] += 1
    common = set(range(n))
    for p in ten:
        common &= set(p)
    hist = collections.Counter(allw.values())
    print(f"n={n}  T={sum(allw.values())}  k={len(ten)}")
    print(f"   weight-10 pairs : {sorted(ten)}")
    print(f"   degree sequence : {dict(sorted(deg.items()))}")
    print(f"   common cube     : {sorted(common) if common else 'NONE -- not a star'}")
    print(f"   weight histogram: {dict(sorted(hist.items(), reverse=True))}")
    eights = [p for p, v in allw.items() if v == 8]
    print(f"   weight-8 pairs  : {sorted(eights) if eights else 'none'}")
    print()
print("star  => k <= n-1, so k <= 3 at n=4  => T <= 10*3 + (max weight of the rest)*3")
print("if the rest never exceed 6 when k = 3, T <= 48 follows.")
