#!/usr/bin/env python3
"""Directed attack on the exact form of W0 <= 84 ([P275]):

    maximise   LHS - RHS  =  [tau3 + (c3-1)]  -  [Ttau + gamma + S]

A violation needs LHS - RHS >= 1, i.e. a depth-3 anomaly that does NOT force
Theorem S slack or triple-level anomalies.  Observed so far: LHS at most 2, RHS
either 0 (only where W0 = 84 and everything vanishes) or at least 6.  So the
search is over a gap of at least 4 and it climbs the objective directly rather
than climbing W0 and hoping.

Seeded from the configurations that HAVE a depth-3 anomaly, since LHS = 0 makes
the objective hopeless from the start.
"""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_level import parse, shares_plane
from w0_exact import terms

SEEDS = ["1,0,0,0;-4,4,-6,5;1,-1,-5,2;1,4,6,3",
         "1,0,0,0;-3,-5,-1,2;4,-3,-5,2;-5,1,5,-2",
         "1,0,0,0;76,86,80,-95;113,-103,44,-53;98,-87,23,53",
         "1,0,0,0;0,5,3,2;1,-4,-1,1;1,1,-1,-4"]
rnd = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 7)
best_all = None
for spec in SEEDS:
    qs = parse(spec)
    r = terms(qs)
    if not r:
        continue
    best = (r["lhs"] - r["rhs"], qs, r)
    stall = 0
    while stall < 160:
        base = best[1]
        sc = rnd.choice((1, 1, 2, 3))
        cand = [base[0]] + [tuple(v * sc + rnd.randint(-2, 2) for v in q) for q in base[1:]]
        if any(not any(q) for q in cand) or shares_plane(cand):
            stall += 1
            continue
        try:
            rr = terms(cand)
        except Exception:
            stall += 1
            continue
        if rr and rr["lhs"] - rr["rhs"] > best[0]:
            best = (rr["lhs"] - rr["rhs"], cand, rr)
            stall = 0
        else:
            stall += 1
    v, qs2, rr = best
    print(f"seed {spec[:30]:30s} -> best LHS-RHS = {v:>4}  "
          f"(LHS={rr['lhs']} RHS={rr['rhs']}, W0={rr['W0']})", flush=True)
    print(f"     {';'.join(','.join(str(x) for x in q) for q in qs2)}", flush=True)
    if best_all is None or v > best_all[0]:
        best_all = (v, rr, qs2)
print(f"\nBEST LHS-RHS FOUND: {best_all[0]}   (a violation of W0<=84 needs >= 1)")
print(f"  W0 there = {best_all[1]['W0']}")
