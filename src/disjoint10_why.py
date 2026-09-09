#!/usr/bin/env python3
"""WHY do the two disjoint pairs never both hold weight 10?

disjoint10.py built 167 configurations with pairs (0,1) and (2,3) BOTH on
weight-10 loci by construction, and none kept both in context.  But "not both"
has two very different explanations:

  (i) assembly costs one of them -- swallowing, a real mechanism, and the star
      property then has a cause;
  (ii) the construction never delivered weight 10 standalone in the first place
       -- e.g. r2 is a weight-10 rotation but q3 = r2*q2 lands somewhere the
       STANDALONE pair weight is already below 10, making the whole run vacuous.

These are distinguished by measuring, for each configuration, the STANDALONE
weight of each disjoint pair alongside its in-context weight.  A drop from 10 to
less is mechanism (i); a standalone value below 10 means the construction was
broken and the conclusion is void.
"""
import collections, itertools, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from twobody_solve import pair_detail
from c_level import shares_plane
from congruent import qmul, qconj

CORNER = [(w, 1, 1, 1) for w in range(2, 5)]
CROSS = [(w, a, -a, -(2 * a + w)) for w in (1, 2) for a in (2, 3)]
FREE = [(1, 0, 0, 0), (2, 1, 0, 0), (3, 1, 1, 0), (2, 1, 1, 0), (5, 2, 1, 1),
        (3, 2, 1, 0), (4, 1, 2, 1), (1, 1, 0, 0)]


def w_standalone(qa, qb):
    d = pair_detail([qa, qb])
    c = d.get((0, 1), collections.Counter())
    return c[4] + 2 * c[6]


joint = collections.Counter()
drops = collections.Counter()
rows = []
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
                s01 = w_standalone(qs[0], qs[1])
                s23 = w_standalone(qs[2], qs[3])
                det = pair_detail(qs)
            except Exception:
                continue
            w = {p: c[4] + 2 * c[6] for p, c in det.items()}
            i01, i23 = w.get((0, 1), 0), w.get((2, 3), 0)
            joint[(s01, s23, i01, i23)] += 1
            drops[(s01 - i01, s23 - i23)] += 1
            rows.append((s01, s23, i01, i23))

n = len(rows)
both_sa10 = sum(1 for r in rows if r[0] == 10 and r[1] == 10)
both_ic10 = sum(1 for r in rows if r[2] == 10 and r[3] == 10)
print(f"configurations: {n}")
print(f"  BOTH disjoint pairs weight 10 STANDALONE : {both_sa10}")
print(f"  BOTH disjoint pairs weight 10 IN CONTEXT : {both_ic10}")
print()
print("if standalone is 10,10 but in-context is not, assembly is the cause (mechanism).")
print("if standalone is never 10,10, the construction failed and the run says nothing.\n")
print("drop (standalone - in-context) per pair, most common:")
for k, v in sorted(drops.items(), key=lambda kv: -kv[1])[:8]:
    print(f"   (0,1) dropped {k[0]:>3},  (2,3) dropped {k[1]:>3} : {v}")
print("\njoint (sa01, sa23, ic01, ic23), most common:")
for k, v in sorted(joint.items(), key=lambda kv: -kv[1])[:8]:
    print(f"   standalone ({k[0]:>2},{k[1]:>2})  in-context ({k[2]:>2},{k[3]:>2}) : {v}")
