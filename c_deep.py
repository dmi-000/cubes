#!/usr/bin/env python3
"""Capture the c>1 instances of the unbiased sweep, especially any at the DEEPEST
level ell = n-1.

That level is the one [P262]/[P263]'s chain uses: `d3 = V3(3)/2 + c3 + 1` gives
`W1 = 2(d3-2)` only when `c3 = 1`, and that step is [OQ 32].  The 32 previously
known c=2 configurations all showed c=2 at ell=1, but they were SELECTED on
depth-1 connectivity, so that told us nothing about the deep levels.  The blind
sweep found one at ell = n-1, which is why this rerun exists: to name it.

(The l=1 ceiling law and Theorem S are NOT affected -- they come from FIB plus the
anchor theorem, which never mention c_ell.  Only the Euler-identity chain does.)
"""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_level import level_graph, shares_plane, engine

rnd = random.Random(17)
for t in range(500):
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
            continue
        if g["c"] > 1:
            spec = ";".join(",".join(str(v) for v in q) for q in qs)
            deep = "  <-- DEEPEST LEVEL ell = n-1" if ell == n - 1 else ""
            print(f"n={n} ell={ell} c={g['c']} d_ell={d} total={e['bounded']} "
                  f"sizes={g['sizes']}{deep}", flush=True)
            print(f"   {spec}", flush=True)
