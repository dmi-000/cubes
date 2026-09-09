#!/usr/bin/env python3
"""Would the RADII SIGNATURE have caught the unsafe n=9 substitution?

[P285]: two representatives of the n=9 record agree in count (2787) and in by_depth
at every one of nine depths, yet extend to 3925 and 3921.  Count and profile were
therefore NOT sufficient evidence that swapping one for the other was safe.

The radius signature is a strictly finer invariant in principle -- it records the
multiset of r^2 over outer-boundary vertices, which is invariant under global
rotation and under each cube's own 24 symmetries by construction (radii.py) -- and
it was INJECTIVE on 44 295 candidate PAIRS ([P collide]: 2 863 signatures, 0
non-congruent pairs sharing one).  Whether that survives at n >= 3 is [OQ 26], and
this is the hardest control available for it: two configurations that every other
measured invariant calls identical.

  signatures DIFFER    -> the radii signature would have caught it; it is strictly
                          finer than count+profile and is the check to run before a
                          representative substitution
  signatures IDENTICAL -> it is not sufficient either, and [OQ 26] gets a negative
                          answer from the sharpest possible instance
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from radii import vertices, radius_signature
from c_level import parse

SEVEN = "4,1,1,-1;3,3,7,3;5,-1,-5,-5;2,1,1,1;1,1,1,1;7,14,1,-5;4,-3,-4,-4;168,-168,168,-415"
OLD = parse(SEVEN + ";88787,-9061,74275,113786")
NEW = parse(SEVEN + ";109,-11,91,140")

CORNER, EDGE = {(3, 3)}, {(2, 2)}
print("n=9 record, two representatives -- identical count (2787) and by_depth at all 9 depths\n")
sigs = {}
for name, qs in (("ORIGINAL  88787,-9061,74275,113786", OLD),
                 ("SIMPLIFIED 109,-11,91,140", NEW)):
    vs = vertices(qs)
    full = radius_signature(qs)
    edge = radius_signature(qs, EDGE)
    corn = radius_signature(qs, CORNER)
    sigs[name] = (full, edge, corn)
    print(f"{name}")
    print(f"   outer vertices        : {len(vs)}")
    print(f"   distinct r^2 values   : {len(full)}")
    print(f"   edge-edge (2,2) radii : {edge}")
    print(f"   corner-corner (3,3)   : {corn}")
    print()

a, b = list(sigs.values())
for i, what in enumerate(("FULL radius signature", "edge-edge radii", "corner-corner radii")):
    same = a[i] == b[i]
    print(f"{what:24s}: {'IDENTICAL' if same else 'DIFFER'}")
if a[0] != b[0]:
    da = dict(a[0]); db = dict(b[0])
    diff = {k: (da.get(k, 0), db.get(k, 0)) for k in set(da) | set(db) if da.get(k) != db.get(k)}
    print(f"\nfirst differences (r^2 -> old count, new count), {len(diff)} of "
          f"{len(set(da) | set(db))} radii:")
    for k in sorted(diff)[:8]:
        print(f"   r^2 = {k}   old {diff[k][0]}, new {diff[k][1]}")
    print("\n=> the radii signature WOULD have caught the substitution.")
else:
    print("\n=> the radii signature would NOT have caught it: not sufficient either.")
