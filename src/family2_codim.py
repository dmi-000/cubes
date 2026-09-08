#!/usr/bin/env python3
"""Is (0,10,0) codimension 2 or codimension 1?  The answer changes the verdict on 195.

The independent probe's (0,10,0) neighbours all share a form:

    (1,7,-7,-15) (1,8,-8,-17) (1,9,-9,-19) (1,10,-10,-21)
    (2,7,-7,-16) (2,8,-8,-18) (2,9,-9,-20) (3,6,-6,-15)

every one has x = -y, i.e. rotation axis proportional to (a, -a, c): the axis lies
in the plane perpendicular to (1,1,0).  That is ONE condition on the axis, leaving
a 1-parameter set of axes plus a free angle -- a 2-dimensional locus, i.e.
CODIMENSION 1, not 2.

It matters directly.  Weight 10 at codimension 1 costs ONE condition per pair, so
T = 60 costs 6 conditions against 9 degrees of freedom -- comfortably solvable, and
max(4) = 195 becomes plausible rather than overdetermined.  [P279]'s "overdetermined
by 3" assumed codimension 2 for both realisations.

Tested by walking the two-parameter family q = (w, a, -a, c) directly: if weight 10
holds across varying (a, c) and varying angle, the locus is 2-dimensional.
"""
import collections, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from twobody_solve import pair_detail

print("family q = (w, a, -a, c):  axis proportional to (a,-a,c), perpendicular to (1,1,0)")
print(f"{'w':>3} {'a':>3} {'c':>4}  {'(deg2,deg4,deg6)':>18} {'weight':>7}")
tally = collections.Counter()
for w in (1, 2, 3, 4):
    for a in (1, 2, 3, 5, 7):
        for c in (-3, -5, -9, -15, 2, 4):
            q = (w, a, -a, c)
            if not any(q):
                continue
            try:
                det = pair_detail([(1, 0, 0, 0), q])
            except Exception:
                continue
            cc = det.get((0, 1), collections.Counter())
            sig = (cc[2], cc[4], cc[6])
            wt = cc[4] + 2 * cc[6]
            tally[(wt, sig)] += 1
            if wt >= 10:
                print(f"{w:>3} {a:>3} {c:>4}  {str(sig):>18} {wt:>7}")
print()
print("signature census over the whole (w,a,c) family:")
for k, v in sorted(tally.items(), key=lambda kv: -kv[1]):
    print(f"   weight {k[0]:>2}  {str(k[1]):>14} : {v}")
n10 = sum(v for k, v in tally.items() if k[1] == (0, 10, 0))
tot = sum(tally.values())
print(f"\n(0,10,0) in {n10} of {tot} family members")
print("most of the family => codimension 1 => T=60 costs 6 of 9 => 195 PLAUSIBLE")
print("a thin subset      => codimension 2 => T=60 costs 12 of 9 => [P279] stands")
