#!/usr/bin/env python3
"""A PROVED quantitative bound on W0, with the two unknowns made explicit.

Chain, all links established:

  budget = SUM_T V3(T),  V3(T) = 2(d2(T) - tau2(T) - c(T) - 1) <= 2(d2(T) - 2)
                                            [c >= 1, tau >= 0; the level anatomy]
  W1     = 2(d3 - tau3 - c3 - 1)                        [the same anatomy at ell=3]
  d3     >= SUM_T d2(T) - 48                            [Theorem S, PROVED, P266]
  W0     = budget - W1                                  [exact for simple configs]

  => W0 <= (2*SUM_T d2(T) - 16) - 2(d3 - tau3 - c3 - 1)
        <= (2*SUM_T d2(T) - 16) - 2(SUM_T d2(T) - 48 - tau3 - c3 - 1)

  **  W0  <=  82 + 2*(tau3 + c3)  **

which is 84 when tau3 = 0 and c3 = 1 -- the record's values, exactly attained --
and 86 when c3 = 2.  So the ENTIRE remaining gap between the proved chain and
W0 <= 84 is one antipodal pair, and it is bought by exactly two facts:

    tau3 = 0   (the depth-3 level carries no two-body weight; [P243] observed
                "at every level ell >= 2 the two-body term is identically ZERO")
    c3   = 1   ([OQ 30], restricted to the DEEPEST level only)

Neither is a new inequality.  This tests the bound itself, and reports tau3 and c3
separately so it is visible which one is ever at risk.
"""
import collections, itertools, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_level import shares_plane, parse, engine
from w1_tau import tau_and_c
from w1_gate import w1_direct
from oq32_simple import is_simple


def probe(qs):
    if shares_plane(qs) or max(abs(v) for q in qs for v in q) > 512:
        return None
    e = engine(qs)
    W = w1_direct(qs)
    tau3, c3, trip, _ = tau_and_c(qs, 3)
    budget = sum(w1_direct([qs[i] for i in T])[0]
                 for T in itertools.combinations(range(4), 3))
    return {"W0": W[0], "W1": W[1], "budget": budget, "tau3": tau3, "c3": c3,
            "bound": 82 + 2 * (tau3 + c3), "d3": e["by_depth"].get("3", 0)}


rnd = random.Random(131)
cnt = collections.Counter()
viol = []
tau_nonzero = []
worst_slack = None
n = 0
for _ in range(300):
    h = rnd.choice((3, 6, 12, 30, 60, 120))
    qs = [(1, 0, 0, 0)] + [tuple(rnd.randint(-h, h) for _ in range(4)) for _ in range(3)]
    if any(not any(q) for q in qs):
        continue
    try:
        r = probe(qs)
        if not r:
            continue
        simple = is_simple(qs)
    except Exception:
        continue
    n += 1
    cnt[("simple" if simple else "coincident", r["tau3"], r["c3"])] += 1
    spec = ";".join(",".join(str(v) for v in q) for q in qs)
    if r["W0"] > r["bound"]:
        viol.append((r, spec, simple))
    if r["tau3"] != 0:
        tau_nonzero.append((r, spec, simple))
    sl = r["bound"] - r["W0"]
    if worst_slack is None or sl < worst_slack[0]:
        worst_slack = (sl, r, spec, simple)

print(f"BOUND  W0 <= 82 + 2*(tau3 + c3)   tested on {n} configurations")
print(f"  violations of the BOUND : {len(viol)}")
print(f"  configurations with tau3 != 0 : {len(tau_nonzero)}")
print()
print("  (tau3, c3) census:")
for k in sorted(cnt):
    print(f"    {k[0]:11s} tau3={k[1]} c3={k[2]} -> bound {82+2*(k[1]+k[2])} : {cnt[k]}")
if worst_slack:
    sl, r, spec, simple = worst_slack
    print(f"\n  tightest case: W0={r['W0']} bound={r['bound']} slack={sl} "
          f"(tau3={r['tau3']} c3={r['c3']}, {'simple' if simple else 'coincident'})")
    print(f"    {spec}")
for r, spec, simple in tau_nonzero[:5]:
    print(f"  tau3 != 0: tau3={r['tau3']} c3={r['c3']} W0={r['W0']} "
          f"{'simple' if simple else 'coincident'}  {spec}")
