#!/usr/bin/env python3
"""The open link  W1 >= 2(d3-2)  restated EXACTLY, via the level-3 anatomy.

[P272]'s anatomy gives, at any level, d_ell = SUM_v (deg/2 - 1) + c + 1.  Split
the level-3 vertices into transversal triple points (degree 3, weight 1/2 each --
these are exactly W1) and two-body vertices (weight deg/2 - 1, so degree 2 counts
0, degree 4 counts 1, degree 6 counts 2).  Writing tau3 for the two-body weight,

    d3  =  W1/2 + tau3 + c3 + 1        =>        W1 = 2(d3 - tau3 - c3 - 1)

and therefore, since c3 >= 1 and tau3 >= 0,

    **W1 >= 2(d3 - 2)   <=>   tau3 + c3 <= 1   <=>   tau3 = 0 AND c3 = 1.**

So the last open link in W0 <= 84 is not a new inequality at all: it is the
conjunction of "the depth-3 level carries no two-body weight" and "the depth-3
level is connected".  [P243] already OBSERVED the first -- "at every level
ell >= 2 the two-body term is identically ZERO" -- on records and Haar draws.
The second is [OQ 30] restricted to the deepest level.

This measures both on the configurations where the link FAILS, which says which
of the two conjuncts is actually at risk.
"""
import collections, itertools, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_level import shares_plane, parse, engine, level_graph
from w0_anatomy import anatomy
from w1_gate import w1_direct


def tau_and_c(qs, ell):
    """(tau, c, W_at_level, breakdown) for the level-ell graph"""
    cls, deg, on = anatomy(qs, ell)
    g = level_graph(qs)[ell]
    tau = 0
    trip = 0
    detail = collections.Counter()
    for (bodies, d), cnt in cls.items():
        if bodies == 2:
            tau += cnt * (d // 2 - 1)
            detail[f"2-body deg{d}"] += cnt
        elif bodies == 3 and d == 3:
            trip += cnt
            detail["triple deg3"] += cnt
        else:
            detail[f"{bodies}-body deg{d}"] += cnt
    return tau, g["c"], trip, dict(detail)


def probe(qs):
    if shares_plane(qs) or max(abs(v) for q in qs for v in q) > 512:
        return None
    e = engine(qs)
    d3 = e["by_depth"].get("3", 0)
    W = w1_direct(qs)
    tau, c3, trip, detail = tau_and_c(qs, 3)
    return {"W1": W[1], "W0": W[0], "d3": d3, "tau3": tau, "c3": c3,
            "trip3": trip, "detail": detail,
            "identity_W1": 2 * (d3 - tau - c3 - 1),
            "step": W[1] - 2 * (d3 - 2)}


print("GATE:  W1 == 2(d3 - tau3 - c3 - 1)?   and   step >= 0 <=> tau3 + c3 <= 1?")
print(f"{'case':20s} {'W1':>4} {'pred':>5} {'d3':>4} {'tau3':>5} {'c3':>3} {'tau+c':>6} "
      f"{'step':>5}  consistent")
cases = [("n=4 record", "1,0,0,0;0,5,3,2;1,-4,-1,1;1,1,-1,-4"),
         ("deep c=2 witness", "1,0,0,0;76,86,80,-95;113,-103,44,-53;98,-87,23,53")]
rnd = random.Random(97)
for _ in range(10):
    qs = [(1, 0, 0, 0)] + [tuple(rnd.randint(-40, 40) for _ in range(4)) for _ in range(3)]
    if not any(not any(q) for q in qs) and not shares_plane(qs):
        cases.append(("random", ";".join(",".join(str(v) for v in q) for q in qs)))
bad = 0
for label, spec in cases:
    r = probe(parse(spec))
    if not r:
        continue
    idok = r["W1"] == r["identity_W1"]
    equiv = (r["step"] >= 0) == (r["tau3"] + r["c3"] <= 1)
    bad += not (idok and equiv)
    print(f"{label:20s} {r['W1']:>4} {r['identity_W1']:>5} {r['d3']:>4} {r['tau3']:>5} "
          f"{r['c3']:>3} {r['tau3']+r['c3']:>6} {r['step']:>5}  "
          f"{'OK' if idok and equiv else '*** MISMATCH ***'}")
print("\nIDENTITY AND EQUIVALENCE HOLD" if bad == 0 else f"\nFAILS on {bad}")
