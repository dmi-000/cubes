#!/usr/bin/env python3
"""What Hypothesis T buys for the TOWER, measured rather than asserted.

If max(4) = 183, then every 4-subset of every record is capped at 183, and the
subsets that ATTAIN it mark where the tower passes through an optimal 4-layer.
That is checkable now, without the hypothesis -- the hypothesis only turns
"183 is the best seen" into "183 is the maximum", which converts these from
observations into optimality statements.

Reported per record: the best 4-subset count, how many subsets attain it, and
the full spread.  A record whose best 4-subset is 183 is built on an optimal
4-layer (conditionally); one whose best is below 183 is not, and that is a
structural fact about the tower worth knowing either way.
"""
import collections, itertools, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_level import parse, engine

BASE = "4,1,1,-1;3,3,7,3;5,-1,-5,-5;2,1,1,1;1,1,1,1"
RECORDS = {4: ("183", "1,0,0,0;0,5,3,2;1,-4,-1,1;1,1,-1,-4"),
           5: ("393", BASE),
           6: ("727", BASE + ";7,14,1,-5"),
           7: ("1217", BASE + ";7,14,1,-5;4,-3,-4,-4"),
           8: ("1895", BASE + ";7,14,1,-5;4,-3,-4,-4;24,-24,24,-61")}

print("4-SUBSET counts of each tower record   (Hypothesis T => all are <= 183)")
print(f"{'n':>2} {'record':>7} {'#4-subsets':>11} {'best':>5} {'#at best':>9} {'at 183':>7}  spread")
for n in sorted(RECORDS):
    name, spec = RECORDS[n]
    qs = parse(spec)
    counts = []
    for sub in itertools.combinations(range(n), 4):
        try:
            counts.append(engine([qs[i] for i in sub])["bounded"])
        except Exception:
            pass
    if not counts:
        continue
    h = collections.Counter(counts)
    best = max(counts)
    print(f"{n:>2} {name:>7} {len(counts):>11} {best:>5} {h[best]:>9} {h.get(183,0):>7}  "
          f"{dict(sorted(h.items(), reverse=True))}")
print()
print("a record whose best 4-subset is 183 passes through an OPTIMAL 4-layer")
print("(conditionally on Hypothesis T); one below 183 does not.")
