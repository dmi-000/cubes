#!/usr/bin/env python3
"""A CHEAP potential refutation of T <= 48, from data already in hand.

The records decompose exactly as  T = 10k + 6m  (k pairs at weight 10, m at 6):

    n=4: 10*3 + 6*3 = 48     n=5: 10*4 + 6*6 = 76     n=6: 10*4 + 6*8  = 88
    n=7: 10*3 + 6*11 = 96    n=8: 10*2 + 6*14 = 104

so k -- the number of weight-10 pairs -- is 3, 4, 4, 3, 2.  **The n=5 and n=6
records carry FOUR weight-10 pairs.**  If any 4-SUBSET of those inherits four of
them, that subset is a 4-cube configuration with k = 4, and

    T >= 10*4 = 40,  and with the other two pairs at 6,  T = 52 > 48

which refutes the assumption outright.  Every 4-subset of a known record is a
legitimate n=4 configuration, so this costs one pass over data already computed --
the cheapest possible attempt at a counterexample, and exactly the test the
assumption should be put through first.

Two-body weight is IN CONTEXT ([P281]), so a subset's weights are NOT the parent's
restricted -- removing cubes can only UNSWALLOW vertices, so subset weights are
>= the parent's.  That makes the test strictly favourable to finding a violation.
"""
import collections, itertools, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from twobody_solve import pair_detail
from c_level import parse, engine

BASE = "4,1,1,-1;3,3,7,3;5,-1,-5,-5;2,1,1,1;1,1,1,1"
RECORDS = {5: BASE,
           6: BASE + ";7,14,1,-5",
           7: BASE + ";7,14,1,-5;4,-3,-4,-4",
           8: BASE + ";7,14,1,-5;4,-3,-4,-4;24,-24,24,-61"}

print("T over every 4-SUBSET of the n=5..8 records   (assumption: T <= 48)")
print(f"{'from':>5} {'subset':>14} {'count':>6} {'k(w10)':>7} {'T':>5}  per-pair weights  verdict")
best = None
viol = 0
for n, spec in sorted(RECORDS.items()):
    qs = parse(spec)
    for sub in itertools.combinations(range(n), 4):
        cfg = [qs[i] for i in sub]
        try:
            det = pair_detail(cfg)
            e = engine(cfg)
        except Exception:
            continue
        w = {p: c[4] + 2 * c[6] for p, c in det.items()}
        vals = sorted((w.get(p, 0) for p in itertools.combinations(range(4), 2)), reverse=True)
        T = sum(vals)
        k = sum(1 for v in vals if v == 10)
        bad = T > 48
        viol += bad
        if bad or best is None or T > best[0]:
            print(f"{n:>5} {str(sub):>14} {e['bounded']:>6} {k:>7} {T:>5}  {vals}  "
                  f"{'*** VIOLATES T<=48 ***' if bad else ''}")
        if best is None or T > best[0]:
            best = (T, n, sub, e["bounded"], vals)
print()
print(f"violations of T <= 48 among record 4-subsets: {viol}")
if best:
    print(f"max T found: {best[0]} (from n={best[1]} subset {best[2]}, count {best[3]}, {best[4]})")
