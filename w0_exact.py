#!/usr/bin/env python3
"""The EXACT accounting for W0 -- no inequalities, so nothing is thrown away.

[P274] bounded W0 by relaxing two things: V3(T) <= 2(d2(T)-2) and Theorem S.  Keep
both as identities instead and every term survives:

    V3(T) = 2(d2(T) - tau2(T) - c2(T) - 1)          [anatomy, triple's deep level]
    W1    = 2(d3 - tau3 - c3 - 1)                   [anatomy, ell = 3]
    d3    = SUM_T d2(T) - 48 + S,   S >= 0          [Theorem S slack, PROVED >= 0]
    W0    = budget - W1

Substituting, with  gamma = SUM_T (c2(T) - 1) >= 0  and  Ttau = SUM_T tau2(T) >= 0:

    **  W0  =  84  +  2[ tau3 + (c3 - 1) ]  -  2[ Ttau + gamma + S ]  **

so, exactly and with no slack discarded,

    **  W0 <= 84   <=>   tau3 + (c3 - 1)  <=  Ttau + gamma + S.  **

The depth-3 anomalies must be dominated by the TRIPLES' own anomalies plus the
Theorem S slack.  Both sides are >= 0 and every term is directly measurable, so
this is checkable rather than conjectural, and it says exactly which quantity has
to pay when depth 3 misbehaves.

Gated below: the identity must reproduce W0 exactly, and V3(T) = 2(d2(T)-tau2-c2-1)
must hold, before any of it is used.
"""
import collections, itertools, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_level import shares_plane, parse, engine
from w1_tau import tau_and_c
from w1_gate import w1_direct


def terms(qs):
    if shares_plane(qs) or max(abs(v) for q in qs for v in q) > 512:
        return None
    e = engine(qs)
    d3 = e["by_depth"].get("3", 0)
    W = w1_direct(qs)
    tau3, c3, trip3, _ = tau_and_c(qs, 3)
    Ttau = gamma = sumd2 = budget = 0
    per = []
    for T in itertools.combinations(range(4), 3):
        sub = [qs[i] for i in T]
        es = engine(sub)
        d2T = es["by_depth"].get("2", 0)
        t2, c2, trip2, _ = tau_and_c(sub, 2)
        v3T = w1_direct(sub)[0]
        Ttau += t2
        gamma += c2 - 1
        sumd2 += d2T
        budget += v3T
        per.append((d2T, t2, c2, v3T, 2 * (d2T - t2 - c2 - 1)))
    S = d3 - (sumd2 - 48)
    return {"W0": W[0], "W1": W[1], "budget": budget, "d3": d3, "sumd2": sumd2,
            "tau3": tau3, "c3": c3, "Ttau": Ttau, "gamma": gamma, "S": S, "per": per,
            "pred": 84 + 2 * (tau3 + c3 - 1) - 2 * (Ttau + gamma + S),
            "lhs": tau3 + (c3 - 1), "rhs": Ttau + gamma + S}


CASES = [("record", "1,0,0,0;0,5,3,2;1,-4,-1,1;1,1,-1,-4"),
         ("tau3=2 (simple)", "1,0,0,0;-4,4,-6,5;1,-1,-5,2;1,4,6,3"),
         ("tau3=2 (simple)", "1,0,0,0;-3,-5,-1,2;4,-3,-5,2;-5,1,5,-2"),
         ("c3=2 witness", "1,0,0,0;76,86,80,-95;113,-103,44,-53;98,-87,23,53"),
         ("W0=84 non-record", "1,0,0,0;-3,-19,-8,-23;-26,-10,-23,-2;-12,-11,-5,-26")]
rnd = random.Random(211)
for _ in range(8):
    qs = [(1, 0, 0, 0)] + [tuple(rnd.randint(-40, 40) for _ in range(4)) for _ in range(3)]
    if not any(not any(q) for q in qs) and not shares_plane(qs):
        CASES.append(("random", ";".join(",".join(str(v) for v in q) for q in qs)))

print("GATE 1: V3(T) == 2(d2(T) - tau2 - c2 - 1) for each triple")
print("GATE 2: W0 == 84 + 2[tau3+(c3-1)] - 2[Ttau+gamma+S]")
print()
print(f"{'case':18s} {'W0':>4} {'pred':>5} {'tau3':>5} {'c3':>3} {'Ttau':>5} {'gam':>4} "
      f"{'S':>3} {'LHS':>4} {'RHS':>4}  dominates  gates")
bad1 = bad2 = 0
for label, spec in CASES:
    r = terms(parse(spec))
    if not r:
        continue
    g1 = all(v3 == pred for _, _, _, v3, pred in r["per"])
    g2 = r["W0"] == r["pred"]
    bad1 += not g1
    bad2 += not g2
    print(f"{label:18s} {r['W0']:>4} {r['pred']:>5} {r['tau3']:>5} {r['c3']:>3} "
          f"{r['Ttau']:>5} {r['gamma']:>4} {r['S']:>3} {r['lhs']:>4} {r['rhs']:>4}  "
          f"{'YES' if r['lhs'] <= r['rhs'] else '*** NO ***':10s} "
          f"{'ok' if g1 and g2 else ('V3!' if not g1 else '') + ('W0!' if not g2 else '')}")
print(f"\nGATE 1 failures: {bad1}   GATE 2 failures: {bad2}")
