#!/usr/bin/env python3
"""Re-test [OQ 32]'s step on SIMPLE configurations -- [P271]'s rate may be an artefact.

w0_anatomy.py showed the worst step failure (-16) has EIGHT 4-body vertices and
four triple points of degree 6: four cube boundaries meeting at a point, and three
meeting non-transversally.  Neither involves a shared face plane, so `shares_plane`
-- the only genericity filter [P271] used -- passes them.

That is FAILURE_MODES 31 again, in the same session that recorded it: integer
sampling lands on rational coincidence loci with positive probability, and
[P271]'s pool was drawn at heights 3, 9, 30, 120 where low heights are dense in
them.  So "fails on 6.9 % of GENERIC configurations" may be measuring the pool.

SIMPLE here means: every vertex of every level graph lies on exactly 2 or 3 cube
boundaries, and every 3-body vertex has degree 3.  That is the transversality the
formula `V3 = 2(d-2)` actually assumes.  The step is re-measured on simple and
non-simple configurations separately, so the answer cannot hide in the average.
"""
import collections, itertools, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_level import shares_plane, parse, engine, level_graph
from w1_gate import w1_direct
from w0_anatomy import anatomy


def is_simple(qs):
    n = len(qs)
    for ell in range(1, n):
        cls, deg, on = anatomy(qs, ell)
        for (bodies, d), cnt in cls.items():
            if bodies >= 4:
                return False
            if bodies == 3 and d != 3:
                return False
    return True


def probe(qs):
    if shares_plane(qs) or max(abs(v) for q in qs for v in q) > 512:
        return None
    e = engine(qs)
    d3 = e["by_depth"].get("3", 0)
    W = w1_direct(qs)
    return {"W0": W[0], "W1": W[1], "d3": d3,
            "step": W[1] - 2 * (d3 - 2), "concl": 84 - W[0], "total": e["bounded"]}


rnd = random.Random(53)
res = collections.defaultdict(lambda: {"n": 0, "stepbad": 0, "conclbad": 0,
                                       "w0max": 0, "worst": 0})
for _ in range(300):
    h = rnd.choice((3, 9, 30, 120))
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
    b = res["SIMPLE" if simple else "coincident"]
    b["n"] += 1
    b["stepbad"] += r["step"] < 0
    b["conclbad"] += r["concl"] < 0
    b["w0max"] = max(b["w0max"], r["W0"])
    b["worst"] = min(b["worst"], r["step"])

print("re-test of  W1 >= 2(d3-2)  and  W0 <= 84,  split by SIMPLICITY")
print(f"{'class':12s} {'n':>4} {'step fails':>11} {'concl fails':>12} {'max W0':>7} {'worst step':>11}")
for k in ("SIMPLE", "coincident"):
    b = res[k]
    if not b["n"]:
        continue
    print(f"{k:12s} {b['n']:>4} {b['stepbad']:>11} {b['conclbad']:>12} "
          f"{b['w0max']:>7} {b['worst']:>11}")
