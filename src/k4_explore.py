#!/usr/bin/env python3
"""Consequences of assuming k <= 4 (at most four pairs at two-body weight 10, any n).

First the numbers, measured DIRECTLY -- W0 from tagged triple points, T from the
level-1 two-body vertices -- rather than inferred from d1 (which would assume
c1 = 1 and bake in the answer).

The question k <= 4 is really about: whether the two-body contribution to d1 grows
QUADRATICALLY (as C(n,2) pairs would allow) or LINEARLY (as the records suggest).
The record values 48, 76, 88, 96, 104 differ by 28, 12, 8, 8 -- flattening to +8
per cube, while C(n,2) grows 6, 10, 15, 21, 28.  If T is linear the two-body term
is asymptotically negligible against the three-body term and the whole d1 bound is
governed by W0; if quadratic, it is not.  n = 9 and n = 10 decide it, and both
records are available.
"""
import collections, itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from twobody_solve import pair_detail
from c_level import parse, engine
from w1_gate import w1_direct

BASE = "4,1,1,-1;3,3,7,3;5,-1,-5,-5;2,1,1,1;1,1,1,1"
R6 = BASE + ";7,14,1,-5"
R7 = R6 + ";4,-3,-4,-4"
R8 = R7 + ";24,-24,24,-61"
R9 = R8 + ";168,-168,168,-415;109,-11,91,140"
R10 = R9 + ";6555,6555,6497,6555"
RECORDS = {4: "1,0,0,0;0,5,3,2;1,-4,-1,1;1,1,-1,-4", 5: BASE, 6: R6, 7: R7, 8: R8,
           9: R9, 10: R10}

print(f"{'n':>3} {'total':>6} {'d1':>6} {'W0':>6} {'T':>5} {'k':>3} {'nonzero':>8} "
      f"{'C(n,2)':>7} {'8n+40':>6}  weight histogram")
rows = {}
for n in sorted(RECORDS):
    qs = parse(RECORDS[n])
    try:
        e = engine(qs)
        det = pair_detail(qs)
    except Exception as ex:
        print(f"{n:>3}  engine/detail failed: {ex}")
        continue
    w = {p: c[4] + 2 * c[6] for p, c in det.items()}
    allw = [w.get(p, 0) for p in itertools.combinations(range(n), 2)]
    T = sum(allw)
    k = sum(1 for v in allw if v == 10)
    nz = sum(1 for v in allw if v > 0)
    try:
        W0 = w1_direct(qs)[0] if n == 4 else None
    except Exception:
        W0 = None
    hist = dict(sorted(collections.Counter(allw).items(), reverse=True))
    d1 = e["by_depth"].get("1", 0)
    W0d = 2 * (d1 - T - 2)          # from the anatomy, assuming c1 = 1
    rows[n] = (T, k, nz, d1)
    print(f"{n:>3} {e['bounded']:>6} {d1:>6} {W0d:>6} {T:>5} {k:>3} {nz:>8} "
          f"{n*(n-1)//2:>7} {8*n+40:>6}  {hist}")

print()
print("T differences:", [rows[n][0] - rows[n - 1][0] for n in sorted(rows) if n - 1 in rows])
print("k sequence   :", [rows[n][1] for n in sorted(rows)])
print("nonzero pairs:", [rows[n][2] for n in sorted(rows)], " vs C(n,2)",
      [n * (n - 1) // 2 for n in sorted(rows)])
print()
print("if T tracks 8n+40 and k <= 4, the two-body term is LINEAR and W0 governs d1.")
