#!/usr/bin/env python3
"""[OQ 32] tested with W1 computed DIRECTLY, not through a void identification.

An earlier attempt (oq32_form.py) restated the question as `SUM(3-deg) >= 2(c-1)`
using W1 = the deepest level graph's vertex count V.  `w1_gate.py` refuted that
identification on 4 of 16 configurations -- V counts arc endpoints lying on cube
EDGES as well as triple points, so V is 44 at n=4 in every case measured while W1
varies (44, 40, 36).  The restatement and its 15 "violations" are withdrawn.

Here W1 and W0 come from the tagged triple points directly (v3_outer.triple_points):
a 3-body vertex is W_s when exactly s of the other cubes strictly contain it.  The
two things worth knowing are then separate:

  (a) does the chain's STEP hold?          W1 >= 2(d3 - 2)
  (b) does the chain's CONCLUSION hold?    W0 <= 84

(a) failing while (b) holds means the bound survives but the argument for it does
not -- which is exactly what [OQ 32] is.
"""
import collections, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_level import level_graph, shares_plane, parse, engine
from w1_gate import w1_direct

WITNESS = "1,0,0,0;76,86,80,-95;113,-103,44,-53;98,-87,23,53"
RECORD = "1,0,0,0;0,5,3,2;1,-4,-1,1;1,1,-1,-4"


def probe(qs):
    if len(qs) != 4 or shares_plane(qs):
        return None
    if max(abs(v) for q in qs for v in q) > 512:
        return None
    e = engine(qs)
    d3 = e["by_depth"].get("3", 0)
    W = w1_direct(qs)
    g = level_graph(qs).get(3)
    c3 = g["c"] if g else None
    return {"W0": W[0], "W1": W[1], "d3": d3, "c3": c3, "total": e["bounded"],
            "step": W[1] - 2 * (d3 - 2), "concl": 84 - W[0]}


for label, spec in (("n=4 record 183", RECORD), ("deep c=2 witness", WITNESS)):
    r = probe(parse(spec))
    print(f"{label:18s} W0={r['W0']:>3} W1={r['W1']:>3} d3={r['d3']:>3} c3={r['c3']} "
          f"| step W1-2(d3-2) = {r['step']:>3} {'OK' if r['step']>=0 else 'FAILS'}"
          f" | concl 84-W0 = {r['concl']:>3} {'OK' if r['concl']>=0 else 'FAILS'}")

print()
rnd = random.Random(53)
step_bad = concl_bad = n = 0
stepd = collections.Counter()
w0max = 0
worst = None
for _ in range(300):
    h = rnd.choice((3, 9, 30, 120))
    qs = [(1, 0, 0, 0)] + [tuple(rnd.randint(-h, h) for _ in range(4)) for _ in range(3)]
    if any(not any(q) for q in qs):
        continue
    try:
        r = probe(qs)
    except Exception:
        continue
    if not r:
        continue
    n += 1
    stepd[r["step"]] += 1
    w0max = max(w0max, r["W0"])
    if r["step"] < 0:
        step_bad += 1
        if worst is None or r["step"] < worst[0]:
            worst = (r["step"], r, ";".join(",".join(str(v) for v in q) for q in qs))
    if r["concl"] < 0:
        concl_bad += 1
print(f"blind non-degenerate n=4 configurations: {n}")
print(f"  STEP   W1 >= 2(d3-2)  fails in {step_bad}  ({step_bad/n:.1%})")
print(f"  CONCL  W0 <= 84       fails in {concl_bad}   (max W0 seen = {w0max})")
print(f"  step slack distribution: {dict(sorted(stepd.items()))}")
if worst:
    print(f"  worst step deficit {worst[0]}: W0={worst[1]['W0']} W1={worst[1]['W1']} "
          f"d3={worst[1]['d3']} c3={worst[1]['c3']}")
    print(f"    {worst[2]}")
