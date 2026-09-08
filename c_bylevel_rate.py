#!/usr/bin/env python3
"""At WHICH levels does c=2 occur?  Unbiased sweep.

The 32 known c=2 configurations all show c=2 at ell=1 -- but they were SELECTED
on depth-1 connectivity (c_lever.log measured c1 only), so that concentration is
a selection artefact and cannot be quoted.  This samples configurations blind and
records (ell, c) for every valid level, which is the only way to see whether c=2
is really a shallow-level phenomenon.

It matters because the levels are not interchangeable: the DEEPEST level ell=n-1
is the one the l=1 ceiling law, the anchor theorem and Theorem S all work with,
while ell=1 is the shallowest and carries the largest count.  If c=2 lives only
at shallow levels, the deep-level results are untouched by it.
"""
import collections, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_level import level_graph, shares_plane, parse, engine

rnd = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 17)
N = int(sys.argv[2]) if len(sys.argv) > 2 else 500
tally = collections.Counter()
depth_of = collections.Counter()
for _ in range(N):
    n = rnd.choice((4, 4, 5, 5, 6))
    h = rnd.choice((3, 9, 30, 120))
    qs = [(1, 0, 0, 0)] + [tuple(rnd.randint(-h, h) for _ in range(4)) for _ in range(n - 1)]
    if any(not any(q) for q in qs):
        continue
    if shares_plane(qs) or max(abs(v) for q in qs for v in q) > 512:
        continue
    try:
        lv = level_graph(qs)
        e = engine(qs)
    except Exception:
        continue
    for ell in sorted(lv):
        g = lv[ell]
        d = e["by_depth"].get(str(ell), 0)
        if g["E"] - g["V"] + g["c"] + 1 != d:
            continue                       # identity fails -> not a measurement
        tally[(n, ell, g["c"])] += 1
        if g["c"] > 1:
            depth_of[("shallowest ell=1" if ell == 1 else
                      "deepest ell=n-1" if ell == n - 1 else "middle")] += 1

print("valid level-instances by (n, ell, c):")
tot = collections.Counter()
for k in sorted(tally):
    tot[(k[0], k[1])] += tally[k]
for k in sorted(tally):
    if k[2] > 1:
        print(f"  n={k[0]} ell={k[1]} c={k[2]} : {tally[k]}   "
              f"(of {tot[(k[0], k[1])]} at that (n,ell))")
allv = sum(tally.values())
c2 = sum(v for k, v in tally.items() if k[2] > 1)
print(f"\ntotal valid level-instances: {allv};  c>1: {c2} ({c2/allv:.2%})")
print("\nwhere the c>1 instances sit:")
for k, v in sorted(depth_of.items()):
    print(f"  {k:20s} {v}")
